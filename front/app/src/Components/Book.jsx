import React from "react";
import "./Book.css";

function Book({book}){
    return(
        <div className="book">
            <div className="thumbnail">
                <img src={book.img} alt="Book Thumbnail"/>
            </div>
            <div className= "BookDetail">
                <h2>{book.title}</h2>
                <p>{book.author}</p>
                <p>{book.description}</p>
                <button>상세 정보 보기</button>
            </div>
        </div>
    );
}

export default Book;