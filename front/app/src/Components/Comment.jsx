import React, {useState} from "react";
import "./css/Comment.css";

function Comment({comment}) {
    const [showEditInput, setShowEditInput] = useState(false);

    const handleEditClick= () => {
        setShowReplyInput((prev) => false);
        setShowEditInput((prev) => !prev);
    }

    const [showReplyInput, setShowReplyInput] = useState(false);

    const handleReplyClick= () => {
        setShowEditInput((prev) => false);
        setShowReplyInput((prev) => !prev);
    }
    return (
        <div className="Comment_frame">
            <div className="Comment_userFrame">
                <div className="Comment_NameBox">
                    <div className="Comment_NameBox2">
                        <div className="Comment_NameBox3">
                            <div className="Comment_NameBox4">
                                <p className="Comment_Name">{comment.user_id}</p>
                            </div>
                        </div>
                        <p className="Comment_text">{comment.context}</p>
                    </div>
                </div>
                <div className="Comment_InfoBox">
                    <p className="Comment_updated">{comment.updated}</p>
                    <button className="Comment_reply" onClick={handleEditClick}>수정</button>
                    <button className="Comment_reply" onClick={handleReplyClick} >답글</button>
                </div>
            </div>

            {showEditInput &&(
                <div className="CommentInputBox">
                <input className="CommentInput" type="text" placeholder="댓글 수정..."/>
                <input className="CommentInputButton" type="submit" value="수정하기" ></input>
                </div>
            )}

            {showReplyInput &&(
                <div className="CommentInputBox">
                <input className="CommentInput" type="text" placeholder="답글 작성..."/>
                <input className="CommentInputButton" type="submit" value="답글달기" ></input>
                </div>
            )} 

            <div className="Comment_divider"/>
        </div>
    );
}

export default Comment;