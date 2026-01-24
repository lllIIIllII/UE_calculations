import random
from typing import List, Dict, Tuple
from UE_core.loadout import Loadout
from UE_core.lieutenant import Lieutenant
from UE_core.utils import Area  # Area enum we defined earlier
from UE_core.gear import GearModifier

def simulate_damage(
    loadout: Loadout,
    base_damage: float = 10.0,
    num_hits: int = 100_000
) -> Tuple[List[float], List[Dict[str, float]]]:
    """
    Simulate damage for a loadout using per-hit random simulation.
    
    Pulls crit chance, crit damage, and ability multipliers from each LT and gear.
    Supports abilities that apply to specific areas (Bossing, EvE, PvP) and
    separate hooks for:
        - Crit bonus only (Overkill)
        - Full-hit crit multipliers (Tanya, Collector)
        - Non-crit procs (Silas)
    """

    # --- Precompute loadout stats (Blue Folder + loadout-wide gear) ---
    loadout.evaluate()  # computes blue_folder_stats once
    blue_stats = loadout.blue_folder_stats
    crit_chance = blue_stats.crit_chance / 100
    crit_damage = blue_stats.crit_dmg / 100
    percent_damage_mod = blue_stats.dmg / 100

    # Precompute bossing/EvE stats for LTs that use them
    bossing_stats = loadout.evaluate_area(Area.BOSSING)
    eve_stats = loadout.evaluate_area(Area.EVE)

    hits: List[float] = []
    proc_data: List[Dict[str, float]] = []

    for _ in range(num_hits):
        hit_ctx: dict = {}
        damage = base_damage * (1 + blue_stats.dmg / 100)

        # 1️⃣ Pre-crit modifiers
        for lt in loadout.lieutenants:
            if hasattr(lt, "pre_crit"):
                damage = lt.pre_crit(damage, hit_ctx)

        # 2️⃣ Determine crit
        is_crit = random.random() < blue_stats.crit_chance / 100
        hit_ctx["IsCrit"] = is_crit

        # Prepare for per-crit bonus
        crit_bonus = 0.0
        for lt in loadout.lieutenants:
            # Always initialize per-hit proc flags
            if hasattr(lt, "on_full_crit_hit"):
                hit_ctx[f"{lt.id}_proc"] = False

        if is_crit:
            # Base crit damage
            crit_bonus = damage * (blue_stats.crit_dmg / 100)

            # Crit-only LT hooks (e.g., Overkill)
            for lt in loadout.lieutenants:
                if hasattr(lt, "on_crit_bonus"):
                    crit_bonus = lt.on_crit_bonus(damage, crit_bonus, hit_ctx)

            # Full-hit crit multipliers (Tanya, Collector)
            for lt in loadout.lieutenants:
                if hasattr(lt, "on_full_crit_hit"):
                    damage, proc_flag = lt.on_full_crit_hit(damage + crit_bonus, hit_ctx)
                    hit_ctx[f"{lt.id}_proc"] = proc_flag
                    # crit_bonus already applied inside hook
                    crit_bonus = 0.0  # avoid double counting

        # 3️⃣ Combine base + crit bonus
        damage += crit_bonus

        # 4️⃣ Non-crit procs
        for lt in loadout.lieutenants:
            if hasattr(lt, "on_proc"):
                damage = lt.on_proc(damage, hit_ctx)

        # 5️⃣ Loadout-wide per-hit gear
        for g in loadout.gear:
            if hasattr(g, "apply_to_hit"):
                damage = g.apply_to_hit(damage, hit_ctx)

        # 6️⃣ Finalize
        for lt in loadout.lieutenants:
            if hasattr(lt, "finalize"):
                damage = lt.finalize(damage, hit_ctx)

        hits.append(damage)
        proc_data.append(hit_ctx)

    return hits, proc_data