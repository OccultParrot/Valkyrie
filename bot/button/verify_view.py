import os

import discord
from discord import Interaction
import requests
import dotenv

dotenv.load_dotenv()


def error_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, color=discord.Color.red())


def success_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, color=discord.Color.green())


class LinkModal(discord.ui.Modal, title="Link Steam Account"):
    def __init__(self, callback: callable):
        super().__init__()
        self.callback = callback
        self.link_input = discord.ui.TextInput(
            label="Steam Profile Link",
            placeholder="https://steamcommunity.com/profiles/XXXXXXXXXXXXXX/",
            required=True
        )
        self.add_item(self.link_input)

    async def on_submit(self, interaction: Interaction):
        await self.callback(interaction, link=self.link_input.value)


class IDModal(discord.ui.Modal, title="Link Steam Account"):
    def __init__(self, callback: callable):
        super().__init__()
        self.callback = callback
        self.id_input = discord.ui.TextInput(
            label="Steam Profile ID",
            placeholder="76561199214551282",
            required=True
        )
        self.add_item(self.id_input)

    async def on_submit(self, interaction: Interaction):
        await self.callback(interaction, steam_id=int(self.id_input.value))


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Prevents the view from expiring

    @discord.ui.button(label="Use Steam Profile Link", style=discord.ButtonStyle.success, custom_id="link_button")
    async def link_callback(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LinkModal(self.link_account))

    @discord.ui.button(label="Use Steam Profile ID", style=discord.ButtonStyle.success, custom_id="id_button")
    async def id_callback(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(IDModal(self.link_account))

    @staticmethod
    async def link_account(interaction: Interaction, link: str = None, steam_id: int = None):
        """
        Parses the given link and adds a user with the /users/ endpoint on our API
        Example link: https://steamcommunity.com/profiles/76561199214551282/
        and the steam ID is the last section AFTER profiles: 76561199214551282
        :param link: The link to your steam account
        :param steam_id: The steam ID
        :param interaction: The discord interaction
        """

        if link is None and steam_id is None:
            await interaction.response.send_message(
                embed=error_embed("You need to supply either your profile link OR your steam ID"),
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        steam_id: int
        try:
            if steam_id is None:
                s = link.split("/")[4]
                steam_id = int(s)
        except (IndexError, ValueError) as e:
            print(f"Invalid link {link} from {interaction.user.name}")
            await interaction.followup.send(
                embed=error_embed(
                    f"Invalid link `{link}`.\nThe link should look like `https://steamcommunity.com/profiles/XXXXXXXXXXXXXX/`"),
                ephemeral=True
            )
            return

        response = requests.post(
            os.environ["BACKEND_URL"] + "users/",
            json={
                "steam_id": steam_id,
                "discord_id": interaction.user.id
            })

        if response.status_code == 404:
            print(f"No user of steam ID {steam_id}")
            await interaction.followup.send(
                embed=error_embed(f"No user found with steam ID: `{steam_id}`"),
                ephemeral=True
            )
            return

        if response.status_code != 200:
            await interaction.followup.send(
                embed=error_embed(f"Failed to link steam account `{steam_id}`"),
                ephemeral=True
            )
            print(f"Failed to link steam account {steam_id}")
            return

        data = response.json()

        await interaction.user.add_roles(discord.Object(id=1517323532621578402))
        if not interaction.user.get_role(1517389443642953778):
            await interaction.user.edit(nick=data["steam_name"])

        print(f"Linked steam account {steam_id} -> {interaction.user.id}")
        await interaction.followup.send(
            embed=success_embed(f"Successfully linked steam account `{steam_id}`!"),
            ephemeral=True
        )
