import shutil


def is_ninja_available():
    return shutil.which("ninja") is not None


def detect_buildsystem() -> str:
    """Return the build system name (e.g. ``make``, ``ninja``)."""

    if is_ninja_available():
        return "ninja"
    else:
        return "make"


def get_buildsystem_command() -> tuple[str, str]:
    buildsystem = detect_buildsystem()

    if buildsystem == "ninja":
        return "ninja", "Ninja"
    elif buildsystem == "make":
        return "make", "Unix Makefiles"
    else:
        raise ValueError(f"Unknown build system: {buildsystem}")
