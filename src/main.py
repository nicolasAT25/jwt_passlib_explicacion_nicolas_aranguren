from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import post, user, vote, auth

from .database import engine

models.Base.metadata.create_all(bind=engine)   # Crea todos los modelos en la DB.

app = FastAPI(title="Red Social / NAT")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido! 😀"}