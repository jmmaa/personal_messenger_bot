from dataclasses import dataclass
import typing
import dew


CommandInput = list[tuple[str, str]]

CommandCaller: typing.TypeAlias = typing.Callable[[CommandInput], str]


class SubCommandData(typing.TypedDict):
    func: CommandCaller | None

    sub_commands: dict[str, CommandCaller]


class CommandData(typing.TypedDict):
    func: CommandCaller | None

    sub_commands: dict[str, SubCommandData]


CommandRegistry: typing.TypeAlias = dict[str, CommandData]


@dataclass
class CommandClient:
    registry: CommandRegistry

    def execute(self, command: str):
        command_data = dew.parse(command)

        command_name = command_data["command_name"]

        sub_command_name = command_data["sub_command_name"]

        sub_command_group_name = command_data["sub_command_group_name"]

        kwargs = command_data["kwargs"]

        # CASE 1

        if (
            command_name is not None
            and sub_command_group_name is not None
            and sub_command_name is not None
        ):
            _1st_level_command_data = self.registry.get(command_name)

            if _1st_level_command_data is not None:
                _1st_level_command_sub_command_data = _1st_level_command_data.get(
                    "sub_commands"
                )

                _2nd_level_command_data = _1st_level_command_sub_command_data.get(
                    sub_command_group_name
                )

                if _2nd_level_command_data is not None:
                    _2nd_level_command_sub_command_data = _2nd_level_command_data.get(
                        "sub_commands"
                    )

                    _3rd_level_command_data = _2nd_level_command_sub_command_data.get(
                        sub_command_name
                    )

                    if _3rd_level_command_data is not None:
                        func = _3rd_level_command_data

                        return func(kwargs)

                    else:
                        raise Exception(
                            f"unknown command '{command_name} {sub_command_group_name} {sub_command_name}'"
                        )

                else:
                    raise Exception(
                        f"unknown command '{command_name} {sub_command_group_name}'"
                    )
            else:
                raise Exception(f"unknown command '{command_name}'")

        # CASE 2
        elif (
            command_name is not None
            and sub_command_group_name is None
            and sub_command_name is not None
        ):
            _1st_level_command_data = self.registry.get(command_name)

            if _1st_level_command_data is not None:
                _1st_level_command_sub_command_data = _1st_level_command_data.get(
                    "sub_commands"
                )

                _2nd_level_command_data = _1st_level_command_sub_command_data.get(
                    sub_command_name
                )

                if _2nd_level_command_data is not None:
                    func = _2nd_level_command_data.get("func")

                    if func is not None:
                        return func(kwargs)

                    else:
                        raise Exception(
                            f"no function defined for '{command_name} {sub_command_name}'"
                        )

                else:
                    raise Exception(
                        f"unknown command '{command_name} {sub_command_name}'"
                    )
            else:
                raise Exception(f"unknown command '{command_name}'")

        # CASE 3
        elif (
            command_name is not None
            and sub_command_group_name is None
            and sub_command_name is None
        ):
            _1st_level_command_data = self.registry.get(command_name)

            if _1st_level_command_data is not None:
                func = _1st_level_command_data.get("func")

                if func is not None:
                    return func(kwargs)

                else:
                    raise Exception(f"no function defined for command '{command_name}'")
            else:
                raise Exception(f"unknown command '{command_name}'")

        else:
            raise Exception(f"unknown command input '{command}'")
