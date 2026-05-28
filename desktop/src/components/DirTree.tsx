import "./DirTree.css";
import { useState } from "react";
import { GoArrowDown, GoArrowRight, GoCodeSquare } from "react-icons/go";

export default function DirTree(props) {
  const dir = props.dirTree;
  const [isCollapsed, setIsCollapsed] = useState(false);
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
              />
            );
          } else {
            return isCollapsed ? null : (
              <div className="file-item">
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
