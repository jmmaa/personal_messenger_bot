import logging

from bot import Core
from bot.types import Plugin
from plugins.command.api import CommandClient
from plugins.config import Config


class CliPlugin(Plugin[Core]):
    async def on_run(self, core):
        config: Config = core.d["config"]

        command_client: CommandClient = core.d["command_client"]
        command_parser = core.d["dew"]

        if config:
            if config.bot.shell_mode:
                try:
                    while True:
                        inp = input()

                        if inp.startswith(config.bot.prefix):
                            logging.debug(f"received command: {inp}")
                            node = command_parser.parse(inp[1:])
                            logging.debug(f"parsed command: {node}")
                            result = await command_client.execute(node)

                            print(result)

                except Exception as e:
                    logging.debug(e)
                    await core.stop()


__plugin__ = CliPlugin()
