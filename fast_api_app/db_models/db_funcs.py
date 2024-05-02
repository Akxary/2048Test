from sqlalchemy.orm import Session
from sqlalchemy import func
import db_models.models as db_models
from rsp_models import user as schemas


def create_user(db: Session, user: schemas.CreateUser) -> db_models.User:
    db_user = db_models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> db_models.User:
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str) -> db_models.User:
    return db.query(db_models.User).filter(db_models.User.name == name).first()


def delete_user(db: Session, user_name: str) -> bool:
    db_user = get_user_by_name(db, user_name)
    if db_user:
        db.delete(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    return False


def get_max_user_score(db: Session, user_id: int) -> db_models.Score | None:
    # db_user = get_user_by_id(db, user_id)
    db_score = db.query(
        db_models.Score.user_id,
        func.max(db_models.Score.user_id).label("value")
    ).group_by(db_models.Score.user_id).filter(db_models.Score.user_id == user_id).first()
    if db_score:
        return db_score
    return None


def get_user_with_max_score(db: Session) -> db_models.Score | None:
    sq = db.query(
        db_models.Score,
        func.row_number()
        .over(
            partition_by=db_models.Score.user_id,
            order_by=[db_models.Score.value.desc(),db_models.Score.game_time.asc()]
        )
        .label("rn"),
    ).subquery()

    db_scores = db.query(sq.c.user_id, sq.c.game_time, sq.c.value).filter(sq.c.rn == 1).first()
    # print(db_scores.statement.compile())
    # db_scores = db_scores.first()

    if db_scores:
        return db_scores
    return None
