import react from "react";
import {useNavigate} from "react-router-dom";
import './css/LoginForm.css';


function LoginForm() {
    const navigate = useNavigate();

    const handleRegisterClick = () => {
        navigate("/register");
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
                        <p className="LoginFormButtonText">로그인</p>
                    </button>
                </div>
                <button className="LoginFormNoID" onClick={handleRegisterClick}>
                    <h6 classname="LoginFormNoidText">계정이 없으신가요? 회원가입</h6>
                </button>
            </div>
        </section>
    )
}

export default LoginForm;