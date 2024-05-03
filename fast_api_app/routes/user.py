from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException

from rsp_models.user import GetUser, CreateUser
from db_models.db_funcs import (
    create_user as create_db_user,
    get_user_by_id as get_db_user_by_id,
    get_user_by_name as get_db_user_by_name,
    get_user_with_max_score as get_db_user_with_max_score,
    get_max_user_score,
)
from db_connect import Session, engine, get_db


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
    db_score = get_db_user_with_max_score(db)

    if not db_score:
        raise HTTPException(status_code=409, detail="No user with max score exists")

    db_user = get_db_user_by_id(db, db_score.user_id)

    if not db_user:
        raise HTTPException(status_code=409, detail=f"User with id {db_score.user_id} and score {db_score.value:_.0f} does not exist")

    return GetUser(id=db_user.id, name=db_user.name, score=db_score.value)
