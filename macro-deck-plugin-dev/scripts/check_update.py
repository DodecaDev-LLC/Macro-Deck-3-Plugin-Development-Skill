#!/usr/bin/env python3
"""Tell whether a newer release of this skill exists. Reports only; never changes anything.

Compares the VERSION file the release build writes into the skill with the latest GitHub release. When
that cannot be checked (offline, a sandbox that blocks GitHub, a copy from before VERSION existed), it
falls back to the age of the bundled docs recorded in references/SOURCES.md.

Exit codes: 0 up to date, 10 a newer release exists, 11 the bundled docs are old and the release could not
be checked, 3 nothing could be determined.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REPOSITORY = "DodecaDev-LLC/Macro-Deck-3-Plugin-Development-Skill"
LATEST_API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
UPDATE_HELP = f"https://github.com/{REPOSITORY}#updating"
STALE_DAYS = 30


def parse_version(text: str | None) -> tuple[int, ...] | None:
    match = re.fullmatch(r"v?(\d{4})\.(\d{1,2})\.(\d{1,2})\.(\d+)", (text or "").strip())
    return tuple(int(part) for part in match.groups()) if match else None


def installed_version() -> str | None:
    path = SKILL / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else None


def latest_version(timeout: float) -> str | None:
    request = urllib.request.Request(LATEST_API, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "macro-deck-plugin-dev-skill",
    })
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response).get("tag_name")
    except (OSError, ValueError):
        return None


def docs_date() -> dt.date | None:
    path = SKILL / "references" / "SOURCES.md"
    if not path.is_file():
        return None
    dates = re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", path.read_text(encoding="utf-8"))
    parsed = []
    for text in dates:
        try:
            parsed.append(dt.date.fromisoformat(text))
        except ValueError:
            pass
    return max(parsed, default=None)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--timeout", type=float, default=5.0, help="seconds to wait for GitHub")
    args = parser.parse_args()

    installed = installed_version()
    latest = latest_version(args.timeout)
    mine, theirs = parse_version(installed), parse_version(latest)

    if mine and theirs:
        if theirs > mine:
            print(f"UPDATE AVAILABLE: installed {installed}, latest {latest}. How to update: {UPDATE_HELP}")
            return 10
        print(f"up to date: {installed}")
        return 0

    if theirs and not mine:
        print(f"UPDATE AVAILABLE (probably): this copy has no release version, latest is {latest}. "
              f"How to update: {UPDATE_HELP}")
        return 10

    newest = docs_date()
    reason = "could not reach GitHub" if latest is None else f"unexpected latest tag {latest!r}"
    if newest is None:
        print(f"unknown: {reason}, and references/SOURCES.md has no dates")
        return 3

    age = (dt.date.today() - newest).days
    if age > STALE_DAYS:
        print(f"POSSIBLY OUTDATED: {reason}; the bundled docs are from {newest} ({age} days old). "
              f"How to update: {UPDATE_HELP}")
        return 11

    print(f"probably current: {reason}; the bundled docs are from {newest} ({age} days old)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
