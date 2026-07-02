import math
import os
from typing import Dict, Type

import requests
import discord
from discord import Client, app_commands, Intents, Interaction

from button.claim_view import ClaimView
from button.verify_view import VerifyView

BUTTON_VIEW_DICT: Dict[str, Type[discord.ui.View]] = {
    "verify account": VerifyView,
    "claim and balance": ClaimView
}


class Bot(Client):
    def __init__(self):
        intents = Intents.all()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.add_view(VerifyView())
        self.add_view(ClaimView())
        print("Syncing Command Tree...")
        await self.tree.sync()


client = Bot()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} | {client.user.id}")


# region Admin Commands
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
@app_commands.describe(button="The buttons to send")
async def send_button(interaction: Interaction, button: str):
    """
    The user picks a button from the autocomplete list, and it sends the buttons in the channel used.
    This is so that the owners (Chebe & Sinna) can send buttons in a prettier way.
    :param button: The button the user selects
    :param interaction: The discord interaction
    """
    channel = interaction.channel
    await channel.send(view=BUTTON_VIEW_DICT[button]())
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


@client.tree.command(name="list-verified", description="List all verified users")
@app_commands.describe(page="The page number to view, default 1")
async def list_verified_users(interaction: Interaction, page: int = 1):
    users = requests.get(os.environ["BACKEND_URL"] + "users/")
    data = users.json()
    pages = math.ceil(len(data) / 10)
    if page < 1 or page > pages:
        await interaction.response.send_message(f"Page {page} does not exist. There are only {pages} pages.",
                                                ephemeral=True)
        return

    start = (page - 1) * 10
    end = start + 10
    u_list = data[start:end]
    embeds = [get_embed(interaction.guild, u) for u in u_list]
    if embeds:
        embeds[-1].set_footer(text=f"Page {page}/{pages}")

    await interaction.response.send_message(embeds=embeds, ephemeral=True)


def get_embed(guild, user) -> discord.Embed:
    embed = discord.Embed(title=user["steam_name"], color=discord.Color.blurple())
    embed.add_field(name="ID", value=user["id"])
    embed.add_field(name="Steam ID", value=user["steam_id"])
    embed.add_field(name="Discord ID", value=user["discord_id"])
    embed.add_field(name="Mention", value=guild.get_member(int(user["discord_id"])).mention)

    return embed


# endregion

# region Vendor Commands
@client.tree.command(name="lookup", description="Returns the data of the user")
@app_commands.describe(user="The user to check")
async def lookup(interaction: Interaction, user: discord.Member):
    response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(user.id))
    data = response.json()
    await interaction.response.send_message(str(data))


@client.tree.command(name="user-balance", description="Get your balance, or the balance of the user")
@app_commands.describe(user="The user to check.")
async def user_balance(interaction: Interaction, user: discord.Member):
    response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(user.id))
    data = response.json()

    embed = discord.Embed(
        title=interaction.user.display_name,
        description=f"Balance: {str(data.get('balance', 0))} dino nuggets",
        color=discord.Color.gold()
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="balance", description="Get your balance, or the balance of the user")
async def balance(interaction: Interaction):
    response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(interaction.user.id))
    data = response.json()

    embed = discord.Embed(
        title=interaction.user.display_name,
        description=f"Balance: {str(data.get('balance', 0))} dino nuggets",
        color=discord.Color.gold()
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


# endregion

if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
