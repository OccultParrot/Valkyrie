import os
from datetime import datetime, timezone, timedelta
from typing import Sequence, cast, Annotated

import requests
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from sqlmodel import select

from database import SessionDep
from models.user_model import User

router = APIRouter(prefix="/users", tags=["users"])

DAILY_AMOUNT = 10
DAILY_COOLDOWN = timedelta(hours=24)


@router.post("/", status_code=201)
def create_user(user: User, session: SessionDep) -> User:
    existing_user = session.exec(select(User).where(User.discord_id == user.discord_id)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists, use PATCH to update")

    steam_taken = session.exec(select(User).where(User.steam_id == user.steam_id)).first()
    if steam_taken:
        raise HTTPException(status_code=409, detail="This Steam account is already linked to another user")

    user_name = get_steam_user(user.steam_id)
    if user_name is None:
        raise HTTPException(status_code=404, detail="Steam user not found")

    user.steam_name = user_name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.patch("/{user_id}/verify")
def verify_user(user_id: int, steam_id: int, session: SessionDep) -> User:
    user = cast(User | None, session.get(User, user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    steam_taken = session.exec(
        select(User).where(User.steam_id == steam_id, User.id != user_id)
    ).first()
    if steam_taken:
        raise HTTPException(status_code=409, detail="This Steam account is already linked to another user")

    user_name = get_steam_user(steam_id)
    if user_name is None:
        raise HTTPException(status_code=404, detail="Steam user not found")

    user.steam_id = steam_id
    user.steam_name = user_name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.patch("/{user_id}/claim")
def claim_daily(user_id: int, session: SessionDep) -> User:
    user = cast(User | None, session.get(User, user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.now(timezone.utc)
    if user.last_daily is not None and now - user.last_daily < DAILY_COOLDOWN:
        remaining = DAILY_COOLDOWN - (now - user.last_daily)
        raise HTTPException(
            status_code=429,
            detail=f"Daily already claimed, try again in {remaining}",
        )

    user.balance += DAILY_AMOUNT
    user.last_daily = now
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/")
def get_users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> Sequence[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/lookup")
def lookup_user(session: SessionDep, steam_id: int | None = None, discord_id: int | None = None) -> User:
    if steam_id is None and discord_id is None:
        raise HTTPException(status_code=400, detail="Must provide steam_id or discord_id")

    query = select(User)
    if steam_id is not None:
        query = query.where(User.steam_id == steam_id)
    if discord_id is not None:
        query = query.where(User.discord_id == discord_id)

    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep) -> User:
    user = cast(User | None, session.get(User, user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
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
