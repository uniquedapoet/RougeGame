from __future__ import annotations

from components.base_components import BaseComponent
from input_handler import GameOverEventHandler
from typing import TYPE_CHECKING
import color

from render_order import RenderOrder

if TYPE_CHECKING:
    from Entity import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power


    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    def die(self) -> None:

        if self.engine.player is self.parent:
            death_color = color.player_die
            death_message = 'you died'
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_color = color.enemy_die
            death_message = f'{self.parent.name} is dead'

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f'remains of {self.parent.name}'
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(text = death_message, fg = death_color)

        

    