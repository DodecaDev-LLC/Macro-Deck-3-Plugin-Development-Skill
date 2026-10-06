#!/usr/bin/env python3
"""Mechanical Store-gate checks for a Macro Deck 3 plugin, before a release.

Checks what a script can check against the live Macro Deck Store policy:
  1. manifest.json carries the publication fields, with real (non-placeholder) values
  2. every MacroDeck.* package in the dependency graph is on the allow-list
  3. every MacroDeck.* package is at least the Store's minimumSdkVersion
  4. no package in the full (transitive) graph is on the blocked list

It does not replace reading the Creator Guidelines, which it fetches and points you to, and it does not run
the conformance suite (use `macrodeck-plugin test`).

Usage (from the plugin's solution directory):
  python3 store_gate.py --project src/MyPlugin
  python3 store_gate.py --project src/MyPlugin --packages-json packages.json   # skip running dotnet
  python3 store_gate.py --project src/MyPlugin --json                          # machine-readable result
  python3 store_gate.py --project src/MyPlugin --sdk-policy sdk.json --blocked-policy blocked.json
      # when this machine cannot reach api.macro-deck.app: save the two JSON documents some other way
      # (a browser, a web-fetch tool) and pass them; the guidelines must then be read separately

`--packages-json` takes the output of
  dotnet list <csproj> package --include-transitive --format json
which is what the script runs itself when dotnet is on PATH.

Exit codes: 0 every check passed, 1 at least one check failed, 2 usage error, 3 policy could not be fetched.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

API = "https://api.macro-deck.app/api/v1/public"
POLICY_URLS = {
    "guidelines": f"{API}/creator-guidelines",
    "blocked": f"{API}/dependency-policy/blocked-packages",
    "sdk": f"{API}/dependency-policy/sdk",
}
PLACEHOLDER_PUBLISHERS = {"example publisher", "example", "your name", "publisher"}
PLACEHOLDER_REPOS = {"https://github.com/example/my-plugin"}
GITHUB_REPO = re.compile(r"^https://github\.com/[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
PUBLICATION_FIELDS = ["description", "icon", "publisher", "license", "repository", "compatibility"]


@dataclass
class Report:
    checks: list[dict] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str) -> None:
        self.checks.append({"check": name, "status": status, "detail": detail})

    @property
    def failed(self) -> bool:
        return any(c["status"] == "fail" for c in self.checks)


def fetch(url: str) -> tuple[str, dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": "macro-deck-plugin-dev-skill/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8"), dict(response.headers)


# SemVer 2.0 precedence, enough for MacroDeck package versions such as 3.0.0-beta.15.
def semver_key(version: str):
    core, _, pre = version.split("+", 1)[0].partition("-")
    nums = [int(p) if p.isdigit() else 0 for p in core.split(".")[:3]]
    nums += [0] * (3 - len(nums))
    if not pre:
        return (*nums, 1, ())
    ids = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split("."))
    return (*nums, 0, ids)


def semver_lt(a: str, b: str) -> bool:
    return semver_key(a) < semver_key(b)


def older_release_line(version: str, minimum: str) -> bool:
    """Macro Deck 3 shipped `preview.N` builds before the `beta.N` line. SemVer sorts `preview` above
    `beta`, so a preview build passes a plain comparison against a beta minimum while being older."""
    pre = version.partition("-")[2].lower()
    minimum_pre = minimum.partition("-")[2].lower()
    same_core = version.partition("-")[0] == minimum.partition("-")[0]
    return same_core and pre.startswith("preview") and minimum_pre.startswith("beta")


def pattern_matches(pattern: str, value: str) -> bool:
    """The policy does not document its pattern syntax; accept exact, glob and anchored regex forms."""
    if pattern.lower() == value.lower():
        return True
    if pattern.startswith("^") or pattern.endswith("$"):
        try:
            return re.search(pattern, value, re.IGNORECASE) is not None
        except re.error:
            return False
    return fnmatch.fnmatch(value.lower(), pattern.lower())


def version_matches(pattern: str | None, version: str) -> bool:
    if pattern is None:
        return True
    interval = re.fullmatch(r"([\[(])\s*([^,]*)\s*,\s*([^\])]*)\s*([\])])", pattern.strip())
    if interval:  # NuGet interval notation, e.g. [1.0.0, 2.0.0)
        lo_inc, lo, hi, hi_inc = interval.groups()
        if lo and (semver_lt(version, lo) or (lo_inc == "(" and version == lo)):
            return False
        if hi and (semver_lt(hi, version) or (hi_inc == ")" and version == hi)):
            return False
        return True
    return pattern_matches(pattern, version)


def find_project(path: Path) -> tuple[Path, Path]:
    """Return (csproj, manifest) for a project path given as a directory or a .csproj."""
    if path.is_file() and path.suffix == ".csproj":
        return path, path.parent / "manifest.json"
    if path.is_dir():
        projects = sorted(path.glob("*.csproj"))
        if len(projects) == 1:
            return projects[0], path / "manifest.json"
        if not projects:
            sys.exit(f"error: no .csproj in {path}")
        sys.exit(f"error: several .csproj in {path}; pass one with --project")
    sys.exit(f"error: {path} is neither a directory nor a .csproj")


def check_manifest(manifest_path: Path, report: Report) -> None:
    if not manifest_path.is_file():
        report.add("manifest", "fail", f"no manifest.json next to the project ({manifest_path})")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    missing = [f for f in PUBLICATION_FIELDS if not manifest.get(f)]
    report.add("publication fields", "fail" if missing else "pass",
               f"missing: {', '.join(missing)}" if missing else "description, icon, publisher, license, repository, compatibility set")

    publisher = (manifest.get("publisher") or {}).get("name", "")
    if not publisher or publisher.strip().lower() in PLACEHOLDER_PUBLISHERS:
        report.add("publisher.name", "fail", f"'{publisher}' is empty or a template placeholder; it must be the Creator Portal owner")
    else:
        report.add("publisher.name", "manual", f"'{publisher}': confirm it equals the Creator Portal Organization name or personal username")

    license_ = manifest.get("license", "")
    if not license_ or len(license_) > 64:
        report.add("license", "fail", "set an SPDX identifier (at most 64 characters), e.g. MIT")
    else:
        report.add("license", "pass", license_)

    repo = manifest.get("repository", "")
    if repo in PLACEHOLDER_REPOS or not GITHUB_REPO.match(repo or ""):
        report.add("repository", "fail", f"'{repo}' must be the real https://github.com/<owner>/<name> the plugin is released from")
    else:
        report.add("repository", "pass", repo)

    plugin_id = manifest.get("id", "")
    if re.search(r"macro-?deck", plugin_id, re.IGNORECASE):
        report.add("id branding", "fail", f"'{plugin_id}' contains 'Macro Deck'; the guidelines forbid it in package ids")
    else:
        report.add("id branding", "manual", f"'{plugin_id}': confirm it uses no third-party brand as the namespace")

    if "ai" not in manifest:
        report.add("ai declaration", "warn", "no 'ai' block: the Store will say AI use is not declared. Add one, all false if unused")
    else:
        report.add("ai declaration", "pass", json.dumps(manifest["ai"]))

    entrypoints = sorted((manifest.get("entrypoints") or {}).keys())
    build_recipe = manifest_path.parent / "macrodeck-build.json"
    if build_recipe.is_file():
        targets = sorted((json.loads(build_recipe.read_text(encoding="utf-8")).get("targets") or {}).keys())
        mismatch = sorted(set(entrypoints) ^ set(targets))
        report.add("entrypoints vs build targets", "fail" if mismatch else "pass",
                   f"out of step: {', '.join(mismatch)}" if mismatch else ", ".join(entrypoints))
    report.add("conformance per platform", "manual",
               f"run `macrodeck-plugin test` and keep the publishing workflow's stub-host run for: {', '.join(entrypoints) or 'no entrypoints'}")


def load_packages(csproj: Path, packages_json: Path | None, report: Report) -> list[tuple[str, str]] | None:
    if packages_json:
        data = json.loads(packages_json.read_text(encoding="utf-8"))
    else:
        if not shutil.which("dotnet"):
            report.add("dependency graph", "manual",
                       "dotnet not on PATH: run `dotnet list <csproj> package --include-transitive --format json > packages.json` and pass --packages-json")
            return None
        result = subprocess.run(["dotnet", "list", str(csproj), "package", "--include-transitive", "--format", "json"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            report.add("dependency graph", "fail", f"`dotnet list package` failed (restore first?): {result.stderr.strip()[:400]}")
            return None
        data = json.loads(result.stdout)

    packages = set()
    for project in data.get("projects", []):
        for framework in project.get("frameworks", []):
            for key in ("topLevelPackages", "transitivePackages"):
                for pkg in framework.get(key, []):
                    packages.add((pkg["id"], pkg.get("resolvedVersion") or pkg.get("requestedVersion", "")))
    return sorted(packages)


def check_packages(packages: list[tuple[str, str]], sdk_policy: dict, blocked_policy: dict, report: Report) -> None:
    allowed = {p.lower() for p in sdk_policy.get("allowedMacroDeckPackages", [])}
    minimum = sdk_policy.get("minimumSdkVersion")
    macrodeck = [(i, v) for i, v in packages if i.lower().startswith("macrodeck.")]

    not_allowed = [f"{i} {v}" for i, v in macrodeck if i.lower() not in allowed]
    report.add("allowed MacroDeck.* packages", "fail" if not_allowed else "pass",
               f"not allowed: {', '.join(not_allowed)}" if not_allowed else f"{len(macrodeck)} MacroDeck.* packages, all allowed")

    if minimum:
        too_old = [f"{i} {v}" for i, v in macrodeck
                   if v and (semver_lt(v, minimum) or older_release_line(v, minimum))]
        report.add("minimum SDK version", "fail" if too_old else "pass",
                   f"older than {minimum}: {', '.join(too_old)}" if too_old else f"all at or above {minimum}")

    hits = []
    for entry in blocked_policy.get("blockedPackages", []):
        pattern = entry.get("packagePattern", "")
        for pkg_id, version in packages:
            if pattern_matches(pattern, pkg_id) and version_matches(entry.get("versionPattern"), version):
                hits.append(f"{pkg_id} {version} ({entry.get('reason') or 'no reason given'})")
    report.add("blocked packages", "fail" if hits else "pass",
               f"blocked: {'; '.join(hits)}" if hits else f"none of {len(packages)} packages is blocked "
               f"({len(blocked_policy.get('blockedPackages', []))} block rules)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True, help="plugin project directory or .csproj")
    parser.add_argument("--packages-json", type=Path, help="output of `dotnet list package --include-transitive --format json`")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--sdk-policy", type=Path, help="saved copy of dependency-policy/sdk, fetched today")
    parser.add_argument("--blocked-policy", type=Path, help="saved copy of dependency-policy/blocked-packages, fetched today")
    args = parser.parse_args()

    csproj, manifest = find_project(args.project.resolve())
    report = Report()

    if bool(args.sdk_policy) != bool(args.blocked_policy):
        parser.error("--sdk-policy and --blocked-policy go together")

    try:
        if args.sdk_policy:
            sdk_policy = json.loads(args.sdk_policy.read_text(encoding="utf-8"))
            blocked_policy = json.loads(args.blocked_policy.read_text(encoding="utf-8"))
            version = "not fetched"
            report.add("creator guidelines", "manual",
                       f"policy read from files; fetch and read the guidelines yourself: {POLICY_URLS['guidelines']}")
        else:
            guidelines, headers = fetch(POLICY_URLS["guidelines"])
            sdk_policy = json.loads(fetch(POLICY_URLS["sdk"])[0])
            blocked_policy = json.loads(fetch(POLICY_URLS["blocked"])[0])
            version = headers.get("X-Creator-Guidelines-Version", "not stated")
            report.add("creator guidelines", "manual",
                       f"version {version}, {len(guidelines)} characters: read all of it at {POLICY_URLS['guidelines']}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as error:
        print(f"error: could not get the Store policy ({error}). Do not assume it is unchanged; fetch "
              "dependency-policy/sdk and dependency-policy/blocked-packages another way and pass them with "
              "--sdk-policy/--blocked-policy, or stop.", file=sys.stderr)
        sys.exit(3)

    check_manifest(manifest, report)
    packages = load_packages(csproj, args.packages_json, report)
    if packages is not None:
        check_packages(packages, sdk_policy, blocked_policy, report)

    if args.json:
        print(json.dumps({"policy": sdk_policy, "guidelinesVersion": version, "checks": report.checks}, indent=2))
    else:
        print(f"Store policy: minimum SDK {sdk_policy.get('minimumSdkVersion')}, minimum CLI {sdk_policy.get('minimumCliVersion')}, "
              f"guidelines version {version}\n")
        width = max(len(c["check"]) for c in report.checks)
        for c in report.checks:
            print(f"[{c['status'].upper():6}] {c['check']:<{width}}  {c['detail']}")
        print("\nRESULT:", "FAIL" if report.failed else "no automatic failures; finish the MANUAL items")
    sys.exit(1 if report.failed else 0)


if __name__ == "__main__":
    main()
