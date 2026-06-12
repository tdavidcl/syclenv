from syclenv.plugins.PluginBase import PluginBase
from syclenv.run_cmd import run_bash_cmd


class HelloWorldPlugin(PluginBase):
    name = "hello world"
    description = "hello world again !"

    def __init__(self):
        run_bash_cmd("touch helloworld__init")

    def check_prerequisites(self, template) -> tuple[bool, str]:
        run_bash_cmd("touch helloworld__prereq_check")
        return True, " "

    def install_prerequisites(self, template) -> None:
        run_bash_cmd("touch helloworld__prereq_install")

    def before_create_env(self, template) -> None:
        run_bash_cmd("touch helloworld__beforeenv")

    def after_create_env(self, template) -> None:
        run_bash_cmd("touch helloworld__afterenv")


PLUGIN_CLASS = HelloWorldPlugin
