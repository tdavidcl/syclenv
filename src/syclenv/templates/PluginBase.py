from typing import Protocol


class PluginBase(Protocol):
    name: str
    description: str

    def check_prerequisites(self, template) -> tuple[bool, str]: ...

    def install_prerequisites(self, template) -> None: ...

    def before_create_env(self, template) -> None: ...

    def after_create_env(self, template) -> None: ...
