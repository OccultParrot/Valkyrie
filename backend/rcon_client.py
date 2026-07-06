import asyncio
import os

import dotenv
from gamercon_async import EvrimaRCON

dotenv.load_dotenv()

class RConClient:
    def __init__(self):
        self.rcon = EvrimaRCON(os.getenv('RCON_HOST'), os.getenv('RCON_PORT'), os.getenv('RCON_PASSWORD'))

    async def announce(self, message: str) -> str:
        await self.rcon.connect()

        # ANNOUNCE (0x10) just takes a message arg
        response = await self.rcon.send_command(b"\x02" + b"\x10" + message.encode() + b"\x00")
        print(f"Announce Response: {response}")

        return response

    async def send_direct_message(self, steam_id64: str, message: str) -> str:
        await self.rcon.connect()

        # DIRECTMESSAGE (0x11) args are comma-delimited: SteamID64, then the message.
        payload = f"{steam_id64},{message}"
        response = await self.rcon.send_command(b"\x02" + b"\x11" + payload.encode() + b"\x00")
        print(f"Direct Message Response: {response}")

        return response

    async def get_player_list(self):
        await self.rcon.connect()
        response = await self.rcon.send_command(b"\x02" + b"\x40" + b"\x00")
        print(f"Get Player List Response: {response}")

        return response