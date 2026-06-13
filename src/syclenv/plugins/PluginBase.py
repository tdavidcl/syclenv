from abc import ABC
from types import ModuleType

# Plugins expose optional on_* event hooks invoked by syclenv at lifecycle points.
# Hooks are not bound to a specific template; the core itself is also a plugin.


class PluginBase(ABC):
    name: str
    description: str

    def on_template_list(self, original: dict[str, str]) -> dict[str, str]:
        """Called when building the template list."""
        return original

    def on_get_template_module(self, template_name: str) -> ModuleType | None:
        return None

    def on_check_prerequisites(self, template) -> tuple[bool, str]:
        return True, ""

    def on_install_prerequisites(self, template) -> None:
        pass

    def on_before_create_env(self, template) -> None:
        pass

    def on_after_create_env(self, template) -> None:
        pass


def implements(plugin: PluginBase, hook: str) -> bool:
    return getattr(type(plugin), hook) is not getattr(PluginBase, hook)
