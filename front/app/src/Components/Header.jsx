import React from "react"
import {useNavigate} from "react-router-dom";
import './css/Header.css';
import { useToken } from "../TokenContext";

function Header() {
    const {token, setToken} = useToken();
    const navigate = useNavigate();

    const handleMypageClick = (e) => {
        if(!token){
            e.preventDefault();
            alert("로그인이 필요합니다.");
            navigate("/login");
        }
    }
    const handleLogoutClick = (e) => {
        alert("로그아웃이 완료되었습니다.");
        setToken(null);
    }
    return (
        <header className="header">
            <div className="nav">
                <div className="left_content">
                    <div className="divider"/>
                    <a href="/">메인</a>
                    <a href="/externallib">다른 도서관 책</a>
                    <a href="/programs">프로그램</a>
                    <a href="/Skmap">오시는 길</a>
                </div>
                <div className="Mypage_frame">
                    <a href="/Mypage" className="Mypage_button" onClick={handleMypageClick}>
                        <div className="logo"/>
                    </a>
                    {token&&<a href="/" className="Mypage_button" onClick={handleLogoutClick}>
                        <div className="logo2"/>
                    </a>}
                </div>
            </div>
            <div className="divider2"/>
        </header>
    );
}

export default Header;