import { useState } from "react";
import "./App.css";
import { open } from "@tauri-apps/plugin-dialog";
import DirTree from "./components/DirTree";
import FileArea from "./components/FileArea";
import ReactMarkdown from "react-markdown";
import Topbar from "./components/TopBar";
import SearchBar from "./components/SearchBar";
import SearchResults from "./components/SearchResults";

function App() {
  const [status, setStatus] = useState("Down");
  const [selected, setSelected] = useState("Select Repository");
  const [active, setActive] = useState(false);
  const [folder, setFolder] = useState<string | null>(null);
  const [repoTree, setRepoTree] = useState<any>(null);
  const [fileOpen, setFileOpen] = useState("HOME_PAGE");
  const [fileContent, setFileContent] = useState<any>(null);
  const [graph, setGraph] = useState<any>(null);
  const [explanation, setExplanation] = useState<any>(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [explanationCache, setExplanationCache] = useState<
    Record<string, string>
  >({});
  const [repoExplanation, setRepoExplanation] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  async function handleButton() {
    const res = await fetch("http://localhost:8000/health");
    const data = await res.json();
    setStatus(data.status);
  }
  async function handleSelect() {
    const file = await open({
      multiple: false,
      directory: true,
    });
    setFolder(file ? file : folder);
    // Prints file path or URI
    setSelected("Select Another");
    setActive(file ? true : active);
  }
  async function handleExec() {
    const res = await fetch("http://localhost:8000/scan-repo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ path: folder }),
    });

    const result = await res.json();
    setRepoTree(result["tree"]);
    setGraph(result["graph"]);

    setLoadingExplanation(true);
    const response = await fetch("http://localhost:8000/explain-repo", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const explained = await response.json();
    setLoadingExplanation(false);
    setRepoExplanation(explained.explanation);
    setExplanation(explained.explanation);

    await handleFileOpen("HOME_PAGE");
  }

  async function handleFileOpen(path) {
    const response = await fetch("http://localhost:8000/read-file", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ path: path }),
    });

    const result = await response.json();
    if (path !== "HOME_PAGE") {
      if (explanationCache[path]) {
        setExplanation(explanationCache[path]);
      } else {
        setExplanation(null);
      }
    }

    setFileContent(result);
  }

  async function handleExplain() {
    setLoadingExplanation(true);
    if (explanationCache[fileOpen]) {
      setExplanation(explanationCache[fileOpen]);
      setLoadingExplanation(false);
    } else {
      const response = await fetch("http://localhost:8000/file-context", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ path: fileOpen }),
      });

      const result = await response.json();

      const explain = await fetch("http://localhost:8000/explain-file", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(result),
      });

      const explained = await explain.json();
      setExplanation(explained.explanation);
      setExplanationCache((prev) => ({
        ...prev,
        [fileOpen]: explained.explanation,
      }));
      setLoadingExplanation(false);
    }
  }

  async function handleSearch() {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    const response = await fetch("http://localhost:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: searchQuery }),
    });

    const results = await response.json();
    setSearchResults(results.results);
  }

  return (
    <div className="app">
      <Topbar
        className="topbar"
        folder={folder}
        handleSelect={handleSelect}
        selected={selected}
        handleExec={handleExec}
        active={active}
        handleExplain={handleExplain}
        fileOpen={fileOpen}
        loadingExplanation={loadingExplanation}
        handleButton={handleButton}
        status={status}
      />
      <div className="workspace">
        <div className="sidebar">
          {repoTree ? (
            <div>
              <SearchBar
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                handleSearch={handleSearch}
              />
              <SearchResults
                results={searchResults}
                handleOpen={(path) => {
                  setFileOpen(path);
                  handleFileOpen(path);
                }}
              />
              <DirTree
                dirTree={repoTree}
                depth={1}
                setCurrFile={setFileOpen}
                handleOpen={handleFileOpen}
                fileOpen={fileOpen}
                graph={graph}
              />
            </div>
          ) : null}
        </div>
        <div className="editor">
          {repoTree && fileContent ? (
            <FileArea fileContent={fileContent} />
          ) : null}
        </div>
        <div className="explanation-panel">
          <ReactMarkdown>
            {loadingExplanation
              ? "Analyzing file..."
              : explanation || "Select a file and click Explain file"}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}

export default App;
