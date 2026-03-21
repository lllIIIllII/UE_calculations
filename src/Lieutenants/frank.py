from UE_core.lieutenant import Lieutenant
from UE_core.utils import Rarity, Faction
from dataclasses import dataclass

import random


# -------------------------
# Ability parameters class
# -------------------------
@dataclass
class FrankAbilityParams:
    no_cost_proc_chance: float = 0.0  # chance for attack to have no cost


class Frank(Lieutenant):
    id = "frank"
    faction = Faction.MAFIA
    rarity = Rarity.EPIC
    ability_areas = []

    def build_ability_params(self) -> FrankAbilityParams:
        # Scaling: 1 + star (e.g. 5* => 6% chance)
        return FrankAbilityParams(no_cost_proc_chance=1 + self.star)

    def resolve_ability(
        self,
        slot: int,
        ctx,
        params: FrankAbilityParams,
        stats,
        gear=None,
        other_lts=None,
    ):
        # No Blue Folder stats for Frank
        pass

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
