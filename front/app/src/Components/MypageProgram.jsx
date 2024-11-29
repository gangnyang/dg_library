import React, { useState, useEffect } from "react";
import './css/Loan.css';
import { useToken } from "../TokenContext";
import axios from "axios";

function Program({ item, onDelete }) {
    const [overdue, setOverdue] = useState(0);
    const {token} = useToken();

    const getIconSrc = () => {
        return "/images/Happy.svg";
    };


    useEffect(() => {
        if (item.event_date) {
            const eventDate = new Date(item.event_date);
            const now = new Date();
            setOverdue(eventDate < now ? 1 : 0);
        }
    }, [item.event_date]);

    const getStatusTitle = () => {
        return overdue === 1 ? "프로그램 종료" : "프로그램 예정";
    };

    const handleButtonClick = () => {
        axios
            .delete(`http://127.0.0.1:8000/api/programs/${item.id}/participants`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                console.log(response.data["message"]);
                alert(response.data["message"]);
                onDelete(); // 부모 컴포넌트에 삭제 요청
            })
            .catch((error) => {
                console.error(error);
                alert("취소에 실패했습니다. 사유: " + error);
            })
    }

    const renderButton = () => {
        if (overdue === 0) {
            return (
                <button className="ReturnButton" onClick={handleButtonClick}>
                    <p className="ReturnButtonText">취소하기</p>
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
                                src={getIconSrc(item, overdue)}
                                alt="상태 아이콘"
                            />
                            <div className="StatusTextFrame">
                                <p className="StatusSubTitle">
                                    프로그램 이름: {item.name}
                                </p>
                                <p className="StatusSubTitle">{item.event_date} 실시 예정</p>
                                <h1 className="StatusTitle">
                                    {getStatusTitle(item, overdue)}
                                </h1>
                            </div>
                        </div>
                        {renderButton(item, overdue)}
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Program;
