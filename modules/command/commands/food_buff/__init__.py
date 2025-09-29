import typing
import os


from modules.command.api import command, name
from yui.utils import load_toml


DATA_PATH = os.path.dirname(__file__) + "/data.toml"

data = load_toml(DATA_PATH)


def get_food_buff_codes(d: dict[str, typing.Any], key: str):
    return d["food_buffs"][key]["text"]


@command
def addr():
    return "no impl yet!"


@addr.command
def max_hp():
    return get_food_buff_codes(data, "max_hp")


@addr.command
def hp():
    return get_food_buff_codes(data, "max_hp")


@addr.command
def maxhp():
    return get_food_buff_codes(data, "max_hp")


@addr.command
def max_mp():
    return get_food_buff_codes(data, "max_mp")


@addr.command
def mp():
    return get_food_buff_codes(data, "max_mp")


@addr.command
def maxmp():
    return get_food_buff_codes(data, "max_mp")


@addr.command
@name("ampr")
def attack_mp_recovery():
    return get_food_buff_codes(data, "attack_mp_recovery")


@addr.command
@name("crit")
def critical_rate():
    return get_food_buff_codes(data, "critical_rate")


@addr.command
def accuracy():
    return get_food_buff_codes(data, "accuracy")


@addr.command
def acc():
    return get_food_buff_codes(data, "accuracy")


@addr.command
def dodge():
    return get_food_buff_codes(data, "dodge")


@addr.command
def agi():
    return get_food_buff_codes(data, "agi")


@addr.command
def dex():
    return get_food_buff_codes(data, "dex")


@addr.command
@name("int")
def _int():
    return get_food_buff_codes(data, "int")


@addr.command
def vit():
    return get_food_buff_codes(data, "vit")


@addr.command
@name("str")
def _str():
    return get_food_buff_codes(data, "str")


@addr.command
def atk():
    return get_food_buff_codes(data, "atk")


@addr.command
@name("watk")
def weapon_atk():
    return get_food_buff_codes(data, "weapon_atk")


@addr.command
def matk():
    return get_food_buff_codes(data, "matk")


@addr.command
@name("fbar")
def fractional_barrier():
    return get_food_buff_codes(data, "fractional_barrier")


@addr.command
@name("mbar")
def magic_barrier():
    return get_food_buff_codes(data, "magic_barrier")


@addr.command
@name("pbar")
def physical_barrier():
    return get_food_buff_codes(data, "physical_barrier")


@addr.command
@name("mres")
def magic_resistance():
    return get_food_buff_codes(data, "magic_resistance")


@addr.command
@name("pres")
def physical_resistance():
    return get_food_buff_codes(data, "physical_resistance")


@addr.command
@name("def")
def _def():
    return get_food_buff_codes(data, "def")


@addr.command
def mdef():
    return get_food_buff_codes(data, "mdef")


@addr.command
def aggro():
    return get_food_buff_codes(data, "aggro")


@addr.command
@name("-aggro")
def naggro():
    return get_food_buff_codes(data, "negative_aggro")


@addr.command
@name("dtedark")
def damage_to_dark():
    return get_food_buff_codes(data, "damage_to_dark")


@addr.command
@name("dteearth")
def damage_to_earth():
    return get_food_buff_codes(data, "damage_to_earth")


@addr.command
@name("dtelight")
def damage_to_light():
    return get_food_buff_codes(data, "damage_to_light")


@addr.command
@name("dtewater")
def damage_to_water():
    return get_food_buff_codes(data, "damage_to_water")


@addr.command
@name("dtewind")
def damage_to_wind():
    return get_food_buff_codes(data, "damage_to_wind")


@addr.command
@name("dtefire")
def damage_to_fire():
    return get_food_buff_codes(data, "damage_to_fire")


@addr.command
@name("dteneutral")
def damage_to_neutral():
    return get_food_buff_codes(data, "damage_to_neutral")


@addr.command
@name("darkres")
def dark_resistance():
    return get_food_buff_codes(data, "dark_resistance")


@addr.command
@name("earthres")
def earth_resistance():
    return get_food_buff_codes(data, "earth_resistance")


@addr.command
@name("fireres")
def fire_resistance():
    return get_food_buff_codes(data, "fire_resistance")


@addr.command
@name("lightres")
def light_resistance():
    return get_food_buff_codes(data, "light_resistance")


@addr.command
@name("windres")
def wind_resistance():
    return get_food_buff_codes(data, "wind_resistance")


@addr.command
@name("neutralres")
def neutral_resistance():
    return get_food_buff_codes(data, "neutral_resistance")


@addr.command
@name("waterres")
def water_resistance():
    return get_food_buff_codes(data, "water_resistance")


@addr.command
@name("droprate")
def drop_rate():
    return get_food_buff_codes(data, "drop_rate")


@addr.command
@name("expgain")
def exp_gain():
    return get_food_buff_codes(data, "exp_gain")


@addr.command
def help():
    return get_food_buff_codes(data, "help")
