from enum import Enum, auto
from dataclasses import dataclass
from collections import Counter

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
    
@dataclass
class FactionCountContext:
    account: Counter[Faction]
    loadout: Counter[Faction]
    virtual: Counter[Faction]  # from gear / other LTs
    
    def total(self, faction: Faction) -> int:
        return self.account[faction] + self.loadout[faction] + self.virtual[faction]