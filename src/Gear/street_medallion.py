from UE_core.gear import GearModifier
from UE_core.utils import Faction


class StreetMedallion(GearModifier):
    display_name = "Ravens Medallion"
    def applies_to(self, lt_data: dict) -> bool:
        return lt_data["faction"] == Faction.STREET

    def get_borrowed_faction_count(self, lt_data, ctx):
        shadow_base = ctx.total(Faction.SHADOW)

        return {
            Faction.SHADOW: shadow_base
        }