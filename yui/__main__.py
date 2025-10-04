import asyncio
import sys

from yui import Kernel


async def main():
    kernel = Kernel()

    await kernel.load_modules(
        [
            "modules.config",
            "modules.env",
            "modules.logging",
            "modules.lifecycle",
            "modules.cmd",
            "modules.shell",
            "modules.toram",
            "modules.facebook",
            "modules.run",
        ]
    )

    await kernel.unload_modules()


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
