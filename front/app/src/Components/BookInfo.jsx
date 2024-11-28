import React from "react";
import './css/Bookinfo.css';

function BookInfo({BookTitle, BookAuthor, BookDescription, BookImg, ButtonColor, ButtonText}) {
    return (
        <section className="BookInfoFrame">
            <div className="BookInfo_imageBox">
                <img className="BookInfo_image" src={BookImg} alt="Book_Img"/>
            </div>
            <div className="BookInfo_Box">
                <h4 className="BookInfo_title">{BookTitle}</h4>
                <p className="BookInfo_description">{BookAuthor}</p>
                <p className="BookInfo_description">{BookDescription}</p>
                <button className="BookInfo_loan" style={{backgroundColor:ButtonColor}} >
                    <p className="BookInfo_loanText">{ButtonText}</p>
                    </button>
            </div>
        </section>
    );
}

export default BookInfo;
