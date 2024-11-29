import react, {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import './css/LoginForm.css';
import axios from "axios";
import { useToken } from "../TokenContext";


function LoginForm() {
    const {setToken} = useToken();
    const navigate = useNavigate();
    const [id, setId] = useState("");
    const [password, setPassword] = useState("");
    const handleRegisterClick = () => {
        navigate("/register");
    }

    const handleLoginClick = () => {
        const requestData = {
            username: id,
            password: password,
        };
        axios
        .post(`http://127.0.0.1:8000/api/users/login`, requestData, {
            headers: {
                "Content-Type": "application/json", // JSON 형식 명시
            },
        })
        .then((response) => {
            alert(response.data["message"]);
            setToken(response.data["token"]);
            navigate("/"); // 메인페이지로 이동
        })
        .catch((error) => {
            console.error("로그인 실패: ", error);
            alert("로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.");
        });
    }

    const handleIdChange = (event) =>{
        setId(event.target.value);
    }

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    }
    return (
        <section className="LoginFormFrame">
            <div className="LoginFormMain">
                <div className="LoginForm">
                    <div className="LoginFormHead">
                        <h2 className="LoginFormHeadTitle">안녕하세요!</h2>
                    </div>
                    <div className="LoginFormForm">
                        <div className="LoginFormGroup">
                            <div className="LoginFormInputFrame">
                                <div className="LoginFormInputBox">
                                    <p className="LoginFormInputDescription">아이디나 이메일</p>
                                </div>
                                <input className="LoginFormInput" type="text" placeholder="아이디나 이메일을 입력하세요" value={id} onChange={handleIdChange} />
                            </div>
                        </div>
                    </div>
                    <div className="LoginFormForm">
                        <div className="LoginFormGroup">
                            <div className="LoginFormInputFrame">
                                <div className="LoginFormInputBox">
                                    <p className="LoginFormInputDescription">비밀번호</p>
                                </div>
                                <input className="LoginFormInput" type="password" placeholder="비밀번호를 입력하세요" value={[password]} onChange={handlePasswordChange} />
                            </div>
                        </div>
                    </div>
                    <button className="LoginFormButton" onClick={handleLoginClick} >
                        <p className="LoginFormButtonText">로그인</p>
                    </button>
                </div>
                <button className="LoginFormNoID" onClick={handleRegisterClick}>
                    <h6 className="LoginFormNoidText">계정이 없으신가요? 회원가입</h6>
                </button>
            </div>
        </section>
    )
}

export default LoginForm;