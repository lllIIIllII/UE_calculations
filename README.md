# UE calculations and simulations

This repo contains two main entry points:
- A single-loadout simulation for detailed inspection.
- A gridsearch over LT combinations for ranking and comparison.

## Single loadout test

File: `src/loadout_test.py`

Runs one loadout with the current simulation pipeline, including free-cost chains and cost-adjusted averages.
It prints:
- Standard damage stats.
- Per-hit proc breakdown (old-style proc data).
- Mean cost per attack and effective mean damage per cost.

How to run:
```powershell
python src/loadout_test.py
```

Key knobs inside the file:
- Which LTs are in the loadout.
- Stars / insignia profiles.
- Gear list.
- `allow_free_cost_chains=True` for chain modeling.

## Big gridsearch

File: `src/boss_setup_gridsearch.py`

Evaluates all combinations for the remaining slots and ranks by simulated damage.
It supports fixed candidates, free-cost chains, and cost-adjusted metrics.

How to run:
```powershell
python src/boss_setup_gridsearch.py
```

Key knobs inside the file:
- `fixed_lts`: LTs always included in each candidate set.
- `total_slots`: how many LTs make a loadout.
- `all_lts`: candidate pool with stars and insignia profiles.
- `gear_list`: loadout-wide gear.
- `allow_free_cost_chains=True` to model free-cost chains.

Outputs:
- `sim_mean_dmg`: mean damage per attack.
- `sim_mean_cost`: mean cost per attack.
- `sim_mean_eff_dmg`: cost-adjusted mean damage.
- `sim_std_dmg`, `sim_median_dmg`, `sim_min_dmg`, `sim_max_dmg`.
- A plot of either mean or median dmg with std deviations sorted descending
