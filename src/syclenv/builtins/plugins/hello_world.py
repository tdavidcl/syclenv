from syclenv.templates import SetupArg
from syclenv.templates.PluginBase import PluginBase

class HelloWorldPlugin(PluginBase):
    name = "hello world"
    description= "hello world again !"

    def __init__(self, args : SetupArg):
        print("hello world from hello world plugin")

    def check_prerequisites(self, template) -> tuple[bool, str]:
        print("--check_prerequisites -> there are none for a hello world")
        return True, " "

    def install_prerequisites(self, template) -> None:
        print("--install_prerequisites -> there are none for a hello world")

    def before_create_env(self, template) -> None:
        print("--no prestep for hello world")

    def after_create_env(self, template) -> None:
        print("patching env with a nice hello world")

PLUGIN_CLASS = HelloWorldPlugin
