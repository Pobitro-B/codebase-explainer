import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import heroImg from "./assets/hero.png";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Down");
  async function handleButton(e) {
    const res = await fetch("http://localhost:8000/health");
    const data = await res.json();
    setStatus(data.status);
  }
  return (
    <div>
      <button onClick={handleButton}>Health: {status}</button>
    </div>
  );
}

export default App;
