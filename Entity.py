from __future__ import annotations

import copy

from typing import Tuple, TypeVar, TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from game_map import GameMap
    from components.ai import BaseAi
    from components.fighter import Fighter 

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc
    """

    gamemap: GameMap

    def __init__(self,
                 game_map: Optional[GameMap] = None,
                 x: int = 0,
                 y: int = 0,
                 char: str = '!',
                 color: Tuple[int, int, int] = (255, 255, 255),
                 name: str = "<Unnamed>",
                 blocks_movement: bool = False,
                 ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if game_map:
            # If gamemap isn't provided now then it will be set later
            self.gamemap = game_map
            game_map.entities.add(self)

    def spawn(self: T, game_map: GameMap, x: int, y: int) -> T:
        """
        Spawns an entity at a given location
        """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = game_map
        game_map.entities.add(clone)
        return clone

    def move(self, dx, dy) -> None:
        """
        Move Entity by a given amount
        """
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """
        Place entity at a given location
        """
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"):
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)


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
        )

        self.ai: Optional[BaseAi] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)