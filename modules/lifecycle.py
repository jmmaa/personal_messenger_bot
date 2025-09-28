from dataclasses import dataclass
import logging

from yui.kernel import Kernel


logger = logging.getLogger("yui")


@dataclass
class StartEvent:
    kernel: Kernel


@dataclass
class StartedEvent:
    kernel: Kernel


@dataclass
class StartingEvent:
    kernel: Kernel


@dataclass
class StoppingEvent:
    kernel: Kernel


@dataclass
class StoppedEvent:
    kernel: Kernel


@dataclass
class StopEvent:
    kernel: Kernel


async def start_lifecycle(event: StartEvent):
    await event.kernel.event_manager.emit(StartingEvent(event.kernel))
    await event.kernel.event_manager.emit(StartedEvent(event.kernel))


async def stop_lifecycle(event: StopEvent):
    await event.kernel.event_manager.emit(StoppingEvent(event.kernel))
    await event.kernel.event_manager.emit(StoppedEvent(event.kernel))


def load(kernel: Kernel):
    kernel.event_manager.add_event(StartEvent)
    kernel.event_manager.add_event(StartingEvent)
    kernel.event_manager.add_event(StartedEvent)
    kernel.event_manager.add_event(StoppingEvent)
    kernel.event_manager.add_event(StoppedEvent)
    kernel.event_manager.add_event(StopEvent)

    kernel.event_manager.subscribe(StartEvent, start_lifecycle)
    kernel.event_manager.subscribe(StopEvent, stop_lifecycle)


def unload(kernel: Kernel):
    kernel.event_manager.unsubscribe(StartEvent, start_lifecycle)
    kernel.event_manager.unsubscribe(StopEvent, stop_lifecycle)

    kernel.event_manager.remove_event(StartEvent)
    kernel.event_manager.remove_event(StartingEvent)
    kernel.event_manager.remove_event(StartedEvent)
    kernel.event_manager.remove_event(StoppingEvent)
    kernel.event_manager.remove_event(StoppedEvent)
    kernel.event_manager.remove_event(StopEvent)
