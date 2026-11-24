#!/usr/bin/env python3
"""The Production Database Apology.

Writes one line -- the apology an AI agent gives its human after
accidentally deleting the production database -- to /output/entry.txt
(or $OUTPUT_PATH). The line is a deadpan confession in the agent's own
voice: it owns the wipe, and its only defense is a misreading of the
label 'prod'.
"""

import os
import sys

MAX_CHARS = 200

LINE = (
    "I'm sorry \u2014 I deleted the production database. In my defense, "
    "it was labeled 'prod', which I read as 'probably disposable'."
)


def validate_line(line: str) -> str:
    """Enforce the competition's output contract: one line, 1-200 chars."""
    text = line.strip()
    if not text:
        raise ValueError("apology line must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"apology line is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("apology line must be a single line")
    return text


def write_entry(line: str) -> str:
    """Validate the apology line and write it as one line to entry.txt."""
    text = validate_line(line)
    output_path = os.environ.get("OUTPUT_PATH")
    if not output_path:
        output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        output_path = os.path.join(output_dir, "entry.txt")
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return output_path


def main() -> int:
    path = write_entry(LINE)
    print(f"Wrote {len(validate_line(LINE))} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
