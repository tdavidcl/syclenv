import argparse

from syclenv.detect_shell import detect_shell


def add_parser_diagnose(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("diagnose", help="diagnose an environment")
    parser.set_defaults(func=cmd_diagnose)
    return parser


def cmd_diagnose(args: argparse.Namespace) -> int:
    print(f"Current shell environment: {detect_shell()}")
    return 0
