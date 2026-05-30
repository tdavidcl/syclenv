import glob
import importlib
import os

from syclenv.templates.SetupArg import SetupArg

# Get current file path
cur_file = os.path.realpath(os.path.expanduser(__file__))

# Get env directory
env_dir = os.path.dirname(cur_file)


def get_template_module(template_name: str) -> importlib.ModuleType:
    # check that the template exists
    if not os.path.exists(os.path.join(env_dir, template_name, "setup.py")):
        raise ValueError(f"Template {template_name} not found")

    # Try to import the template
    try:
        return importlib.import_module("syclenv.templates." + template_name + ".setup")
    except ImportError:
        raise ValueError(f"Template {template_name} import failed")


def get_templates_list():
    list_machines = {}

    for i in glob.glob(env_dir + "/**/setup.py", recursive=True):
        path = os.path.relpath(i, env_dir).replace("/", ".").replace(".setup.py", "")
        mod = get_template_module(path)

        list_machines[path] = mod.NAME
    return list_machines


def setup_env(template_name: str, env_dir_path: str):
    mod = importlib.import_module("syclenv.templates." + template_name + ".setup")
    mod.setup(SetupArg(env_dir_path))
