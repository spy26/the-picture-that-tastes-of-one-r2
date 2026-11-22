#!/usr/bin/env python3
"""Entry: molten chocolate lava cake (single dish, one ingredient story).

Reads the bundled source.jpg and writes it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.png. No re-encoding, so the output is fully
deterministic: identical bytes on every run.
"""
import os
import sys

SOURCE_NAME = "source.jpg"
OUTPUT_NAME = "entry.png"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_source_bytes(path):
    """Read the bundled image; kept separate so main() stays a thin pipeline."""
    with open(path, "rb") as handle:
        return handle.read()


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(repo_dir, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_path = os.path.join(out_dir, OUTPUT_NAME)

    if os.path.abspath(out_path) == os.path.abspath(source_path):
        fail("output path would overwrite the bundled source; refusing")

    try:
        data = read_source_bytes(source_path)
    except OSError as exc:
        fail(f"cannot read source {source_path}: {exc}")

    if not data:
        fail("source image is empty")

    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)
    except OSError as exc:
        fail(f"cannot write output {out_path}: {exc}")

    try:
        with open(out_path, "rb") as f:
            written = f.read()
    except OSError as exc:
        fail(f"cannot re-read output {out_path}: {exc}")

    if written != data:
        fail("written output differs from source bytes")

    print(f"wrote {out_path} ({len(written)} bytes)")


if __name__ == "__main__":
    main()
