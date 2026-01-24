from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, FactionCountContext

from Gear.cartel_insignia import CartelInsignia

from dataclasses import dataclass
from typing import Any

# -------------------------
# Ability parameters class
# -------------------------
@dataclass
class JaredAbilityParams:
    dmg_per_cartel: float = 0.0055  # base 0.55%

# -------------------------
# Jared star scaling table
# -------------------------
JARED_STAR_PARAMS = {
    1: {"dmg_per_cartel": 0.1},
    2: {"dmg_per_cartel": 0.15},
    3: {"dmg_per_cartel": 0.2},
    4: {"dmg_per_cartel": 0.25},
    5: {"dmg_per_cartel": 0.35},
    6: {"dmg_per_cartel": 0.45},
    7: {"dmg_per_cartel": 0.55},
    8: {"dmg_per_cartel": 0.65},
    9: {"dmg_per_cartel": 0.8},
}

# -------------------------
# Jared Lieutenant class
# -------------------------
class Jared(Lieutenant):
    id = "jared"
    faction = Faction.CARTEL
    rarity = Rarity.EPIC
    ability_areas = [] 
       
    def default_insignia_profile(self) -> dict:
        return {
            "crit_chance": 1
        }

    def build_ability_params(self) -> JaredAbilityParams:
        """
        Build base ability parameters based on star, before gear or other LT modifications.
        """
        base = JARED_STAR_PARAMS.get(self.star, JARED_STAR_PARAMS[1])
        params = JaredAbilityParams(**base)
        return params
    

    def resolve_ability(
        self,
        slot: int,
        ctx: "FactionCountContext",
        params: JaredAbilityParams,
        stats: "BlueFolderStats",
        gear,
    ):
        """
        Apply Jared's ability to Blue Folder stats.
        Reads:
        - self.star (for thresholds)
        - params (may be modified by gear or other LTs)
        - faction counts (from ctx)
        """

        # Total counts include account, loadout, and virtual contributions
        # Base counts
        cartel_count = ctx.account.get(Faction.CARTEL, 0)
        shadow_count = ctx.account.get(Faction.SHADOW, 0)

        # Determine cartel insignia multiplier from gear
        cartel_multiplier = 1
        for g in gear:
            if isinstance(g, CartelInsignia) and g.applies_to(self.get_lt_data()):
                # Apply formula: 2 + (num_cartels_in_loadout_after_first)
                loadout_cartels = ctx.loadout.get(Faction.CARTEL, 0)
                if loadout_cartels > 1:
                    cartel_multiplier = 2 + (loadout_cartels - 1)
                else:
                    cartel_multiplier = 2
                break  # assume only one insignia applies

        # Check for any gear that adds borrowed shadow
        borrowed_shadow = 0
        for g in gear:
            if g.applies_to(self.get_lt_data()):
                borrowed_shadow += g.get_borrowed_faction_count(self.get_lt_data(), ctx).get(Faction.SHADOW, 0)

        total_dmg = params.dmg_per_cartel * (cartel_count * cartel_multiplier + borrowed_shadow)

        stats.dmg += total_dmg

    # Optional hooks for other LTs or gear to modify faction counts or ability params
    def apply_faction_context_modifier(self, ctx: "FactionCountContext"):
        """
        Other LTs may override this to modify the context seen by Jared.
        """
        pass

    def apply_ability_param_modifier(self, target: "Lieutenant", params: Any):
        """
        Other LTs may override this to modify Jared's ability parameters.
        """
        pass