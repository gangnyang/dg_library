import React, {useState, useEffect} from "react";
import './css/Loan.css';
import axios from "axios";
import { useToken } from "../TokenContext";

function Loan({ item, onUpdate }) {
    const [book, setBook] = useState([]);
    const {token} = useToken();
    const [newStatus, setNewStatus] = useState(item.status);

    useEffect(() => {
        axios
        .get(`http://127.0.0.1:8000/api/books/${item.book_id}`)
        .then((response) => {
            setBook(response.data);
        })
        .catch((error) => console.error(error));
    }, []);

    const getIconSrc = () => {
        if (item.status === "progress") return "images/Clock.png";
        if (item.status === "overdue") return "images/Sad.svg";
        return "images/Happy.svg";
    };

    const getStatusTitle = () => {
        if (item.status === "progress") return "대출 중";
        if (item.status === "overdue") return "연체 상태";
        return "반납 완료";
    };

    const handleButtonClick = () => {
        const updatedData = {status: newStatus};

        axios
            .put(`http://127.0.0.1:8000/api/loan/return/${item.id}`, updatedData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                console.log(response.data["message"]);
                alert(response.data["message"]);
                onUpdate(); // 부모 컴포넌트에 업데이트
            })
            .catch((error) => {
                console.error(error);
                alert("반납에 실패했습니다. 사유: " + error);
            })
    }

    const renderButton = () => {
        if (item.status === "progress") {
            return (
                <button className="ReturnButton" onClick={handleButtonClick}>
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
                                src={getIconSrc(item)}
                                alt="상태 아이콘"
                            />
                            <div className="StatusTextFrame">
                                <p className="StatusSubTitle" >
                                    책 이름: {book.title}
                                </p>
                                <p className="StatusSubTitle">{item.loan_date}에 빌렸습니다.</p>
                                <p className="StatusSubTitle">{item.will_return_date}까지 반납해야합니다.</p>
                                <h1 className="StatusTitle">
                                    {getStatusTitle(item)}
                                </h1>
                            </div>
                        </div>
                        {renderButton(item)}
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Loan;
