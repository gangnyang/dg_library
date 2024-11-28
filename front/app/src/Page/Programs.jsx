import react from 'react';
import Header from '../Components/Header';
import MainBanner from '../Components/MainBanner';
import Search from '../Components/Search';
import BookList from '../Components/BookList';
import LoadButton from '../Components/LoadButton';
import BottomImage from '../Components/BottomImage';
import styled from "styled-components";

const Frame = styled.div`
    display: flex;
    flex-direction: column; /* 요소를 수직으로 배치 */
    align-items: center; /* 요소를 중앙 정렬 (수평 기준) */
    width: 99vw; /* 가로 크기 */
    margin: 0 auto;
    overflow-x: hidden;
`

function Programs() {
    return (
        <Frame>
            <Header/>
            <MainBanner
                bannerColor="#FCBBBB"
                title="도서관에서 하는 프로그램을 봐요"
                description="도서관에서 진행하는 다양한 프로그램을 살펴봐요"
                imagesrc="/images/programs.jpg"
            />
            <Search
                query="프로그램명"
                ph="프로그램명 입력"
            />
            <BookList/>
            <LoadButton/>
            <BottomImage/>
        </Frame>
    );
}



export default Programs;
