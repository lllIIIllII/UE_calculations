from UE_core.gear import GearModifier
from UE_core.utils import Faction


class CartelMedallion(GearModifier):
    def applies_to(self, lt_data: dict) -> bool:
        return lt_data["faction"] == Faction.CARTEL

    def get_borrowed_faction_count(self, lt_data, ctx):
        shadow_base = ctx.account.get(Faction.SHADOW, 0)

        return {
            Faction.SHADOW: shadow_base
        }