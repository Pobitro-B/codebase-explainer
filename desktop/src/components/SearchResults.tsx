import "./SearchResults.css";

export default function SearchResults(props) {
  return (
    <div className="search-results">
      {props.results.map((result) => (
        <div
          key={result.path}
          className="search-result"
          onClick={() => props.handleOpen(result.path)}
        >
          <div className="search-result-name">{result.name}</div>

          <div className="search-result-path">{result.path}</div>
        </div>
      ))}
    </div>
  );
}
