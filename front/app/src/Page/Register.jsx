import react from 'react';
import Login_Hello from '../Components/Login_Hello';
import RegisterForm from '../Components/RegisterForm';
import styled from "styled-components";

const Frame = styled.div`
    display: flex;
    flex-direction: row; /* 요소를 수평으로 배치 */
    align-items: center; /* 요소를 중앙 정렬 (수평 기준) */
    width: 100vw; /* 가로 크기 */
    height:100vh;
    margin: 0 auto;
    overflow-x: hidden;
`

function Login() {
    return (
        <Frame>
            <Login_Hello/>
            <RegisterForm/>
        </Frame>
    );
}



export default Login;
