from dataclasses import dataclass, replace


@dataclass
class Spell:
    name: str
    cost: int
    turns: int
    immediate: bool

    armor: int = 0
    damage: int = 0
    heal: int = 0
    mana: int = 0

    def clone(self) -> "Spell":
        return replace(self)


all_spells = [
    Spell(name="Magic Missile", cost=53, turns=1, damage=4, immediate=True),
    Spell(name="Drain", cost=73, turns=1, damage=2, heal=2, immediate=True),
    Spell(name="Shield", cost=113, turns=6, armor=7, immediate=False),
    Spell(name="Poison", cost=173, turns=6, damage=3, immediate=False),
    Spell(name="Recharge", cost=229, turns=5, mana=101, immediate=False),
]


@dataclass
class GameState:
    boss_hp: int
    boss_damage: int

    player_hp: int = 50
    player_mana: int = 500
    player_armor: int = 0

    current_cost: int = 0
    active_spells: tuple[Spell, ...] = ()

    @property
    def is_game_over(self) -> bool:
        return self.boss_hp <= 0 or self.player_hp <= 0

    @property
    def is_winning(self) -> bool:
        return self.boss_hp <= 0 < self.player_hp

    def clone(self) -> "GameState":
        clone = replace(self)
        clone.active_spells = tuple(spell.clone() for spell in clone.active_spells)
        return clone

    def _init_turn(self) -> None:
        self.player_armor = 0

    def _apply_spell(self, spell: Spell) -> None:
        self.player_armor += spell.armor
        self.player_hp += spell.heal
        self.player_mana += spell.mana
        self.boss_hp -= spell.damage

    def _apply_spells(self) -> None:
        new_active_spells: tuple[Spell, ...] = ()
        for spell in self.active_spells:
            self._apply_spell(spell)
            if spell.turns > 1:
                spell.turns -= 1
                new_active_spells += (spell,)
        self.active_spells = new_active_spells

    def prepare_new_turn(self, hard_mode: bool) -> None:
        self._init_turn()
        if hard_mode:
            self.player_hp -= 1
            if self.is_game_over:
                return
        self._apply_spells()

    def apply_boss_turn(self) -> None:
        self.player_hp -= max(1, self.boss_damage - self.player_armor)

    def apply_player_turn(self, spell: Spell) -> None:
        assert spell.name not in (s.name for s in self.active_spells)
        self.current_cost += spell.cost
        self.player_mana -= spell.cost
        if not spell.immediate:
            self.active_spells += (spell.clone(),)
        else:
            assert spell.turns == 1
            self._apply_spell(spell)

    def list_possible_spells(self) -> list[Spell]:
        current_active_spells = {spell.name for spell in self.active_spells}
        return [
            spell
            for spell in all_spells
            if spell.name not in current_active_spells
            and spell.cost <= self.player_mana
            and (spell.name != "Recharge" or self.player_mana < 1000)
        ]


def _main(hard_mode: bool) -> int:
    boss_hp = int(input().split(": ")[1])
    boss_damage = int(input().split(": ")[1])

    game_state = GameState(boss_hp=boss_hp, boss_damage=boss_damage)

    current_min_cost = 99999

    def inner(state: GameState, is_player_turn: bool) -> int:
        nonlocal current_min_cost
        if state.current_cost >= current_min_cost:
            return current_min_cost

        if state.is_game_over:
            if state.is_winning:
                current_min_cost = state.current_cost
            return current_min_cost

        state.prepare_new_turn(hard_mode=hard_mode and is_player_turn)

        if state.is_game_over:
            if state.is_winning:
                current_min_cost = state.current_cost
            return current_min_cost

        if is_player_turn:
            available_spells = state.list_possible_spells()
            if not available_spells:
                return current_min_cost

            for spell in available_spells:
                new_state = state.clone()
                new_state.apply_player_turn(spell)
                current_min_cost = inner(new_state, False)
        else:
            new_state = state.clone()
            new_state.apply_boss_turn()
            current_min_cost = inner(new_state, True)
        return current_min_cost

    return inner(game_state, True)


def main1() -> int:
    return _main(hard_mode=False)


def main2() -> int:
    return _main(hard_mode=True)
