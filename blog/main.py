from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from blog.schemas import Blog, User, ShowUser
from . import models
from blog.authentication import Hash
from blog.database import engine, SessionLocal
from blog.routers import blog, login, user, register

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/blogs", status_code=status.HTTP_201_CREATED, tags=["Blog"])
# def create_blog(request: Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.get("/blogs", tags=["Blog"])
# def get_blog(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

# @app.get("/blogs/{id}", tags=["Blog"])
# def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail": f"Blog with id {id} is not available"}
#     response.status_code = status.HTTP_200_OK
#     return blog

# @app.delete("/blogs/{id}", tags=["Blog"])
# def remove_blog(id, response: Response, db: Session = Depends(get_db)):
#     del_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not del_blog:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail": f"Blog with id {id} is not available"}
#     db.delete(del_blog)
#     db.commit()
#     response.status_code = status.HTTP_200_OK
#     return {"message": f"Blog with id {id} has been deleted successfully"}


# @app.put("/blogs/{id}", tags=["Blog"])
# def update_blog(id, response: Response, request: Blog, db: Session = Depends(get_db)):
#     new_blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not new_blog.first():
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail": f"Blog with id {id} is not available"}
#     new_blog.update({"title":request.title, "body": request.body}, synchronize_session=False)
#     db.commit()
#     response.status_code = status.HTTP_202_ACCEPTED
#     return {"message": f"Blog with id {id} has been updated successfully"}


# user data
# @app.post("/user", response_model=ShowUser, tags=["User"])
# def create_user(request: User, db: Session = Depends(get_db)):
#     new_user = models.User(name=request.name, email=request.email, password=Hash.hash_password(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/user/{id}", response_model=ShowUser, tags=["User"])
# def get_user(id, response: Response, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {id} not available"
#         )
#     response.status_code = status.HTTP_200_OK
#     return user

