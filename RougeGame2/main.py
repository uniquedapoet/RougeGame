import tcod
from actions import EscapeAction, MovementAction
from Entity import Entity
from input_handler import EventHandler
from engine import Engine
from game_map import GameMap
from procgen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "Python-Projects/RougeGame2/dejavu10x10_gs_tc.png",
        32,
        8,
        tcod.tileset.CHARMAP_TCOD,
    )
    event_handler = EventHandler()

    player = Entity(
        color=(255, 255, 255),
        x=int(screen_width / 2),
        y=int(screen_height / 2),
        char="@",
    )
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "$", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width, map_height)

    engine = Engine(entites=entities, event_handler=event_handler,game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="First Rogue-like Game",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:

            
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)



if __name__ == "__main__":
    main()
