import React from "react";
import {useNavigate} from "react-router-dom";
import "./css/Book.css";

function Book({book, Page}) {
    const navigate = useNavigate();

    const handleDetailClick = () => {
        if(Page==="books"){
            navigate(`/BookDetail/${book.id}`);
        }else{
            navigate(`/ExternalBookDetail/${book.id}`);
        }
    }

    
    return (
        <div className="Book_frame">
            <div className="Book_thumbnailFrame">
                <div className="Book_thumbnail">
                    <img className="Book_thumbnailImage" src={book.image} alt="Book Thumbnail"/>
                </div>
            </div>
            <div className="BookDetail">
                <h2 className="Book_title">{book.title}</h2>
                <p className="Book_description">{book.author}</p>
                <p className="Book_description">{book.description}</p>
                <div className="Book_BottomBox">
                    <p className="Book_isbn">{book.isbn}</p>
                    <div className="Book_LookDetailBox">
                    <button className="Book_LookDetail" onClick={handleDetailClick}>상세 정보 보기</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Book;