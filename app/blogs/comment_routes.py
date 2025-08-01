from typing import List
from fastapi import APIRouter, Depends
from users.models import User
from core.database import get_session
from sqlmodel import Session, select
from blogs.models import Blog, Comment
from blogs.schema import CommentData
from auth.auth import get_current_user
from fastapi.exceptions import HTTPException
from datetime import timezone, datetime

router = APIRouter()


@router.post("/create/{blog_id}")
async def create_comment(
    blog_id: int,
    content: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
        Post method to create comment in blog needs to be authenticated to perform this action.
    """
    try:
        new_comment = Comment(
            blog_id=blog_id,
            content=content, 
            commmented_by=current_user.id,
        ) 
        
        session.add(new_comment)
        session.commit()
                
        return {"detail": "Successfully commented on the blog"}

    except HTTPException:
        raise

    except Exception as e:
        raise (HTTPException(status_code=500, detail=f"Something went wrong {str(e)}"))



@router.get("/read/{blog_id}", response_model=List[CommentData])
async def read_comment(blog_id:int, session: Session = Depends(get_session)):
    
    try:
        if not (session.exec(select(Blog).where(Blog.id == blog_id)).first()):
            raise HTTPException(status_code=404, detail="Blog not found")
        
        comments = session.exec(select(Comment).where(Comment.blog_id == blog_id)).all()

        return comments
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {str(e)}")


@router.patch("/update/{comment_id}")
async def update_comment(
    comment_id: int,
    content: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        comment = session.exec(select(Comment).where(Comment.id == comment_id)).first()
        
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.commmented_by != current_user.id:
            raise HTTPException(status_code=401, detail="You are not the owner of the comment")

        comment.content = content
        comment.last_modified = datetime.now(timezone.utc)
        session.add(comment)
        session.commit()

        return {"detail": "Successfulyy updated comment"}
        

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong{str(e)}")


@router.delete("/delete/{comment_id}")
async def delete_comment(
    comment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        comment = session.exec(select(Comment).where(Comment.id == comment_id)).first()

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.commmented_by != current_user.id:
            raise HTTPException(status_code=401, detail="You are not the owner of the comment")
        
        session.delete(comment)
        session.commit()
        return {"detail": "Successfully deleted comment"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong{str(e)}")