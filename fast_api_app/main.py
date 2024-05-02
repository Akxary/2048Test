import uvicorn
from fastapi import FastAPI
import os
from routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from db_connect import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
