import typing as t
import os


from modules.cmd.api import command, CommandTree
from yui.kernel import Kernel
from yui.utils import load_toml


DATA_PATH = os.path.dirname(__file__) + "/data.toml"

data = load_toml(DATA_PATH)


def get_food_buff_codes(d: dict[str, t.Any], key: str):
    return d["food_buffs"][key]["text"]


FoodBuffData = t.NewType("FoodBuffData", dict)


@command(name="addr")
def addr(kernel: Kernel):
    root = t.cast(CommandTree, kernel.cache["__LEGACY_CMD_API__"])

    addr_tree = root.get_tree([">", "addr"])
    addr_child_trees = addr_tree.get_trees()
    addr_child_trees_sequences = [tree.get_command_sequence()[1:] for tree in addr_child_trees]
    command_names = [">" + " ".join([seq.data.name for seq in sequence]) for sequence in addr_child_trees_sequences]

    return "\n".join(command_names)


@addr.command(name="max_hp")
def max_hp():
    return get_food_buff_codes(data, "max_hp")


@addr.command(name="hp")
def hp():
    return get_food_buff_codes(data, "max_hp")


@addr.command(name="maxhp")
def maxhp():
    return get_food_buff_codes(data, "max_hp")


@addr.command(name="max_mp")
def max_mp():
    return get_food_buff_codes(data, "max_mp")


@addr.command(name="mp")
def mp():
    return get_food_buff_codes(data, "max_mp")


@addr.command(name="maxmp")
def maxmp():
    return get_food_buff_codes(data, "max_mp")


@addr.command(name="ampr")
def attack_mp_recovery():
    return get_food_buff_codes(data, "attack_mp_recovery")


@addr.command(name="critical_rate")
def critical_rate():
    return get_food_buff_codes(data, "critical_rate")


@addr.command(name="crit")
def crit():
    return get_food_buff_codes(data, "critical_rate")


@addr.command(name="accuracy")
def accuracy():
    return get_food_buff_codes(data, "accuracy")


@addr.command(name="acc")
def acc():
    return get_food_buff_codes(data, "accuracy")


@addr.command(name="dodge")
def dodge():
    return get_food_buff_codes(data, "dodge")


@addr.command(name="agi")
def agi():
    return get_food_buff_codes(data, "agi")


@addr.command(name="dex")
def dex():
    return get_food_buff_codes(data, "dex")


@addr.command(name="int")
def _int():
    return get_food_buff_codes(data, "int")


@addr.command(name="vit")
def vit():
    return get_food_buff_codes(data, "vit")


@addr.command(name="str")
def _str():
    return get_food_buff_codes(data, "str")


@addr.command(name="atk")
def atk():
    return get_food_buff_codes(data, "atk")


@addr.command(name="weapon_atk")
def weapon_atk():
    return get_food_buff_codes(data, "weapon_atk")


@addr.command(name="watk")
def watk():
    return get_food_buff_codes(data, "weapon_atk")


@addr.command(name="matk")
def matk():
    return get_food_buff_codes(data, "matk")


@addr.command(name="fractional_barrier")
def fractional_barrier():
    return get_food_buff_codes(data, "fractional_barrier")


@addr.command(name="fbar")
def fbar():
    return get_food_buff_codes(data, "fractional_barrier")


@addr.command(name="magic_barrier")
def magic_barrier():
    return get_food_buff_codes(data, "magic_barrier")


@addr.command(name="mbar")
def mbar():
    return get_food_buff_codes(data, "magic_barrier")


@addr.command(name="physical_barrier")
def physical_barrier():
    return get_food_buff_codes(data, "physical_barrier")


@addr.command(name="pbar")
def pbar():
    return get_food_buff_codes(data, "physical_barrier")


@addr.command(name="magic_resistance")
def magic_resistance():
    return get_food_buff_codes(data, "magic_resistance")


@addr.command(name="mres")
def mres():
    return get_food_buff_codes(data, "magic_resistance")


@addr.command(name="physical_resistance")
def physical_resistance():
    return get_food_buff_codes(data, "physical_resistance")


@addr.command(name="pres")
def pres():
    return get_food_buff_codes(data, "physical_resistance")


