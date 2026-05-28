import { useState } from "react";
import {GoArrowDown, GoArrowRight, GoCodeSquare} from "react-icons/go";

export default function DirTree(props) {
  const dir = props.dirTree;
  const [isCollapsed, setIsCollapsed] = useState(false);
  function handleCollapse() {
    setIsCollapsed(isCollapsed ? false : true);
  }
  return (
    <div style={{paddingLeft: 5*props.depth}}>
      <button onClick={handleCollapse}>
        {isCollapsed ? <GoArrowRight/> : <GoArrowDown/>}{dir["name"]}
      </button>
      {dir["children"].map((child) => {
        if (child["type"] == "directory") {
          return isCollapsed ? null : (
            <DirTree dirTree={child} depth={props.depth + 1} />
          );
        } else {
          return isCollapsed ? null : (
            <div style={{paddingLeft: 5*(props.depth+1)}}>
              <GoCodeSquare />{child["name"]}
            </div>
          );
        }
      })}
    </div>
  );
}
