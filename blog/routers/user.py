from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from blog.schemas import User, ShowUser
from .. import database
from blog.repsitories import user_repo

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

get_db = database.get_db

@router.post("/", response_model=ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    return user_repo.create_user(request, db)

@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    return user_repo.get_user(id, response, db)
