from __future__ import annotations

from dataclasses import dataclass
import typing as t
import logging

from bot.commands.di import DependencyInjector
from dew import CommandNode, KwargNodes, parse

logging = logging.getLogger(__name__)


def get_kwargs(node: CommandNode) -> KwargNodes:
    tail = node["tail"]

    if isinstance(tail, dict):
        return get_kwargs(tail)

    else:
        return tail


def get_keyword_seq(node: CommandNode) -> list[str]:
    return __get_keyword_seq(node, [node["name"]])


def __get_keyword_seq(node: CommandNode, acc: list[str]) -> list[str]:
    tail = node["tail"]

    if isinstance(tail, dict):
        return __get_keyword_seq(tail, [*acc, tail["name"]])

    else:
        return acc


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
    di: DependencyInjector
    registry: CommandRegistry

    def register(self, command: Command):
        self.registry[command.name] = command

        logging.info(f"registered command '{command.name}'")

    def get_func(self, command: str):
        inp = parse(command)

        command_seq = get_keyword_seq(inp)

        kwargs = get_kwargs(inp)

        func = self.__get_func(self.registry, command_seq)

        if func:
            self.di.set(KwargNodes, kwargs, teardown=None)

            return self.di.inject(func)

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

    async def execute(self, command: str):
        func = self.get_func(command)

        return await func()


def command(func: t.Callable[..., t.Any | None]) -> Command:
    return Command(func.__name__, func, {})


def name(
    _name: str,
) -> t.Callable[
    [t.Callable[..., t.Any | None]],
    t.Callable[..., t.Any | None],
]:
    def __wrapper__(func: t.Callable[..., t.Any | None]):
        func.__name__ = _name

        return func

    return __wrapper__
