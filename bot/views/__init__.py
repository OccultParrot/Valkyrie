from typing import Dict, Type

import discord

from .claim_view import ClaimView
from .verify_view import VerifyView

BUTTON_VIEW_DICT: Dict[str, Type[discord.ui.View]] = {
    "verify account": VerifyView,
    "claim and balance": ClaimView
}
