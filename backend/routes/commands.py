from typing import Sequence, cast, Annotated

import requests
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from sqlmodel import select

from database import SessionDep
from models.command_model import Announcement

router = APIRouter(prefix="/commands", tags=["commands"])


@router.post("/announce")
async def announce(announcement: Announcement):
    # TODO: Write RCon client to send messages to the game server
    return {"ok": True}
