import React from "react";
import './css/Libmap.css';

function Libmap(){
    return(
        <section className="LibmapFrame">
            <div className="OpinionFrame">
                <h1 className="OpinionTitle">의견 제출</h1>
                <p className="OpinionDescription">의견이 있다면 전달해주세요!</p>
                <div className="OpinionForm">
                    <input className="OpinionInput" type="text" placeholder = "이름" />
                    <input className="OpinionInput" type="text" placeholder = "이메일" />
                    <input className="OpinionInput" type="text" placeholder = "내용" />
                </div>
                <button className="OpinionSubmit"  >
                    <p className="OpinionSubmitText">제출하기</p>
                    </button>
                </div>
            <div className="LibmapFrame2">
                <div className="mapFrame">
                    <img className="map" src="images/SKmap.jpg" alt="map"/>
                </div>
            </div>
        </section>
    );
}

export default Libmap;