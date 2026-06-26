import os

import discord
import requests
import dotenv
from discord import Client, app_commands, Intents, Interaction


class Bot(Client):
    def __init__(self):
        intents = Intents.all()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        print("Syncing Command Tree...")
        await self.tree.sync()


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


@client.tree.command(name="send-button", description="Send a set of buttons as the bot")
async def send_button(interaction: Interaction):
    """
    The user picks a button from the autocomplete list, and it sends the buttons in the channel used.
    This is so that the owners (Chebe & Sinna) can send buttons in a prettier way.
    :param interaction: The discord interaction
    """
    channel = interaction.channel
    # TODO: Write the send button command. It should let them pick from a list of buttons.
    await channel.send("Not done yet lol")
    await interaction.response.send_message("Button send!", ephemeral=True)


@client.tree.command(name="link", description="Link your steam account to the server")
@app_commands.describe(link="The link to your steam account")
async def link_account(interaction: Interaction, link: str):
    """
    Parses the given link and adds a user with the /users/ endpoint on our API
    Example link: https://steamcommunity.com/profiles/76561199214551282/
    and the steam ID is the last section AFTER profiles: 76561199214551282
    :param link: The link to your steam account
    :param interaction: The discord interaction
    """
    await interaction.response.defer()
    steam_id: int
    try:
        s = link.split("/")[3]
        steam_id = int(s)
    except IndexError or ValueError as e:
        print(f"Invalid link {link} from {interaction.user.name}")
        response = await interaction.original_response()
        await response.edit(
            content=f"Invalid link {link}. The link should look like https://steamcommunity.com/profiles/**XXXXXXXXXXXXXX**/")
        return

    response = requests.post(
        os.environ["BACKEND_URL"] + "/users/",
        json={
            "steam_id": steam_id,
            "discord_id": interaction.user.id
        })

    if response.status_code != 200:
        response = await interaction.original_response()
        await response.edit(content=f"Failed to link steam account {steam_id}")
        print(f"Failed to link steam account {steam_id}")
        return

    await interaction.user.add_roles(discord.Object(id=1520180800317030481))

    print(f"Linked steam account {steam_id} -> {interaction.user.id}")
    response = await interaction.original_response()
    await response.edit(content=f"Successfully linked steam account {steam_id}!")


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
