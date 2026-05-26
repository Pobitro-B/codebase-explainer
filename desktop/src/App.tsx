import { useState } from "react";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Down");
  const [selected, setSelected] = useState("Select Repository");
  const [active, setActive] = useState(false);
  async function handleButton() {
    const res = await fetch("http://localhost:8000/health");
    const data = await res.json();
    setStatus(data.status);
  }

  function handleSelect() {
    setSelected("Select Another");
    setActive(true);
  }
  function handleExec(e) {
    setActive(true);
  }
  return (
    <div>
      <button onClick={handleSelect}>{selected}</button>
      <button
        onClick={() => alert("tree parse should start now")}
        disabled={!(active)}
      >
        Explain!
      </button>
      <button onClick={handleButton}>Health: {status}</button>
    </div>
  );
}

export default App;
