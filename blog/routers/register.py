from fastapi import APIRouter, Depends
from blog.schemas import Register
from sqlalchemy.orm import Session
from .. import database, models
from blog.authentication import Hash

router = APIRouter()

get_db = database.get_db

@router.post("/register")
def register(request: Register, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.hash_password(request.password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}