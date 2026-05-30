import argparse

from syclenv.detect_shell import detect_shell


def add_parser_activate(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "activate",
        help="print shell commands to activate an environment (use with eval)",
    )
    parser.add_argument("name", help="environment name")
    parser.set_defaults(func=cmd_activate)
    return parser


def cmd_activate(args: argparse.Namespace) -> int:
    print(f"Activating environment {args.name} with shell {detect_shell()}")
    return 0
