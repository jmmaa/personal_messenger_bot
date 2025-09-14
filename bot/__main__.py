import asyncio
import logging
import sys

from bot import Core, load_plugin_spec, load_plugin_specs
from plugins.config import Config


async def main():
    bot = Core()

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
            "plugins.dew",
            "plugins.command",
            "plugins.toram",
            "plugins.cli",
            "plugins.facebook",
        ]
    )

    for plugin in plugins:
        bot.add_plugin(plugin)

    await bot.start()


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
