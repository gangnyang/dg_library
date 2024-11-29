import React, {useState} from "react";
import './css/Libmap.css';
import axios from "axios";

function Libmap(){
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [description, setDescription] = useState("");

    const handleSendingMail = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/send-mail/", {
                name,
                email,
                description,
            });
            alert(response.data.message);
        } catch (error) {
            console.error("메일 전송 실패:", error);
            alert("메일 전송에 성공했습니다.");
        }
    };
    return(
        <section className="LibmapFrame">
            <div className="OpinionFrame">
                <h1 className="OpinionTitle">의견 제출</h1>
                <p className="OpinionDescription">의견이 있다면 전달해주세요!</p>
                <div className="OpinionForm">
                    <input className="OpinionInput" type="text" placeholder = "이름" value={name} onChange={(e)=>setName(e.target.value)} />
                    <input className="OpinionInput" type="text" placeholder = "이메일" value={email} onChange={(e)=>setEmail(e.target.value)} />
                    <input className="OpinionInput" type="text" placeholder = "내용" value={description} onChange={(e)=>setDescription(e.target.value)} />
                </div>
                <button className="OpinionSubmit" onClick={handleSendingMail} >
                    <p className="OpinionSubmitText">제출하기</p>
                    </button>
                </div>
            <div className="LibmapFrame2">
                <div className="mapFrame">
                    <img className="map" src="images/SKmap.jpg" alt="map"/>
                </div>
            </div>
        </section>
    );
}

export default Libmap;