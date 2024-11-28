import React from "react";
import Comment from "./Comment";
import './css/CommentList.css';

function CommentList(){
    const Comments = [
        {id:1, book_id:10, user_id: 3, parent_id: null, context: "내용", created:"2024-11-02", updated:"2024-11-03"},
        {id:1, book_id:10, user_id: 3, parent_id: null, context: "내용", created:"2024-11-02", updated:"2024-11-03"},
        {id:1, book_id:10, user_id: 3, parent_id: null, context: "내용", created:"2024-11-02", updated:"2024-11-03"},
        {id:1, book_id:10, user_id: 3, parent_id: null, context: "내용", created:"2024-11-02", updated:"2024-11-03"},
    ];
    return(
        <section className="CommentListFrame">
            <div className="CommentStartFrame">
                <h1 className="CommentStart">댓글을 달아보세요. 책 추천 정보를 담아주시면 더욱 좋아요!</h1>
            </div>
            <div className="CommentInputBox">
            <input className="CommentInput" type="text" placeholder="댓글 작성..."/>
            <input className="CommentInputButton" type="submit" value="작성하기" ></input>
            </div>
            <div className="CommentList">
                <p className="CommentNumber">3개의 댓글</p>
                {Comments.map((comment)=>(
                    <Comment key={comment.id} comment = {comment} />
                ))}
            </div>
        </section>
    );
}

export default CommentList;