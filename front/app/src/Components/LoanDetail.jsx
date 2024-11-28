import React, {useState, useEffect} from "react";
import './css/LoanDetail.css';
import Loan from './Loan';

function LoanDetail({frameNumber}){
    const [data, setData] = useState([]);
    const loanData = [
        {id:1, user_id: 3, book_id: 3, loan_date: "2024-11-03", will_return_date: "2024-11-17", returned_date:null, overdue:0, status: "progress"},
        {id:2, user_id: 3, book_id: 3, loan_date: "2024-11-03", will_return_date: "2024-11-17", returned_date:null, overdue:0, status: "progress"},
        {id:3, user_id: 3, book_id: 3, loan_date: "2024-11-03", will_return_date: "2024-11-17", returned_date:null, overdue:0, status: "progress"},
        {id:4, user_id: 3, book_id: 3, loan_date: "2024-11-03", will_return_date: "2024-11-17", returned_date:null, overdue:0, status: "progress"},
    ]
    const interloanData = [
        {id:1, user_id: 3, book_id: 3, request_date: "2024-11-03", status: "progress"},
        {id:1, user_id: 3, book_id: 3, request_date: "2024-11-03", status: "progress"},
        {id:1, user_id: 3, book_id: 3, request_date: "2024-11-03", status: "progress"},
        {id:1, user_id: 3, book_id: 3, request_date: "2024-11-03", status: "progress"},
    ]
    const programData = [
        {id:1, program_id: 1, user_id: 3, joined: "2024-11-01"},
        {id:1, program_id: 1, user_id: 3, joined: "2024-11-01"},
        {id:1, program_id: 1, user_id: 3, joined: "2024-12-21"},
        {id:1, program_id: 1, user_id: 3, joined: "2024-12-01"},
        {id:1, program_id: 1, user_id: 3, joined: "2024-12-01"},
    ]
    useEffect(() => {
        if (frameNumber === 2) {
            setData(loanData); // loan 테이블 데이터
        } else if (frameNumber === 3) {
            setData(interloanData); // interloan 테이블 데이터
        } else if (frameNumber === 4) {
            setData(programData); // program 테이블 데이터
        } else {
            setData([]); // 기본값: 빈 데이터
        }
    }, [frameNumber]);
    return(
        <section className="LoanDetailFrame">
            <h1 className="LoanDetailTitle">
                {frameNumber === 2 && "내 대출 기록"}
                {frameNumber === 3 && "내 상호 대차 기록"}
                {frameNumber === 4 && "프로그램"}
            </h1>
            {data.map((item)=>(
                <Loan key={item.id} item = {item} frameNumber={frameNumber} />
            ))}
        </section>
    );
}

export default LoanDetail;