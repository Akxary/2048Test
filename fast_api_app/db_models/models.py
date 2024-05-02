from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from db_connect import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    # связь с классом Score по полю score.user (в db такого нет)
    scores = relationship("Score", back_populates="user")


class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    game_time = Column(TIMESTAMP, nullable=False, default=datetime.now)
    value = Column(Integer, nullable=False)
    # связь с классом User по полю user.scores (в db такого нет)
    user = relationship("User", back_populates="scores")
