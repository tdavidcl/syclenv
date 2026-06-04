from importlib.resources import files
from os.path import dirname

SPACER = "\n###########################################################################"


def fetch_helper_script(path: str) -> str:
    with open(path) as f:
        helper_script = ""
        helper_script += f"\n{SPACER}\n# Imported script {path}{SPACER}\n"
        helper_script += f.read()
        helper_script += f"{SPACER}{SPACER}{SPACER}\n\n"

        return helper_script


HELPER_SCRIPTS_DIR = dirname(files(__package__))
