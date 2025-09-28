import asyncio
import sys

from yui.kernel import Kernel


async def main():
    kernel = Kernel()

    await kernel.load_modules(
        [
            "modules.config",
            "modules.env",
            "modules.logging",
            "modules.lifecycle",
            "modules.command_parser",
            "modules.command",
            # "modules.shell",
            "modules.facebook",
            "modules.run",
        ]
    )

    await kernel.unload_modules()


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
