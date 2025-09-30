from __future__ import annotations
import asyncio
from dataclasses import dataclass
import typing as t
import logging

from dew import CommandNode, get_keyword_seq
import dew

from yui.utils import maybe_await

from pprint import pprint

logging = logging.getLogger(__name__)


# TODO


# command_client = CommandClient({})


# @command_client.command
# @t.overload
# def main():
#     return 0


# @main.command
# def main():
#     return 0


# async def _main():
#     print(command_client.registry)
#     print(await command_client.execute("main"))


# asyncio.run(_main())


@dataclass
class Command:
    name: str
    func: t.Callable[..., t.Any | None]


@dataclass
class CommandTree:
    parent: CommandTree | None
    data: Command
    children: list[CommandTree]

    def get_command_sequence(self):
        sequence: list[CommandTree] = []

        curr = self

        in_root = False

        while not in_root:
            sequence.insert(0, curr)
            if curr.parent is None:
                in_root = True

            else:
                curr = curr.parent
        return sequence

    def command(self, name: str) -> t.Callable[[t.Callable[..., t.Any | None]], CommandTree]:
        def __wrap__(func: t.Callable[..., t.Any | None]):
            children_names = list(map(lambda c: c.data.name, self.children))

            if name in children_names:
                command_sequence = self.get_command_sequence()

                full_command_path = list(map(lambda x: x.data.name, command_sequence))
                full_command_path.append(name)
                full_command_debug_name = " ".join(full_command_path)

                raise Exception(f"cannot add duplicate command '{full_command_debug_name}'")

            data = Command(name=name, func=func)
            tree = CommandTree(parent=self, data=data, children=[])

            self.children.append(tree)

            return tree

        return __wrap__


root = CommandTree(
    parent=None,
    children=[],
    data=Command(name=".", func=lambda: print("hello!")),
)


@root.command(name="main")
def main():  # pyright: ignore
    return 0


@main.command(name="submain1")
def submain1():  # pyright: ignore
    return "gg1a"


@main.command(name="submain2")
def submain2():
    return "gg1b"


@submain2.command(name="gg1")
def gg1():
    return "gg1b"


@submain2.command(name="gg2")
def gg2():
    return "gg1b"


@main.command(name="submain3")
def submain3():
    return "gg1b"


@main.command(name="submain4")
def submain4():
    return "gg1b"


# root.add_command(Command(name="hello", func=lambda: print("hello!")))


pprint(root)


for command in root.children[0].children[0].get_command_sequence():
    print(command.data.name)
