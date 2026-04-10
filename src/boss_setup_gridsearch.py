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
from Lieutenants.cole import Cole
from Lieutenants.frank import Frank
from Lieutenants.slaughterer import Slaughterer
from Lieutenants.maddox import Maddox

from Gear.cartel_insignia import CartelInsignia
from Gear.cartel_medallion import CartelMedallion
from Gear.street_insignia import StreetInsignia
from Gear.street_medallion import StreetMedallion
from Gear.phantom_claw import PantomClaw
from Gear.thanatos_mortar import ThanatosMortar
from Gear.underworld_crown import UnderworldCrown
from Gear.underworld_ring import UnderworldRing
from Gear.collector.flame_time import FlameTime
from Gear.collector.gilded_obsidian import GildedObsidian
from Gear.gustavo.tohil import Tohil
from Gear.overkill.megakill import Megakill
from Gear.overkill.overkills_body_armor import OverkillsBodyArmor
from Gear.overkill.ultrakill import Ultrakill
from Gear.silas.bullet_storm import BulletStorm
from Gear.silas.pulse_breaker import PulseBreaker
from Gear.silas.scythe_claw import ScytheClaw
from Gear.tanya.flaming_heart import FlamingHeart
from Gear.tanya.grisha import Grisha
from Gear.tanya.nightfang import Nightfang
from Gear.tanya.nightshade_grips import NightshadeGrips
from Gear.tanya.obsidian_edge import ObsidianEdge


def compute_gridsearch():
    account_100_percent = Account({
        Faction.STREET: 70,
        Faction.SYNDICATE: 54,
        Faction.MAFIA: 78,
        Faction.CARTEL: 63,
        Faction.SHADOW: 76,
    })

    all_lts = [
        Jared(star=7, insignia_profile={"crit_chance": 1}),
        Gustavo(star=4, insignia_profile={"crit_chance": 1}),
        Tanya(star=5, insignia_profile={"crit_chance": 1}),
        Yugo(star=9, insignia_profile={"crit_chance": 1}),
        Collector(star=4, insignia_profile={"crit_chance": 1}),
        Silas(star=4, insignia_profile={"crit_chance": 1}),
        Overkill(star=6, insignia_profile={"crit_chance": 1}),
        #Slaughterer(star=5, insignia_profile={"crit_chance": 1}),
        #Maddox(star=5, insignia_profile={"crit_chance": 1}),
        Cole(star=4, insignia_profile={"crit_chance": 1}),
        Frank(star=6, insignia_profile={"crit_chance": 1}),
    ]

    # ---- Fixed candidates (always included) ----
    fixed_lts = [
        # Example:
        # Cole(star=4, insignia_profile={"crit_chance": 1}),
        Frank(star=6, insignia_profile={"crit_chance": 1}),
        Collector(star=4, insignia_profile={"crit_chance": 1}),
    ]
    total_slots = 5
    remaining_slots = total_slots - len(fixed_lts)
    if remaining_slots < 0:
        raise ValueError("fixed_lts exceeds total_slots")

    gear_list = [
        CartelInsignia(),
        CartelMedallion(),
        PantomClaw(),
        ThanatosMortar(),
        StreetInsignia(),
        StreetMedallion(),
        UnderworldCrown(),
        UnderworldRing(),
    ]

    generic_gear_names = sorted(
        g.display_name for g in gear_list if not g.display_name.startswith("(")
    )
    lt_specific_gear_names = sorted(
        g.display_name for g in gear_list if g.display_name.startswith("(")
    )
    gear_combo = "+".join(generic_gear_names)

    lt_pool = ", ".join(
        f"{lt.id} {lt.star}*"
        for lt in sorted(all_lts, key=lambda lt: lt.id)
    )

    lt_specific_gear_combo = "+".join(lt_specific_gear_names)

    results = []

    # Generate all unique combinations for remaining slots
    available_lts = [lt for lt in all_lts if lt not in fixed_lts]
    combos = list(combinations(available_lts, remaining_slots))

    for combo in tqdm(combos, desc="Evaluating loadouts"):
        # Build loadout
        loadout_lts = fixed_lts + list(combo)
        loadout = Loadout(loadout_lts, account_100_percent, gear=gear_list, sk_added_crit_chance=15)

        # 1. Compute deterministic Blue Folder stats
        loadout.evaluate()
        bf_stats = loadout.blue_folder_stats

        # 2. Run stochastic hit simulation
        hits, proc_data = simulate_damage(
            loadout,
            base_damage=10.0,
            num_hits=100_000,
            allow_free_cost_chains=True,
        )
        df_hits = pd.DataFrame(hits, columns=["Damage"])
        df_proc = pd.DataFrame(proc_data)
        cost_col = "total_cost" if "total_cost" in df_proc.columns else "cost"
        mean_cost = df_proc[cost_col].mean()
        effective_mean_dmg = df_hits["Damage"].mean() / mean_cost

        # 3. Aggregate summary for this combo
        results.append({
            "lt_combo": ", ".join(sorted(lt.id for lt in loadout_lts)),
            "gear_combo": gear_combo,
            "lt_pool": lt_pool,
            "lt_specific_gear_combo": lt_specific_gear_combo,
            "bf_dmg": bf_stats.dmg,
            "bf_crit_chance": bf_stats.crit_chance,
            "bf_crit_dmg": bf_stats.crit_dmg,
            "sim_mean_dmg": df_hits["Damage"].mean(),
            "sim_mean_cost": mean_cost,
            "sim_mean_eff_dmg": effective_mean_dmg,
            "sim_std_dmg": df_hits["Damage"].std(),
            "sim_median_dmg": df_hits["Damage"].median(),
            "sim_min_dmg": df_hits["Damage"].min(),
            "sim_max_dmg": df_hits["Damage"].max(),
        })

    # Convert to DataFrame for analysis
    df_results = pd.DataFrame(results)

    # Example: top 10 loadouts by mean simulation damage
    top10 = df_results.sort_values("sim_mean_dmg", ascending=False).head(10)
    print(top10[[
        "lt_combo",
        "bf_dmg", "bf_crit_chance", "bf_crit_dmg",
        "sim_mean_dmg", "sim_mean_cost", "sim_mean_eff_dmg",
        "sim_median_dmg", "sim_min_dmg", "sim_max_dmg",
    ]])

    return df_results


if __name__ == "__main__":
    results = compute_gridsearch()

    # Keep only top 20 by mean simulated damage
    results = (
        results
        .sort_values("sim_mean_eff_dmg", ascending=False)
        .head(20)
        .reset_index(drop=True)
    )

    plot_gridsearch(results, filter_by="mean")
