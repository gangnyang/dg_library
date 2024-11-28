import react from "react";
import {useNavigate} from "react-router-dom"
import styled from "styled-components";
import Header from "../Components/Header"
import BookInfo from "../Components/BookInfo";
import CommentList from "../Components/CommentList";
import BottomImage from "../Components/BottomImage";

const Frame = styled.div`
    display: flex;
    flex-direction: column; /* 요소를 수직으로 배치 */
    align-items: center; /* 요소를 중앙 정렬 (수평 기준) */
    width: 99vw; /* 가로 크기 */
    margin: 0 auto;
    overflow-x:hidden;
`

function BookDetail(){
    return(
        <Frame>
            <Header/>
            <BookInfo 
                BookTitle="제목"
                BookAuthor="~~~"
                BookDescription="~~~~~~"
                BookImg="images/Books_MBimage.jpg"
                ButtonColor="#F4FCBB"
                ButtonText="대출 신청하기"
            />
            <CommentList />
            <BottomImage />
        </Frame>
    );
}

export default BookDetail;