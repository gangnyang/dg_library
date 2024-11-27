import react from "react";
import '/Search.css';

function Search(){
    return(
        <div className="Search">
            <input type="text" placeholder="작가 이름 또는 제목 입력"></input>
            <button>검색</button>
        </div>
    )
}