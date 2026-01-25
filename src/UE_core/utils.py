from enum import Enum, auto
from dataclasses import dataclass
from collections import defaultdict

class Rarity(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()
    
class Faction(Enum):
    STREET = auto()
    SYNDICATE = auto()
    MAFIA = auto()
    CARTEL = auto()
    SHADOW = auto()
    
class Area(Enum):
    BLUE_FOLDER = auto()
    PVP = auto()
    BOSSING = auto()
    EVE = auto()
    
    
class FactionCountContext:
    def __init__(self, account, loadout, virtual=None, flags=None):
        self.account = account
        self.loadout = loadout
        self.virtual = virtual if virtual is not None else defaultdict(float)

    def total(self, faction: Faction) -> int:
        return (
            self.account.get(faction, 0)
            + self.virtual.get(faction, 0)
        )