from syclenv.plugins.PluginBase import PluginBase
from syclenv.templates import TEMPLATES_DIR, get_template_module


class SYCLEnvMainPlugin(PluginBase):
    name = "SYCLenv main plugin"
    description = "main plugin for SYCL env. Internally it is a plugin like everyone"

    def on_template_list(self, original: dict[str, str]) -> dict[str, str]:
        # original should be empty this plugin must be first
        # because we will ignore its content
        if original:
            raise ValueError("SYCLEnvMainPlugin must be first in the plugin list")

        templates: dict[str, str] = {}
        for setup_py in TEMPLATES_DIR.glob("**/setup.py"):
            template_name = ".".join(setup_py.relative_to(TEMPLATES_DIR).parts[:-1])
            mod = get_template_module(template_name)
            templates[template_name] = mod.TEMPLATE_CLASS.name
        return templates


PLUGIN_CLASS = SYCLEnvMainPlugin
