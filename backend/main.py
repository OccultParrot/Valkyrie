import os
from typing import Annotated, Sequence, cast

import dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy import create_engine
from sqlmodel import Session, select

from models.user_model import User

dotenv.load_dotenv()

app = FastAPI()

engine = create_engine(os.environ['DATABASE_URL'])


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/api/users/")
def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/api/users/")
def get_users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> Sequence[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/api/users/{user_id}")
def get_user(user_id: int, session: SessionDep) -> User:
    user = cast(User | None, session.get(User, user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = cast(User | None, session.get(User, user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}