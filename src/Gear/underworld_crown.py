from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats
from UE_core.utils import Rarity

class UnderworldCrown(GearModifier):
    display_name = "Underworld Crown"
    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        epic_count = sum(
            1 for lt in lieutenants if lt.rarity == Rarity.EPIC
        )

        stats.crit_chance += 1 * epic_count