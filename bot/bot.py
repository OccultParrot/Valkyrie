from discord import Client, app_commands, Intents

import buttons


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
