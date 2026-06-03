from pathlib import Path


def repo_search(keywords, CURRENT_PROJECT):
    query = keywords.lower()
    tokens = query.split()
    nodes = CURRENT_PROJECT["graph"]["nodes"]
    analysis = CURRENT_PROJECT["analysis"]
    scores = {}
    for file in nodes:
        score = 0
        filename = Path(file).name.lower()
        stem = Path(file).stem.lower()
        if query == stem:
            score += 100
        elif query in filename:
            score += 20
        file_analysis = analysis.get(file, {})
        for token in tokens:
            if token in filename:
                score += 10
            for symbol in file_analysis.get("symbols", []):
                if token in str(symbol).lower():
                    score += 5
            for structure in file_analysis.get("structure", []):
                if token in str(structure).lower():
                    score += 3
            for imp in file_analysis.get("imports", []):
                if token in str(imp).lower():
                    score += 2
        if score > 0:
            scores[file] = score
    results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]

    returnPart = [
        {
            "path": path,
            "name": Path(path).name,
            "score": score,
        }
        for path, score in results
    ]
    return returnPart
