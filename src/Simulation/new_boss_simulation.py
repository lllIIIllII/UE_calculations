import random
from typing import List, Dict, Tuple, Union
from UE_core.loadout import Loadout
from UE_core.lieutenant import Lieutenant
from UE_core.utils import Area  # Area enum we defined earlier
from UE_core.gear import GearModifier


def simulate_damage(
    loadout: Loadout,
    base_damage: float = 10.0,
    num_hits: int = 100_000,
    base_cost: float = 1.0,
    allow_free_cost_chains: bool = False,
    max_chain: int = 50,
    return_chain_data: bool = False,
) -> Union[
    Tuple[List[float], List[Dict[str, float]]],
    Tuple[List[float], List[Dict[str, float]], List[Dict[str, float]]],
]:
    """
    Simulate damage for a loadout using per-hit random simulation.

    Pulls crit chance, crit damage, and ability multipliers from each LT and gear.
    Supports abilities that apply to specific areas (Bossing, EvE, PvP) and
    separate hooks for:
        - Crit bonus only (Overkill)
        - Full-hit crit multipliers (Tanya, Collector)
        - Non-crit procs (Silas)
    When allow_free_cost_chains is enabled and return_chain_data is True,
    returns (hits, per_hit_proc_data, chain_data).
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
    chain_data: List[Dict[str, float]] = []

    def simulate_single_hit() -> tuple[float, float, dict]:
        hit_ctx: dict = {}
        damage = base_damage * (1 + percent_damage_mod)

        # 1. Pre-crit modifiers
        for lt in loadout.lieutenants:
            if hasattr(lt, "pre_crit"):
                damage = lt.pre_crit(damage, hit_ctx)

        # 2. Determine crit
        is_crit = random.random() < crit_chance
        hit_ctx["IsCrit"] = is_crit

        # Prepare for per-crit bonus
        crit_bonus = 0.0
        for lt in loadout.lieutenants:
            # Always initialize per-hit proc flags
            if hasattr(lt, "on_full_crit_hit"):
                hit_ctx[f"{lt.id}_proc"] = False

        if is_crit:
            # Base crit damage
            if random.random() > 0.5:
                base_crit_dmg = 1.0
            else:
                base_crit_dmg = 2.0
            crit_bonus = (damage * (1 + base_crit_dmg + crit_damage)) - damage

            # Crit-only LT hooks (e.g., Overkill)
            for lt in loadout.lieutenants:
                if hasattr(lt, "on_crit_bonus"):
                    crit_bonus = lt.on_crit_bonus(damage, crit_bonus, hit_ctx, gear=loadout.gear)

            # Full-hit crit multipliers (Tanya, Collector)
            for lt in loadout.lieutenants:
                if hasattr(lt, "on_full_crit_hit"):
                    damage, proc_flag = lt.on_full_crit_hit(damage + crit_bonus, hit_ctx, gear=loadout.gear)
                    hit_ctx[f"{lt.id}_proc"] = proc_flag
                    # crit_bonus already applied inside hook
                    crit_bonus = 0.0  # avoid double counting

        # 3. Combine base + crit bonus
        damage += crit_bonus

        # 4. Non-crit procs
        for lt in loadout.lieutenants:
            if hasattr(lt, "on_proc"):
                damage = lt.on_proc(damage, hit_ctx)

        # 5. Loadout-wide per-hit gear
        for g in loadout.gear:
            if hasattr(g, "apply_to_hit"):
                damage = g.apply_to_hit(damage, hit_ctx)

        # 6. Per-hit cost (separate from damage math)
        cost = base_cost
        for lt in loadout.lieutenants:
            if hasattr(lt, "on_cost"):
                cost = lt.on_cost(cost, hit_ctx)
        hit_ctx["cost"] = cost

        # 7. Finalize
        for lt in loadout.lieutenants:
            if hasattr(lt, "finalize"):
                damage = lt.finalize(damage, hit_ctx)

        hit_ctx["damage"] = damage
        return damage, cost, hit_ctx

    for _ in range(num_hits):
        if allow_free_cost_chains:
            chain_damage = 0.0
            chain_cost = 0.0
            chain_len = 0
            free_hits = 0

            while True:
                damage, cost, hit_ctx = simulate_single_hit()
                chain_damage += damage
                chain_cost += cost
                chain_len += 1
                if cost == 0:
                    free_hits += 1
                if return_chain_data:
                    proc_data.append(hit_ctx)

                if cost > 0 or chain_len >= max_chain:
                    break

            hits.append(chain_damage)
            chain_entry = {
                "chain_len": chain_len,
                "free_hits": free_hits,
                "total_cost": chain_cost,
            }

            if return_chain_data:
                # Preserve per-hit proc data and return chain metadata separately.
                chain_data.append(chain_entry)
            else:
                # Default: return chain summary instead of per-hit proc data.
                proc_data.append(chain_entry)
        else:
            damage, cost, hit_ctx = simulate_single_hit()
            hits.append(damage)
            proc_data.append(hit_ctx)

    if allow_free_cost_chains and return_chain_data:
        return hits, proc_data, chain_data
    return hits, proc_data
