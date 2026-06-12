from syclenv.plugins.PluginBase import PluginBase
from syclenv.templates import get_native_templates_list


class SYCLEnvMainPlugin(PluginBase):
    name = "SYCLenv main plugin"
    description = "main plugin for SYCL env. Internally it is a plugin like everyone"

    def __init__(self):
        ...

    def check_prerequisites(self, template) -> tuple[bool, str]:
        ...
        return True, " "

    def install_prerequisites(self, template) -> None:
        ...

    def before_create_env(self, template) -> None:
        ...

    def after_create_env(self, template) -> None:
        ...

    def template_list_hook(self, original: dict[str, str]) -> dict[str, str]:
        return get_native_templates_list()


PLUGIN_CLASS = SYCLEnvMainPlugin
