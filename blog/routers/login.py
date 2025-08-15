from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from blog.schemas import ShowUser
from sqlalchemy.orm import Session
from .. import models, database
from blog.authentication import Hash, create_access_token

router = APIRouter(tags=["Login"])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):  # , request: Login
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.varify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
    