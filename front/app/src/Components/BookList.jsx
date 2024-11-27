import React from "react";
import Book from "./Book";
import './css/BookList.css';

function BookList(){
    const books = [
        {id:1, title: "책 제목", author: "누구누구 지음", image:"/images/Books_MBimage.jpg", description:"상세설명 있어요", isbn:"123123123"},
        {id:1, title: "책 제목", author: "누구누구 지음", image:"/images/Books_MBimage.jpg", description:"상세설명 있어요", isbn:"123123123"},
        {id:1, title: "책 제목", author: "누구누구 지음", image:"/images/Books_MBimage.jpg", description:"상세설명 있어요", isbn:"123123123"},
        {id:1, title: "책 제목", author: "누구누구 지음", image:"/images/Books_MBimage.jpg", description:"상세설명 있어요", isbn:"123123123"},
    ];
    return(
        <div className="BookList">
            {books.map((book)=>(
                <Book key={book.id} book = {book} />
            ))}
        </div>
    );
}

export default BookList;