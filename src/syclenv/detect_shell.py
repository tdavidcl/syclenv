import os
import sys
from pathlib import Path


def detect_shell() -> str:
    """Return the host shell name (e.g. ``bash``, ``zsh``, ``fish``)."""
    if shell := os.environ.get("SHELL"):
        return Path(shell).name

    if sys.platform == "win32":
        if comspec := os.environ.get("ComSpec"):
            return Path(comspec).stem.lower()
        return "powershell"

    try:
        import pwd

        login_shell = pwd.getpwuid(os.getuid()).pw_shell
        return Path(login_shell).name
    except (ImportError, KeyError):
        return "sh"
