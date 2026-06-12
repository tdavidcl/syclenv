import importlib
import os
from types import ModuleType

from syclenv.logs import print_panel
from syclenv.plugins.PluginBase import implements_template_list_hook


def get_plugin_module(plugin_name: str) -> ModuleType:
    module_name = f"{plugin_name}"
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise ValueError(f"Plugin {plugin_name} import failed ({module_name})") from exc


# Note that the order matter
LOADED_PLUGINS = []


def load_plugins():
    global LOADED_PLUGINS

    plugins = [
        p.strip() for p in os.environ.get("SYCLENV_PLUGINS", "").split(",") if p.strip()
    ]

    # Should be like this to avoid a print
    #LOADED_PLUGINS.append(SYCLEnvMainPlugin())
    plugins = ["syclenv.builtins.plugins.syclenv"] + plugins

    for p in plugins:
        try:
            print(f"Loading plugin : {p}")
            mod = get_plugin_module(p)
            LOADED_PLUGINS.append(mod.PLUGIN_CLASS())
        except ValueError as e:
            print_panel("Error", str(e), color="red")
            raise ValueError(f"Plugin {p} not found")


def run_plugin_hook_template_list(templates: dict[str, str]) -> dict[str, str]:
    for p in LOADED_PLUGINS:
        if implements_template_list_hook(p):
            templates = p.template_list_hook(templates)
    return templates
