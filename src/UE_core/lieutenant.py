from UE_core.utils import Rarity, Faction, FactionCountContext, Area
from UE_core.stats import BlueFolderStats
from UE_core.gear import GearModifier

from collections import Counter
from dataclasses import dataclass, field
from typing import Optional, Any

@dataclass
class Lieutenant:
    id: str
    faction: Faction
    rarity: Rarity
    # By default, abilities apply to the Blue Folder only
    ability_areas: list["Area"] = field(default_factory=list)
    INSIGNIA_SLOTS = {
        Rarity.RARE: [
            (1, 2),
            (3, 3),
            (6, 4),
            (9, 5),
        ],
        Rarity.EPIC: [
            (1, 2),
            (2, 3),
            (3, 4),
            (6, 5),
            (9, 6),
        ],
    }
    
    def __init__(self, star: int, insignia_profile: dict | None = None):
        self.star = star
        self.insignia_profile = insignia_profile
        
    def default_insignia_profile(self) -> dict:
        return {}
        
    def get_insignia_slots(self) -> int:
        progression = self.INSIGNIA_SLOTS.get(self.rarity, [])
        slots = 0
        for required_star, slot_count in progression:
            if self.star >= required_star:
                slots = slot_count
        return slots

    def get_insignia_profile(self) -> dict:
        if self.insignia_profile is not None:
            return self.insignia_profile
        return self.default_insignia_profile()
    
    def apply_insignias(self, stats: "BlueFolderStats"):
        slots = self.get_insignia_slots()
        profile = self.get_insignia_profile()

        for stat, value_per_slot in profile.items():
            setattr(stats, stat, getattr(stats, stat) + slots * value_per_slot)

    def get_area_stats(
        self,
        area: Area,
        slot: int,
        loadout_factions: Counter,
        account_factions: Counter,
        gear: Optional[list["GearModifier"]] = None,
        other_lts: Optional[list] = None,
    ) -> "BlueFolderStats":
        stats = BlueFolderStats()
        
        ctx = FactionCountContext(
            account=account_factions.copy(),
            loadout=loadout_factions.copy(),
            virtual={},
        )

        gear = gear or []
        other_lts = other_lts or []

        for g in gear:
            if g.applies_to(self.get_lt_data()):
                g.apply_to_faction_context(ctx)

        params = self.build_ability_params()
        
        if area == Area.BLUE_FOLDER:
            self.resolve_ability(slot, ctx, params, stats, gear, other_lts)
        elif area in self.ability_areas:
            self.resolve_ability_area(area, slot, ctx, params, stats, gear, other_lts)
        self.apply_insignias(stats)

        return stats
    
        # --- Generic wrapper for Loadout evaluation ---
    def get_blue_folder_stats(
        self,
        slot: int,
        loadout_factions: dict,
        account_factions: dict,
        gear: list = None,
        other_lts: list = None,
    ) -> BlueFolderStats:
        if gear is None:
            gear = []
        if other_lts is None:
            other_lts = []

        stats = BlueFolderStats()
        params = self.build_ability_params()

        ctx = FactionCountContext(
            loadout=loadout_factions,
            virtual={},
            account=account_factions
        )

        self.resolve_ability(slot=slot, ctx=ctx, params=params, stats=stats, gear=gear)
        return stats

    def build_ability_params(self):
        return object()  # placeholder for concrete LT

    def resolve_ability(
        self,
        slot: int,
        ctx: "FactionCountContext",
        params: Any,
        stats: "BlueFolderStats",
        gear: list[Any] = None
    ):
        """
        Default implementation (can be overridden by concrete LTs).
        `gear` is optional for abilities that need it.
        """
        pass
    
        def resolve_ability_area(
            self,
            area: "Area",
            slot: int,
            ctx: "FactionCountContext",
            params: Any,
            stats: "BlueFolderStats",
            gear: list[Any] = None,
            other_lts: list["Lieutenant"] = None
        ):
            """
            Default: do nothing.
            Concrete LTs like Tanya override this to apply their area-specific effects.
            """
            pass
    
    def get_lt_data(self) -> dict:
        return {
            "id": self.id,
            "faction": self.faction,
            "rarity": self.rarity,
            "star": self.star,
            "insignia_profile": self.insignia_profile,
        }