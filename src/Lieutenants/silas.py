from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, Area, FactionCountContext
from dataclasses import dataclass

import random

# -------------------------
# Ability parameters class
# -------------------------
@dataclass
class SilasAbilityParams:
    crit_bonus: float = 0.0        # Blue Folder crit %
    proc_chance: float = 0.05      # hit proc chance
    hit_multiplier: float = 2.0    # multiplier when proc occurs

# -------------------------
# Star scaling tables
# -------------------------
SILAS_STAR_PARAMS = {
    1: {"crit_bonus": 2, "proc_chance": 5},
    2: {"crit_bonus": 3, "proc_chance": 7},
    3: {"crit_bonus": 4, "proc_chance": 9},
    4: {"crit_bonus": 5, "proc_chance": 12},
    5: {"crit_bonus": 7, "proc_chance": 15},
    6: {"crit_bonus": 9, "proc_chance": 19},
    7: {"crit_bonus": 11, "proc_chance": 23},
    8: {"crit_bonus": 14, "proc_chance": 28},
    9: {"crit_bonus": 18, "proc_chance": 35},
}

class Silas(Lieutenant):
    id = "silas"
    faction = Faction.CARTEL
    rarity = Rarity.EPIC
    ability_areas: list[Area] = [Area.BOSSING, Area.EVE]  # optional
    
    def build_ability_params(self) -> SilasAbilityParams:
        base = SILAS_STAR_PARAMS.get(self.star, SILAS_STAR_PARAMS[1])
        return SilasAbilityParams(**base)
    
    def resolve_ability(
        self,
        slot: int,
        ctx: "FactionCountContext",
        params: SilasAbilityParams,
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

    def resolve_ability_area(
        self,
        area: Area,
        slot: int,
        ctx: "FactionCountContext",
        params: SilasAbilityParams,
        stats: "BlueFolderStats",
        gear=None,
        other_lts=None,
        hit_ctx: dict = None,
    ):
        # no crit bonus here, leave it in Blue Folder only
        pass