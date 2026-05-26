from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from app.services.scanner import root_scan

class ScanRequest(BaseModel):
    path: str

app = FastAPI()

origins = [
    "http://localhost:5173",  # Common React/Vue dev port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows specific origins
    allow_credentials=True,           # Allows cookies and headers
    allow_methods=["*"],               # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],               # Allows all headers
)

@app.get("/health")
def health_check():
    return {"status": "backend alive"}

@app.post("/scan-repo")
async def read_root(req: ScanRequest):
    return root_scan(req.path)