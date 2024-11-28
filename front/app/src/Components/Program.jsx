import React from "react";
import {useNavigate} from "react-router-dom";
import "./css/Book.css";
import axios from "axios";

function Program({program}) {

    const handleSubmitClick = () => {
        axios
        .post(`http://127.0.0.1:8000/api/programs/${program.id}/participants`)
    }
    return (
        <div className="Book_frame">
            <div className="Book_thumbnailFrame">
                <div className="Book_thumbnail" >
                    <img className="Book_thumbnailImage" src={program.image} alt="Book Thumbnail"/>
                </div>
            </div>
            <div className="BookDetail">
                <h2 className="Book_title">{program.name}</h2>
                <p className="Book_description">{program.participants}명 참여중</p>
                <p className="Book_description">{program.description}</p>
                <p className="Book_isbn">{program.event_date}</p>
                <button className="SubmitButton" onClick={handleSubmitClick} >신청하기</button>
            </div>
        </div>
    );
}

export default Program;