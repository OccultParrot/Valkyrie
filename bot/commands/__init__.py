import discord
import vendor
import admin


def init_commands(client: discord.Client):
    vendor.init_vendor_commands(client)
    admin.init_admin_commands(client)
