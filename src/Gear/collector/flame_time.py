from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats


class FlameTime(GearModifier):
    display_name = "(Collector) Flame Time"

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        if any(getattr(lt, "id", None) == "collector" for lt in lieutenants):
            stats.crit_chance += 3
