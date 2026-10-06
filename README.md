# Macro Deck 3 plugin development skill

An [Agent Skill](https://support.claude.com/en/articles/12512176-what-are-skills) that makes Claude effective at
building, extending, debugging, testing, packaging and publishing **Macro Deck 3** plugins. It covers v3 and
later only; Macro Deck 2 plugins are out of scope.

It bundles the official plugin documentation from [docs.macro-deck.app](https://docs.macro-deck.app), the
[plugin template](https://github.com/Macro-Deck-App/Macro-Deck-Plugin-Template) and the
[sample plugins](https://github.com/Macro-Deck-App/Macro-Deck-Sample-Plugins), plus a hand-written cheatsheet and
two scripts. A GitHub Action refreshes the bundle from those repositories every day and publishes a new release
when anything changed.

This is a community project, not an official Macro Deck project.

## Install

Download `macro-deck-plugin-dev.zip` from the [latest release](https://github.com/DodecaDev-LLC/Macro-Deck-3-Plugin-Development-Skill/releases/latest).

- **Claude (web, desktop, mobile):** Customize > Skills > **+** > Create skill > Upload a skill, choose the zip,
  and make sure the skill is toggled on. On Free, Pro and Max plans, Settings > Capabilities > *Code execution
  and file creation* must be on. On Team and Enterprise plans you can then share it from the skill's **...**
  menu or publish it to your organization.
- **Claude Code:** unzip into `~/.claude/skills/` (every project) or into a project's `.claude/skills/`
  (that project, shared through git).

Then just ask, for example: *"Scaffold a Macro Deck plugin that controls my Hue lights"*, *"Add a webhook
action to my plugin"*, or *"Why does my plugin never get a pairing prompt?"*.

## What's inside

```
macro-deck-plugin-dev/
  SKILL.md                    workflows, the rules that matter most, verification, versions, Store gate
  references/
    cheatsheet.md             code shapes for every common capability
    agent-rules.md            the template's official agent rulebook
    INDEX.md                  every docs page, which file holds it, and its live URL
    docs/*.md                 the plugin docs, merged into ten topic files
    template.md               the plugin template's files
    samples/*.md              the four sample plugins with their tests
    licenses/                 upstream LICENSE and NOTICE files
    SOURCES.md                upstream commits this copy reflects
  scripts/
    sync_docs.py              regenerate references/ from the upstream repositories
    store_gate.py             check a plugin against the Store's live publishing policy
scripts/build_release.py      validate upload limits and build the release zip
evals/evals.json              test prompts used to evaluate the skill
```

## How the daily update works

`.github/workflows/sync-and-release.yml` runs every day at 11:17 UTC, on manual dispatch, and on pushes that
change the skill:

1. `sync_docs.py` clones the three Macro Deck repositories and regenerates `macro-deck-plugin-dev/references/`.
2. If nothing but the upstream commit ids changed, it stops: no commit, no release.
3. Otherwise `build_release.py` checks the claude.ai limits (description at most 200 characters, under 30 MB)
   and builds the zip, the workflow commits the refreshed references, and publishes a release tagged
   `vYYYY.MM.DD.<run>` with the zip attached.

Run **Actions > Sync docs and release > Run workflow** with *force release* to publish without an upstream
change. To work locally:

```bash
python3 macro-deck-plugin-dev/scripts/sync_docs.py   # refresh references (needs git and network)
python3 scripts/build_release.py                      # validate and build dist/
```

## Licences

The bundled Macro Deck documentation is licensed under the Apache License 2.0 and the template and samples
under the MIT License, both Copyright (c) Macro Deck Contributors. Their licence texts and Macro Deck's NOTICE
ship inside the skill in `references/licenses/`, and `references/SOURCES.md` describes what was changed. The
Macro Deck name and branding belong to their owners and are used here only to say what the skill is for.
