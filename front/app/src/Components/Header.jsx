import React from "react"
import './Header.css';

function Header(){
    return(
        <header className="header">
            <nav>
                <ul classname = "nav_menu">
                    <li><a href="#">메인</a></li>
                    <li><a href="#">다른 도서관 책</a></li>
                    <li><a href="#">프로그램</a></li>
                    <li><a href="#">오시는 길</a></li>
                    <li className= "Mypage_icon">👤</li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;