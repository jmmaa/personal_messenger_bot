import os

from bot.commands import command, name
from bot.utils import load_toml


data = load_toml(os.path.dirname(__file__) + "/data.toml")


@command
def info(_) -> str:
    return "no impl yet!"


@info.command
@name("refinepoints")
def refine_points(_) -> str:
    return data["info"]["refine_pts"]["text"]


@info.command
@name("summerevent")
def summer_event(_) -> str:
    return data["info"]["summer_event_guide_by_lies"]["text"]


@info.command
@name("statcalc")
def stat_calc_sheet(_) -> str:
    return data["info"]["status_calculator_links"]["text"]


@info.command
@name("bsprof")
def blacksmith_prof_leveling(_) -> str:
    return data["info"]["blacksmith_prof_leveling"]["text"]
