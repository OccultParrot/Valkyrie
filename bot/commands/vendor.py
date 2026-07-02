import math
import os
from typing import Dict, Type

import requests
import discord
from discord import Client, app_commands, Intents, Interaction

from buttons.claim_view import ClaimView
from buttons.verify_view import VerifyView


def init_vendor_commands(client: discord.Client):
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
