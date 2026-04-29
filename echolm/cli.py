"""Command-line interface for EchoLM."""

import sys

from echolm import EchoLM


def main() -> None:
    """Entry point for the ``echolm`` command."""
    if len(sys.argv) < 2:
        print("Usage: echolm <prompt>", file=sys.stderr)
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    model = EchoLM()
    print(model.generate(prompt))


if __name__ == "__main__":
    main()
