from syclenv.plugins.PluginBase import PluginBase
from syclenv.run_cmd import run_bash_cmd


class HelloWorldPlugin(PluginBase):
    name = "hello world"
    description = "hello world again !"

    def __init__(self):
        run_bash_cmd("touch helloworld__init")

    def on_check_prerequisites(self, template) -> tuple[bool, str]:
        run_bash_cmd("touch helloworld__prereq_check")
        return True, " "

    def on_install_prerequisites(self, template) -> None:
        run_bash_cmd("touch helloworld__prereq_install")

    def on_before_create_env(self, template) -> None:
        run_bash_cmd("touch helloworld__beforeenv")

    def on_after_create_env(self, template) -> None:
        run_bash_cmd("touch helloworld__afterenv")

    def on_template_list(self, original: dict[str, str]) -> dict[str, str]:
        return {**original, "hello world": "hello world"}


PLUGIN_CLASS = HelloWorldPlugin
