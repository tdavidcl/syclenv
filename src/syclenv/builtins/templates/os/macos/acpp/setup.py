from importlib.resources import files
from pathlib import Path

from syclenv.detect_buildsystem import get_buildsystem_command
from syclenv.run_cmd import run_cmd
from syclenv.templates.SetupArg import SetupArg
from syclenv.templates.TemplateBase import TemplateBase
from syclenv.utils.macos import (
    has_brew_packages,
)

template_file_bash = files(__package__) / "template.bash"
template_file_prerequisites = files(__package__) / "prerequisites.bash"

common_helper_scripts = files(__package__) / ".." / ".." / ".." / "helper_scripts"
clone_acpp_bash = common_helper_scripts / "clone_acpp.bash"

mandatory_packages = [
    "adaptivecpp",
    "cmake",
]


default_install_packages = [
    "adaptivecpp",
    "cmake",
    # so much faster than make
    "ninja",
]


class MacOSBrewAcppTemplate(TemplateBase):
    name = "MacOS /w AdaptiveCpp"
    description = "MacOSBrewAcpp template"

    def __init__(self, args: SetupArg):
        self.args = args

    def check_prerequisites(self) -> tuple[bool, str]:
        missing_packages = []
        for package in mandatory_packages:
            if not has_brew_packages([package]):
                missing_packages.append(package)

        if len(missing_packages) > 0:
            str_missing_packages = " ".join(missing_packages)
            return False, (
                f"Missing packages: {str_missing_packages}. Install them with:\n"
                f"brew install {str_missing_packages}"
            )
        return True, None

    def install_prerequisites(self) -> None:
        cmd = f"brew install {' '.join(default_install_packages)}"

        if self.args.noconfirm:
            run_cmd(cmd, log_cmd=True, ask_confirm=False, live_output=True)
        else:
            run_cmd(cmd, log_cmd=True, ask_confirm=True, live_output=True)

    def create_env(self) -> None:
        generator, cmake_generator = get_buildsystem_command()

        env_vars = {
            "SYCLENV_CURRENT_ENV_PATH": Path(self.args.path).absolute(),
            "CMAKE_GENERATOR": '"' + cmake_generator + '"',
            "MAKE_EXEC": generator,
            "MAKE_OPT": "()",
            "CMAKE_OPT": "()",
            "ACPP_APPDB_DIR": "/tmp/acpp-appdb",
        }

        # create a dir at the path
        Path(self.args.path).mkdir(parents=True, exist_ok=True)

        template = ""

        # add env vars to template
        for var, value in env_vars.items():
            line = f"export {var}={value}"
            template += line + "\n"

        template += "function _internal_deactivate {"
        for var in env_vars.keys():
            template += f"  unset {var}\n"
        template += "}\n"
        template += "\n"

        # load template file
        with open(template_file_bash) as f:
            template += f.read()

        # Create activate scripts
        with open(self.args.path + "/activate.sh", "w") as f:
            f.write(template)

        with open(self.args.path + "/activate.bash", "w") as f:
            f.write(template)

        with open(self.args.path + "/activate.zsh", "w") as f:
            f.write(template)


TEMPLATE_CLASS = MacOSBrewAcppTemplate
