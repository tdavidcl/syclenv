import argparse
from pathlib import Path
from syclenv.detect_shell import detect_shell


def add_parser_activate(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "activate",
        help="print shell commands to activate an environment",
    )
    parser.add_argument("path", help="environment path")
    parser.set_defaults(func=cmd_activate)
    return parser


def cmd_activate(args: argparse.Namespace) -> int:
    
    # list all the activate scripts in env_dir_path
    activate_scripts = [s.name for s in Path(args.path).glob("activate.*")]

    supported_shells = []
    for ascript in activate_scripts:
        suffix = ascript.split(".")[-1]
        supported_shells.append(suffix)

    if(len(activate_scripts) == 0):
        raise ValueError(f"No activate scripts found in {env_dir_path}")
        
    current_shell = detect_shell()
    if(current_shell == "sh" and "sh" in supported_shells):
        print("source " + args.path + "/activate.sh")
    elif(current_shell == "bash" and "bash" in supported_shells):
        print("source " + args.path + "/activate.bash")
    elif(current_shell == "zsh" and "zsh" in supported_shells):
        print("source " + args.path + "/activate.zsh")
    else:
        raise ValueError(f"Unsupported shell: {current_shell}")


    return 0
