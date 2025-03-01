from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
import random

from input_handler import MainGameEventHandler
from render_functions import render_bar, render_names_at_mouse_location
from message_log import MessageLog

if TYPE_CHECKING:
    from entity import Actor  
    from game_map import GameMap
    from input_handler import EventHandler


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler = MainGameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is visible it should be added to the explored array
        self.game_map.explored |= self.game_map.visible

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai and random.random() < 0.5:
                entity.ai.perform()

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=self.player.fighter.max_hp,
        )

        render_names_at_mouse_location(x=21,y=44,console=console,engine=self)
