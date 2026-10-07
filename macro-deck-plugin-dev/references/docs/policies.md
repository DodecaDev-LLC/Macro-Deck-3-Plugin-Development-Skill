# Policies: compatibility, deprecations, migrations, security

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Compatibility policy: https://docs.macro-deck.app/policies/compatibility/
- Deprecations: https://docs.macro-deck.app/policies/deprecations/
- Migrations: https://docs.macro-deck.app/policies/migrations/
- Security model: https://docs.macro-deck.app/policies/security/

## Compatibility policy

> Source: https://docs.macro-deck.app/policies/compatibility/
>
> Which Macro Deck plugin surfaces are frozen, what counts as a breaking change, how contracts are evolved additively, and how protocol majors are negotiated.

A plugin ships as a compiled assembly, built against an SDK version and updated on a schedule its author
controls, not Macro Deck. So the promise is: **a plugin compiled against an older SDK keeps loading and
behaving the same against a newer host - no recompile, no behaviour change.** Every contract below is
frozen while it is public and not marked `[Obsolete]`, and changes only through the process under
[how contracts change](#how-contracts-change). The few deliberate exceptions to that promise are listed
under [behaviour changes that moved no version](https://docs.macro-deck.app/ui/reference/compatibility/#behaviour-changes-that-moved-no-version).

### What is covered

| Surface | Examples | Promise |
| --- | --- | --- |
| SDK packages | `MacroDeck.Sdk`, `MacroDeck.Plugin.Hosting`, `MacroDeck.Plugin.Testing`, `MacroDeck.Plugin.Packaging`, `MacroDeck.Plugin.Serilog`, `MacroDeck.Plugin.Cli`, `MacroDeck.Localization` | No public type or member is removed or changed incompatibly, source or binary. |
| UI model | `MacroDeck.Ui`, `MacroDeck.Ui.Model`, `MacroDeck.Ui.Testing` | Frozen like the SDK; the UI model's wire major is negotiated separately - see [the UI model majors](#ui-model-majors). |
| Protocol | `MacroDeck.Plugin.Protocol`: the envelope, DTOs, message types, error codes | Append-only within a protocol major; a break needs a new major. |
| Plugin HTTP and WebSocket | `/api/plugins/*`, `/plugins/ws` | Existing endpoints keep their shape and meaning - see [the protocol reference](https://docs.macro-deck.app/reference/protocol/). |
| Capability and host API catalogues | `device-provider`/`devices`, `layout-provider`/`layouts`, `folder-view-provider`/`folder-views`, `widget-type-provider`/`widget-types`, `screensaver-provider`/`screensavers`, `messaging`/`messaging`, `video-stream-provider`/`video-streams`, `calendar`, `event-bindings` | Names stay; see [capability operations](https://docs.macro-deck.app/reference/protocol/#capability-operations). |
| Manifest and package format | `manifest.json`, the `.macroDeckPlugin` package | An existing manifest and package keep installing - see [the manifest reference](https://docs.macro-deck.app/reference/manifest/). |
| Analyzer diagnostic ids | `MDP1001`, …, the `MDLOC` family `MDLOC001`-`MDLOC008` | An id keeps its meaning and is never reused - see [analyzers](https://docs.macro-deck.app/reference/analyzers/). |
| Conformance check ids | `MDC0305`, … | Stable, so you can gate CI on them - see [conformance](https://docs.macro-deck.app/reference/conformance/). |
| Plugin `.resx` contract | the default-language file, `Strings.<culture>.resx`, named placeholders, the bracketed parameter type in a `<comment>` | A plugin's `Localization/*.resx` keeps compiling - see [Localization](https://docs.macro-deck.app/features/localization/). |
| Macro Deck's localization catalog | `macrodeck:Common.Save`, … exposed as `MacroDeckStrings` | **Additive-only**: a shipped key is never deleted outright. |

Retiring a catalog key follows the same idea as [SDK deprecation](https://docs.macro-deck.app/policies/deprecations/): the key
keeps resolving, a plugin referencing it gets [MDLOC006](https://docs.macro-deck.app/reference/analyzers/#mdloc006) naming the
replacement, and the record stays for as long as the deprecation lifecycle requires.

Background: [ADR 0026](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0026-plugin-protocol-and-sdk-boundary.md)
(protocol and SDK boundary) and
[ADR 0029](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0029-plugin-packaging-installation-and-supervision.md)
(packaging).

### Breaking or not?

**Source *and* binary compatibility both count.** A plugin ships compiled, so a change that recompiles
cleanly can still break it at run time.

| Change | Verdict |
| --- | --- |
| Remove or rename a public type, member, parameter, enum value, constant, message type, field or error code | Break |
| Change a parameter or return type, or parameter order | Break |
| Add a parameter to a public method, **even with a default value** | Binary break |
| Change `class` to `struct`, or add or narrow a generic constraint | Break |
| Add a member to a public interface without a default implementation, or make an existing member abstract | Break for every implementer |
| Add a member to a public interface **with** a default implementation | Allowed |
| Add a new overload | Allowed |
| Add a value to a C# enum | Allowed by .NET's own rules - give a `switch` over a Macro Deck enum a default branch |
| Add an optional DTO or manifest field | Allowed - unknown fields are ignored on read |
| Rename a JSON property, change its type, or change an enum's wire representation | Break |
| Make an optional field required, tighten validation, or change a default a plugin relied on | Break |
| Change an error code's meaning, even with the same spelling | Break |
| Change ordering guarantees, id formats (the `integrationId::localId` shape), thrown exception types, timing or lifecycle contracts | Break |

The two that surprise people most:

**A parameter with a default is a binary break.** The compiler bakes the full argument list into the
call site, so an already-compiled plugin calls a method that no longer exists and gets a
`MissingMethodException`.

```csharp
// illustrative method
// before
public Task ShowAsync(string text);

// after - recompiles cleanly, breaks every compiled caller
public Task ShowAsync(string text, TimeSpan? duration = null);

// instead - keep the old method, add an overload
public Task ShowAsync(string text);
public Task ShowAsync(string text, TimeSpan duration);
```

**A changed meaning is a break.** Nothing about the spelling changes, but a plugin branching on it now
branches wrongly.

```text
hypothetical: an error code that meant "retry later" starts to mean "give up"
same spelling, same field - still a break, because plugins that retry now retry wrongly
```

### How contracts change

The rule is *add, do not change*.

**New overloads**, rather than new parameters on an existing method - see the example above.

**New optional members** with a sensible default, rather than required ones.

**New optional DTO fields.** Unknown fields are ignored on read, so an older plugin simply does not see
what it was not built for.

```jsonc
// illustrative: a reader built before displayName existed reads this exactly as {"id":"a"}
{ "id": "a", "displayName": "Kitchen" }
```

**New message types.** An unrecognised message type produces `UNKNOWN_MESSAGE_TYPE` and is never fatal:
the peer reports it and carries on. That makes every additive protocol change backward-compatible by
construction.

**New capability interfaces** a plugin opts into, rather than new members on an existing one. An existing
interface is extended only through a default interface implementation.

```csharp
// illustrative interface names
// not this: every existing implementer stops loading
public interface IStateProvider { Task RefreshAsync(); }

// this: a new opt-in interface
public interface IRefreshableStateProvider : IStateProvider { Task RefreshAsync(); }

// or, on the existing interface, a default implementation
public interface IStateProvider { Task RefreshAsync() => Task.CompletedTask; }
```

**Anything that has to go follows the deprecation lifecycle.** It is marked with `[Obsolete]` *and*
`[MacroDeckDeprecated]` carrying a declared removal version, registered so it appears in the registry
table, and it **keeps working unchanged** the whole time. Removal happens only in the major release its
`RemovedIn` names - never earlier, never in a minor or a patch. You are told at compile time as
[MDP5002](https://docs.macro-deck.app/reference/analyzers/#mdp5002), with the removal version and replacement in the message, and at
run time in the desktop app, where the person running your plugin sees the same finding under the same
id. See [deprecations](https://docs.macro-deck.app/policies/deprecations/) and
[ADR 0037](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0037-sdk-deprecation-is-declared-metadata.md).

**A wire break means a new protocol major, with the previous one still served** - see
[protocol majors](#protocol-majors).

### The 3.0 metadata retype

One break was taken deliberately before 3.0 shipped, and it is the only non-additive change on this page.
The members carrying an action's, a parameter's and a config-flow step's user-facing text changed type
from `string` to `LocalizedText`:

`IActionDefinition.Name`/`.Description`, `ActionParameter.Label`/`.Description`/`.Placeholder` and its
factories, `ActionParameterOption.Label`, `ActionStateDefinition.Label`,
`WidgetTargetOptions.Label`/`.Description`, `ConfigFlowStep.Title`/`.Description`, `ConfigFlowLink.Label`,
`ConfigFlowCopyValue.Label`, `ConfigFlowInstruction.Text`, and `IIntegration.Name`.

```csharp
Label = "Client ID"                       // assigning: unchanged, LocalizedText converts from string
public string Name => "Timer";            // implementing: no longer compiles
public LocalizedText Name => "Timer";     // implementing: fixed
```

Implementing one of those members is a source and a binary break. It was affordable because 3.0 had not
been released and no plugin existed to break; the alternative was a permanent parallel surface (`Name`
beside `NameLocalized`). After 3.0 this page's ordinary rules apply to these members like any other.

Two things did **not** change:

- **`VariableDefinition.Name` is still a `string`.** It is the variable's identity - the host derives a
  definition id from it and substitutes it into a template placeholder - so it cannot differ by language.
  Localized display text goes in the additive `DisplayName` property.
- **Descriptor metadata is localized from protocol v3.** `ActionDescriptorDto.Name`,
  `ActionParameterDto.Label`, the event and issue descriptors and the config-flow DTOs carry
  `LocalizedText`, so an out-of-process plugin's action names render in the reader's language. Below v3
  the SDK resolves them in the plugin's own default language first, because an older host would reject an
  object where it expects a string - the negotiated version decides, and v1 and v2 are still served. A
  plugin's text inside a Macro Deck UI tree was never affected; it always travelled as a reference.
  `ConfigFlowResultDto.EntryTitle` stays a plain string on purpose: the host stores it as the configured
  entry's name, which the user then owns and can rename.

### Versions

| Version | Scheme | Breaks allowed |
| --- | --- | --- |
| SDK packages | Ordinary semver | Only at an SDK major, and only removals whose `RemovedIn` names that major |
| Plugin protocol | One monotonically increasing integer major, not semver | Only with a new major; the previous one stays served |
| Capability, per kind | Integer min/max range per kind | Only with a new capability version; negotiated separately from the protocol |
| UI model (`UiModelVersions`) | Integer major | Only with a new major; negotiated separately from the protocol |

#### Protocol majors

Unknown fields are ignored and unknown message types are reported rather than fatal, so every additive
change is backward-compatible without a version change. A bump therefore only ever means *breaking*.

Today `minimum` is `1` and `current` is `3`.

| Major | Changes exactly one thing | Older majors |
| --- | --- | --- |
| `2` | A widget appearance change names its states by stable id instead of the fixed `Current`/`On`/`Off`/`Both` selector, because a button may have any number of states. | `1` fully served - see the [migration guide](https://docs.macro-deck.app/policies/migrations/) for what a version `1` plugin sees when it restyles a three-state button. |
| `3` | Action names, parameter labels and config-flow text may be a `{"$localized":…}` reference the reader's client resolves, instead of a plain string. | `1` and `2` fully served. A plugin below `3` must keep sending a plain string, since an older host would reject the object. |

What did **not** need a major:

- Actions gained the ability to supply a button's states: an additive descriptor field plus an additive
  capability operation, so a version `1` plugin can be a state provider. Additive changes never move the
  major, however visible the feature.
- The `variables` catalog half - `discover`, `resolve`, `subscribe` and the `variable-values` host API's
  `value`/`invalidate` - is ordinary `capability.invoke`/`capability.result` and
  `host.invoke`/`host.result` traffic. Variable definition attributes, a `write` capability and a `set`
  operation *did* change a payload plugins already send, so the **capability** version moved from `1` to
  `2` while `ProtocolVersions.Current` stayed at `3`.
- Widget appearance gained an accent colour: `WidgetAppearancePatch.AccentColor`,
  `WidgetAppearanceProperty.AccentColor` and an optional `accentColor` field on the wire patch. An older
  host ignores the field, so a patch carrying only it applies nothing there and `ApplyAsync` returns
  `false`. While a Slider's or History Graph's colour thresholds are on, a stored accent has no visible
  effect.
- [Video streams](https://docs.macro-deck.app/features/video-streams/) added a capability kind, `video-stream-provider`, a host API,
  `video-streams`, and `video_stream_` error reasons under the existing `CAPABILITY_UNAVAILABLE` code, all
  within major `3`. An older host rejects the kind non-fatally, and a plugin that does not implement
  `IVideoStreamIntegration` never declares it. The surface was reshaped before any release: Macro Deck now
  relays the media itself, and signaling, the consumer context and the `webrtc` and `whep` transports are
  gone. A development build written against the earlier, unreleased shape must be updated.
- [Calendars](https://docs.macro-deck.app/features/calendars/) added a capability kind, `calendar`, at capability version `1`, with
  its own operations, DTOs and reply limits, all within major `3`. An older host rejects the kind
  non-fatally and the plugin's other capabilities keep working, and a plugin that does not implement
  `ICalendarProvider` never declares it. The host's calendar widget types and the `calendar` trigger
  provider are host-owned additions, not protocol changes.
- Colour variables added `VariableType.Color`, whose values travel as an ordinary `text` value, and an
  optional `allowAlpha` field on `ActionParameterDto` (`ActionParameter.AllowAlpha`), all within major `3`.
  An older host drops a variable definition that declares `Color` and ignores `allowAlpha`. A colour
  parameter without `allowAlpha` still receives opaque `#rrggbb`, also when the user bound it to a
  variable. A new optional `hostApiFeatures` list on the session request lets a plugin declare
  `scripts.input-color`; only then does a Color script input reach it as `color`, every other plugin keeps
  receiving it as `text` with the hex value. The SDK declares it automatically. See
  [Color variables](https://docs.macro-deck.app/features/variables/#color-variables).
- Colour variables are also a one-way step for the host's own data, which no plugin contract covers: once
  a user variable of type `Color` exists, the persisted user-variables file cannot be read by a Macro Deck
  release from before `Color`, which then starts without any user variables. Downgrading the host is
  unsupported from that point; see [Colors from a variable](https://docs.macro-deck.app/guide/tips/#colors-from-a-variable).
- Resolving colours added the `colors` host api (`resolve`, `watches` and a `colors` `host.state`), the
  optional `maxColorWatches` field in the protocol descriptor's limits, and `IIntegrationContext.Colors` as
  a default interface member, so an existing `IIntegrationContext` implementation keeps compiling and
  loading. An older host answers `CAPABILITY_UNSUPPORTED`, and the SDK falls back to resolving fixed colours
  locally, giving `null` for a reference and delivering a watch once. See
  [Resolving colours yourself](https://docs.macro-deck.app/features/variables/#resolving-colours-yourself).
- Localization moved the **UI model** major, not this one - see [the localization major](#the-localization-major).

**Negotiation happens exactly once**, in `POST /api/plugins/sessions`:

```text
plugin sends:  { minimum: clientMin, maximum: clientMax }
host computes: negotiated = min(clientMax, current)
fails with PROTOCOL_VERSION_UNSUPPORTED when negotiated < max(clientMin, minimum),
echoing the host's own supported range
```

The later `session.hello` only *asserts* the outcome - it never re-negotiates.

**A protocol break means bumping the major and keeping the previous version served for the negotiated
range.** Version `1` is never silently redefined. A plugin declaring `{ minimum: 1, maximum: 1 }` in its
manifest's `compatibility.protocol` keeps negotiating version 1 against a host that has moved on, until 1
leaves that host's supported range - at which point the failure is explicit and diagnosable.

**Capabilities negotiate independently**, per kind, on the same min/max algorithm but with a
**non-fatal** failure policy: an unknown kind, or one whose range does not overlap the host's, is
rejected with a reason and the session proceeds degraded. An unknown host API call is answered with
`CapabilityUnsupported` rather than failing the session, and a plugin that never declares a kind is never
asked about it.

#### UI model majors

##### The localization major

Localizable Macro Deck UI text properties moved **`MacroDeck.Ui.Model`** (`UiModelVersions.Current`)
from `1` to `2`: a text-bearing configuration property may now carry a localization reference where it
always carried a JSON string, so the session has to say which version it speaks.

**Localization did not move the plugin protocol's major.** The protocol moved to `2` for an unrelated
reason (widget state by stable id) and localization would have left it at `1`. The two majors have never
been coupled (see
[ADR 0038](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0038-ui-model-and-declarative-dsl.md)).
Localization broke neither wire: the `localization` capability kind and its limits are additive, and a
localized value reads a plain JSON string as literal text.

**Version `1` of the UI model stays served**: the host opens every session at the current version and
honours whatever a provider negotiates down to, so a plugin on version `1` keeps emitting plain strings
untouched. See
[ADR 0057](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0057-localization-is-a-deferred-reader-resolved-reference.md).

##### The component major

Renaming the component vocabulary moved **`MacroDeck.Ui.Model`** (`UiModelVersions.Current`) from `2` to
`3`. Every node type was respelled: the ten a reader can draw from the tree alone became `ui.*`, the four
that resolve a Macro Deck reference became `macrodeck.*`.

```text
widget.*  ->  ui.*          (drawn from the tree alone)
widget.*  ->  macrodeck.*   (resolves a Macro Deck reference)
```

**This one also moved `UiModelVersions.Minimum`.** It is a hard cut - no `widget.*` spelling is
accepted, and no shim is published - so **majors `1` and `2` of the UI model are no longer served.**
Advertising them would be worse than refusing them: an unknown node type is non-fatal, so a version `2`
tree would negotiate and then render every node as the unsupported placeholder. This was affordable
exactly once, because no plugin served a component surface and a UI tree is built per session and never
persisted. See
[ADR 0064](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0064-components-are-a-registry-over-two-namespaces.md).

##### What did not need a UI model major

New component types and properties are additive. The [modifiers](https://docs.macro-deck.app/ui/components/modifier/) added a
`modifiers` property an older reader ignores, five gesture event names it never sends, and the `ui.modifier`
type it answers with the node's `fallback`; `UiModelVersions` did not move. [Responsive layouts](https://docs.macro-deck.app/ui/components/responsive/)
added the `ui.responsive` type the same way, and [first-fit layouts](https://docs.macro-deck.app/ui/components/first-fit/) the `ui.first-fit` type. See
[UI model compatibility](https://docs.macro-deck.app/ui/reference/compatibility/#additions-that-moved-no-version).

#### What "maintained per major" means in practice

- **Within an SDK major**, nothing frozen is removed or changed incompatibly. A minor or patch may add,
  and may deprecate; it may not remove. Upgrading the SDK inside a major should never require a source
  change to your plugin.
- **At an SDK major**, only APIs whose `[MacroDeckDeprecated]` named *that* major as their `RemovedIn`
  disappear. You will have had at least one release cycle of compile-time and run-time warnings naming
  the replacement.
- **Within a protocol major**, the error-code list and the message-type catalogue are append-only.
- **At a protocol major**, the previous major stays negotiable for as long as the host's supported range
  says it does. Read the descriptor at `GET /api/plugins/protocol`, which needs no authentication, rather
  than hard-coding a version.
- **Limits and timeouts are advertised, not fixed.** They are published in the protocol descriptor and
  again in the session response. A value changing is not a breaking change; read them at run time.

### Verifying compatibility yourself

- Run the **conformance suite** against your plugin: `macrodeck-plugin test`. A broken check id is a
  break, and the ids are stable, so gate CI on them. See [conformance](https://docs.macro-deck.app/reference/conformance/).
- Reference **`MacroDeck.Plugin.Analyzers`**. Its source generator records the deprecated APIs your
  compilation actually references, so the host can report *confirmed* rather than *inferred* usage. A
  plugin without it lands in `inferred`, which is never presented to a user as fact.
- Check the **compatibility report** in the session response: an overall state, the evidence source, and
  per-finding guidance. States, best to worst: `compatible`, `deprecated_apis`, `update_recommended`,
  `update_required`, `partially_incompatible`, `incompatible`.

### If a fix cannot be made without a break

It is not made. A change that breaks a non-obsolete public contract is not shipped as a bug fix, is not
made unilaterally, and does not arrive in a minor release. It goes through deprecation, or through a
protocol major, or it does not happen.

### See also

- [Deprecations](https://docs.macro-deck.app/policies/deprecations/) - the lifecycle, the registry, and the evidence model.
- [Migrations](https://docs.macro-deck.app/policies/migrations/) - what a migration guide contains, and when one is published.
- [Conformance](https://docs.macro-deck.app/reference/conformance/) - the contract suite and its stable check ids.
- [Plugin protocol](https://docs.macro-deck.app/reference/protocol/) - version and capability negotiation in detail.

## Deprecations

> Source: https://docs.macro-deck.app/policies/deprecations/
>
> The lifecycle for deprecating and removing a Macro Deck SDK API, how the host reports confirmed usage, and the compatibility states shown to a plugin's users.

A deprecated Macro Deck SDK API carries two attributes. This is a real one, from
`MacroDeck.Sdk.Widgets.WidgetTargetInfo`:

```csharp
[Obsolete("Use States.Count > 1. Removed in Macro Deck 4.0.0.")]
[MacroDeckDeprecated("3.0.0",
	"4.0.0",
	"Read States.Count > 1 instead of this collapsed on/off flag.",
	Replacement = "MacroDeck.Sdk.Widgets.WidgetTargetInfo.States")]
public bool HasOnOffStates { get; init; }
```

You are told twice: at compile time, as an analyzer warning with the removal version and the
replacement in the message, and at run time, in the desktop app, where the person running your plugin
sees the same finding under the same id.

```csharp
bool toggle = info.HasOnOffStates;       // MDP5002 (and CS0618)
bool toggle = info.States.Count > 1;     // fixed
```

This page is the contract behind both, and it is machine-checked: `SdkDeprecationLifecycleTests` checks
every registry entry against [the registry](#the-registry) below, so an API cannot be removed from the
SDK without its lifecycle appearing here.

### The attribute

`MacroDeckDeprecatedAttribute` lives in `MacroDeck.Sdk.Deprecation`.

| Argument | Kind | Meaning |
| --- | --- | --- |
| `deprecatedIn` | constructor, required | The `major.minor.patch` the API was deprecated in. |
| `removedIn` | constructor, required | The release that removes it. Must be after `deprecatedIn`. |
| `guidance` | constructor, required | What to do instead, in one sentence. Must not be empty. |
| `Replacement` | named, optional | The replacement API as a searchable display name; omit when there is no one-for-one replacement. |
| `MigrationUrl` | named, optional | A deep link to longer migration notes. |

Both attributes, always. `[Obsolete]` is what the compiler, the IDE and every third-party analyzer
already understand; `[MacroDeckDeprecated]` carries the lifecycle `[Obsolete]` has nowhere to put.

The attribute is public, so a plugin may use it on its own surface too - the analyzer rules apply to any
assembly that declares it.

### What you see

| Id | Severity | When |
| --- | --- | --- |
| [MDP5001](https://docs.macro-deck.app/reference/analyzers/#mdp5001) | Warning | You use an `[Obsolete]` SDK, hosting or protocol API that carries no deprecation metadata. |
| [MDP5002](https://docs.macro-deck.app/reference/analyzers/#mdp5002) | Warning | You use an API carrying `[MacroDeckDeprecated]`; the message names the API, both versions and the guidance. |
| [MDP5003](https://docs.macro-deck.app/reference/analyzers/#mdp5003) | Warning | A declaration is missing its companion `[Obsolete]`, has a removal version not after the deprecation version, or has empty guidance. |
| [MDP5004](https://docs.macro-deck.app/reference/analyzers/#mdp5004) | Error | You use an API whose declared removal version has been reached. An API still present after that version is itself a bug. |

### The lifecycle

| Stage | What happens | When |
| --- | --- | --- |
| 1. Deprecate | The API gets `[Obsolete]` *and* `[MacroDeckDeprecated]`. It keeps working exactly as before. An entry is added to `SdkDeprecations.Active` and to the table below. | Any release |
| 2. Warn | Plugin builds report MDP5002 at every call site. The host reports the same finding, under the same id, to the user running the plugin. | At least one release cycle before removal |
| 3. Remove | The member is deleted and its registry entry moves from `Active` to `Removed`. | Only in a major release, and only the one its `RemovedIn` names - never earlier |
| 4. Remember | The entry stays in `Removed`, and in the table below, forever: a plugin built years ago still gets "removed in 4.0.0, use X" rather than "unknown". | Permanently |

To migrate, follow the replacement the warning names; longer write-ups are in
[migrations](https://docs.macro-deck.app/policies/migrations/).

### The registry

Deprecated, still present:

| API | Deprecated in | Removal planned | Replacement |
| --- | --- | --- | --- |
| `MacroDeck.Sdk.Widgets.WidgetStateSelector` | 3.0.0 | 4.0.0 | `MacroDeck.Sdk.Widgets.WidgetAppearanceRequest.StateIds` |
| `MacroDeck.Sdk.Widgets.WidgetAppearanceRequest.State` | 3.0.0 | 4.0.0 | `MacroDeck.Sdk.Widgets.WidgetAppearanceRequest.StateIds` |
| `MacroDeck.Sdk.Widgets.WidgetTargetInfo.HasOnOffStates` | 3.0.0 | 4.0.0 | `MacroDeck.Sdk.Widgets.WidgetTargetInfo.States` |

Removed:

| API | Deprecated in | Removed in | Replacement |
| --- | --- | --- | --- |
| _None yet._ | | | |

Action buttons moved from a binary on/off appearance to N states with stable ids (issue #612), so the
fixed four-way `WidgetStateSelector` and the two-appearance flag are superseded by
`WidgetAppearanceRequest.StateIds` and `WidgetTargetInfo.States`.

#### How the registry is enforced

The registry is `SdkDeprecations` in `MacroDeck.Sdk.Deprecation`, keyed by documentation comment id
(`T:`, `M:`, `P:`, `E:` or `F:`). `SdkDeprecationLifecycleTests` fails the build when:

- a member carries `[MacroDeckDeprecated]` without a registry entry, or without `[Obsolete]`;
- an entry's removal version is not after its deprecation version, or its guidance is empty;
- an `Active` entry no longer exists in the SDK, or a `Removed` entry still does;
- an entry has no row on this page.

### How the host knows what your plugin uses

"This plugin *calls* a deprecated API" and "this plugin was *built against* an SDK in which something is
deprecated" are different, and only the first is shown to a user as fact. Every finding carries its
evidence:

| Source | Means |
| --- | --- |
| `confirmed` | Your plugin reported this exact API in its build-time usage manifest. |
| `negotiated` | Observed directly during protocol or capability negotiation. |
| `inferred` | Derived from your SDK version alone - the plugin *may* be affected. Never presented as fact. A plugin that does not reference the analyzer package lands here. |
| `unknown` | The plugin reported nothing the host could reason from. |

`MacroDeck.Plugin.Analyzers` includes a source generator that records the deprecated APIs your
compilation actually references and emits them as an assembly attribute; `MacroDeck.Plugin.Hosting`
reads it at startup and sends it in the session handshake. It uses the same semantic analysis that
raises MDP5002, so the manifest and the warnings cannot disagree.

An empty list and a missing list are never conflated: empty means "the generator ran, and this plugin
uses none"; missing means "no manifest", which is only ever enough for an inference.

Nothing in the manifest is a secret - it is a list of Macro Deck's own API names, capped at 64 entries.

### Compatibility states

The desktop app shows one state per plugin, in the Developer page's Compatibility tab and as a badge on
the plugin's card. A plugin's state is the *worst* of everything found about it, in this order:

| State | Means |
| --- | --- |
| `compatible` | Nothing to report. |
| `deprecated_apis` | Confirmed use of deprecated APIs, none due for removal yet. |
| `update_recommended` | Nothing is broken, but the plugin is behind - typically an older SDK. |
| `update_required` | Confirmed use of an API whose declared removal version has been reached. |
| `partially_incompatible` | The session works, but at least one declared capability was rejected. |
| `incompatible` | No negotiable protocol version - the plugin cannot connect at all. |

### Run-time diagnostic ids

The host reuses `MDP5002` and `MDP5004` for the same findings, so a warning you saw while building and a
row your user sees are visibly the same thing. Three ids exist only at run time, because nothing about
them is visible at compile time:

| Id | Meaning |
| --- | --- |
| `MDP5005` | The plugin *may* use a deprecated API, inferred from its SDK version. |
| `MDP5006` | A declared capability the host did not accept. |
| `MDP5007` | No protocol version in common. |

These are reserved in the same `MacroDeck.Compatibility` band as the analyzer rules and must not be
reused for a future analyzer rule.

### See also

- [Compatibility policy](https://docs.macro-deck.app/policies/compatibility/) - what is frozen and what counts as a break.
- [Migrations](https://docs.macro-deck.app/policies/migrations/) - migration guides for superseded APIs.
- [Analyzers](https://docs.macro-deck.app/reference/analyzers/) - MDP5001-MDP5004 in full.
- [ADR 0037](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0037-sdk-deprecation-is-declared-metadata.md) - why deprecation is declared metadata.

## Migrations

> Source: https://docs.macro-deck.app/policies/migrations/
>
> Migration guides between Macro Deck SDK and protocol majors - what changed, what to use instead, and how long the previous version stays negotiable.

What to change in a plugin when the SDK or the plugin protocol moves a major. Importing a user's Macro
Deck 2 settings is a different thing - see [settings migrations](https://docs.macro-deck.app/features/settings-migrations/).

| Step | What changed | You must act? | Flagged by |
| --- | --- | --- | --- |
| [Protocol 1 to 2](#protocol-1-to-2-widget-states-are-addressed-by-id) | Widget appearance names states by stable id | No - deprecated in `3.0.0`, removed in `4.0.0` | [MDP5002](https://docs.macro-deck.app/reference/analyzers/#mdp5002) |
| [Protocol 2 to 3](#protocol-2-to-3-descriptor-text-may-be-localized) | Descriptor text may be a localization reference | No | - |

### Protocol 1 to 2: widget states are addressed by id

**What changed:** a widget appearance change names the states it applies to by stable id instead of the
fixed `Current` / `On` / `Off` / `Both` selector. Nothing else on the wire changed, and **major `1`
remains negotiable** - a plugin that speaks only `1` keeps working against a host that speaks `2`, with the
emulation [below](#what-a-protocol-1-plugin-sees).

An Action Button can now have any number of states, each with an id separate from its display label, so
`On` and `Off` no longer name anything a three-state button has. See
[ADR 0056](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0056-widget-state-is-addressed-by-stable-state-id.md).

Nothing here is urgent. Do it when you next touch widget appearance code, or when the compatibility report
in the desktop app says your plugin is affected.

| Deprecated in `3.0.0`, removed in `4.0.0` | Use instead |
| --- | --- |
| `WidgetStateSelector` | Stable state ids, or the `WidgetStates.Current` / `WidgetStates.All` sentinels |
| `WidgetAppearanceRequest.State` | `WidgetAppearanceRequest.StateIds` |
| `WidgetTargetInfo.HasOnOffStates` | `WidgetTargetInfo.States` |

All three keep working until `4.0.0`. Recompiling reports each call site as
[MDP5002](https://docs.macro-deck.app/reference/analyzers/#mdp5002); with warnings as errors that is a build break at your chosen
warning level, but the API itself still works.

#### Before and after

```diff
 var target = widgets.GetWidgets().Single(w => w.Id == widgetId);
-if (target.HasOnOffStates)
+if (target.States.Count > 1)
 {
     await widgets.ApplyAsync(new WidgetAppearanceRequest
     {
         WidgetId = widgetId,
-        State = WidgetStateSelector.Both,
+        StateIds = [WidgetStates.All],
         Patch = new WidgetAppearancePatch { BackgroundColor = "#00ff00" }
     });
 }
```

| Old | New |
| --- | --- |
| `State = WidgetStateSelector.Current` | `StateIds = [WidgetStates.Current]` - the default: whichever state is showing |
| `State = WidgetStateSelector.Both` | `StateIds = [WidgetStates.All]` - every state |
| `State = WidgetStateSelector.On` / `Off` | `StateIds = ["on"]`, or whatever id `GetWidgets()` reported, such as `["muted"]` |
| `HasOnOffStates` | `States.Count > 1` |

`WidgetTargetInfo` now reports the states a widget has and the one it is showing:

```csharp
foreach (var state in target.States)      // empty when the widget has one appearance
{
    Console.WriteLine($"{state.Id} = {state.Label}");
}

var showing = target.CurrentStateId;      // null when the widget has one appearance
```

Rules:

- Address a state by its **id**, never by its label or position. A user can rename and reorder states at
  any time; the id survives both.
- An id the widget does not have is dropped. A request naming no state the widget has changes nothing and
  returns `false` - a plugin cannot create a state this way.
- If you set both `StateIds` and the deprecated `State`, `StateIds` wins. Leaving both at their defaults
  means the current state.

#### What a protocol 1 plugin sees

Nothing to do. A session negotiated at major `1` keeps sending the old payload, and the host maps it onto
real states:

| Old selector | What it changes on the new host |
| --- | --- |
| `Current` | The state the widget is showing. Unchanged. |
| `Off` | The state whose id is literally `off`; failing that, the first state; failing that, nothing. |
| `On` | The state whose id is literally `on`; failing that, the second state; failing that, nothing. |
| `Both` | **Every** state the widget has, including a third and beyond. |
| `HasOnOffStates` | Whether the widget has more than one state. |

A button carried over from the two-appearance model keeps the literal ids `off` and `on`, so `Off` and
`On` land exactly where they always did. On a button whose states came from an action (`Playing` /
`Paused` / `Stopped`, say), `Off` and `On` fall back to the first and second state, and states past the
second are invisible and unreachable until you move to major `2`. Nothing fails.

#### Actions can now supply a button's states

New in this release and **available in protocol major `1` as well** - no need to move to `2`. An action
that knows a live state implements `IStateProviderActionDefinition`:

```csharp
internal sealed class ToggleMuteAction : IActionDefinition, IStateProviderActionDefinition
{
    public Task<ActionStateSnapshot?> GetActionStateAsync(
        IReadOnlyDictionary<string, object?> parameters, CancellationToken cancellationToken)
    {
        if (!_client.IsConnected)
        {
            return Task.FromResult<ActionStateSnapshot?>(new ActionStateSnapshot(
                [new("unmuted", "Unmuted"), new("muted", "Muted"), new("unavailable", "Unavailable")],
                "unavailable"));
        }

        return Task.FromResult<ActionStateSnapshot?>(new ActionStateSnapshot(
            [new("unmuted", "Unmuted"), new("muted", "Muted"), new("unavailable", "Unavailable")],
            _client.IsMuted ? "muted" : "unmuted"));
    }
}
```

| Rule | Why |
| --- | --- |
| Answer from the configured `parameters`, not from a widget | The same action can sit on many buttons with different configuration; each answers for itself |
| Keep state ids stable across reconfiguration | Users style appearance per id; a changed id orphans it |
| Be side-effect free and quick; tolerate a partly filled parameter set, never throw | It is polled while the button is on screen, and called while the user is still typing the configuration |
| Declare your own "cannot tell" state instead of returning `null` when you know the set but not the value | Users can style "disconnected" apart from "connected and off". Return `null` only when nothing is known |

See [capabilities](https://docs.macro-deck.app/features/) for the full contract.

### Protocol 2 to 3: descriptor text may be localized

**What changed:** descriptor text - action names, parameter labels, config-flow text - may be a
`{"$localized":…}` reference instead of a plain string. Below major `3` a plugin must send a plain string.
Earlier majors stay negotiable, and the host translates for them.

If you use `MacroDeck.Plugin.Hosting`, there is nothing to change: against a host older than protocol `3`
the SDK resolves descriptor text in your default language before sending it. If you implement the protocol
yourself, send plain strings unless the session negotiated `3` or higher. See
[localization](https://docs.macro-deck.app/features/localization/) and [the protocol reference](https://docs.macro-deck.app/reference/protocol/).

### When a migration guide appears

Only for a **major** release, the only release in which anything frozen may change:

| Trigger | Scope of the guide |
| --- | --- |
| An SDK major in which at least one API reaches the removal version its `[MacroDeckDeprecated]` declared | That release's `RemovedIn` list - exactly the APIs that disappear in it, no others |
| A protocol major (an incompatible wire change) | A window rather than a cliff: the previous major stays negotiable for as long as the host's supported range says |
| A manifest or artifact format version, if `manifestVersion` ever advances beyond `1` | The format change |

Minor and patch releases never get one: they may add and deprecate, but never remove or change anything
frozen. See [the compatibility policy](https://docs.macro-deck.app/policies/compatibility/).

### What a migration guide contains

Each guide covers one major-to-major step:

- **What was removed**, by name, with the version it was deprecated in and removed in - the same entries
  the deprecation registry carries, so the two cannot disagree.
- **What to use instead**, per removed API, from the `Replacement` and guidance its `[MacroDeckDeprecated]`
  declared.
- **Behaviour changes** that are not removals: a changed default, a tightened validation rule, a changed
  error-code meaning.
- **Protocol changes**, if the protocol major moved: new or removed message types, changed payload shapes,
  and which versions remain negotiable.
- **How to check your plugin**: the analyzer diagnostics that flag each case, and the conformance checks
  that fail if you missed one.

### What to do meanwhile

- **Reference `MacroDeck.Plugin.Analyzers`.** Deprecated-API use is [MDP5002](https://docs.macro-deck.app/reference/analyzers/#mdp5002)
  at every call site, with the removal version and replacement in the message, long before the removal.
  Use of an API whose removal version this SDK has already reached is the error
  [MDP5004](https://docs.macro-deck.app/reference/analyzers/#mdp5004).
- **Read the compatibility report** the host returns in the session response, and the Compatibility tab in
  the desktop app. `update_recommended` or `update_required` is the earliest signal that a migration is
  coming for your plugin specifically.
- **Do not hard-code advertised values.** Limits, timeouts and the protocol version range are published at
  run time; hard-coding them turns a non-breaking change into a migration for yourself.

### See also

- [Compatibility policy](https://docs.macro-deck.app/policies/compatibility/) - what is frozen, what counts as a break, and how majors
  are negotiated.
- [Deprecations](https://docs.macro-deck.app/policies/deprecations/) - the lifecycle, the registry, and how the host tells confirmed use
  from a guess.

## Security model

> Source: https://docs.macro-deck.app/policies/security/
>
> The trust boundary around a Macro Deck plugin, what the host does and does not guarantee, how credentials and artifacts are handled, and the limits of the model.

What the host enforces around a plugin, and what it does not. Use it to decide whether to install
someone else's plugin, or what your own plugin can be trusted with. Anything declared but not enforced,
or shipped but not implemented, is stated as such.

### The trust model at a glance

| Party | Trusted for | Not trusted for, or the limit |
| --- | --- | --- |
| Host | Everything: it owns state, credentials, secrets and install decisions | - |
| Desktop app, over the private loopback port | **Admin**, with a per-launch secret instead of a token | A process running as the same user can read that secret - see [loopback trust](#loopback-trust-needs-a-per-launch-secret) |
| Plugin process | Scope `plugin`: the plugin protocol surface, and nothing else | Not sandboxed: it runs with the user's full privileges. Declared permissions are [not enforced](#permissions-declared-not-enforced), except `host:adb` |
| Deck clients (web client, companion) | Scope `client`: the viewer-safe endpoints | Plugin endpoints refuse them |
| LAN callers and browsers | The public listener's API and web client | Every plugin endpoint refuses them |
| Creator Portal and Store | Signing Store plugins after checking the publishing workflow's provenance; publishing the signed registry and its revoked keys | Revocation refuses new installs and updates, not a plugin that is already installed |

### Network exposure

Your plugin's own listener binds `127.0.0.1:0` by default, and the host's plugin endpoints answer only
from loopback. Exposing custom endpoints of your plugin to the network is a separate, explicit security
decision.

| Listener | Reachable from | Notes |
| --- | --- | --- |
| Public listener | The LAN | Serves the API and the web client. HTTPS is optional and configurable - see [ADR 0040](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0040-public-listeners-and-tls.md). While its plain-HTTP port is serving, the host announces its instance name, version and that port on the LAN over mDNS (`_macrodeck._tcp`), unless this is turned off in Settings > Network - see [ADR 0082](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0082-lan-discovery-uses-the-platform-responder.md). |
| Private loopback listener | The local machine only | Never gets TLS: the desktop shell and the plugin SDK reach it over plain HTTP on `127.0.0.1`. |

| Rule | Consequence |
| --- | --- |
| Plugin endpoints are served on both listeners but accept only a loopback remote address | A LAN caller is refused whichever port it used. A self-registering plugin must run on the same machine as the host ([ADR 0028](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0028-plugin-credentials-and-pairing.md)) |
| A browser-shaped request (cross-site `Origin` or `Sec-Fetch-Site`) is refused | Plugin paths are also excluded from the app-wide CORS policy |
| Enabling HTTPS on the public listener does not widen this | The local-only gate grants no principal of its own: reaching it from another listener adds reachability, not authority |
| `/_macrodeck/*` on the plugin's listener is reserved (`/_macrodeckery` is not) | Middleware added with `Configure` runs after the SDK's and cannot answer there; a constant path there is analyzer error MDP2005. See [reserved routes](https://docs.macro-deck.app/reference/plugin-hosting/#reserved-routes) |

#### Loopback trust needs a per-launch secret

A request on the *private* loopback port, from a loopback address, with a loopback `Host` header, is
authenticated as **admin** only when it also presents a secret the desktop app generates for every
launch: the app itself sends it as a header, and its window holds a session cookie derived from it. That
is how the desktop UI works without handling a token.

Reaching the port is therefore not enough: another account on the same computer, a local tool that
fetches URLs for someone else, a sandboxed process or a browser tab gets no admin rights there.
[ADR 0098](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0098-loopback-trust-requires-a-per-launch-secret.md) states the limit that remains: **a hostile process running as the same user** can
read the secret, as can anything with that user's file access, such as WSL on Windows, and is outside
what this boundary defends against. The `Host` header check is a
DNS-rebinding guard, and a request a browser marks as cross-site is refused even with the cookie.

Plain HTTP on the LAN leaves tokens visible to on-path attackers, so the public listener can be configured
for TLS. The shipped posture is a self-signed certificate: it "exists to encrypt a link the user already
trusts, not to prove identity to strangers".

#### Scopes

Authorisation is deny-by-default: an endpoint with no authorisation metadata is admin-only.

| Scope | Grants |
| --- | --- |
| `admin` | Everything, including the plugin installation surface |
| `client` | The viewer-safe endpoints a deck client needs |
| `plugin` | The plugin protocol surface, and nothing else |
| `plugin:enroll` | Developer (enrollment) tokens - the only Developer-token scope defined today |

`plugin` is a peer scope, not a subset. A plugin session token does not grant `client` access to the
deck-viewing endpoints, and neither an admin token nor a client token is accepted where a plugin token is
required.

### Credentials and tokens

A plugin holds one credential to buy a session, then sends the session token on every request. The
mechanics are in [the authentication guide](https://docs.macro-deck.app/reference/authentication/); this is how they are stored,
revoked, and must be handled.

```http
# Right: the session token in the Authorization header, the secret only on the session exchange
POST /api/plugins/sessions HTTP/1.1
X-MacroDeck-Plugin-Id: com.example.ref-probe
X-MacroDeck-Plugin-Secret: <plugin-secret>

GET /plugins/ws HTTP/1.1
Authorization: Bearer <session-token>

# Wrong: a token in the query string lands in logs
GET /plugins/ws?access_token=<session-token> HTTP/1.1
```

| Credential | Where it is kept | Rules |
| --- | --- | --- |
| Launch bootstrap token (managed) | Host: memory only, keyed by hash. Minted per launch, discarded on every exit path | A process that outlives its own termination sequence can never present a token the host still recognises. The managed credential store refuses to save it |
| Developer token | Host: SQLite, as a SHA-256 hash. Plaintext shown exactly once | Never persist the plaintext; a caller that displays it should discard it |
| Per-plugin secret | Host: SQLite, as a SHA-256 hash, plaintext shown once. Plugin: `credentials.json` in its state directory, **not encrypted at rest** | Sent only to `POST /api/plugins/sessions` - never on the WebSocket upgrade, in a query string or in a log line |
| Session token | Plugin memory; 15-minute JWT | `Authorization` header only - never a cookie or a URL |
| PKCE `codeVerifier` | Plugin memory | Sent only to the redemption call |

- **Hashing.** Verification is constant-time. A plain SHA-256 hash is used deliberately: Developer tokens
  and per-plugin secrets are high-entropy random values, unlike user passwords, which use PBKDF2.
- **The plugin's copy of its secret** is written owner-only, to a temporary file made owner-only before
  anything is written to it, then moved into place. On Windows the per-user profile ACL is the protection.
- **Revocation cascades.** Revoking a Developer token revokes every registration derived from it and
  terminates those sessions immediately. Revoking one registration terminates that plugin's session. The
  host re-checks the live session registry on every request, so a terminated session stops working at
  once even though its 15-minute JWT is still cryptographically valid.
- **Identity is never taken from a claim.** The host checks the credential against its own record.
  `MACRO_DECK_PLUGIN_LAUNCH_ID` is yours to log and nothing more.
- **Client sessions** (web client, companion) hold an access token - 15 minutes for the admin surface,
  60 days for a deck device - and a refresh token that rotates on every use and lives 365 days. Signing a
  device out in the devices list, removing it, or changing the account password or username is checked on
  every request from then on, so a long device token ends the moment you end the session rather than when
  it expires - every device at once for a credential change. A client session that is not tied to a device keeps the 15 minute token, because there is
  nothing to revoke it by. A rotated refresh token presented again within 30 days of its
  rotation revokes that token's rotation chain - the session it belongs to - and leaves every other session
  of the account signed in. One exception: the token rotated out most recently is accepted once more, from the same device and
  scope, so a client whose rotation response was lost in transit can retry - within a minute of the
  rotation, or, when the host restarted in between, within ten minutes of it starting up - and then only
  for the rotation that restart interrupted, because a restart is exactly when a rotation response goes
  missing. The companion pairs with a six-digit, single-use code
  from the desktop app's network panel: one code at a time, minted only on the loopback listener, cleared
  after five failed guesses from any caller, and throttled globally. See
  [ADR 0083](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0083-companion-pairing-code-and-year-long-refresh.md).

#### Interactive pairing

By default a self-registering plugin gets its per-plugin secret by pairing, not from a Developer token:
it creates a request, the user approves it in the desktop app, and the plugin redeems it. Mechanics:
[the authentication guide](https://docs.macro-deck.app/reference/authentication/#self-registering-interactive-pairing).

| Guarantee | Detail |
| --- | --- |
| Loopback only | Pairing endpoints are ordinary plugin endpoints: served on both listeners, reachable only from a loopback remote address |
| Gated by Developer Mode, continuously | Off by default. Turning it off invalidates redemption of an already-approved request, so no stale approval survives it |
| Approved only in the trusted desktop app | The prompt is rendered over the private loopback transport ([ADR 0003](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0003-loopback-trust-token-scopes-and-device-identity.md)). An admin bearer token over the network listener is **not** sufficient to approve: approval is a human act in a specific UI, not an API call |
| Proof of possession | The plugin presents a PKCE-style verifier at redemption; the host stores only the SHA-256 challenge, never the verifier. `requestId` is unguessable but authorises nothing on its own, so it is safe in a URL |
| One-time, short-lived, one per plugin id, capped, rate-limited | Expires on a host-advertised timer; consumed permanently on successful redemption; a second create for a plugin id with a live request is refused with `429` instead of replacing it; a global cap on pending requests; separate rate limits on creation and redemption |
| Nothing persists past a host restart | Requests are memory-only in every state - pending, approved, rejected |
| Self-reported fields shown as unverified; transport origin verified | Executable path, process id, SDK version and display name are shown as reported, labelled unverified, since deriving them from the loopback socket would authenticate nothing. Whether the request arrived on the public listener is verified and shown as verified |
| Replacement is atomic at redemption | If the host holds a registration for the plugin id but the local credential is gone, the prompt offers, with a separate confirmation, to replace it. Redemption rotates the secret in place and terminates live sessions in the same step, so old and new never both authenticate. The secret is minted at redemption, never at approval: an unredeemed approval leaves an existing working credential untouched |

#### Accepted residual exposure

Pairing uses the same loopback check as the rest of the plugin protocol, which has no port clause: a device
reaching the loopback address through an `adb reverse` tunnel is indistinguishable at the socket level from
a local process ([ADR 0030](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0030-android-usb-connections-over-adb.md)).
Pairing does not widen that existing exposure. A connection from a USB link without debugging is different:
the host dials it itself and marks it, so it is never taken for a local process and cannot reach pairing
([ADR 0095](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0095-usb-connections-without-debugging.md)).

What pairing changes is what a hostile local process needs. Before, it could mint a Developer token itself
through the then credential-less loopback admin. Now it needs a human to approve a specific prompt while
Developer Mode is on, unless it runs as the same user and reads the desktop app's
[loopback secret](#loopback-trust-needs-a-per-launch-secret). That is bounded by Developer Mode being off by default, approval only over the trusted transport, a
prompt that names what is approved and labels unverified fields, the one-request-per-plugin-id and
rate-limit rules, and nothing being minted before proof of the verifier - a bound, not a cryptographic
guarantee, as recorded in
[ADR 0028](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0028-plugin-credentials-and-pairing.md).

### Secrets in configuration

Declare a secret field in a setup flow, and read it back only when you need it:

```csharp
ActionParameter.Secret("api_key", label: Strings.Setup.ApiKey(), required: true)

// Values the user never typed, such as OAuth tokens:
["access_token"] = ConfigFlowValue.Secret(token.AccessToken),

// At runtime - decrypted only on request:
var apiKey = await context.Config.GetSecretAsync(entry.Id, "api_key");
```

| Rule | Detail |
| --- | --- |
| Stored encrypted | `Secret` and `Password` fields and `ConfigFlowValue.Secret` values go into SQLite through ASP.NET Core Data Protection. `Plain` values are stored as they are |
| Referenced, never inlined | Configuration refers to a secret as `{ "$secret": "<id>" }`, so no flow or action document carries plaintext |
| Key ring protected by the OS | The Data Protection key ring on disk under the host's data root is encrypted under a key in the OS credential store - Windows Credential Manager, macOS keychain, or Secret Service on Linux - so a copy of the data directory does not carry the key that opens it |
| Honest fallback | With no credential store, and in a portable installation, the key ring stays readable on disk and the host reports that state rather than implying protection |
| Never log or show | Secrets never belong in logs or user-visible errors: log the failure type, not the value |

See [setup flows](https://docs.macro-deck.app/features/setup-flows/#secrets) and
[ADR 0047](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0047-secrets-backups-and-restore.md).

### Signing and install trust

Check an artifact yourself, or in CI, before it reaches a host:

```bash
macrodeck-plugin verify ./artifacts/com.example.hello-deck-1.0.0-linux-x64.macroDeckPlugin
```

#### Artifacts

A `.macroDeckPlugin` artifact is a ZIP whose root is the version directory. Before a byte reaches its
destination, the installer enforces:

| Check | Rejects |
| --- | --- |
| Path safety (zip-slip) | Absolute paths, Windows drive letters, `..` segments, any resolved destination outside the target |
| Filesystem traps | Illegal filename characters, reserved Windows device names (`CON`, `PRN`, `COM1`, ...), any symlink, fifo, socket or device node |
| Zip-bomb caps | Entry count, per-entry uncompressed size, total uncompressed size, compressed size, compression ratio - measured **live through a bounded stream**, never taken from the archive's central directory |
| Payload identity | When the manifest declares `files[]`: a file whose SHA-256 or size does not match, and any extracted file *not* declared |
| Identity | `id` or `version` that does not match the directory names they install under |

**Nothing from an artifact is ever executed during install, activate or uninstall.** The manifest has no
hook field; the only process a version directory ever produces is the supervisor's own health-gated launch
after activation. The execute bit is set only on the entrypoints for the current runtime identifier, and a
self-contained entrypoint may not be a shell script.

**Activation is atomic.** `current.json` is written to a sibling temporary file and renamed over the real
one - a single filesystem operation on every supported platform - so it always names the previous version
or the new one. If the new version does not reach a healthy running state in time, the rename is undone,
the failed version is removed, and the previous version is restarted if it was running. See
[ADR 0029](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0029-plugin-packaging-installation-and-supervision.md).

#### Signing: the Creator Portal signs, and the host verifies before install and before every load

Verification lives in
[`MacroDeck.Signing`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/sdk/src/MacroDeck.Signing/README.md),
used by both the host and the `macrodeck-plugin` CLI's [`verify`](https://docs.macro-deck.app/cli/signing/#verify) and
[`keygen`/`sign`](https://docs.macro-deck.app/cli/signing/#keygen) commands.

**When it is checked:** in a staging directory before anything is written into the plugin directory, and
again on every launch of an installed plugin. The plugin directory is user-writable on every platform, so
editing a plugin's files after installation, or stripping the certificate from one installed as trusted,
stops it from loading.

The host resolves a package to exactly one verdict:

| Outcome | Verdict | Blocks install? |
| --- | --- | --- |
| Signature valid, chained to the Macro Deck root directly or through an issuer certificate | `Trusted` | No |
| No `signature` declared | `Unsigned` | Only without consent |
| Signature block malformed | `Malformed` | Yes |
| Signature present but does not verify | `SignatureInvalid` | Yes |
| Contents do not match the signature | `ContentMismatch` | Yes |
| Certificate does not chain to the pinned root | `UntrustedRoot` | Yes |
| Certificate issued for another purpose | `WrongCertificatePurpose` | Yes |
| Certificate not valid at `signedAt` | `CertificateNotValidAtSignature` | Yes |
| Certificate, or the issuer that signed it, revoked by the Store registry | `Revoked` | Yes, at install and update only |
| Package unreadable, or algorithm unknown to this host | `VerificationUnavailable` | Yes |

**`Unsigned` is the only verdict a confirmation can admit**, because nothing published today is signed yet:

| Source of an unsigned plugin | Installs? |
| --- | --- |
| A `.macroDeckPlugin` you select yourself, open through the file association, or upload | After a deliberate confirmation, and stays marked unverified |
| The Store or registry, Developer Mode on | Refused first; installs only if you then confirm the same warning. Developer Mode is read by the host from its own settings, so asking for the exception without it changes nothing |
| The Store or registry, Developer Mode off | No |
| An update to a plugin installed as `Trusted` | No, regardless of consent |
| An update Macro Deck found for you | Only ever reported to you, never installed unsigned on your behalf |

Icon packs and profile templates have no signature of their own and are unaffected. A signature that is
*present but does not verify* is a failure, not a weaker kind of unsigned: no confirmation installs it. An
unknown signature algorithm fails closed rather than being treated more leniently than no signature.

**Signature format.** Every signable format - `.macroDeckPlugin`, `.macroDeckIconPack`, and the portable
`.macroDeckProfile`, `.macroDeckFolder` and `.macroDeckWidget` - carries its signature in its own manifest
and its certificate as `certificate.json` and `certificate.sig` at the archive root, plus `issuer.json` and
`issuer.sig` when an issuer certificate signed that certificate. There is no detached signature file: a
signed artifact verifies on its own. The signature covers a format-specific canonical
digest - the package identity and the declared file list, never the manifest's own JSON encoding - so
reformatting a manifest does not invalidate a signature, while adding a file or repointing an entrypoint
does. See [the manifest's `signature` field](https://docs.macro-deck.app/reference/manifest/#signature) and the
certificate ([v1](https://docs.macro-deck.app/schemas/macrodeck-certificate-v1.schema.json),
[v2](https://docs.macro-deck.app/schemas/macrodeck-certificate-v2.schema.json)) and
[package signature](https://docs.macro-deck.app/schemas/macrodeck-package-signature-v1.schema.json) schemas.

**Trust anchor.** `MacroDeck.Signing.MacroDeckRootKey` (formerly
`MacroDeckHost.Domain.Security.MacroDeckRootKey`, which no longer exists) holds the public half of an
offline Ed25519 key pair, verification-only. The private half never exists on a build machine or in CI, and
is not any of the release-signing keys. `--root-public` on `sign` and `verify` points at a different root
for testing; both commands then warn `non-production-root` and report a result not anchored to the Macro
Deck root.

**Certificate chain.** A certificate is signed either by the root itself or by exactly one **issuer
certificate** the root signed, so the root can stay offline while the Creator Portal issues certificates
with the issuer's key. The rules are strict:

- An issuer certificate carries exactly the `issuer` key usage and the `issuer` subject kind, uses
  `schemaVersion` 2, is signed by the root, and names no issuer of its own. There is never a second
  intermediate level.
- A certificate it signs uses `schemaVersion` 2, names the issuer's `certificateId` in `issuer` and the same
  `rootKeyId`, carries exactly `package` or `registry`, and has a validity window inside the issuer's.
- An issuer certificate never signs a package or a registry manifest, and a `package` or `registry`
  certificate never signs another certificate.
- Both validity windows are evaluated at the signature's `signedAt`.
- A `schemaVersion` 1 certificate is always signed by the root, exactly as before.

The registry publishes an issuer certificate under `certificates/` beside the certificates it signed. Macro
Deck versions from before this chain refuse an issuer-signed certificate. See
[ADR 0096](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0096-offline-root-with-an-online-issuer.md).

**Store artifacts are signed by the Creator Portal, not by their author.** Publishing runs as Trusted
Publishing: the plugin's CI workflow authenticates to the Creator Portal with its own workload identity,
the Portal verifies that the workflow is a trusted publisher and checks the run's provenance, then signs
the artifact server-side. **Plugin developers and their CI workflows do not generate, receive, manage or
hold signing keys, certificates or signing credentials** - no signing secret in a repository or CI secret
store, and no manual artifact upload in the publishing path. Certificate issuance and revocation also live
in the Creator Portal. See [Publishing to the Store](https://docs.macro-deck.app/guides/publishing/) and
[ADR 0042](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0042-plugin-signing-and-trusted-publishing.md).

**The CLI signs and verifies; it never issues trust.** The public CLI has no root key generation, no
certificate issuance and no registry signing, and `keygen`/`sign` is not the Store path - it is for
artifacts distributed outside the Store and for Macro Deck's own infrastructure. `keygen` produces a
creator Ed25519 key pair and nothing else; `sign` requires a certificate only the Creator Portal can issue,
validates the whole artifact against it, and embeds the signature. `verify` checks the certificate chain,
the certificate's validity **at the signature's own `signedAt`** rather than at verify time, the canonical
digest, and every declared file's hash and size. See [`sign`](https://docs.macro-deck.app/cli/signing/#sign) and
[`verify`](https://docs.macro-deck.app/cli/signing/#verify).

| Limit | What it means |
| --- | --- |
| `verify` never consults revocation | It says so on every run, in both output formats. A `valid` verdict is a fact about the signature and chain at signing time, not a live trust decision |
| Revocation stops new installs, not installed plugins | The revoked keys come from the `security.json` of the signed Store registry the host has loaded. A package whose certificate, or whose certificate's issuer, is listed there is refused at install and update. A version that is already installed keeps activating and launching, and the Store marks it **Certificate revoked**. See [ADR 0096](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0096-offline-root-with-an-online-issuer.md) |
| Revocation needs a loaded registry | A host that has not loaded a registry snapshot yet, or never can because it is offline, answers `Unavailable`, and that deliberately does not block: failing closed would refuse every signed plugin. See [ADR 0044](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0044-plugin-and-store-trust-enforcement.md) |
| A leaked signing key must be contained by other means | Treat everything signed with it as untrusted. For the Store that is a Creator Portal concern, since the keys are the Portal's; outside the Store see [private-key handling](https://docs.macro-deck.app/cli/signing/#private-key-handling) |
| `signedAt` is not authenticated | No canonical digest covers it, so the key holder can set any value. Checking validity at `signedAt` is advisory against that key holder: it only protects a package from its certificate's later expiry. Revocation is the control that stops new installs signed with a compromised or misused key |
| `publisher` is a claim | It becomes an attribution only behind a `Trusted` verdict. Verified publisher identity comes from the Creator Portal having checked the workflow's provenance before signing, never from the manifest |
| Only plugins carry a publisher signature | Store icon packs and profile templates are authenticated by the signed registry: the pinned root signs the registry's certificate, directly or through an issuer certificate, that certificate signs the registry manifest, and the manifest carries the digest and size of every file, including the release manifest that declares each artifact's digest. That proves the bytes are the ones the Macro Deck registry published, nothing more: they are never presented as publisher-verified, and a publisher's revoked certificate does not apply to them |

<a id="permissions-declared-not-enforced"></a>

### Permissions: declared, and enforced only for ADB

```json
{ "permissions": ["host:variables", "host:adb"] }
```

A manifest may declare permissions from a fixed vocabulary (`host:variables` through `device:usb`),
mirroring the host callback surface one for one. They are parsed, shape-validated, persisted and surfaced
through the installed-plugins API so a consent surface has something real to render.

**The host gates exactly one host API on a declared permission: `adb`, on `host:adb`.** Every other host
callback is served whether or not the calling plugin declared the permission that covers it. Plugins that
predate the vocabulary declare nothing, so a default-deny posture for the rest would break every plugin
already running, and a default-allow posture would not be a boundary worth the name.

`host:adb` is enforced because it is new: no existing plugin relied on it. A plugin reaches Macro Deck's
ADB connection only when ADB is enabled, the user has left **Allow plugins to use ADB** on, and the active
version of the installed plugin declares `host:adb`. Installing a plugin that declares it while ADB or
that setting is off asks the user whether to turn both on. A self-registered session, admitted through a
developer token or interactive pairing, is exempt from the declaration because the user admitted it by
hand. See [Android devices](https://docs.macro-deck.app/features/android-devices/) and
[ADR 0092](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0092-plugins-reach-adb-through-a-permission-gated-host-api.md).

**This is user control, not isolation.** A plugin process is not sandboxed and could run its own `adb`
without declaring anything. `host:adb` gives the user a visible, switchable decision about plugins using
Macro Deck's connection; it does not stop a hostile plugin from reaching a device. Local paths an `adb`
call names are read and written with Macro Deck's identity, which is the same user the plugin already runs
as.

Treat the other declared permissions as documentation of intent, not as a constraint on what a plugin can
reach.

### Messages between plugins

Plugins and integrations can exchange messages through Macro Deck's
[message channel](https://docs.macro-deck.app/features/messaging/). Macro Deck stamps every message with the sender's integration
id, so `Sender` is reliable, but it authorizes nothing: any plugin can publish on any topic, send commands
and requests to any handled topic, and handle any topic nobody has claimed yet. Treat a message like any
other input from another process: validate its payload, and check `Sender` before acting on a command
where it matters who asked. `host:messaging` is declared, not enforced.

### Colour variables

Any plugin can resolve the current value of any Color variable through
[`IColorApi`](https://docs.macro-deck.app/features/variables/#resolving-colours-yourself): every global one, and the widget-scoped ones
of any existing widget, whichever plugin or user created them. It can also watch them for changes. That is
all the `colors` host api reveals: a variable of any other type, a missing one or an unknown widget
resolves to no colour, and the api accepts only a colour or a Color variable reference, never an arbitrary
template, so it cannot be used to read text, numbers or other values. No permission covers it.

### Video streams

A [video stream provider](https://docs.macro-deck.app/features/video-streams/) gives Macro Deck the URL of a stream, and Macro Deck
relays the media to every client signed in to Macro Deck, the desktop app or any paired device. The
provider's URL never reaches a client, so credentials in it stay on the computer; a provider still must
not serve anything it would not show every signed-in client, and never puts the source's own password or
API key in a URL. Macro Deck never logs a description. `host:video-streams` is declared, not enforced.

The relay is a deliberate, bounded fetch on behalf of a plugin:

- **The relay URL is a capability.** `/api/video-streams/relay/<token>/...` carries an unguessable token that
  is bound to one session, sent only over the authenticated UI WebSocket to the connection that owns the
  session, and dead once the session ends. The route is anonymous by design, because an image or video
  element cannot send an authorization header. Anyone who holds the URL can read that one stream until it
  ends, which is no more than the client it was sent to could. Macro Deck redacts the token from its logs.
- **It pins the origin of the provider's URL and nothing else.** Redirects and HLS playlist URIs stay on that
  origin (apart from `data:` and `skd:` URIs, which are passed on untouched), and only `GET` and `HEAD` are sent. The provider chooses the origin, so a plugin can point the
  relay at any service on the computer or the local network, or at Macro Deck itself. A plugin could make
  those requests without the relay, so this adds no capability, but the relay returns the response to a
  client, which is why only responses that look like the session's media are passed on.
- **Plugin bytes cannot run as a page.** Content types are checked against the session's transport,
  responses carry `X-Content-Type-Options: nosniff` and a sandboxing Content-Security-Policy, and a
  response that does not fit is refused, so a plugin cannot serve a script or an HTML page from Macro
  Deck's own origin.
- **It is bounded.** Eight concurrent relayed requests per session, 64 in all, a header timeout and an
  idle timeout on media.

A tree can name any provider's stream in a [`macrodeck.video-stream`](https://docs.macro-deck.app/ui/components/video-stream/), so
any plugin's view can make the clients that draw it open sessions on another plugin's provider. That is no
wider than what a signed-in client can already open, but it means a stream's audience is everyone who can
see any Macro Deck view, not only the views its own plugin draws.

### Logging and redaction

```csharp
_logger.Information("Authenticated as {User}", account.DisplayName); // not the token
```

The host redacts every event once, before any sink, to `***`: values of sensitive keys (`password`,
`token`, `secret`, `api_key`, `authorization`, `client_secret` and similar) in `key=value` or
`"key": value` form, credentials in URLs (`https://user:pass@`), `Bearer`/`Basic`/`Digest` credentials,
JWTs and PEM private keys. That is a safety net, not a licence: a secret in an unrecognised shape is written
as-is into a file users attach to bug reports. Plugin identity on a log line comes from the authenticated
session, so a plugin cannot log under another integration's name. See
[logging](https://docs.macro-deck.app/features/logging/#never-log-secrets).

### Threat-model limitations

Read this before deciding what a plugin should be trusted with.

| Limitation | Detail |
| --- | --- |
| A plugin runs with the user's full privileges | A managed plugin is an ordinary child process: no sandbox, container, separate account or privilege reduction. It can do anything the user can - read and write their files, open network connections, start processes. Installing one is equivalent to running any other downloaded program |
| Permissions are not a boundary | A plugin that declares nothing can still reach every host API except `adb`, and even `host:adb` gates only Macro Deck's own ADB connection, not a plugin's own - see [above](#permissions-declared-not-enforced) |
| An unsigned plugin is still admitted on your say-so | See [signing](#signing-the-creator-portal-signs-and-the-host-verifies-before-install-and-before-every-load). For an unsigned install the declared-digest check is corruption detection, not a boundary: whoever can rewrite the binary can rewrite the unsigned manifest. Trust rests on where you got the file |
| Revocation stops new installs only | A plugin installed before its certificate or issuer was revoked keeps running; the Store marks it, and removing it is your decision |
| A process running as the same user can become admin | It can read the desktop app's loopback secret. The model defends against LAN callers, browsers and other local accounts, not a hostile process running as the same user |
| The plugin secret and session token cross plain HTTP on loopback | The local-only rule confines that to processes already on the machine, but it is not encryption |
| A self-signed public certificate proves nothing about identity | It encrypts the link; it does not authenticate the host to a stranger, and a DHCP change means regenerating it |
| Supervision contains failure, not intent | Isolation is not a goal. The child's environment is scrubbed of inherited `MACRO_DECK_PLUGIN_*` and `ASPNETCORE_URLS`; the listener port is bound by the host and handed to the child; a fresh credential is minted per launch and discarded on exit; a restart budget stops a crash loop. See [ADR 0029](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0029-plugin-packaging-installation-and-supervision.md) |
| A hard kill is a hard kill | A plugin that does not exit within its graceful timeout has its process tree killed. An SDK that does not recognise close code `4004` gets no notice and no chance to flush ("kill-only" in ADR 0029) |
| Imported fonts are parsed as untrusted input | A `.macroDeckProfile`, `.macroDeckFolder` or `.macroDeckWidget` archive, including a Store profile template, can carry TTF or OTF fonts. The host checks each font's bytes against its recorded SHA-256, accepts only single-face TTF/OTF files up to 32 MB that it can parse, and never lets an imported font replace or extend a family installed on the computer, so an archive cannot change how installed fonts or the app font render. The font bytes are still parsed by the host's font engine and by every client's renderer |
| macOS arm64 and unsigned binaries | An unsigned, freshly extracted Mach-O needs at least an ad-hoc signature on Apple silicon before the kernel runs it, and the installer does not add one. This is a known, unsolved gap. |

### Reporting a vulnerability

Report privately through GitHub's
[private vulnerability reporting](https://github.com/Macro-Deck-App/Macro-Deck/security/advisories/new),
never a public issue, discussion or Discord. What to include, supported versions and scope are in
[SECURITY.md](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/SECURITY.md).

| The flaw is in | Report to |
| --- | --- |
| Macro Deck: host, first-party clients, built-in integrations, SDK, plugin infrastructure | This repository, privately |
| A third-party plugin that exploits Macro Deck or bypasses a boundary Macro Deck should enforce | This repository, privately |
| Only a third-party plugin | Its author, or its repository's security process. Store plugin with no suitable contact: report it through the Store |

### See also

- [Authentication](https://docs.macro-deck.app/reference/authentication/) - credentials, session exchange, and what a plugin must
  never do with either.
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - the artifact format, the installer's rejection rules, and
  what the supervisor injects.
- [Compatibility policy](https://docs.macro-deck.app/policies/compatibility/) - what is frozen and what may change.
