from UE_core.utils import Faction
from collections import Counter
from typing import Mapping

class Account:
    def __init__(self, faction_counts: Mapping[Faction, int]):
        # copy so callers can’t mutate you accidentally
        self.faction_counts = Counter(faction_counts)

    def get_faction_count(self, faction: Faction) -> int:
        return self.faction_counts[faction]