from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, FactionCountContext

from dataclasses import dataclass

from typing import Dict

class Gustavo(Lieutenant):
    id = "gustavo"
    faction = Faction.CARTEL
    rarity = Rarity.EPIC
    ability_areas = [] 

    # Star-to-ability mapping
    star_params: Dict[int, Dict[str, float]] = {
        1: {"crit_chance": 4.0, "crit_dmg": 15.0},
        2: {"crit_chance": 5.0, "crit_dmg": 22.0},
        3: {"crit_chance": 6.0, "crit_dmg": 30.0},
        4: {"crit_chance": 7.0, "crit_dmg": 39.0},
        5: {"crit_chance": 8.0, "crit_dmg": 48.0},
        6: {"crit_chance": 10.0, "crit_dmg": 58.0},
        7: {"crit_chance": 12.0, "crit_dmg": 69.0},
        8: {"crit_chance": 14.0, "crit_dmg": 81.0},
        9: {"crit_chance": 16.0, "crit_dmg": 98.0},
    }
        
    def default_insignia_profile(self) -> dict:
        return {
            "crit_dmg": 0.02
        }

    def build_ability_params(self) -> Dict[str, float]:
        """Return the ability parameters for the current star."""
        return self.star_params.get(self.star, {"crit_chance": 0, "crit_dmg": 0})

    def resolve_ability(
        self, slot: int, ctx: "FactionCountContext", params: Dict[str, float], stats: "BlueFolderStats", gear
    ):
        """Apply Gustavo's ability to the Blue Folder stats."""
        stats.crit_chance += params["crit_chance"]
        stats.crit_dmg += params["crit_dmg"]