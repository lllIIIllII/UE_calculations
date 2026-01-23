from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, FactionCountContext

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
    
    def __init__(self, star: int):
        super().__init__(star)

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
        stats: "BlueFolderStats"
    ):
        """
        Apply Jared's ability to Blue Folder stats.
        Reads:
        - self.star (for thresholds)
        - params (may be modified by gear or other LTs)
        - faction counts (from ctx)
        """

        # Total counts include account, loadout, and virtual contributions
        cartel_total = ctx.total(Faction.CARTEL)

        # Formula: per-cartel bonus times counts
        stats.dmg += params.dmg_per_cartel * cartel_total

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