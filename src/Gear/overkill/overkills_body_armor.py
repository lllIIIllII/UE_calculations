from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats


class OverkillsBodyArmor(GearModifier):
    display_name = "(Overkill) Overkill's Body Armor"

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        if any(getattr(lt, "id", None) == "overkill" for lt in lieutenants):
            stats.crit_chance += 1
