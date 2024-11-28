import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const ScrollToTop = () => {
    const { pathname } = useLocation();

    useEffect(() => {
        window.scrollTo(0, 0); // 스크롤을 최상단으로 이동
    }, [pathname]); // 경로가 바뀔 때마다 실행

    return null; // UI 렌더링은 하지 않음
};

export default ScrollToTop;
