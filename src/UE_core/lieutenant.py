from UE_core.utils import Rarity, Faction, FactionCountContext
from UE_core.stats import BlueFolderStats
from UE_core.gear import GearModifier

from collections import Counter
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Lieutenant:
    id: str
    faction: Faction
    rarity: Rarity
    
    def __init__(self, star: int):
        self.star = star

    def get_blue_folder_stats(
        self,
        slot: int,
        loadout_factions: Counter,
        account_factions: Counter,
        gear: Optional[list["GearModifier"]] = None,
        other_lts: Optional[list] = None,
    ) -> "BlueFolderStats":
        stats = BlueFolderStats()
        ctx = FactionCountContext(
            account=account_factions,
            loadout=loadout_factions.copy(),  # copy for safe gear modifications
            virtual=Counter(),
        )

        gear = gear or []
        other_lts = other_lts or []

        # Apply gear effects on faction context
        lt_data = {
            "id": getattr(self, "id", ""),
            "faction": getattr(self, "faction", ""),
            "rarity": getattr(self, "rarity", ""),
            "star": getattr(self, "star", 1),
        }

        for g in gear:
            if g.applies_to(lt_data):
                g.apply_to_faction_context(ctx)

        params = self.build_ability_params()
        self.resolve_ability(slot, ctx, params, stats)

        return stats

    def build_ability_params(self):
        return object()  # placeholder for concrete LT

    def resolve_ability(self, slot, ctx, params, stats):
        pass