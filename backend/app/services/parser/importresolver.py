import os
import re
import importlib.util
from pathlib import Path

from tree_sitter_language_pack import (
    process,
    ProcessConfig,
    get_parser,
)


# =========================================================
# Parser Loader
# =========================================================

def get_language_parser(language: str):
    try:
        return get_parser(language)
    except Exception:
        return None


# =========================================================
# Python Resolver
# =========================================================

def resolve_python_import(
    raw: str,
    base_dir: str,
    project_root: str,
) -> str | None:
    """
    Resolve Python imports to absolute file paths.

    Examples:
        import os
        import app.utils.parser
        from pathlib import Path
        from app.services.parser import extract
    """

    module = None

    # -----------------------------------------
    # import x
    # import x as y
    # -----------------------------------------

    if raw.startswith("import "):
        module = raw.replace("import ", "").split(" as ")[0].strip()

    # -----------------------------------------
    # from x import y
    # -----------------------------------------

    elif raw.startswith("from "):
        module = raw.split(" import ")[0].replace("from ", "").strip()

    if not module:
        return None

    # -----------------------------------------
    # Relative imports
    # from .utils import x
    # from ..core import y
    # -----------------------------------------

    if module.startswith("."):
        relative_level = len(module) - len(module.lstrip("."))

        relative_module = module.lstrip(".")

        parent_dir = Path(base_dir)

        for _ in range(relative_level):
            parent_dir = parent_dir.parent

        parts = relative_module.split(".") if relative_module else []

        candidates = [
            parent_dir.joinpath(*parts).with_suffix(".py"),
            parent_dir.joinpath(*parts, "__init__.py"),
        ]

        for candidate in candidates:
            if candidate.exists():
                return str(candidate.resolve())

        return None

    # -----------------------------------------
    # Project-local imports
    # app.services.parser
    # -----------------------------------------

    parts = module.split(".")

    candidates = [
        Path(project_root).joinpath(*parts).with_suffix(".py"),
        Path(project_root).joinpath(*parts, "__init__.py"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return str(candidate.resolve())

    # -----------------------------------------
    # Stdlib / Installed packages
    # pathlib
    # numpy
    # fastapi
    # -----------------------------------------

    try:
        spec = importlib.util.find_spec(parts[0])

        if spec and spec.origin:
            return spec.origin

    except Exception:
        pass

    return None


# =========================================================
# JS / TS Resolver
# =========================================================

def resolve_js_import(
    raw: str,
    base_dir: str,
    project_root: str,
) -> str | None:
    """
    Resolve JS/TS imports.

    Examples:
        import x from "./foo"
        import y from "../utils/bar"
        import React from "react"
        import "./App.css"
    """

    match = re.search(r'["\'](.+?)["\']', raw)

    if not match:
        return None

    import_path = match.group(1)

    # -----------------------------------------
    # External packages
    # -----------------------------------------

    if not import_path.startswith("."):
        return f"node_modules/{import_path}"

    # -----------------------------------------
    # Relative imports
    # -----------------------------------------

    extensions = [
        "",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".json",
        ".css",
        "/index.js",
        "/index.ts",
        "/index.tsx",
    ]

    for ext in extensions:
        candidate = Path(base_dir) / f"{import_path}{ext}"

        if candidate.exists():
            return str(candidate.resolve())

    return None


# =========================================================
# Rust Resolver
# =========================================================

def resolve_rust_import(
    raw: str,
    base_dir: str,
    project_root: str,
) -> str | None:
    """
    Resolve Rust imports.

    Examples:
        use crate::utils::parser;
        use std::collections::HashMap;
    """

    if raw.startswith("use "):
        raw = raw.replace("use ", "").replace(";", "").strip()

    # -----------------------------------------
    # crate::
    # -----------------------------------------

    if raw.startswith("crate::"):
        parts = raw[len("crate::"):].split("::")

        candidates = [
            Path(project_root) / "src" / Path(*parts).with_suffix(".rs"),
            Path(project_root) / "src" / Path(*parts) / "mod.rs",
        ]

        for candidate in candidates:
            if candidate.exists():
                return str(candidate.resolve())

    return None


# =========================================================
# Resolver Registry
# =========================================================

RESOLVERS = {
    "python": resolve_python_import,
    "javascript": resolve_js_import,
    "typescript": resolve_js_import,
    "tsx": resolve_js_import,
    "rust": resolve_rust_import,
}


# =========================================================
# Generic Resolver Dispatcher
# =========================================================

def resolve_import(
    language: str,
    raw: str,
    base_dir: str,
    project_root: str,
) -> str | None:

    resolver = RESOLVERS.get(language)

    if not resolver:
        return None

    return resolver(raw, base_dir, project_root)


# =========================================================
# Main Extractor
# =========================================================

def extract(
    language: str,
    content_chunk: str,
    base_dir: str = ".",
    project_root: str = ".",
) -> dict:

    analysis = {
        "imports": [],
        "structure": [],
        "symbols": [],
    }
    
    if language not in RESOLVERS.keys():
        return analysis
    # -----------------------------------------
    # Parse + Analyze
    # -----------------------------------------

    result = process(
        content_chunk,
        ProcessConfig(
            language=language,
            imports=True,
            structure=True,
            exports=True,
            symbols=True,
        ),
    )

    # =====================================================
    # Imports
    # =====================================================

    for imp in result.imports:

        raw = imp.source

        analysis["imports"].append({
            "raw": raw,
            "resolved_path": resolve_import(
                language=language,
                raw=raw,
                base_dir=base_dir,
                project_root=project_root,
            ),
            "items": imp.items,
            "alias": imp.alias,
            "is_wildcard": imp.is_wildcard,
            "span": {
                "start_line": imp.span.start_line,
                "end_line": imp.span.end_line,
            },
        })

    # =====================================================
    # Structure
    # =====================================================

    for item in result.structure:

        analysis["structure"].append({
            "kind": str(item.kind),
            "name": item.name,
            "visibility": item.visibility,
            "signature": item.signature,
            "decorators": item.decorators,
            "doc_comment": item.doc_comment,
            "span": {
                "start_line": item.span.start_line,
                "end_line": item.span.end_line,
            },
        })

    # =====================================================
    # Symbols
    # =====================================================

    for symbol in result.symbols:

        analysis["symbols"].append({
            "name": symbol.name,
            "kind": str(symbol.kind),
            "type_annotation": symbol.type_annotation,
            "doc": symbol.doc,
            "span": {
                "start_line": symbol.span.start_line,
                "end_line": symbol.span.end_line,
            },
        })

    return analysis