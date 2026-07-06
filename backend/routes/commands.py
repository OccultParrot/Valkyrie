from http.client import responses
from typing import Sequence, cast, Annotated

import requests
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from sqlmodel import select

from database import SessionDep
from models.command_model import Announcement, DirectMessage
from rcon_client import RConClient

router = APIRouter(prefix="/commands", tags=["commands"])
rcon_client = RConClient()


@router.post("/announce")
async def announce(announcement: Announcement):
    response = await rcon_client.announce(announcement.message)

    return {"ok": True, "message": response}


@router.post("/dm")
async def dm(direct_message: DirectMessage):
    return {"ok": True}


@router.get("/players")
async def get_players():
    response = await rcon_client.get_player_list()
    return {"ok": True, "players": response}
