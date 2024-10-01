from typing import Set, Iterable, Any, TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handler import EventHandler
from game_map import GameMap

# if TYPE_CHECKING:
from entity import Entity

class Engine:
    def __init__(
        self, 
        event_handler: EventHandler, 
        player: Entity, 
        game_map: GameMap
    ):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is visible it should be added to the explored array
        self.game_map.explored |= self.game_map.visible



    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        context.present(console)
        console.clear()
