import react from "react";
import './css/Search.css';

function Search({query, ph}){
    return(
        <div className="Search">
            <div className="Frame1">
                <div className="Search_Caption">
                    <p className="Search_Title">{query}</p>
                </div>
                <div className="Inp_background">
            <input className="InputBox" type="text" placeholder={ph}/>
            </div>
            <button className="SearchButton">
                <div className="Search_logo"/>
            </button>
            </div>
        </div>
    )
}

export default Search;