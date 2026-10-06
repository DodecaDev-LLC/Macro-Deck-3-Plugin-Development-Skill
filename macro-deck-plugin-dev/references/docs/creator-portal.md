# Creator Portal: publishing to the Store

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Creator Portal: https://docs.macro-deck.app/creator-portal/
- Conformance report: https://docs.macro-deck.app/creator-portal/conformance/
- Projects and Store listing: https://docs.macro-deck.app/creator-portal/projects/
- Publish an icon pack: https://docs.macro-deck.app/creator-portal/publish-icon-pack/
- Publish a plugin: https://docs.macro-deck.app/creator-portal/publish-plugin/
- Release workflow reference: https://docs.macro-deck.app/creator-portal/release-workflow/
- Review and release: https://docs.macro-deck.app/creator-portal/review/
- Testers: https://docs.macro-deck.app/creator-portal/testers/

## Creator Portal

> Source: https://docs.macro-deck.app/creator-portal/
>
> Publish plugins and icon packs to the Macro Deck Store through the Creator Portal.

The Creator Portal is where you publish to the Macro Deck Store. Sign in with your Macro Deck account.

*[Image: The Creator Portal dashboard with a plugin in review and an icon pack draft]*

### What you can publish

| Project type | Published from | Guide |
| --- | --- | --- |
| Plugin / Integration | A build that a GitHub release uploads | [Publish a plugin](https://docs.macro-deck.app/creator-portal/publish-plugin/) |
| Icon Pack | A `.macroDeckIconPack` you upload | [Publish an icon pack](https://docs.macro-deck.app/creator-portal/publish-icon-pack/) |

### How it fits together

```text
Create Project  ->  Version  ->  Submit for Review  ->  Approved  ->  Store
                     ^
                     plugin: started from a build
                     icon pack: the uploaded file
```

- Every change goes through a review: new versions, but also the Display Name, the Store listing
  text and the images.
- An approved version cannot be changed. Fixes ship as a new version.
- The Store signs what it publishes. You never need a signing key or a secret.

### Pages

- [Projects and Store listing](https://docs.macro-deck.app/creator-portal/projects/): create a Project, fill in what the Store shows.
- [Publish a plugin](https://docs.macro-deck.app/creator-portal/publish-plugin/): repository, release workflow, builds, versions.
- [Publish an icon pack](https://docs.macro-deck.app/creator-portal/publish-icon-pack/): versions and package upload.
- [Review and release](https://docs.macro-deck.app/creator-portal/review/): what happens after you submit.
- [Testers](https://docs.macro-deck.app/creator-portal/testers/): let people install a plugin before it is reviewed.
- [Release workflow reference](https://docs.macro-deck.app/creator-portal/release-workflow/): inputs and error messages.

## Conformance report

> Source: https://docs.macro-deck.app/creator-portal/conformance/
>
> What the conformance status of a build means, every warning the Creator Portal shows about it, and how to fix each one.

The [release workflow](https://docs.macro-deck.app/creator-portal/release-workflow/) runs your plugin on a disposable stub host
with the [conformance suite](https://docs.macro-deck.app/reference/conformance/) and uploads the report with the build. The
Creator Portal shows it under every build in **Builds**, and to the moderator reviewing the version.

- A failed **required** check stops the release before anything is uploaded. Fix it and publish the
  release again.
- Everything else is advisory: a warning never blocks an upload, a release or a review. The moderator
  sees the same warnings you do.
- Each check in the report links to its entry in the [conformance reference](https://docs.macro-deck.app/reference/conformance/),
  which says what it asserts and how to fix it.

### Status

| Status | Meaning |
| --- | --- |
| Conformant | The report is readable and raised no warning. |
| Conformant, with warnings | No required check failed, but something below deserves a look. |
| Not conformant | A required check failed. |
| Not run on a stub host | No report came with the build. |
| Report unreadable | A report came with the build, but the portal could not read it. |

### Warnings

| Warning | Cause | Fix |
| --- | --- | --- |
| <a id="notprovided"></a>No conformance report | The workflow did not run the plugin on a stub host: `run-stub-host` is `false`, the manifest declares no platform a GitHub runner provides (`linux-x64`, `win-x64`, `osx-arm64`, `linux-arm64`, `win-arm64`, `osx-x64`), or the build predates conformance reports. | Remove `run-stub-host: false` from your release workflow, and declare at least one of those runtime identifiers in `manifest.json`. Publish the release again. |
| <a id="unreadable"></a>Report unreadable | The uploaded `conformance.json` is not the suite's JSON report: invalid JSON, over 1 MiB, or a check without a valid id, outcome or requirement. The reason is shown with the warning. | Use the official `publish-plugin.yml` at its current tag, and do not change `conformance.json` in your own steps. Run `macrodeck-plugin test --artifact <package> --report json` locally to see what the suite writes. |
| <a id="nosession"></a>No session with the stub host | `MDC0201`, the session handshake, did not pass. Without a session most checks cannot exercise the plugin. | Run `macrodeck-plugin run --artifact <package> --stub-host` and look for `Session established`. If it never appears, the plugin crashes on start, listens on the wrong address, or does not answer `session.hello`; see [MDC0201](https://docs.macro-deck.app/reference/conformance/#mdc0201), [MDC0704](https://docs.macro-deck.app/reference/conformance/#mdc0704) and [Troubleshooting](https://docs.macro-deck.app/guides/troubleshooting/). |
| <a id="nothingpassed"></a>No check passed | Every check was skipped or failed, so the run most likely never reached the plugin. | As for no session: run the package on a stub host locally and fix what stops it from starting. |
| <a id="notconformant"></a>Required check failed | At least one required check failed. The workflow stops before the upload when this happens, so a build showing it was changed after the suite ran. | Open the failed check's link and apply its fix. Run `macrodeck-plugin test --artifact <package>` until it exits with `0`. |
| <a id="recommendedfailed"></a>Recommended check failed | A recommended check failed. It never makes the plugin non-conformant, but it points at behaviour users notice, such as a late reply or lost log output. | Open the failed check's link and apply its fix. |
| <a id="inconclusive"></a>Check inconclusive | The stub host could not reach a verdict for reasons outside your plugin, such as a slow runner. | Usually nothing. Publish the release again; if the same check stays inconclusive, run it locally with `macrodeck-plugin test --artifact <package> --check <id>`. |
| <a id="otherplugin"></a>Report for another plugin | The report names another plugin id than the build. | Keep one id: the `id` in `manifest.json` must be the id the plugin reports at runtime ([MDC0105](https://docs.macro-deck.app/reference/conformance/#mdc0105)). |
| <a id="otherversion"></a>Report for another version | The report names another version than the build. | Do not override the version at runtime. The workflow writes the release version into `manifest.json` and the assembly version ([MDC0106](https://docs.macro-deck.app/reference/conformance/#mdc0106)). |
| <a id="verdictdisagrees"></a>Verdict contradicts its checks | The report's own `conformant` does not match its checks. | Use the official workflow and do not edit `conformance.json`. |

### Run it before you release

```bash
macrodeck-plugin build --source src/HelloDeck --output ./artifacts
macrodeck-plugin test --artifact ./artifacts/*.macroDeckPlugin
```

This runs the same suite as the release workflow. See [`macrodeck-plugin test`](https://docs.macro-deck.app/cli/test/) for filters
and report formats.

## Projects and Store listing

> Source: https://docs.macro-deck.app/creator-portal/projects/
>
> Create a Project in the Creator Portal and fill in the Store listing.

### Create a Project

On the **Dashboard**, select **Create Project**.

*[Image: The Create Project dialog with Plugin / Integration selected]*

| Field | Example | Notes |
| --- | --- | --- |
| Project type | Plugin / Integration | Cannot be changed later. |
| Display Name | `Weather Deck` | Up to 100 characters, unique in the Store. Can be changed later. |
| Package ID | `com.example.weather-deck` | Permanent. For a plugin it must equal the `id` in its `manifest.json`. |

A Project starts as **Draft**. Nothing is public until a review is approved.

### Store listing

**General Information** holds what the Store shows about the Project.

*[Image: General Information of an icon pack: Display Name, Summary, Description, Author link, Licence and Tags]*

| Field | Example |
| --- | --- |
| Summary | `Buttons that greet your deck.` |
| Description | Markdown, shown on the package page |
| Author link | `https://github.com/example` |
| Licence | `MIT` |
| Tags | `utilities`, `home-automation` (up to ten) |

- **Save** stages the changes. They go live with your next approved submission.
- A plugin's description, publisher and licence come from its `manifest.json`, so the portal only asks
  for the Summary and Tags.
- The Store listing falls back to the Display Name when there is no Summary.

### Images

| Image | Plugin | Icon pack |
| --- | --- | --- |
| Icon | From `manifest.json`, added when you create a release | Uploaded under **Images** |
| Screenshots | Up to ten | Up to ten |

A Project cannot be submitted without an icon. New images wait for review like the listing text.
Reordering screenshots that were already approved takes effect immediately.

### Transfer a Project

Under **General Information**, the **Danger Zone** transfers a Project to another publisher. Only its
owner can do this: you for your own Projects, the Owner for an Organization's. Choose where it goes,
select **Transfer**, and confirm with the Project's Display Name. The confirmation spells out what
changes.

*[Image: The Danger Zone with Transfer this Project, Another person by email chosen and an email address]*

| Where to | What happens |
| --- | --- |
| An Organization you own | It moves at once. |
| Your personal account (from an Organization you own) | It moves at once. |
| An Organization you are a Member of | Its Owner has to accept. Once they do, the Owner decides over the Project; you keep working on it as a Member. |
| Another person, by email | They get a link and accept with the Macro Deck account that uses this address. You lose access once they do. |

Until an offer is answered, the Project stays where it is and the Danger Zone shows it. **Withdraw
offer** takes it back. An offer expires after 14 days, and you are notified when it is accepted or
declined.

*[Image: The Danger Zone showing an offer to friend@example.com that waits for acceptance, with Withdraw offer]*

After a transfer:

- The Package ID stays the same, so installed copies keep updating.
- The Store shows the new publisher from the next release on, and releases are signed with the new
  publisher's key.
- For a plugin, the next build must name the new publisher as `publisher.name` in its `manifest.json`.
- It leaves the previous context. Everyone with access there, an Organization's Members included, loses it.

A transfer is refused while a review is in progress, an approved version waits to be released, or a
Store change is still running.

#### Receiving a Project

An Owner finds offers for their Organization on the **Dashboard** under **Transfer offers**, where
they **Accept** or **Decline** them.

*[Image: Transfer offers on the Dashboard: Weather Station into Example Labs, with Decline and Accept]*

An offer to a person arrives as an email with a link. It only works for the Macro Deck account whose
verified email address it was sent to, and that account needs a Creator profile.

*[Image: The transfer offer page: Take over Clock Deck, with the Project, who offered it, the expiry, Decline and Accept the Project]*

When a Project comes to you from another person, nothing of theirs comes along:

- Its testers and open tester invitations are removed.
- A plugin's repository has to be [connected again](https://docs.macro-deck.app/creator-portal/publish-plugin/#change-the-repository)
  by you, with your own GitHub access, before builds are taken from it. If the repository is not yours on GitHub yet,
  have its previous owner transfer it to you there first.
- Builds uploaded before the transfer cannot become your version; upload a new one.
- It cannot be transferred to a person while a version is in preparation.

### Delete or unlist

- **Delete Project** works until a version has been published. It removes the versions, builds and
  images.
- After that, a Project can only be unlisted: it disappears from the Store, but installed copies keep
  working and the Package ID stays taken. You can list it again later.

## Publish an icon pack

> Source: https://docs.macro-deck.app/creator-portal/publish-icon-pack/
>
> Create a version, upload the .macroDeckIconPack and submit it for review.

An icon pack needs no repository. The version is the file you upload.

```text
Start this version  ->  upload .macroDeckIconPack  ->  Add to submission  ->  Submit for Review
```

### 1. Export the pack

In Macro Deck, open **Icon packs**, open the pack's menu and select **Export pack**. You get a
`.macroDeckIconPack` file.

Icons keep their [appearances](https://docs.macro-deck.app/guide/concepts/#icon-appearances) in the export, so one icon can ship light,
dark, animated and static versions. In `pack.json` each appearance is nested under its icon's entry, in
`appearances`, with its `traits` (for example `{"colorScheme": "dark"}`), and its master is a file of its own
in `files`. A Macro Deck without appearances imports the pack and shows the default images.

Before you export, open the pack's menu, select **Edit pack** and set **AI-created icons**. The setting is
saved in the exported pack's `pack.json` as the same [`ai` declaration](https://docs.macro-deck.app/reference/manifest/#ai) plugins
use. **Not declared** is never treated as free of AI.

#### Size limits

A pack holds at most 29,996 files, `pack.json` included, and a `pack.json` of at most 32 MiB minus 64 KiB. Every icon takes one file,
its master image, plus one more file for each of its appearances, and `pack.json` lists each icon and each file. The two limits apply separately: icons with
long non-Latin names fill `pack.json` well before the file limit.

The smaller sizes a deck shows are not part of the pack: the Macro Deck that installs it creates them from each
master the first time an icon is shown at that size. Packs exported by Macro Deck 3.0.0-beta.13 and older also
carry a file per downscaled size; they still import, and Macro Deck ignores those files and creates its own.
Macro Deck 3.0.0-beta.13 and older do not create sizes, so they show the full master of a pack, profile or
widget exported by a newer version at every size. On a device, a large animated icon can then be too big to
show.

Macro Deck refuses to export a pack above either limit, so split a larger collection into several packs.
The limits leave room for the certificate files and the signature that the Store adds when it signs the pack,
so the signed pack stays within 30,000 files and 32 MiB, which is what Macro Deck imports. The room assumes
`pack.json` as Macro Deck writes it; a `pack.json` edited by hand can grow when it is signed.
`IconPackArchiveLimits` in `MacroDeck.Plugin.Packaging` carries these numbers for tools.

Macro Deck 3.0.0-beta.13 and older import at most 10,000 files per pack.

### 2. Create the Project

Create a Project of type **Icon Pack** and fill in [General Information](https://docs.macro-deck.app/creator-portal/projects/#store-listing).
Upload the **Icon** under **Images**; an icon pack cannot be submitted without one.

### 3. Start a version

Open **Releases**.

*[Image: Next version with Version and Changelog fields and Start this version]*

| Field | Example |
| --- | --- |
| Version | `1.0.0` |
| Changelog | `First release: 120 line icons.` |

Select **Start this version**. Only one version can be open at a time.

### 4. Upload the package

*[Image: Version 1.0.0 in preparation with the upload area for the .macroDeckIconPack]*

Drop the `.macroDeckIconPack` on the upload area or choose it. The portal checks size, checksum and
contents before the version can be submitted. Until it is submitted, you can replace the file.

### 5. Submit

Select **Add to submission**, then **Submit for Review** in the Project header. Continue with
[Review and release](https://docs.macro-deck.app/creator-portal/review/).

### Release an update

Export the pack again, then **Start this version** with a higher version, for example `1.1.0`, upload
and submit. A declined version stays editable: replace the file and submit it again.

## Publish a plugin

> Source: https://docs.macro-deck.app/creator-portal/publish-plugin/
>
> Connect a GitHub repository, add the release workflow, publish a GitHub release and submit the build for review.

A plugin reaches the Store from a GitHub release. The release runs the Macro Deck publishing workflow,
which uploads a build to the Creator Portal. You pick the build there and submit it.

```text
GitHub release v1.0.0  ->  build in Builds  ->  Create release  ->  Add to submission  ->  Submit for Review
```

Before you start:

- A [Project](https://docs.macro-deck.app/creator-portal/projects/) of type **Plugin / Integration**.
- A **public** GitHub repository with the plugin. The `id` in `manifest.json` must equal the Project's
  Package ID.

### 1. Connect the repository

Open **Builds** and select **Connect GitHub**. Install the Macro Deck Platform App on your account or
organization if GitHub asks for it.

*[Image: The Repository panel searching for hello, with mock-creator/hello-deck matching]*

- **Search your repositories**: type any part of the name, pick the repository and select **Connect**, or
- **New repository from the template** creates a public repository from the plugin template.

One repository per Project, one Project per repository. Private repositories are not offered.

#### Change the repository

Select **Change** next to the connected repository to pick it again, for example after you moved it to
a GitHub organization or renamed it.

*[Image: The Repository panel after Change, with the repository picker, Connect GitHub again and Cancel]*

- If the repository moved to another account, install the Macro Deck Platform App there and select
  **Connect GitHub again** first, so the picker offers it.
- Once a version is published, only the same GitHub repository can be connected: moved or renamed is
  fine, a different repository is refused. **Disconnect** is no longer offered.
- Upload a new build afterwards. Builds from before the move name the old location in their
  `manifest.json` and do not pass review.
- After a Project was [transferred to you](https://docs.macro-deck.app/creator-portal/projects/#transfer-a-project) by another
  person, builds are refused until you connect its repository again here.

### 2. Add the release workflow

While there are no builds, the portal checks the default branch for the workflow.

*[Image: No release workflow found, with an Add with a pull request button]*

**Add with a pull request** commits the workflow to the branch `macro-deck/release-workflow`. Open the
pull request on GitHub and merge it.

Or add it yourself as `.github/workflows/release.yml`:

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

`source` is the directory with `manifest.json` and `macrodeck-build.json`. No secrets are needed: the
workflow signs in with the token GitHub issues for the run. All inputs are in the
[release workflow reference](https://docs.macro-deck.app/creator-portal/release-workflow/).

### 3. Publish a GitHub release

```bash
gh release create v1.0.0 --title "1.0.0" --notes "- Add the Greet action"
```

Or use **Draft a new release** on GitHub with the tag `v1.0.0`.

- The version comes from the tag. One leading `v` is dropped; the rest must be a semantic version.
- The version in your repository is ignored. The workflow writes the tag's version into
  `manifest.json`.
- The release notes become the default changelog.

When the run finishes, the build appears under **Builds**.

*[Image: The build library with build 1.0.0, its commit, run and dependency summary]*

Each build shows the commit and tag it came from, a link to the workflow run and the NuGet packages it
restored, including known vulnerabilities.

### 4. Create a release

Install the build in Macro Deck and try it first. Then select **Create release** on the build.

The dialog has two steps. **Changelog** comes first; the version number comes from the build and
cannot be changed, and the changelog can still be edited on **Releases**.

*[Image: The Create release 1.0.0 dialog, first step: the changelog]*

**Testing** asks how you tested the build. The moderator reads it with your submission.

*[Image: The Create release 1.0.0 dialog, second step: tested by hand, Macro Deck 3.0.0, Windows 11 24H2 x64, macOS 15.1 arm64 and OBS Studio 31.0]*

| Field | |
| --- | --- |
| I installed this build in Macro Deck and tested it by hand | Required. |
| Macro Deck version | Required. The version you tested with, for example `3.0.0`. |
| Tested on | At least one operating system and architecture, with the operating system's version. Only the platforms the build ships are offered. |
| Third-party software | Optional. Programs the plugin talks to, with their version, for example OBS Studio. |
| Additional information for the reviewer | Optional. Anything that helps the review: an account it needs, a setting to turn on. Not shown in the Store. |

**Create release** becomes available once the first box and a platform are ticked.

### 5. Submit for review

On **Releases**, check the release and select **Add to submission**.

*[Image: Version 1.0.0 in preparation with how it was tested, dependencies and the changelog]*

- **How you tested it**: **Edit** changes the test report until you submit.
- **Release automatically once approved**: turn it off to publish the approved version yourself later.
- **Discard version** removes the release. The build stays in the library.

Then select **Submit for Review** in the Project header. The dialog lists every change that goes to the
moderator; **Revert** removes one.

*[Image: The Submit for Review dialog listing Summary, Tags, Images and Version 1.0.0]*

Submitting needs the current Creator Guidelines accepted; the portal asks when they are not. A release
created before test reports were asked for needs one first: **Add test report** on **Releases**. Continue with
[Review and release](https://docs.macro-deck.app/creator-portal/review/).

### Release an update

```bash
gh release create v1.1.0 --notes "- Fix the greeting on light themes"
```

Then **Create release** on the new build and submit again. The version must be higher than the last
published one.

- Re-running a workflow uploads a new build. It never replaces one.
- While a submission is in review, uploads are refused. Withdraw the submission first.
- Builds that no Version was started from are removed when a newer build arrives.

### Troubleshooting

| Problem | Fix |
| --- | --- |
| No build appears | Open the workflow run on GitHub. The upload step prints why it was refused. |
| `403`, repository does not match | The repository connected to the Project is not the one the workflow ran in, or `manifest.json` has a different `id`. |
| `409`, not a tag | The workflow ran from a branch. Trigger it with a published release. |
| `409`, in review | Withdraw the submission, then re-run the workflow. |
| `422`, plugin CLI | The build was made with a MacroDeck.Plugin.Cli older than the Store accepts. Raise `cli-version`, or leave it empty for the workflow's default. |
| Repository no longer offered | It is private. Only public repositories can publish. |

See all refusals in the [release workflow reference](https://docs.macro-deck.app/creator-portal/release-workflow/#errors).

## Release workflow reference

> Source: https://docs.macro-deck.app/creator-portal/release-workflow/
>
> Inputs, permissions and error responses of the Macro Deck plugin publishing workflow.

`Macro-Deck-App/GitHub-Actions/.github/workflows/publish-plugin.yml` builds, packs and uploads a plugin
to the Creator Portal. Call it as a reusable workflow; only builds from this workflow are accepted.

```yaml
jobs:
  publish:
    uses: Macro-Deck-App/GitHub-Actions/.github/workflows/publish-plugin.yml@v1
    permissions:
      contents: read
      id-token: write
    with:
      version: ${{ github.event.release.tag_name }}
      source: src/HelloDeck
```

### Permissions

| Permission | Why |
| --- | --- |
| `id-token: write` | Required. The upload signs in with the run's GitHub token. Without it the upload has no credential. |
| `contents: read` | Checks out the tagged commit. |

There is no secret to create. A step that uses a signing key or a publishing token is not part of this
workflow.

### Inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `version` | yes | | Version of the build. One leading `v` is dropped (`v1.2.0` → `1.2.0`). Written into `manifest.json` and the assembly version. |
| `source` | yes | | Plugin project directory with `manifest.json` and `macrodeck-build.json`. |
| `build` | no | run number | Build identifier, 1-64 letters, digits, `.`, `-`, `_` or `+`. |
| `changelog` | no | empty | Default changelog of a release created from the build. |
| `build-per-platform` | no | `false` | Build each runtime identifier the manifest declares on a runner of its own platform and merge the packages. See [Building each platform on its own runner](#building-each-platform-on-its-own-runner). |
| `runners` | no | `{}` | JSON object naming the runner that builds a runtime identifier, merged over the defaults, for example `'{"osx-arm64": "macos-15"}'`. |
| `run-tests` | no | `true` | Run the repository's tests with `dotnet test -c Release` after the build. A failing test stops the release. |
| `test-path` | no | the only solution | Solution, project or directory `dotnet test` runs, relative to the repository root. With no `*.sln`/`*.slnx` at the root, or several, the step is skipped with a warning. |
| `run-stub-host` | no | `true` | Run the plugin on a disposable stub host with the conformance suite and upload its report. A failed required check stops the release. |
| `cli-version` | no | newest prerelease | `MacroDeck.Plugin.Cli` version to build with. |
| `upload-artifact` | no | `false` | Also keep the `.macroDeckPlugin` as a workflow artifact. |
| `artifact-name` | no | package file name | Name of that artifact. |
| `artifact-retention-days` | no | `0` | Days to keep the artifact, 1-90. `0` uses the repository default. |
| `platform-url` | no | `https://api.macro-deck.app` | Where the build is uploaded. |
| `audience` | no | `https://api.macro-deck.app` | Audience the Platform expects in the OIDC token. Changing it means the upload is refused. |

### Examples

Keep the package on the run:

```yaml
    with:
      version: ${{ github.event.release.tag_name }}
      source: src/HelloDeck
      upload-artifact: true
      artifact-retention-days: 7
```

### Building each platform on its own runner

By default one `ubuntu-latest` runner builds every runtime identifier the manifest declares: a .NET
plugin cross-builds from Linux, in one job and one restore. Turn the build into one job per platform
only when a target cannot be built that way - a `net10.0-windows` target, a native library compiled per
platform, or a build step needing Windows or macOS tooling:

```yaml
    with:
      version: ${{ github.event.release.tag_name }}
      source: src/HelloDeck
      build-per-platform: true
```

Each job then builds its own platform with [`build --rid`](https://docs.macro-deck.app/cli/build/), and a merge job combines them
with [`merge`](https://docs.macro-deck.app/cli/merge/) into the single package that is uploaded - the one a build on a machine
that could build every platform would have produced. Merging refuses packages that do not belong
together: a different plugin or version, a manifest differing beyond its `entrypoints`, a runtime
identifier twice, or a shared file whose bytes differ.

- The tests and the dependency list run once, on the first platform (Linux when the manifest declares
  it): they are about the repository, not about a runner.
- `upload-artifact` keeps the merged package, not the per-platform ones.
- The runner per platform defaults to `ubuntu-latest` (`linux-x64`), `windows-latest` (`win-x64`),
  `macos-latest` (`osx-arm64`), `ubuntu-24.04-arm` (`linux-arm64`), `windows-11-arm` (`win-arm64`) and
  `macos-15-intel` (`osx-x64`). `runners` replaces one, or names one for a platform not listed.
- One platform failing does not cancel the others, so a run shows every platform that is broken.

A rule of thumb: if `macrodeck-plugin build` succeeds on Ubuntu, leave this off.

### What gets uploaded

| File | Content |
| --- | --- |
| `.macroDeckPlugin` | The built, unsigned package. |
| `build-metadata.json` | Package id (from `manifest.json`), version, build, changelog and the MacroDeck.Plugin.Cli version that made the package. |
| `dependencies.json` | The NuGet packages the build restored, with known vulnerabilities. |
| `conformance.json` | Optional. The conformance suite's report from the stub host run; see [Conformance report](https://docs.macro-deck.app/creator-portal/conformance/). |

Commit, tag, repository and workflow are read from GitHub's signed token, never from these files.

### Errors

| Status | Cause | Fix |
| --- | --- | --- |
| `401` | No valid GitHub Actions token. | Add `id-token: write` to the job's permissions. |
| `403` | The build did not run through `publish-plugin.yml`. | Call the workflow with `uses:` instead of copying its steps. |
| `403` | Repository is not the Project's, or the package id is unknown. | Connect this repository to the Project and check the `id` in `manifest.json`. |
| `400` | The package or its metadata is unreadable. | Check the build step's log. |
| `409` | The run was not started from a tag. | Trigger the workflow with a published release. |
| `409` | The Project is in review. | Withdraw the submission and re-run. |
| `422` | The plugin CLI is older than the minimum the Store requires, or the workflow did not report it. | Set `cli-version` to a newer version or leave it empty, and call `publish-plugin.yml@v1`. The minimum is published at `/api/v1/public/dependency-policy/sdk` as `minimumCliVersion`. |
| `503` | GitHub's signing keys were unreachable. | Nothing was stored. Re-run the workflow. |

## Review and release

> Source: https://docs.macro-deck.app/creator-portal/review/
>
> What happens after you submit - review statuses, change requests, manual release, updates and unlisting.

A Creator Moderator reviews every submission before anything reaches the Store.

*[Image: Version 1.0.0 in review, with the Project locked while it is reviewed]*

### Statuses

| Status | Meaning | What you can do |
| --- | --- | --- |
| In Review | Waiting for a moderator. The Project is read-only. | **View submission** and withdraw it |
| Needs changes | The moderator asked for changes. | Read the feedback, change, submit again |
| Declined | Not accepted. | Fix the version and submit again |
| Ready to release | Approved, with automatic release turned off. | Release the version |
| Published | In the Store. | Start the next version |

You are notified in the portal under **Notifications**, and by email for decisions.

### Before the moderator decides

The portal runs automated checks on every submission and shows the findings in the review:

- the commit the build came from still exists in the repository,
- the repository is public and reachable,
- the package is unchanged since upload,
- `manifest.json` can be read and signed.

The moderator also sees the build's [conformance report](https://docs.macro-deck.app/creator-portal/conformance/) and its warnings.

A check that could not run, for example because GitHub was unavailable, is a warning, never an error.

### Changes requested

The submission comes back to you with the moderator's feedback. The version is editable again.
Change what was asked, then **Submit for Review**. The same submission keeps its history.

### Withdraw a submission

Open **View submission** and withdraw it. Use this to fix something before the moderator gets to it,
or to upload a new plugin build.

### Release by hand

Turn off **Release automatically once approved** before submitting. After approval the version waits
as **Ready to release**; release it from **Releases** when you are ready.

### After publishing

- The Store signs the package. Macro Deck verifies it before installing and before every launch.
- Users see the update when the Store version is higher than the installed one.
- An approved version is final. Ship fixes as a new version.

### Repository checks after publishing

The portal checks a published plugin's repository every few hours.

| Repository | Result |
| --- | --- |
| Private, deleted or App access removed | Email with a deadline. After 14 days the plugin is unlisted. |
| Reachable again | The plugin is listed again automatically. |

A repository renamed or moved within the same GitHub account is followed and needs nothing from you.
A repository transferred to another account has to be
[connected again](https://docs.macro-deck.app/creator-portal/publish-plugin/#change-the-repository) from there before the deadline.

### Unlist

Unlisting removes a published Project from the Store. Installed copies keep working and the Package ID
stays yours. List it again at any time.

## Testers

> Source: https://docs.macro-deck.app/creator-portal/testers/
>
> Let up to ten people install a plugin build in Macro Deck before it is reviewed.

Testers install a plugin build before it is reviewed or published. Only plugins can have testers.

*[Image: The Testers page with an invitation form and one tester]*

### Invite a tester

Open **Testers**, enter the address and select **Send invitation**.

```text
tester@example.com
```

- Up to **10 testers**. Pending invitations count too.
- The link is valid for 30 days.
- The invitation can only be accepted by the Macro Deck account with that verified email address.
  Forwarding the link does not work.

### What testers get

- Every build you **Create release** from becomes installable for testers, even if you discard the
  version later.
- The five newest of those builds stay available.
- Testers find them under **Tests** in the Creator Portal.

Test builds were never reviewed. Only invite people you trust with that.
