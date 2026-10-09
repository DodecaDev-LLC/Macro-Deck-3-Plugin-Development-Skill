# Plugin CLI

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Plugin CLI: https://docs.macro-deck.app/cli/
- macrodeck-plugin build: https://docs.macro-deck.app/cli/build/
- CI and automation: https://docs.macro-deck.app/cli/ci/
- macrodeck-plugin icon-pack: https://docs.macro-deck.app/cli/icon-pack/
- macrodeck-plugin inspect: https://docs.macro-deck.app/cli/inspect/
- macrodeck-plugin merge: https://docs.macro-deck.app/cli/merge/
- macrodeck-plugin new: https://docs.macro-deck.app/cli/new/
- macrodeck-plugin pack: https://docs.macro-deck.app/cli/pack/
- macrodeck-plugin preview: https://docs.macro-deck.app/cli/preview/
- macrodeck-plugin run: https://docs.macro-deck.app/cli/run/
- Signing packages: https://docs.macro-deck.app/cli/signing/
- macrodeck-plugin test: https://docs.macro-deck.app/cli/test/
- macrodeck-plugin validate: https://docs.macro-deck.app/cli/validate/

## Plugin CLI

> Source: https://docs.macro-deck.app/cli/
>
> macrodeck-plugin: scaffold, build, validate, inspect, pack, merge, bundle icon packs, run, preview, test and sign a Macro Deck plugin without installing a host.

`macrodeck-plugin` scaffolds, builds, checks, runs and packages a Macro Deck plugin without Macro Deck
installed.

### Installing

```bash
dotnet tool install --global MacroDeck.Plugin.Cli --prerelease
```

- `--prerelease` is required until a stable 3.0 build ships: only prerelease versions are published, and
  `dotnet tool install` skips them unless asked.
