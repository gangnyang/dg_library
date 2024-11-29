import react from "react";
import {useNavigate, useParams} from "react-router-dom"
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

function ExternalBookDetail(){
    const {id} = useParams();
    return(
        <Frame>
            <Header/>
            <BookInfo 
                Book_id={id}
                Tag ="external_books/interloan"
                Tag2 = "external_books"
                ButtonText="상호대차 신청"
            />
            <CommentList 
                Book_id={id}
            />
            <BottomImage />
        </Frame>
    );
}

export default ExternalBookDetail;