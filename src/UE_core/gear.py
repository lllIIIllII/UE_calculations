from UE_core.loadout import BlueFolderStats
from UE_core.utils import FactionCountContext, Faction

from typing import Dict
from abc import ABC, abstractmethod

class GearModifier(ABC):
    @abstractmethod
    def applies_to(self, lt_data: Dict) -> bool:
        ...

    # modify Blue Folder stats
    def apply_to_stats(self, stats: BlueFolderStats) -> None:
        pass

    # modify faction context for the LT
    def apply_to_faction_context(self, ctx: FactionCountContext) -> None:
        pass

    # modify ability parameters (like Jared's 0.55% → 0.56%)
    def apply_to_ability_params(self, params: object) -> None:
        pass