from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from blog.schemas import User
from .. import models
from blog.authentication import Hash



def create_user(request: User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=Hash.hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, response: Response, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not available"
        )
    response.status_code = status.HTTP_200_OK
    return user
