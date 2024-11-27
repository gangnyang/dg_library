import React from "react";
import "./MainBanner.css";

function MainBanner(){
    return(
        <section className = "MainBanner">
            <div className = "BannerText">
                <h1>도서관의 책들을 둘러보세요</h1>
                <p>이곳에 도서관에 있는 모든 책의 정보가 있어요. 온라인으로도 대출을 신청할 수 있어요.</p>
            </div>
            <div className = "BannerImage">
                <img src="/images/Books_MBimage.jpg" alt="Main_Banner" />
            </div>
        </section>
    );
}

export default MainBanner;