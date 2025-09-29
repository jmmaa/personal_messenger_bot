from __future__ import annotations
from dataclasses import dataclass
import typing as t
import logging

from dew import CommandNode, KwargNodes, get_keyword_seq, get_kwargs

from modules.command.di import DependencyInjector


logging = logging.getLogger(__name__)


@dataclass
class Command:
    name: str
    func: t.Callable[..., t.Any | None]
    registry: CommandRegistry

    def command(self, func: t.Callable[..., t.Any | None]):
        self.registry[func.__name__] = Command(func.__name__, func, {})

        return self.registry[func.__name__]


CommandRegistry: t.TypeAlias = dict[str, Command]


@dataclass
class CommandClient:
    registry: CommandRegistry

    def __str__(self) -> str:
        return "CommandClient"

    def register(self, command: Command):
        self.registry[command.name] = command

        logging.info(f"registered command '{command.name}'")

    def get_func(self, command: CommandNode):
        command_seq = get_keyword_seq(command)

        func = self.__get_func(self.registry, command_seq)

        if func:
            return func

        raise Exception(f"cannot find implementation for '{' '.join(command_seq)}'")

    def __get_func(self, registry: CommandRegistry, command_sequence: list[str]) -> t.Callable | None:
        name = command_sequence.pop(0)

        command = registry.get(name)

        if command is not None:
            if len(command_sequence) != 0:
                return self.__get_func(command.registry, [*command_sequence])

            else:
                return command.func
        else:
            raise Exception(f"could not find command '{name}'")

    async def execute(self, command: CommandNode):
        func = self.get_func(command)

        return await func()

    def command(self, func: t.Callable[..., t.Any | None]) -> Command:
        return Command(func.__name__, func, {})


def command(func: t.Callable[..., t.Any | None]) -> Command:
    return Command(func.__name__, func, {})


# TODO
