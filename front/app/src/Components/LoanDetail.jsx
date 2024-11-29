import React, {useState, useEffect} from "react";
import './css/LoanDetail.css';
import Loan from './Loan';
import Interloan from "./Interloan";
import MypageProgram from "./MypageProgram";
import axios from "axios";
import { useToken } from "../TokenContext";

function LoanDetail({frameNumber}){
    const [data, setData] = useState([]);
    const [loanData, setLoanData] = useState([]);
    const [interloanData, setInterLoanData] = useState([]);
    const [programData, setProgramData] = useState([]);
    const {token} = useToken();

    const handleProgramUpdate = (id) => {
        axios
        .get(`http://127.0.0.1:8000/api/programs/user-program`, {
            headers:{
                Authorization: `Bearer ${token}`,
            }
        })
        .then((response) => {
            setProgramData(response.data);
        })
        .catch((error) => console.error(error));
    };
    
    // Loan 업데이트 알림 처리
    const handleLoanUpdate = () => {
        axios
        .get(`http://127.0.0.1:8000/api/loan/user-loan`, {
            headers:{
                Authorization: `Bearer ${token}`,
            }
        })
        .then((response) => {
            setLoanData(response.data);
        })
        .catch((error) => console.error(error));
    };

    // Interloan 업데이트 알림 처리
    const handleInterloanUpdate = () => {
        axios
        .get(`http://127.0.0.1:8000/api/loan/user-interloan`, {
            headers:{
                Authorization: `Bearer ${token}`,
            }
        })
        .then((response) => {
            setInterLoanData(response.data);
        })
        .catch((error) => console.error(error));
    };
    

    useEffect(() => {
        handleLoanUpdate();
    }, [token]);

    useEffect(() => {
        handleInterloanUpdate();
    }, [token]);

    useEffect(() => {
        handleProgramUpdate();
    }, [token]);

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
    }, [frameNumber, loanData, interloanData, programData]);



    return(
        <section className="LoanDetailFrame">
            <h1 className="LoanDetailTitle">
                {frameNumber === 2 && "내 대출 기록"}
                {frameNumber === 3 && "내 상호 대차 기록"}
                {frameNumber === 4 && "프로그램"}
            </h1>
            {frameNumber === 2 && data.map((item) => <Loan key={item.id} item={item} onUpdate={handleLoanUpdate} />)}
            {frameNumber === 3 && data.map((item) => <Interloan key={item.id} item={item} onUpdate={handleInterloanUpdate} />)}
            {frameNumber === 4 && data.map((item) => <MypageProgram key={item.id} item={item} onDelete={handleProgramUpdate}/>)}
        </section>
    );
}

export default LoanDetail;