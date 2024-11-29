import React, {useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import './css/Bookinfo.css';
import axios from "axios";
import { useToken } from "../TokenContext";

function BookInfo({Book_id, Tag, Tag2, ButtonText}) {
    const [book, setBook] = useState([]);
    const {token} = useToken();
    const navigate = useNavigate();
    useEffect(() => {
        axios
        .get(`http://127.0.0.1:8000/api/${Tag2}/${Book_id}`)
        .then((response) => {
            setBook(response.data);
        })
        .catch((error) => console.error(error));
    }, []);

    const handleLoanClick = (e) => {
        if(!token){
            e.preventDefault();
            alert("로그인이 필요합니다.");
            navigate("/login");
        }else{
            axios
            .put(`http://127.0.0.1:8000/api/${Tag}/${Book_id}`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                console.log(response.data["message"]);
                alert(response.data["message"]);
            })
            .catch((error) => {
                console.error(error);
                alert("신청이 실패했습니다. 사유: " + error);
            })
        }
    }
    return (
        <section className="BookInfoFrame">
            <div className="BookInfo_imageBox">
                <img className="BookInfo_image" src={book.image} alt="Book_Img"/>
            </div>
            <div className="BookInfo_Box">
                <h4 className="BookInfo_title">{book.title}</h4>
                <p className="BookInfo_description">{book.author}</p>
                <p className="BookInfo_description">{book.description}</p>
                <p className="BookInfo_description">{book.status === "borrowed" ? "대출 불가" : "대출 가능"}</p>
                <button className="BookInfo_loan" onClick={handleLoanClick} >
                    <p className="BookInfo_loanText">{ButtonText}</p>
                    </button>
            </div>
        </section>
    );
}

export default BookInfo;
