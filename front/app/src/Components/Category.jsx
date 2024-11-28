import React from "react"
import './css/Category.css';

function Category({frameNumber, onFrameChange}){
    
    return(
        <section className="CategoryFrame">
            <div className="ListFrame1" onClick={()=>onFrameChange(1)}>
                <img className="ListFrame1Logo" src="images/Lock.svg" alt=""/>
                <p className={`ListFrame1Title ${
                        frameNumber === 1 ? "active" : ""}`}>회원 정보 변경</p>
            </div>
            <div className="ListFrame1" onClick={()=>onFrameChange(2)}>
                <img className="ListFrame2Logo" src="images/inform.png" alt=""/>
                <p className={`ListFrame1Title ${
                        frameNumber === 2 ? "active" : ""}`}>내 대출 기록</p>
            </div>
            <div className="ListFrame1" onClick={()=>onFrameChange(3)}>
                <img className="ListFrame1Logo" src="images/inform.png" alt=""/>
                <p className={`ListFrame1Title ${
                        frameNumber === 3 ? "active" : ""}`}>내 상호 대차 기록</p>
            </div>
            <div className="ListFrame1" onClick={()=>onFrameChange(4)}>
                <img className="ListFrame1Logo" src="images/inform.png" alt=""/>
                <p className={`ListFrame1Title ${
                        frameNumber === 4 ? "active" : ""}`}>내 프로그램</p>
            </div>
        </section>
    );
}

export default Category;