import React from "react";
import "./css/Book.css";

function Book({book}) {
    return (
        <div className="Book_frame">
            <div className="Book_thumbnailFrame">
                <div className="Book_thumbnail" >
                    <img src={book.img} alt="Book Thumbnail"/>
                </div>
            </div>
            <div className="BookDetail">
                <h2 className="Book_title">{book.title}</h2>
                <p className="Book_description">{book.author}</p>
                <p className="Book_description">{book.description}</p>
                <p className="Book_isbn">{book.isbn}</p>
                <button className="Book_LookDetail">상세 정보 보기</button>
            </div>
        </div>
    );
}

export default Book;