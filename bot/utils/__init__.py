import tomllib
import typing


def load_toml(path: str) -> dict[str, typing.Any]:
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)

            return data

    except Exception as e:
        raise e
