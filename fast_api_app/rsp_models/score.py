from datetime import datetime

from pydantic import BaseModel, Field


class CreateScore(BaseModel):
    user_id: int = Field(..., alias='user_id')
    score: int = Field(..., alias='score')


class GetScore(CreateScore):
    game_time: datetime = Field(..., alias='game_time')
