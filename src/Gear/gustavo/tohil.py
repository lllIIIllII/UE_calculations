from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats


class Tohil(GearModifier):
    display_name = "(Gustavo) Tohil"

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        if any(getattr(lt, "id", None) == "gustavo" for lt in lieutenants):
            stats.crit_dmg += 5
