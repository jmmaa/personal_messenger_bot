import asyncio
import sys

from yui import Kernel


async def main():
    kernel = Kernel()

    kernel.add_modules_from_packages(
        [
            "yui.modules.config",
            "yui.modules.env",
            "yui.modules.logging",
            "yui.modules.lifecycle",
            "yui.modules.cmd",
            # "yui.modules.shell",
            # "modules.toram",
            # "modules.facebook",
        ]
    )

    await kernel.boot()

    # this api is only available if you have 'yui.modules.lifecycle' module added
    # starts the program
    await kernel.emit("kernel:lifecycle:start", kernel)

    # stops the program
    await kernel.emit("kernel:lifecycle:stop", kernel)

    await kernel.shutdown()


if __name__ == "__main__":
    if sys.platform.startswith("win"):  # this is needed to run fbchat
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
