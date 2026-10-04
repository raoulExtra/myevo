#!/usr/bin/env python3
# version: 0.2.0
# version-date: 2026-10-04
# checksum: sha256:0000000000000000000000000000000000000000000000000000000000000000
# checksum verification is temporarily disabled; presence and format remain checked.
"""Entry point for executable artifact verification."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from myevo.artifact_verify import main


if __name__ == "__main__":
    raise SystemExit(main())
