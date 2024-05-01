from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    id: int


class CreateUser(BaseUser):
    name: str


class GetUser(CreateUser):
    score:int = Field(default=0)
