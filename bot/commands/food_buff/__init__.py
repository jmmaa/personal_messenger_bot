from bot.commands import CommandInput
from bot.utils import load_config


def food_buff_command(kwargs: CommandInput) -> str:
    key, value = kwargs.pop(0)

    if key.lower() == "stat":
        config_path = "./food_buff_data.toml"

        try:
            data = load_config(config_path)

        except Exception as e:
            raise e

        match value.lower():
            case "maxhp" | "hp" | "max hp":
                key = "max_hp"

            case "maxmp" | "mp" | "max mp":
                key = "max_mp"

            case "ampr":
                key = "attack_mp_recovery"

            case "crit" | "critrate" | "critical rate" | "crate" | "crit rate":
                key = "critical_rate"

            case "acc" | "accuracy":
                key = "accuracy"

            case "dodge":
                key = "dodge"

            case "agi":
                key = "agi"

            case "dex":
                key = "dex"

            case "int":
                key = "int"

            case "vit":
                key = "vit"

            case "str":
                key = "str"

            case "atk" | "attack":
                key = "atk"

            case "watk" | "weaponatk" | "weapon atk":
                key = "weapon_atk"

            case "matk":
                key = "matk"

            case "fractional barrier" | "fbar" | "fbarrier":
                key = "fractional_barrier"

            case "magic barrier" | "mbar" | "mbarrier":
                key = "magic_barrier"

            case "physical barrier" | "pbar" | "pbarrier":
                key = "physical_barrier"

            case "magic resistance" | "mres" | "mresist":
                key = "magic_resistance"

            case "physical resistance" | "pres" | "presist":
                key = "physical_resistance"

            case "def":
                key = "def"

            case "mdef":
                key = "mdef"

            case "+aggro" | "+agg" | "aggro" | "agg":
                key = "aggro"

            case "-aggro" | "-agg":
                key = "negative_aggro"

            case "dtedark" | "dtdark" | "dte dark":
                key = "damage_to_dark"

            case "dteearth" | "dtearth" | "dte earth":
                key = "damage_to_earth"

            case "dtelight" | "dtlight" | "dte light":
                key = "damage_to_light"

            case "dtewater" | "dtwater" | "dte water":
                key = "damage_to_water"

            case "dtewind" | "dtwind" | "dte wind":
                key = "damage_to_wind"

            case "dtefire" | "dtfire" | "dte fire":
                key = "damage_to_fire"

            case "dteneutral" | "dtneutral" | "dte neutral" | "dteneut" | "dte neut":
                key = "damage_to_neutral"

            case "rtedark" | "rtdark" | "rte dark" | "darkres" | "darkresist":
                key = "dark_resistance"

            case "rteearth" | "rtearth" | "rte earth" | "earthres" | "earthresist":
                key = "earth_resistance"

            case "rtefire" | "rtfire" | "rte fire" | "fireres" | "fireresist":
                key = "fire_resistance"

            case "rtelight" | "rtlight" | "rte light" | "lightres" | "lightresist":
                key = "light_resistance"

            case "rtewind" | "rtwind" | "rte wind" | "windres" | "windresist":
                key = "wind_resistance"

            case (
                "rteneutral"
                | "rtneutral"
                | "rte neutral"
                | "neutralres"
                | "neutralresist"
                | "neutres"
                | "neutresist"
            ):
                key = "neutral_resistance"

            case "rtewater" | "rtwater" | "rte water" | "waterres" | "waterresist":
                key = "water_resistance"

            case "drop" | "droprate" | "drop rate":
                key = "drop_rate"

            case "exp" | "expgain" | "exp gain":
                key = "exp_gain"

            case "":
                return "mali"

            case _:
                return "mali"

        try:
            res = data["food_buffs"][key]["text"]
            return res

        except Exception as e:
            raise e

    else:
        raise Exception("need keyword 'stat' to know which buff to get")
