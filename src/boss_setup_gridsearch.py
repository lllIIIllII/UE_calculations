from itertools import combinations
import pandas as pd
from tqdm import tqdm

from Simulation.new_boss_simulation import simulate_damage
from Simulation.plot_gridsearch import plot_gridsearch

from UE_core.loadout import Loadout
from UE_core.account import Account
from UE_core.utils import Faction

from Lieutenants.jared import Jared
from Lieutenants.gustavo import Gustavo
from Lieutenants.tanya import Tanya
from Lieutenants.yugo import Yugo
from Lieutenants.collector import Collector
from Lieutenants.silas import Silas
from Lieutenants.overkill import Overkill
from Lieutenants.slaughterer import Slaughterer
from Lieutenants.maddox import Maddox

from Gear.cartel_insignia import CartelInsignia
from Gear.cartel_medallion import CartelMedallion
from Gear.street_insignia import StreetInsignia
from Gear.street_medallion import StreetMedallion
from Gear.phantom_claw import PantomClaw
from Gear.thanatos_mortar import ThanatosMortar

def compute_gridsearch():
    account_100_percent = Account({
        Faction.STREET: 68,
        Faction.SYNDICATE: 53,
        Faction.MAFIA: 76,
        Faction.CARTEL: 63,
        Faction.SHADOW: 76,
    })

    all_lts = [
        Jared(star=5, insignia_profile={"crit_chance": 1}),
        Gustavo(star=5, insignia_profile={"crit_chance": 1}),
        Tanya(star=5, insignia_profile={"crit_chance": 1}),
        Yugo(star=9, insignia_profile={"crit_chance": 1}),
        Collector(star=5, insignia_profile={"crit_chance": 1}),
        Silas(star=5, insignia_profile={"crit_chance": 1}),
        Overkill(star=5, insignia_profile={"crit_chance": 1}),
        Slaughterer(star=5, insignia_profile={"crit_chance": 1}),
        Maddox(star=5, insignia_profile={"crit_chance": 1}),
    ]

    gear_list = [
        CartelInsignia(),
        CartelMedallion(),
        PantomClaw(),
        ThanatosMortar(),
        StreetInsignia(),
        StreetMedallion()
    ]
    
    gear_names = sorted(g.display_name for g in gear_list)
    gear_combo = "+".join(gear_names)

    results = []

    # Generate all unique 5-LT combinations (order doesn't matter)
    combos = list(combinations(all_lts, 5))

    for combo in tqdm(combos, desc="Evaluating loadouts"):
        # Build loadout
        loadout = Loadout(list(combo), account_100_percent, gear=gear_list)
        
        # 1️⃣ Compute deterministic Blue Folder stats
        loadout.evaluate()
        bf_stats = loadout.blue_folder_stats

        # 2️⃣ Run stochastic hit simulation
        hits, proc_data = simulate_damage(loadout, base_damage=10.0, num_hits=100_000)
        df_hits = pd.DataFrame(hits, columns=['Damage'])

        # 3️⃣ Aggregate summary for this combo
        results.append({
            "lt_combo": ", ".join(sorted(lt.id for lt in combo)),
            "gear_combo": gear_combo,
            "bf_dmg": bf_stats.dmg,
            "bf_crit_chance": bf_stats.crit_chance,
            "bf_crit_dmg": bf_stats.crit_dmg,
            "sim_mean_dmg": df_hits['Damage'].mean(),
            "sim_std_dmg": df_hits['Damage'].std(),          # <-- add this line
            "sim_median_dmg": df_hits['Damage'].median(),
            "sim_min_dmg": df_hits['Damage'].min(),
            "sim_max_dmg": df_hits['Damage'].max()
        })

    # Convert to DataFrame for analysis
    df_results = pd.DataFrame(results)

    # Example: top 10 loadouts by mean simulation damage
    top10 = df_results.sort_values("sim_mean_dmg", ascending=False).head(10)
    print(top10[[
        "lt_combo",
        "bf_dmg", "bf_crit_chance", "bf_crit_dmg",
        "sim_mean_dmg", "sim_median_dmg", "sim_min_dmg", "sim_max_dmg"
    ]])
    
    return df_results

if __name__ == "__main__":
    results = compute_gridsearch()
    
        # Keep only top 20 by mean simulated damage
    results = (
        results
        .sort_values("sim_mean_dmg", ascending=False)
        .head(20)
        .reset_index(drop=True)
    )
    
    plot_gridsearch(results, filter_by="median")
    
    