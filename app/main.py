from fastapi import FastAPI
from . import models
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db
from .routers import post, user, auth, vote


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {"message": "Hello Worlld!!!!!!!"}
