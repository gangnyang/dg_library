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
    overflow-x:hidden;
`

function ExternalLibrary() {
    return (
        <Frame>
            <Header/>
            <MainBanner
                bannerColor="#FCD9BB"
                title="다른 도서관의 책들을 둘러보세요"
                description="이곳에는 다른 도서관의 책들도 있어요. 한번 둘러봐요. 상호대차를 신청해서 이 도서관으로 빌릴 수 있어요."
                imagesrc="/images/external_library.jpg"
            />
            <Search
                query="도서명"
                ph = "도서명 혹은 작가명 입력"
            />
            <BookList/>
            <LoadButton/>
            <BottomImage/>
        </Frame>
    );
}



export default ExternalLibrary;
