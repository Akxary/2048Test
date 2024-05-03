import json

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
import redis as redis_module
from db_connect import Session, get_db
from db_models.db_funcs import (
    create_user as create_db_user,
    get_user_by_id as get_db_user_by_id,
    get_user_by_name as get_db_user_by_name,
    get_user_with_max_score as get_db_user_with_max_score,
    get_max_user_score,
)
from env_settings import settings as s
from rsp_models.user import GetUser, CreateUser

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=GetUser)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = get_db_user_by_name(db, user.name)
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")
    return create_db_user(db, user)


@router.get("/id/{user_id}", response_model=GetUser)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_db_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=409, detail="User does not exist")
    # почему-то не работает get_max_user_score
    db_score = get_max_user_score(db, user_id)
    if not db_score:
        return GetUser(id=db_user.id, name=db_user.name)
    return GetUser(id=db_user.id, name=db_user.name, score=db_score.value)


@router.get("/name/{name}", response_model=GetUser)
async def get_user_by_name(name: str, db: Session = Depends(get_db)):
    db_user = get_db_user_by_name(db, name)
    if not db_user:
        raise HTTPException(status_code=409, detail="User does not exist")

    db_score = get_max_user_score(db, db_user.id)

    if not db_score:
        return GetUser(id=db_user.id, name=db_user.name)

    return GetUser(id=db_user.id, name=db_user.name, score=db_score.value)


@router.get("/max-score/", response_model=GetUser)
async def get_user_with_max_score(db: Session = Depends(get_db)):
    """
    Не работает, пока score пустой
    """
    redis = redis_module.from_url(s.redis_url)

    key:str = redis.get("max-score")
    if key:
        get_user = GetUser.model_validate_json(key)
    else:
        db_score = get_db_user_with_max_score(db)

        if not db_score:
            raise HTTPException(status_code=409, detail="No user with max score exists")

        db_user = get_db_user_by_id(db, db_score.user_id)

        if not db_user:
            raise HTTPException(
                status_code=409,
                detail=f"User with id {db_score.user_id} and score {db_score.value:_.0f} does not exist",
            )

        get_user = GetUser(id=db_user.id, name=db_user.name, score=db_score.value)

        redis.set("max-score", json.dumps(get_user.model_dump(), ensure_ascii=False))
        redis.expire("max-score", s.redis_timeout)
    return get_user
