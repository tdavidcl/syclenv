from importlib.resources import files
from pathlib import Path

from syclenv.detect_buildsystem import get_buildsystem_command
from syclenv.run_cmd import run_cmd
from syclenv.templates.SetupArg import SetupArg

NAME = "Hello world env"

template_file_bash = files(__package__) / "template.bash"
template_file_prerequisites = files(__package__) / "prerequisites.bash"


def has_pacman_package(package: str) -> bool:
    return run_cmd(f"pacman -Q {package} >/dev/null 2>&1", log_error=False)


def get_pacman_llvm_version() -> str:
    for ver in [21, 20]:
        if has_pacman_package(f"llvm{ver}") and has_pacman_package(f"clang{ver}"):
            return ver
    return None


def get_pacman_llvm_install_dir() -> str:
    llvm_version = get_pacman_llvm_version()
    if llvm_version is None:
        return None
    return f"/usr/lib/llvm{llvm_version}"


mandatory_packages = [
    "base-devel",
    "git",
    "cmake",
    "boost",
    "openmp",
    "lld",
    "numactl",
    "python",
]


def check_prerequisites():
    if get_pacman_llvm_version() is None:
        raise ValueError(
            "No LLVM 20 or 21 found via pacman. Install one with:\n"
            "sudo pacman -S llvm20 clang20 or sudo pacman -S llvm21 clang21"
        )

    missing_packages = []
    for package in mandatory_packages:
        if not has_pacman_package(package):
            missing_packages.append(package)

    if len(missing_packages) > 0:
        str_missing_packages = " ".join(missing_packages)
        raise ValueError(
            f"Missing packages: {str_missing_packages}. Install them with:\n"
            f"sudo pacman -S {str_missing_packages}"
        )


default_install_packages = [
    "base-devel",
    "git",
    "cmake",
    "boost",
    "openmp",
    "llvm20",
    "clang20",
    "lld",
    "numactl",
    "python",
]


def install_prerequisites():
    run_cmd(
        f"sudo pacman -S --noconfirm {' '.join(default_install_packages)}",
        log_cmd=True,
        log_error=True,
    )


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
        "LLVM_INSTALL_DIR": get_pacman_llvm_install_dir(),
        "ACPP_VERSION": "develop",
        "ACPP_APPDB_DIR": "/tmp/acpp-appdb",
    }

    # create a dir at the path
    Path(arg.path).mkdir(parents=True, exist_ok=True)

    template = ""

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
