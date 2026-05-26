from pathlib import Path

IGNORE_DIRS = set(["node_modules", ".git", "target", "venv", "back-env", "__pycache__", "build", "dist", ".cache", ".env", ".next", ".idea"])
def root_scan(path: str, root=None):
    """_summary_

    Args:
        path (str): _description_
        root (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    res = {}
    p = Path(path)
    res["name"] = p.name
    res["type"] = "directory"
    res["path"] = str((Path(path).resolve())) if not root else str((Path(path).resolve()).relative_to(Path(root).resolve()))
    res["children"] = []
    if root is None:
        root = path
    for entry in p.iterdir():
        if entry.name in IGNORE_DIRS:
            continue
        elif entry.is_dir():
            rc = root_scan(str((Path(path) / entry.name).resolve()), root)
            res["children"].append(rc)
        else:
            res["children"].append({
                "name":entry.name,
                "type":"file",
                "path": str((Path(path) / entry.name).resolve().relative_to(Path(root).resolve()))
            })
    return res