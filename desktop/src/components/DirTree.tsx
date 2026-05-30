import "./DirTree.css";
import { useState } from "react";
import { GoArrowDown, GoArrowRight, GoCodeSquare } from "react-icons/go";

export default function DirTree(props) {
  const dir = props.dirTree;
  const [isCollapsed, setIsCollapsed] = useState(false);
  const deps = props.graph?.dependencies?.[props.fileOpen] ?? [];
  const dependents = props.graph?.dependents?.[props.fileOpen] ?? [];
  function handleCollapse() {
    setIsCollapsed(isCollapsed ? false : true);
  }
  function handleFileButton(path) {
    props.setCurrFile(path);
    props.handleOpen(path);
  }
  return (
    <div className="tree-node">
      <div className="tree-item">
        <button onClick={handleCollapse}>
          {isCollapsed ? <GoArrowRight /> : <GoArrowDown />}
          {dir["name"]}
        </button>
      </div>
      <div className="tree-children">
        {dir["children"].map((child) => {
          if (child["type"] == "directory") {
            return isCollapsed ? null : (
              <DirTree
                dirTree={child}
                depth={props.depth + 1}
                setCurrFile={props.setCurrFile}
                handleOpen={props.handleOpen}
                fileOpen={props.fileOpen}
                graph={props.graph}
              />
            );
          } else {
            return isCollapsed ? null : (
              <div
                className={
                  props.fileOpen == child["path"]
                    ? "active-item file-item"
                    : deps.includes(child["path"])
                      ? "dependency file-item"
                      : dependents.includes(child["path"])
                        ? "dependent file-item"
                        : "file-item"
                }
              >
                <button onClick={() => handleFileButton(child["path"])}>
                  <GoCodeSquare />
                  {child["name"]}
                </button>
              </div>
            );
          }
        })}
      </div>
    </div>
  );
}
