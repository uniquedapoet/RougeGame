from __future__ import annotations

import copy

from typing import Tuple, TypeVar, TYPE_CHECKING, Optional, Type

from render_order import RenderOrder

if TYPE_CHECKING:
    from game_map import game_map
    from components.ai import BaseAi
    from components.fighter import Fighter 

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc
    """
    game_map: game_map

    def __init__(self,
                 game_map: Optional[game_map] = None,
                 x: int = 0,
                 y: int = 0,
                 char: str = '!',
                 color: Tuple[int, int, int] = (255, 255, 255),
                 name: str = "<Unnamed>",
                 blocks_movement: bool = False,
                 render_order: RenderOrder = RenderOrder.CORPSE,
                 ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

        if game_map:
            # If game_map isn't provided now then it will be set later
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self: T, game_map: game_map, x: int, y: int) -> T:
        """
        Spawns an entity at a given location
        """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        game_map.entities.add(clone)
        return clone

    def move(self, dx, dy) -> None:
        """
        Move Entity by a given amount
        """
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int, game_map: Optional[game_map] = None) -> None:
        """
        Place entity at a given location
        """
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = '?',
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAi],
        fighter: Fighter,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAi] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)