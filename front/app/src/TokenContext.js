import React, { createContext, useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";

// Context 생성
const TokenContext = createContext();

// 토큰 만료 확인 함수
const isTokenExpired = (token) => {
    if (!token) return true;
    try {
        const base64Url = token.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const decodedPayload = JSON.parse(window.atob(base64));
        const now = Math.floor(Date.now() / 1000); // 현재 시간 (초 단위)
        return decodedPayload.exp < now; // 만료 시간이 현재 시간보다 이전인지 확인
    } catch (error) {
        console.error("토큰 디코딩 실패:", error);
        return true; // 디코딩 실패 시 만료된 것으로 간주
    }
};

// Context Provider 컴포넌트
export const TokenProvider = ({ children }) => {
    const [token, setToken] = useState(() => {
        return sessionStorage.getItem("token") || "";
    });
    const navigate = useNavigate();

    useEffect(() => {
        if(token && !isTokenExpired(token)){
            sessionStorage.setItem("token", token);
        }else{
            sessionStorage.removeItem("token");
            setToken(null);
        }
    }, [token, navigate]);

    return (
        <TokenContext.Provider value={{ token, setToken }}>
            {children}
        </TokenContext.Provider>
    );
};

// Context 값을 쉽게 가져오는 커스텀 훅
export const useToken = () => useContext(TokenContext);
