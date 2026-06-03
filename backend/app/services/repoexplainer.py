import requests
import json
from app.config import OPENROUTER_API_KEY


def build_repo_prompt(context):
    return f"""
You are a senior software architect.

Analyze this repository.

TREE:
{context["tree"]}

GRAPH:
{context["graph"]}

ANALYSIS:
{context["analysis"]}

Provide:

# Executive Summary
Explain what this project does in 2-3 paragraphs.

# How It Works
Walk through the user flow from start to finish.

# Architecture
Explain the major subsystems and how they interact.

# Important Files
List the most important files a new developer should read first and why.

# Data Flow
Explain how data moves through the application.

# Dependency Graph Insights
Identify the most central files and modules.

# Potential Risks
Point out architectural weaknesses, tight coupling, missing abstractions, or scaling concerns.

# Suggestions
Recommend improvements.
"""


def repo_explain(context):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": "openai/gpt-oss-120b:free",
                "messages": [{"role": "user", "content": build_repo_prompt(context)}],
                "reasoning": {"enabled": True},
            }
        ),
    )

    response = response.json()
    #print(response)
    response = response["choices"][0]["message"]["content"]
    return {"explanation": response}
