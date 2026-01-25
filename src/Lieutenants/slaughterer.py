from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, FactionCountContext

from Gear.street_insignia import StreetInsignia

from dataclasses import dataclass
from typing import Any

# -------------------------
# Ability parameters class
# -------------------------
@dataclass
class SlaughtererAbilityParams:
    dmg_per_street: float = 0.0055  # base 0.55%

# -------------------------
# Slaughterer star scaling table
# -------------------------
SLAUGHTERER_STAR_PARAMS = {
    1: {"dmg_per_street": 0.1},
    2: {"dmg_per_street": 0.15},
    3: {"dmg_per_street": 0.2},
    4: {"dmg_per_street": 0.3},
    5: {"dmg_per_street": 0.4},
    6: {"dmg_per_street": 0.5},
    7: {"dmg_per_street": 0.65},
    8: {"dmg_per_street": 0.8},
    9: {"dmg_per_street": 1.0},
}

# -------------------------
# Slaughterer Lieutenant class
# -------------------------
class Slaughterer(Lieutenant):
    id = "slaughterer"
    faction = Faction.STREET
    rarity = Rarity.EPIC
    ability_areas = [] 
       
    def default_insignia_profile(self) -> dict:
        return {
            "crit_chance": 1
        }

    def build_ability_params(self) -> SlaughtererAbilityParams:
        """
        Build base ability parameters based on star, before gear or other LT modifications.
        """
        base = SLAUGHTERER_STAR_PARAMS.get(self.star, SLAUGHTERER_STAR_PARAMS[1])
        params = SlaughtererAbilityParams(**base)
        return params
    

    def resolve_ability(
        self,
        slot: int,
        ctx: "FactionCountContext",
        params: SlaughtererAbilityParams,
        stats: "BlueFolderStats",
        gear,
        other_lts: list["Lieutenant"] = None,
    ):
        """
        Apply Slaughterer's ability to Blue Folder stats.
        Reads:
        - self.star (for thresholds)
        - params (may be modified by gear or other LTs)
        - faction counts (from ctx)
        """

        # Total counts include account, loadout, and virtual contributions
        # Base counts
        street_count = ctx.total(Faction.STREET)

        # Check for any gear that adds borrowed shadow
        borrowed_shadow = 0
        for g in gear:
            if hasattr(g, "get_borrowed_faction_count") and g.applies_to(self.get_lt_data()):
                shadow_bonus = g.get_borrowed_faction_count(self.get_lt_data(), ctx).get(Faction.SHADOW, 0)
                if shadow_bonus > 0:  # only count gear that actually adds shadow
                    borrowed_shadow += shadow_bonus

        total_dmg = params.dmg_per_street * (street_count + borrowed_shadow)

        stats.crit_dmg += total_dmg

    # Optional hooks for other LTs or gear to modify faction counts or ability params
    def apply_faction_context_modifier(self, ctx: "FactionCountContext"):
        """
        Other LTs may override this to modify the context seen by Slaughterer.
        """
        pass

    def apply_ability_param_modifier(self, target: "Lieutenant", params: Any):
        """
        Other LTs may override this to modify Slaughterer's ability parameters.
        """
        pass