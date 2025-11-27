from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import post, user, vote, auth

from .database import engine

models.Base.metadata.create_all(bind=engine)   # Creates all models in the DB. Used in Render deployment. Commented after Alembic implementation.

app = FastAPI(title="Social Media App / NAT")

origins = ["*"]     # All domains allowed.

app.add_middleware(
    CORSMiddleware,         # Function that runs before every request
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
    # return {"message": "Successfully deployed from CI/CD pipeline !"}
    return {"message": "Pushing out to Ubuntu 😀"}