from __future__ import annotations

import importlib
import os
from types import ModuleType

from typing import TYPE_CHECKING

from syclenv.logs import print_panel
from syclenv.plugins.PluginBase import implements

if TYPE_CHECKING:
    from syclenv.templates.TemplateBase import TemplateBase


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
    from syclenv.builtins.plugins.syclenv import SYCLEnvMainPlugin

    LOADED_PLUGINS.append(SYCLEnvMainPlugin())
    # plugins = ["syclenv.builtins.plugins.syclenv"] + plugins

    for p in plugins:
        try:
            print(f"Loading plugin : {p}")
            mod = get_plugin_module(p)
            LOADED_PLUGINS.append(mod.PLUGIN_CLASS())
        except ValueError as e:
            print_panel("Error", str(e), color="red")
            raise ValueError(f"Plugin {p} not found")


def run_on_template_list() -> dict[str, str]:
    templates: dict[str, str] = {}
    for p in LOADED_PLUGINS:
        if implements(p, "on_template_list"):
            templates = p.on_template_list(templates)
    return templates


def run_get_template_module(template_name: str) -> ModuleType:
    matches: list[tuple[str, ModuleType]] = []
    for p in LOADED_PLUGINS:
        if not implements(p, "on_get_template_module"):
            continue
        mod = p.on_get_template_module(template_name)
        if mod is not None:
            matches.append((p.name, mod))

    if not matches:
        raise ValueError(f"Template {template_name} not found")

    if len(matches) > 1:
        plugin_names = ", ".join(name for name, _ in matches)
        print_panel(
            "Warning",
            f"Multiple plugins resolved {template_name!r}: {plugin_names}. "
            f"Using {matches[-1][0]}.",
            color="yellow",
        )

    return matches[-1][1]


def run_get_template_class(template_name: str) -> type[TemplateBase]:
    from syclenv.templates.TemplateBase import TemplateBase

    mod = run_get_template_module(template_name)

    template_class = getattr(mod, "TEMPLATE_CLASS", None)
    if template_class is None:
        raise ValueError(
            f"Template module {template_name!r} is missing TEMPLATE_CLASS"
        )

    if not isinstance(template_class, type) or not issubclass(
        template_class, TemplateBase
    ):
        raise ValueError(
            f"TEMPLATE_CLASS in {template_name!r} must be a subclass of "
            f"TemplateBase, got {template_class!r}"
        )

    return template_class
