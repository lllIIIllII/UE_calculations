from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, Area, FactionCountContext
from dataclasses import dataclass
from typing import Any, List

import random

# -------------------------
# Tanya star multipliers
# -------------------------
TANYA_STAR_MULTIPLIERS = {
    1: 1.5,
    2: 1.6,
    3: 1.7,
    4: 1.9,
    5: 2.1,
    6: 2.4,
    7: 2.7,
    8: 3.1,
    9: 3.5,
}

# -------------------------
# Tanya Ability Parameters
# -------------------------
@dataclass
class TanyaAbilityParams:
    crit_multiplier: float = 1.5  # base value, overridden by star
    proc_chance: float = 30.0     # 30% chance on crit

# -------------------------
# Tanya Lieutenant
# -------------------------
class Tanya(Lieutenant):
    id = "tanya"
    faction = Faction.MAFIA
    rarity = Rarity.EPIC
    # She affects Bossing and EvE areas
    ability_areas: List[Area] = [Area.BOSSING, Area.EVE]

    def default_insignia_profile(self) -> dict:
        return {
            "crit_chance": 1
        }

    def build_ability_params(self) -> TanyaAbilityParams:
        multiplier = TANYA_STAR_MULTIPLIERS.get(self.star, TANYA_STAR_MULTIPLIERS[1])
        return TanyaAbilityParams(crit_multiplier=multiplier, proc_chance=30.0)

    def on_full_crit_hit(self, damage: float, ctx: dict, gear=None) -> tuple[float, bool]:
        """
        Called by the simulation when a crit occurs.
        Applies Tanya's chance-based multiplier to the full hit.
        Returns modified damage and whether the proc occurred.
        """
        params = self.get_modified_ability_params(gear)
        proc_occurred = random.random() < params.proc_chance / 100
        if proc_occurred:
            damage *= params.crit_multiplier
        # Track proc in hit-level context
        ctx[f"{self.id}_proc"] = proc_occurred
        return damage, proc_occurred
    
    def resolve_ability_area(
        self,
        area: "Area",
        slot: int,
        ctx: "FactionCountContext",
        params: TanyaAbilityParams,
        stats: "BlueFolderStats",
        gear: list[Any] = None,
        other_lts: list["Lieutenant"] = None,
        hit_ctx: dict = None
    ):
        if area not in self.ability_areas:
            return

        if hit_ctx is None:
            hit_ctx = {}

        if random.random() < params.proc_chance / 100:
            hit_ctx[f"{self.id}_proc"] = True
            hit_ctx[f"{self.id}_multiplier"] = params.crit_multiplier
        else:
            hit_ctx[f"{self.id}_proc"] = False
            hit_ctx[f"{self.id}_multiplier"] = 1.0
