from UE_core.gear import GearModifier
from UE_core.utils import Faction, FactionCountContext

from typing import Dict

class ShadowInsignia(GearModifier):
    display_name = "Shadow Insignia"
    def applies_to(self, lt_data: Dict) -> bool:
        # Applies to any SHADOW LT
        return lt_data["faction"] == Faction.SHADOW  # can use lt_data["faction"] if enum

    def apply_to_faction_context(self, ctx: "FactionCountContext"):
        """
        Multiply the SHADOW count in the loadout by:
        2 + (number of SHADOW LTs in the loadout after the first)
        """
        loadout_shadows = ctx.loadout.get(Faction.SHADOW, 0)
        if loadout_shadows > 1:
            multiplier = 2 + (loadout_shadows - 1)
        else:
            multiplier = 2
        ctx.account[Faction.SHADOW] *= multiplier