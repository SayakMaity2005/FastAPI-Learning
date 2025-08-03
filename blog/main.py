from fastapi import FastAPI

app = FastAPI()

@app.post("/blogs")
def create():
    return "Creating a blog"