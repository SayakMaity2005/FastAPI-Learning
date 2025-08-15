from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from blog.schemas import Blog, User
from .. import models


def create_blog(request: Blog, db: Session, current_user: User):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all_blog(current_user: User):
    # blogs = db.query(models.Blog).all()
    return [{"title": blog.title, "body": blog.body} for blog in current_user.blogs]


def get_blog_by_id(id: int, response: Response, db: Session, current_user: User):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available"
        )
    if blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this blog"
        )
    response.status_code = status.HTTP_200_OK
    return blog


def remove_blog(id: int, response: Response, db: Session, current_user: User):
    del_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not del_blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} is not available"}
    if del_blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this blog"
        )
    db.delete(del_blog)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {"message": f"Blog with id {id} has been deleted successfully"}


def update_blog(id: int, response: Response, request: Blog, db: Session, current_user: User):
    new_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not new_blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} is not available"}
    if new_blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this blog"
        )
    new_blog.update({"title":request.title, "body": request.body}, synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": f"Blog with id {id} has been updated successfully"}
