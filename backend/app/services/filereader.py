from pathlib import Path

def file_contents(path: str):
    """_summary_

    Args:
        path (str): _description_

    Returns:
        _type_: _description_
    """
    if path == "HOME_PAGE":
        path = "./app/static/home.txt"
    print(Path(path).resolve())
    with open(Path(path).resolve(), "r", encoding='utf-8') as f:
        content = f.readlines()
    return {
        "name": Path(path).name,
        "path": path,
        "content": content
    }
