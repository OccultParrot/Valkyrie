import os

from discord import Client, app_commands, Intents

import buttons
import commands


class Bot(Client):
    def __init__(self):
        intents = Intents.all()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        for view in buttons.BUTTON_VIEW_DICT.values():
            self.add_view(view())

        print("Syncing Command Tree...")
        await self.tree.sync()


client = Bot()

commands.init_commands(client)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} | {client.user.id}")


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
