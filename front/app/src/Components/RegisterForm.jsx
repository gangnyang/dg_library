import react, {useState} from "react";
import {useNavigate} from "react-router-dom";
import './css/RegisterForm.css';
import './css/LoginForm.css';
import axios from "axios";

function RegisterForm() {
    const navigate = useNavigate();
    const [name, setName] = useState();
    const [id, setId] = useState();
    const [password, setPassword] = useState();

    const handleNameChange = (event) => {
        setName(event.target.value);
    }
    const handleIdChange = (event) => {
        setId(event.target.value);
    }
    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    }

    const handleLoginClick = () => {
        navigate("/login");
    }

    const handleRegisterClick = () => {
        const requestData = {
            username: id,
            password: password,
            name: name,
        };
        axios
        .post(`http://127.0.0.1:8000/api/users`, requestData, {
            headers: {
                "Content-Type": "application/json", // JSON 형식 명시
            },
        })
        .then((response) => {
            console.log(response.data["message"]);
            alert("회원가입이 완료되었습니다. 입력하신 아이디와 비밀번호로 로그인해주세요.")
            navigate("/login"); // 메인페이지로 이동
        })
        .catch((error) => {
            console.error("회원가입 실패: ", error);
            alert("회원가입에 실패했습니다. 사유: " + error);
        });
    }
    return (
        <section className="LoginFormFrame">
            <div className="LoginFormMain">
                <div className="LoginForm">
                    <div className="LoginFormHead">
                        <h2 className="LoginFormHeadTitle">계정 생성하기</h2>
                    </div>
                    <div className="LoginFormForm">
                        <div className="LoginFormGroup">
                            <div className="LoginFormInputFrame">
                                <div className="LoginFormInputBox">
                                    <p className="LoginFormInputDescription">이름</p>
                                </div>
                                <input className="LoginFormInput" type="text" placeholder="이름을 입력하세요" value={name} onChange={handleNameChange}/>
                            </div>
                        </div>
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
                                <input className="LoginFormInput" type="password" placeholder="비밀번호를 입력하세요" value={password} onChange={handlePasswordChange} />
                            </div>
                        </div>
                    </div>
                    <button className="LoginFormButton" onClick={handleRegisterClick}>
                        <p className="LoginFormButtonText">회원가입</p>
                    </button>
                </div>
                <button className="LoginFormNoID" onClick={handleLoginClick}>
                    <h6 className="LoginFormNoidText">이미 계정이 있으신가요? 로그인</h6>
                </button>
            </div>
        </section>
    )
}

export default RegisterForm;