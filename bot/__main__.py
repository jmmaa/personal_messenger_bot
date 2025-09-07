import asyncio
import logging

from bot import Bot, load_plugin_spec, load_plugin_specs
from plugins.config import Config


async def main():
    bot = Bot()

    # default plugin
    bot.add_plugin(load_plugin_spec("plugins.config"))

    config: Config | None = bot.d.get("config")

    if config:
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(config.bot.logging.file),
                logging.StreamHandler(),
            ],
            force=True,
        )

        logging.getLogger().setLevel(logging._nameToLevel[config.bot.logging.level])

    plugins = load_plugin_specs(
        [
            "plugins.env",
            "plugins.db",
            "plugins.toram",
            "plugins.dew_parser",
            "plugins.command",
        ]
    )

    for plugin in plugins:
        bot.add_plugin(plugin)

    await bot.load_plugins()

    if config:
        if config.bot.shell_mode:
            if config.bot.shell_mode:
                try:
                    while True:
                        inp = input()

                        if inp.startswith(config.bot.prefix):
                            result = await bot.execute(inp[1:])

                            print(result)

                except Exception as e:
                    await bot.unload_plugins()

                    raise e


if __name__ == "__main__":
    asyncio.run(main())
