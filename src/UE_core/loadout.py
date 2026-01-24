from UE_core.stats import BlueFolderStats
from UE_core.lieutenant import Lieutenant
from UE_core.gear import GearModifier
from UE_core.account import Account
from UE_core.utils import Area


from collections import Counter
from typing import Optional


class Loadout:
    def __init__(
            self, 
            lieutenants: list[Lieutenant],
            account: Account, 
            gear: Optional[list[GearModifier]] = None
        ):
        self.lieutenants = lieutenants
        self.gear = gear if gear is not None else []
        self.account = account
        self.blue_folder_stats = BlueFolderStats()

        # Local faction counts
        self.loadout_faction_counts = Counter(lt.faction for lt in lieutenants)

    def evaluate(self):
        self.blue_folder_stats.reset()
        for slot, lt in enumerate(self.lieutenants, start=1):
            lt_stats = lt.get_blue_folder_stats(
                slot=slot,
                loadout_factions=self.loadout_faction_counts,
                account_factions=self.account.faction_counts,
                gear=self.gear,
                other_lts=[l for l in self.lieutenants if l != lt],
            )
            self.blue_folder_stats.add(lt_stats)
        
        # loadout-wide gear
        for g in self.gear:
            if hasattr(g, "apply_to_loadout_stats"):
                g.apply_to_loadout_stats(self.blue_folder_stats, self.lieutenants)
            
    def evaluate_area(self, area: Area):
        area_stats = BlueFolderStats()
        for slot, lt in enumerate(self.lieutenants, start=1):
            lt_stats = lt.get_area_stats(
                area=area,
                slot=slot,
                loadout_factions=self.loadout_faction_counts,
                account_factions=self.account.faction_counts,
                gear=self.gear,
                other_lts=[l for l in self.lieutenants if l != lt],
            )
            area_stats.add(lt_stats)
            
        # loadout-wide gear still applies if relevant
        for g in self.gear:
            g.apply_to_loadout_stats(area_stats, self.lieutenants)
            
        return area_stats

    