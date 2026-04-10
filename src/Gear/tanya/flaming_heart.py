from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats


class FlamingHeart(GearModifier):
    display_name = "(Tanya) Flaming Heart"

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        if any(getattr(lt, "id", None) == "tanya" for lt in lieutenants):
            stats.crit_chance += 2
