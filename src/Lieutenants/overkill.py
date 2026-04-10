from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, Area, FactionCountContext
from dataclasses import dataclass

import random

@dataclass
class OverkillAbilityParams:
    crit_bonus: float = 1.0     # Adds 1% crit chance per star
    proc_chance: float = 5.0    # Chance to chain-doubles on crit
    max_multiplier: int = 64    # Hard cap for chain

OVERKILL_STAR_PARAMS = {
    1: {"crit_bonus": 1, "proc_chance": 10},
    2: {"crit_bonus": 2, "proc_chance": 13},
    3: {"crit_bonus": 3, "proc_chance": 16},
    4: {"crit_bonus": 4, "proc_chance": 19},
    5: {"crit_bonus": 5, "proc_chance": 22},
    6: {"crit_bonus": 6, "proc_chance": 24},
    7: {"crit_bonus": 7, "proc_chance": 26},
    8: {"crit_bonus": 8, "proc_chance": 28},
    9: {"crit_bonus": 9, "proc_chance": 30},
}

class Overkill(Lieutenant):
    id = "overkill"
    faction = Faction.SHADOW
    rarity = Rarity.EPIC
    ability_areas: list[Area] = [Area.BOSSING, Area.EVE]

    def build_ability_params(self) -> OverkillAbilityParams:
        base = OVERKILL_STAR_PARAMS.get(self.star, OVERKILL_STAR_PARAMS[1])
        return OverkillAbilityParams(**base)

    def resolve_ability(self, slot, ctx, params, stats, gear=None, other_lts=None):
        """Add crit bonus to Blue Folder stats only."""
        stats.crit_chance += params.crit_bonus

    def on_crit_bonus(self, damage: float, crit_extra: float, hit_ctx: dict, gear=None) -> float:
        """
        Called after crit is calculated. Applies the Overkill chain multiplier
        to the crit bonus part of the damage.
        """
        params = self.get_modified_ability_params(gear)
        ok_proc_occurred = False
        ok_proc_depth = 0
        multiplier = 1

        while random.random() < params.proc_chance / 100:
            ok_proc_occurred = True
            ok_proc_depth += 1
            multiplier *= 2
            if multiplier >= params.max_multiplier:
                break

        # Apply multiplier only to the crit_extra part
        crit_extra *= multiplier

        # Track in hit-level context
        hit_ctx[f"{self.id}_proc"] = ok_proc_occurred
        hit_ctx[f"{self.id}_proc_depth"] = ok_proc_depth
        return crit_extra

    def resolve_ability_area(
        self,
        area: Area,
        slot: int,
        ctx: "FactionCountContext",
        params: OverkillAbilityParams,
        stats: "BlueFolderStats",
        gear=None,
        other_lts=None,
        hit_ctx: dict = None,
    ):
        """Nothing extra for area; crit bonus already handled in Blue Folder."""
        pass
