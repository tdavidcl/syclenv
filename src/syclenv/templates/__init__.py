import importlib
from importlib.resources import files
from pathlib import Path
from types import ModuleType

from syclenv.logs import print_panel
from syclenv.plugins import LOADED_PLUGINS, load_plugins
from syclenv.plugins.PluginBase import (
    implements_after_create_env,
    implements_before_create_env,
    implements_template_list_hook,
)
from syclenv.templates import TemplateBase
from syclenv.templates.SetupArg import SetupArg

TEMPLATES_DIR = files(__package__) / ".." / "builtins" / "templates"


def _setup_path(template_name: str) -> Path:
    return TEMPLATES_DIR.joinpath(*template_name.split("."), "setup.py")


def get_template_module(template_name: str) -> ModuleType:
    setup_py = _setup_path(template_name)
    if not setup_py.is_file():
        raise ValueError(f"Template {template_name} not found")

    module_name = f"syclenv.builtins.templates.{template_name}.setup"
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise ValueError(f"Template {template_name} import failed") from exc


def get_templates_list() -> dict[str, str]:
    templates: dict[str, str] = {}
    for setup_py in TEMPLATES_DIR.glob("**/setup.py"):
        template_name = ".".join(setup_py.relative_to(TEMPLATES_DIR).parts[:-1])
        mod = get_template_module(template_name)
        templates[template_name] = mod.TEMPLATE_CLASS.name
    
    for p in LOADED_PLUGINS:
        if implements_template_list_hook(p):
            templates = p.on_template_list(templates)
    
    return templates


def meta_run_prerequisites(inputclass, install_prerequisites: bool, *args):
    print(f"Checking prerequisites for {inputclass.name}")
    is_ok, error_message = inputclass.check_prerequisites(*args)

    if not is_ok:
        if install_prerequisites:
            print_panel("prerequisites failed", error_message, color="yellow")
            print("Installing prerequisites...")
            inputclass.install_prerequisites(*args)

            print(f"Checking prerequisites again for {inputclass.name}")
            is_ok, error_message = inputclass.check_prerequisites(*args)
            if not is_ok:
                print_panel("Error", error_message, color="red")
                raise ValueError("Prerequisites failed")
        else:
            print_panel("Error", error_message, color="red")
            raise ValueError("Prerequisites failed")


def run_setup(
    template_class: TemplateBase,
    install_prerequisites: bool,
):
    meta_run_prerequisites(template_class, install_prerequisites)

    for p in LOADED_PLUGINS:
        meta_run_prerequisites(p, install_prerequisites, template_class)

    for p in LOADED_PLUGINS:
        if implements_before_create_env(p):
            print(f"-- applying before env step for plugin {p.name}")
            p.before_create_env(template_class)

    print(f"Creating env for {template_class.name}")
    template_class.create_env()
    print(f"Env created for {template_class.name}")

    for p in LOADED_PLUGINS:
        if implements_after_create_env(p):
            print(f"-- applying after env step for plugin {p.name}")
            p.after_create_env(template_class)


def setup_env(
    template_name: str,
    env_dir_path: str,
    install_prerequisites: bool,
    noconfirm: bool,
    plugins: list[str],
) -> None:
    try:
        mod = get_template_module(template_name)
    except ValueError as e:
        print_panel("Error", str(e), color="red")
        tlist = get_templates_list()
        lst = ""
        for k, v in tlist.items():
            if len(lst) > 0:
                lst += "\n"
            lst += f"{k}: {v}"
        print_panel("Chose a valid template from the list below", lst, color="green")
        raise ValueError(f"Template {template_name} not found")

    load_plugins(plugins)

    print("--------------------------------")
    print(f"Setting up env {template_name} in {env_dir_path}")
    print("--------------------------------")

    setup_arg = SetupArg(env_dir_path, noconfirm)

    run_setup(mod.TEMPLATE_CLASS(setup_arg), install_prerequisites)

    print("--------------------------------")
    print("Setup complete")
    print("--------------------------------")

    # list all the activate scripts in env_dir_path
    activate_scripts = [s.name for s in Path(env_dir_path).glob("activate.*")]

    if len(activate_scripts) == 0:
        raise ValueError(f"No activate scripts found in {env_dir_path}")

    elif len(activate_scripts) > 0:
        print(f"Shell support for {env_dir_path}:")
        for ascript in activate_scripts:
            if ascript.endswith(".sh"):
                print('  sh -> eval "$(syclvenv activate .yolo)"')
            elif ascript.endswith(".bash"):
                print('  bash -> eval "$(syclvenv activate .yolo)"')
            elif ascript.endswith(".zsh"):
                print('  zsh -> eval "$(syclvenv activate .yolo)"')
            else:
                print(ascript)
