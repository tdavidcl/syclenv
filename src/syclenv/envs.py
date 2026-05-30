import os
import re
import venv
from pathlib import Path

ENV_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


def envs_root() -> Path:
    if home := os.environ.get("SYCLENV_HOME"):
        return Path(home).expanduser() / "envs"
    return Path.home() / ".local" / "share" / "syclenv" / "envs"


def env_path(name: str) -> Path:
    validate_env_name(name)
    return envs_root() / name


def validate_env_name(name: str) -> None:
    if not ENV_NAME_PATTERN.match(name):
        msg = (
            f"invalid environment name {name!r}: "
            "use letters, digits, '.', '_', or '-', starting with a letter or digit"
        )
        raise ValueError(msg)


def create_env(name: str) -> Path:
    path = env_path(name)
    if path.exists():
        raise FileExistsError(f"environment already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    venv.create(path, with_pip=True)
    return path


def activation_shell(name: str) -> str:
    path = env_path(name)
    if not path.is_dir():
        raise FileNotFoundError(f"environment not found: {name} ({path})")
    activate = path / "bin" / "activate"
    if not activate.is_file():
        raise FileNotFoundError(f"environment is missing activate script: {activate}")
    # Source the venv's activate script so behavior matches a normal virtualenv.
    return f'. "{activate}"'
