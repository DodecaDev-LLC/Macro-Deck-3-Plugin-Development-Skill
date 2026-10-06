# Guides: debugging, publishing, troubleshooting

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Debugging plugins: https://docs.macro-deck.app/guides/debugging/
- Publishing to the Store: https://docs.macro-deck.app/guides/publishing/
- Troubleshooting: https://docs.macro-deck.app/guides/troubleshooting/

## Debugging plugins

> Source: https://docs.macro-deck.app/guides/debugging/
>
> Hit a breakpoint in a .NET plugin from Rider, Visual Studio or VS Code, against the desktop app or a disposable stub host.

Put a breakpoint in your plugin and run it under your IDE, against the desktop app or a throwaway stub host.

### Quick start

`macrodeck-plugin new` already generates this profile in `src/<Name>/Properties/launchSettings.json`:

```json
{
  "$schema": "https://json.schemastore.org/launchsettings.json",
  "profiles": {
    "Macro Deck - Real Host": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": false,
      "workingDirectory": "$(ProjectDir)",
      "environmentVariables": {
        "DOTNET_ENVIRONMENT": "Development",
        "MACRO_DECK_PLUGIN_MODE": "SelfRegistering",
        "MACRO_DECK_PLUGIN_HOST_URL": "http://127.0.0.1:8193",
        "MACRO_DECK_PLUGIN_STATE_DIRECTORY": ".macrodeck-dev-state"
      }
    }
  }
}
```

