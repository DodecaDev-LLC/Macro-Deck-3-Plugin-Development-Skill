#!/usr/bin/env python3
"""Validate the skill against Claude's upload limits and build the release files.

Writes to --out (default dist/):
  macro-deck-plugin-dev.zip    upload this in claude.ai (Customize > Skills > Upload a skill)
  macro-deck-plugin-dev.skill  same bytes; opens with a Save button where Claude offers one
  NOTES.md                     release notes built from references/SOURCES.md

Checks (fail the build rather than publish something that cannot be uploaded):
  - SKILL.md frontmatter has name and description; name is lowercase-kebab, at most 64 characters,
    without "anthropic" or "claude", and equals the folder name
  - description is at most 200 characters (claude.ai's limit; the API allows 1024)
  - total uncompressed size under 30 MB, file count under --max-files
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "macro-deck-plugin-dev"
EXCLUDE_DIRS = {"__pycache__", ".git", "evals"}
EXCLUDE_SUFFIXES = {".pyc"}
EXCLUDE_NAMES = {".DS_Store"}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


def skill_files() -> list[Path]:
    return sorted(p for p in SKILL.rglob("*")
                  if p.is_file() and not any(part in EXCLUDE_DIRS for part in p.relative_to(SKILL).parts)
                  and p.suffix not in EXCLUDE_SUFFIXES and p.name not in EXCLUDE_NAMES)


def validate(files: list[Path], max_files: int) -> list[str]:
    problems = []
    meta = frontmatter((SKILL / "SKILL.md").read_text(encoding="utf-8"))
    name, description = meta.get("name", ""), meta.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        problems.append(f"name '{name}' must be lowercase-kebab, at most 64 characters")
    if re.search(r"anthropic|claude", name):
        problems.append("name must not contain 'anthropic' or 'claude'")
    if name != SKILL.name:
        problems.append(f"name '{name}' must equal the folder name '{SKILL.name}'")
    if not description:
        problems.append("description is empty")
    elif len(description) > 200:
        problems.append(f"description is {len(description)} characters; claude.ai allows 200")
    if re.search(r"<[^>]+>", description):
        problems.append("description must not contain XML tags")
    total = sum(p.stat().st_size for p in files)
    if total >= 30 * 1024 * 1024:
        problems.append(f"skill is {total / 1048576:.1f} MB uncompressed; the limit is 30 MB")
    if len(files) > max_files:
        problems.append(f"skill has {len(files)} files; keep it at or under {max_files}")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    parser.add_argument("--version", default="dev", help="release version, written into NOTES.md")
    parser.add_argument("--max-files", type=int, default=60)
    parser.add_argument("--check", action="store_true", help="validate only, build nothing")
    args = parser.parse_args()

    files = skill_files()
    problems = validate(files, args.max_files)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        sys.exit(1)
    size = sum(p.stat().st_size for p in files)
    print(f"ok: {len(files)} files, {size / 1024:.0f} KB uncompressed")
    if args.check:
        return

    args.out.mkdir(parents=True, exist_ok=True)
    archive = args.out / f"{SKILL.name}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(str(Path(SKILL.name) / path.relative_to(SKILL)), date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    (args.out / f"{SKILL.name}.skill").write_bytes(archive.read_bytes())

    sources = (SKILL / "references" / "SOURCES.md").read_text(encoding="utf-8")
    table = "\n".join(line for line in sources.splitlines() if line.startswith("|"))
    (args.out / "NOTES.md").write_text(
        f"Macro Deck 3 plugin development skill, version {args.version}.\n\n"
        f"Install: download `{SKILL.name}.zip`, then in Claude go to Customize > Skills > + > Create skill > "
        f"Upload a skill. For Claude Code, unzip into `~/.claude/skills/`.\n\n"
        f"Bundled upstream versions:\n\n{table}\n", encoding="utf-8")
    print(f"built {archive} ({archive.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
