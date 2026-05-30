from app.services.filereader import file_contents


def build_graph(tree, project_root):
    dependents = {}
    dependencies = {}
    nodes = set()
    analysis_cache = {}
    queue = [tree]
    while queue:
        node = queue.pop()
        if node["type"] == "directory":
            queue.extend(node["children"])
            continue
        file_path = node["path"]
        nodes.add(file_path)
        file_data = file_contents(file_path)
        analysis_cache[file_path] = file_data["analysis"]
        imports = file_data["imports"]
        dependencies.setdefault(file_path, [])
        dependents.setdefault(file_path, [])
        for imp in imports:
            resolved = imp["resolved_path"]
            if not resolved:
                continue
            if not resolved.startswith(project_root):
                continue
            dependencies[file_path].append(resolved)
            dependents.setdefault(resolved, [])
            dependents[resolved].append(file_path)
    return {
        "graph": {
            "nodes": list(nodes),
            "dependencies": dependencies,
            "dependents": dependents,
        },
        "analysis": analysis_cache,
    }
