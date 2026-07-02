import os

import discord
import requests


class ClaimView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success, custom_id="claim_button")
    async def claim_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        lookup_response = requests.get(f"{os.environ['BACKEND_URL']}/users/lookup?discord_id={interaction.user.id}")
        print(lookup_response.status_code, lookup_response.text)  # temp debug

        if lookup_response.status_code == 404:
            if lookup_response.json()["detail"] == "User not found":
                await interaction.response.send_message(
                    f"You are not verified! Please use the verified button *first*!")
                return
            await interaction.response.send_message(f"An error occurred!")
            return

        user_id = lookup_response.json()["id"]
        claim_response = requests.patch(f"{os.environ['BACKEND_URL']}/users/{user_id}/claim")

        if claim_response.status_code == 429:
            await interaction.response.send_message(claim_response.json()["detail"])
            return

        if claim_response.status_code != 200:
            await interaction.response.send_message(f"An error occurred!")
            return

        data = claim_response.json()
        await interaction.response.send_message(f"Daily claimed! New balance: {data['balance']} dino nuggets")

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