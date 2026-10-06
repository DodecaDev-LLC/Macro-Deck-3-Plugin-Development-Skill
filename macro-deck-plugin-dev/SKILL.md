---
name: macro-deck-plugin-dev
description: Build, extend, debug, test and publish Macro Deck 3 plugins (.NET SDK, manifest, macrodeck-plugin CLI, UI, Store). Use for any Macro Deck plugin work, even if v3 isn't named. Not for Macro Deck 2.
---

# Macro Deck 3 plugin development

This skill makes you effective on any Macro Deck 3 plugin task: a plugin from scratch, a new capability in
an existing one, a bug, a failing conformance check, a release. It bundles the official plugin docs, the
plugin template and the four sample plugins, so you can work from the real contracts instead of memory.

**Scope: Macro Deck 3 and later only.** Macro Deck 2 used a completely different, in-process plugin model,
and nothing about it carries over. If a project looks like a Macro Deck 2 plugin (a class deriving from
`MacroDeckPlugin`, an `ExtensionManifest.json`, a reference to the desktop app's `Macro Deck 2.dll`), say
that this skill covers v3 only, and offer to port it to a fresh v3 plugin instead. The one v3 feature that
touches v2 is `IMigrationProvider`, which lets a v3 plugin take over a user's v2 settings
(the *Settings migrations* section of `references/docs/features.md`).

## The model in one paragraph

A v3 plugin is a small **.NET 10 console app** that Macro Deck starts as a separate process and talks to over
a local protocol the SDK handles for you. Its identity lives **only** in `manifest.json` (id, name, version,
icon, one entrypoint per platform). `Program.cs` builds it with `MacroDeckPlugin.CreatePlugin(args)` and
registers one or more **integrations** (`IPluginIntegration`). An integration exposes `Actions` and opts into
everything else by **implementing capability interfaces** on the same class: `IVariableProvider`,
`IEventProvider`, `IConfigFlowProvider`, `IIntegrationIssueProvider`, `IUiProvider`, `IWidgetTypeProvider`
and more. Every user-facing string comes from `Localization/Strings.resx` through a generated `Strings`
class. The `macrodeck-plugin` CLI scaffolds, runs against a stub host, tests conformance, builds and packs a
`.macroDeckPlugin`. Publishing goes through a GitHub release workflow to the Creator Portal, which signs it.

## Where things are

| Need | Read |
| --- | --- |
| Code shape of every common capability, on one page | `references/cheatsheet.md` (start here for coding) |
| The rules a clean plugin follows (identity, async, localization, logging, Store gate) | `references/agent-rules.md`, the official agent rulebook shipped with the template |
| Which doc page covers what | `references/INDEX.md`, then that page's section in `references/docs/<topic>.md` |
| A complete, idiomatic plugin to imitate | `references/samples/<sample>.md` (`samples/README.md` has a capability-by-sample matrix) |
| The exact files a new plugin starts with | `references/template.md` |
| When this copy was synced | `references/SOURCES.md` |

The docs are copies of docs.macro-deck.app, merged into ten topic files (`introduction`, `features`, `ui`,
`ui-views`, `ui-components`, `cli`, `guides`, `reference`, `creator-portal`, `policies`). Each page is an
`## <Page title>` section with its live URL, and `INDEX.md` lists which file holds which page. These files are
long: grep for the page heading or the type and read the section around it rather than the whole file, e.g.
`grep -n "^## Button states" references/docs/features.md` or `grep -rn "IDynamicOptionsActionDefinition" references/`.
Read the relevant doc page before writing a capability you have not written in this session: the pages are
short, precise, and full of rules that are easy to get wrong from intuition (for example, `GetIssuesAsync`
is polled and must never do I/O).

Treat the bundle as a strong default, not gospel. The SDK is still in prerelease and moves. When the user's
project, a compiler error or an analyzer contradicts the bundled docs, believe the project and the compiler,
then check the live page. If the network is available and the bundle looks stale (see `SOURCES.md`), you can
refresh it with `python3 scripts/sync_docs.py`.

## Before you touch code: orient

1. **Find the plugin root**: the directory with `manifest.json`, `macrodeck-build.json` and the `.csproj`.
   A scaffolded solution keeps it under `src/<Name>/` with tests under `tests/<Name>.Tests/`.
2. **Read** `manifest.json`, `Program.cs`, the integration class(es) and `Localization/Strings.resx`. Note
   which capability interfaces the integration already implements.
3. **Check the SDK version** in `Directory.Packages.props` (`MacroDeckSdkVersion`) or the `.csproj`. A floating
   `3.0.0-*` resolves to the newest preview; a pin older than the Store minimum (below) needs bumping before
   release.
4. If the repo has its own `AGENTS.md` or `CLAUDE.md`, follow it. A plugin generated from the template
   carries a copy of the same rulebook bundled here.

## Workflows

### A. A new plugin from scratch

1. Pick identity with the user: display name, reverse-domain lowercase id (`com.acme.light-control`; at least
   two segments, kebab-case segments, no "macro-deck" or third-party brand in the id), publisher name (must
   equal their Creator Portal owner if they will publish), GitHub repository URL, and target platforms.
2. Scaffold. Prefer the CLI, which also fills publication metadata:
   ```bash
   macrodeck-plugin new --name "Acme Light Control" --id com.acme.light-control \
     --publisher "Acme" --project-name Acme.LightControl --yes
   ```
   Without the CLI: `dotnet new install "MacroDeck.Plugin.Templates@*-*"` then
   `dotnet new macrodeck-plugin -n Acme.LightControl -o Acme.LightControl --pluginId com.acme.light-control --pluginName "Acme Light Control"`.
   If neither tool is available in your environment, write the files by hand from `references/template.md`
   (rename `MacroDeck.PluginTemplate` everywhere, including `AssemblyName`, `RootNamespace` and the
   `entrypoints` paths, which must change together).
3. Replace the example `LogMessageAction` with the plugin's real first action, and its `Strings.resx` keys
   with real ones. Do not grow the template into a second sample.
4. Add capabilities one at a time (workflow B), each with a test.
5. Verify (see "Verification loop"), then hand over: what was built, how to run it, what is left.

### B. Add a capability to an existing plugin

1. Map the user's goal to a capability with the table in `references/cheatsheet.md` ("Which interface"), and
   read that capability's doc page.
2. Find the closest sample in `references/samples/README.md` and read its implementation. Mirror its shape.
3. Implement it on the integration class (or a definition class the integration lists). Add every string to
   `Strings.resx` first, then use the generated `Strings.*` members.
4. If the change affects a catalogue the host caches (variables, events, profiles, instances) after
   `InitializeAsync` or a config change, call `IPluginCatalogNotifier.CatalogChanged(kind)`.
5. Add a `PluginTestHarness` test for the new behaviour, including a failure path.
6. Verify.

### C. Debug or fix an existing plugin

Read the *Troubleshooting* and *Debugging plugins* sections of `references/docs/guides.md`; most first-run
problems (no pairing prompt, `ready` stays 503, manifest not found, `409` already registered, close code
`4000`, unhealthy installed plugin) are in their tables. For build errors with `MDP`/`MDLOC`/`MDC` codes, read
the *Analyzers* or *Conformance suite* section of `references/docs/reference.md` and fix the cause
rather than suppressing it. `Build()` throws one `PluginConfigurationException` listing every problem: read
all of it before changing anything.

### D. Package and publish

1. `macrodeck-plugin build --output ../../artifacts` from the directory holding `manifest.json` (it builds
   every platform and packs; never zip by hand, and never pack a `dotnet build -c Release` output).
2. `macrodeck-plugin validate --level publication --artifact <file>` and
   `macrodeck-plugin test --artifact <file>`.
3. Run the **Store gate** below.
4. Publish with the release workflow in the *Publishing to the Store* section of `references/docs/guides.md`
   (`Macro-Deck-App/GitHub-Actions/.github/workflows/publish-plugin.yml@v1`, triggered by a GitHub
   release). The release tag sets the version. Never add signing keys or a manual upload: the Creator Portal
   signs server-side. Creator Portal steps are in `references/docs/creator-portal.md`.

### E. Not .NET, or protocol-level work

A plugin can be written in any language that speaks the plugin protocol, and some tasks (custom hosts,
debugging the wire) need it. In `references/docs/reference.md`, start at the *Plugin protocol* section, then
*Authentication*, *WebSocket reference*, the REST pages on docs.macro-deck.app/reference/rest/, and
*Conformance suite*. Recommend the .NET SDK unless the user has
a real reason not to: it implements negotiation, sessions, reconnection, heartbeats and backpressure, and a
hand-rolled client must still pass the same conformance suite.

## Rules that matter most

These are the mistakes that compile fine and break at runtime or at Store review. The full rulebook, with
the reasons, is `references/agent-rules.md`.

- **Identity is the manifest.** No `Id`/`Name`/`Version` on the integration, no `WithId()` on the builder.
- **Ids are local, stable and kebab-case** (`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`, max 64, never `::`). Action,
  event, variable, state and widget-type ids are persisted in users' profiles: never rename a shipped one.
  Action ids are unique across the whole plugin.
- **Constructors and capability lists are side-effect free.** `Actions` and friends are read before
  `InitializeAsync`, and `Build()` constructs everything during validation. Connect in `InitializeAsync`,
  release in `ShutdownAsync`.
- **`InitializeAsync` runs more than once** (after reconnects and config changes). Make it idempotent;
  unsubscribe event handlers before resubscribing.
- **Results are truthful.** `ActionResult.Success()` only when it really happened; `Failed(ActionErrorCodes.X,
  localized message)` otherwise; `Accepted` only when the provider genuinely cannot confirm. Forward
  `context.CancellationToken` into every await. Bound any wait.
- **Never block.** No `.Result`, `.Wait()`, `GetAwaiter().GetResult()`, `Thread.Sleep` or `async void` in SDK
  contract types (MDP3001-3003). Invocations run concurrently: synchronize shared state.
- **Polled members are cheap and cached.** `GetActionStateAsync`, `GetIssuesAsync`, variable `ReadAsync`:
  answer from state you hold; never connect or authenticate there.
- **No user-facing literals.** Every label, name, description, error and state label is a `Strings.resx` key
  (dotted names, named placeholders). Reuse `MacroDeckStrings` (`Common.*`, `States.*`, `Validation.*`)
  before adding generic keys. Log messages stay English literals. Keep
  `.UseLocalization(Strings.LocalizationCatalog)` in `Program.cs`, or every label renders as `[[plugin:...]]`.
- **Secrets**: collect with `ActionParameter.Secret`, store as `ConfigFlowValue.Secret`, read with
  `GetSecretAsync`, never log them. OAuth goes through `ConfigFlowResult.External`, never your own listener.
- **Never set the listener URL** (`UseUrls`, `ASPNETCORE_URLS`, `applicationUrl`); never map routes under
  `/_macrodeck/`. Write files only under `MACRO_DECK_PLUGIN_DATA_DIRECTORY`.
- **Log with Serilog** (`ILogger` injected, `.ForContext<T>()`), message templates not interpolation, and no
  extra console sink (lines would print twice).
- **Keep `manifest.json` entrypoints and `macrodeck-build.json` targets in lockstep**; never hand-edit
  `files[]` or `languages` (the tooling writes them).

## Verification loop

Run what applies, in order, and report the results honestly. If your environment cannot run `dotnet` (no
SDK, no network to NuGet), say so plainly, list the exact commands the user should run, and review your code
against the cheatsheet and the relevant doc pages instead of claiming it builds.

```bash
dotnet build                                   # warning-free; analyzers catch most contract mistakes
dotnet test                                    # PluginTestHarness tests
macrodeck-plugin run --project src/<Name> --stub-host        # look for "Session established"
macrodeck-plugin test --project src/<Name>                   # conformance; every Required check must pass
```

Against the real desktop app: Developer Mode on, then the **Macro Deck - Real Host** launch profile (F5) or
`macrodeck-plugin run --project src/<Name>`, and approve the pairing prompt. Restart the plugin after changing
its capability lists so the host re-reads them.

## Versions: check before you trust a number

- Everything is prerelease until 3.0 ships. Add `--prerelease` (or an exact `--version`) to every
  `dotnet tool install` and `dotnet add package`.
- `dotnet tool install --global MacroDeck.Plugin.Cli --prerelease` can pick an **older** build, because SemVer
  sorts `beta` before `preview`. Install the CLI by exact version, matching the SDK version the project
  resolves.
- The Store enforces a minimum SDK and CLI version and an allow-list of `MacroDeck.*` packages. Read them live
  from `https://api.macro-deck.app/api/v1/public/dependency-policy/sdk` (fields `minimumSdkVersion`,
  `minimumCliVersion`, `allowedMacroDeckPackages`). At the last sync both minimums were `3.0.0-beta.15`, and
  the bundled sample plugins pin an older SDK, so do not copy their version pin into a project you will publish.

## Store gate (before any release)

The Creator Portal refuses builds that break its policy, and the policy changes, so fetch it fresh each time:

| What | URL |
| --- | --- |
| Creator Guidelines (Markdown) | `https://api.macro-deck.app/api/v1/public/creator-guidelines` |
| Blocked packages (JSON) | `https://api.macro-deck.app/api/v1/public/dependency-policy/blocked-packages` |
| Minimum SDK and allowed Macro Deck packages (JSON) | `https://api.macro-deck.app/api/v1/public/dependency-policy/sdk` |

`scripts/store_gate.py` automates the mechanical checks (manifest publication fields and placeholders,
SDK minimum, allowed `MacroDeck.*` packages, blocked packages across the transitive graph). Run it from the
plugin's solution directory; it needs network access and, for the package checks, the `dotnet` CLI:

```bash
python3 <skill-dir>/scripts/store_gate.py --project src/<Name>
```

If the shell cannot reach `api.macro-deck.app` (some sandboxes and proxies block it), fetch the two JSON
documents with a web-fetch tool, save them, and pass `--sdk-policy sdk.json --blocked-policy blocked.json`.
Without `dotnet`, pass the output of `dotnet list <csproj> package --include-transitive --format json` with
`--packages-json`. Exit 1 means a check failed; 3 means the policy could not be read, so stop rather than
assume it is unchanged.

Then check by reading what a script cannot: the Creator Guidelines (public GitHub repo with an OSI licence,
no bundled precompiled third-party binaries, no "Macro Deck" or third-party brand in the id or a name that
implies endorsement, AI use declared in the manifest's `ai` block, honest Store description and icon), and a
conformance report for every platform in `entrypoints`. Report each point as holding or not; never claim the
gate passed without having fetched the documents.

## Talking to the user

Many plugin authors are experienced C# developers; some are hobbyists automating their stream setup. Match
their level. When you finish a change, say what you built, what you verified (and what you could not), and
the one next step that matters, such as "run `macrodeck-plugin test` and approve the pairing prompt".
