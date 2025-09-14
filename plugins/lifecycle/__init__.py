from bot import Core
from bot.types import Plugin
from plugins.event import AsyncSignal


class LifeCyclePlugin(Plugin[Core]):
    async def on_run(self, core):
        event_manager = core.d.type_safe_get(AsyncSignal, "event_manager")

        if isinstance(event_manager, AsyncSignal):
            try:
                event_manager.value = "starting"
                await event_manager.notify()

                event_manager.value = "started"
                await event_manager.notify()

            except Exception as e:
                raise e

            finally:
                event_manager.value = "stopping"
                await event_manager.notify()

                event_manager.value = "stopped"
                await event_manager.notify()

        else:
            raise Exception("cannot get event_manager, is event plugin installed?")


__plugin__ = LifeCyclePlugin()
