from blog.database import engine
from . import models

# WARNING: This will delete ALL data in the DB
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

print("Database reset and recreated!")