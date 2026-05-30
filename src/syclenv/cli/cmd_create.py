import argparse


def add_parser_create(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("create", help="create a new environment")
    parser.add_argument("name", help="environment name")
    parser.set_defaults(func=cmd_create)
    return parser


def cmd_create(args: argparse.Namespace) -> int:
    print(f'Activate it with: eval "$(syclvenv activate {args.name})"')
    return 0
