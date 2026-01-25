from UE_core.gear import GearModifier
from UE_core.utils import Faction, FactionCountContext

from typing import Dict

class StreetInsignia(GearModifier):
    display_name = "Street Insignia"
    def applies_to(self, lt_data: Dict) -> bool:
        # Applies to any STREET LT
        return lt_data["faction"] == Faction.STREET  # can use lt_data["faction"] if enum

    def apply_to_faction_context(self, ctx: "FactionCountContext"):
        """
        Multiply the STREET count in the loadout by:
        2 + (number of STREET LTs in the loadout after the first)
        """
        loadout_streets = ctx.loadout.get(Faction.STREET, 0)
        if loadout_streets > 1:
            multiplier = 2 + (loadout_streets - 1)
        else:
            multiplier = 2
        ctx.account[Faction.STREET] *= multiplier