@addr.command(name="def")
def _def():
    return get_food_buff_codes(data, "def")


@addr.command(name="mdef")
def mdef():
    return get_food_buff_codes(data, "mdef")


@addr.command(name="aggro")
def aggro():
    return get_food_buff_codes(data, "aggro")


@addr.command(name="-aggro")
def negative_aggro():
    return get_food_buff_codes(data, "negative_aggro")


@addr.command(name="damage_to_dark")
def damage_to_dark():
    return get_food_buff_codes(data, "damage_to_dark")


@addr.command(name="dtedark")
def dtedark():
    return get_food_buff_codes(data, "damage_to_dark")


@addr.command(name="damage_to_earth")
def damage_to_earth():
    return get_food_buff_codes(data, "damage_to_earth")


@addr.command(name="dteearth")
def dteearth():
    return get_food_buff_codes(data, "damage_to_earth")


@addr.command(name="damage_to_light")
def damage_to_light():
    return get_food_buff_codes(data, "damage_to_light")


@addr.command(name="dtelight")
def dtelight():
    return get_food_buff_codes(data, "damage_to_light")


@addr.command(name="damage_to_water")
def damage_to_water():
    return get_food_buff_codes(data, "damage_to_water")


@addr.command(name="dtewater")
def dtewater():
    return get_food_buff_codes(data, "damage_to_water")


@addr.command(name="damage_to_wind")
def damage_to_wind():
    return get_food_buff_codes(data, "damage_to_wind")


@addr.command(name="dtewind")
def dtewind():
    return get_food_buff_codes(data, "damage_to_wind")


@addr.command(name="damage_to_fire")
def damage_to_fire():
    return get_food_buff_codes(data, "damage_to_fire")


@addr.command(name="dtefire")
def dtefire():
    return get_food_buff_codes(data, "damage_to_fire")


@addr.command(name="damage_to_neutral")
def damage_to_neutral():
    return get_food_buff_codes(data, "damage_to_neutral")


@addr.command(name="dteneutral")
def dteneutral():
    return get_food_buff_codes(data, "damage_to_neutral")


@addr.command(name="dark_resistance")
def dark_resistance():
    return get_food_buff_codes(data, "dark_resistance")


@addr.command(name="darkres")
def darkres():
    return get_food_buff_codes(data, "dark_resistance")


@addr.command(name="earth_resistance")
def earth_resistance():
    return get_food_buff_codes(data, "earth_resistance")


@addr.command(name="earthres")
def earthres():
    return get_food_buff_codes(data, "earth_resistance")


@addr.command(name="fire_resistance")
def fire_resistance():
    return get_food_buff_codes(data, "fire_resistance")


@addr.command(name="fireres")
def fireres():
    return get_food_buff_codes(data, "fire_resistance")


@addr.command(name="light_resistance")
def light_resistance():
    return get_food_buff_codes(data, "light_resistance")


@addr.command(name="lightres")
def lightres():
    return get_food_buff_codes(data, "light_resistance")


@addr.command(name="wind_resistance")
def wind_resistance():
    return get_food_buff_codes(data, "wind_resistance")


@addr.command(name="windres")
def windres():
    return get_food_buff_codes(data, "wind_resistance")


@addr.command(name="neutral_resistance")
def neutral_resistance():
    return get_food_buff_codes(data, "neutral_resistance")


@addr.command(name="neutralres")
def neutralres():
    return get_food_buff_codes(data, "neutral_resistance")


@addr.command(name="water_resistance")
def water_resistance():
    return get_food_buff_codes(data, "water_resistance")


@addr.command(name="waterres")
def waterres():
    return get_food_buff_codes(data, "water_resistance")


@addr.command(name="drop_rate")
def drop_rate():
    return get_food_buff_codes(data, "drop_rate")


@addr.command(name="drop")
def drop():
    return get_food_buff_codes(data, "drop_rate")


@addr.command(name="exp_gain")
def exp_gain():
    return get_food_buff_codes(data, "exp_gain")


@addr.command(name="exp")
def exp():
    return get_food_buff_codes(data, "exp_gain")


@addr.command(name="help")
def help():
    return get_food_buff_codes(data, "help")
