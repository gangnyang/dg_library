import react from "react";
import {useNavigate} from "react-router-dom";
import './css/RegisterForm.css';
import './css/LoginForm.css';

function RegisterForm() {
    const navigate = useNavigate();

    const handleRegisterClick = () => {
        navigate("/login");
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
                                <input className="LoginFormInput" type="text" placeholder="이름을 입력하세요"/>
                            </div>
                        </div>
                    </div>
                    <div className="LoginFormForm">
                        <div className="LoginFormGroup">
                            <div className="LoginFormInputFrame">
                                <div className="LoginFormInputBox">
                                    <p className="LoginFormInputDescription">아이디나 이메일</p>
                                </div>
                                <input className="LoginFormInput" type="text" placeholder="아이디나 이메일을 입력하세요"/>
                            </div>
                        </div>
                    </div>
                    <div className="LoginFormForm">
                        <div className="LoginFormGroup">
                            <div className="LoginFormInputFrame">
                                <div className="LoginFormInputBox">
                                    <p className="LoginFormInputDescription">비밀번호</p>
                                </div>
                                <input className="LoginFormInput" type="text" placeholder="비밀번호를 입력하세요"/>
                            </div>
                        </div>
                    </div>
                    <button className="LoginFormButton">
                        <p className="LoginFormButtonText">회원가입</p>
                    </button>
                </div>
                <button className="LoginFormNoID" onClick={handleRegisterClick}>
                    <h6 classname="LoginFormNoidText">이미 계정이 있으신가요? 로그인</h6>
                </button>
            </div>
        </section>
    )
}

export default RegisterForm;