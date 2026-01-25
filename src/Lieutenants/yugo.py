from UE_core.lieutenant import Lieutenant
from UE_core.utils import Faction, Rarity, FactionCountContext
from dataclasses import dataclass

# -------------------------
# Ability parameters
# -------------------------
@dataclass
class YugoAbilityParams:
    faction_multiplier: float  # e.g. 0.40 = +40%


# -------------------------
# Star scaling
# -------------------------
YUGO_STAR_PARAMS = {
    1: 0.20,
    2: 0.25,
    3: 0.30,
    4: 0.35,
    5: 0.40,
    6: 0.45,
    7: 0.50,
    8: 0.55,
    9: 0.60,
}

class Yugo(Lieutenant):
    id = "yugo"
    faction = Faction.SHADOW
    rarity = Rarity.RARE
    ability_areas = [] 

    def build_ability_params(self) -> YugoAbilityParams:
        bonus = YUGO_STAR_PARAMS.get(self.star, YUGO_STAR_PARAMS[1])
        return YugoAbilityParams(faction_multiplier=bonus)

    def apply_faction_context_modifier(self, ctx: FactionCountContext):
        """
        Yugo increases effective account faction counts by X%
        via virtual injection.
        """
        params = self.build_ability_params()

        for faction, count in ctx.account.items():
            ctx.virtual[faction] += count * params.faction_multiplier