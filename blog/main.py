from fastapi import FastAPI, Depends, status, Response
from sqlalchemy.orm import Session
from blog.schemas import Blog
from . import models
from blog.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blogs")
def get_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blogs/{id}")
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} is not available"}
    response.status_code = status.HTTP_200_OK
    return blog

@app.delete("/blogs/{id}")
def remove_blog(id, response: Response, db: Session = Depends(get_db)):
    del_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not del_blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} is not available"}
    db.delete(del_blog)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {"message": f"Blog with id {id} has been deleted successfully"}


@app.put("/blogs/{id}")
def update_blog(id, response: Response, request: Blog, db: Session = Depends(get_db)):
    new_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not new_blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} is not available"}
    new_blog.update({"title":request.title, "body": request.body}, synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": f"Blog with id {id} has been updated successfully"}
