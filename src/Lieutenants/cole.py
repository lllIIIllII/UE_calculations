from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, Area, FactionCountContext
from dataclasses import dataclass

import random

# -------------------------
# Ability parameters class
# -------------------------
@dataclass
class ColeAbilityParams:
    crit_bonus: float = 0.0        # Blue Folder crit %
    proc_chance: float = 0.05      # hit proc chance
    hit_multiplier: float = 1.5    # multiplier when proc occurs
    no_cost_proc_chance: float = 0.0  # chance for attack to have no cost

# -------------------------
# Star scaling tables
# -------------------------
COLE_STAR_PARAMS = {
    1: {"crit_bonus": 3, "proc_chance": 5, "no_cost_proc_chance": 2},
    2: {"crit_bonus": 4, "proc_chance": 5, "no_cost_proc_chance": 2.5},
    3: {"crit_bonus": 5, "proc_chance": 10, "no_cost_proc_chance": 3},
    4: {"crit_bonus": 6, "proc_chance": 10, "no_cost_proc_chance": 4},
    5: {"crit_bonus": 8, "proc_chance": 20, "no_cost_proc_chance": 5},
    6: {"crit_bonus": 10, "proc_chance": 20, "no_cost_proc_chance": 6},
    7: {"crit_bonus": 12, "proc_chance": 30, "no_cost_proc_chance": 7},
    8: {"crit_bonus": 15, "proc_chance": 30, "no_cost_proc_chance": 8},
    9: {"crit_bonus": 18, "proc_chance": 40, "no_cost_proc_chance": 10},
}

class Cole(Lieutenant):
    id = "cole"
    faction = Faction.STREET
    rarity = Rarity.EPIC
    ability_areas: list[Area] = [Area.BOSSING, Area.EVE]  # optional
    
    def build_ability_params(self) -> ColeAbilityParams:
        base = COLE_STAR_PARAMS.get(self.star, COLE_STAR_PARAMS[1])
        return ColeAbilityParams(**base)
    
    def resolve_ability(
        self,
        slot: int,
        ctx: "FactionCountContext",
        params: ColeAbilityParams,
        stats: "BlueFolderStats",
        gear=None,
        other_lts=None,
    ):
        # Only add crit bonus once to Blue Folder
        stats.crit_chance += params.crit_bonus

    def on_proc(self, damage: float, ctx: dict) -> float:
        """
        Called per-hit during simulation (non-crit). Applies 2x multiplier based on proc chance.
        """
        params = self.build_ability_params()
        proc_occurred = random.random() < params.proc_chance / 100
        ctx[f"{self.id}_proc"] = proc_occurred
        if proc_occurred:
            damage *= params.hit_multiplier
        return damage

    def on_cost(self, cost: float, ctx: dict) -> float:
        """
        Called per-hit during simulation to allow a chance for this attack to have no cost.
        """
        params = self.build_ability_params()
        proc_occurred = random.random() < params.no_cost_proc_chance / 100
        ctx[f"{self.id}_no_cost_proc"] = proc_occurred
        if proc_occurred:
            return 0.0
        return cost

    def resolve_ability_area(
        self,
        area: Area,
        slot: int,
        ctx: "FactionCountContext",
        params: ColeAbilityParams,
        stats: "BlueFolderStats",
        gear=None,
        other_lts=None,
        hit_ctx: dict = None,
    ):
        # no crit bonus here, leave it in Blue Folder only
        pass
