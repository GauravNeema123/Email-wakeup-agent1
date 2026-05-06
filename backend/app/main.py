from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.email_routes import router as email_router
from app.routes.thread_routes import router as thread_router

from app.database.connection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router)
app.include_router(thread_router)

@app.get("/")
def home():
    return {"message": "Email Wake-Up Agent Running"}
