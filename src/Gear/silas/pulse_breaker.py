from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats


class PulseBreaker(GearModifier):
    display_name = "(Silas) Pulse Breaker"

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        if any(getattr(lt, "id", None) == "silas" for lt in lieutenants):
            stats.crit_chance += 3
