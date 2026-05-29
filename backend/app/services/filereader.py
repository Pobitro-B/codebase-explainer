from pathlib import Path
from app.static.extensions import EXTENSION_MAP
from app.services.parser.importresolver import extract
from tree_sitter_language_pack import process, ProcessConfig

def file_contents(path: str):
    """_summary_

    Args:
        path (str): _description_

    Returns:
        _type_: _description_
    """
    if path == "HOME_PAGE":
        path = "./app/static/home.txt"
    with open(Path(path).resolve(), "r", encoding='utf-8') as f:
        content = f.readlines()
    contentChunk = ''.join(content)
    extension = Path(path).suffix.replace(".", "")
    language = EXTENSION_MAP.get(extension, "text")
    analysis = extract(
        language=language,
        content_chunk=contentChunk,
        base_dir=str(Path(path).resolve().parent),
        project_root=str(Path.cwd()),
    )
    return {
        "name": Path(path).name,
        "path": path,
        "content": content,
        "language": language,
        "analysis": analysis,
        "imports": analysis["imports"]
    }

(file_contents("./app/services/filereader.py"))