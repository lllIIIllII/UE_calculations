from UE_core.loadout import Loadout
from UE_core.account import Account
from UE_core.utils import Faction

from Simulation.new_boss_simulation import simulate_damage

from Lieutenants.jared import Jared
from Lieutenants.gustavo import Gustavo
from Lieutenants.tanya import Tanya
from Lieutenants.yugo import Yugo
from Lieutenants.collector import Collector
from Lieutenants.silas import Silas
from Lieutenants.overkill import Overkill
from Lieutenants.slaughterer import Slaughterer
from Lieutenants.maddox import Maddox
from Lieutenants.cole import Cole

from Gear.cartel_insignia import CartelInsignia
from Gear.cartel_medallion import CartelMedallion
from Gear.street_insignia import StreetInsignia
from Gear.street_medallion import StreetMedallion
from Gear.phantom_claw import PantomClaw
from Gear.thanatos_mortar import ThanatosMortar
from Gear.underworld_crown import UnderworldCrown

import pandas as pd


if __name__ == "__main__":

    account_80_percent = Account({
        Faction.STREET: 68,
        Faction.SYNDICATE: 53,
        Faction.MAFIA: 76,
        Faction.CARTEL: 63,
        Faction.SHADOW: 76,
    })

    jared = Jared(
        star=5,
        insignia_profile={"crit_chance": 1}
    )
    gustavo = Gustavo(
        star=5,
        insignia_profile={"crit_chance": 1}
    )
    tanya = Tanya(
        star=5,
        insignia_profile={"crit_chance": 1}
    )
    yugo = Yugo(
        star=9,
        insignia_profile={"crit_chance": 1}
    )
    collector = Collector(
        star=4,
        insignia_profile={"crit_chance": 1}
    )
    silas = Silas(
        star=5,
        insignia_profile={"crit_chance": 1}
    )
    overkill = Overkill(
        star=6,
        insignia_profile={"crit_chance": 1}
    )
    slaughterer = Slaughterer(
        star=5,
        insignia_profile={"crit_chance": 1}
    )
    maddox = Maddox(
        star=4,
        insignia_profile={"crit_chance": 1}
    )
    cole = Cole(
        star=4,
        insignia_profile={"crit_chance": 1}
    )
    
    loadout = Loadout(
        [overkill, tanya, collector, slaughterer, jared],
        account_80_percent,
        gear=[
            CartelInsignia(),
            CartelMedallion(),
            PantomClaw(),
            ThanatosMortar(),
            StreetInsignia(),
            StreetMedallion(),
            UnderworldCrown()
        ],
        sk_added_crit_chance=10,
    )
    loadout.evaluate()

    hits, proc_data, chain_data = simulate_damage(
        loadout,
        base_damage=10.0,
        num_hits=100_000,
        allow_free_cost_chains=True,
        return_chain_data=True,
    )

    df_hits = pd.DataFrame(hits, columns=["Damage"])
    df_proc_data = pd.DataFrame(proc_data)
    df_chain_data = pd.DataFrame(chain_data)

    # Basic statistics
    print(df_hits.describe())
    print("\n")
    print(df_proc_data.value_counts())
    print("\n")
    mean_cost = df_chain_data["total_cost"].mean()
    effective_mean_dmg = df_hits["Damage"].mean() / mean_cost
    print(f"Mean cost per hit: {mean_cost:.4f}")
    print(f"Effective mean damage (per cost): {effective_mean_dmg:.4f}")

    print(f"Blue Folder stats for loadout:")
    print(f"Dmg: {loadout.blue_folder_stats.dmg:.4f}")
    print(f"Crit Chance: {loadout.blue_folder_stats.crit_chance:.4f}")
    print(f"Crit Dmg: {loadout.blue_folder_stats.crit_dmg:.4f}")
