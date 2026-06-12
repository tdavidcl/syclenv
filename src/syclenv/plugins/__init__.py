import importlib
from types import ModuleType

from syclenv.logs import print_panel


def get_plugin_module(plugin_name: str) -> ModuleType:
    module_name = f"{plugin_name}"
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise ValueError(f"Plugin {plugin_name} import failed ({module_name})") from exc


LOADED_PLUGINS = []


def load_plugins(plugins: list[str]):
    global LOADED_PLUGINS

    for p in plugins:
        try:
            mod = get_plugin_module(p)
            LOADED_PLUGINS.append(mod.PLUGIN_CLASS())
        except ValueError as e:
            print_panel("Error", str(e), color="red")
            raise ValueError(f"Plugin {p} not found")
