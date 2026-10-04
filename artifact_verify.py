#!/usr/bin/env python3
# version: 0.1.0
# version-date: 2026-10-04
# checksum: sha256:0cbbc1486a354953705f8d311f8d4da287d0fdbfedbaab3c80fbb0a8568ad38e
"""Verify embedded version metadata and checksums for executable artifacts."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


CODE_SUFFIXES = {".c", ".cpp", ".go", ".js", ".py", ".rs", ".sh", ".ts", ".tsx"}
COMMENT_PREFIXES = {
    ".c": "//",
    ".cpp": "//",
    ".go": "//",
    ".js": "//",
    ".py": "#",
    ".rs": "//",
    ".sh": "#",
    ".ts": "//",
    ".tsx": "//",
}
SKIP_DIRECTORIES = {".git", "__pycache__", ".venv", "venv"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CHECKSUM_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


class ArtifactVerification:
    def __init__(self, root: Path, verbose: bool = False) -> None:
        self.root = root
        self.verbose = verbose
        self.errors: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.relative_to(self.root)}: {message}")

    def step(self, path: Path | None, message: str) -> None:
        if not self.verbose:
            return
        prefix = f"{path.relative_to(self.root)}: " if path else ""
        print(f"VERIFY {prefix}{message}")

    def code_files(self) -> list[Path]:
        self.step(None, f"filesystem: scanning {self.root} for executable code files")
        files = [
            path
            for path in self.root.rglob("*")
            if path.is_file()
            and not any(part in SKIP_DIRECTORIES for part in path.parts)
            and path.suffix.lower() in CODE_SUFFIXES
        ]
        for path in sorted(files):
            self.step(path, "filesystem: discovered executable code file")
        return sorted(files)

    @staticmethod
    def metadata_pattern(path: Path) -> re.Pattern[str]:
        prefix = re.escape(COMMENT_PREFIXES[path.suffix.lower()])
        return re.compile(
            rf"^\s*{prefix}\s+(version|version-date|checksum):\s*(.*?)\s*$"
        )

    def read_source(self, path: Path) -> str | None:
        self.step(path, "filesystem: reading source text")
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            self.error(path, f"cannot read file: {exc}")
            return None

    def embedded_metadata(self, path: Path, source: str) -> dict[str, str]:
        metadata: dict[str, str] = {}
        pattern = self.metadata_pattern(path)
        for line in source.splitlines():
            match = pattern.match(line)
            if not match:
                continue
            key, value = match.groups()
            if key in metadata:
                self.error(path, f"duplicate embedded field: {key}")
                continue
            metadata[key] = value
        return metadata

    def canonical_source(self, path: Path) -> bytes:
        self.step(path, "filesystem: reading bytes for canonical checksum")
        prefix = COMMENT_PREFIXES[path.suffix.lower()]
        pattern = self.metadata_pattern(path)
        canonical_lines: list[bytes] = []
        for raw_line in path.read_bytes().splitlines(keepends=True):
            line = raw_line.decode("utf-8")
            newline = ""
            body = line
            if line.endswith("\r\n"):
                body, newline = line[:-2], "\r\n"
            elif line.endswith(("\n", "\r")):
                body, newline = line[:-1], line[-1]
            match = pattern.match(body)
            if match and match.group(1) == "checksum":
                canonical_lines.append(f"{prefix} checksum: <checksum>{newline}".encode())
            else:
                canonical_lines.append(raw_line)
        return b"".join(canonical_lines)

    def verify_file(self, path: Path) -> None:
        self.step(path, "reading embedded metadata")
        source = self.read_source(path)
        if source is None:
            return
        metadata = self.embedded_metadata(path, source)
        for key in ("version", "version-date", "checksum"):
            if not metadata.get(key):
                self.error(path, f"missing embedded field: {key}")
            else:
                self.step(path, f"{key} present")

        version_date = metadata.get("version-date")
        if version_date and not DATE_PATTERN.fullmatch(version_date):
            self.error(path, "version-date must use YYYY-MM-DD")
        elif version_date:
            self.step(path, "version-date format valid")

        checksum = metadata.get("checksum")
        if checksum and not CHECKSUM_PATTERN.fullmatch(checksum):
            self.error(path, "checksum must use sha256:<64 lowercase hexadecimal characters>")
        if checksum:
            expected = "sha256:" + hashlib.sha256(self.canonical_source(path)).hexdigest()
            if checksum != expected:
                self.error(path, "checksum does not match the canonical file contents")
            else:
                self.step(path, "checksum matches canonical file contents")

    def show_versions(self, code_files: list[Path]) -> int:
        for path in code_files:
            source = self.read_source(path)
            if source is None:
                continue
            metadata = self.embedded_metadata(path, source)
            print(f"{path.relative_to(self.root)}")
            print(f"  version: {metadata.get('version', '<missing>')}")
            print(f"  version-date: {metadata.get('version-date', '<missing>')}")
            print(f"  checksum: {metadata.get('checksum', '<missing>')}")
        if self.errors:
            for error in self.errors:
                print(f"ERROR: {error}")
            return 1
        return 0

    def run(self, code_files: list[Path] | None = None) -> int:
        if code_files is None:
            code_files = self.code_files()
        self.step(None, "filesystem: read-only verification; no files modified")
        self.step(None, f"found {len(code_files)} executable code file(s)")
        for path in code_files:
            self.verify_file(path)
        if self.errors:
            for error in self.errors:
                print(f"ERROR: {error}")
            print(f"Artifact verification failed: {len(self.errors)} error(s).")
            return 1
        print(f"Artifact verification passed: {len(code_files)} executable code file(s).")
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify embedded executable artifact metadata.")
    parser.add_argument("--version", action="store_true", help="show artifact information for all code files")
    parser.add_argument("-v", "--verbose", action="store_true", help="show verification steps")
    parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.path.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project folder does not exist: {root}", file=sys.stderr)
        return 2

    verification = ArtifactVerification(root, verbose=args.verbose)
    code_files = verification.code_files()
    if args.version:
        return verification.show_versions(code_files)
    return verification.run(code_files)


if __name__ == "__main__":
    raise SystemExit(main())
