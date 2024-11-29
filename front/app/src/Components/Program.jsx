import React from "react";
import {useNavigate} from "react-router-dom";
import "./css/Book.css";
import axios from "axios";
import { useToken } from "../TokenContext";

function Program({program}) {
    const {token} = useToken();
    const navigate = useNavigate();

    const handleSubmitClick = (e) => {
        if(!token){
            e.preventDefault();
            alert("로그인이 필요합니다.");
            navigate("/login");
        }else{
            axios
            .post(`http://127.0.0.1:8000/api/programs/${program.id}/participants`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                console.log(response.data["message"]);
                alert(response.data["message"]);
            })
            .catch((error) =>{
                console.error(error);
                alert("신청이 실패했습니다. 사유: " + error["detail"]);
            })
        }
    }
    return (
        <div className="Book_frame">
            <div className="Book_thumbnailFrame">
                <div className="Book_thumbnail">
                    <img className="Book_thumbnailImage" src={program.image} alt="Book Thumbnail"/>
                </div>
            </div>
            <div className="BookDetail">
                <h2 className="Book_title">{program.name}</h2>
                <p className="Book_description">{program.participants}명 참여중</p>
                <p className="Book_description">{program.description}</p>
                <div className="Book_BottomBox">
                    <p className="Book_isbn">{program.event_date}</p>
                    <div className="Book_LookDetailBox">
                    <button className="SubmitButton" onClick={handleSubmitClick}>신청하기</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Program;