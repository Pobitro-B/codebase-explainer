from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from app.services.scanner import root_scan
from app.services.filereader import file_contents
from app.services.graphbuilder import build_graph


class ScanRequest(BaseModel):
    path: str


class ReadRequest(BaseModel):
    path: str


class ContextRequest(BaseModel):
    path: str


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
    CURRENT_PROJECT = {"tree": tree, "graph": graph, "analysis": analysis_cache}
    return {
        "tree": tree,
        "graph": graph,
    }


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
