from typing import List, Reversible, Tuple, Iterable
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
        """the full text of the message including count if nessasary"""
        if self.count > 1:
            return f'{self.plain_text} (x{self.count})'
        return self.plain_text
    
class MessageLog:
    def __init__(self) -> None:
        self.messages: List(Message) = []

    def add_message(
            self, text: str, fg: Tuple[int, int ,int] = color.white, *, stack: bool = True
    ) -> None:
        """
        add a message to this log
        'text' is the message text, 'fg' is the color.
        If 'stack' is True then the messages with the previous message will stack
        """
        if stack and self.messages and self.messages[-1].plain_text == text:
            self.messages[-1].count += 1

        else:
            self.messages.append(Message(text=text, fg=fg))

    def render(self, console: tcod.console, x: int, y: int, width: int, height: int) -> None:
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        for line in string.splitlines():
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

    @classmethod
    def render_messages(
        cls,
        console: tcod.console,
        x:int,
        y:int,
        width:int,
        height:int,
        messages: Reversible[Message],
    ) -> None:
        """
        Render the messages
        """
        y_offest = height - 1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x, y=y + y_offest, string=line, fg=message.fg)
                y_offest -= 1
                if y_offest <0:
                    return
        
