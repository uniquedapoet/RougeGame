from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console

def render_bar(
        console: Console,
        current_value: int,
        maximum_value: int,
        total_width: int,
 )-> None:
    """
    Displays a bar to show the health of the player
    """
    bar_width = int(float(current_value) / maximum_value * total_width) # Calculate the length of the bar


    # Render the background first with total_width
    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    # Render the bar on top of the background depending on the current value
    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(1, 45, f'HP: {current_value}/{maximum_value}', fg=color.bar_text)