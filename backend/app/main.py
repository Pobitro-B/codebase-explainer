from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from app.services.scanner import root_scan
from app.services.filereader import file_contents
from app.services.graphbuilder import build_graph
from app.services.explainer import file_explain, llm_call
from app.services.repoexplainer import repo_explain
from app.services.reposearch import repo_search
from app.services.chatutils import build_chat_prompt


class ScanRequest(BaseModel):
    path: str


class ReadRequest(BaseModel):
    path: str


class ContextRequest(BaseModel):
    path: str


class ExplainRequest(BaseModel):
    file: str
    content: str
    language: str
    dependencies: list
    dependents: list
    imports: list
    symbols: list
    structure: list


class SearchRequest(BaseModel):
    query: str


class ChatRequest(BaseModel):
    message: str


CURRENT_PROJECT = {}

app = FastAPI()

origins = [
    "http://localhost:5173",  # Common React/Vue dev port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,  # Allows cookies and headers
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/health")
def health_check():
    return {"status": "backend alive"}


@app.post("/scan-repo")
async def read_root(req: ScanRequest):
    global CURRENT_PROJECT
    tree = root_scan(req.path)
    graphData = build_graph(tree, req.path)
    graph = graphData["graph"]
    analysis_cache = graphData["analysis"]
    CURRENT_PROJECT = {
        "tree": tree,
        "graph": graph,
        "analysis": analysis_cache,
        "summaries": {},
        "chat_history": [],
    }
    return {
        "tree": tree,
        "graph": graph,
    }


@app.get("/explain-repo")
async def explain_repo():
    CURRENT_PROJECT["repo_explanation"] = repo_explain(CURRENT_PROJECT)
    return CURRENT_PROJECT["repo_explanation"]


@app.post("/read-file")
async def read_file(req: ReadRequest):
    return file_contents(req.path)


@app.post("/file-context")
async def file_context_builder(req: ContextRequest):
    if not CURRENT_PROJECT:
        return {"error": "No repository loaded"}
    file_analysis = CURRENT_PROJECT["analysis"].get(req.path, {})
    file_data = file_contents(req.path)
    return {
        "file": req.path,
        "content": "".join(file_data["content"]),
        "language": file_data["language"],
        "dependencies": CURRENT_PROJECT["graph"]["dependencies"].get(req.path, []),
        "dependents": CURRENT_PROJECT["graph"]["dependents"].get(req.path, []),
        "imports": file_analysis.get("imports", []),
        "symbols": file_analysis.get("symbols", []),
        "structure": file_analysis.get("structure", []),
    }


@app.post("/explain-file")
async def explain_file(req: ExplainRequest):
    dependency_context = []
    dependent_context = []
    for dep in req.dependencies:
        analysis = CURRENT_PROJECT["analysis"].get(dep, {})
        dependency_context.append(
            {
                "file": dep,
                "symbols": analysis.get("symbols", []),
                "structure": analysis.get("structure", []),
            }
        )
    for dep in req.dependents:
        analysis = CURRENT_PROJECT["analysis"].get(dep, {})
        dependent_context.append(
            {
                "file": dep,
                "symbols": analysis.get("symbols", []),
                "structure": analysis.get("structure", []),
            }
        )
    context = req.model_dump()
    context["dependency_context"] = dependency_context
    context["dependent_context"] = dependent_context
    CURRENT_PROJECT["summaries"][req.file] = file_explain(context)["explanation"]
    return {"explanation": CURRENT_PROJECT["summaries"][req.file]}


@app.post("/search")
async def search_repo(req: SearchRequest):
    return {"results": repo_search(req.query, CURRENT_PROJECT)}


@app.post("/chat")
async def chat_repo(req: ChatRequest):
    context = {
        "repo_summary": CURRENT_PROJECT["repo_explanation"],
        "file_summaries": CURRENT_PROJECT["summaries"],
        "chat_history": CURRENT_PROJECT["chat_history"][-10::],
        "question": req.message,
    }
    CURRENT_PROJECT["chat_history"].append({"role":"user", "content":req.message})
    prompt = build_chat_prompt(context)
    response = llm_call(prompt)
    CURRENT_PROJECT["chat_history"].append({"role": "assistant", "content": response})
    return {"response": response}
