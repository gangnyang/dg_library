import React from "react"
import {useNavigate} from "react-router-dom";
import './css/Header.css';

function Header() {
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
                    <a href="/Mypage" className="Mypage_button">
                        <div className="logo"/>
                    </a>
                </div>
            </div>
            <div className="divider2"/>
        </header>
    );
}

export default Header;