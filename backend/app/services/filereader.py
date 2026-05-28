from pathlib import Path

EXTENSION_MAP = {
  # Web
  "js": "javascript",
  "mjs": "javascript",
  "cjs": "javascript",
  "jsx": "javascriptreact",

  'ts': "typescript",
  "tsx": "typescriptreact",

  "html": "html",
  "css": "css",
  "scss": "scss",
  "svelte": "svelte",
  "vue": "vue",

  # Backend
  "py": "python",
  "java": "java",
  "go": "go",
  "rs": "rust",
  "php": "php",
  "rb": "ruby",

  # Systems
  "c": "c",
  "h": "c",
  "cpp": "cpp",
  "cc": "cpp",
  "cxx": "cpp",
  "hpp": "cpp",

  "cs": "csharp",

  # Mobile
  "kt": "kotlin",
  "swift": "swift",
  "dart": "dart",

  # Scripting
  "sh": "bash",
  "bash": "bash",
  "zsh": "bash",
  "ps1": "powershell",

  # Data / Config
  "json": "json",
  "yaml": "yaml",
  "yml": "yaml",
  "toml": "toml",
  "xml": "xml",

  # Markup
  "md": "markdown",

  # SQL
  "sql": "sql",

  # Functional
  "hs": "haskell",
  "clj": "clojure",
  "scm": "scheme",
  "lisp": "lisp",

  # Misc
  "lua": "lua",
  'r': "r",
  "scala": "scala",
  "pl": "perl",

  # Notebooks
  "ipynb": "json",
  "txt": "text",
}

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
    try:
        lang = EXTENSION_MAP[Path(path).name.split(".")[-1]]
    except(KeyError):
        lang = "text"    
    return {
        "name": Path(path).name,
        "path": path,
        "content": content,
        "language": lang
    }
