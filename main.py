from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    name: str
    description: str | None

@app.get("/home")
def get_home():
    return {"data": "Hello world!"}