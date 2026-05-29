from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
from app.static.extensions import EXTENSION_MAP

def file_contents(path: str):
    """_summary_

    Args:
        path (str): _description_

    Returns:
        _type_: _description_
    """
    if path == "HOME_PAGE":
        path = "./app/static/home.txt"
    PY_LANGUAGE = Language(tspython.language())
    parser = Parser(PY_LANGUAGE)
    with open(Path(path).resolve(), "r", encoding='utf-8') as f:
        content = f.readlines()
    contentChunk = ''.join(content)
    tree = parser.parse(bytes(contentChunk,"utf8"))
    root = tree.root_node
    imports = []
    for child in root.children:
        if child.type == "import_from_statement" or child.type == "import_statement":
            module = None
            importName = []
            alias = None
            for c in child.children:
                if c.type == "dotted_name":
                    if module is None:
                        module = c.text.decode()
                    else:
                        importName.append(c.text.decode())
                if c.type == "aliased_import":
                    for sub in c.children:
                        if sub.type == "dotted_name":
                            module = sub.text.decode()
                        if sub.type == "identifier":
                            alias = sub.text.decode()
            if alias:
                imports.append({
                    "type":"alias_import",
                    "module": module,
                    "alias": alias,
                })
            elif importName == []:
                imports.append({
                    "type":"import",
                    "module":module})
            else:
                imports.append({
                    "type":"from_import",
                    "module":module,
                    "import": importName
                })
    try:
        lang = EXTENSION_MAP[Path(path).name.split(".")[-1]]
    except(KeyError):
        lang = "text"    
    return {
        "name": Path(path).name,
        "path": path,
        "content": content,
        "language": lang,
        "imports": imports
    }

file_contents("./app/services/filereader.py")