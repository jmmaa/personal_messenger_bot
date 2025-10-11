from yui.utils import load_env
from yui.kernel import Kernel


class Env(dict):
    def __repr__(self) -> str:
        return "I hide this sht cause it got some sensitive details :)"


def load(kernel: Kernel):
    kernel.store["__ENV__"] = Env(**load_env())


def unload(kernel: Kernel):
    del kernel.store["__ENV__"]
