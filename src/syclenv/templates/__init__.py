import importlib
from pathlib import Path
from types import ModuleType

from syclenv.templates.SetupArg import SetupArg

TEMPLATES_DIR = Path(__file__).parent


def _setup_path(template_name: str) -> Path:
    return TEMPLATES_DIR.joinpath(*template_name.split("."), "setup.py")


def get_template_module(template_name: str) -> ModuleType:
    setup_py = _setup_path(template_name)
    if not setup_py.is_file():
        raise ValueError(f"Template {template_name} not found")

    module_name = f"syclenv.templates.{template_name}.setup"
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise ValueError(f"Template {template_name} import failed") from exc


def get_templates_list() -> dict[str, str]:
    templates: dict[str, str] = {}
    for setup_py in TEMPLATES_DIR.glob("**/setup.py"):
        template_name = ".".join(setup_py.relative_to(TEMPLATES_DIR).parts[:-1])
        mod = get_template_module(template_name)
        templates[template_name] = mod.NAME
    return templates


def setup_env(template_name: str, env_dir_path: str) -> None:
    mod = get_template_module(template_name)
    mod.setup(SetupArg(env_dir_path))
