from UE_core.gear import GearModifier
from UE_core.lieutenant import Lieutenant
from UE_core.stats import BlueFolderStats


class BulletStorm(GearModifier):
    display_name = "(Silas) Bullet Storm"

    def apply_to_loadout_stats(
        self,
        stats: BlueFolderStats,
        lieutenants: list["Lieutenant"]
    ):
        if any(getattr(lt, "id", None) == "silas" for lt in lieutenants):
            stats.dmg += 3
