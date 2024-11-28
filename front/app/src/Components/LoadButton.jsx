import React from "react";
import './css/LoadButton.css';

function LoadButton({limit, onMoreClick}){
    return(
        <button className="LoadButton" onClick={() => onMoreClick(limit+10)}>10개 더 불러오기</button>
    );
}

export default LoadButton;