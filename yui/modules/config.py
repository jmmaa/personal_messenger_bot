from __future__ import annotations

import typing as t

from yui.utils import load_toml
from yui.kernel import Kernel


def load(kernel: Kernel):
    try:
        config = load_toml("./yui.toml")

    except Exception:
        config = {}

    kernel.store["__CONFIG__"] = config


def unload(kernel: Kernel):
    del kernel.store["__CONFIG__"]
