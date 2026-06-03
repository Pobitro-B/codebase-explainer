import "./SearchBar.css"

export default function SearchBar(props) {
  function handleChange(e) {
    props.setSearchQuery(e.target.value);
  }
  return (
    <div className="search-bar">
      <button onClick={props.handleSearch}>Search</button>
      <input
        type="text"
        onChange={handleChange}
        onKeyDown={(e) => {
          if (e.key == "Enter") {
            props.handleSearch();
          }
        }}
      />
    </div>
  );
}
