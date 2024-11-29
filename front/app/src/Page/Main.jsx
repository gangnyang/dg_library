import react, {useState} from 'react';
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

function Main() {
    const [limit, setLimit] = useState(20);
    const handleMoreClick = (newLimit) => {
        setLimit(newLimit);
    }
    const[squery, setSquery] = useState("");
    const handleSearchClick = (newSquery) => {
        setSquery(newSquery);
    }
    const[countBook, setCountBook] = useState(21);
    const handleCalcCount = (newCount) => {
        setCountBook(newCount);
    }
    return (
        <Frame>
            <Header/>
            <MainBanner
                bannerColor="#F4FCBB"
                title="도서관의 책들을 둘러보세요"
                description="이곳에 도서관에 있는 모든 책의 정보가 있어요. 온라인으로도 대출을 신청할 수 있어요."
                imagesrc="/images/Books_MBimage.jpg"
            />
            <Search
                query = "도서명"
                ph = "도서명 혹은 작가명 입력"
                squery={squery}
                onSearchClick={handleSearchClick}
                onSetLimit = {setLimit}
            />
            <BookList
                Page="books"
                limit={limit}
                squery={squery}
                countBook={handleCalcCount}
            />
            { limit<countBook && <LoadButton limit={limit} onMoreClick={handleMoreClick} /> }
            <BottomImage/>
        </Frame>
    );
}



export default Main;
