import typing
import os

from bot.commands import command, name
from bot.utils import load_toml


DATA_PATH = os.path.dirname(__file__) + "/data.toml"

data = load_toml(DATA_PATH)


def get_food_buff_codes(d: dict[str, typing.Any], key: str):
    return d["food_buffs"][key]["text"]


@command
def addr(_) -> str:
    return "no impl yet!"


@addr.command
def max_hp(_):
    return get_food_buff_codes(data, "max_hp")


@addr.command
def max_mp(_):
    return get_food_buff_codes(data, "max_mp")


@addr.command
def attack_mp_recovery(_):
    return get_food_buff_codes(data, "attack_mp_recovery")


@addr.command
def critical_rate(_):
    return get_food_buff_codes(data, "critical_rate")


@addr.command
def accuracy(_):
    return get_food_buff_codes(data, "accuracy")


@addr.command
def dodge(_):
    return get_food_buff_codes(data, "dodge")


@addr.command
def agi(_):
    return get_food_buff_codes(data, "agi")


@addr.command
def dex(_):
    return get_food_buff_codes(data, "dex")


@addr.command
@name("int")
def _int(_):
    return get_food_buff_codes(data, "int")


@addr.command
def vit(_):
    return get_food_buff_codes(data, "vit")


@addr.command
@name("str")
def _str(_):
    return get_food_buff_codes(data, "str")


@addr.command
def atk(_):
    return get_food_buff_codes(data, "atk")


@addr.command
@name("watk")
def weapon_atk(_):
    return get_food_buff_codes(data, "weapon_atk")


@addr.command
def matk(_):
    return get_food_buff_codes(data, "matk")


@addr.command
@name("fbar")
def fractional_barrier(_):
    return get_food_buff_codes(data, "fractional_barrier")


@addr.command
@name("mbar")
def magic_barrier(_):
    return get_food_buff_codes(data, "magic_barrier")


@addr.command
@name("pbar")
def physical_barrier(_):
    return get_food_buff_codes(data, "physical_barrier")


@addr.command
@name("mres")
def magic_resistance(_):
    return get_food_buff_codes(data, "magic_resistance")


@addr.command
@name("pres")
def physical_resistance(_):
    return get_food_buff_codes(data, "physical_resistance")


@addr.command
@name("def")
def _def(_):
    return get_food_buff_codes(data, "def")


@addr.command
def mdef(_):
    return get_food_buff_codes(data, "mdef")


@addr.command
def aggro(_):
    return get_food_buff_codes(data, "aggro")


@addr.command
def negative_aggro(_):
    return get_food_buff_codes(data, "negative_aggro")


@addr.command
@name("dtedark")
def damage_to_dark(_):
    return get_food_buff_codes(data, "damage_to_dark")


@addr.command
@name("dteearth")
def damage_to_earth(_):
    return get_food_buff_codes(data, "damage_to_earth")


@addr.command
@name("dtelight")
def damage_to_light(_):
    return get_food_buff_codes(data, "damage_to_light")


@addr.command
@name("dtewater")
def damage_to_water(_):
    return get_food_buff_codes(data, "damage_to_water")


@addr.command
@name("dtewind")
def damage_to_wind(_):
    return get_food_buff_codes(data, "damage_to_wind")


@addr.command
@name("dtefire")
def damage_to_fire(_):
    return get_food_buff_codes(data, "damage_to_fire")


@addr.command
@name("dteneutral")
def damage_to_neutral(_):
    return get_food_buff_codes(data, "damage_to_neutral")


@addr.command
@name("darkres")
def dark_resistance(_):
    return get_food_buff_codes(data, "dark_resistance")


@addr.command
@name("earthres")
def earth_resistance(_):
    return get_food_buff_codes(data, "earth_resistance")


@addr.command
@name("fireres")
def fire_resistance(_):
    return get_food_buff_codes(data, "fire_resistance")


@addr.command
@name("lightres")
def light_resistance(_):
    return get_food_buff_codes(data, "light_resistance")


@addr.command
@name("windres")
def wind_resistance(_):
    return get_food_buff_codes(data, "wind_resistance")


@addr.command
@name("neutralres")
def neutral_resistance(_):
    return get_food_buff_codes(data, "neutral_resistance")


@addr.command
@name("waterres")
def water_resistance(_):
    return get_food_buff_codes(data, "water_resistance")


@addr.command
@name("droprate")
def drop_rate(_):
    return get_food_buff_codes(data, "drop_rate")


@addr.command
@name("expgain")
def exp_gain(_):
    return get_food_buff_codes(data, "exp_gain")


@addr.command
def help(_):
    return data[""]
