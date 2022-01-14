import itertools
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Weapon:
    name: str
    damage: int
    cost: int


@dataclass
class Armor:
    name: str
    armor: int
    cost: int


@dataclass
class Ring:
    name: str
    damage: int
    armor: int
    cost: int


class Character:
    def __init__(self, hit_points: int, damage: int, armor: int) -> None:
        self._base_hp = hit_points
        self._base_damage = damage
        self._base_armor = armor

        self.hp = self._base_hp
        self.damage = self._base_damage
        self.armor = self._base_armor

    def reset(self) -> None:
        self.hp = self._base_hp
        self.damage = self._base_damage
        self.armor = self._base_armor

    @property
    def is_dead(self) -> bool:
        return self.hp <= 0

    def equip_weapon(self, weapon: Weapon) -> None:
        self.damage += weapon.damage

    def equip_armor(self, armor: Armor) -> None:
        self.armor += armor.armor

    def equip_rings(self, rings: tuple[Ring, ...]) -> None:
        self.damage += sum(ring.damage for ring in rings)
        self.armor += sum(ring.armor for ring in rings)

    def attack(self, character: "Character") -> None:
        character.hp -= max(1, self.damage - character.armor)


all_weapons = [
    Weapon(name="Dagger", damage=4, cost=8),
    Weapon(name="Shortsword", damage=5, cost=10),
    Weapon(name="Warhammer", damage=6, cost=25),
    Weapon(name="Longsword", damage=7, cost=40),
    Weapon(name="Greataxe", damage=8, cost=74),
]

all_armors = [
    Armor(name="None", armor=0, cost=0),
    Armor(name="Leather", armor=1, cost=13),
    Armor(name="Chainmail", armor=2, cost=31),
    Armor(name="Splintmail", armor=3, cost=53),
    Armor(name="Bandedmail", armor=4, cost=75),
    Armor(name="Platemail", armor=5, cost=102),
]


all_rings = [
    Ring(name="Damage +1", armor=0, damage=1, cost=25),
    Ring(name="Damage +2", armor=0, damage=2, cost=50),
    Ring(name="Damage +3", armor=0, damage=3, cost=100),
    Ring(name="Defense +1", armor=1, damage=0, cost=20),
    Ring(name="Defense +2", armor=2, damage=0, cost=40),
    Ring(name="Defense +3", armor=3, damage=0, cost=80),
]

__cache: dict[tuple[int, int], bool] = {}


def is_winner(player: Character, boss: Character) -> bool:
    cache_key = (player.armor, player.damage)
    if cache_key in __cache:
        return __cache[cache_key]

    attacker = player
    defender = boss
    while True:
        attacker.attack(defender)
        if defender.is_dead:
            res = defender is boss
            __cache[cache_key] = res
            return res

        attacker, defender = defender, attacker


def get_characters() -> tuple[Character, Character]:
    hp = int(input().split(": ")[1])
    damage = int(input().split(": ")[1])
    armor = int(input().split(": ")[1])

    boss = Character(hit_points=hp, damage=damage, armor=armor)
    player = Character(hit_points=100, damage=0, armor=0)
    return player, boss


def iterate_equipment() -> Iterator[tuple[Weapon, Armor, tuple[Ring, ...]]]:
    for weapon in all_weapons:
        for armor in all_armors:
            for nb_rings in [0, 1, 2]:
                for rings in itertools.combinations(all_rings, nb_rings):
                    yield weapon, armor, rings


def main1() -> int:
    player, boss = get_characters()
    lowest_cost = 9999
    for weapon, armor, rings in iterate_equipment():
        current_cost = (
            weapon.cost
            + (armor.cost if armor else 0)
            + sum(ring.cost for ring in rings)
        )
        if current_cost > lowest_cost:
            continue

        player.equip_weapon(weapon)
        player.equip_armor(armor)
        player.equip_rings(rings)

        if is_winner(player, boss):
            lowest_cost = current_cost

        player.reset()
        boss.reset()

    return lowest_cost


def main2() -> int:
    player, boss = get_characters()
    greatest_cost = 0
    for weapon, armor, rings in iterate_equipment():
        current_cost = (
            weapon.cost
            + (armor.cost if armor else 0)
            + sum(ring.cost for ring in rings)
        )
        if current_cost < greatest_cost:
            continue

        player.equip_weapon(weapon)
        player.equip_armor(armor)
        player.equip_rings(rings)

        if not is_winner(player, boss):
            greatest_cost = current_cost

        player.reset()
        boss.reset()

    return greatest_cost
