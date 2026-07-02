import os

import commands
import events
from bot import Bot

client = Bot()

commands.init_commands(client)
events.init_events(client)

if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
