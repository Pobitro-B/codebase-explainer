export default function FileArea(props) {
  const name = props.fileContent["name"];
  const path = props.fileContent["path"];
  const contents = props.fileContent["content"];
  return (<div>
    <h2>{name}</h2>
    {contents.map((line)=><div>{line}</div>)}
  </div>);
}
