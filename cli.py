#!/usr/bin/env python3
# version: 0.2.0
# version-date: 2026-10-04
# checksum: sha256:0000000000000000000000000000000000000000000000000000000000000000
# checksum verification is temporarily disabled in artifact_verify.py.
"""Entry point for the myevo project verifier."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from myevo.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
