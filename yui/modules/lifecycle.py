import logging

from yui.kernel import Kernel


logger = logging.getLogger("yui")


async def start_lifecycle(kernel: Kernel):
    await kernel.emit("kernel:lifecycle:starting", kernel)
    await kernel.emit("kernel:lifecycle:started", kernel)


async def stop_lifecycle(kernel: Kernel):
    await kernel.emit("kernel:lifecycle:stopping", kernel)
    await kernel.emit("kernel:lifecycle:stopped", kernel)


def load(kernel: Kernel):
    kernel.add_hook("kernel:lifecycle:start")
    kernel.add_hook("kernel:lifecycle:starting")
    kernel.add_hook("kernel:lifecycle:started")
    kernel.add_hook("kernel:lifecycle:stopping")
    kernel.add_hook("kernel:lifecycle:stopped")
    kernel.add_hook("kernel:lifecycle:stop")

    kernel.sub("kernel:lifecycle:start", start_lifecycle)
    kernel.sub("kernel:lifecycle:stop", stop_lifecycle)


def unload(kernel: Kernel):
    kernel.unsub("kernel:lifecycle:start", start_lifecycle)
    kernel.unsub("kernel:lifecycle:stop", stop_lifecycle)

    kernel.remove_hook("kernel:lifecycle:start")
    kernel.remove_hook("kernel:lifecycle:starting")
    kernel.remove_hook("kernel:lifecycle:started")
    kernel.remove_hook("kernel:lifecycle:stopping")
    kernel.remove_hook("kernel:lifecycle:stopped")
    kernel.remove_hook("kernel:lifecycle:stop")
