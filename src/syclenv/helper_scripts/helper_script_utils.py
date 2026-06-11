from importlib.resources import files
from importlib.resources.abc import Traversable

SPACER = "\n###########################################################################"


def fetch_helper_script(path: Traversable) -> str:
    with path.open() as f:
        helper_script = ""
        helper_script += f"\n{SPACER}\n# Imported script {path.name}{SPACER}\n"
        helper_script += f.read()
        helper_script += f"{SPACER}{SPACER}{SPACER}\n\n"

        return helper_script


HELPER_SCRIPTS_DIR = files(__package__)
