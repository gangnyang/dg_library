import react, {useState} from "react";
import './css/Search.css';

function Search({query, ph, squery, onSearchClick, onSetLimit}){
    const [inputValue, setInputValue] = useState("");

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleButtonClick = () =>{
        onSearchClick(inputValue);
        onSetLimit(20);
    };
    return(
        <div className="Search">
            <div className="Frame1">
                <div className="Search_Caption">
                    <p className="Search_Title">{query}</p>
                </div>
                <div className="Inp_background">
            <input className="InputBox" type="text" placeholder={ph} value={inputValue} onChange={handleInputChange}/>
            </div>
            <button className="SearchButton" onClick={handleButtonClick}>
                <div className="Search_logo"/>
            </button>
            </div>
        </div>
    )
}

export default Search;