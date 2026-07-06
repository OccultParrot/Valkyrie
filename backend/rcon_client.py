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
        response = await self.rcon.send_command(b"\x02" + b"\x10" + message.encode() + b"\x00")
        print(f"Announce Response: {response}")

        return response

    async def get_player_list(self):
        await self.rcon.connect()
        response = await self.rcon.send_command(b"\x02" + b"\x40" + b"\x00")
        print(f"Get Player List Response: {response}")

        return response