import react from "react";
import {useNavigate} from "react-router-dom"
import styled from "styled-components";
import Header from "../Components/Header"
import Libmap from "../Components/Libmap";
import BottomImage from "../Components/BottomImage";

const Frame = styled.div`
    display: flex;
    flex-direction: column; /* 요소를 수직으로 배치 */
    align-items: center; /* 요소를 중앙 정렬 (수평 기준) */
    width: 100vw; /* 가로 크기 */
    margin: 0 auto;
    overflow-x:hidden;
`

function Skmap(){
    return(
        <Frame>
            <Header/>
            <Libmap/>
            <BottomImage />
        </Frame>
    );
}

export default Skmap;