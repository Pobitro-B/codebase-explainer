import { useState } from "react";
import "./App.css";
import { open } from "@tauri-apps/plugin-dialog";
import DirTree from "./components/DirTree";

function App() {
  const [status, setStatus] = useState("Down");
  const [selected, setSelected] = useState("Select Repository");
  const [active, setActive] = useState(false);
  const [folder, setFolder] = useState<string | null>(null);
  const [repoTree, setRepoTree] = useState(null);
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
      body: JSON.stringify({path:folder}),
    });

    const result = await res.json();
    setRepoTree(result);
  }
  return (
    <div>
      <input type="text" disabled value={folder ? folder : "Select a repository"} />
      <button onClick={handleSelect}>{selected}</button>
      <button onClick={handleExec} disabled={!active}>
        Explain!
      </button>
      <button onClick={handleButton}>Health: {status}</button>
      {repoTree ? <DirTree dirTree={repoTree} depth={1}/> : null}
    </div>
  );
}

export default App;
