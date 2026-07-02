import os

import discord
import requests
from discord import app_commands, Interaction

from bot import Bot


def init_vendor_commands(client: Bot):
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

    @client.tree.command(name="withdraw", description="Withdraw nuggets from the user")
    @app_commands.describe(user="The user to withdraw", amount="The amount to withdraw")
    async def withdraw(interaction: Interaction, user: discord.Member, amount: int):
        response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(user.id))
        if response.status_code == 404:
            await interaction.response.send_message(f"{user.mention} is not verified!", ephemeral=True)
            return

        data = response.json()
        new_balance = data["balance"] - amount

        if new_balance < 0:
            await interaction.response.send_message(
                f"{user.mention} only has {data['balance']} dino nuggets, can't withdraw {amount}.",
                ephemeral=True
            )
            return

        patch_response = requests.patch(
            os.environ["BACKEND_URL"] + f"users/{data['id']}",
            json={"balance": new_balance}
        )

        if patch_response.status_code != 200:
            await interaction.response.send_message("Failed to withdraw nuggets!", ephemeral=True)
            return

        await interaction.response.send_message(
            f"Withdrew {amount} dino nuggets from {user.mention}. New balance: {new_balance}",
            ephemeral=True
        )

    @client.tree.command(name="deposit", description="Deposit nuggets to the user")
    @app_commands.describe(user="The user to deposit", amount="The amount to deposit")
    async def deposit(interaction: Interaction, user: discord.Member, amount: int):
        response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(user.id))
        if response.status_code == 404:
            await interaction.response.send_message(f"{user.mention} is not verified!", ephemeral=True)
            return

        data = response.json()
        new_balance = data["balance"] + amount

        patch_response = requests.patch(
            os.environ["BACKEND_URL"] + f"users/{data['id']}",
            json={"balance": new_balance}
        )

        if patch_response.status_code != 200:
            await interaction.response.send_message("Failed to deposit nuggets!", ephemeral=True)
            return

        await interaction.response.send_message(
            f"Deposited {amount} dino nuggets to {user.mention}. New balance: {new_balance}",
            ephemeral=True
        )
