import discord

from .admin import init_admin_commands
from .vendor import init_vendor_commands


def init_commands(client: discord.Client):
    init_vendor_commands(client)
    init_admin_commands(client)