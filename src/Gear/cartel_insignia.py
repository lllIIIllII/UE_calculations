from UE_core.gear import GearModifier
from UE_core.utils import Faction, FactionCountContext

from typing import Dict
from collections import Counter

class CartelInsignia(GearModifier):
    def applies_to(self, lt_data: Dict) -> bool:
        # Applies to any CARTEL LT
        return lt_data["faction"] == Faction.CARTEL  # can use lt_data["faction"] if enum

    def apply_to_faction_context(self, ctx: "FactionCountContext"):
        """
        Multiply the CARTEL count in the loadout by:
        2 + (number of CARTEL LTs in the loadout after the first)
        """
        loadout_cartels = ctx.loadout.get(Faction.CARTEL, 0)
        if loadout_cartels > 1:
            multiplier = 2 + (loadout_cartels - 1)
        else:
            multiplier = 2
        ctx.account[Faction.CARTEL] *= multiplier