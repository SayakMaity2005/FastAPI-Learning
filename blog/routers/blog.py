from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from blog.schemas import Blog, ShowBlog, User
from .. import  database
from blog.repsitories import blog_repo
from blog.authentication import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)

get_db = database.get_db

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
def create_blog(request: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return blog_repo.create_blog(request, db, current_user)

@router.get("/")
def get_all_blog(current_user: User = Depends(get_current_user)):
    return blog_repo.get_all_blog(current_user)

@router.get("/{id}", response_model=ShowBlog)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return blog_repo.get_blog_by_id(id, response, db, current_user)

@router.delete("/{id}")
def remove_blog(id: int, response: Response, db: Session = Depends(get_db),  current_user: User = Depends(get_current_user)):
    return blog_repo.remove_blog(id, response, db, current_user)

@router.put("/{id}")
def update_blog(id: int, response: Response, request: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return blog_repo.update_blog(id, response, request, db, current_user) # {"message": f"Blog with id {id} has been updated successfully"}
