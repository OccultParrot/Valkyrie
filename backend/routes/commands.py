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

    return {"success": True, "output": response, "error": None}


@router.post("/dm")
async def dm(direct_message: DirectMessage):
    response = await rcon_client.send_direct_message(direct_message.target, direct_message.message)

    return {"success": True, "output": response, "error": None}


@router.get("/players")
async def get_players():
    """
    Example player list rcon output
    PlayerList\n76561199214551282,76561199761519070,\nOccultParrot,muddysoldier,
    """
    response = await rcon_client.get_player_list()
    response = response.split("\n")

    if len(response) != 3:
        return {"success": False, "output": response,
                "error": f"There are not 3 rows in the RCon response. {len(response)}"}

    ids = response[1].split(",")
    names = response[2].split(",")

    if len(ids) != len(names):
        return {"success": False, "output": response,
                "error": f"Length of IDs does not match length of names: {len(ids)}, {len(names)}"}

    players = []
    for i in range(len(ids)):
        try:
            steam_id = int(ids[i])
            steam_name = names[i]
        except ValueError:
            continue

        players.append((steam_name, steam_id))

    print(players)

    return {"success": True, "output": players, "error": None}
