from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    name: str


class BaseUser(CreateUser):
    id: int


class GetUser(BaseUser):
    score: int = Field(default=0)
