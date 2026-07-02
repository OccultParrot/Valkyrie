from typing import Dict, Type

import discord

from verify_view import VerifyView
from claim_view import ClaimView

BUTTON_VIEW_DICT: Dict[str, Type[discord.ui.View]] = {
    "verify account": VerifyView,
    "claim and balance": ClaimView
}
