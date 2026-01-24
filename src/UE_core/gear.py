from UE_core.loadout import BlueFolderStats
from UE_core.utils import FactionCountContext, Faction

from typing import Dict, Any
from abc import ABC, abstractmethod

class GearModifier(ABC):
    def applies_to(self, lt_data: Dict) -> bool:
        return False
        
    def get_borrowed_faction_count(
        self,
        lt_data: dict,
        ctx: FactionCountContext
    ) -> dict[Faction, int]:
        return {}

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list[Any]
    ):
        pass

    # modify faction context for the LT
    def apply_to_faction_context(self, ctx: FactionCountContext) -> None:
        pass

    # modify ability parameters (like Jared's 0.55% → 0.56%)
    def apply_to_ability_params(self, params: object) -> None:
        pass