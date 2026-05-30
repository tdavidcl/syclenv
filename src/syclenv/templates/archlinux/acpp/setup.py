import subprocess
import sys
from pathlib import Path
from importlib.resources import files


from syclenv.detect_buildsystem import get_buildsystem_command
from syclenv.templates.SetupArg import SetupArg


def run_cmd(command, log_cmd=False, bash=True):
    sys.stdout.flush()
    sys.stderr.flush()
    if bash:
        if log_cmd:
            print(f"   Running command : bash -c '{command}'")

        try:
            subprocess.run(
                ["bash", "-c", command],
                check=True,
                stdout=sys.stdout,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            return False
        return True
    else:
        raise NotImplementedError("Only bash=True is currently supported for run_cmd")


NAME = "Hello world env"

template_file_bash = files(__package__) / "template.bash"
template_file_prerequisites = files(__package__) / "prerequisites.bash"

def check_prerequisites():
    # run the prerequisites.bash file
    if not run_cmd(
        "source "
        + template_file_prerequisites.absolute().__str__()
        + " && check_prerequisites"
    ):
        raise ValueError("Prerequisites are not installed")


def install_prerequisites():
    # run the prerequisites.bash file
    if not run_cmd(
        "source "
        + template_file_prerequisites.absolute().__str__()
        + " && install_prerequisites"
    ):
        raise ValueError("Issue installing prerequisites")


def setup(arg: SetupArg):
    print(f"Hello, World! {arg.path}")

    if arg.install_prerequisites:
        install_prerequisites()

    check_prerequisites()

    generator, cmake_generator = get_buildsystem_command()

    ENV_VARS = {
        "SYCLENV_CURRENT_ENV_PATH": Path(arg.path).absolute(),
        "CMAKE_GENERATOR": cmake_generator,
        "MAKE_EXEC": generator,
        "MAKE_OPT": "()",
        "CMAKE_OPT": "()",
    }

    # create a dir at the path
    Path(arg.path).mkdir(parents=True, exist_ok=True)

    # load prerequisites file
    with open(template_file_prerequisites) as f:
        template = f.read()

    # add env vars to template
    for var, value in ENV_VARS.items():
        line = f"export {var}={value}"
        template += line + "\n"

    # load template file
    with open(template_file_bash) as f:
        template += f.read()

    # create a file called activate.bash
    with open(arg.path + "/activate.bash", "w") as f:
        f.write(template)

    with open(arg.path + "/activate.zsh", "w") as f:
        f.write(template)

    with open(arg.path + "/activate.sh", "w") as f:
        f.write(template)
