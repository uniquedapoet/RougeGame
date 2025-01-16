from typing import List, Reversible, Tuple
import textwrap

import tcod

import color


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1
        
    @property
    def full_text(self) -> str:
        """The full text of this message, including the count if necessary"""
        if self.count > 1:
            return f'{self.plain_text} (x{self.count})'
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []
    
    def add_message(
            self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True
    ) -> None:
        """
        Add a message to this log
        `text` is the message text, `fg` is the text color.
        If `stack` is True then the messages with the previous message IF its the same text
        """
        if stack and self.messages and self.messages[-1].plain_text == text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text=text, fg=fg))

    def render(self, console: tcod.Console, x: int, y:int, width: int, height: int) -> None:
        """
        Render this log over the given area
        `x`, `y`, `width`, `height` is the rectangular region to render onto the `console`
        """
        self.render_messages(console, x, y, width, height, self.messages)
    
    @staticmethod
    def render_messages(
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        """
        Render the messages
        The `messages` are rendered starting at the last message and working backwards.
        """
        y_offset = height - 1

        for messenge in reversed(messages):
            for line in reversed(textwrap.wrap(messenge.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=messenge.fg)
                y_offset -= 1
                if y_offset < 0:
                    return