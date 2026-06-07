# Codebase Explainer

Codebase Explainer is an AI-powered desktop application that helps developers understand unfamiliar codebases through repository visualization, semantic search, dependency analysis, and natural-language explanations.

Built with **React**, **Tauri**, **FastAPI**, **Tree-sitter**, and **OpenRouter**, the application allows users to open any local repository, explore its structure, search across files, and generate AI explanations for individual files or entire projects.

---

## Features

### Repository Scanning
- Recursively scans a selected project directory
- Detects supported source code files
- Reads file contents and extracts import relationships
- Builds a dependency graph representing file interactions

### Interactive File Explorer
- Visual tree view of the repository structure
- Expand and collapse folders
- Quickly navigate large projects

### Dependency Graph Generation
- Automatically identifies imports between files
- Constructs a directed dependency graph
- Provides a structural overview of the codebase

### Code Search
- Search for files, symbols, or text across the repository
- Fast repository-wide lookup
- Jump directly to relevant files

### AI File Explanations
- Generate natural-language explanations for any file
- Understand:
  - Purpose
  - Responsibilities
  - Key functions
  - Important classes
  - Data flow
  - Dependencies

### AI Repository Summaries
- Generate high-level project overviews
- Understand:
  - Architecture
  - Major modules
  - Component relationships
  - Overall system design

### Syntax Highlighting
- Source code displayed with syntax highlighting
- Easy side-by-side reading with AI explanations

### Native Desktop Experience
- Built with Tauri for lightweight native performance
- Supports Windows, Linux, and macOS

---

# Architecture

```text
+--------------------+        HTTP (JSON)        +-----------------------+
|  React Frontend    | <----------------------> |   FastAPI Backend     |
|  (Vite + Tauri)    |                           |      (Python)         |
+--------------------+                           +-----------------------+
       |                                                |
       | Tauri Bridge                                   |
       v                                                v
+--------------------+                       +-----------------------+
|  Rust Runtime      |                       |  Core Services        |
+--------------------+                       +-----------------------+
                                             | Scanner               |
                                             | File Reader           |
                                             | Import Resolver       |
                                             | Graph Builder         |
                                             | Repository Search     |
                                             | AI Explainer          |
                                             +-----------------------+
```

---

# Technology Stack

## Frontend

- React
- TypeScript
- Vite
- React Markdown
- React Syntax Highlighter

## Desktop

- Tauri
- Rust

## Backend

- FastAPI
- Python

## AI & Parsing

- OpenRouter
- Tree-sitter
- tree-sitter-language-pack

---

# Project Structure

```text
Codebase-Explainer/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── config.py
│       │
│       ├── services/
│       │   ├── scanner.py
│       │   ├── filereader.py
│       │   ├── graphbuilder.py
│       │   ├── reposearch.py
│       │   ├── explainer.py
│       │   ├── repoexplainer.py
│       │   └── parser/
│       │       └── importresolver.py
│       │
│       └── static/
│           └── extensions.py
│
├── desktop/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   └── assets/
│   │
│   └── src-tauri/
│       ├── src/
│       │   └── main.rs
│       └── build.rs
│
└── README.md
```

---

# How It Works

## 1. Select a Repository

The user chooses a local folder using the native file picker provided by Tauri.

---

## 2. Scan the Repository

The frontend sends a request to:

```http
POST /scan
```

The backend:

1. Walks the directory tree
2. Identifies supported source files
3. Reads file contents
4. Extracts imports using Tree-sitter
5. Builds a dependency graph

---

## 3. Explore the Repository

The generated graph is returned to the frontend and rendered as an interactive file tree.

Users can:

- Browse files
- Expand folders
- Navigate project structure

---

## 4. Search

Users can search across the repository:

```http
POST /repo_search
```

The backend performs repository-wide matching and returns relevant files.

---

## 5. Explain a File

When a file is selected:

```http
POST /explain_file
```

The backend:

1. Reads the file content
2. Collects contextual information
3. Builds an LLM prompt
4. Sends the prompt to OpenRouter
5. Returns a markdown explanation

---

## 6. Explain the Entire Repository

Users can request a project-level summary:

```http
POST /explain_repo
```

The backend:

1. Summarizes the repository graph
2. Generates architecture context
3. Sends the information to the LLM
4. Returns a complete repository overview

---

# API Endpoints

## Scan Repository

```http
POST /scan
```

### Request

```json
{
  "path": "/path/to/repository"
}
```

### Response

```json
{
  "nodes": [],
  "edges": []
}
```

---

## Search Repository

```http
POST /repo_search
```

### Request

```json
{
  "query": "authentication"
}
```

---

## Explain File

```http
POST /explain_file
```

### Request

```json
{
  "file_path": "src/auth/login.py"
}
```

---

## Explain Repository

```http
POST /explain_repo
```

### Request

```json
{
  "repository_path": "/project"
}
```

---

# Setup

## Prerequisites

- Python 3.10+
- Node.js 18+
- Rust
- Tauri CLI

---

## Clone the Repository

```bash
git clone https://github.com/yourusername/codebase-explainer.git

cd codebase-explainer
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Run the API:

```bash
uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd desktop

npm install
```

Run the development server:

```bash
npm run tauri dev
```

---

# Supported Workflow

```text
Open Repository
        ↓
Scan Files
        ↓
Build Dependency Graph
        ↓
Browse File Tree
        ↓
Search Repository
        ↓
Select File
        ↓
Generate AI Explanation
        ↓
Understand Code Faster
```

---

# Current Limitations

- Requires an OpenRouter API key
- Search is currently keyword-based
- No automated tests yet
- Limited error handling for unreadable files
- Dependency graph is rebuilt on every scan
- Backend and frontend communicate via localhost HTTP

---

# Future Improvements

- Semantic vector search
- Repository chat interface
- Interactive dependency visualization
- Incremental scanning
- Graph caching
- Multi-repository support
- Async LLM requests
- Test suite
- Plugin architecture for language parsers
- Tauri IPC integration instead of HTTP
- Offline/local model support

---

# Use Cases

### New Team Members
Understand large repositories quickly without reading thousands of lines of code.

### Open Source Contributors
Get architectural overviews before making contributions.

### Code Reviews
Understand unfamiliar modules faster.

### Documentation Generation
Generate repository summaries automatically.

### Learning Projects
Explore how real-world projects are structured.

---

# Why Codebase Explainer?

Modern codebases are often too large to understand by reading files one at a time. Codebase Explainer combines static analysis with large language models to provide a faster, more intuitive way to explore and understand software systems.

Instead of asking:

> "Where do I start?"

You can simply open the repository and ask the codebase to explain itself.

---