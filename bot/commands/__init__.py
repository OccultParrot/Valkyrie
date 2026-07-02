from bot import Bot

from .admin import init_admin_commands
from .vendor import init_vendor_commands


def init_commands(client: Bot):
    init_vendor_commands(client)
    init_admin_commands(client)