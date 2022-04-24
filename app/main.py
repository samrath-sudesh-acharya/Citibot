from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from app.search import search

app = FastAPI()

@app.get("/search={query}")
def intro(query:str):
    result = search(query)
    return result

origins = ["*"]

app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)