1. Start the Macro Deck desktop app and turn on **Developer Mode** in its settings (off by default).
2. Open the solution, pick **Macro Deck - Real Host**, and press F5 in Rider or Visual Studio (VS Code:
   see [below](#vs-code)).
3. Approve the pairing prompt in the desktop app.

The plugin asks the desktop app to pair, and after you approve it stores its own credential in
`.macrodeck-dev-state/`. Later runs connect without a prompt.

### Run against the desktop app

Use the Quick start profile, or from the plugin project directory:

```bash
dotnet run --launch-profile "Macro Deck - Real Host"
```

- The desktop app must run on the same machine: plugin endpoints reject non-loopback callers.
- `SelfRegistering` is the only mode an independently started plugin can use against a real host. Managed
  mode needs a bootstrap token only the real supervisor can mint.
- `MACRO_DECK_PLUGIN_HOST_URL` is the **host's** address, not the plugin's own listener.
- `.macrodeck-dev-state` resolves against the profile's working directory, the project directory.
- Never set `ASPNETCORE_URLS`, `applicationUrl`, `UseUrls(...)` or a `urls` value. The SDK binds to
  `http://127.0.0.1:0`; an installed plugin's listener is chosen and probed by the supervisor.
  [MDP4002](https://docs.macro-deck.app/reference/analyzers/#mdp4002) catches the visible forms.

Breakpoints in `Program.cs` hit at process start. `IPluginIntegration.InitializeAsync` runs only once a
session opens, and action handlers only when triggered from Macro Deck.

### Live reload while you work

```bash
dotnet watch --non-interactive run --launch-profile "Macro Deck - Real Host"
```

Run this from the plugin project directory and leave a [developer preview](https://docs.macro-deck.app/ui/views/developer-preview/#iterating-on-a-preview)
open in Macro Deck. When you save, `dotnet watch` applies the change with .NET Hot Reload and the open
preview updates in place. Widgets on the deck and open configuration views of your plugin are opened again
with the new code, keeping unsaved configuration changes; see
[Real views](https://docs.macro-deck.app/ui/views/developer-preview/#real-views). A change Hot Reload cannot apply restarts the plugin;
without `--non-interactive`, `dotnet watch` asks first. The preview waits and reopens by itself, and the credential in
`.macrodeck-dev-state` means no new pairing prompt.

Rider and Visual Studio do the same with their Hot Reload button while debugging.
[`macrodeck-plugin run --project . --watch`](https://docs.macro-deck.app/cli/run/#watching-for-changes) is the equivalent without an
IDE profile.

### Run against the stub host

```bash
macrodeck-plugin run --project . --stub-host
```

```text
Started a disposable stub host at http://127.0.0.1:59826.
Started process 38264 (mode: SelfRegistering, host: http://127.0.0.1:59826). Press Ctrl-C to stop.
[plugin] info: Microsoft.Hosting.Lifetime[14]
[plugin]       Now listening on: "http://127.0.0.1:59827"
...
[plugin]       Registered with the host as '"com.example.demo"'.
...
[plugin]       Initialized.
```

No Macro Deck install, no Developer Mode, no pairing. The stub is a real in-process `MacroDeckTestHost`
with the real registration, session and WebSocket implementation, and `run` composes the same
environment as the supervisor. Use it for registration, reconnect and shutdown; use the desktop app when
the real UI matters. Without `--stub-host`, `run` connects to the running desktop app instead. Every
option is in [`macrodeck-plugin run`](https://docs.macro-deck.app/cli/run/).

### Attach to a process started by `run`

`run` is the parent; your plugin is a separate .NET child. Debugging the CLI alone binds nothing.

1. Start `run` and note the PID in `Started process <pid>`.
2. Attach the IDE's .NET (CoreCLR) debugger to that PID. A framework-dependent plugin may show as
   `dotnet`: match the PID, or the command line ending in your plugin's DLL.

`run --project` makes a normal Debug build, so the PDB is present. A hollow breakpoint usually means you
attached to the CLI or to a previous run's child.

### VS Code

`.vscode/launch.json`, with the C# extension, after `dotnet build`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Macro Deck - Real Host",
      "type": "coreclr",
      "request": "launch",
      "program": "${workspaceFolder}/src/Demo/bin/Debug/net10.0/Demo.dll",
      "cwd": "${workspaceFolder}/src/Demo",
      "env": {
        "DOTNET_ENVIRONMENT": "Development",
        "MACRO_DECK_PLUGIN_MODE": "SelfRegistering",
        "MACRO_DECK_PLUGIN_HOST_URL": "http://127.0.0.1:8193",
        "MACRO_DECK_PLUGIN_STATE_DIRECTORY": ".macrodeck-dev-state"
      }
    },
    {
      "name": "Attach to plugin",
      "type": "coreclr",
      "request": "attach",
      "processId": "${command:pickProcess}"
    }
  ]
}
```

Replace `Demo` with your project name. Keep `cwd` on the project directory: the SDK reads
`manifest.json` from there. Use **Attach to plugin** for a child started by `run`.

### Rider

- **Desktop app:** choose the **Macro Deck - Real Host** launch profile and Debug.
- **Stub host:** create a .NET Executable configuration for `macrodeck-plugin` with arguments
  `run --project . --stub-host`, working directory the plugin project, and enable **Attach to child .NET
  processes**. The tool must be on Rider's `PATH`, or use its absolute path and keep that change
  private.

### Visual Studio

- **Desktop app:** select **Macro Deck - Real Host** in the start button's drop-down and press F5.
- **Stub host:** start `run` in a terminal, then **Debug → Attach to Process** and pick the child PID.

### Developer Mode, pairing and Developer tokens

- **Developer Mode** gates pairing, enrolment and every session for a development credential. It
  persists, and toggling it takes effect without restarting the plugin or Macro Deck.
- The SDK creates the pairing request, waits for approval, redeems it and writes the per-plugin secret
  to `.macrodeck-dev-state/<plugin-id>/credentials.json` before using it. The file also records the
  issuing host, for reference only: the plugin always connects to `MACRO_DECK_PLUGIN_HOST_URL`, so the
  credential keeps working when Macro Deck moves to another port. It is owner-only on Unix, inherits the
  directory ACL on Windows, and is **not encrypted at rest**.
- The generated `.gitignore` already ignores `**/.macrodeck-dev-state/`. Keep that rule: the directory
  holds the long-lived secret and fallback logs. `launchSettings.json` holds no secret and can be
  committed.

Full protocol: [Authentication](https://docs.macro-deck.app/reference/authentication/).

#### Advanced: enroll with a Developer token for headless runs

For CI and other runs with nobody to approve a prompt. It replaces the prompt, not Developer Mode, and is
needed only while the state directory has no stored credential.

Create a token under **Developer Tools → Plugin development → Credentials**. The plaintext is shown once.
Run once from a terminal with the token only in the environment (zsh):

```bash
read -s "MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN?Enrollment token: "
export MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN
echo
MACRO_DECK_PLUGIN_MODE=SelfRegistering \
  MACRO_DECK_PLUGIN_HOST_URL=http://127.0.0.1:8193 \
  MACRO_DECK_PLUGIN_STATE_DIRECTORY=.macrodeck-dev-state \
  dotnet run
unset MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN
```

Bash: `read -rsp "Enrollment token: " MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN`. PowerShell 7:

```powershell
$env:MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN = Read-Host "Enrollment token" -MaskInput
$env:MACRO_DECK_PLUGIN_MODE = "SelfRegistering"
$env:MACRO_DECK_PLUGIN_HOST_URL = "http://127.0.0.1:8193"
$env:MACRO_DECK_PLUGIN_STATE_DIRECTORY = ".macrodeck-dev-state"
dotnet run
Remove-Item Env:MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN, Env:MACRO_DECK_PLUGIN_MODE, Env:MACRO_DECK_PLUGIN_HOST_URL, Env:MACRO_DECK_PLUGIN_STATE_DIRECTORY
```

Stop once `/_macrodeck/ready` returns 200 or the log says it registered. The SDK has swapped the token
for a per-plugin secret in the same `credentials.json`; later IDE runs need no token.

:::caution
Never put the token in `launchSettings.json`, User Secrets, CLI arguments or other persisted config:
shell history, process lists and screenshots expose it. Discard the plaintext, but keep the token
**active** in Macro Deck: revoking or letting it expire stops every registration it enrolled. Removing a
revoked token from the list also deletes those registrations. Don't delete `credentials.json` to get rid
of the token - it holds the separate per-plugin secret.
:::

### Read logs while debugging

| Where | What you see |
| --- | --- |
| IDE console (direct launch) | Startup, unhandled failures, the plugin's own log output. |
| `macrodeck-plugin run` | `[plugin]` (stdout) and `[plugin:stderr]` (stderr) lines; against the stub also `[log:...]` forwarded events. |
| Desktop app log viewer | Events forwarded by `.UseMacroDeckLogging()` (the template calls it), default minimum `Information`. |
| `.macrodeck-dev-state/<plugin-id>/logs/plugin-fallback.log` | The bounded tail of batches that could not be delivered. Never replayed. |

`.UseMacroDeckLogging()` keeps writing to the console too, so an extra Serilog console sink prints every
line twice. Limits and levels: [Logging and health](https://docs.macro-deck.app/features/logging/).

The plugin's own routes, on its `Now listening on` port (never `8193`, which is the host):

```bash
curl -i http://127.0.0.1:<plugin-port>/_macrodeck/health       # 200 once serving: liveness only
curl -i http://127.0.0.1:<plugin-port>/_macrodeck/ready        # 200 once a session is open, else 503
curl -s http://127.0.0.1:<plugin-port>/_macrodeck/info         # identity, mode, SDK and protocol version
curl -s http://127.0.0.1:<plugin-port>/_macrodeck/diagnostics  # status, faultReason, session, reconnects, close code
```

### Common first-run failures

| Symptom | Fix |
| --- | --- |
| No pairing prompt | Turn on Developer Mode (no restart needed; the plugin pairs on its next reconnect and says so on stderr). Check `MACRO_DECK_PLUGIN_HOST_URL` points at this desktop app. Prompts appear only in the desktop app, with a system notification and a notification-list entry. |
| `health` 200, `ready` 503 | No session. Read `diagnostics.status` and `faultReason`; check the host runs, the URL is loopback and the credential belongs to this host. An unreachable host is retried with backoff, not a startup error. |
| "No stored credential and no enrollment token" | Headless path only: token exported in the same shell, exact name `MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN`, mode `SelfRegistering` with the loopback host URL, working directory the project. |
| Already registered (`409`) | See [below](#registration-is-refused-as-already-registered). |
| WebSocket closes with `4000` (`SESSION_REPLACED`) | One live session per plugin id: stop the other debug run. |
| Plugin is already installed in Macro Deck | Approve the takeover in the prompt: see [Debug an installed plugin](#debug-an-installed-plugin). |
| Installed plugin reported unhealthy | Remove every listener override; check the manifest's `health.path` (default `/_macrodeck/health`) and timeouts. |
| Manifest not found | The SDK reads `manifest.json` from the content root: keep it at the project root and copy it to output (below). Don't override the profile's working directory with an absolute path. |
| Breakpoint in `InitializeAsync` never hits | Check `ready` and `diagnostics`: the process may still be reconnecting. |
| Logs local but not in the host viewer | `.UseMacroDeckLogging()` called, `ready` is 200, event meets `MacroDeck:Plugin:Logging:MinimumLevel`; then read `plugin-fallback.log`. |

```xml
<ItemGroup>
    <Content Include="manifest.json" CopyToOutputDirectory="PreserveNewest" />
    <Content Include="Assets\icon.svg" CopyToOutputDirectory="PreserveNewest" />
</ItemGroup>
```

More symptoms, including rejected or expired pairing and `429`: [Troubleshooting](https://docs.macro-deck.app/guides/troubleshooting/#pairing).

#### Registration is refused as already registered

The host knows this plugin id, but your `credentials.json` is gone (deleted state directory, fresh clone).
Run again with Developer Mode on and approve **replace the development credential** in the prompt. The
host rotates in the new secret and ends the old sessions; no manual revocation.

If the refusal says the plugin is installed (`details.reason: "plugin_installed"`), the build enrolled
with a Developer token. That headless path never takes over an installed plugin. Unset
`MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN` and pair interactively with Developer Mode on (see
[Debug an installed plugin](#debug-an-installed-plugin)), or uninstall the plugin first.

#### Debug an installed plugin

Run the development build as usual, with Developer Mode on. If Macro Deck already has a plugin with the
same id installed, the prompt asks you to approve the pairing **and** to confirm that the build takes
over the installed plugin. Read the warning: your unverified build gets the installed plugin's settings
and stored credentials.

While the takeover lasts:

- the installed copy is stopped, and Macro Deck does not start it again;
- installing or updating the plugin is refused;
- the build is listed under **Paired plugins** on the Developer page and shown as unverified;
- the Store shows the plugin as running a development build instead of verified.

The takeover ends, and the installed copy starts again, when you revoke the build under **Paired
plugins**, switch Developer Mode off, uninstall the plugin, or restart Macro Deck. Nothing about it is
saved. Uninstalling during a takeover can fail on Windows while the installed copy is still shutting
down; try again after a minute.

The next debug run after a takeover ended asks again by itself: when the host rejects the stored
credential before the plugin has connected, the SDK pairs once and replaces `credentials.json`. Builds
on an older SDK stop with an authentication error instead. Delete
`.macrodeck-dev-state/<plugin-id>/credentials.json` and run again.

#### If credentials leak

- **`credentials.json` committed or shared:** delete it locally, run again and approve **replace the
  development credential**. Removing it from the next commit is not enough.
- **Developer token exposed:** revoke it (which invalidates its registrations), delete `credentials.json`,
  create a new token and enroll again.

### See also

- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - registration modes and every `MACRO_DECK_PLUGIN_*` variable.
- [Authentication](https://docs.macro-deck.app/reference/authentication/) - pairing, Developer tokens, stored credentials.
- [Logging and health](https://docs.macro-deck.app/features/logging/) - forwarding, fallback log, health probes.
- [`macrodeck-plugin run`](https://docs.macro-deck.app/cli/run/) - every option and exit code.
- [Troubleshooting](https://docs.macro-deck.app/guides/troubleshooting/) - error codes by stage.

## Publishing to the Store

> Source: https://docs.macro-deck.app/guides/publishing/
>
> How a plugin reaches the Macro Deck Store - checks before you publish, the release workflow, signing and updates.

A GitHub release runs the Macro Deck publishing workflow, which uploads an unsigned build to the
[Creator Portal](https://docs.macro-deck.app/creator-portal/). The Portal signs and publishes it after review - you never hold a
signing key. The step-by-step guide is [Publish a plugin](https://docs.macro-deck.app/creator-portal/publish-plugin/).

### Before you publish

Run each check on the build output, not the project directory:

- **Store metadata is complete** - `description`, `icon`, `license`, `repository`, `compatibility` and
  `publisher.name` are filled in ([manifest reference](https://docs.macro-deck.app/reference/manifest/#requirement-categories)):

  ```bash
  macrodeck-plugin validate --level publication --artifact ./artifacts/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin
  ```

  Exit `1` means a field is missing. `build` and `pack` only warn about these fields; the Creator Portal
  applies the same check at upload.
- **AI use is declared** - a plugin that lets users interact with an AI system, generates content with AI,
  or ships assets created with AI says so in `ai` ([manifest reference](https://docs.macro-deck.app/reference/manifest/#ai)). Without
  it, the plugin's Store page says its publisher has not declared whether it uses AI.
- **The artifact passes conformance** ([conformance suite](https://docs.macro-deck.app/reference/conformance/)):

  ```bash
  macrodeck-plugin test --artifact ./artifacts/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin
  ```

- **`id` equals the Project's Package ID** in the Creator Portal. The upload selects the Project by it.

### Publish with the release workflow

Save as `.github/workflows/release.yml`:

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  publish:
    uses: Macro-Deck-App/GitHub-Actions/.github/workflows/publish-plugin.yml@v1
    permissions:
      contents: read
      id-token: write
    with:
      version: ${{ github.event.release.tag_name }}
      source: src/HelloDeck
      changelog: ${{ github.event.release.body }}
```

How the trust chain works:

1. You connect your public repository to the Project in the Creator Portal.
2. The workflow authenticates with the short-lived token GitHub issues for the run. It proves which
   repository, commit and workflow built the package. It is not a secret you store.
3. The Portal accepts the build only from `publish-plugin.yml` and only for the connected repository.
4. After review, the Portal signs the package server-side and publishes it.

What the workflow must never do:

- **Sign anything.** No signing key, certificate or signing credential belongs in your repository, your CI
  configuration or your CI provider's secret store. If a publishing setup asks you for one, it is not this
  one.
- **Replace the release workflow with a manual upload.** A plugin package cannot be uploaded by hand.

See the [release workflow reference](https://docs.macro-deck.app/creator-portal/release-workflow/) for all inputs.

### Release a new version

```bash
gh release create v1.1.0 --notes "- Fix the greeting on light themes"
```

- The version comes from the release tag, not from `manifest.json`: the workflow writes it into the
  manifest. `v1.1.0` becomes `1.1.0` (SemVer 2.0).
- Every release goes through review again. Because the Store distributes the artifact the Portal
  signed, nobody can silently replace or modify an approved package.

### What the Store signs

```bash
macrodeck-plugin verify ./downloads/com.example.hello-deck-1.1.0-linux-x64.macroDeckPlugin
```

- The Creator Portal is the only component that signs Store artifacts. It signs server-side, with keys that
  exist only in Macro Deck infrastructure. It also issues and revokes certificates. Plugin authors do
  neither, and the `macrodeck-plugin` CLI cannot do either.
- An artifact you pack is unsigned. That is what the Store expects to receive.
- [`verify`](https://docs.macro-deck.app/cli/signing/#verify) checks a signed artifact against the pinned Macro Deck root. It works
  offline and needs no credentials. A `valid` verdict is a cryptographic fact about the signature at signing
  time, not a live trust decision, and it does not check revocation. See the
  [security model](https://docs.macro-deck.app/policies/security/).
- [`keygen`](https://docs.macro-deck.app/cli/signing/#keygen) and [`sign`](https://docs.macro-deck.app/cli/signing/#sign) are for artifacts distributed outside
  the Store and for Macro Deck's own infrastructure. They are not part of publishing. Signing a plugin
  locally does not make it a Store artifact.

### How updates reach users

```text
installed 1.0.0  <  Store 1.1.0  ->  shown as an update
```

- When the Store catalogue refreshes, Macro Deck compares the installed version with the latest Store
  version by SemVer. It offers an update only if the Store version is higher. It never offers an update
  when either version fails to parse.
- An update is only reported to the user. It is never installed unsigned on their behalf. Once a plugin is
  installed as signed, an unsigned update to it is refused, even if the user consents.
- The host verifies every package before install and again before every launch. Editing files after
  installation stops the plugin from loading.

### Removing a plugin from the Store

Unlist the Project in the Creator Portal: the plugin disappears from the Store listing, installed copies
keep working and the package id stays yours. See [Review and release](https://docs.macro-deck.app/creator-portal/review/#unlist).

Macro Deck can remove a single version or the whole plugin; the signed registry lists each removed version.
Macro Deck never installs or offers an update to a removed version and warns users who have one installed,
with the reason and any suggested replacement. When the latest version is removed, the plugin disappears from
the Store and cannot be installed or updated; installed copies stay under **Installed** with a warning.

### See also

- [Publish a plugin](https://docs.macro-deck.app/creator-portal/publish-plugin/) - the Creator Portal steps with screenshots.
- [CI and automation](https://docs.macro-deck.app/cli/ci/) - build, validate and test on pull requests.
- [`macrodeck-plugin validate`](https://docs.macro-deck.app/cli/validate/) - levels and problem codes.
- [Signing packages](https://docs.macro-deck.app/cli/signing/) - `verify`, and `keygen`/`sign` outside the Store.
- [Manifest reference](https://docs.macro-deck.app/reference/manifest/) - `publisher` and the publication fields.
- [Security model](https://docs.macro-deck.app/policies/security/) - what a signature covers and what the host enforces.
- [ADR 0042](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0042-plugin-signing-and-trusted-publishing.md) -
  why signing is server-side and why creator keys never reach a developer machine or a CI runner.

## Troubleshooting

> Source: https://docs.macro-deck.app/guides/troubleshooting/
>
> Symptom-driven fixes for the failures a Macro Deck plugin actually hits - build, packaging, connection, runtime and installation - each tied to a real diagnostic.

Find the symptom, read the cause, apply the fix. For breakpoints and IDE launches, see
[Debugging plugins](https://docs.macro-deck.app/guides/debugging/).

### First steps

```bash
macrodeck-plugin validate --directory bin/Release/net10.0
```

Anything manifest-shaped. Reports every problem in one run; exit `1` is a bad manifest, `3` an unreadable one.

```bash
macrodeck-plugin inspect --artifact com.example.my-plugin-1.0.0.macroDeckPlugin
```

What installing an artifact would find: entrypoints per RID, compatibility, signature shape.

```bash
macrodeck-plugin run --project src/MyPlugin --stub-host
```

Anything connection-shaped. `Session established` means registration, session and WebSocket all work.

```bash
tail -f ~/Library/Application\ Support/MacroDeck/logs/host-$(date +%Y%m%d).log
```

The host log, which includes your plugin's forwarded lines. Windows: `%APPDATA%\MacroDeck\logs`, Linux:
`~/.local/share/MacroDeck/logs`. Check the file names in that folder; see [where the lines end up](https://docs.macro-deck.app/features/logging/#where-the-lines-end-up).

### Installing the CLI

#### `dotnet tool install` finds no package

Only `-preview` versions are published before 3.0, and `dotnet tool install` skips prereleases.

```bash
dotnet tool install --global MacroDeck.Plugin.Cli --prerelease
```

#### `run` or `test` reports it cannot find `Microsoft.AspNetCore.App`

`run` and `test` start a real Kestrel loopback host, so they need the ASP.NET Core shared framework. Install
the ASP.NET Core runtime, or the .NET SDK.

#### A mistyped command prints one confusing line

```text
$ macrodeck-plugin pakc --source .
error unknown-command: 'pakc' is not a macrodeck-plugin command. Did you mean 'pack'?
```

Not a fault: one line and exit `2` (usage error), not one error per option after the typo.

### Building the plugin

#### `Build()` throws `PluginConfigurationException`

```text
The plugin is not configured correctly:
  - <problem>
  - <problem>
```

`Build()` validates everything local and throws once with every problem: a missing or malformed plugin id,
an illegal or duplicated capability id, a route under `/_macrodeck`, a missing or unreadable icon, a service
graph that will not resolve. Read the whole list and fix it in one pass. Connectivity is never checked here:
an absent host is a retry, not a configuration error.

#### `Build()` fails naming `manifest.json`

The SDK reads the manifest from the content root and it is not there: the `Content` item is missing, or
you ran the executable from another working directory.

```xml
<ItemGroup>
    <Content Include="manifest.json" CopyToOutputDirectory="PreserveNewest" />
    <Content Include="Assets\icon.svg" CopyToOutputDirectory="PreserveNewest" />
</ItemGroup>
```

Running a built plugin by hand from elsewhere needs `--contentRoot <dir>`: the content root defaults to the
working directory, not the executable's folder.

#### `WithId` / `WithName` / `WithVersion` / `WithDescription` / `WithIcon` do not compile

They were removed. Move the values into `manifest.json` as `id`, `name`, `version`, `description` and
`icon`, and add the `Content` items above.

#### Two integrations declare the same action id

On the wire an action belongs to the plugin, so its id must be unique across every integration in the
process. `Build()` fails naming the id; [MDP2001](https://docs.macro-deck.app/reference/analyzers/#mdp2001) catches constant ids at
compile time. Rename one.

#### The analyzers flag something you did not expect

| Id | Meaning |
| --- | --- |
| [MDP1001](https://docs.macro-deck.app/reference/analyzers/#mdp1001) | `manifest.json` declares no usable `id`, or no `name`/`version`. |
| [MDP1003](https://docs.macro-deck.app/reference/analyzers/#mdp1003) | The manifest's `icon` has an extension with no known media type. |
| [MDP1004](https://docs.macro-deck.app/reference/analyzers/#mdp1004) | Your `IPluginIntegration` restates manifest-owned identity. |
| [MDP2005](https://docs.macro-deck.app/reference/analyzers/#mdp2005) | You mapped a route under the reserved `/_macrodeck` prefix. |
| [MDP3002](https://docs.macro-deck.app/reference/analyzers/#mdp3002) | `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` or `Thread.Sleep` in a handler type. |
| [MDP4001](https://docs.macro-deck.app/reference/analyzers/#mdp4001) | A singleton takes `ICapabilityInvocationContext`, which only resolves inside one invocation's scope. |
| [MDP4002](https://docs.macro-deck.app/reference/analyzers/#mdp4002) | You override your own listener URL - see [below](#the-supervisor-reports-the-plugin-unhealthy-but-it-is-running-fine). |
| [MDP5004](https://docs.macro-deck.app/reference/analyzers/#mdp5004) | An API whose declared removal version this SDK has reached. |

Each id can be suppressed or escalated on its own: `<NoWarn>MDP2003</NoWarn>`, `-warnaserror:MDP5001`.

### Validating and packaging

#### `validate` reports an error

```text
error invalid-version: '1.0' is not a valid SemVer version. [/version]
warning unknown-permission: 'host:everything' is not a known permission. [/permissions/0]

com.example.my-plugin 1.0: 1 error(s), 1 warning(s).
```

`validate` prints `error <code>: <message>` lines on stdout, with a JSON pointer where there is one.

| Code | Meaning | Fix |
| --- | --- | --- |
| `manifest-not-found` (exit `3`) | No `manifest.json` at the path, or run from the wrong directory. | Point at the build output: `--manifest bin/Release/net10.0/manifest.json`. |
| `malformed` | Not valid JSON; the message names a 1-based line and position. | Fix the JSON there. |
| `invalid-version` | `version` is not SemVer 2.0: `"1.0"` and `"v1.0.0"` fail. | Use `1.0.0`. |
| `invalid-plugin-id` | `id` is not reverse-domain: two or more dot-separated segments, lowercase, no underscores. | `com.example.my-plugin`. |
| `id-mismatch`, `version-mismatch` | The manifest disagrees with the directories it is installed under. | Match `<id>/versions/<version>/`. |
| `unknown-permission` | A permission outside the vocabulary. Advisory: it still installs. | Check [the vocabulary](https://docs.macro-deck.app/reference/manifest/#permissions). |
| `invalid-additional-link` | An `additionalLinks` entry has no `type` or `url`, a URL that is not absolute `http`/`https`, a `custom` link without a `label`, a `label` on a standard type, or repeats a URL, type or label. | Follow [the rules](https://docs.macro-deck.app/reference/manifest/#additionallinks). |
| `unknown-link-type` | An `additionalLinks` type outside the standard list. Advisory: it installs, but the Store does not show the link. | Use a standard type or `custom` with a `label`. |
| `file-missing`, `file-size-mismatch`, `file-digest-mismatch` | `files[]` disagrees with the disk. | Do not hand-write `files[]`; let `pack` recompute it. |
| `undeclared-file` | A file in the artifact that `files[]` omits; once present, `files[]` is a complete inventory. | Repack. |
| `not-an-artifact` (exit `3`) | `--artifact` is not a ZIP, often a `manifest.json`. | Use `--manifest`; the CLI suggests it. |
| `source-directory` | Pointed at a source tree: `manifest.json` next to a `.csproj` with no built entrypoint. | Build, then validate the output directory. |
| `no-selector`, `too-many-selectors` (from `inspect`) | `inspect` needs exactly one of `--artifact`/`--directory`, with no default. | Pass exactly one. |

```text
error not-an-artifact: '.../manifest.json' is not a .macroDeckPlugin artifact (not a ZIP archive). Did you mean validate --manifest?
```

#### `pack` prints warnings

None changes the exit code.

| Warning | Meaning |
| --- | --- |
| `entrypoint-not-packed` | A declared RID's binary is not in the payload. Packing only your own platform is a legitimate intermediate state. |
| `source-looks-like-debug-build` | `--source` looks like `bin/Debug/...`. Pack a Release build for distribution. |
| `languages-recomputed` | The declared `languages` disagree with `Localization/*.resx`; the resource files win, and the message names both lists. |
| `plugin-id-generated` (from `run`) | No `--plugin-id` and no manifest id, so a development id was invented. |

#### `pack` fails

| Code | Fix |
| --- | --- |
| `source-not-found` | Point `--source` at an existing payload directory. |
| `output-exists` | Add `--force`. |
| `source-entry-rejected` | Remove the symlink or unsafe path. |
| `limit-exceeded` | Trim the payload below the artifact size/entry limits. |
| `write-failed` | Check the output location is writable. |
| `manifest-invalid` | Fix the manifest; `pack` prints the same report as `validate` and writes nothing. |

#### A signature stopped verifying after packing

`pack` recomputes `files[]` and passes an existing `signature` through, so a manifest signed before packing
no longer matches its own digest. Sign after packing; `pack --show-digest` and `inspect --show-digest` print
the exact bytes a signature covers.

### Starting and connecting

#### The plugin starts but never connects, and keeps retrying

Expected: a plugin starts without a host and retries with full-jitter exponential backoff (1s initial, 30s
maximum, factor 2). To fail instead:

```json
{ "MacroDeck": { "Plugin": { "FailFastOnFirstConnect": true } } }
```

#### `host-not-found`

```text
error host-not-found: No running Macro Deck host was found. Its loopback port file is written while the host runs and removed when it stops; none was readable at ... Start Macro Deck, pass --host-url <url>, or use --stub-host to run against a disposable stub host instead.
```

`run` finds the host through `macro-deck-host.port` (or `macro-deck-host-development.port`) in the system
temp directory, which exists only while the host runs.

```bash
macrodeck-plugin run --project src/MyPlugin --stub-host                        # no Macro Deck needed
macrodeck-plugin run --project src/MyPlugin --host-url http://127.0.0.1:5000   # a host run cannot discover
```

#### `run --mode managed` is refused

```text
error managed-needs-stub-host: Managed mode needs a launch bootstrap token only a real supervisor can mint - run cannot manufacture one against a real host. Use --stub-host, or --mode self-registering (the default) against the running host.
```

Add `--stub-host`. Against a real host use the default `--mode self-registering`, or the direct-project
workflow in [Debugging plugins](https://docs.macro-deck.app/guides/debugging/), which keeps a Developer token out of history and the
process list.

#### `watch-needs-project` or `watch-needs-real-host`

`run --watch` rebuilds from source against the running Macro Deck. Pass `--project` instead of
`--executable` or `--artifact`, and drop `--stub-host`. See
[Watching for changes](https://docs.macro-deck.app/cli/run/#watching-for-changes).

#### `developer-mode-disabled`

`run` asked the host and Developer Mode is off, so no approval prompt can appear. Turn it on under
**Settings > Developer**. Nothing restarts: `run` stays up and the plugin pairs on its next reconnect.

#### `enrollment-token-required`

```text
error enrollment-token-required: --mode self-registering against a real host needs --enrollment-token when --pairing is off.
```

`--pairing false` with no `--enrollment-token`. Drop `--pairing false` and approve the prompt, or pass
`--enrollment-token`. An inherited `MACRO_DECK_PLUGIN_ENROLLMENT_TOKEN` is scrubbed from the child and does
not count. The option exposes the token in shell history, process lists and screenshots, so prefer the
masked one-time enrollment in [Debugging plugins](https://docs.macro-deck.app/guides/debugging/).

#### `UNAUTHENTICATED` (HTTP 401)

```text
Authentication failed.
```

Deliberately identical for an unknown plugin id, a wrong secret, a spent or expired bootstrap token, a
revoked registration, an unknown or expired Developer token and a missing header. Check:

- the `X-MacroDeck-Plugin-Id` and `X-MacroDeck-Plugin-Secret` headers are present and spelled correctly;
- a self-registered secret file was not deleted;
- the registration was not revoked;
- a managed launch token is used within two minutes; otherwise it needs a fresh launch;
- a development build that took over an installed plugin lost its credential when the takeover ended.
  Current SDKs pair again once by themselves; on an older SDK delete
  `.macrodeck-dev-state/<plugin-id>/credentials.json` and run again.

A `401` on the `/plugins/ws` upgrade, with "The plugin session no longer exists" in the host log, means
the host does not know the session the plugin presented: Macro Deck restarted, or the session token
expired. Current SDKs open a new session with the stored credential. An older SDK keeps presenting the
old session until it gets `429`, and never reconnects: update the SDK, or restart the plugin.

#### `UNAUTHENTICATED` with HTTP 403

The request was not from loopback, looked like a browser, or its session token names another session. Run
the plugin on the host's machine: both listeners serve plugin endpoints, but only to loopback callers.

`403` also means **Developer Mode** is off. That gates pairing (see [Pairing](#pairing)),
`POST /api/plugins/registration`, and `POST /api/plugins/sessions` for a plugin that enrolled with a
Developer token or paired - not a plugin Macro Deck installed and launches. Such a refusal carries
`"reason": "developer_mode_disabled"` in `details`, and
[`GET /api/plugins/protocol`](https://docs.macro-deck.app/reference/authentication/) reports `pairing.developerModeEnabled` and
`enrollment.developerModeEnabled`. Turn Developer Mode on; no restart.

#### `PLUGIN_ALREADY_REGISTERED` (HTTP 409)

```text
A plugin is already registered with this identity.
```

If `details.reason` is `plugin_installed`, Macro Deck has a plugin with this id installed and the build
enrolled with a Developer token. Only that headless path is refused: nobody confirms a takeover there.
Unset the token and run the build with Developer Mode on, so the prompt can ask you to take over the
installed plugin (see [Debug an installed plugin](https://docs.macro-deck.app/guides/debugging/#debug-an-installed-plugin)), or
uninstall the plugin first.

Otherwise a registration exists, but this machine or directory lost its `credentials.json`. Reuse the stored secret,
or run the plugin with Developer Mode on and let the pairing prompt **replace the development credential**
(it rotates the secret and ends the old session) - see
[Interactive pairing](https://docs.macro-deck.app/reference/authentication/#self-registering-interactive-pairing) and
[Registration is refused as already registered](https://docs.macro-deck.app/guides/debugging/#registration-is-refused-as-already-registered).
`DELETE /api/plugins/registration/{pluginId}` (admin: a login token, or the development host's loopback secret header
on the loopback port) still works but is no longer the recommended path.

#### `PROTOCOL_VERSION_UNSUPPORTED` (HTTP 422, or close `4001`)

```text
The requested protocol version is not supported.
```

No version in common; `details` carry the host's `supportedMinimum` and `supportedMaximum`. Widen your
declared range or update the SDK. A `4001` close means `session.hello` asserted a version other than the
negotiated one, which the SDK never does: suspect a hand-rolled client.

#### `RATE_LIMITED` (HTTP 429)

```text
Too many requests; retry after the given delay.
```

Too many enrollment or session attempts. Wait for `details.retryAfterSeconds` / `Retry-After`. Enrollment
shares one bucket; session exchange is keyed per plugin id; the `/plugins/ws` upgrade is keyed per session
id, so repeatedly presenting a session the host no longer knows ends here (see the `401` section above). A
reconnect loop without backoff keeps hitting it.

#### The socket closes with code…

| Code | Meaning | What to do |
| --- | --- | --- |
| `1013` | `QUEUE_OVERFLOW`: you ignored `flow.pause` past `maxInboundQueueDepth`. | Honour backpressure; the SDK does. |
| `4000` | `SESSION_REPLACED`: another connection for this plugin arrived without `resumeSessionId`. | Expected when a second instance starts; `maxSessionsPerPlugin` is 1. |
| `4001` | `PROTOCOL_VERSION_UNSUPPORTED`. | See above. Fatal. |
| `4002` | `SESSION_EXPIRED`. | Retryable: open a fresh session. |
| `4003` | Authentication failed. | Retryable up to `MaxAuthenticationFailures` (default 3), then fatal. A `401` on the upgrade of a just-issued session token counts against the same limit. |
| `4004` | `SupervisorShutdown`: the supervisor is stopping you. | Not an error; clean up within the grace period. |
| `4005` | `RegistrationRejected`: invalid or duplicated declared ids, or a colliding integration id. | Terminal. Fix the declaration and reconnect. |

#### `UNKNOWN_MESSAGE_TYPE` or `MALFORMED_ENVELOPE` in the logs

Neither closes the connection. `UNKNOWN_MESSAGE_TYPE` is a peer speaking a newer catalogue.
`MALFORMED_ENVELOPE` is oversize input, excessive depth or a missing `type`. Suspect a hand-rolled client,
especially one that emits numbers as strings (`"deadlineMs": "30000"`), a hard failure here.

### Pairing

Symptoms of the default flow in
[Interactive pairing](https://docs.macro-deck.app/reference/authentication/#self-registering-interactive-pairing).

#### No approval prompt appears

Developer Mode is off, or `MACRO_DECK_PLUGIN_HOST_URL` points at another host instance. While Developer
Mode is off, `POST /api/plugins/pairing` and redemption answer `403 UNAUTHENTICATED`, even for a request
approved earlier. Turn it on and check the host URL; the plugin keeps retrying and pairs without a restart.
Once a request is pending the plugin writes to stderr:

```text
Waiting for pairing approval in Macro Deck...
```

#### The prompt was rejected

Rejection is fatal by design: the SDK pairs at most once per process, so it never re-prompts. Restart the
plugin process for a fresh request.

#### The pairing request expired

It outlived its `expiresAt`. Requests live in memory only, so a host restart expires every pending or
approved one. Restart the plugin process and approve in time.

#### `429` on `POST /api/plugins/pairing`

This plugin id already has a live request (a second does not replace it), the global pending cap was hit,
or the endpoint rate limit was. Resolve the existing request first; honour `Retry-After`.

#### The host does not support pairing

`GET /api/plugins/protocol` has no `pairing` block: the host predates pairing. Use a Developer token -
see [Advanced: enroll with a Developer token for headless runs](https://docs.macro-deck.app/guides/debugging/#advanced-enroll-with-a-developer-token-for-headless-runs).

### Running

#### `InitializeAsync` runs more than once, or not at process start

Initialization waits for a connection, because `IIntegrationContext` calls the host. It runs once per
session: a resume is a no-op, a non-resume reconnect shuts every integration down and re-initialises it.
Make `InitializeAsync` safely repeatable.

#### State corrupts under load, or a handler behaves as if re-entered

Invocations run concurrently, up to `maxConcurrentInvocations` (32); earlier SDKs ran them one at a time.
Synchronise state shared across invocations. Each invocation gets its own DI scope, so scoped services are
already isolated.

#### The UI shows a stale catalogue after something changed

`GetInstances`, `GetProfiles`, `DeclaredVariables`, `EventDefinitions` and similar are served from a cached
`describe`. Tell the host when they change outside a host-initiated invocation:

```csharp
notifier.CatalogChanged(kind); // IPluginCatalogNotifier, injected
```

Fire-and-forget, never throws, a no-op before a session exists.

#### The supervisor reports the plugin unhealthy but it is running fine

Almost always an overridden listener URL. The supervisor binds a port before your process starts and
passes it as `ASPNETCORE_URLS`; a URL in `appsettings.json`, a launch profile or `UseUrls` listens where
nobody probes, silently. Remove it; [MDP4002](https://docs.macro-deck.app/reference/analyzers/#mdp4002) catches the visible cases.

Otherwise check that `health.path` matches the route you serve (default `/_macrodeck/health`) and that
`health.timeoutSeconds` is long enough. `unhealthyThreshold` has a floor of 2, so one missed probe never
restarts anything.

```bash
curl http://127.0.0.1:<port>/_macrodeck/diagnostics
```

#### The plugin is killed at shutdown instead of exiting cleanly

```text
The plugin did not exit within its 10s grace period; killing it.
```

It missed `shutdown.gracefulTimeoutSeconds` (default 10, clamped 1-60) after `session.goodbye` and the
`4004` close. Make `ShutdownAsync` fast: stop new work, drain what is bounded, release. Lines logged at the
very end may be lost - see [logging](https://docs.macro-deck.app/features/logging/#shutdown).

#### Your logs never reach the host's log viewer

Check in order:

1. `UseMacroDeckLogging()` is called.
2. The level is at or above `MacroDeck:Plugin:Logging:MinimumLevel` (default `Information`, independent of
   the pipeline's own minimum).
3. The plugin is connected: `log.publish` has no replay, so a batch lost in an outage is gone.
4. You are under the ingestion rate limit, which drops excess events without closing the session.

See [logging](https://docs.macro-deck.app/features/logging/).

### Installing an artifact

#### The install API returns an error code

| Code | Cause | Fix |
| --- | --- | --- |
| `invalid_archive` | Not a readable ZIP. | Repack. |
| `unsafe_entry` | An absolute path, drive letter, `..` segment, reserved Windows device name, illegal filename character, or symlink/fifo/socket/device node. | Remove it - see [what the installer rejects](https://docs.macro-deck.app/reference/plugin-hosting/#the-macrodeckplugin-artifact). |
| `artifact_too_large`, `artifact_limit_exceeded` | Entry count, byte totals or compression ratio over the limits. | Trim the payload. |
| `manifest_missing` | No `manifest.json` at the archive root (the version directory, no wrapper folder). | Repack with `macrodeck-plugin pack`. |
| `manifest_invalid` | The reader rejected the manifest. | Run `macrodeck-plugin validate --artifact …`. |
| `id_mismatch` | The manifest names a different plugin than the caller asked to install. | Check `id`. |
| `incompatible` | `compatibility.protocol` or `compatibility.macroDeck` excludes this host; a rejection, not a warning. | Widen the range, or use a matching host. |
| `hash_mismatch` | A declared file digest, or the artifact's expected hash, did not match. | Repack; never edit an artifact in place. |
| `signature_invalid` | The signature block is malformed: no `keyId`, non-base64 `value`, or an `ed25519` value that is not 64 bytes. | Fix or remove the block. |
| `already_installed` | That version is on disk. | Pass `force`; it does not bypass compatibility, digests or signature rejection. |
| `health_validation_failed` | The version never became healthy, so activation was rolled back and the version deleted. | Fix health (usually [the listener URL](#the-supervisor-reports-the-plugin-unhealthy-but-it-is-running-fine)) and reinstall. |
| `dependency_in_use` | Another plugin hard-depends on the one being uninstalled. | Remove the dependent first, or force it. |
| `no_artifact` | `install` or `inspect` was called with no file. | Attach the file. |
| `DesktopOnly` | A local-path endpoint was called outside the desktop app (shared portability refusal, hence PascalCase). | Use the upload endpoint. |

#### It installed, but it will not start

- **A missing hard dependency or a live conflict.** A *Blocking* warning withholds the automatic start.
  Install what is missing, or start it manually.
- **No entrypoint for this host's RID.** The only fallbacks are `osx-arm64 → osx-x64` and
  `win-arm64 → win-x64`; there is no `"any"` key and `linux-musl-*` resolves nothing. The installer adds
  an advisory warning without health-gating. Check with `inspect`: the RID shows `(missing)`.

#### A framework-dependent plugin reports a missing runtime

Packaged Macro Deck ships .NET 10 (`Microsoft.NETCore.App` and `Microsoft.AspNetCore.App`), so this means
the plugin needs something that runtime lacks: another .NET major, or a framework such as
`Microsoft.WindowsDesktop.App` named in its `<Name>.runtimeconfig.json`. Macro Deck then looks for a
system `dotnet` (in `DOTNET_ROOT`, then `PATH`, then well-known locations) that has it, and found none. A
higher major never satisfies a lower one unless the runtimeconfig allows rolling forward. A host run from
source (`dotnet run`) has no bundled runtime and relies on the system search alone.

Install the matching runtime, then restart Macro Deck: installed runtimes are read once per host
process. Until then the plugin stays stopped instead of burning restart budget. The selection rule is in
the [manifest reference](https://docs.macro-deck.app/reference/manifest/#runtime).

#### A plugin shows up as dotnet in the process list

Framework-dependent plugins run as the .NET muxer, so Task Manager shows them as `dotnet` or ".NET Host"
and Activity Monitor as `dotnet`, not under the plugin's name. Tell them apart by PID or by the command
line, which ends in the plugin's `.dll`. Self-contained plugins keep their own executable name.

### Signing and install trust

#### The install is refused with a signature error

The host verifies in a staging directory before writing anything; every verdict but unsigned refuses.

| Verdict | Meaning |
| --- | --- |
| `SignatureInvalid` | The block is malformed, does not verify, or the contents do not match it. |
| `SignatureUntrusted` | The certificate does not chain to the pinned root, has another purpose, or was not valid at `signedAt`. |
| `SignatureRevoked` | The certificate is revoked. |
| `SignatureUnverifiable` | The package could not be read, or its algorithm is unknown to this host. |

```bash
macrodeck-plugin verify ./downloads/com.example.my-plugin-1.0.0.macroDeckPlugin
```

[`verify`](https://docs.macro-deck.app/cli/signing/#verify) names the failing check. Reinstall from a good copy: a signature that does
not verify is never treated as unsigned, so no confirmation installs it.

#### An unsigned plugin will not install

`UnsignedNotPermitted`. Unsigned packages install only with an explicit per-install confirmation, for a file
you selected or uploaded - never from a store or registry. A plugin id previously admitted as signed never
accepts an unsigned package. Install from a local file and confirm, or install a signed build.

#### A plugin that used to work now refuses to launch

Installed plugins are re-verified on every launch, because the plugin directory is user-writable. Editing
files or stripping the certificate breaks it, and the refusal lasts for the process lifetime. Reinstall
from a good artifact over the existing one - see
[signing](https://docs.macro-deck.app/policies/security/#signing-the-creator-portal-signs-and-the-host-verifies-before-install-and-before-every-load).

### See also

- [Plugin CLI](https://docs.macro-deck.app/cli/) - every command, diagnostic and exit code.
- [Debugging plugins](https://docs.macro-deck.app/guides/debugging/) - breakpoints, IDE profiles, enrollment tokens.
- [Logging](https://docs.macro-deck.app/features/logging/) - log locations, health routes, shutdown.
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - artifact format, supervision and shutdown.
- [Authentication](https://docs.macro-deck.app/reference/authentication/) - credentials, session exchange and their errors.
- [Analyzers](https://docs.macro-deck.app/reference/analyzers/) - every diagnostic.
- [Conformance](https://docs.macro-deck.app/reference/conformance/) - a verdict rather than a symptom.
