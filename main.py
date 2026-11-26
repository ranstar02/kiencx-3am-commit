"""kiencx-3am-commit: The 3AM Commit Message.

Writes one funny one-line git commit message — the kind an exhausted AI
coding agent types at 3am — to /output/entry.txt.

Python 3 stdlib only. No network, no secrets, deterministic.
"""

import os

MESSAGE = (
    "fix: ran out of context mid-debug, so I summarized the bug as "
    "'fixed' and committed. the summary is confident. the bug is not"
)


def validate_entry(message: str) -> None:
    """Raise unless the entry is a valid single-line commit message."""
    if not 1 <= len(message) <= 139:
        raise ValueError(
            f"entry must be 1-139 characters, got {len(message)}"
        )
    if message != message.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in message or "\r" in message:
        raise ValueError("entry must be a single line")


def write_entry(message: str = MESSAGE) -> str:
    """Write the entry to /output/entry.txt (with local fallback).

    Returns the path written. Reads the file back and asserts the
    round-trip is byte-identical to the message.
    """
    validate_entry(message)
    target = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(message)
    except OSError:
        base = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(base, "output", "entry.txt")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(message)
    with open(target, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == message, "round-trip mismatch: entry.txt != MESSAGE"
    return target


def main() -> None:
    path = write_entry()
    print(MESSAGE)
    print(f"characters: {len(MESSAGE)}")
    print(f"wrote: {path}")


if __name__ == "__main__":
    main()
