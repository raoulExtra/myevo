#!/usr/bin/env python3
# version: 0.1.0
# version-date: 2026-10-04
# checksum: sha256:38c68341690cff9beb45f5ee02044066343c6728bb70c1a7bfb4dc1acd632b9b
"""Read-only checks for the myevo Markdown project structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_DIRECTORIES = (
    "action",
    "glossary/system",
    "glossary/project",
    "rule/system",
    "relation/system",
    "decision/system/DONE",
    "requirement/project",
)

STATUS_VALUES = {"draft", "active", "archived", "done"}
ALLOWED_RELATION_TYPES = {"broader", "related", "has", "inherits_from"}


class Verification:
    def __init__(self, root: Path, verbose: bool = False) -> None:
        self.root = root
        self.verbose = verbose
        self.errors: list[str] = []
        self.ids: dict[str, dict[str, Path]] = {}
        self.relations: list[tuple[Path, dict[str, Any]]] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.relative_to(self.root)}: {message}")

    def step(self, path: Path | None, message: str) -> None:
        if not self.verbose:
            return
        prefix = f"{path.relative_to(self.root)}: " if path else ""
        print(f"VERIFY {prefix}{message}")

    def parse_frontmatter(self, path: Path) -> dict[str, Any] | None:
        self.step(path, "filesystem: reading Markdown frontmatter")
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            self.error(path, f"cannot read file: {exc}")
            return None

        if not lines or lines[0].strip() != "---":
            self.error(path, "missing YAML frontmatter")
            return None

        try:
            end = lines.index("---", 1)
        except ValueError:
            self.error(path, "unterminated YAML frontmatter")
            return None

        metadata: dict[str, Any] = {}
        list_key: str | None = None
        for line in lines[1:end]:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("  - ") and list_key:
                metadata.setdefault(list_key, []).append(self.scalar(line[4:]))
                continue
            if ":" not in line:
                self.error(path, f"invalid frontmatter line: {line}")
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                self.error(path, "empty frontmatter key")
                continue
            if value:
                metadata[key] = self.scalar(value)
                list_key = None
            else:
                metadata[key] = []
                list_key = key
        return metadata

    @staticmethod
    def scalar(value: str) -> str:
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            return value[1:-1]
        return value

    def check_directory_layout(self) -> None:
        self.step(None, "filesystem: checking required directories")
        for directory in REQUIRED_DIRECTORIES:
            path = self.root / directory
            if not path.is_dir():
                self.error(path, "required directory is missing")
            else:
                self.step(path, "directory exists")

    def check_record(
        self,
        path: Path,
        required: tuple[str, ...],
        id_key: str,
        prefix: str | None = None,
    ) -> dict[str, Any] | None:
        metadata = self.parse_frontmatter(path)
        if metadata is None:
            return None
        self.step(path, f"content: checking required fields {', '.join(required)}")
        for key in required:
            if key not in metadata or metadata[key] in ("", []):
                self.error(path, f"missing required field: {key}")

        status = metadata.get("status")
        if status and status not in STATUS_VALUES:
            self.error(path, f"unsupported status: {status}")
        elif status:
            self.step(path, f"content: status is valid ({status})")

        record_id = metadata.get(id_key)
        if record_id:
            self.step(path, f"content: checking identifier {record_id}")
            if prefix and not re.fullmatch(rf"{prefix}-\d{{3}}", str(record_id)):
                self.error(path, f"{id_key} must match {prefix}-###")
            records = self.ids.setdefault(prefix or id_key, {})
            previous = records.get(str(record_id))
            if previous:
                self.error(path, f"duplicate {record_id}; already used by {previous}")
            else:
                records[str(record_id)] = path
        return metadata

    def check_glossary(self) -> None:
        self.step(None, "filesystem: scanning glossary Markdown files")
        for path in sorted((self.root / "glossary").rglob("*.md")):
            self.step(path, "content: validating glossary noun term")
            metadata = self.parse_frontmatter(path)
            if metadata is None:
                continue
            for key in ("term", "scope", "type", "status"):
                if key not in metadata or metadata[key] in ("", []):
                    self.error(path, f"missing required field: {key}")
            if metadata.get("type") != "noun":
                self.error(path, "glossary terms must have type: noun")

    def check_relations(self) -> None:
        self.step(None, "filesystem: scanning relation Markdown files")
        relation_root = self.root / "relation"
        for path in sorted(relation_root.rglob("*.md")) if relation_root.exists() else []:
            metadata = self.check_record(
                path,
                ("id", "type", "scope", "from", "relation", "to", "status"),
                "id",
                "RELA",
            )
            if metadata is None:
                continue
            self.relations.append((path, metadata))
            if metadata.get("type") != "relation":
                self.error(path, "relation records must have type: relation")
            relation_type = metadata.get("relation")
            if relation_type not in ALLOWED_RELATION_TYPES:
                self.error(path, f"unsupported relation type: {relation_type}")
            scope = metadata.get("scope")
            for key in ("from", "to"):
                term = metadata.get(key)
                term_scope = metadata.get(f"{key}_scope", scope)
                if term_scope and term:
                    term_path = self.root / "glossary" / str(term_scope) / f"{term}.md"
                    if not term_path.is_file():
                        self.error(
                            path,
                            f"{key} term does not exist: {term_path.relative_to(self.root)}",
                        )
            if metadata.get("from") == metadata.get("to"):
                self.error(path, "relation cannot reference the same term on both sides")

    def check_relation_semantics(self) -> None:
        self.step(None, "content: checking relation inheritance semantics")
        has_relations: set[tuple[tuple[str, str], tuple[str, str]]] = set()

        def endpoint(metadata: dict[str, Any], side: str) -> tuple[str, str]:
            scope = str(metadata.get(f"{side}_scope", metadata.get("scope", "")))
            return scope, str(metadata.get(side, ""))

        for _, metadata in self.relations:
            relation_type = metadata.get("relation")
            source = endpoint(metadata, "from")
            target = endpoint(metadata, "to")
            if relation_type == "has":
                has_relations.add((source, target))

        for path, metadata in self.relations:
            if metadata.get("relation") != "inherits_from":
                continue
            child = endpoint(metadata, "from")
            parent = endpoint(metadata, "to")
            parent_metadata = {
                target
                for source, target in has_relations
                if source == parent
            }
            for target in parent_metadata:
                if (child, target) in has_relations:
                    self.error(
                        path,
                        f"duplicates inherited relation: {child[1]} --has--> {target[1]}",
                    )

    def check_decisions(self) -> None:
        self.step(None, "filesystem: scanning decision Markdown files")
        decision_root = self.root / "decision"
        for path in sorted(decision_root.rglob("*.md")) if decision_root.exists() else []:
            metadata = self.check_record(
                path,
                ("decision_id", "scope", "status"),
                "decision_id",
                "DECI",
            )
            if metadata is None:
                continue
            in_done = "DONE" in path.parts
            if in_done and metadata.get("status") != "done":
                self.error(path, "decisions in DONE must have status: done")
            if not in_done and metadata.get("status") == "done":
                self.error(path, "status: done decisions must be stored in DONE")


    def check_actions(self) -> None:
        self.step(None, "filesystem: scanning action Markdown files")
        action_root = self.root / "action"
        for path in sorted(action_root.glob("*.md")) if action_root.exists() else []:
            self.check_record(path, ("name", "kind", "status"), "name")

    def check_requirements(self) -> None:
        self.step(None, "filesystem: scanning requirement Markdown files")
        requirement_root = self.root / "requirement"
        for path in sorted(requirement_root.rglob("*.md")) if requirement_root.exists() else []:
            self.check_record(
                path,
                ("requirement_id", "scope", "status"),
                "requirement_id",
                "REQUI",
            )

    def run(self) -> int:
        self.step(None, "filesystem: read-only verification; no files modified")
        self.check_directory_layout()
        self.check_glossary()
        self.check_relations()
        self.check_relation_semantics()
        self.check_decisions()
        self.check_actions()
        self.check_requirements()
        if self.errors:
            for error in self.errors:
                print(f"ERROR: {error}")
            print(f"Verification failed: {len(self.errors)} error(s).")
            return 1
        print(f"Verification passed: {self.root}")
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a myevo Markdown project folder.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify", help="verify project folders and records")
    verify.add_argument("-v", "--verbose", action="store_true", help="show filesystem and content checks")
    verify.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    if args.command == "verify":
        root = args.path.expanduser().resolve()
        if not root.is_dir():
            print(f"ERROR: project folder does not exist: {root}", file=sys.stderr)
            return 2
        return Verification(root, verbose=args.verbose).run()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
