import { useState } from "react";
import "./App.css";
import { open } from "@tauri-apps/plugin-dialog";
import DirTree from "./components/DirTree";
import FileArea from "./components/FileArea";

function App() {
  const [status, setStatus] = useState("Down");
  const [selected, setSelected] = useState("Select Repository");
  const [active, setActive] = useState(false);
  const [folder, setFolder] = useState<string | null>(null);
  const [repoTree, setRepoTree] = useState<any>(null);
  const [fileOpen, setFileOpen] = useState("HOME_PAGE");
  const [fileContent, setFileContent] = useState<any>(null);
  const [graph, setGraph] = useState<any>(null);
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
    handleFileOpen("HOME_PAGE");
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
    setFileContent(result);
  }

  return (
    <div className="app">
      <div className="topbar">
        <input
          type="text"
          disabled
          value={folder ? folder : "Select a repository"}
        />
        <button onClick={handleSelect}>{selected}</button>
        <button onClick={handleExec} disabled={!active}>
          Explain!
        </button>
        <button onClick={handleButton}>Health: {status}</button>
      </div>
      <div className="workspace">
        <div className="sidebar">
          {repoTree ? (
            <DirTree
              dirTree={repoTree}
              depth={1}
              setCurrFile={setFileOpen}
              handleOpen={handleFileOpen}
              fileOpen={fileOpen}
              graph={graph}
            />
          ) : null}
        </div>
        <div className="editor">
          {repoTree && fileContent ? (
            <FileArea fileContent={fileContent} />
          ) : null}
        </div>
      </div>
    </div>
  );
}

export default App;
