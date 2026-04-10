from UE_core.gear import GearModifier


class GildedObsidian(GearModifier):
    display_name = "(Collector) Gilded Obsidian"

    def applies_to(self, lt_data: dict) -> bool:
        return lt_data["id"] == "collector"

    def apply_to_ability_params(self, params: object) -> None:
        if hasattr(params, "crit_multiplier"):
            params.crit_multiplier += 0.5
