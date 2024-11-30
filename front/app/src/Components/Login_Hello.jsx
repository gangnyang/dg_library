import react from "react";
import './css/Login_Hello.css';

function Login_Hello(){
    return(
        <section className="Login_HelloFrame">
            <div className="sidenav-bg">
                <h1 className="LoginHelloTitle">도서관에 오신 걸 환영해요</h1>
                <p className="LoginHelloDescription">도서관 서비스를 이용하시려면 로그인이 필요해요</p>
                
            </div>
            <img className="LoginHelloImage" src='/images/login_image.jpg' alt='login_image'/>
        </section>
    )
}

export default Login_Hello;