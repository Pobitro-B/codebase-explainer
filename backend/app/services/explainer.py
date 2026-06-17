import requests
import json
from app.config import OPENROUTER_API_KEY


def build_prompt(context):
    return f"""
You are a senior software architect.

Analyze the following file in the context of its codebase.

FILE:
{context["file"]}

LANGUAGE:
{context["language"]}

DEPENDENCIES:
{context["dependencies"]}

DEPENDENTS:
{context["dependents"]}

STRUCTURE:
{context["structure"]}

SOURCE:
{context["content"]}

IMPORTS:
{context["imports"]}

SYMBOLS:
{context["symbols"]}

DEPENDENCY_CONTEXT:
{context["dependency_context"]}

DEPENDENT_CONTEXT:
{context["dependent_context"]}

Provide:

1. High-level purpose
2. Role in the architecture
3. Key functions/classes and what they do
4. Dependency relationships
5. Important implementation details
6. Potential issues or improvements

Be concise but technically accurate.
Do not suggest improvements unless there is a clear issue.
Focus on explaining what the file currently does.
"""


def llm_call(content):
    print("llm called")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": "openai/gpt-oss-120b:free",
                "messages": [{"role": "user", "content": content}],
                "reasoning": {"enabled": True},
            }
        ),
    )

    response = response.json()
    print("llm call finished")
    if "choices" in response:
        response = response["choices"][0]["message"]["content"]
    else:
        response = f"LLM Error: {response}"
        print(response)
    return response

def file_explain(context):
    response = llm_call(build_prompt(context))
    return {"explanation": response}