- It does not install the newest one today. SemVer orders `beta` before `preview`, so `--prerelease`
  resolves to `3.0.0-preview.10` while the newest release is `3.0.0-beta.11`. Commands added since
  `preview.10`, [`merge`](https://docs.macro-deck.app/cli/merge/) among them, need it by name:
  `dotnet tool install --global MacroDeck.Plugin.Cli --version 3.0.0-beta.11`.
- The tool needs the **ASP.NET Core shared framework**, not just the .NET runtime, because `run` and
  `test` start a real Kestrel loopback host (via
  [`MacroDeck.Plugin.Testing`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/sdk/src/MacroDeck.Plugin.Testing/README.md)).
  If they report that `Microsoft.AspNetCore.App` is missing, install the ASP.NET Core runtime or SDK.

### Typical workflow

```bash
macrodeck-plugin new --name "Spotify Controller" --publisher "Example Publisher" --yes
cd SpotifyController/src/SpotifyController
macrodeck-plugin run --project SpotifyController.csproj --stub-host
macrodeck-plugin build --output ../../artifacts
macrodeck-plugin validate --artifact ../../artifacts/com.example.spotify-controller-1.0.0.macroDeckPlugin
```

The artifact `build` (or `pack`) produces is what your publishing workflow submits to the Creator Portal,
which signs it - see [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/). There is no `keygen` or `sign` step on
the way to the Store: those commands are for artifacts distributed outside the Store and for Macro Deck's
own infrastructure.

### Commands

| Command | What it does |
| --- | --- |
| [`new`](https://docs.macro-deck.app/cli/new/) | Scaffold a plugin project from the official template. |
| [`build`](https://docs.macro-deck.app/cli/build/) | Build every runtime identifier the manifest declares and package the result. |
| [`validate`](https://docs.macro-deck.app/cli/validate/) | Validate a manifest, a version directory or a packed artifact. |
| [`inspect`](https://docs.macro-deck.app/cli/inspect/) | Report what installing an artifact would find, without a running host. |
| [`pack`](https://docs.macro-deck.app/cli/pack/) | Pack an existing payload directory into a `.macroDeckPlugin` artifact. |
| [`merge`](https://docs.macro-deck.app/cli/merge/) | Merge packages built for different runtime identifiers into one package. |
| [`icon-pack`](https://docs.macro-deck.app/cli/icon-pack/) | Bundle icon packs with the plugin project, list them and remove them. |
| [`run`](https://docs.macro-deck.app/cli/run/) | Run a plugin against the running host or a disposable stub host. |
| [`preview`](https://docs.macro-deck.app/cli/preview/) | Render a plugin's widget previews to PNG files, for store images. |
| [`test`](https://docs.macro-deck.app/cli/test/) | Run the [conformance suite](https://docs.macro-deck.app/reference/conformance/) and write a text, JSON or Markdown report. |
| [`keygen` / `sign` / `verify`](https://docs.macro-deck.app/cli/signing/) | Creator key pairs and package signatures, for artifacts distributed outside the Store. |

Run `macrodeck-plugin <command> --help` for a command's options.

### Global options

These work on every command, before or after the command name:

| Option | Default | Description |
| --- | --- | --- |
| `--verbosity <quiet\|normal\|diagnostic>` | `normal` | How much a command narrates while it works. |
| `--no-color` | off | Disable ANSI colour in text output. |

`quiet` hides progress lines only. A command's result - a validation report, a conformance report, a
plugin's own console output, any `error` or `warning` line - always prints.

`--output` is not global. `validate`, `inspect` and `icon-pack list` use it for a render format (`text`/`json`), `pack` and
`test` for a destination file, and `new`, `build`, `merge` and `keygen` for a destination directory.

### Errors and warnings

```text
$ macrodeck-plugin build
error manifest-not-found: No manifest at '~/src/SpotifyController/manifest.json'.
```

- Failures print one line on **stderr**: `error <kebab-case-code>: <sentence>`, red unless `--no-color`
  is given.
- Non-fatal observations (a missing foreign-RID entrypoint, a Debug-looking source tree, missing
  publication metadata) print the same way as `warning <code>: <sentence>`, also on stderr. A warning
  **never changes the exit code**.
- `validate` is the exception: its `error`/`warning` lines are its result, so they go to **stdout** and
  `validate ... > report.txt` captures them.
- Paths in messages are always resolved and absolute.

Running with no arguments prints the command list (exit 2). A mistyped command gets a suggestion when one
command name is close, otherwise a pointer to `--help`:

```text
$ macrodeck-plugin pakc --source .
error unknown-command: 'pakc' is not a macrodeck-plugin command. Did you mean 'pack'?
```

### Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success, or conformant. |
| 1 | The subject is wrong: validation failed, or a required conformance check failed. |
| 2 | Usage error: bad arguments, an unknown `--check`/`--category` token, or an output file that already exists without `--force`. |
| 3 | The input could not be read: a missing file, something that is not a ZIP, or a permissions failure. |
| 4 | Cancelled (Ctrl-C). |
| 70 | An error the command did not anticipate. |

1 and 3 are kept apart so CI can tell a broken plugin from a broken environment. [`run`](https://docs.macro-deck.app/cli/run/) is
the one exception on a normal exit: it returns the launched plugin's own exit code.

### See also

- [Testing plugins](https://docs.macro-deck.app/features/testing/) - `MacroDeck.Plugin.Testing`, which `run` and `test` are built on.
- [Conformance](https://docs.macro-deck.app/reference/conformance/) - the suite `test` runs and its report shape.
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - the artifact format `pack`/`validate`/`inspect` read, and
  what the supervisor injects that `run` reproduces.
- [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/) - how a plugin is published and signed.
- [Security model](https://docs.macro-deck.app/policies/security/) - the trust model `verify` checks against.
- [`MacroDeck.Signing` package README](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/sdk/src/MacroDeck.Signing/README.md) -
  the library behind `sign` and `verify`.
- Certificate schema ([v1](https://docs.macro-deck.app/schemas/macrodeck-certificate-v1.schema.json),
  [v2](https://docs.macro-deck.app/schemas/macrodeck-certificate-v2.schema.json)) and
  [package signature schema](https://docs.macro-deck.app/schemas/macrodeck-package-signature-v1.schema.json).
- [`MacroDeck.Plugin.Cli` package README](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/sdk/src/MacroDeck.Plugin.Cli/README.md).

## macrodeck-plugin build

> Source: https://docs.macro-deck.app/cli/build/
>
> Build every runtime identifier the manifest declares, stage them into one payload, and package the result.

`build` builds every runtime identifier your manifest declares and packages the result into one
`.macroDeckPlugin`, using the same packer as [`pack`](https://docs.macro-deck.app/cli/pack/).

### Examples

```bash
cd ~/src/SpotifyController/src/SpotifyController
macrodeck-plugin build --output ../../artifacts
```

```text
Building linux-x64...
Building osx-arm64...
Building win-x64...
Built linux-x64, osx-arm64, win-x64.
Packed com.example.spotify-controller 1.0.0 -> ../../artifacts/com.example.spotify-controller-1.0.0.macroDeckPlugin (1041 entries, 342566393 bytes uncompressed).
```

A full multi-platform package. Run it from the directory holding `manifest.json`.

```bash
macrodeck-plugin build --rid osx-arm64 --output ../../artifacts
```

```text
Building osx-arm64...
Built osx-arm64.
Packed com.example.spotify-controller 1.0.0 -> ../../artifacts/com.example.spotify-controller-1.0.0-osx-arm64.macroDeckPlugin (...).
```

One platform only. Use it in a CI matrix job.

```bash
macrodeck-plugin build --source src/SpotifyController --output artifacts --force
```

Build from the repository root and overwrite the previous artifact.

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--source <dir>` | `.` | The plugin project directory. |
| `--manifest <path>` | `<source>/manifest.json` | The manifest that decides which runtime identifiers to build. |
| `--build-config <path>` | `macrodeck-build.json` beside the manifest | The build recipe. |
| `--rid <rid>` | all declared | Build only this runtime identifier, which the manifest must declare. |
| `--output <dir>` | `.` | **Directory** for the artifact, unlike `pack --output`, which is a file path. |
| `--force` | off | Overwrite an existing artifact. |

The artifact is named `<id>-<version>.macroDeckPlugin`, or `<id>-<version>-<rid>.macroDeckPlugin` with
`--rid`.

### What gets built

`manifest.entrypoints` decides what to build; `macrodeck-build.json` decides how.

- A runtime identifier declared in the manifest without a matching target fails with
  `target-not-configured` - a declared platform is never skipped.
- Each target runs in turn: its `executable` with its `arguments` as a vector, never through a shell, so
  spaces, quotes or `$HOME` reach the tool exactly as written.
- The CLI does not know which platforms a machine can build. Every requested target is attempted, and a
  missing or failing toolchain is reported with the runtime identifier and the tool's stdout and stderr.
- Whether the output is Release or Debug is up to the recipe; the generated one publishes Release. (`pack`'s
  `source-looks-like-debug-build` warning cannot fire here, because `build` packs a temporary directory.)

### Staging layout

```text
manifest.json
runtimes/win-x64/MyPlugin.exe
runtimes/osx-arm64/MyPlugin
runtimes/linux-x64/MyPlugin
assets/icon.png
icon-packs/logos.macroDeckIconPack
```

```json
{
  "version": 1,
  "include": ["assets", "data/defaults.json"],
  "targets": { "...": {} }
}
```

- Each target's output is staged under the directory its entrypoint declares, so identically named macOS
  and Linux executables do not overwrite each other.
- Besides that output and `manifest.json`, the package holds only the file the manifest's `icon` names, the
  pack files its [`bundledIconPacks`](https://docs.macro-deck.app/reference/manifest/#bundled-icon-packs) declare, and whatever the
  recipe's `include` lists, each at its project-relative path. Bundled packs are listed in `files[]` like
  any other payload file, so the signature covers them.
- An `include` entry is a file or directory relative to the project root and must stay inside it; one that
  does not exist fails with `build-config-invalid`.
- Never packaged, not even inside an included directory: project and source files (`*.csproj`, `*.sln`,
  `*.cs`, `*.resx`, `Properties/`, dotfiles and the like), `macrodeck-build.json`, each target's `output`
  directory, the `--output` directory, `bin/`, `obj/`, `node_modules/` and any `.macroDeckPlugin` file.
- A declared path one of these rules drops is named in an `include-not-packaged` warning, and every other
  file beside the manifest that was left out in a `file-not-packaged` warning, so a forgotten asset never
  disappears silently.
- An `--output` directory inside the project, such as `.` or `./artifacts`, is safe to build into repeatedly.
- Staging happens in a temporary directory outside your project, removed when the command finishes.

### Entrypoint checks

Every requested runtime identifier must produce its declared entrypoint, or the build fails with
`entrypoint-missing` (where `pack` only warns). This catches a manifest declaring a Windows `.exe` while the
recipe produces a framework-dependent `.dll`.

A full build checks every declared runtime identifier; `--rid win-x64` checks only `win-x64`, so a matrix
job is not failed by platforms it never built.

### Single-platform artifacts

A `--rid` artifact's manifest declares only that runtime identifier, so it never claims platforms the job
did not produce. To get one package covering every platform from per-runner builds, combine them with
[`merge`](https://docs.macro-deck.app/cli/merge/).

### What build changes in the manifest

- **Never signs.** The package is unsigned, needs no key, and any `signature` and `files[]` in the project
  manifest are dropped. `files[]` is recomputed from the staged bytes. Signing is
  [`sign`](https://docs.macro-deck.app/cli/signing/#sign) or the Creator Portal.
- **Fills in `languages`.** [`languages`](https://docs.macro-deck.app/reference/manifest/#languages) is derived from
  `Localization/*.resx`: an unsuffixed `Strings.resx` counts as `en`, and each culture-suffixed sibling adds
  its BCP-47 tag. `pack` cannot do this, because its payload no longer contains the project tree. See
  [the localization guide](https://docs.macro-deck.app/features/localization/#the-manifest-languages-field).
- **Warns about publication readiness.** Every unsatisfied field at the `publication`
  [requirement level](https://docs.macro-deck.app/reference/manifest/#requirement-categories) (for example a missing `description` or
  `publisher`) is a `publication-metadata-missing` warning. It never fails the build, and there is no
  `--level` flag to turn it off.

### Exit codes

```text
$ macrodeck-plugin build --rid win-arm64
error rid-not-declared: The manifest does not declare 'win-arm64'. Declared runtime identifiers: linux-x64, osx-arm64, win-x64.
```

| Code | When |
| --- | --- |
| 0 | The artifact was written. |
| 1 | A build failed, or the manifest, build configuration or result does not match what the manifest declares. |
| 2 | A `--rid` the manifest does not declare, or an artifact that already exists without `--force`. |
| 3 | The source, the manifest, the build configuration or the build tool could not be found. |
| 4 | Cancelled (Ctrl-C). |
| 70 | Staging failed. |

### See also

- [`new`](https://docs.macro-deck.app/cli/new/) - scaffold a project with a ready `macrodeck-build.json`.
- [`merge`](https://docs.macro-deck.app/cli/merge/) - combine `--rid` artifacts into one package.
- [`pack`](https://docs.macro-deck.app/cli/pack/) - package output you built yourself.
- [`validate`](https://docs.macro-deck.app/cli/validate/) - check the artifact `build` produced.
- [Manifest reference](https://docs.macro-deck.app/reference/manifest/).

## CI and automation

> Source: https://docs.macro-deck.app/cli/ci/
>
> A GitHub Actions workflow that builds, validates and conformance-tests a plugin on every platform, gated on exit codes.

Every command reports its verdict through an [exit code](https://docs.macro-deck.app/cli/#exit-codes), and `build`, `validate` and
`test` need no Macro Deck installation and no credentials, so the CLI drops straight into a pipeline.

### One runner, or one per platform

`build` without `--rid` builds every runtime identifier the manifest declares, in one job and one
restore. A .NET plugin cross-builds from Linux, so for most plugins one `ubuntu-latest` runner is the
whole build:

```bash
macrodeck-plugin build --source src/HelloDeck --output ./artifacts
```

```text
Building linux-x64...
Building osx-arm64...
Building win-x64...
Built linux-x64, osx-arm64, win-x64.
```

Split the build across runners only when a target cannot be built from Linux: a `net10.0-windows`
target, a native library compiled per platform, or a build step that needs Windows or macOS tooling.
Then each runner builds its own platform with `--rid` and [`merge`](https://docs.macro-deck.app/cli/merge/) puts the packages back
together. The matrix below is that case; if a plain `build` succeeds on Ubuntu, you do not need it.

If you publish through [`publish-plugin.yml`](https://docs.macro-deck.app/creator-portal/release-workflow/), do not write this
matrix yourself - set `build-per-platform: true` and the workflow splits and merges for you.

### GitHub Actions

Save as `.github/workflows/plugin.yml` in a project created with [`macrodeck-plugin new`](https://docs.macro-deck.app/cli/new/)
(here `HelloDeck`; replace it with your project name). It builds each platform on its own runner, so
use it for a plugin that needs that; otherwise drop the matrix and the `--rid`, and build every
platform in the one job.

```yaml
name: Plugin

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: windows-latest
            rid: win-x64
          - os: macos-latest
            rid: osx-arm64
          - os: ubuntu-latest
            rid: linux-x64
    runs-on: ${{ matrix.os }}
    defaults:
      run:
        shell: bash
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: 10.0.x

      - name: Install the CLI
        run: dotnet tool install --global MacroDeck.Plugin.Cli --version 3.0.0-beta.11

      - name: Unit tests
        run: dotnet test

      - name: Build the artifact
        run: macrodeck-plugin build --source src/HelloDeck --rid ${{ matrix.rid }} --output ./artifacts

      - name: Validate for publication
        run: macrodeck-plugin validate --level publication --artifact ./artifacts/*.macroDeckPlugin

      - name: Conformance
        run: |
          macrodeck-plugin test --artifact ./artifacts/*.macroDeckPlugin \
            --report markdown --output conformance.md
          cat conformance.md >> "$GITHUB_STEP_SUMMARY"

      - uses: actions/upload-artifact@v4
        with:
          name: plugin-${{ matrix.rid }}
          path: artifacts/*.macroDeckPlugin
```

Each step fails the job on a non-zero exit code; no output parsing is needed.

To publish one package for every platform, add a job that merges what the matrix built:

```yaml
  package:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: 10.0.x

      - name: Install the CLI
        run: dotnet tool install --global MacroDeck.Plugin.Cli --version 3.0.0-beta.11

      - uses: actions/download-artifact@v4
        with:
          pattern: plugin-*
          path: artifacts
          merge-multiple: true

      - name: Merge
        run: macrodeck-plugin merge artifacts/*.macroDeckPlugin --output dist

      - uses: actions/upload-artifact@v4
        with:
          name: plugin
          path: dist/*.macroDeckPlugin
```

### Notes

- **One runtime identifier per runner.** `build --rid` builds only that target, so each job produces and
  tests its own single-platform artifact. The RIDs must be ones your `manifest.json` declares.
- **`test` launches the plugin**, so it tests the artifact whose entrypoint matches the runner's own
  platform. It needs the ASP.NET Core shared framework, which the .NET SDK includes.
- **`validate --level publication`** fails (exit 1) on missing Store metadata such as `repository`; drop
  the step until you are ready to publish. See [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/).
- **Pin the version.** `--prerelease` resolves to `3.0.0-preview.10`: SemVer orders `beta` before
  `preview`, so the newest published release, `3.0.0-beta.11`, is not the one it picks - and
  `preview.10` has no `merge`. Install with `--version` until a stable 3.0 CLI ships.
- **Never put a signing key or certificate in CI.** A publishing workflow submits an unsigned artifact;
  the Creator Portal signs it.
- **Tell a broken plugin from a broken runner:** exit 1 means the plugin is wrong, exit 3 means an input
  could not be read or launched.

### Verifying a signed artifact

```yaml
      - name: Verify signature
        run: macrodeck-plugin verify ./downloads/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin --output json
```

- [`verify`](https://docs.macro-deck.app/cli/signing/#verify) is the only signing command a plugin's CI needs.
- **It needs no network.** The Macro Deck root public key is compiled in, so it runs offline and in
  air-gapped runners.
- Gate on the exit code. `--output json` gives the same verdict as
  `{ valid, format, certificateId, issuerCertificateId, rootAnchored, revocationChecked, problems[] }` when
  you need details. `issuerCertificateId` names the issuer certificate that signed the signing certificate,
  or is `null` when the root signed it directly.
- Every run states that revocation was not checked. A `valid` verdict is a cryptographic fact about the
  signature and chain at signing time, not a live trust decision; nothing in the CLI consults
  `security.json` or any other revocation feed.
- `--root-public` lets a test pipeline use a throwaway root instead of the pinned one. Never use it to
  verify a production release; it prints `warning non-production-root`.

These points apply equally to [`sign`](https://docs.macro-deck.app/cli/signing/#sign), wherever it does run.

### See also

- [`macrodeck-plugin build`](https://docs.macro-deck.app/cli/build/) - the `--rid` matrix build.
- [`macrodeck-plugin merge`](https://docs.macro-deck.app/cli/merge/) - one package from the matrix.
- [Release workflow reference](https://docs.macro-deck.app/creator-portal/release-workflow/) - `build-per-platform` does all of
  this inside the publishing workflow.
- [`macrodeck-plugin test`](https://docs.macro-deck.app/cli/test/) - filters and report formats.
- [Signing packages](https://docs.macro-deck.app/cli/signing/) - `verify` in full.
- [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/) - what the publishing workflow submits.

## macrodeck-plugin icon-pack

> Source: https://docs.macro-deck.app/cli/icon-pack/
>
> Bundle icon packs with a plugin project, list the bundled packs and remove them again.

`icon-pack` manages the icon packs a plugin ships inside its own package. A bundled pack is declared in the
manifest's [`bundledIconPacks`](https://docs.macro-deck.app/reference/manifest/#bundled-icon-packs) under a key that is unique within
the plugin, such as `logos`. The host imports it as a read-only pack owned by the plugin, and the plugin
addresses its icons by key and icon name.

`icon-pack` edits the plugin project, never a built artifact. [`build`](https://docs.macro-deck.app/cli/build/) and
[`pack`](https://docs.macro-deck.app/cli/pack/) then package the pack file like any other payload file, so the plugin's signature
covers it.

The group is named `icon-pack` because `pack` already means "build the artifact" in this CLI.

### Example

```bash
macrodeck-plugin icon-pack add ~/Downloads/service-logos.macroDeckIconPack
```

```text
Copied the pack to 'icon-packs/service-logos.macroDeckIconPack'.
Added icon pack 'Service Logos' (12 icon(s)) under the key 'service-logos'.
```

```bash
macrodeck-plugin icon-pack list
macrodeck-plugin icon-pack remove service-logos
```

Run `add` once per pack. A plugin can bundle up to 32 packs.

### add

```text
macrodeck-plugin icon-pack add <path.macroDeckIconPack> [--key <key>] [--copy] [--force]
```

`add` validates the pack, places it at `icon-packs/<key>.macroDeckIconPack` and records it in the
manifest's `bundledIconPacks`. The rest of `manifest.json`, including property order and any property the
CLI does not know, is kept, and the file keeps its indentation.

Where the pack comes from decides what happens to the file:

| Source | What `add` does |
| --- | --- |
| Outside the project | Copies it. |
| Inside the project | Moves it, so the pack never sits in the project twice, and prints where it moved it from. `--copy` keeps the original in place. |
| Already at `icon-packs/<key>.macroDeckIconPack` | Uses it as it is. |

The pack must pass these checks, or nothing is changed:

- It is a readable `.macroDeckIconPack` archive with a `pack.json` (`icon-pack-invalid`) and fits in one
  plugin artifact entry (`icon-pack-too-large`). A readable pack has at most 30,000 archive entries and a
  `pack.json` of at most 32 MiB (`IconPackArchiveLimits`); Macro Deck 3.0.0-beta.13 and older sync at most
  10,000 entries per bundled pack.
- Every icon has a master image, and every icon name is unique (compared case-insensitively) and usable as
  an address: not blank, no surrounding whitespace, no `/`, no control characters, at most 128 characters
  (`icon-pack-names-invalid`, which lists every offending name).
  [Appearances](https://docs.macro-deck.app/guide/concepts/#icon-appearances) are not icons of their own: they need no name, and the
  plugin addresses an icon by its name whatever appearances it has. A trait `variant` marks a named style such
  as `outlined` and is never picked automatically; it is limited like every trait to a lowercase-first
  letters-and-digits token of at most 32 characters.
- A pack that declares AI-generated assets needs the plugin to declare them too: set `ai.generatedAssets`
  to `true` in `manifest.json` first (`ai-declaration-mismatch`). A pack that declares nothing about AI is
  added with the warning `icon-pack-ai-undeclared`, because its icons ship as part of the plugin.

| Option | Default | Description |
| --- | --- | --- |
| `<path>` | required | The `.macroDeckIconPack` file to bundle. |
| `--key <key>` | slug of the pack name | The key the plugin addresses the pack by: lowercase letters, digits and inner hyphens, at most 64 characters. `Service Logos` becomes `service-logos`. When the name yields no key, pass one. |
| `--copy` | off | Copy a pack that is already inside the project instead of moving it. |
| `--force` | off | Replace a pack already bundled under the key: its file and its manifest entry. Without it, `add` refuses an existing key (`icon-pack-exists`). |
| `--source <dir>` | `.` | The plugin project directory. Bundled pack paths are relative to it. |
| `--manifest <path>` | `<source>/manifest.json` | The manifest to edit. |

### list

```text
macrodeck-plugin icon-pack list [--output text|json]
```

```text
logos: icon-packs/logos.macroDeckIconPack - Service Logos, 12 icon(s)
status: icon-packs/status.macroDeckIconPack - missing
```

Lists every declared pack with its key, path, pack name, icon count and whether the file is there.
`--output json` prints the same as a stable shape:

```json
{
  "bundledIconPacks": [
    {
      "key": "logos",
      "path": "icon-packs/logos.macroDeckIconPack",
      "present": true,
      "name": "Service Logos",
      "iconCount": 12,
      "problem": null
    }
  ]
}
```

`name` and `iconCount` are `null` when the file is missing or unreadable; `problem` then says why it could
not be read.

### remove

```text
macrodeck-plugin icon-pack remove <key>
```

Removes the entry from `bundledIconPacks` and deletes the file at its declared path, as long as that path is
inside the project. An unknown key is an error (`icon-pack-not-declared`).

`list` and `remove` take `--source` and `--manifest` like `add`.

### During development

[`run`](https://docs.macro-deck.app/cli/run/#bundled-icon-packs) against a real host syncs the bundled packs when the session starts,
and with `--watch` syncs an `add`, `remove` or replaced pack file right away, without restarting the plugin.

### Exit codes

| Code | When |
| --- | --- |
| 0 | The manifest was updated, or the list was printed. |
| 1 | The pack fails a check, the key is taken or unknown, or the manifest already declares 32 packs. |
| 2 | Bad arguments, including an invalid `--key`. |
| 3 | The project, the manifest or the pack file could not be found or read. |
| 70 | An error the command did not anticipate. |

### See also

- [Manifest reference: bundled icon packs](https://docs.macro-deck.app/reference/manifest/#bundled-icon-packs)
- [`inspect`](https://docs.macro-deck.app/cli/inspect/) - lists the bundled packs of a built artifact.

## macrodeck-plugin inspect

> Source: https://docs.macro-deck.app/cli/inspect/
>
> Describe what installing an artifact or version directory would find, without a running host.

Reports what installing an artifact or version directory would find, without a running host and without
writing anything.

### Examples

Inspect a packed artifact:

```bash
macrodeck-plugin inspect --artifact com.example.my-plugin-1.0.0.macroDeckPlugin
```

```text
warning entrypoint-not-packed: Entrypoint 'linux-x64' declares 'runtimes/linux-x64/MyPlugin', which is not in the artifact.
warning entrypoint-not-packed: Entrypoint 'win-x64' declares 'runtimes/win-x64/MyPlugin.exe', which is not in the artifact.
com.example.my-plugin 1.0.0 (My Plugin)
A Macro Deck plugin.

Entrypoints:
  linux-x64: runtimes/linux-x64/MyPlugin (missing)
  osx-arm64: runtimes/osx-arm64/MyPlugin
  win-x64: runtimes/win-x64/MyPlugin.exe (missing)

Permissions: (none declared)

Languages: (none declared)
AI: (not declared)

Dependencies: (none declared)

Conflicts: (none declared)

Icon packs: (none declared)

Bundled icon packs:
  logos: icon-packs/logos.macroDeckIconPack - Service Logos, 12 icon(s)

Compatibility:
  macroDeck: >=3.0.0-0

Signature: (not signed)

Entries: 346, uncompressed: 118565046 bytes, archive: 46689899 bytes, ratio: 2.5:1
```

Inspect a version directory before packing it:

```bash
macrodeck-plugin inspect --directory stage
```

Print the digest a signature is computed over:

```bash
macrodeck-plugin inspect --artifact com.example.my-plugin-1.0.0.macroDeckPlugin --show-digest
```

```text
...
Digest to sign (base64): bWFjcm8tZGVjay1wbHVnaW4vMQpjb20uZXhhbXBsZS5teS1wbHVnaW4K...
```

Machine-readable output:

```bash
macrodeck-plugin inspect --artifact com.example.my-plugin-1.0.0.macroDeckPlugin --output json
```

```json
{
  "pluginId": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "A Macro Deck plugin.",
  "entrypoints": [
    {
      "rid": "linux-x64",
      "executable": "runtimes/linux-x64/MyPlugin",
      "arguments": [],
      "runtimeKind": "SelfContained",
      "dotnetVersion": null,
      "present": false
    },
    ...
  ],
  "permissions": [],
  "languages": [],
  "ai": null,
  "dependencies": [],
  "conflicts": [],
  "iconPacks": [],
  "bundledIconPacks": [
    {
      "key": "logos",
      "path": "icon-packs/logos.macroDeckIconPack",
      "present": true,
      "listedInFiles": true,
      "name": "Service Logos",
      "version": "1.0.0",
      "iconCount": 12,
      "problem": null
    }
  ],
  "compatibility": { "sdk": null, "macroDeck": ">=3.0.0-0", "protocolMinimum": null, "protocolMaximum": null },
  "signature": null,
  "entryCount": 346,
  "totalUncompressedBytes": 118565046,
  "archiveBytes": 46689899,
  "compressionRatio": 2.539415345490467,
  "warnings": [
    { "code": "entrypoint-not-packed", "message": "Entrypoint 'linux-x64' declares ..." },
    ...
  ],
  "digestBase64": null
}
```

Forgetting the input is a usage error - unlike `validate` and `pack`, `inspect` has no default:

```bash
macrodeck-plugin inspect
```

```text
error no-selector: Specify one of --artifact or --directory. Unlike validate and pack, inspect has no default input.
```

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--artifact <path>` | - | Path to a `.macroDeckPlugin` artifact. |
| `--directory <path>` | - | A version directory containing `manifest.json`. |
| `--show-digest` | off | Also print the manifest's signable digest, base64-encoded. |
| `--output <text\|json>` | `text` | How to render the result. |

Exactly one of `--artifact` and `--directory` is required: neither is `no-selector`, both is
`too-many-selectors`.

### What is reported

Entrypoints, permissions, declared languages, the AI declaration, dependencies, conflicts, icon packs,
bundled icon packs, compatibility, signature shape, entry count, size and compression ratio.

`inspect` describes, it does not judge: it never runs the JSON Schema, never checks a declared file's digest,
never flags an undeclared file, and marks an unknown permission `(unknown)` without failing. Use
[`validate`](https://docs.macro-deck.app/cli/validate/) for a verdict.

The one payload check is entrypoint presence: every declared entrypoint, for every RID, is checked against
the real content. A missing one prints `warning entrypoint-not-packed`, is marked `(missing)` in the text
report, and has `"present": false` in JSON (`null` when the payload could not be read, so presence was not
checked). JSON also carries a top-level `warnings[]` of `{ code, message }`. A single-platform build is a
legitimate intermediate state, so this never changes the exit code.

[Bundled icon packs](https://docs.macro-deck.app/reference/manifest/#bundled-icon-packs) are read out of the payload, from inside the
artifact with `--artifact`, and listed with their key, path, pack name and icon count. Like an entrypoint,
a declared pack that is not in the payload prints `warning bundled-icon-pack-missing` and is shown as
`missing`. With `--artifact`, a pack path that `files[]` does not list prints
`warning bundled-icon-pack-not-in-files`, because the host skips such a pack; `listedInFiles` is `null`
for a directory. A pack file that is not a readable icon pack prints `warning bundled-icon-pack-invalid`.
None of these change the exit code.

### Signature shape

Reported as one of `not signed`, `well-formed ed25519 (not cryptographically verified)`,
`unverifiable (unrecognized algorithm)` or `invalid ed25519 length` - shape only, as the
[signing section](https://docs.macro-deck.app/reference/plugin-hosting/#signing) describes. `inspect` has no key material to verify
against.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | The manifest was read; there is no "read fine but invalid" outcome. |
| `2` | Usage error: `no-selector` or `too-many-selectors`. |
| `3` | The input could not be read, e.g. `artifact-not-found`, `manifest-not-found`. |

An artifact or manifest the reader rejects exits with the code for that reader error.

### See also

- [`validate`](https://docs.macro-deck.app/cli/validate/)
- [`pack`](https://docs.macro-deck.app/cli/pack/)
- [`signing`](https://docs.macro-deck.app/cli/signing/)
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/)

## macrodeck-plugin merge

> Source: https://docs.macro-deck.app/cli/merge/
>
> Merge single-platform packages built on different machines into one multi-platform package.

`merge` combines the packages [`build --rid`](https://docs.macro-deck.app/cli/build/#single-platform-artifacts) produced on different
runners into one `.macroDeckPlugin` declaring every runtime identifier. Use it when each platform has to be
built natively, for example a `net10.0-windows` target on Windows and a native library on macOS.

### Example

```bash
macrodeck-plugin merge \
  artifacts/com.example.spotify-controller-1.0.0-win-x64.macroDeckPlugin \
  artifacts/com.example.spotify-controller-1.0.0-osx-arm64.macroDeckPlugin \
  artifacts/com.example.spotify-controller-1.0.0-linux-x64.macroDeckPlugin \
  --output dist
```

```text
Merged linux-x64, osx-arm64, win-x64.
Packed com.example.spotify-controller 1.0.0 -> dist/com.example.spotify-controller-1.0.0.macroDeckPlugin (...).
```

The result is the package a full `build` of the same commit produces on a machine that can build every
platform.

### Options

| Option | Default | Description |
| --- | --- | --- |
| `<artifacts>...` | required | The packages to merge. |
| `--output <dir>` | `.` | **Directory** for the artifact, named `<id>-<version>.macroDeckPlugin`. |
| `--force` | off | Overwrite an existing artifact. |

### What merge checks

Nothing is written unless every check passes.

- **Each package is intact.** Every file must match the digest its own manifest lists, and no file may be
  unlisted (`hash-mismatch`), since packages usually travel between CI jobs.
- **Same plugin, same version** (`identity-mismatch`).
- **Same manifest apart from `entrypoints`** (`manifest-mismatch`). Build every package from the same commit
  with the same version.
- **Each runtime identifier appears once** (`duplicate-rid`).
- **Shared files are identical.** A file outside a runtime identifier's own directory, such as the icon or an
  `include`d asset, may appear in several packages but must have the same bytes in each (`file-conflict`).

Like `build`, `merge` never signs: any `signature` is dropped and `files[]` is recomputed.

### Exit codes

| Code | When |
| --- | --- |
| 0 | The artifact was written. |
| 1 | A package is invalid or the packages do not belong together. |
| 2 | Bad arguments, or an artifact that already exists without `--force`. |
| 3 | A package could not be found or is not a ZIP archive. |
| 4 | Cancelled (Ctrl-C). |
| 70 | Staging failed. |

### See also

- [`build`](https://docs.macro-deck.app/cli/build/) - `--rid` produces the packages merged here.
- [CI and automation](https://docs.macro-deck.app/cli/ci/) - a matrix workflow that merges its results.

## macrodeck-plugin new

> Source: https://docs.macro-deck.app/cli/new/
>
> Scaffold a new plugin project from the official template, interactively or from a script.

`new` creates a plugin project from the official
[plugin template](https://github.com/Macro-Deck-App/Macro-Deck-Plugin-Template), with a `manifest.json`
and `macrodeck-build.json` ready for [`build`](https://docs.macro-deck.app/cli/build/).

### Examples

```bash
macrodeck-plugin new
```

Walks an interactive wizard. Use it when starting a plugin by hand.

```bash
macrodeck-plugin new --name "Spotify Controller" --publisher "Example Publisher" \
  --repository https://github.com/example/spotify-controller --yes
```

```text
Created plugin project at '~/src/SpotifyController'.
Manifest: ~/src/SpotifyController/src/SpotifyController/manifest.json
Build configuration: ~/src/SpotifyController/src/SpotifyController/macrodeck-build.json
```

No prompts; the id (`com.example.spotify-controller`), project name and output directory are derived. Use
it from a script or an IDE integration.

```bash
macrodeck-plugin new --name "Spotify Controller" --id com.example.spotify-controller \
  --publisher "Example Publisher" --non-interactive
```

No prompts and no guessing: a missing required value fails instead of being defaulted. Use it in CI.

```text
$ macrodeck-plugin new --name "Spotify Controller" --publisher "Example Publisher" --non-interactive
error missing-required-option: --id must be supplied when running non-interactively.
```

```bash
macrodeck-plugin new --name "Acme Light Control" --publisher Acme --platform win-x64 --yes
```

```text
Created plugin project at '~/src/AcmeLightControl'.
...
warning publication-metadata-missing: 'repository' is required to publish to the Macro Deck plugin ecosystem. It is not required to develop or run this plugin locally.
```

A Windows-only plugin. After scaffolding, `new` warns about each field still missing for publication.

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--name <name>` | prompted | The plugin's display name. Required. |
| `--id <id>` | prompted | The reverse-domain plugin id, checked by the manifest's rule. Required unless `--yes`. |
| `--publisher <name>` | prompted | The publisher's display name. Required. |
| `--description <text>` | `A Macro Deck plugin.` | Written to `manifest.description`. |
| `--repository <url>` | omitted | Absolute `http`/`https` URL. |
| `--homepage <url>` | omitted | Absolute `http`/`https` URL; the wizard offers the repository URL. |
| `--license <spdx>` | `MIT` | Written to `manifest.license` verbatim. |
| `--platform <rid>` | `win-x64`, `osx-arm64`, `linux-x64` | A target runtime identifier; repeat for each platform. |
| `--project-name <name>` | derived from `--name` | The C# project and assembly name. |
| `--output <dir>` | `./<project name>` | Directory to scaffold into; must not exist or be empty. |
| `-y`, `--yes` | off | Never prompt; accept every default the wizard would offer. |
| `--non-interactive` | off | Never prompt; a missing required value is a usage error. |
| `--template-version <v>` | latest prerelease | Install this exact template version. |
| `--skip-template-install` | off | Never probe or install the template; it must already be installed. |
| `--no-restore` | off | Skip the NuGet restore `dotnet new` would run. |

### Prompting

The wizard runs only when stdin is a terminal and neither `--yes` nor `--non-interactive` is given. Options
you pass become the wizard's defaults, so it only fills gaps, then asks `Create plugin? [Y/n]`.

Without a terminal, a missing required value is a `missing-required-option` usage error rather than a
prompt that would hang a CI job.

| | Missing `--id` | Missing `--name` or `--publisher` |
| --- | --- | --- |
| `--yes` | derived from `--name` as `com.example.<kebab-name>` | usage error |
| `--non-interactive` | usage error | usage error |

### Platforms

```bash
macrodeck-plugin new --name "Acme Light Control" --publisher Acme --yes \
  --platform win-x64 --platform win-arm64
```

- `--platform` accepts `win-x64`, `win-arm64`, `osx-arm64`, `osx-x64`, `linux-x64` and `linux-arm64`.
  Anything else fails with `unknown-platform`; selecting none fails with `no-platform-selected`.
- The wizard offers only `win-x64`, `osx-arm64` and `linux-x64`, the platforms Macro Deck ships builds
  for, as a checkbox list (a numbered list on a terminal without ANSI support).
- Only the selected platforms are written to `manifest.entrypoints` and `macrodeck-build.json`.

### Template handling

`new` checks whether the template is installed and only reaches the network if it is not, so later runs
work offline. It installs `MacroDeck.Plugin.Templates@*-*` (the `*-*` picks up `-preview` versions) or
the exact `--template-version`. If the install fails, the error carries the `dotnet` output.

### Generated files

```text
SpotifyController/
  SpotifyController.slnx
  src/SpotifyController/
    manifest.json
    macrodeck-build.json
    SpotifyController.csproj
    Program.cs
    PluginIntegration.cs
    Assets/icon.svg
    Localization/Strings.resx
    ...
  tests/SpotifyController.Tests/
```

`manifest.json` and `macrodeck-build.json` sit in `src/<ProjectName>/`, so run `build` there (or pass
`--source`).

#### manifest.json

```json
{
  "id": "com.example.spotify-controller",
  "name": "Spotify Controller",
  "version": "1.0.0",
  "description": "A Macro Deck plugin.",
  "entrypoints": {
    "win-x64": {
      "executable": "runtimes/win-x64/SpotifyController.dll",
      "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" }
    },
    "osx-arm64": {
      "executable": "runtimes/osx-arm64/SpotifyController.dll",
      "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" }
    },
    "linux-x64": {
      "executable": "runtimes/linux-x64/SpotifyController.dll",
      "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" }
    }
  },
  "publisher": { "name": "Example Publisher" },
  "license": "MIT",
  "compatibility": { "macroDeck": ">=3.0.0-0" },
  "repository": "https://github.com/example/spotify-controller"
}
```

- Optional fields you did not supply are left out entirely, never written as empty strings. `license` is
  the exception: `MIT` is a deliberate default.
- `publisher` carries only `name`; set its `id`, `email` and `url` by hand.
- `version` always starts at `1.0.0`.
- `compatibility.macroDeck` is `>=3.0.0-0`, so the plugin installs on 3.0.0 prerelease hosts as well as
  3.0.0 and later. See the [version range grammar](https://docs.macro-deck.app/reference/manifest/#version-range-grammar).
- Entrypoints use the `runtimes/<rid>/` layout, which keeps each platform's native assets apart in one
  multi-platform package.
- Entrypoints are framework-dependent `.dll`s on .NET 10: Macro Deck runs them on the .NET runtime it
  ships, so the package carries no runtime of its own. See
  [Runtime](https://docs.macro-deck.app/reference/manifest/#runtime) for when to switch to self-contained.

#### macrodeck-build.json

The build recipe `build` reads. The manifest describes what a plugin is; this file says how to build it.

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": ["publish", "SpotifyController.csproj", "-c", "Release",
                    "-r", "win-x64", "--self-contained", "false",
                    "-p:UseAppHost=false", "-o", "bin/publish/win-x64"],
      "output": "bin/publish/win-x64"
    }
  }
}
```

- `executable` and `arguments` are separate values and never go through a shell.
- An optional `workingDirectory`, relative to the project root, runs the tool from somewhere else.
- An optional top-level `include` lists files and directories beyond the build output that belong in the
  package - see [`build`](https://docs.macro-deck.app/cli/build/#staging-layout).
- `output`, `workingDirectory` and `include` must stay inside the project directory.
- Nothing here is .NET-specific: any toolchain can be described the same way.
- Generated targets publish **framework-dependent** Release builds, one per runtime identifier so each
  carries only that platform's native assets. For the generated plugin that is well under 1 MB
  compressed per platform, against about 43 MB self-contained.
- To publish self-contained instead, set `--self-contained true`, drop `-p:UseAppHost=false`, and point
  the entrypoint at the native executable with no `runtime` block: an entrypoint without one must not
  be a `.dll`.

### Exit codes

| Code | When |
| --- | --- |
| 0 | The project was created. |
| 1 | The template itself failed to generate (`template-create-failed`). |
| 2 | Invalid input, a missing required value, or a non-empty `--output` directory (`output-exists`). |
| 3 | `dotnet` is missing (`dotnet-not-found`) or the template could not be installed (`template-install-failed`). |
| 4 | You declined the confirmation. |
| 70 | Writing or rewriting the generated files failed. |

### See also

- [`build`](https://docs.macro-deck.app/cli/build/) - build and package the scaffolded project.
- [`run`](https://docs.macro-deck.app/cli/run/) - run it against a stub host.
- [Manifest reference](https://docs.macro-deck.app/reference/manifest/).

## macrodeck-plugin pack

> Source: https://docs.macro-deck.app/cli/pack/
>
> Build a .macroDeckPlugin artifact from a payload directory, validating the manifest first.

Packs a payload directory into a `.macroDeckPlugin` artifact, validating the manifest and recomputing
`files[]` from disk first.

### Examples

Pack a staged payload directory:

```bash
macrodeck-plugin pack --source stage
```

```text
warning entrypoint-not-packed: Entrypoint 'linux-x64' declares 'runtimes/linux-x64/MyPlugin', which is not in the artifact.
warning entrypoint-not-packed: Entrypoint 'win-x64' declares 'runtimes/win-x64/MyPlugin.exe', which is not in the artifact.
warning publication-metadata-missing: 'repository' is required to publish to the Macro Deck plugin ecosystem. It is not required to develop or run this plugin locally.
Packed com.example.my-plugin 1.0.0 -> com.example.my-plugin-1.0.0.macroDeckPlugin (346 entries, 118565046 bytes uncompressed).
```

Write to a chosen path, overwrite it, and print the digest to sign:

```bash
macrodeck-plugin pack --source stage --output dist/my-plugin.macroDeckPlugin --force --show-digest
```

```text
...
Created output directory '~/src/MyPlugin/dist'.
Packed com.example.my-plugin 1.0.0 -> dist/my-plugin.macroDeckPlugin (346 entries, 118565046 bytes uncompressed).
Digest to sign (base64): bWFjcm8tZGVjay1wbHVnaW4vMQpjb20uZXhhbXBsZS5teS1wbHVnaW4K...
```

Packing again without `--force`:

```text
error output-exists: '~/src/MyPlugin/com.example.my-plugin-1.0.0.macroDeckPlugin' already exists. Pass --force to overwrite it.
```

A bad manifest never becomes an artifact - it is reported exactly as `validate` would:

```bash
macrodeck-plugin pack --source broken
```

```text
error invalid-version: '1.0' is not a valid SemVer version. [/version]
warning unknown-permission: 'host:everything' is not a known permission. [/permissions/0]

com.example.my-plugin 1.0: 1 error(s), 1 warning(s).
```

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--source <dir>` | `.` | The payload directory to pack. |
| `--manifest <path>` | `<source>/manifest.json` | The manifest to pack. |
| `--output <path>` | `<id>-<version>.macroDeckPlugin` | Where to write the artifact. |
| `--force` | off | Overwrite an existing output file. |
| `--show-digest` | off | Also print the packed manifest's signable digest, base64-encoded, re-read from the written artifact. |

`--output` is a file path, not a format selector: `pack` has no `--output text|json`, and its report is always
plain text.

### What pack does

1. Validates the manifest with the same validator as [`validate`](https://docs.macro-deck.app/cli/validate/). Any error stops `pack`
   before a byte is written.
2. Hashes every file under `--source` except `manifest.json`, the `--output` file and any `.macroDeckPlugin` file into a fresh `files[]`. Any `files[]` the source
   manifest declared is discarded, never merged. [Bundled icon packs](https://docs.macro-deck.app/reference/manifest/#bundled-icon-packs)
   are payload files like any other, so they are hashed here too.
3. Stops on a symlink, an unsafe path, or any artifact size or entry limit from the
   [`.macroDeckPlugin` artifact section](https://docs.macro-deck.app/reference/plugin-hosting/#the-macrodeckplugin-artifact).
4. Writes the archive, creating the output directory if needed and saying so.

[`build`](https://docs.macro-deck.app/cli/build/) calls this same implementation after staging, so built and packed artifacts are the
same kind. Use `pack` when a custom build system already produced the payload.

### Warnings

None of these change the exit code:

| Code | When |
| --- | --- |
| `entrypoint-not-packed` | A declared entrypoint, per RID, is not in the payload. `build` turns this into a failure for every RID it builds. |
| `publication-metadata-missing` | A `publication` field is missing; always evaluated at the Publication level, and `pack` has no `--level`. |
| `generated-field-authored` | The source manifest in an unbuilt project tree already has `files` or `signature`. |
| `languages-recomputed` | The derived `languages` list replaced a different declared one. |
| `source-looks-like-debug-build` | `--source` looks like `bin/Debug/...`; pack a Release build for distribution. |

### Languages

When the manifest sits in a project tree, `pack` derives [`languages`](https://docs.macro-deck.app/reference/manifest/#languages) from
the project's `Localization/*.resx`, as `build` does, and the derived list wins (`languages-recomputed`). A
staged payload without the `.resx` keeps whatever the manifest declares.

### Signature

`pack` never signs. It passes any existing `signature` through, but since `files[]` was recomputed that
signature no longer matches. A packed artifact is meant to be unsigned: the Creator Portal, or
[`sign`](https://docs.macro-deck.app/cli/signing/#sign) for a non-Store artifact, signs it afterwards.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Packed (warnings allowed). |
| `1` | Invalid manifest, `source-entry-rejected` or `limit-exceeded`. |
| `2` | `output-exists` without `--force`. |
| `3` | `source-not-found`, or the manifest could not be read. |
| `70` | `write-failed`. |

### See also

- [`build`](https://docs.macro-deck.app/cli/build/)
- [`validate`](https://docs.macro-deck.app/cli/validate/)
- [`inspect`](https://docs.macro-deck.app/cli/inspect/)
- [`signing`](https://docs.macro-deck.app/cli/signing/)

## macrodeck-plugin preview

> Source: https://docs.macro-deck.app/cli/preview/
>
> Render a plugin's widget previews to PNG files without a running Macro Deck, for store images and release automation.

`macrodeck-plugin preview render` loads a plugin against a disposable stub host, opens every
[`[UiPreview]`](https://docs.macro-deck.app/ui/views/developer-preview/) scenario, draws it with the same UI runtime the web client uses, and
writes one PNG per scenario and size. It needs no running Macro Deck and no sign-in, so it also runs in CI.

### Examples

```bash
macrodeck-plugin preview render --project src/DeviceBatteryInfo \
  --size 200x200 --size 420x200 --size 420x420 \
  --scale 2 --theme dark --background transparent \
  --output artifacts/previews
```

```text
Wrote artifacts/previews/battery-tile-200x200.png
Wrote artifacts/previews/battery-tile-420x200.png
Wrote artifacts/previews/battery-tile-420x420.png
Rendered 3 image(s) to artifacts/previews.
```

Every scenario at three sizes, at twice the resolution, with transparent corners.

```bash
macrodeck-plugin preview render --project src/DeviceBatteryInfo --cells 1x1 --cells 2x1 --preview "Low battery"
```

One scenario at deck sizes: a cell is 120 px with a 12 px gap, so `2x1` is 252 by 120 px.

### What it draws

Only widget previews. A widget is laid out in the deck's 120 px reference cell and scaled to the requested
size, exactly as a tile on the deck is, so a size that is not a whole number of cells still looks like a tile.
Configuration views, such as an action editor or a configuration flow, are drawn by the desktop app and are
skipped with a `preview-unsupported` warning. A skipped preview does not fail the run.

Text from the plugin's own localization catalog is drawn in the `--locale` language. When the catalog cannot be
read, the run continues with a `preview-localization-unavailable` warning and the plugin's strings show as
placeholders.

### Video streams

A preview has no running host and so no live video. A video stream component is left empty, which shows only what
the widget draws behind it. Pass `--video-stream-image <file>` to draw that image in every video stream instead, framed
by the component's own `fit`: `contain` keeps the whole picture and `cover` fills the component. Space left by `contain`
stays transparent, so the widget's own background shows. A bad path, an unsupported type, a file whose content is not the
image its extension claims, or one over 8 MB is a usage error with the code `invalid-video-stream-image`.

```bash
macrodeck-plugin preview render --project src/PrinterStatus --cells 2x1 --video-stream-image assets/camera.png
```

The image is the tile: its background and rounded corners are part of the picture. `--background` is what shows
behind the corners.

### Options

Pick exactly one of `--project`, `--executable` or `--artifact`, as for [`run`](https://docs.macro-deck.app/cli/run/) and
[`test`](https://docs.macro-deck.app/cli/test/).

| Option | Meaning |
| --- | --- |
| `--size <W>x<H>` | A size in pixels. Repeatable. Defaults to one deck cell, `120x120`. |
| `--cells <C>x<R>` | A size in deck cells. Repeatable, and combinable with `--size`. |
| `--preview <name>` | Only the scenario with this name or id. Repeatable. Defaults to every scenario. An unknown name is a usage error. |
| `--scale <n>` | Device pixels per pixel, greater than 0 and at most 8. Defaults to `2`, so `200x200` is a 400 by 400 image. |
| `--theme dark\|light` | Defaults to `dark`. |
| `--background <color>` | `transparent` (the default), a color name or a `#hex` color. |
| `--radius <px>` | The tile's corner radius in the 120 px reference cell, scaled with the tile as on the deck. Defaults to `22`, the deck's default. |
| `--locale <culture>` | The culture dates and numbers are formatted in, and the language of the plugin's own text. Plugin text falls back to the plugin's default language when it has no resources for the culture. Defaults to `en-US`. |
| `--video-stream-image <file>` | A PNG, JPEG or WebP of up to 8 MB, drawn in place of every video stream. See [Video streams](#video-streams). |
| `--output <dir>` | Where the files go. Defaults to `./previews`. |
| `--browser <path>` | The browser to use, see below. |

A scenario is a static method with no access to the tile, so `--radius` only shapes the tile's corners. A
widget's own safe area comes from its own padding.

Files are named `<scenario>-<width>x<height>.png`, in lower case. When two views declare a scenario with the
same name, both files are prefixed with their view name.

The clock is fixed, so time-based components draw the same on every run.

### The browser

The pixels come from a locally installed Chrome, Chromium or Edge, which the tool starts headless with a
throwaway profile. Nothing is downloaded. It looks, in order, at `--browser`, the `MACRODECK_BROWSER`
environment variable, the usual install locations, and your `PATH`. If none is found the command exits with
`browser-not-found`.

Text is drawn with the fonts installed on the machine, so an image made on a CI runner can differ from one made
on your computer. Render on the same kind of machine every time when the images need to match.

### Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Every selected preview was rendered or skipped, or the plugin declares no previews. |
| 1 | A scenario could not be built or drawn. The other images are still written. |
| 2 | Usage error: a bad size, scale, radius, background, theme or `--video-stream-image`, no or several subject selectors, or an unknown `--preview`. |
| 3 | The plugin could not be launched or built, or no browser was found. |
| 4 | Cancelled (Ctrl-C). |

### See also

- [Developer previews](https://docs.macro-deck.app/ui/views/developer-preview/) - writing the scenarios this command renders
- [`run`](https://docs.macro-deck.app/cli/run/) - the same stub host, with the plugin's output streamed

## macrodeck-plugin run

> Source: https://docs.macro-deck.app/cli/run/
>
> Launch a plugin with the environment the supervisor would give it, against the running host or a disposable stub.

Launches a plugin as a child process with the environment the supervisor would give it, and streams its
output live.

### Examples

```bash
macrodeck-plugin run --project src/HelloDeck --stub-host
```

```text
Started a disposable stub host at http://127.0.0.1:49789.
Started process 18593 (mode: SelfRegistering, host: http://127.0.0.1:49789). Press Ctrl-C to stop.
[plugin] info: Microsoft.Hosting.Lifetime[14]
[plugin]       Now listening on: "http://127.0.0.1:49790"
...
[plugin] info: MacroDeck.Plugin.Hosting.Transport.PluginConnectionHostedService[0]
[plugin]       Registered with the host as '"com.example.hello-deck"'.
Session established (negotiated plugin protocol v3).
[plugin] info: HelloDeck.PluginIntegration[0]
[plugin]       Initialized.
[log:information] HelloDeck.PluginIntegration: Initialized.
...
^CStopping the plugin...
The plugin did not exit within its 10s grace period; killing it.
```

An isolated loop with no Macro Deck installed. The stub is a real in-process `MacroDeckTestHost`, not a
mock.

```bash
macrodeck-plugin run --project src/HelloDeck
```

Against the running Macro Deck. Approve the pairing prompt that appears in Macro Deck - see
[Pairing with a real host](#pairing-with-a-real-host).

```bash
macrodeck-plugin run --project src/HelloDeck --watch
```

Against the running Macro Deck, rebuilt on every save. Leave a developer preview open and it follows along -
see [Watching for changes](#watching-for-changes).

```bash
macrodeck-plugin run --artifact ./artifacts/com.example.hello-deck-1.0.0-osx-arm64.macroDeckPlugin --stub-host
```

Run exactly what you packed, rather than the Debug build.

```bash
macrodeck-plugin run --project src/HelloDeck --stub-host --mode managed
```

Reproduce a managed (supervisor-launched) plugin. Managed mode works only against the stub.

```bash
macrodeck-plugin run --executable ./bin/Debug/net10.0/HelloDeck.dll --host-url http://127.0.0.1:5000
```

An already-built executable or framework-dependent `.dll`, against a host you name explicitly.

For breakpoints, child-process attach and the direct-project launch against a desktop host, see
[Debugging plugins](https://docs.macro-deck.app/guides/debugging/).

### Options

Exactly one of `--project`, `--executable` or `--artifact` is required.

| Option | Default | Description |
| --- | --- | --- |
| `--project <path>` | - | A plugin's `.csproj`, or its directory. |
| `--executable <path>` | - | An already-built executable or framework-dependent `.dll`. |
| `--artifact <path>` | - | A packed `.macroDeckPlugin` artifact. |
| `--host-url <url>` | the running host | A real host's URL; cannot be combined with `--stub-host`. |
| `--stub-host` | off | Run against a disposable in-process stub host. |
| `--mode <managed\|self-registering>` | `self-registering` | Registration mode; `managed` needs `--stub-host`. |
| `--pairing <true\|false>` | `true` | Self-registering only: let interactive pairing supply the credential when no token is given. |
| `--enrollment-token <token>` | placeholder on the stub | Self-registering only: required against a real host when `--pairing false`. |
| `--plugin-id <id>` | the manifest's `id` | Managed only: the injected plugin id. |
| `--secret <secret>` | generated on the stub | Managed only. |
| `--state-directory <dir>` | temp dir | Self-registering only: where the persisted credential is stored. |
| `--data-directory <dir>` | temp dir | Managed only. |
| `--instance-id <id>` | fresh id | Both modes. |
| `--launch-id <id>` | fresh id | Managed only, diagnostic; never asserted on the wire. |
| `--listen-url <url>` | `http://127.0.0.1:0` | Where the plugin listens; port 0 lets the OS pick. |
| `--watch` | off | With `--project` against a real host: run the plugin under `dotnet watch`. See [Watching for changes](#watching-for-changes). |

Temp directories `run` created itself are deleted when it exits.

### Which host `run` uses

```bash
macrodeck-plugin run --project src/HelloDeck --host-url http://127.0.0.1:5000   # this host
macrodeck-plugin run --project src/HelloDeck --stub-host                        # no discovery at all
```

- **The running Macro Deck host is the default.** While it runs, the host writes the loopback port it
  bound to `macro-deck-host.port` (or `macro-deck-host-development.port` for a Development build) in the
  system temp directory, and deletes it on exit. `run` reads it and points the plugin at
  `http://127.0.0.1:<port>` - the same URL the supervisor injects as `MACRO_DECK_PLUGIN_HOST_URL`.
- Both names are probed. If a Development and a Production host run side by side, the most recently
  written port file wins - the host you started last.
- No readable port file fails with `host-not-found` (exit 3). `run` never falls back to the stub
  silently.

### Watching for changes

```bash
macrodeck-plugin run --project src/HelloDeck --watch
```

`--watch` runs the project with `dotnet watch run`, using the environment `run` composes:

- A saved change that .NET Hot Reload supports - a new text, a changed layout, a different mock value in a
  preview scenario - is applied to the running plugin. Open [developer previews](https://docs.macro-deck.app/ui/views/developer-preview/#iterating-on-a-preview)
  are rebuilt in place, without a restart, and the plugin's other open views, such as widgets and
  configuration editors, are opened again with the new code. See [Real views](https://docs.macro-deck.app/ui/views/developer-preview/#real-views).
- Any other change rebuilds the project and restarts the plugin. Macro Deck keeps the open preview on
  screen, marked as waiting, and reopens it when the plugin is back.

The plugin runs from the project directory, like `dotnet run`, and ignores `launchSettings.json` so a profile
cannot point it at another host or state directory. The state directory is kept for the whole command, so you
pair once per `run --watch`; pass `--state-directory` to keep the credential across runs.

`--watch` needs `--project` (`watch-needs-project`, exit 2) and a real host (`watch-needs-real-host`, exit 2):
the stub host has no previews to follow the plugin.

### Bundled icon packs

A self-registered session against a real host brings the host's copy of the plugin's
[bundled icon packs](https://docs.macro-deck.app/reference/manifest/#bundled-icon-packs) in line with `manifest.json` when the session
starts: packs are added, replaced or removed by key, so the icons are in the icon picker and on buttons
without installing the plugin.

With `--watch`, `run` also watches `icon-packs/` and the manifest's `bundledIconPacks`. An
[`icon-pack add`](https://docs.macro-deck.app/cli/icon-pack/) or `remove`, or a replaced pack file, is synced right away without
restarting the plugin, buttons re-render with the new icons, and open plugin views reload.

- Only self-registered sessions sync. Nothing is synced against `--stub-host` or in managed mode.
- A pack larger than 8 MiB cannot be synced live. Build and install the plugin to try it.
- `run` asks the plugin to sync through `MACRO_DECK_PLUGIN_BUNDLED_ICON_PACKS` (`sync`, or `watch` with
  `--watch`). A host that predates bundled icon packs answers that it does not support them, and the plugin
  runs on without them.
- With `--project`, `run` also sets `MACRO_DECK_PLUGIN_BUNDLED_ICON_PACKS_ROOT` to the project directory, so
  the packs are read from the project even though the plugin runs from its build output.

### Pairing with a real host

**`self-registering` is the default, and the only mode a real host accepts.** A managed launch needs a
launch bootstrap token that only a real supervisor can mint, so `--mode managed` without `--stub-host`
fails with `managed-needs-stub-host` (exit 2).

With pairing on (the default) and no token, `run` asks the host whether pairing is available and reports:

| Diagnostic | Meaning |
| --- | --- |
| `developer-mode-disabled` | Developer Mode is off, so no prompt can appear. `run` keeps going; the plugin pairs as soon as you turn it on, with no restart. |
| `pairing-prompt-expected` | The host could not be asked (unreachable or too old). A prompt is expected but not guaranteed. |
| *(neither)* | Developer Mode is on; a prompt will appear. |

Once a request is pending, the plugin writes `Waiting for pairing approval in Macro Deck...` to stderr,
and reports the outcome the same way after you approve or reject it.

#### Using an enrollment token instead

```bash
macrodeck-plugin run --project src/HelloDeck --pairing false --enrollment-token <token>
```

```text
$ macrodeck-plugin run --project src/HelloDeck --pairing false
error enrollment-token-required: --mode self-registering against a real host needs --enrollment-token when --pairing is off.
```

:::caution
A token passed this way is visible in plaintext on the command line. Prefer pairing, or the masked
one-time enrollment and IDE profile in
[Debugging plugins](https://docs.macro-deck.app/guides/debugging/#advanced-enroll-with-a-developer-token-for-headless-runs).
:::

### The environment `run` composes

Every inherited `MACRO_DECK_PLUGIN_*` variable and `ASPNETCORE_URLS` is scrubbed, then set fresh for the
resolved mode, mirroring
[what the supervisor injects](https://docs.macro-deck.app/reference/plugin-hosting/#what-the-supervisor-injects).
Against a real host in self-registering mode `run` also sets `MACRO_DECK_PLUGIN_BUNDLED_ICON_PACKS` (see
[Bundled icon packs](#bundled-icon-packs)), which the supervisor never sets.

In managed mode, `MACRO_DECK_PLUGIN_ID` comes from the `manifest.json` next to the launch target, because
the host rejects an injected id that disagrees with the manifest. `--plugin-id` overrides it. Only when
neither exists does `run` generate a development id, and it warns:

```text
warning plugin-id-generated: No manifest.json next to the launch target, so a development id was generated. ...
```

### Output

- `[plugin]` lines are the plugin's stdout and go to `run`'s stdout; `[plugin:stderr]` lines go to
  stderr.
- `[log:...]` lines are the stub host's forwarded logs.
- `--verbosity quiet` hides `[log:...]` lines and progress narration. The plugin's own output always
  prints.

### Stopping

Ctrl-C runs the supervisor's shutdown sequence against the stub host:

1. `session.goodbye`.
2. Close with code `4004` (`SupervisorShutdown`).
3. Wait for the manifest's `shutdown.gracefulTimeoutSeconds` (clamped to 1-60s; 10s if absent).
4. Kill the process tree if it is still running.

Against a real host, `run` owns no session to say goodbye on, so only steps 3 and 4 apply.

### Exit codes

| Code | When |
| --- | --- |
| the plugin's own | The plugin exited on its own. |
| 2 | Usage error: wrong number of launch targets, `--host-url` with `--stub-host`, `managed-needs-stub-host`, `enrollment-token-required`, `watch-needs-project`, `watch-needs-real-host`. |
| 3 | `host-not-found`, a project that fails to build, an unreadable artifact, or a process that fails to start. |
| 4 | Ctrl-C, whether the plugin exited gracefully or had to be killed. |

See the [shared exit codes](https://docs.macro-deck.app/cli/#exit-codes).

### See also

- [Debugging plugins](https://docs.macro-deck.app/guides/debugging/) - breakpoints, IDE profiles, enrollment tokens.
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - registration modes and every `MACRO_DECK_PLUGIN_*`
  variable.
- [`macrodeck-plugin test`](https://docs.macro-deck.app/cli/test/) - the conformance suite, against the same stub host.

## Signing packages

> Source: https://docs.macro-deck.app/cli/signing/
>
> keygen, sign and verify: creator key pairs, embedded package signatures, and private-key handling.

`keygen` creates a creator key pair, `sign` embeds a signature in a package, and `verify` checks one.

:::note
**None of these is a step towards the Store.** The Creator Portal signs Store artifacts server-side, and
no plugin author ever holds a signing key - see [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/). `keygen`
and `sign` are for artifacts distributed outside the Store and for Macro Deck's own infrastructure.
`verify` is the only one a normal plugin's CI needs.
:::

### Examples

```bash
macrodeck-plugin verify ./downloads/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin
```

```text
invalid: signature-missing: The manifest carries no 'signature' object.
Revocation was not checked; this is cryptographic verification only.
```

Check a downloaded artifact offline. This one is unsigned, so it fails with exit 1.

```bash
macrodeck-plugin verify ./artifacts/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin --output json
```

```json
{
  "valid": false,
  "format": null,
  "certificateId": null,
  "issuerCertificateId": null,
  "rootAnchored": true,
  "revocationChecked": false,
  "problems": [
    {
      "code": "signature-missing",
      "message": "The manifest carries no 'signature' object."
    }
  ]
}
```

The same verdict as a document, for a pipeline that needs more than the exit code.

```bash
macrodeck-plugin keygen --output ~/.macrodeck/keys
```

```text
Public key:  ~/.macrodeck/keys/macrodeck-creator.public
Private key: ~/.macrodeck/keys/macrodeck-creator.private
Public key (base64): 3ay/DcXb90fbA+uH8jh5iMvx6ORF3AfUfOyA/0CPRPY=
Submit the public key above to the Creator Portal for certificate issuance - this command does not issue certificates.
```

Create a key pair outside your repository. Read [Private-key handling](#private-key-handling) first.

```bash
macrodeck-plugin sign ./artifacts/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin \
  --output ./signed/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin \
  --certificate certificate.json \
  --certificate-signature certificate.sig \
  --private-key ~/.macrodeck/keys/macrodeck-creator.private
```

Sign a package for distribution outside the Store, with a certificate the Creator Portal issued. If the
certificate names an issuer, add `--issuer-certificate issuer.json --issuer-certificate-signature issuer.sig`.

### `keygen`

Generates a creator Ed25519 key pair. It never issues a certificate; only the Creator Portal can turn a
public key into a certificate signed by the Macro Deck root.

| Option | Default | Description |
| --- | --- | --- |
| `--output <dir>` | `.` | Directory to write the key pair into. |
| `--key-name <name>` | `macrodeck-creator` | Base file name for the key pair. |

- Writes `<key-name>.public` and `<key-name>.private`.
- Never overwrites: an existing file at either path fails with `output-exists` before anything is
  written.
- `root`, `macrodeck-root`, `registry` and `macrodeck-registry` fail with `reserved-key-name`: `keygen`
  only ever makes creator keys.

```text
$ macrodeck-plugin keygen --key-name root
error reserved-key-name: 'root' is reserved for Macro Deck's own trust anchors and cannot be used as a creator key name.
```

Exit codes: 0 on success, 2 for `output-exists` or `reserved-key-name`.

### `sign`

Signs a `.macroDeckPlugin`, `.macroDeckIconPack`, `.macroDeckProfile`, `.macroDeckFolder` or
`.macroDeckWidget` package. There is no detached signature: the signature goes into the artifact's own
manifest, and the certificate into the archive root as `certificate.json` and `certificate.sig`, plus
`issuer.json` and `issuer.sig` when an issuer certificate signed it, so the signed artifact verifies on its
own.

| Option | Default | Description |
| --- | --- | --- |
| `<package>` (argument) | - | The package to sign. |
| `--output <path>` | - | **Required.** Where to write the signed artifact; never overwritten. |
| `--certificate <path>` | - | **Required.** The signing certificate (`certificate.json`). |
| `--certificate-signature <path>` | - | **Required.** The root's signature over the certificate (`certificate.sig`). |
| `--private-key <path>` | - | **Required.** The base64-encoded private key `keygen` wrote. |
| `--issuer-certificate <path>` | - | The issuer certificate (`issuer.json`) that signed the certificate. Required exactly when the certificate names an `issuer`; give it together with `--issuer-certificate-signature`. |
| `--issuer-certificate-signature <path>` | - | The root's signature over the issuer certificate (`issuer.sig`). |
| `--root-public <path>` | pinned Macro Deck root | Verify the certificate against this root instead; testing only. |

`sign` runs these steps in order and stops at the first failure:

1. Declared-file validation, as `validate --artifact` does it: every file in `files[]` checked by
   SHA-256 and size.
2. Certificate chain verification against the pinned root (or `--root-public`), through the issuer
   certificate when the certificate names one. The certificate needs exclusive `package` key usage, and it
   and its issuer must be valid now. See [the certificate chain](https://docs.macro-deck.app/policies/security/#signing-the-creator-portal-signs-and-the-host-verifies-before-install-and-before-every-load).
3. The certificate's public key must match `--private-key`.
4. The format's canonical digest (`macro-deck-plugin/1`, `macro-deck-iconpack/1` or
   `macro-deck-portable/1`), then the signature.
5. Write `--output`, then re-verify it exactly as [`verify`](#verify) would. An artifact that does not
   verify is a failure.

An already-signed package fails with `already-signed`; `sign` never replaces a signature.

```text
$ macrodeck-plugin sign app.macroDeckPlugin --output signed.macroDeckPlugin --certificate certificate.json ...
error certificate-untrusted: The certificate signature does not verify against the root key.
```

| Exit code | Failures |
| --- | --- |
| 1 | Certificate malformed, untrusted, wrong-purpose, not yet valid or expired; issuer certificate missing (`certificate-issuer-missing`), not the one the certificate names (`certificate-issuer-mismatch`), or ending before the certificate (`certificate-outlives-issuer`). Private key malformed or not matching the certificate. Package already signed; manifest missing, malformed or too large (8 MiB, or 32 MiB for an icon pack's `pack.json`); an icon pack with more than 30,000 entries once signed (`too-many-entries`); declared files not matching (digest or size mismatch, undeclared file, missing declared file, unsafe entry). |
| 2 | Unsupported package format, `--output` already exists, or only one of the two `--issuer-certificate` options given (`issuer-options-incomplete`). |
| 3 | The package, certificate, certificate signature, issuer certificate, issuer signature, private key or `--root-public` file could not be read. |
| 4 | Ctrl-C. |
| 70 | Writing the output failed, or the written artifact failed its own re-verification. |

### `verify`

Checks a signed package's embedded signature and certificate against the pinned Macro Deck root (or
`--root-public`), with the same
[`MacroDeck.Signing`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/sdk/src/MacroDeck.Signing/README.md)
checks `sign` self-verifies with:

- the certificate chain and its `package` key usage, through the archive's `issuer.json` and `issuer.sig`
  when the certificate names an issuer;
- the certificate's validity, and its issuer's, **at the signature's `signedAt`**, not at verify time - a package signed
  while its certificate was valid still verifies after the certificate expires;
- the format's canonical digest, and every declared file's SHA-256 and size.

| Option | Default | Description |
| --- | --- | --- |
| `<package>` (argument) | - | The package to verify. |
| `--root-public <path>` | pinned Macro Deck root | Verify against this root public key instead; testing only. |
| `--output <text\|json>` | `text` | How to render the result. |

- **Text:** one line with the format, the signing certificate id and, when there is one, the issuer's
  certificate id, or `invalid: <code>: <message>`.
- **JSON:** `{ valid, format, certificateId, issuerCertificateId, rootAnchored, revocationChecked, problems[] }`.
  `issuerCertificateId` is `null` for a certificate the root signed directly; older CLI versions omit it.
- Every run ends by stating that revocation was not checked; `revocationChecked` is always `false`.
  This is local cryptographic verification only.
- With a `--root-public` that is not the pinned root, `rootAnchored` is `false` and a
  `warning non-production-root` line prints, in both formats.

| Exit code | When |
| --- | --- |
| 0 | Valid, and anchored to the pinned root (or to `--root-public`). |
| 1 | Unsigned, tampered or invalid: signature missing, malformed, algorithm-mismatched or not verifying; certificate malformed, untrusted, wrong-purpose or not valid at `signedAt`; issuer certificate missing, mismatched or ending before the certificate; declared files not matching; manifest malformed. |
| 2 | The extension is not a signable package format. |
| 3 | The package or the `--root-public` file could not be read. |
| 4 | Ctrl-C. |

`verify` writes nothing, so it never returns 70.

### Private-key handling

This applies only if you run `keygen` and `sign`. **Publishing to the Store never puts a private key in
your hands or your CI.**

The private key is the only thing that can produce a valid signature under your certificate; `sign` asks
for nothing else to prove who you are.

```bash
echo '*.private' >> .gitignore   # before running keygen, not after
```

- **Never commit it.** Ignore `*.private` (or your key name) before you run `keygen`.
- On Unix, `keygen` writes it with mode `0600` (owner read/write only). Windows has no in-band
  equivalent: `keygen` prints `restrictive-file-mode-unavailable`, and restricting the file with an NTFS
  ACL is up to you.
- **A leaked key taints every artifact ever signed with it**, and the certificate must be revoked. Report
  the leak so the certificate can be revoked, run `keygen` for a fresh pair, and get a new certificate
  for the new public key.
- The CLI cannot issue, re-issue or revoke certificates; that lives in the Creator Portal.

### See also

- [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/) - how Store artifacts are signed.
- [CI and automation](https://docs.macro-deck.app/cli/ci/) - `verify` as a pipeline gate.
- [Security model](https://docs.macro-deck.app/policies/security/) - the trust model `verify` checks against.
- Certificate schema ([v1](https://docs.macro-deck.app/schemas/macrodeck-certificate-v1.schema.json),
  [v2](https://docs.macro-deck.app/schemas/macrodeck-certificate-v2.schema.json)) and
  [package signature schema](https://docs.macro-deck.app/schemas/macrodeck-package-signature-v1.schema.json).

## macrodeck-plugin test

> Source: https://docs.macro-deck.app/cli/test/
>
> Run the conformance suite against a project, executable or artifact and write a text, JSON or Markdown report.

Runs the [conformance suite](https://docs.macro-deck.app/reference/conformance/) against a plugin and writes a report.

### Examples

```bash
macrodeck-plugin test --project src/HelloDeck
```

```text
Macro Deck plugin conformance report (suite 1.2.0)
Plugin: com.example.hello-deck 1.0.0
Started: 2026-09-12T09:36:25.7456760+00:00, duration: 00:00:22.3743497
Passed: 25, Failed: 0, Skipped: 24
Conformant: yes

[PASS] MDC0101 The plugin id is a valid reverse-domain package id (Required)
[PASS] MDC0102 Every declared capability's local id is a valid declared-kind identifier (Required)
...
[SKIP] MDC0403 No two eager variables resolve to the same id (Required)
    Reason:   This subject does not declare the variables capability.
...
```

Run every check against a project. `test` builds it first.

```bash
macrodeck-plugin test --artifact ./artifacts/com.example.hello-deck-1.0.0-osx-arm64.macroDeckPlugin \
  --report markdown --output conformance.md
```

```markdown
# Macro Deck plugin conformance report

Suite version: `1.2.0`
Plugin: `com.example.hello-deck` `1.0.0`
Conformant: **yes**
Passed: 29 - Failed: 0 - Skipped: 20

| Id | Title | Category | Requirement | Outcome | Detail |
|---|---|---|---|---|---|
| MDC0101 | The plugin id is a valid reverse-domain package id | ManifestAndIdentifiers | Required | PASS |  |
| MDC0103 | Every weather station instance id is a valid resource-kind identifier | ManifestAndIdentifiers | Required | SKIP | This subject does not declare the weather capability. |
...
```

Test the artifact you ship, and keep the report as a CI artifact or job summary. The artifact must
contain an entrypoint for the machine running `test`.

```bash
macrodeck-plugin test --project src/HelloDeck --category health-endpoint --category duplicate-ids
macrodeck-plugin test --project src/HelloDeck --check MDC0305
```

Iterate on one area or one failing check.

```bash
macrodeck-plugin test --project src/HelloDeck --required-only --report json --output conformance.json
```

Gate on Required checks only, with a machine-readable report.

```bash
macrodeck-plugin test --list-checks
```

```text
MDC0101	ManifestAndIdentifiers	Required	The plugin id is a valid reverse-domain package id
MDC0102	ManifestAndIdentifiers	Required	Every declared capability's local id is a valid declared-kind identifier
...
MDC0805	BoundedQueues	Recommended	A burst of variables/get invocations beyond MaxConcurrentInvocations never exceeds the reported in-flight bound
```

Every check id, category and requirement level.

### Options

Exactly one of `--project`, `--executable` or `--artifact` is required, unless `--list-checks` is given.

| Option | Default | Description |
| --- | --- | --- |
| `--project <path>` | - | A plugin's `.csproj`, or its directory. |
| `--executable <path>` | - | An already-built executable or framework-dependent `.dll`. |
| `--artifact <path>` | - | A packed `.macroDeckPlugin` artifact. |
| `--category <token>` | all | Restrict to one [category](#categories); repeatable. |
| `--check <id>` | all | Restrict to one check id, e.g. `MDC0305`; repeatable. |
| `--required-only` | off | Run only Required checks. |
| `--report <text\|json\|markdown>` | `text` | The report format. |
| `--output <path>` | stdout | Where to write the report. |
| `--timeout <seconds>` | `60` | Per-check timeout. |
| `--list-checks` | off | List every check and exit; ignores every other option except `--output` and the global options. |

### Filters

`--category`, `--check` and `--required-only` intersect. A `--check` id outside the selected
`--category` selects nothing, without an error.

`--check` is validated against the full catalogue, whatever the other filters select:

```text
$ macrodeck-plugin test --project src/HelloDeck --check MDC9999
error unknown-check-id: 'MDC9999' is not a known check id. Run --list-checks to see every id.
```

#### Categories

| Token | Checks |
| --- | --- |
| `manifest-and-identifiers` | `MDC01xx` |
| `registration-and-negotiation` | `MDC02xx` |
| `capability-serialization` | `MDC03xx` |
| `duplicate-ids` | `MDC04xx` |
| `timeout-and-cancellation` | `MDC05xx` |
| `disconnect-and-reconnect` | `MDC06xx` |
| `health-endpoint` | `MDC07xx` |
| `bounded-queues` | `MDC08xx` |

The exact shape of each report format is in [Conformance: the report](https://docs.macro-deck.app/reference/conformance/#the-report).

### Exit codes

| Code | When |
| --- | --- |
| 0 | The report's `conformant` is `true`. |
| 1 | A Required check failed. |
| 2 | Usage error: wrong number of subjects, an unknown `--category` or `--check`. |
| 3 | The subject could not be built or launched at all - not a conformance verdict. |

See the [shared exit codes](https://docs.macro-deck.app/cli/#exit-codes).

### See also

- [Conformance](https://docs.macro-deck.app/reference/conformance/) - what every check asserts, and the report shape.
- [Testing plugins](https://docs.macro-deck.app/features/testing/) - running the same suite from your own test project.
- [CI and automation](https://docs.macro-deck.app/cli/ci/) - using `test` as a pipeline gate.

## macrodeck-plugin validate

> Source: https://docs.macro-deck.app/cli/validate/
>
> Check a manifest, version directory or packed artifact and report every problem in one run.

Checks a manifest, a version directory or a `.macroDeckPlugin` artifact and reports every problem it finds.

### Examples

Validate a staged payload directory while developing:

```bash
macrodeck-plugin validate --directory stage
```

```text

com.example.my-plugin 1.0.0: 0 error(s), 0 warning(s).
```

Check that a plugin is ready to publish:

```bash
macrodeck-plugin validate --directory stage --level publication
```

```text
error publication-metadata-missing: 'repository' is required to publish to the Macro Deck plugin ecosystem. It is not required to develop or run this plugin locally. [/repository] (publication)
error entrypoint-not-packed: Entrypoint 'linux-x64' declares 'runtimes/linux-x64/MyPlugin', which is not in the artifact. [/entrypoints/linux-x64/executable] (package)
error entrypoint-not-packed: Entrypoint 'win-x64' declares 'runtimes/win-x64/MyPlugin.exe', which is not in the artifact. [/entrypoints/win-x64/executable] (package)

com.example.my-plugin 1.0.0: 3 error(s), 0 warning(s).
```

Validate a packed artifact (defaults to `--level package`):

```bash
macrodeck-plugin validate --artifact com.example.my-plugin-1.0.0.macroDeckPlugin
```

```text
warning publication-metadata-missing: 'repository' is required to publish to the Macro Deck plugin ecosystem. It is not required to develop or run this plugin locally. [/repository] (publication)
error entrypoint-not-packed: Entrypoint 'linux-x64' declares 'runtimes/linux-x64/MyPlugin', which is not in the artifact. [/entrypoints/linux-x64/executable] (package)
error entrypoint-not-packed: Entrypoint 'win-x64' declares 'runtimes/win-x64/MyPlugin.exe', which is not in the artifact. [/entrypoints/win-x64/executable] (package)

com.example.my-plugin 1.0.0: 2 error(s), 1 warning(s).
```

A manifest with several defects - every independent problem is reported at once:

```bash
macrodeck-plugin validate --directory broken
```

```text
error invalid-version: '1.0' is not a valid SemVer version. [/version]
warning unknown-permission: 'host:everything' is not a known permission. [/permissions/0]

com.example.my-plugin 1.0: 1 error(s), 1 warning(s).
```

Pointing at the project instead of the build output:

```bash
cd ~/src/MyPlugin/src/MyPlugin
macrodeck-plugin validate
```

```text
error source-directory: Entrypoint 'osx-arm64' resolves to '~/src/MyPlugin/src/MyPlugin/runtimes/osx-arm64/MyPlugin', which does not exist. This looks like a source directory - validate the build output instead, e.g. bin/Release/net10.0.

~/src/MyPlugin/src/MyPlugin/manifest.json: 1 error(s), 0 warning(s).
```

Machine-readable output for CI:

```bash
macrodeck-plugin validate --directory stage --level publication --output json
```

```json
{
  "valid": false,
  "pluginId": "com.example.my-plugin",
  "version": "1.0.0",
  "level": "publication",
  "problems": [
    {
      "severity": "error",
      "code": "publication-metadata-missing",
      "message": "'repository' is required to publish to the Macro Deck plugin ecosystem. ...",
      "pointer": "/repository",
      "requiredBy": "publication"
    },
    ...
  ]
}
```

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--manifest <path>` | `./manifest.json` | Path to a `manifest.json` file. |
| `--directory <path>` | - | A version directory containing `manifest.json`. |
| `--artifact <path>` | - | Path to a `.macroDeckPlugin` artifact. |
| `--level <development\|package\|publication>` | from the selector | How strictly to validate - see [Levels](#levels). |
| `--output <text\|json>` | `text` | How to render the result. |

Give at most one of `--manifest`, `--directory` and `--artifact` (more is `too-many-selectors`, exit 2). Giving
none validates `./manifest.json`, so running `validate` inside a plugin's build output needs no flag.

### Levels

The three cumulative [requirement levels](https://docs.macro-deck.app/reference/manifest/#requirement-categories),
`development ⊂ package ⊂ publication`:

| Level | Adds over the level before |
| --- | --- |
| `development` | The manifest reader, the embedded JSON Schema, the permission vocabulary, SemVer `version`, the [`additionalLinks` rules](https://docs.macro-deck.app/reference/manifest/#additionallinks), and declared `files[]` digests when present. What the host enforces at install time, except `additionalLinks`, which the host never enforces. |
| `package` | Every declared entrypoint (every RID, not only the current host's) and a declared `icon` checked against real content; a valid multi-RID layout; missing `publication` fields as warnings. |
| `publication` | Missing `publication` fields become errors. |

When `--level` is omitted, `--manifest`/`--directory` (or no selector) use `development` and `--artifact` uses
`package`. An unrecognised level is a usage error (exit 2) reported before the manifest is read:

```text
error usage-error: 'strict' is not a recognized --level. Expected one of: development, package, publication.
```

On an unbuilt source tree (a `manifest.json` next to a project file) the `package`/`publication` payload and
layout checks are skipped, so validating a project root before building does not report files that do not
exist yet.

### What is checked

- The schema and permission-vocabulary checks run for every input. An unknown permission is a warning.
- `version` is checked against SemVer independently of the reader: `1.0` or `v1.0.0` is `invalid-version`.
- File digests are checked only when the manifest declares `files[]`. Only `--artifact` also flags a file
  present but not declared, because a bare manifest or directory has no separate file listing.
- A schema error that is only a follow-on of another reported problem beneath it is suppressed, so one defect
  never appears twice.

### Problem codes

| Code | Meaning |
| --- | --- |
| `malformed` | Not valid JSON; the message names the file with a 1-based line and position. |
| `invalid-version` | `version` is not SemVer. |
| `unknown-permission` | A permission outside the vocabulary (warning). |
| `invalid-additional-link` | An `additionalLinks` entry breaks a [rule](https://docs.macro-deck.app/reference/manifest/#additionallinks); the pointer names the entry and field. Replaces any `schema:*` problem inside `additionalLinks`. |
| `unknown-link-type` | An `additionalLinks` type outside the standard list (warning; the link is not shown). |
| `schema:<keyword>` | A JSON Schema violation, e.g. `schema:required`. |
| `file-missing`, `file-size-mismatch`, `file-digest-mismatch` | A declared `files[]` entry does not match the real bytes. |
| `undeclared-file` | A file in the artifact that `files[]` does not declare (`--artifact` only). |
| `entrypoint-not-packed` | A declared entrypoint, for any RID, is not in the content (`package` and above). |
| `icon-declared-not-present` | `icon` is declared but not in the content (error, `package` and above). |
| `entrypoint-layout-invalid` | Two entrypoints stage into the same directory, or one stages at the package root (error, `package` and above) - the same rule [`build`](https://docs.macro-deck.app/cli/build/) enforces, see [Staging layout](https://docs.macro-deck.app/cli/build/#staging-layout). |
| `publication-metadata-missing` | A `publication`-required field is missing or blank (warning at `package`, error at `publication`). |
| `generated-field-authored` | `files` or `signature` in a manifest that has not been built or packed yet (warning, unbuilt source tree only). |
| `source-directory` | The manifest sits next to a project file with no built entrypoint - validate the build output instead. |
| `not-an-artifact` | `--artifact` is not a ZIP; adds `Did you mean validate --manifest?` when the file is named `manifest.json`. |
| `manifest-not-found`, `artifact-not-found` | The input does not exist. |

Other manifest reader failures are reported under their own kebab-case code, e.g. `entrypoint-missing`.

### Output

Text output is one line per problem - severity, code, message, the JSON pointer in `[...]` when there is one,
and the requiring level in `(...)` when a level requires it - then a summary line. The summary names
`<id> <version>`, or the resolved absolute path when the manifest could not be read.

`--output json` returns `valid`, `pluginId`, `version`, `level` (always present: the level actually used) and
`problems[]`. Each problem has `severity`, `code`, `message` and `pointer`, plus `requiredBy` only when a level
requires it (for example absent on `generated-field-authored`).

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Valid at the chosen level (warnings allowed). |
| `1` | The manifest was read but has at least one error. |
| `2` | Usage error: too many selectors, unknown `--level`. |
| `3` | The input could not be read: missing file, not a ZIP, permissions. |

### See also

- [`inspect`](https://docs.macro-deck.app/cli/inspect/) - describe an artifact without judging it
- [`pack`](https://docs.macro-deck.app/cli/pack/) - runs the same validation before writing an artifact
- [`build`](https://docs.macro-deck.app/cli/build/)
- [Manifest reference](https://docs.macro-deck.app/reference/manifest/)
