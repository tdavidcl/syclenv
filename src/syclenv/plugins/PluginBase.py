from typing import Protocol


class PluginBase(Protocol):
    name: str
    description: str

    def check_prerequisites(self, template) -> tuple[bool, str]: ...

    def install_prerequisites(self, template) -> None: ...

    def before_create_env(self, template) -> None: ...

    def after_create_env(self, template) -> None: ...

    def template_list_hook(self, original: dict[str, str]) -> dict[str, str]: ...


def implements_before_create_env(plugin):
    return plugin.__class__.before_create_env is not PluginBase.before_create_env


def implements_after_create_env(plugin):
    return plugin.__class__.after_create_env is not PluginBase.after_create_env


def implements_template_list_hook(plugin):
    return plugin.__class__.template_list_hook is not PluginBase.template_list_hook
