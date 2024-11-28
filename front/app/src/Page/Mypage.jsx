import react from 'react';
import Header from '../Components/Header';
import MyPageDetail from '../Components/MyPageDetail';
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
    return (
        <Frame>
            <Header/>
            <MyPageDetail/>
            <BottomImage/>
        </Frame>
    );
}



export default Main;
