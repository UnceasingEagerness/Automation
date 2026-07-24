from pathlib import Path

import yaml


def load_yaml(path: str | Path):

    with open(path, "r") as file:

        return yaml.safe_load(file)