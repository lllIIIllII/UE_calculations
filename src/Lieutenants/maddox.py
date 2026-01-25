from UE_core.lieutenant import Lieutenant
from UE_core.loadout import BlueFolderStats
from UE_core.utils import Rarity, Faction, FactionCountContext

from dataclasses import dataclass

from typing import Dict

class Maddox(Lieutenant):
    id = "maddox"
    faction = Faction.STREET
    rarity = Rarity.EPIC
    ability_areas = [] 

    # Star-to-ability mapping
    star_params: Dict[int, Dict[str, float]] = {
        1: {"crit_chance": 5.0, "crit_dmg": 10.0},
        2: {"crit_chance": 6.0, "crit_dmg": 15.0},
        3: {"crit_chance": 7.0, "crit_dmg": 20.0},
        4: {"crit_chance": 8.0, "crit_dmg": 25.0},
        5: {"crit_chance": 10.0, "crit_dmg": 30.0},
        6: {"crit_chance": 12.0, "crit_dmg": 35.0},
        7: {"crit_chance": 14.0, "crit_dmg": 40.0},
        8: {"crit_chance": 17.0, "crit_dmg": 50.0},
        9: {"crit_chance": 20.0, "crit_dmg": 60.0},
    }
        
    def default_insignia_profile(self) -> dict:
        return {
            "crit_dmg": 0.02
        }

    def build_ability_params(self) -> Dict[str, float]:
        """Return the ability parameters for the current star."""
        return self.star_params.get(self.star, {"crit_chance": 0, "crit_dmg": 0})

    def resolve_ability(
        self, 
        slot: int, 
        ctx: "FactionCountContext", 
        params: Dict[str, float], 
        stats: "BlueFolderStats", 
        gear,
        other_lts: list["Lieutenant"] = None,
    ):
        """Apply Maddox's ability to the Blue Folder stats."""
        stats.crit_chance += params["crit_chance"]
        stats.crit_dmg += params["crit_dmg"]