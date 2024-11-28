import React, {useState, useEffect} from "react";
import Book from "./Book";
import './css/BookList.css';
import axios from "axios";

function BookList({Page, limit}){
    const [books, setBooks] = useState([]);

    useEffect(() => {
        axios
        .get(`http://127.0.0.1:8000/api/${Page}?limit=${limit}&offset=0`)
        .then((response) => setBooks(response.data["books"]))
        .catch((error) => console.error(error));
    }, [limit]);


    return(
        <div className="BookList">
            {books.map((book)=>(
                <Book key={book.id} book = {book} />
            ))}
        </div>
    );
}

export default BookList;