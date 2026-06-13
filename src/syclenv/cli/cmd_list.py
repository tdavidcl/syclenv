import argparse

from syclenv.plugins import load_plugins


def add_parser_list(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("list", help="list all environments")
    parser.set_defaults(func=cmd_list)
    return parser


def cmd_list(args: argparse.Namespace) -> int:
    from syclenv.plugins import run_on_template_list

    load_plugins()

    for path, name in run_on_template_list().items():
        print(f"{path}: {name}")
    return 0
