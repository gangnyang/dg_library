import React, {useState, useEffect} from "react";
import {useParams} from "react-router-dom";
import Comment from "./Comment";
import './css/CommentList.css';
import axios from "axios";
import { useToken } from "../TokenContext";

function CommentList({Book_id}){
    const [comments, setComments] = useState([]);
    const [count, setCount] = useState(0);
    const [text, setText] = useState("");
    const {token} = useToken();
    const fetchComments = () => {
        axios
            .get(`http://127.0.0.1:8000/api/comments?book_id=${Book_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            })
            .then((response) => {
                setComments(response.data["result"]); // 댓글 데이터
                setCount(response.data["count"]); // 댓글 개수
                console.log(token);
            })
            .catch((error) => { 
                console.error("댓글 가져오기 실패:", error);
                console.error(Book_id);
            });
    };

    useEffect(() => {
        fetchComments();
    }, [Book_id]);

    const handleSubmitClick = () => {
        axios
            .post(`http://127.0.0.1:8000/api/comments/add`,
                { book_id: Book_id, context: text.trim() }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            })
            .then((response) => {
                alert("댓글 작성이 완료되었습니다.");
                setText("");
                fetchComments();
            })
            .catch((error) => alert("댓글 작성에 실패했습니다. 사유: "+ error));
    }
    return(
        <section className="CommentListFrame">
            <div className="CommentStartFrame">
                <h1 className="CommentStart">댓글을 달아보세요. 책 추천 정보를 담아주시면 더욱 좋아요!</h1>
            </div>
            <div className="CommentInputBox">
            <input className="CommentInput" type="text" placeholder="댓글 작성..." value={text} onChange={(e)=>{setText(e.target.value)}} />
            <input className="CommentInputButton" type="submit" value="작성하기" onClick={handleSubmitClick} ></input>
            </div>
            <div className="CommentList">
                <p className="CommentNumber">{count["count"]}개의 댓글</p>
                {comments.map((comment)=>(
                    <div className="CommentWithReply">
                    <Comment key={comment.id} comment = {comment} mode="parent" onUpdate={fetchComments}/>
                    {comment.replies &&
                        comment.replies.map((reply) => (
                            <div key={reply.id} className="ReplyFrame">
                                <img className="ReplyImage" src="/images/reply.svg" alt=""/>
                                <Comment comment={reply} mode="child" onUpdate={fetchComments} />
                            </div>
                        ))}
                    </div>
                ))}
                
            </div>
        </section>
    );
}

export default CommentList;