from dataclasses import dataclass

@dataclass
class BlueFolderStats:
    dmg: float = 0.0
    crit_chance: float = 0.0
    crit_dmg: float = 0.0

    def reset(self):
        self.dmg = 0.0
        self.crit_chance = 0.0
        self.crit_dmg = 0.0

    def add(self, other: "BlueFolderStats"):
        self.dmg += other.dmg
        self.crit_chance += other.crit_chance
        self.crit_dmg += other.crit_dmg