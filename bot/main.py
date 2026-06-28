import os
from typing import Dict

import discord
from discord import Client, app_commands, Intents, Interaction

from button.verify_view import VerifyView

BUTTON_VIEW_DICT: Dict[str, discord.ui.View] = {
    "verify account": VerifyView()
}


class Bot(Client):
    def __init__(self):
        intents = Intents.all()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        print("Syncing Command Tree...")
        await self.tree.sync(guild=discord.Object(id=1517273639324614707))


client = Bot()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} | {client.user.id}")


@client.tree.command(name="send-message", description="Send a message as the bot")
@app_commands.describe(message="The message to send")
async def send_message(interaction: Interaction, message: str):
    """
    Sends the users message from the bot so that the owners (Chebe & Sinna) can send messages as the bot.
    :param message: The message to send as the bot
    :param interaction: The discord interaction
    """
    channel = interaction.channel
    await channel.send(message)
    await interaction.response.send_message("Message sent!", ephemeral=True)


async def send_embed(interaction: Interaction, title: str, description: str, color: discord.Color):
    embed = discord.Embed(title=title, description=description, color=color)
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message(f"Message sent!", ephemeral=True)


@client.tree.command(name="send-button", description="Send a set of buttons as the bot")
@app_commands.describe(buttons="The buttons to send")
async def send_button(interaction: Interaction, button: str):
    """
    The user picks a button from the autocomplete list, and it sends the buttons in the channel used.
    This is so that the owners (Chebe & Sinna) can send buttons in a prettier way.
    :param interaction: The discord interaction
    """
    channel = interaction.channel
    await channel.send(view=BUTTON_VIEW_DICT[button])
    await interaction.response.send_message("Button sent!", ephemeral=True)


@send_button.autocomplete("button")
async def send_button_autocomplete(interaction: Interaction, current: str):
    filtered = [
        b for b in BUTTON_VIEW_DICT.keys() if b.startswith(current)
    ]

    return [
        app_commands.Choice(name=b.title(), value=b)
        for b in filtered[:25]
    ]


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
