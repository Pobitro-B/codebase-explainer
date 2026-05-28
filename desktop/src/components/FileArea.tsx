import "./FileArea.css";
import SyntaxHighlighter from "react-syntax-highlighter";
import { dark } from "react-syntax-highlighter/dist/esm/styles/hljs";

export default function FileArea(props) {
  const name = props.fileContent["name"];
  const path = props.fileContent["path"];
  const contents = props.fileContent["content"];
  return (
    <div className="file-area">
      <div className="file-header">
        <h2>{name}</h2>
      </div>
      <div className="code-area">
        {contents.map((line) => (
          <div className="code-line">
            <SyntaxHighlighter
              language={props.fileContent["language"]}
              style={dark}
            >
              {line}
            </SyntaxHighlighter>
          </div>
        ))}
      </div>
    </div>
  );
}
