import os
from typing import Annotated, Sequence, cast

import requests
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
    user_name = get_steam_user(user.steam_id)
    if user_name is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user = session.get(User, user.discord_id)
    if existing_user:
        existing_user.steam_id = user.steam_id
        existing_user.steam_name = user_name
        session.add(existing_user)
    else:
        user.steam_name = user_name
        session.add(user)

    session.commit()
    session.refresh(existing_user if existing_user else user)
    return existing_user if existing_user else user


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


def get_steam_user(steam_id: int) -> str | None:
    response = requests.get(
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
        params={
            "key": os.environ["STEAM_API_KEY"],
            "steamids": steam_id
        }
    )

    print(f"Steam API status: {response.status_code}")
    print(f"Steam API response: {response.text}")  # Add this temporarily

    data = response.json()
    print(data)
    players = data["response"]["players"]

    if not players:
        print(f"User has no steam id: {steam_id}")
        return None

    return players[0]["personaname"]
