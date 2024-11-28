import React, { useState, useEffect } from "react";
import './css/Loan.css';

function Loan({ item, frameNumber }) {
    const [overdue, setOverdue] = useState(0);

    // 프로그램 참여 상태 업데이트
    useEffect(() => {
        if (frameNumber === 4 && item.joined) {
            const joinedDate = new Date(item.joined);
            const now = new Date();
            setOverdue(joinedDate < now ? 1 : 0);
        }
    }, [frameNumber, item.joined]);

    // 상태에 따라 적합한 아이콘 이미지 경로 반환
    const getIconSrc = () => {
        if (frameNumber === 2) {
            if (item.status === "progress") return "images/Clock.png";
            if (item.status === "overdue") return "images/Sad.svg";
            return "images/Happy.svg";
        }
        if (frameNumber === 3) {
            if (item.status === "progress") return "images/Clock.png";
            if (item.status === "complete") return "images/Happy.svg";
            return "images/Sad.svg";
        }
        if (frameNumber === 4) {
            return "images/Happy.svg";
        }
        return "images/Sad.png";
    };

    // 상태에 따라 적합한 텍스트 반환
    const getStatusTitle = () => {
        if (frameNumber === 2) {
            if (item.status === "progress") return "대출 중";
            if (item.status === "overdue") return "연체 상태";
            return "반납 완료";
        }
        if (frameNumber === 3) {
            if (item.status === "progress") return "상호 대차 중";
            if (item.status === "complete") return "반납 완료";
            return "예기치 않은 상태";
        }
        if (frameNumber === 4) {
            return overdue === 1 ? "프로그램 종료" : "프로그램 예정";
        }
        return "오류!";
    };

    // 상태에 따라 적합한 버튼 JSX 반환
    const renderButton = () => {
        if (frameNumber === 4) {
            return overdue === 0 ? (
                <button className="ReturnButton">
                    <p className="ReturnButtonText">취소하기</p>
                </button>
            ) : null;
        }
        if (item.status === "progress") {
            return (
                <button className="ReturnButton">
                    <p className="ReturnButtonText">반납하기</p>
                </button>
            );
        }
        return null;
    };

    return (
        <section className="LoanFrame">
            <div className="LoanBox">
                <div className="LoanBackground">
                    <h1 className="LoanID">#{item.id}</h1>
                    <div className="LoanInnerFrame">
                        <div className="StatusFrame">
                            <img
                                className="ClockIcon"
                                src={getIconSrc()}
                                alt=""
                            />
                            <div className="StatusTextFrame">
                                <p className="StatusSubTitle">상태</p>
                                <p className="StatusSubTitle">
                                    {frameNumber === 4 ? "프로그램 번호" : "책 번호"}: {item.id}
                                </p>
                                <h1 className="StatusTitle">{getStatusTitle()}</h1>
                            </div>
                        </div>
                        {renderButton()}
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Loan;
