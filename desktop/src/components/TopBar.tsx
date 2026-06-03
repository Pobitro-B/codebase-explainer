export default function Topbar(props) {
  return (
    <div className="topbar">
      <input
        type="text"
        disabled
        value={props.folder ? props.folder : "Select a repository"}
      />
      <button onClick={props.handleSelect}>{props.selected}</button>
      <button onClick={props.handleExec} disabled={!props.active}>
        Explain!
      </button>
      <button
        onClick={props.handleExplain}
        disabled={props.fileOpen == "HOME_PAGE" || props.loadingExplanation ? true : false}
      >
        Explain file
      </button>
      <button onClick={props.handleButton}>Health: {props.status}</button>
    </div>
  );
}
