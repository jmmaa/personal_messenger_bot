from __future__ import annotations

from dataclasses import dataclass
import typing
import dew
from dew import Command, Kwarg

CommandInput = list[tuple[str, str]]

CommandCaller: typing.TypeAlias = typing.Callable[[CommandInput], str]


@dataclass
class CommandData:
    name: str
    func: typing.Callable[[list[tuple[str, str]]], str]
    tail: dict[str, CommandData]

    def command(self, func: typing.Callable[[list[tuple[str, str]]], str]):
        self.tail[func.__name__] = CommandData(func.__name__, func, {})

        return self.tail[func.__name__]

    def register(self, command: CommandData):
        self.tail[command.name] = command


CommandRegistry: typing.TypeAlias = dict[str, CommandData]


def name(
    _name: str,
) -> typing.Callable[
    [typing.Callable[[list[tuple[str, str]]], str]],
    typing.Callable[[list[tuple[str, str]]], str],
]:
    def __wrapper__(func: typing.Callable[[list[tuple[str, str]]], str]):
        func.__name__ = _name

        return func

    return __wrapper__


def command(func: typing.Callable[[list[tuple[str, str]]], str]) -> CommandData:
    """
    A helper function to turn a function declaration into a `CommandData`

    helpful for grouping commands

    ```python

    @command
    def hello(_) -> str:
        return "hello there!"

    @hello.command
    def sub_hello1(_) -> str:
        return "hello from sub!"

    @hello.command
    def sub_hello2(_) -> str:
        return "hello from sub!"

    client = CommandClient({})

    client.register(hello)

    ```
    """
    return CommandData(func.__name__, func, {})


@dataclass
class CommandClient:
    registry: CommandRegistry

    def get_result(self, cmd_data: CommandRegistry, cmd_inp: Command) -> str:
        new_cmd_inp = cmd_inp
        new_cmd_data = cmd_data.get(new_cmd_inp["name"])

        if new_cmd_data is not None:
            tail = new_cmd_inp["tail"]

            if isinstance(tail, dict):
                return self.__get_result_recursive(
                    new_cmd_inp["name"], new_cmd_data.tail, new_cmd_inp["tail"]
                )

            else:
                if new_cmd_data is not None:
                    func = new_cmd_data.func

                    if func is not None:
                        return func(tail)

                    else:
                        raise Exception(
                            f"function implementation not found for '{new_cmd_inp['name']}'"
                        )

                else:
                    raise Exception(f"could not find '{new_cmd_inp['name']} command'")

        raise Exception(f"could not find '{new_cmd_inp['name']}' command")

    def __get_result_recursive(
        self,
        prev_cmd_name: str,
        cmd_data: CommandRegistry,
        cmd_inp: Command | list[Kwarg],
    ):
        if isinstance(cmd_inp, dict):
            new_cmd_inp = cmd_inp

            new_cmd_data = cmd_data.get(new_cmd_inp["name"])

            if new_cmd_data is not None:
                new_cmd_inp_tail = new_cmd_inp["tail"]

                if isinstance(new_cmd_inp_tail, list):
                    func = new_cmd_data.func

                    if func is not None:
                        return func(new_cmd_inp_tail)

                    else:
                        raise Exception(
                            f"function implementation not found for '{new_cmd_inp['name']}'"
                        )
                else:
                    return self.__get_result_recursive(
                        new_cmd_inp_tail["name"],
                        new_cmd_data.tail,
                        new_cmd_inp["tail"],
                    )

            raise Exception(f"could not find '{new_cmd_inp['name']}' command")

        else:
            new_cmd_inp = cmd_inp

            new_cmd_data = cmd_data.get(prev_cmd_name)

            if new_cmd_data is not None:
                func = new_cmd_data.func

                if func is not None:
                    return func(new_cmd_inp)

                else:
                    raise Exception(
                        f"function implementation not found for '{prev_cmd_name}'"
                    )

            else:
                raise Exception(f"could not find '{prev_cmd_name} command'")

    def execute(self, command: str):
        inp = dew.parse(command)

        return self.get_result(self.registry, inp)

    def command(self, func: typing.Callable[[list[tuple[str, str]]], str]):
        self.registry[func.__name__] = CommandData(func.__name__, func, {})

        return self.registry[func.__name__]

    def register(self, command: CommandData):
        self.registry[command.name] = command


# client = CommandClient({})


# @client.command
# def my_command(kwargs: list[tuple[str, str]]) -> str:
#     return "my command here"


# @my_command.command
# def my_sub_command1(kwargs: list[tuple[str, str]]) -> str:
#     return "my sub command here"


# @my_command.command
# def my_sub_command2(kwargs: list[tuple[str, str]]) -> str:
#     return "my sub command here"


# def my_sub_command3(kwargs: list[tuple[str, str]]) -> str:
#     return "my sub command here 3"


# my_command.command(my_sub_command3)


# @my_sub_command1.command
# def my_sub_sub_command1(kwargs: list[tuple[str, str]]) -> str:
#     return "\n".join(f"{e[0]}:{e[1]}" for e in kwargs)


# print(
#     client.execute(
#         "my_command my_sub_command1 my_sub_sub_command1 stat:INT stat:DEX stat:STR"
#     )
# )
