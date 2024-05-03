from fastapi import APIRouter, Depends, HTTPException
from rsp_models.score import CreateScore, GetScore
from db_connect import Session, engine, get_db
from db_models.db_funcs import (
    add_score,
    get_user_scores as get_db_user_scores,
    get_user_by_id,
)

router = APIRouter(prefix="/score", tags=["score"])


@router.post("/", response_model=GetScore)
async def add_user_score(score: CreateScore, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, score.user_id)
    if not db_user:
        raise HTTPException(409, f"User with id {score.user_id} not found")

    db_score = add_score(db, score)

    return GetScore(
        user_id=db_score.user_id, score=db_score.value, game_time=db_score.game_time
    )


@router.get("/{user_id}", response_model=list[GetScore])
async def get_user_scores(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(409, f"User with id {user_id} not found")

    db_score = get_db_user_scores(db, user_id)

    if not db_score:
        raise HTTPException(409, f"User with id {user_id} does not have any scores")

    return GetScore(
        user_id=db_score.user_id, score=db_score.value, game_time=db_score.game_time
    )
