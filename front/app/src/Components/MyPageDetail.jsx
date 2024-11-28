import React, {useState} from "react"
import './css/MyPageDetail.css';
import Category from "./Category";
import UpdateUser from "./UpdateUser";
import LoanDetail from "./LoanDetail";

function MyPageDetail(){
    const [frameNumber, setFrameNumber] = useState(1);

    const handleFrameChange = (newFrameNumber) => {
        setFrameNumber(newFrameNumber);
    };
    return(
        <section className="MyPageFrame">
            <div className="MyPageContentFrame">
            <Category frameNumber ={frameNumber} onFrameChange={handleFrameChange} />
            
            {frameNumber === 1 && <UpdateUser />}
            {frameNumber === 2 && <LoanDetail frameNumber={frameNumber}/>}
            {frameNumber === 3 && <LoanDetail frameNumber={frameNumber} />}
            {frameNumber === 4 && <LoanDetail frameNumber={frameNumber} />}


            </div>
        </section>
    );
}

export default MyPageDetail;