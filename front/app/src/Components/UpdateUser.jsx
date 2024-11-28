import React from "react";
import './css/UpdateUser.css';

function UpdateUser(){
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
                            <input className="UpdateUserInput" type="text" placeholder="이름 입력" />
                        </div>
                    </div>
                    <div className="UpdateUserInputSpace">
                        <div className="UpdateUserInputSpace2">
                            <p className="UpdateUserInputTitle">전화번호</p>
                            <input className="UpdateUserInput" type="text" placeholder="전화번호 입력" />
                        </div>
                    </div>
                    <div className="UpdateUserInputSpace">
                        <div className="UpdateUserInputSpace2">
                            <p className="UpdateUserInputTitle">비밀번호</p>
                            <input className="UpdateUserInput" type="text" placeholder="비밀번호 입력" />
                        </div>
                    </div>
                </div>
                <div className="UpdateUserdivider"/>
                <button className="UpdateUserButton">
                    <p className="UpdateUserButtonText">정보 수정</p>
                </button>
            </div>
        </section>
    );
}

export default UpdateUser;