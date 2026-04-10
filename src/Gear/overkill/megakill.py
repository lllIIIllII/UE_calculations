from UE_core.gear import GearModifier


class Megakill(GearModifier):
    display_name = "(Overkill) Megakill"

    def applies_to(self, lt_data: dict) -> bool:
        return lt_data["id"] == "overkill"

    def apply_to_ability_params(self, params: object) -> None:
        if hasattr(params, "proc_chance"):
            params.proc_chance += 2
