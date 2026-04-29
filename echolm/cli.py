"""Command-line interface for EchoLM."""

import argparse
import sys

from echolm import EchoLM


def _cmd_generate(args: argparse.Namespace) -> None:
    if not args.prompt:
        print("Usage: echolm generate <prompt>", file=sys.stderr)
        sys.exit(1)
    model = EchoLM()
    print(model.generate(" ".join(args.prompt)))


def _cmd_serve(args: argparse.Namespace) -> None:
    from echolm.server import serve
    serve(host=args.host, port=args.port)


def main() -> None:
    """Entry point for the ``echolm`` command."""
    parser = argparse.ArgumentParser(
        prog="echolm",
        description="EchoLM — a language model that returns exactly what you give it.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # echolm generate <prompt>
    gen_parser = subparsers.add_parser("generate", help="Echo a prompt")
    gen_parser.add_argument("prompt", nargs="+", help="The text to echo")

    # echolm serve
    serve_parser = subparsers.add_parser(
        "serve", help="Start the OpenAI-compatible HTTP server"
    )
    serve_parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    )

    # Backwards-compat: if the first arg is not a known subcommand, treat
    # everything as a prompt (i.e. `echolm hello world` still works).
    known_commands = {"generate", "serve", "-h", "--help"}
    if len(sys.argv) >= 2 and sys.argv[1] not in known_commands:
        model = EchoLM()
        print(model.generate(" ".join(sys.argv[1:])))
        return

    args = parser.parse_args()
    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.command == "generate":
        _cmd_generate(args)
    elif args.command == "serve":
        _cmd_serve(args)


if __name__ == "__main__":
    main()
