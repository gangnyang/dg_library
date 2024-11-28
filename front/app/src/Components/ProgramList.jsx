import React, {useState, useEffect} from "react";
import Program from "./Program";
import './css/BookList.css';
import axios from "axios";

function ProgramList({squery, limit}){
    const [programs, setPrograms] = useState([]);

    useEffect(() => {
        axios
        .get(`http://127.0.0.1:8000/api/programs?limit=${limit}`)
        .then((response) => setPrograms(response.data))
        .catch((error) => console.error(error));
    }, [limit]);


    return(
        <div className="BookList">
            {programs.map((program)=>(
                <Program key={program.id} program = {program} />
            ))}
        </div>
    );
}

export default ProgramList;