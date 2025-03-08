from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple
import color

if TYPE_CHECKING:
    from Entity import Entity, Actor
    from engine import Engine



class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """
        Return the engine this action belongs to.
        """
        return self.entity.gamemap.engine


    def perform(self) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in 

        `self.entity` is the object performing the action

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """
        Returns this entities destination x, y coordinates
        """
        return self.entity.x + self.dx, self.entity.y + self.dy 
   
    @property
    def blocking_entity(self) -> Optional[Entity]:
        """
        Return the blocking entity at this actions destination
        """
        return self.engine.game_map.get_blocking_enemy_at_location(*self.dest_xy)
    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)
    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """
    Perform a melee action in the given direction
    Inherits from ActionWithDirection
    """
    def perform(self) -> None:   
        target = self.target_actor

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"

        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
            

        if damage > 0:
            self.engine.message_log.add_message(text = f"{attack_desc} for {damage} hit points", fg = attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(text = f"{attack_desc} but does no damage", fg = attack_color)


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # if were out of bounds dont move
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if self.engine.game_map.get_blocking_enemy_at_location(dest_x, dest_y):
            return              

        self.entity.move(self.dx, self.dy)

class WaitAction(Action):
    def perform(self) -> None:
        pass

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
        