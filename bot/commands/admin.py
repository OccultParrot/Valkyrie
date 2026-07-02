import math
import os
import datetime

import discord
import requests
from discord import app_commands, Interaction

import buttons
from bot import Bot


def init_admin_commands(client: Bot):
    @client.tree.command(name="send-message", description="Send a message as the bot")
    @app_commands.describe(message="The message to send")
    @app_commands.checks.has_permissions(administrator=True)
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

    @client.tree.command(name="send-buttons", description="Send a set of buttons as the bot")
    @app_commands.describe(button="The buttons to send")
    @app_commands.checks.has_permissions(administrator=True)
    async def send_button(interaction: Interaction, button: str):
        """
        The user picks a buttons from the autocomplete list, and it sends the buttons in the channel used.
        This is so that the owners (Chebe & Sinna) can send buttons in a prettier way.
        :param button: The buttons the user selects
        :param interaction: The discord interaction
        """
        channel = interaction.channel
        await channel.send(view=buttons.BUTTON_VIEW_DICT[button]())
        await interaction.response.send_message("Button sent!", ephemeral=True)

    @send_button.autocomplete("button")
    async def send_button_autocomplete(interaction: Interaction, current: str):
        filtered = [
            b for b in buttons.BUTTON_VIEW_DICT.keys() if b.startswith(current)
        ]

        return [
            app_commands.Choice(name=b.title(), value=b)
            for b in filtered[:25]
        ]

    @client.tree.command(name="lookup", description="Returns the data of the user")
    @app_commands.describe(user="The user to check")
    @app_commands.checks.has_permissions(administrator=True)
    async def lookup(interaction: Interaction, user: discord.Member):
        response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(user.id))
        data = response.json()
        await interaction.response.send_message(get_embed(interaction.guild, data), ephemeral=True)

    @client.tree.command(name="list-verified", description="List all verified users")
    @app_commands.describe(page="The page number to view, default 1")
    @app_commands.checks.has_permissions(administrator=True)
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
        for key, value in user.items():
            if key == "steam_name":
                continue

            if key == "discord_id":
                value = guild.get_member(value).mention

            if key in ("created_at", "last_daily", "updated_at") and value is not None:
                dt = datetime.fromisoformat(value)
                value = f"<t:{int(dt.timestamp())}:R>"

            embed.add_field(name=key, value=value, inline=False)

        return embed
