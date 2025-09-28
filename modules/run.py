from yui import Kernel
from modules.lifecycle import StartEvent, StopEvent


async def load(kernel: Kernel):
    await kernel.event_manager.emit(StartEvent(kernel))


async def unload(kernel: Kernel):
    await kernel.event_manager.emit(StopEvent(kernel))
