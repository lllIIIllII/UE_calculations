from UE_core.loadout import Loadout
from UE_core.account import Account
from UE_core.utils import Faction

from Lieutenants.jared import Jared
from Lieutenants.gustavo import Gustavo

from Gear.cartel_insignia import CartelInsignia

if __name__ == "__main__":

    account_80_percent = Account({
        Faction.STREET: 72,
        Faction.SYNDICATE: 61,
        Faction.MAFIA: 80,
        Faction.CARTEL: 63,
        Faction.SHADOW: 73,
    })

    jared = Jared(star=5)
    gustavo = Gustavo(star=5)
    loadout = Loadout([jared, gustavo], account_80_percent, gear=[CartelInsignia()])
    loadout.evaluate()

    print(f"Blue Folder stats for loadout:")
    print(f"Dmg: {loadout.blue_folder_stats.dmg:.4f}")
    print(f"Crit Chance: {loadout.blue_folder_stats.crit_chance:.4f}")
    print(f"Crit Dmg: {loadout.blue_folder_stats.crit_dmg:.4f}")