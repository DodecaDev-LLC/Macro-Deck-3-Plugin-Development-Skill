#!/usr/bin/env python3
"""Regenerate this skill's bundled references from the official Macro Deck 3 sources.

Pulls (or reuses local clones of) three public repositories:
  - Macro-Deck-App/Macro-Deck                 docs/src/content/docs  -> references/docs/<group>.md
  - Macro-Deck-App/Macro-Deck-Plugin-Template  src/, tests/, props    -> references/template.md
  - Macro-Deck-App/Macro-Deck-Sample-Plugins   src/, tests/, README   -> references/samples/<sample>.md

Pages are merged into a handful of files on purpose: claude.ai skill uploads work best with few files, and
one file per topic group is still easy to grep. It also writes references/INDEX.md (which page lives in
which file), references/SOURCES.md, and the upstream licence files under references/licenses/.

Only plugin-development docs are kept. The end-user "guide/" section and the site landing page are
skipped, because they describe using Macro Deck rather than building for it.

Usage:
  python3 scripts/sync_docs.py                    # clone fresh into a temp dir (needs git + network)
  python3 scripts/sync_docs.py --src /path/clones # reuse clones named after the repositories
Exit code 0 always means the references were written; compare with git to see whether anything changed.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS_SITE = "https://docs.macro-deck.app"
REPOS = {
    "macrodeck": "Macro-Deck",
    "template": "Macro-Deck-Plugin-Template",
    "samples": "Macro-Deck-Sample-Plugins",
}

# Output file -> (title, docs subpaths it collects). Order is reading order.
GROUPS = [
    ("introduction", "Get started", ["introduction"]),
    ("features", "Features (capabilities)", ["features"]),
    ("ui", "Macro Deck UI: overview, concepts and reference", ["ui/index.md", "ui/concepts", "ui/reference"]),
    ("ui-views", "Macro Deck UI: views and surfaces", ["ui/views"]),
    ("ui-components", "Macro Deck UI: components", ["ui/components"]),
    ("cli", "Plugin CLI", ["cli"]),
    ("guides", "Guides: debugging, publishing, troubleshooting", ["guides"]),
    ("reference", "Reference: SDK packages, hosting, manifest, protocol, auth, REST", ["reference"]),
    ("creator-portal", "Creator Portal: publishing to the Store", ["creator-portal"]),
    ("policies", "Policies: compatibility, deprecations, migrations, security", ["policies"]),
]

CODE_SUFFIXES = {".cs", ".json", ".resx", ".svg", ".csproj", ".props", ".targets", ".slnx", ".md", ".yml", ".config"}
SKIP_DIRS = {".git", "bin", "obj", "local-feed", ".template.config", "packaging", ".idea", ".vs", ".github"}
LANG = {".cs": "csharp", ".json": "json", ".resx": "xml", ".svg": "xml", ".csproj": "xml", ".props": "xml",
        ".targets": "xml", ".slnx": "xml", ".md": "markdown", ".yml": "yaml", ".config": "xml"}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"\]\((/[^)\s]*)\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
HEADING = re.compile(r"^(#{1,5}) ", re.M)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def clone_all(dest: Path) -> dict[str, Path]:
    paths = {}
    for key, repo in REPOS.items():
        target = dest / repo
        url = f"https://github.com/Macro-Deck-App/{repo}.git"
        if key == "macrodeck":
            run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", url, str(target)])
            run(["git", "sparse-checkout", "set", "--no-cone", "/docs/src/content/docs/", "/LICENSE", "/NOTICE"], cwd=target)
        else:
            run(["git", "clone", "-q", "--depth", "1", url, str(target)])
        paths[key] = target
    return paths


def locate(src: Path) -> dict[str, Path]:
    paths = {}
    for key, repo in REPOS.items():
        found = next((c for c in (src / repo, src / key) if c.is_dir()), None)
        if found is None:
            sys.exit(f"error: no clone of {repo} under {src} (expected {src / repo})")
        paths[key] = found
    return paths


def read_repo_file(repo: Path, name: str) -> str | None:
    path = repo / name
    if path.is_file():
        return path.read_text(encoding="utf-8")
    try:
        return subprocess.run(["git", "show", f"HEAD:{name}"], cwd=repo, check=True,
                              capture_output=True, text=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[match.end():]


def demote(body: str) -> str:
    """Pages become sections of a bigger file: the page title is H2, so page headings move down one level.
    Lines inside fenced code blocks are left alone."""
    out, fenced = [], False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and HEADING.match(line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def page_url(rel: Path) -> str:
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "index":
        parts = parts[:-1]
    return f"{DOCS_SITE}/{'/'.join(parts)}/"


def pages_for(docs_root: Path, subpaths: list[str]) -> list[Path]:
    pages = []
    for sub in subpaths:
        target = docs_root / sub
        if target.is_file():
            pages.append(target)
        elif target.is_dir():
            found = sorted(target.rglob("*.md*"))
            # A section's landing page reads best first.
            pages += sorted(found, key=lambda p: (p.parent != target or p.stem != "index", str(p)))
    return pages


def sync_docs(docs_root: Path, out: Path) -> list[tuple[str, str, str, str]]:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    index = []
    for name, title, subpaths in GROUPS:
        pages = pages_for(docs_root, subpaths)
        toc, sections = [], []
        for path in pages:
            rel = path.relative_to(docs_root)
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            page_title = meta.get("title", rel.stem)
            description = meta.get("description", "")
            body = LINK.sub(lambda m: f"]({DOCS_SITE}{m.group(1)})", IMAGE.sub(lambda m: f"*[Image: {m.group(1)}]*", body))
            url = page_url(rel)
            toc.append(f"- {page_title}: {url}")
            header = f"## {page_title}\n\n> Source: {url}\n"
            if description:
                header += f">\n> {description}\n"
            sections.append(header + "\n" + demote(body.strip("\n")) + "\n")
            index.append((f"docs/{name}.md", page_title, description, url))
        text = (f"# {title}\n\nPages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an "
                f"`## <Page title>` section with its source URL. Grep for a type or heading to jump to it.\n\n"
                f"Contents:\n\n" + "\n".join(toc) + "\n\n" + "\n".join(sections))
        (out / f"{name}.md").write_text(text, encoding="utf-8")
    return index


def collect(src: Path, roots: list[str]) -> list[Path]:
    files = []
    for root in roots:
        base = src / root
        items = [base] if base.is_file() else sorted(base.rglob("*")) if base.is_dir() else []
        for item in items:
            rel = item.relative_to(src)
            if not item.is_file() or any(p in SKIP_DIRS for p in rel.parts):
                continue
            if item.suffix in CODE_SUFFIXES or item.name == ".gitignore":
                files.append(item)
    return files


def bundle(src: Path, files: list[Path], title: str, intro: str) -> str:
    listing = "\n".join(f"- `{f.relative_to(src).as_posix()}`" for f in files)
    parts = [f"# {title}\n\n{intro}\n\nFiles:\n\n{listing}\n"]
    for f in files:
        rel = f.relative_to(src).as_posix()
        body = f.read_text(encoding="utf-8", errors="replace").rstrip()
        fence = "````" if "```" in body else "```"
        parts.append(f"\n## File: {rel}\n\n{fence}{LANG.get(f.suffix, '')}\n{body}\n{fence}\n")
    return "".join(parts)


def sync_template(src: Path, refs: Path) -> int:
    files = collect(src, ["src", "tests", "Directory.Build.props", "Directory.Packages.props", "NuGet.config",
                          ".gitignore", "README.md"])
    intro = ("The official Macro Deck 3 plugin template (what `macrodeck-plugin new` / `dotnet new macrodeck-plugin` "
             "generates), one `## File: <path>` section per file. To write a project by hand, recreate these files and "
             "rename `MacroDeck.PluginTemplate` everywhere (project, namespace, `AssemblyName`, manifest entrypoints). "
             "The template's agent rulebook is in `references/agent-rules.md`.")
    (refs / "template.md").write_text(bundle(src, files, "Plugin template", intro), encoding="utf-8")
    rules = read_repo_file(src, "AGENTS.md")
    if rules:
        (refs / "agent-rules.md").write_text(
            "<!-- AGENTS.md from Macro-Deck-App/Macro-Deck-Plugin-Template, the official rulebook for agents writing "
            "Macro Deck 3 plugins. Its Workflow section is about the template repository itself. -->\n\n" + rules,
            encoding="utf-8")
    return len(files)


def sync_samples(src: Path, refs: Path) -> int:
    out = refs / "samples"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    count = 0
    readme = read_repo_file(src, "README.md")
    if readme:
        (out / "README.md").write_text(readme, encoding="utf-8")
        count += 1
    for sample in sorted((src / "src").iterdir()):
        if not sample.is_dir():
            continue
        name = sample.name
        files = collect(src, [f"src/{name}"])
        tests = src / "tests" / f"{name}.Tests"
        if tests.is_dir():
            files += collect(src, [f"tests/{name}.Tests"])
        short = name.removeprefix("MacroDeck.").removeprefix("Sample").removesuffix("Plugin").lower() or name.lower()
        intro = (f"The `{name}` sample plugin and its tests, one `## File: <path>` section per file. "
                 "See `samples/README.md` for what each sample demonstrates.")
        (out / f"{short}.md").write_text(bundle(src, files, f"Sample: {name}", intro), encoding="utf-8")
        count += len(files)
    return count


def copy_licenses(paths: dict[str, Path], refs: Path) -> None:
    out = refs / "licenses"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for key, repo in REPOS.items():
        for name in ("LICENSE", "NOTICE"):
            text = read_repo_file(paths[key], name)
            if text:
                (out / f"{repo}-{name}.txt").write_text(text, encoding="utf-8")


def write_index(refs: Path, index) -> None:
    lines = [
        "# Macro Deck 3 plugin docs index",
        "",
        "Every plugin-development page of docs.macro-deck.app, merged into topic files under `references/docs/`.",
        "Each page is an `## <Page title>` section of the file shown, with its live URL. Links inside the pages",
        "point at the live site; to read one locally, find its URL in this table.",
        "",
        "Search everything: `grep -rn \"<Type or term>\" references/`.",
        "",
        "| File | Page | What it covers | Live URL |",
        "| --- | --- | --- | --- |",
    ]
    for file, title, description, url in index:
        lines.append(f"| `{file}` | {title} | {description.replace('|', '/')} | {url} |")
    (refs / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def commit_of(repo: Path) -> str:
    try:
        return run(["git", "log", "-1", "--format=%h %cs"], cwd=repo)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def write_sources(refs: Path, paths: dict[str, Path], counts: dict[str, int]) -> None:
    rows = {"macrodeck": ("references/docs/", "Apache-2.0"),
            "template": ("references/template.md, references/agent-rules.md", "MIT"),
            "samples": ("references/samples/", "MIT")}
    lines = ["# Sources of the bundled references", "",
             "Generated by `scripts/sync_docs.py`. The commit column says which upstream version this copy reflects.", "",
             "| Bundled as | Repository | Commit | Upstream files | Licence |", "| --- | --- | --- | --- | --- |"]
    for key, repo in REPOS.items():
        where, licence = rows[key]
        lines.append(f"| {where} | https://github.com/Macro-Deck-App/{repo} | {commit_of(paths[key])} | {counts[key]} | {licence} |")
    lines += [
        "",
        "## Licences and changes",
        "",
        "The documentation is Copyright (c) Macro Deck Contributors, licensed under the Apache License 2.0; the template",
        "and samples are Copyright (c) Macro Deck Contributors under the MIT License. The full texts and Macro Deck's",
        "NOTICE are in `references/licenses/`. The Macro Deck name and branding are not covered by those licences;",
        "this skill uses the name only to describe what it is for and is not an official Macro Deck project.",
        "",
        "Changes made to the upstream files: the documentation's front matter is turned into a heading and a source",
        "line, headings are moved down one level, pages are merged into topic files, site-relative links are made",
        "absolute and images are replaced by their alt text. Template and sample files are copied unmodified into",
        "Markdown bundles. When this copy and the live site disagree, the live site wins.",
        "",
    ]
    (refs / "SOURCES.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", type=Path, help="directory holding existing clones of the three repositories")
    parser.add_argument("--skill", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="skill root to write into (default: this script's skill)")
    args = parser.parse_args()

    tmp = None
    if args.src:
        paths = locate(args.src.resolve())
    else:
        tmp = Path(tempfile.mkdtemp(prefix="macrodeck-sync-"))
        paths = clone_all(tmp)

    try:
        refs = args.skill / "references"
        refs.mkdir(parents=True, exist_ok=True)
        # Remove the older one-file-per-page layout if present.
        for stale in ("template",):
            if (refs / stale).is_dir():
                shutil.rmtree(refs / stale)
        index = sync_docs(paths["macrodeck"] / "docs/src/content/docs", refs / "docs")
        template = sync_template(paths["template"], refs)
        samples = sync_samples(paths["samples"], refs)
        copy_licenses(paths, refs)
        write_index(refs, index)
        write_sources(refs, paths, {"macrodeck": len(index), "template": template, "samples": samples})
        print(f"docs: {len(index)} pages in {len(GROUPS)} files, template: {template} files, samples: {samples} files")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
