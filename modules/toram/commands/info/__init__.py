import os

from modules.cmd.api import command
from yui.utils import load_toml


data = load_toml(os.path.dirname(__file__) + "/data.toml")


@command(name="info")
def info() -> str:
    return "no impl yet!"


@info.command(name="refpts")
def refine_points() -> str:
    return data["info"]["refine_pts"]["text"]


@info.command(name="summerevent")
def summer_event() -> str:
    return data["info"]["summer_event_guide_by_lies"]["text"]


@info.command(name="statcalc")
def stat_calc_sheet() -> str:
    return data["info"]["status_calculator_links"]["text"]


@info.command(name="bsprof")
def blacksmith_prof_leveling() -> str:
    return data["info"]["blacksmith_prof_leveling"]["text"]


@info.command(name="traitfarm")
def trait_farm_locations() -> str:
    return data["info"]["trait_farm_locations"]["text"]
