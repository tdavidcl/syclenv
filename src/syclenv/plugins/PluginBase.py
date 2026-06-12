from typing import Protocol

"""
A plugin is a general list of hook that will be applied on the corresponding step.
It is not bound to the execution of a specific template but to syclenv as a whole
"""


class PluginBase(Protocol):
    name: str
    description: str

    def template_list_hook(self, original: dict[str, str]) -> dict[str, str]:
        """
        Intercept the generation of the template list
        """
        ...

    def check_prerequisites(self, template) -> tuple[bool, str]: ...

    def install_prerequisites(self, template) -> None: ...

    def before_create_env(self, template) -> None: ...

    def after_create_env(self, template) -> None: ...


def implements_before_create_env(plugin):
    return plugin.__class__.before_create_env is not PluginBase.before_create_env


def implements_after_create_env(plugin):
    return plugin.__class__.after_create_env is not PluginBase.after_create_env


def implements_template_list_hook(plugin):
    return plugin.__class__.template_list_hook is not PluginBase.template_list_hook
