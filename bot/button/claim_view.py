import os

import discord
import requests


class ClaimView:
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success, custom_id="claim_button")
    async def claim_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        daily_amount = 10
        daily_cooldown = 24 * 60 * 60  # The cool down 24 hours (60 * 60 = seconds -> minutes -> hours)

        response = requests.get(f"{os.environ['BACKEND_URL']}/users/lookup?discord_id={interaction.user.id}")

        if response.status_code == 404:
            if response.json()["detail"] == "User not found":
                await interaction.response.send_message(f"You are not verified! Please use the verified button *first*!")
                return
            await interaction.response.send_message(f"An error occurred!")
            return

        data = response.json()
        data["balance"] += daily_amount




    @discord.ui.button(label="Balance", style=discord.ButtonStyle.success, custom_id="balance_button")
    async def balance_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        response = requests.get(os.environ["BACKEND_URL"] + "users/lookup/?discord_id=" + str(interaction.user.id))
        data = response.json()

        embed = discord.Embed(
            title=interaction.user.display_name,
            description=f"Balance: {str(data.get('balance', 0))} dino nuggets",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
