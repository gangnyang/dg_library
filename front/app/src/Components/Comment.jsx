import React, {useState, useEffect} from "react";
import "./css/Comment.css";
import axios from "axios";
import { useToken } from "../TokenContext";

function Comment({comment, mode, onUpdate}) {
    const [showEditInput, setShowEditInput] = useState(false);
    const [user, setUser] = useState([]);
    const [updateText, setUpdateText] = useState("");
    const [replyText, setReplyText] = useState("");
    const {token} = useToken();

    useEffect(() => {
            axios
                .get(`http://127.0.0.1:8000/api/users/${comment.user_id}`)
                .then((response) => {
                    setUser(response.data);
                })
                .catch((error) => console.error("사용자 정보 가져오기 실패:", error));
    }, [comment.user_id]);

    const handleEditSubmit=()=>{
            axios
            .put(`http://127.0.0.1:8000/api/comments/`,
                { comment_id: comment.id, context: updateText.trim() }, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                alert("댓글 수정이 완료되었습니다.");
                setUpdateText("");
                setShowEditInput(false);
                onUpdate();
            })
            .catch((error) => alert("댓글 수정에 실패했습니다. 사유: " + error));
        }

    const handleReplySubmit=()=>{
            axios
            .post(`http://127.0.0.1:8000/api/comments/add`, 
                { book_id: comment.book_id, context: replyText.trim(), parent_id: comment.id }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            })
            .then((response) => {
                alert("답글 작성이 완료되었습니다.");
                setReplyText("");
                setShowReplyInput(false);
                onUpdate();
            })
            .catch((error) => alert("답글 작성에 실패했습니다. 사유: "+ error));
    }

    const handleEditClick= () => {
        setShowReplyInput((prev) => false);
        setShowEditInput((prev) => !prev);
    }

    const [showReplyInput, setShowReplyInput] = useState(false);

    const handleReplyClick= () => {
        setShowEditInput((prev) => false);
        setShowReplyInput((prev) => !prev);
    };
    const handleDeleteClick= () => {
        axios
            .delete(`http://127.0.0.1:8000/api/comments/${comment.id}`, 
                {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                alert("댓글 삭제가 완료되었습니다.");
                onUpdate();
            })
            .catch((error) => alert("댓글 삭제에 실패했습니다. 사유: "+ error));
    };
    return (
        <div className="Comment_frame">
            <div className="Comment_userFrame">
                <div className="Comment_NameBox">
                    <div className="Comment_NameBox2">
                        <div className="Comment_NameBox3">
                            <div className="Comment_NameBox4">
                                <p className="Comment_Name">{user.username}</p>
                            </div>
                        </div>
                        <p className="Comment_text">{comment.context}</p>
                    </div>
                </div>
                <div className="Comment_InfoBox">
                    <p className="Comment_updated">{comment.updated}</p>
                    <button className="Comment_reply" onClick={handleEditClick}>수정</button>
                    {mode==="parent" && <button className="Comment_reply" onClick={handleReplyClick} >답글</button>}
                    <button className="Comment_reply" onClick={handleDeleteClick}>삭제</button>
                </div>
            </div>

            {showEditInput &&(
                <div className="CommentInputBox">
                <input className="CommentInput" type="text" placeholder="댓글 수정..."
                value={updateText} onChange={ (e) => { setUpdateText(e.target.value); }}
                />
                <input className="CommentInputButton" type="submit" value="수정하기" onClick={handleEditSubmit} ></input>
                </div>
            )}

            {showReplyInput &&(
                <div className="CommentInputBox">
                <input className="CommentInput" type="text" placeholder="답글 작성..."
                value={replyText} onChange={ (e) => { setReplyText(e.target.value); }}
                />
                <input className="CommentInputButton" type="submit" value="답글달기" onClick={handleReplySubmit} ></input>
                </div>
            )} 

            <div className="Comment_divider"/>
        </div>
    );
}

export default Comment;