import argparse

from syclenv.cli.BANNER import BANNER
from syclenv.cli.cmd_activate import add_parser_activate
from syclenv.cli.cmd_create import add_parser_create
from syclenv.cli.cmd_diagnose import add_parser_diagnose
from syclenv.cli.cmd_list import add_parser_list


class BannerParser(argparse.ArgumentParser):
    def format_help(self):
        return BANNER + "\n" + super().format_help()


def build_parser() -> argparse.ArgumentParser:
    parser = BannerParser(
        prog="syclvenv",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser_create(subparsers)
    add_parser_activate(subparsers)
    add_parser_diagnose(subparsers)
    add_parser_list(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    return args.func(args)
