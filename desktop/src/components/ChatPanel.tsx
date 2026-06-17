import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./ChatPanel.css";

export default function ChatPanel(props) {
  const [userInput, setUserInput] = useState("");

  function handleSubmit() {
    if (!userInput.trim()) return;

    props.onSend(userInput);
    setUserInput("");
  }
  return (
    <div className="chat-panel">
      <div className="chat-messages">
        {props.messages.map((msg) => (
          <div className={`chat-message ${msg.role}`}>
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
        {props.chatLoading && (
          <div className="chat-message assistant">Thinking...</div>
        )}
      </div>
      <div className="chat-input-area">
        <input
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Ask about the repository..."
          disabled={props.chatLoading}
          onKeyDown={(e) => {
            if (e.key == "Enter") {
              handleSubmit();
            }
          }}
        />
        <button
          onClick={handleSubmit}
          disabled={props.chatLoading}
        >
          Send
        </button>
      </div>
    </div>
  );
}
