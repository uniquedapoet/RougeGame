import numpy as np
from typing import Tuple, TYPE_CHECKING, List, Iterable
from tcod.console import Console
import tiles_types

from entity import Entity

class GameMap:
    def __init__(self, width: int, height:int, entities:Iterable[Entity]=()):   
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tiles_types.wall, order='F')
        self.entities = set(entities)
        self.visible = np.full((width, height), fill_value=False, order='F') # Tiles we can see
        self.explored = np.full((width, height), fill_value=False, order='F') # Tiles we have been to but can't see 


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map"""
        return 0 <= x , self.width and 0 <= y < self.height 
    
    def render(self, console: Console) -> None:
        """
        Render's the map
        If a tile is in the visible array, then draw it with the "light" colors
        If it isn't, but it's in the explored array, then draw it with the "dark" colors
        Otherwise, the default is "SHROUD"
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tiles_types.SHROUD
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)