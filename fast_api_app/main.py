import uvicorn
from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from rsp_models.user import GetUser

app = FastAPI()
port = int(os.environ.get("BACK_PORT", 8007))

origins = [
    "*",
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user/id/{id}", response_model=GetUser)
async def get_user_by_id(id: int):
    if id == 1:
        name = "Mike"
    else:
        name = "Team"
    return GetUser(id=id, name=name)


@app.get("/user/name/{name}", response_model=GetUser)
async def get_user_by_name(name: str):
    if name == "Mike":
        id = 1
    else:
        id = 2
    return GetUser(id=id, name=name)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
