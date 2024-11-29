import React, {useState} from "react";
import {useNavigate} from "react-router-dom";
import './css/UpdateUser.css';
import axios from "axios";
import {useToken} from  "../TokenContext";

function UpdateUser(){
    const [name, setName] = useState();
    const [phone, setPhone] = useState();
    const [password, setPassword] = useState();
    const {token, setToken} = useToken();
    const navigate = useNavigate();

    const handleNameChange = (event) => {
        setName(event.target.value);
    }
    const handlePhoneChange = (event) => {
        setPhone(event.target.value);
    }
    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    }

    const handleUpdateUser = () => {
        const requestData = {
            password: password,
            phone: phone,
            name: name,
        };
        axios
        .put(`http://127.0.0.1:8000/api/users/update`, requestData, {
            headers: {
                "Content-Type": "application/json", 
                Authorization: `Bearer ${token}`,
            },
        })
        .then((response) => {
            console.log(response.data["message"]);
            alert("회원정보 수정을 완료했습니다. 다시 로그인해주세요.")
            setToken(null);
            navigate("/login"); // 메인페이지로 이동
        })
        .catch((error) => {
            console.error("정보 수정 실패: ", error);
            alert("회원 정보 수정에 실패했습니다. 사유: " + error);
        });
    }

    
    return(
        <section className="UpdateUserFrame">
            <div className="UpdateUserTitle">
                <h1 className="UpdateUserTitleText">회원정보 변경</h1>
            </div>
            <div className="UpdateUserInputFrame">
                <div className="UpdateUserInputBox">
                    <div className="UpdateUserInputSpace">
                        <div className="UpdateUserInputSpace2">
                            <p className="UpdateUserInputTitle">이름</p>
                            <input className="UpdateUserInput" type="text" placeholder="이름 입력"
                            value={name} onChange={handleNameChange}
                            />
                        </div>
                    </div>
                    <div className="UpdateUserInputSpace">
                        <div className="UpdateUserInputSpace2">
                            <p className="UpdateUserInputTitle">전화번호</p>
                            <input className="UpdateUserInput" type="text" placeholder="전화번호 입력" 
                            value={phone} onChange={handlePhoneChange} />
                        </div>
                    </div>
                    <div className="UpdateUserInputSpace">
                        <div className="UpdateUserInputSpace2">
                            <p className="UpdateUserInputTitle">비밀번호</p>
                            <input className="UpdateUserInput" type="text" placeholder="비밀번호 입력" 
                            value={password} onChange={handlePasswordChange} />
                        </div>
                    </div>
                </div>
                <div className="UpdateUserdivider"/>
                <button className="UpdateUserButton" onClick={handleUpdateUser}>
                    <p className="UpdateUserButtonText">정보 수정</p>
                </button>
            </div>
        </section>
    );
}

export default UpdateUser;