import argparse


def add_parser_create(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("create", help="create a new environment")
    parser.add_argument("template", help="template name")
    parser.add_argument("path", help="environment path")
    parser.add_argument(
        "--install-prerequisites", action="store_true", help="install prerequisites"
    )
    parser.add_argument(
        "--noconfirm", action="store_true", help="do not confirm commands"
    )
    parser.add_argument(
        "--plugin",
        action="append",
        default=[],
        metavar="PLUGIN",
        help="plugin name or path (can be specified multiple times)",
    )
    parser.set_defaults(func=cmd_create)
    return parser


def cmd_create(args: argparse.Namespace) -> int:
    from syclenv.templates import setup_env

    setup_env(
        args.template,
        args.path,
        install_prerequisites=args.install_prerequisites,
        noconfirm=args.noconfirm,
        plugins=args.plugin,
    )

    return 0
