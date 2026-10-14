# Features (capabilities)

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Features: https://docs.macro-deck.app/features/
- Actions: https://docs.macro-deck.app/features/actions/
- Android devices: https://docs.macro-deck.app/features/android-devices/
- Batteries: https://docs.macro-deck.app/features/batteries/
- Button icons: https://docs.macro-deck.app/features/button-icons/
- Button states: https://docs.macro-deck.app/features/button-states/
- Calendars: https://docs.macro-deck.app/features/calendars/
- Companion devices: https://docs.macro-deck.app/features/companion-devices/
- Deck and clients: https://docs.macro-deck.app/features/deck/
- Device providers: https://docs.macro-deck.app/features/devices/
- Email inboxes: https://docs.macro-deck.app/features/email-inboxes/
- Events: https://docs.macro-deck.app/features/events/
- Integration issues: https://docs.macro-deck.app/features/integration-issues/
- Integration storage: https://docs.macro-deck.app/features/integration-storage/
- Layout providers: https://docs.macro-deck.app/features/layouts/
- Localization: https://docs.macro-deck.app/features/localization/
- Logging and health: https://docs.macro-deck.app/features/logging/
- Messaging between plugins: https://docs.macro-deck.app/features/messaging/
- Music players: https://docs.macro-deck.app/features/music-players/
- Notifications: https://docs.macro-deck.app/features/notifications/
- Settings migrations: https://docs.macro-deck.app/features/settings-migrations/
- Setup flows: https://docs.macro-deck.app/features/setup-flows/
- Testing plugins: https://docs.macro-deck.app/features/testing/
- Variables: https://docs.macro-deck.app/features/variables/
- Video streams: https://docs.macro-deck.app/features/video-streams/
- Virtual profiles: https://docs.macro-deck.app/features/virtual-profiles/
- Weather: https://docs.macro-deck.app/features/weather/

## Features

> Source: https://docs.macro-deck.app/features/
>
> Every feature a Macro Deck plugin can add, the SDK contract behind it, and where it is documented.

A plugin adds features by implementing small SDK interfaces on its integration. Implement only what you
need - every plugin starts with actions.

```csharp
public sealed class ObsIntegration : IPluginIntegration, IVariableProvider, IEventProvider
{
	public IReadOnlyList<IActionDefinition> Actions { get; } = [new StartRecordingAction()];
	// IVariableProvider and IEventProvider members, see their pages.
}
```

### Buttons

| Feature | Contract | Use it to |
| --- | --- | --- |
| [Actions](https://docs.macro-deck.app/features/actions/) | `IActionDefinition`, `IActionExecutor` | Do something when a button is pressed or a flow runs. |
| [Button states](https://docs.macro-deck.app/features/button-states/) | `IStateProviderActionDefinition` | Show on/off, muted, recording and similar states on a button. |
| [Button icons](https://docs.macro-deck.app/features/button-icons/) | `IIconProviderActionDefinition` | Draw album art, avatars or weather imagery on a button. |

### Data

| Feature | Contract | Use it to |
| --- | --- | --- |
| [Variables](https://docs.macro-deck.app/features/variables/) | `IVariableProvider` | Expose live values such as `{{ vars.music_track }}`. |
| [Events](https://docs.macro-deck.app/features/events/) | `IEventProvider`, `IEventPublisher` | Let users trigger automation when something happens. |
| [Messaging between plugins](https://docs.macro-deck.app/features/messaging/) | `IIntegrationContext.Messages` | Talk to other plugins and integrations by topic: events, commands and requests. |
| [Deck and clients](https://docs.macro-deck.app/features/deck/) | `IIntegrationContext.Deck` | Navigate folders and profiles, and find out which folder each client has open. |
| [Music players](https://docs.macro-deck.app/features/music-players/) | `IMusicPlayerProvider`, `IIntegrationContext.MusicPlayers` | Drive the Music Player widget and reuse Macro Deck's ready-made music actions, and read every provider's players and album colours. |
| [Weather](https://docs.macro-deck.app/features/weather/) | `IWeatherProvider` | Supply weather stations to Macro Deck's weather features. |
| [Calendars](https://docs.macro-deck.app/features/calendars/) | `ICalendarProvider` | Supply calendar accounts and events to Macro Deck's calendar widgets, triggers and Join Meeting action. |
| [Email inboxes](https://docs.macro-deck.app/features/email-inboxes/) | `IEmailInboxProvider` | Supply email inboxes to Macro Deck's email widget, variables and triggers. |
| [Virtual profiles](https://docs.macro-deck.app/features/virtual-profiles/) | `IProfileProvider` | Offer profiles the plugin generates. |

### Setup and maintenance

| Feature | Contract | Use it to |
| --- | --- | --- |
| [Setup flows](https://docs.macro-deck.app/features/setup-flows/) | `IConfigFlowProvider`, `IConfigFlow` | Ask for connection details, API keys or an OAuth login. |
| [Integration issues](https://docs.macro-deck.app/features/integration-issues/) | `IIntegrationIssueProvider` | Tell the user what is wrong and how to fix it. |
| [Notifications](https://docs.macro-deck.app/features/notifications/) | `INotificationService` | Show a toast or a dialog on every client and get the user's answer. |
| [Settings migrations](https://docs.macro-deck.app/features/settings-migrations/) | `IMigrationProvider` | Take over a user's setup from Macro Deck 2. |
| [Integration storage](https://docs.macro-deck.app/features/integration-storage/) | `IIntegrationContext.Storage` | Keep small documents of your own, such as devices you have seen, across restarts. |
| [Localization](https://docs.macro-deck.app/features/localization/) | `MacroDeck.Localization` | Ship every user-facing string in every language. |
| [Logging](https://docs.macro-deck.app/features/logging/) | `ILogger` | Write diagnostics the user can send you. |
| [Testing](https://docs.macro-deck.app/features/testing/) | `MacroDeck.Plugin.Testing` | Test your integration without a running Macro Deck. |

### Hardware and surfaces

| Feature | Contract | Use it to |
| --- | --- | --- |
| [Devices](https://docs.macro-deck.app/features/devices/) | `IDeviceProvider` | Connect hardware or custom clients as Macro Deck devices. |
| [Layouts](https://docs.macro-deck.app/features/layouts/) | `ILayoutProvider` | Describe a device's regions and geometry. |
| [Android devices](https://docs.macro-deck.app/features/android-devices/) | `IAndroidDeviceManager` | Run shell commands, copy files and install apps on Android devices through Macro Deck's ADB connection. |
| [Batteries](https://docs.macro-deck.app/features/batteries/) | `IBatteryProvider`, `IIntegrationContext.Batteries` | Report the battery levels of phones, headphones, controllers and other devices, and read every provider's devices. |
| [Companion devices](https://docs.macro-deck.app/features/companion-devices/) | `ICompanionDeviceApi` | Read what the phones and tablets connected through the Companion app report, send them commands and take screenshots. |
| [Macro Deck UI](https://docs.macro-deck.app/ui/) | `IUiProvider` | Draw configuration views, widgets and folder views. |
| [Widget types](https://docs.macro-deck.app/ui/views/widget-types/) | `IWidgetTypeProvider` | Add deck widgets beside Macro Deck's own. |
| [Folder views](https://docs.macro-deck.app/ui/views/folder-views/) | `IFolderViewProvider` | Replace a folder's button grid with your own rendering. |
| [Screensavers](https://docs.macro-deck.app/ui/views/screensavers/) | `IScreenSaverProvider` | Show something of your own on a device that has sat idle. |
| [Video streams](https://docs.macro-deck.app/features/video-streams/) | `IVideoStreamIntegration`, `IVideoStreamProvider` | Offer live video, such as cameras or OBS scenes, for Macro Deck to show. |

### Host APIs

`IIntegrationContext` gives an integration access to what Macro Deck owns: [`Deck`](https://docs.macro-deck.app/features/deck/) navigation and client positions, `Scripts`,
`Widgets`, [`NotificationService`](https://docs.macro-deck.app/features/notifications/), `Notifications`, variables, configuration, events, [messaging](https://docs.macro-deck.app/features/messaging/), [battery devices](https://docs.macro-deck.app/features/batteries/#reading-devices), [music players](https://docs.macro-deck.app/features/music-players/#reading-every-providers-players), [images for your own UI](https://docs.macro-deck.app/ui/reference/resources/#registering-your-own-images), [storage](https://docs.macro-deck.app/features/integration-storage/), the user's [time format](https://docs.macro-deck.app/features/localization/#formatting-a-time-of-day) and the [User-Agent](https://docs.macro-deck.app/reference/plugin-hosting/#outgoing-http-requests) for outgoing requests. In a plugin every call crosses the
plugin protocol, so don't call them in a hot loop. [Android devices](https://docs.macro-deck.app/features/android-devices/) and
[Companion devices](https://docs.macro-deck.app/features/companion-devices/) can also be taken from dependency injection, as
`IAndroidDeviceManager` and `ICompanionDeviceApi`.

### Ids

Action, event and variable ids are yours to choose and stay stable once shipped - profiles and
configuration store them.

```csharp
public sealed class StartRecordingAction : IActionDefinition
{
	public string Id => "start-recording"; // local id: lowercase kebab-case
	// ...
}
```

- **Pass the local id.** Macro Deck qualifies it with your plugin's identity; never pass an
  `owner::local` value to an API that expects a local id.
- **Runtime resource ids** that come from provider state (entities, sources, topics) may use a broader
  grammar, but must not contain `::`.

### See also

- [Capability parity](https://docs.macro-deck.app/reference/capability-parity/) - where a plugin differs from a built-in integration.
- [Compatibility](https://docs.macro-deck.app/policies/compatibility/) and [deprecations](https://docs.macro-deck.app/policies/deprecations/) - how these contracts evolve.
- [Contributing an integration](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/development/contributing-integrations.md) - built-in integrations.

## Actions

> Source: https://docs.macro-deck.app/features/actions/
>
> Expose actions with IActionDefinition and IActionExecutor - parameters, truthful ActionResults, dynamic options, UI-tree configuration, and how an action behaves inside an action flow.

An action is something a user can put on a button or into an action flow. You declare it with an
`IActionDefinition` (id, name, parameters) and run it with the `IActionExecutor` the definition creates.

### Quick start

```csharp
using System.Globalization;
using MacroDeck.Localization;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;

public sealed class LightsIntegration : IPluginIntegration
{
	private readonly LightClient _client = new();

	public IReadOnlyList<IActionDefinition> Actions => [new SetBrightnessAction(_client)];

	// Other IPluginIntegration members omitted.
}

internal sealed class SetBrightnessAction(LightClient client) : IActionDefinition
{
	public string Id => "set-brightness";

	public LocalizedText Name => Strings.Actions.SetBrightness();

	public LocalizedText Description => Strings.Actions.SetBrightnessDescription();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Text("light", label: Strings.Parameters.Light(), required: true),
		ActionParameter.Slider("brightness", 0, 100, label: Strings.Parameters.Brightness(), defaultValue: 100)
	];

	public IActionExecutor CreateExecutor() => new Executor(client);

	private sealed class Executor(LightClient client) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (!client.IsConnected)
			{
				return ActionResult.Failed(ActionErrorCodes.NotConnected, Strings.Errors.BridgeOffline());
			}

			if (context.Parameters.GetValueOrDefault("light") is not string light || light.Length == 0)
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter, Strings.Errors.NoLightSelected());
			}

			var brightness = Convert.ToDouble(context.Parameters.GetValueOrDefault("brightness") ?? 100,
				CultureInfo.InvariantCulture);

			await client.SetBrightnessAsync(light, brightness, context.CancellationToken);
			return ActionResult.Success();
		}
	}
}
```

The user gets a **Set brightness** action with a text field and a 0-100 slider, usable on any button and
in any action flow.

Things to know:

- **`Id` is persisted.** Profiles store it, so use stable lowercase kebab-case and never rename a
  released id. It is a local id - the host qualifies it with your plugin; never pass an
  `owner::local` value to an API that expects a local id.
- **`Actions` is read before `InitializeAsync`.** The list must be complete and side-effect free from
  construction on: building it must not connect, probe hardware or do other I/O.
- **The result is a claim.** `Success` says the operation completed. Anything else is `Failed` (or
  `Accepted`, see below) - never a quiet `Success`.
- **Honour `context.CancellationToken`.** It is cancelled when the running flow is aborted.

### Returning a result

```csharp
return ActionResult.Success();                                         // it happened
return ActionResult.Failed(ActionErrorCodes.NotFound, Strings.Errors.SceneGone()); // it did not
return ActionResult.Accepted(Strings.Status.WaitingForDevice());       // taken, not yet confirmed
```

| Result | Use when |
| --- | --- |
| `Success()` | The operation completed. `ActionResult.SucceededTask` is a cached `Task` for a synchronous executor. |
| `Failed(code, message)` | It did not complete. `code` is a stable, machine-readable reason; `message` is shown to the user as-is. |
| `Accepted(message)` | The provider took the request and its API **genuinely cannot confirm** completion. `message` says what it is waiting on. |

Do not return `Success` merely because a request was sent. If the provider can confirm completion, wait
for it (with a bound, see [long-running work](#long-running-work)) and report the real outcome.

The error message must read as an explanation, be localized, and carry no provider internals, tokens or
paths. Throwing is also fine - the flow engine records a failure and sanitizes the message - but a known
condition deserves its own code. Reuse `ActionErrorCodes` so a client can react the same way across
integrations:

| `ActionErrorCodes` | Meaning |
| --- | --- |
| `NotConfigured` | No usable configuration - no account, no instance. |
| `NotConnected` | Configured, but the provider is not reachable right now. |
| `PermissionDenied` | Missing scope, grant or OS permission. |
| `ProviderError` | The provider errored - unexpected response, broken call. |
| `ProviderRejected` | The provider understood the request and declined it. |
| `InvalidParameter` | A parameter is missing, malformed or unusable. |
| `NotFound` | The target does not exist. |
| `Timeout` | Completion could not be confirmed in time. |
| `Unavailable` | Not available here - wrong platform, unsupported provider version. |

A button's state provider can also report which state it expects next - see
[Button states](https://docs.macro-deck.app/features/button-states/#bridging-the-poll-delay).

### Declaring parameters

```csharp
public IReadOnlyList<ActionParameter> Parameters { get; } =
[
	ActionParameter.Choice("auth", [
		new ActionParameterOption { Value = "none", Label = Strings.Auth.None() },
		new ActionParameterOption { Value = "header", Label = Strings.Auth.Header() }
	], label: Strings.Parameters.Auth(), defaultValue: "none"),
	ActionParameter.Text("headerName", label: Strings.Parameters.HeaderName()).OnlyWhen("auth", "header"),
	ActionParameter.Secret("token", label: Strings.Parameters.Token()).OnlyWhen("auth", "header"),
	ActionParameter.Url("url", label: Strings.Parameters.Url(), required: true, autoPrefixHttps: true),
	ActionParameter.Duration("timeout", label: Strings.Parameters.Timeout(), defaultMilliseconds: 5000)
];
```

`ActionParameter` has a factory per editor: `Text`, `MultilineText`, `Number`, `Slider`, `Toggle`,
`Password`, `Secret`, `Choice`, `DynamicChoice`, `Autocomplete`, `MultiSelect`, `Color`, `File`,
`Folder`, `Hotkey`, `Duration`, `DateTime`, `Json`, `Code`, `KeyValue`, `Object`, `Array`, `IpAddress`,
`Url`, `Icon`, `Image`, `KeyboardSequence`, `KeyboardCombo` and `WidgetTarget`. The executor reads
values by `Name` from `context.Parameters`. The key names in `Hotkey`, `KeyboardCombo` and
`KeyboardSequence` values are listed under [Keyboard combos](https://docs.macro-deck.app/features/events/#keyboard-combos).

A `Color` parameter receives `#rrggbb`. The user can bind it to a
[Color variable](https://docs.macro-deck.app/features/variables/#color-variables); the host resolves it when the action runs and drops
any alpha, so you still get six digits, or an empty value when the variable is unavailable. Set the parameter's `AllowAlpha` to `true` when your action can use
transparency: the picker then offers opacity and the value may be `#rrggbbaa`. A Macro Deck release from
before `AllowAlpha` ignores it.

`OnlyWhen` is presentation only: a hidden parameter keeps what the user typed, is skipped by validation,
and **is still sent to the executor** - never infer anything from a field being hidden.

Set `Platforms` on the definition only when the capability does not exist on other platforms at all
(hibernation on macOS); the action is then neither listed nor executable there.

`Role` names a job the action does for Macro Deck itself, one of the `ActionRoles` values, and is `null`
for an ordinary action. A role fixes the parameters: `ActionRoles.LaunchApplication` takes a required
`path` and an optional `arguments`. When the user drops an application onto the deck, Macro Deck binds the
new button to a built-in action with that role; a plugin's action with the role is never chosen, so a
plugin never receives the dropped path. A Macro Deck release from before `Role` ignores it.

`ActionRoles.RunScript` and `ActionRoles.RunRemoteScript` mark an action that runs a Macro Deck script, here
or on another instance. Such an action takes a required dynamic-choice `scriptId`; an option may carry the
metadata `scriptInputs` (the script's inputs as a JSON array) and `runsOnWidget` (`"true"`). The action
editor then adds an `input:<name>` parameter per declared input and, for `RunScript` only, a `widget`
target for a widget script. `RunRemoteScript` also takes an optional dynamic-choice `instance`, sent along
when the editor lists the scripts. Any action with one of these roles, a plugin's included, gets this editor.

#### Letting the user search a long list

A `Choice` or `DynamicChoice` parameter draws a plain select. For a long list, call `AsSearchable()` on it
and the user can type into the field to filter the options by label:

```csharp
ActionParameter.DynamicChoice("counter", label: Strings.Parameters.Counter(), required: true).AsSearchable()
```

Typed text alone is never stored: the value is still one of the options, and the field shows the picked
option's label. Other parameter
types ignore it, and so does a Macro Deck release from before `Searchable`, which draws the plain select.
For a configuration view, see [Letting the user search a long list](https://docs.macro-deck.app/ui/views/configuration/#letting-the-user-search-a-long-list).

### What the executor gets

| `ActionExecutionContext` | |
| --- | --- |
| `Parameters` | Configured values, keyed by parameter name. |
| `CancellationToken` | Cancelled when the flow is aborted. |
| `OwnerWidgetId` | The widget whose flow is running; `null` for scripts, automations and other widget-less runs. |
| `OriginClientId` | The client that pressed, or `null` for a backend-initiated run. |
| `Interactions`, `Ui` | Ask the originating client a question or open a [modal](https://docs.macro-deck.app/ui/views/modal/). `null` when nobody is there to ask - handle it. |
| `CallDepth` | Script hops this run is nested behind. Pass it on, incremented, when handing work to another Macro Deck. |

### Options that depend on provider state

```csharp
internal sealed class JoinChannelAction(DiscordClient client) : IDynamicOptionsActionDefinition
{
	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("guildId", label: Strings.Parameters.Server(), required: true),
		ActionParameter.DynamicChoice("channelId", label: Strings.Parameters.Channel(), required: true)
	];

	public async Task<DynamicOptionsResult> GetDynamicOptionsAsync(
		DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		if (!client.IsConnected)
		{
			return new DynamicOptionsResult { Options = [], Error = Strings.Errors.DiscordNotRunning() };
		}

		if (context.ParameterName == "channelId")
		{
			if (context.CurrentParameters.GetValueOrDefault("guildId") is not string guildId)
			{
				return new DynamicOptionsResult { Options = [], Error = Strings.Errors.PickServerFirst() };
			}

			var channels = await client.GetChannelsAsync(guildId, cancellationToken);
			return new DynamicOptionsResult
			{
				Options = [.. channels.Select(c => new ActionParameterOption { Value = c.Id, Label = c.Name })],
				CacheSeconds = 15
			};
		}

		var guilds = await client.GetGuildsAsync(cancellationToken);
		return new DynamicOptionsResult
		{
			Options = [.. guilds.Select(g => new ActionParameterOption { Value = g.Id, Label = g.Name })]
		};
	}

	// Id, Name, Description, CreateExecutor omitted.
}
```

`DynamicChoice`, `Autocomplete` and `MultiSelect` without static options are filled by
`GetDynamicOptionsAsync`. `context.ParameterName` says which list is wanted, `CurrentParameters` holds the
rest of the (possibly unfinished) draft and `Filter` the typed text.

- **`Error` explains an empty list.** Set it to a localized message when you cannot answer right now
  (not connected, a prerequisite missing) instead of returning an unexplained empty list. A non-empty
  `Error` **replaces** the options in the editor. An empty list without an error is fine when there is
  legitimately nothing to offer.
- **`AllowsCustomValue`** lets the user type a value that is not in the list; **`CacheSeconds`** lets the
  editor reuse the answer.
- **Give an optional dynamic choice a `placeholder`** ("First available"): options are only fetched when
  the list opens, so until then an empty field would read as "still to choose".

### Options Macro Deck answers

Some lists are Macro Deck's own. Name one of the ids in `HostOptionsSources` (`MacroDeck.Sdk.Actions`) as the
parameter's `optionsSourceId`, and Macro Deck fills the list itself; `GetDynamicOptionsAsync` is not asked for
that parameter:

```csharp
ActionParameter.Autocomplete("variable",
	label: Strings.Parameters.SaveTo(),
	optionsSourceId: HostOptionsSources.UserVariables,
	required: true)
```

| Id | Lists | Option value |
| --- | --- | --- |
| `HostOptionsSources.Variables` | every variable, a typed name allowed | the canonical name |
| `HostOptionsSources.UserVariables` | the user's own variables, a typed name allowed | the canonical name |
| `HostOptionsSources.Devices` | the devices paired with Macro Deck | the device id |
| `HostOptionsSources.AndroidDevices` | the connected Android devices, after an empty "default device" option | the serial |

The ids are the strings Macro Deck has always answered, so a parameter declared with them works on every
Macro Deck version; a version that does not know an id offers no options for it. Widget pickers use
`WidgetOptionsSources` the same way.

### Configuring with a UI tree

```csharp
internal sealed class ToggleAction : IUiConfigurableActionDefinition
{
	public Task<IUiSession?> CreateConfigurationSessionAsync(
		ActionConfigurationRequest request, CancellationToken cancellationToken)
		=> Task.FromResult<IUiSession?>(new ToggleConfigSession(request.Parameters));

	// IActionDefinition members omitted - Parameters is still required.
}
```

Implement `IUiConfigurableActionDefinition` when a Macro Deck UI tree expresses the configuration better
than a flat list; the descriptor then reports `configuresWithUiTree`. `Parameters` stays authoritative: it
is what a client that cannot render a tree falls back to and what the host persists into. Returning `null`
declines and is not an error. See [Serving a configuration view](https://docs.macro-deck.app/ui/views/configuration/#from-an-action).

### Inside an action flow

Action flows are user-authored block trees - action calls, conditions, delays, loops, scripts - stored and
run by the host's flow engine. Widgets, scripts and automations trigger them. Your integration
participates only through the actions it exposes; it does not own the flow graph or the scheduler, and
the persisted flow model is a host contract, not SDK surface.

What that means for an executor:

- **Failures propagate.** The flow engine does not treat every invoked action as successful: a `Failed`
  result (or an exception) is recorded and the originating client is told.
- **Cancellation stops the flow.** Pass `context.CancellationToken` to every await.
- **Widget-less runs are normal.** `OwnerWidgetId`, `Interactions` and `Ui` can all be `null`.

#### Long-running work

```csharp
private async Task<ActionResult> ConfirmAsync(Func<MeldState, bool> reached, CancellationToken cancellationToken)
{
	var deadline = DateTime.UtcNow + TimeSpan.FromSeconds(5);
	while (!reached(_state))
	{
		var remaining = deadline - DateTime.UtcNow;
		if (remaining <= TimeSpan.Zero)
		{
			return ActionResult.Accepted();
		}

		try
		{
			await _stateChanged.WaitAsync(remaining, cancellationToken);
		}
		catch (TimeoutException)
		{
			break;
		}
	}

	return reached(_state) ? ActionResult.Success() : ActionResult.Accepted();
}
```

Never poll or wait unbounded in an executor. When you have to wait for confirmation, use a bounded
timeout and then return the truthful answer: `Failed(ActionErrorCodes.Timeout, ...)` when completion
should have been confirmable, `Accepted` when the provider simply does not report it. The built-in Meld
integration uses the pattern above after starting a stream.

### Over the plugin protocol

| Operation | SDK member |
| --- | --- |
| `describe` | `Actions` and each definition's parameters and capabilities |
| `execute` | `CreateExecutor().ExecuteAsync` |
| `options` | `IDynamicOptionsActionDefinition.GetDynamicOptionsAsync` |
| `state` | [`IStateProviderActionDefinition.GetActionStateAsync`](https://docs.macro-deck.app/features/button-states/) |
| `icon`, `icon.content` | [`IIconProviderActionDefinition`](https://docs.macro-deck.app/features/button-icons/) |

`PluginTestHarness.Actions` drives each operation the way the host does - see
[Testing](https://docs.macro-deck.app/features/testing/).

### See also

- [Button states](https://docs.macro-deck.app/features/button-states/) and [Button icons](https://docs.macro-deck.app/features/button-icons/)
- [Serving a configuration view](https://docs.macro-deck.app/ui/views/configuration/)
- [Localization](https://docs.macro-deck.app/features/localization/)
- [Capability parity](https://docs.macro-deck.app/reference/capability-parity/#failure-behavior)

## Android devices

> Source: https://docs.macro-deck.app/features/android-devices/
>
> Work with Android devices through Macro Deck's own ADB connection with IAndroidDeviceManager - the host:adb permission, the user's control, operations, errors, limits and testing.

A plugin can press keys, tap, type, start apps, take screenshots, run shell commands, read the battery, copy
files and install or uninstall apps on an Android device through Macro Deck's own ADB (Android Debug Bridge)
connection. Macro Deck finds the
`adb` program, runs the ADB server and tracks the attached devices; your plugin ships no `adb` client of
its own and never talks to the ADB server directly.

### Quick start

Declare the permission in `manifest.json`:

```json
"permissions": ["host:adb"]
```

Then take `IAndroidDeviceManager` from dependency injection:

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Android;

public sealed class PhoneIntegration(IAndroidDeviceManager android) : IPluginIntegration
{
	public IReadOnlyList<IActionDefinition> Actions => [new SleepPhoneAction(android)];

	// Other IPluginIntegration members omitted.
}

internal sealed class SleepPhoneAction(IAndroidDeviceManager android) : IActionDefinition
{
	public string Id => "sleep-phone";

	public LocalizedText Name => Strings.Actions.SleepPhone();

	public LocalizedText Description => Strings.Actions.SleepPhoneDescription();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
		[ActionParameter.Text("serial", label: Strings.Parameters.Serial(), required: true)];

	public IActionExecutor CreateExecutor() => new Executor(android);

	private sealed class Executor(IAndroidDeviceManager android) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (android.Access != AndroidDeviceAccess.Available)
			{
				return ActionResult.Failed(ActionErrorCodes.PermissionDenied, Strings.Errors.AdbNotAvailable());
			}

			if (context.Parameters.GetValueOrDefault("serial") is not string serial ||
				android.FindDevice(serial) is not { State: AndroidDeviceState.Online } device)
			{
				return ActionResult.Failed(ActionErrorCodes.NotConnected, Strings.Errors.PhoneNotConnected());
			}

			try
			{
				await device.SendKeyAsync(AndroidKey.Sleep, context.CancellationToken);
				return ActionResult.Success();
			}
			catch (AndroidDeviceException)
			{
				return ActionResult.Failed(ActionErrorCodes.ProviderError, Strings.Errors.PhoneRefused());
			}
		}
	}
}
```

The user gets a **Sleep phone** action that turns off the screen of the phone with that serial.

Things to know:

- **Resolve it from DI, or read `context.AndroidDevices`.** Take it in a constructor, like any other
  service; the SDK registers it for every plugin. `IIntegrationContext.AndroidDevices` returns the same
  instance, for code that only has the context.
- **Check `Access` before you rely on it.** Whether your plugin may use ADB is the user's decision and
  can change while your plugin runs - see [Who decides](#who-decides).
- **Macro Deck owns the devices.** It discovers, connects and forgets them. A plugin never creates,
  connects or disposes a device.

### Declaring `host:adb`

An installed plugin reaches ADB only when its manifest lists `host:adb` in
[`permissions`](https://docs.macro-deck.app/reference/manifest/#permissions). It is one of the two permissions the host enforces,
next to [`host:companion-devices`](https://docs.macro-deck.app/features/companion-devices/#declaring-hostcompanion-devices); every
other entry in the vocabulary is still declared for disclosure only. If plugins are not allowed to use ADB
when the user installs the first version of your plugin that declares it, Macro Deck asks the user whether
to allow it. It does not ask again for an update of a version that already declared it.

A plugin you run yourself during development, through a
[developer token](https://docs.macro-deck.app/reference/authentication/#developer-token-headless-enrolment) or
[interactive pairing](https://docs.macro-deck.app/reference/authentication/#self-registering-interactive-pairing), is allowed without
the declaration, because you admitted it by hand. Declare it anyway: the packaged plugin needs it.

### Who decides

`Access` is `Available` only when all of these hold:

| Condition | Where the user controls it | `Access` otherwise |
| --- | --- | --- |
| ADB is enabled in Macro Deck | **Settings > ADB**, **Enable ADB** | `AdbNotEnabled` |
| Plugins may use ADB | **Settings > ADB**, **Allow plugins to use ADB** (on by default) | `AdbNotAllowed` |
| The plugin declares `host:adb` | The installed version's manifest | `AdbNotAllowed` |

The user sees the permission before and after installing: the install dialog says the plugin uses ADB,
and the plugin's page lists **Uses ADB** under its capabilities. When a plugin that declares `host:adb` is installed
while **Enable ADB** or **Allow plugins to use ADB** is off, Macro Deck asks the user in a dialog, and
keeps the question in its notifications, whether to turn both on. It asks the same way, once per run of
Macro Deck, when your plugin calls an ADB operation and is refused for either reason, or when ADB is on
but Macro Deck cannot find adb (the call then fails with `AdbUnavailable` and the user is offered the
platform-tools download); a plugin that does not declare `host:adb` is refused without asking. That switch covers every plugin that
declares the permission, not only yours. The user guide describes
all of this in [Plugins and ADB](https://docs.macro-deck.app/guide/usb-connection/#plugins-and-adb).

| `AndroidDeviceAccess` | Meaning |
| --- | --- |
| `Unsupported` | The host has not reported access yet, or predates this API. |
| `Available` | This plugin may use ADB now. |
| `AdbNotEnabled` | ADB is switched off in Macro Deck. |
| `AdbNotAllowed` | ADB is on, but this plugin may not use it. |

Tell the user which of these applies rather than a generic failure: only the user can change it, and the
fix differs. `AccessChanged` is raised whenever the value changes.

### Devices and events

```csharp
android.DeviceConnected += (_, e) => _ = RefreshBatteryAsync(e.Device);
android.DeviceStateChanged += (_, e) =>
{
	if (e.Device.State == AndroidDeviceState.Online && e.PreviousState != AndroidDeviceState.Online)
	{
		_ = RefreshBatteryAsync(e.Device);
	}
};
```

- **`Devices` lists every attached device in any state**, and is empty unless `Access` is `Available`.
  `FindDevice(serial)` returns one of them, or `null`.
- **A device is one stable instance.** The same `IAndroidDevice` stays valid while the device goes
  offline, is unauthorized or reconnects, so you may keep it. `Serial` identifies it.
- **`State`** is `Online` (ready for operations), `Connecting` (waiting for the user to confirm the
  authorization prompt on the device), `Unauthorized`, or `Offline`. Operations need `Online`.
- **`Info`** carries `Model`, `Manufacturer` and `Product` as the device reports them; any of them can be
  `null` until the device is online.
- **`Info.StableId`** is the same for the same hardware over USB and Wi-Fi, and across a Wi-Fi port change,
  while `Serial` differs per connection. It is a keyed hash of the device's hardware serial with a key
  unique to this Macro Deck installation, so it cannot be matched against a serial, or between two
  installations. It is `null` until Macro Deck has read it and on an older host, and it is the local id
  under which the built-in ADB integration publishes the device's [battery](https://docs.macro-deck.app/features/batteries/), so a
  plugin with `host:adb` can tell which battery entry belongs to which device.
- **`LacksUsbPermission`** is `true` for an `Unauthorized` device the computer lacks the USB permissions
  for, a missing Linux udev rule for example, rather than one that has not authorized this computer. Tell
  the user which: the fix differs. A change of it raises `DeviceStateChanged` even though `State` stays
  `Unauthorized`. It is always `false` on an older host.
- **`Mode`** tells an `Offline` device in the `Bootloader`, `Recovery` or `Sideload` apart from one that is
  simply not answering (`Normal`); `Unknown` is a state adb reported that Macro Deck does not recognise. It is
  `Normal` for every other state. A change of it raises `DeviceStateChanged` even though `State` stays
  `Offline`. It is always `Normal` on an older host.
- **`IsAdbUnavailable`** on the manager is `true` while `Access` is `Available` but Macro Deck cannot find the
  `adb` program: no device can appear and every operation fails with `AdbUnavailable`, so tell the user to
  install the platform tools in **Settings > ADB** rather than to attach a device. A change raises
  `AccessChanged`. It is always `false` on an older host.
- **`DefaultDevice`** is the device to use when the user picked none: the default device chosen in
  **Settings > ADB**, or the only attached device when none is chosen. It is `null` when none is chosen and
  not exactly one device is attached. A chosen default device that has just gone away is still returned, so
  check `FindDevice(DefaultDevice.Serial)` before you treat it as attached; its operations then fail with
  `DeviceOffline` or `DeviceNotFound`. It is `null` on an older host.
- **`DeviceDisconnected`** is also raised for every device when access is withdrawn.
- **Handlers run on the connection's receive loop.** Keep them short and start real work, such as an
  operation on the device, without awaiting it in the handler. An exception from a handler is logged and
  does not end the connection.

### Operations

| `IAndroidDevice` member | What it does |
| --- | --- |
| `ExecuteShellAsync(command)` | Runs `command` in the device's shell and returns an `AndroidShellResult`. |
| `GetBatteryStateAsync()` | Returns `Level` (0 to 100), `IsCharging`, `Status` and `Health`. |
| `PushFileAsync(localPath, remotePath)` | Copies a file from the computer to the device. |
| `PullFileAsync(remotePath, localPath)` | Copies a file from the device to the computer. |
| `InstallApkAsync(apkPath)` | Installs an APK, replacing an installed version of the same app. |
| `UninstallPackageAsync(packageName)` | Uninstalls an app. |
| `IsPackageInstalledAsync(packageName)` | Whether an app is installed. |
| `SendKeyAsync(key)` | Presses one `AndroidKey`, such as `Home`, `Wakeup`, `Sleep`, `VolumeUp` or `MediaPlayPause`. |
| `TapAsync(x, y)` | Taps the screen at a point, in screen pixels from the top left. |
| `SwipeAsync(fromX, fromY, toX, toY, duration)` | Swipes from one point to another. |
| `InputTextAsync(text)` | Types text into the focused field. |
| `StartAppAsync(packageName)` | Starts an app's launcher activity, or brings the app to the front. |
| `ForceStopAppAsync(packageName)` | Force-stops an app. |
| `OpenUriAsync(uri)` | Opens a URI with the app the device picks for it. |
| `RebootAsync(mode)` | Restarts the device into Android, recovery or the bootloader (`AndroidRebootMode`). |
| `CaptureScreenshotAsync()` | Returns the current screen as PNG bytes. |
| `GetStatusAsync()` | Returns whether the screen is on, whether the lock screen shows, and the foreground app. |

Every operation is a round trip to Macro Deck, so do not call them in a tight loop.

#### Keys, touches, apps and screenshots

```csharp
await device.SendKeyAsync(AndroidKey.Wakeup, cancellationToken);
await device.StartAppAsync("com.spotify.music", cancellationToken);
var png = await device.CaptureScreenshotAsync(cancellationToken);
```

- **These are fixed commands.** Macro Deck builds the adb command itself and validates and quotes every
  argument, so they need no shell and keep working while Macro Deck is locked, see [Limits](#limits).
  Coordinates are 0 to 8192, a swipe lasts at most five seconds, text is at most 500 characters, a URI at
  most 2000. An argument outside these fails with `InvalidArgument` before adb runs.
- **A screenshot is at most 8 MiB for a plugin.** It travels in chunks after the reply; a larger one fails
  with `CommandFailed`.
- **`GetStatusAsync` returns `null` until Macro Deck has a reading.** Macro Deck reads the screen state in
  the background for every device someone asked about recently and shares the reading between callers, so
  the first call starts the readings and returns `null`; ask again a few seconds later. A value the device
  does not report is `null`.

#### Shell commands

```csharp
var result = await device.ExecuteShellAsync("getprop ro.build.version.release", cancellationToken);
if (result.ExitCode == 0)
{
	var version = result.StandardOutput.Trim();
}
```

- **A non-zero exit code is a result, not an exception.** Check `ExitCode` yourself.
- **Devices before Android 7 always report exit code 0**, whatever the command did. On those devices,
  judge success from the output.
- **The command runs as given** by the device's shell, with Macro Deck's ADB identity. It must not be
  empty, may be at most 8 KiB, and must not start with `-`.
- **There is no standard input.** A command that waits for input sees end of input at once.
- **Long output is cut.** `Truncated` is `true` when Macro Deck shortened the standard output or error
  to fit one protocol message. Redirect large output to a file on the device and pull it instead.

#### Battery

Macro Deck shares one battery reading between all callers, so a result can be a few seconds old. A
device that does not report its battery fails with `Unsupported`.

#### Connecting over Wi-Fi

`ConnectAsync("192.168.1.20:5555")` connects Macro Deck's adb to a device with wireless debugging on, the
same as `adb connect`. The address is `host:port` with a host name or IPv4 address, and becomes the
device's serial. It returns the device, which stays attached for every plugin and in **Settings > ADB**
until it disconnects; its `State` can be `Offline` for a moment until Macro Deck reports it `Online`.
Connecting a connected device succeeds. An address adb cannot reach fails with `CommandFailed` and adb's
own message; a malformed one fails with `InvalidArgument` before adb runs. It is refused while Macro Deck
is locked. Users can connect a device themselves in **Settings > ADB**, **Connect over Wi-Fi**; a device
connected either way is visible to both.

Android 11 and later pair a new computer with a code before the first wireless connection. Macro Deck
does not pair; a device that was never paired with this computer, or never switched to network debugging
over USB (`adb tcpip`), refuses the connection.

#### Files and apps

- **Paths on the computer are absolute paths on the machine Macro Deck runs on.** Macro Deck reads and
  writes them as the user it runs as, not as your plugin. A file to push or install must exist; the
  directory of a file to pull must exist.
- **Paths on the device are absolute**, starting with `/`.
- **Package names** use Android's grammar, such as `com.example.app`.
- A refused install or uninstall fails with `CommandFailed`, and the message carries adb's own text.

### Errors

Every operation throws `AndroidDeviceException` when it cannot be carried out, and
`OperationCanceledException` when you cancel it. `ErrorCode` says why:

| `AndroidDeviceErrorCode` | Meaning | What to do |
| --- | --- | --- |
| `AdbNotEnabled` | ADB is switched off in Macro Deck. | Ask the user to turn on **Enable ADB**. |
| `AdbNotAllowed` | ADB is on, but this plugin may not use it. | Ask the user to turn on **Allow plugins to use ADB**, or declare `host:adb`. |
| `AdbUnavailable` | Macro Deck cannot find `adb`, or cannot reach its server. | Point the user to **Settings > ADB**. |
| `DeviceNotFound` | No device with this serial is attached. | Wait for `DeviceConnected`. |
| `DeviceOffline` | The device is attached but not reachable. | Wait for `DeviceStateChanged`. |
| `DeviceUnauthorized` | The device has not authorized this computer. | Ask the user to confirm the prompt on the device. |
| `Timeout` | adb did not finish in time. | Retry, or split the work. |
| `CommandFailed` | adb ran and reported a failure, such as a rejected install. | Show the message. |
| `InvalidArgument` | An argument was rejected before anything ran. | Fix the call. |
| `HostUnavailable` | There is no connection to Macro Deck. | Retry after the plugin reconnects. |
| `Unsupported` | The host does not offer ADB to plugins, or the device cannot answer this operation. | Degrade the feature. |
| `HostLocked` | Macro Deck is locked. | Retry after it is unlocked. |
| `RateLimited` | Too many calls at once or in quick succession. | Retry later. |
| `Unknown` | A failure this SDK version does not recognise. | Treat as a failure. |

`AdbNotEnabled` and `AdbNotAllowed` are the user's settings, everything from `AdbUnavailable` to
`CommandFailed` is adb or the device, and `HostLocked` and `RateLimited` are temporary. `Access` tells the
first two apart before you call anything.

### Limits

- **At most four calls in flight per plugin.** A fifth is refused at once with `RateLimited`; it is not
  queued. ADB calls also count toward the plugin's shared callback throttle.
- **While Macro Deck is locked**, shell commands, pushes, pulls, installs, uninstalls and connects are refused with
  `HostLocked`. Battery reads, `IsPackageInstalledAsync` and the fixed operations (keys, taps, swipes, text,
  starting and stopping apps, opening a URI, reboots, screenshots and the status) still work, for plugins and
  built-in integrations alike, so a deck button bound to one keeps working on a locked computer.
- **Every operation has a time limit** on the host, about a minute for a shell command or an uninstall,
  five minutes for a push, pull or install, twenty seconds for a connect, and ten seconds for the battery
  and package queries. It then
  fails with `Timeout`. Pass a `CancellationToken` to give up sooner: cancelling also ends the call on the
  host.

### Integrations built into Macro Deck

Macro Deck's own integrations reach ADB through the same `IAndroidDeviceManager`, read from
`IIntegrationContext.AndroidDevices` (see [ADR 0107](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0107-built-in-integrations-are-built-as-extractable-plugins.md)).
For them `Access` is `Available` whenever ADB is enabled: they are part of Macro Deck, so neither
**Allow plugins to use ADB** nor `host:adb` applies. Everything else does, the locked-host rule and the
shell output limit included. Should such an integration ever move out of process, it becomes a plugin like
any other and needs `host:adb` and the user's permission.

The built-in ADB integration uses nothing else. Its actions run the fixed operations on the device the user
picked or on `DefaultDevice`, its variables read `Devices`, `DefaultDevice`, `GetStatusAsync` and the
battery, its issues use `LacksUsbPermission`, an action reports a missing adb from `IsAdbUnavailable`
before it looks for a device, and it derives its own device events (connected,
disconnected, authorized, unauthorized, online, offline) from `DeviceConnected`, `DeviceDisconnected` and
`DeviceStateChanged`, remembering a device that went away for five minutes so that its return reads as
online again.

The built-in ADB integration's battery provider is written against this API alone and is a worked example
of it: it publishes each device under `Info.StableId`, skips a device until it reports one, reads
`GetBatteryStateAsync` on every change and every 15 seconds, and asks
`getprop ro.build.characteristics` once per device to tell a tablet from a phone.

### Older hosts

On a Macro Deck that predates this API, `Access` stays `Unsupported`, `Devices` stays empty and every
operation fails with `Unsupported`. A host that predates the fixed operations fails each of them with
`Unsupported`, answers `GetStatusAsync` with `null`, reports `LacksUsbPermission` as `false` (such a device
still reads `Unauthorized`), `Mode` as `Normal` (a device in recovery still reads `Offline`),
`IsAdbUnavailable` as `false` and `DefaultDevice` as `null`. An `IAndroidDevice` or `IAndroidDeviceManager` you
implemented yourself against an older SDK behaves the same way through the default interface members. A
host that predates `StableId` leaves it `null`, and a context from a
host that offers no ADB to integrations answers `context.AndroidDevices` with an always-`Unsupported`
manager. A plugin that uses ADB for an optional feature keeps working there with
that feature off. Set a minimum host version in
[`compatibility.macroDeck`](https://docs.macro-deck.app/reference/manifest/#compatibility) if ADB is the point of your plugin.

### Testing

`MacroDeck.Plugin.Testing` has an in-memory `FakeAndroidDeviceManager`:

```csharp
var android = new FakeAndroidDeviceManager();
var phone = android.AddDevice("R58M123", info: new AndroidDeviceInfo("SM-G991B", "samsung", "o1s"));
phone.ShellHandler = command => new AndroidShellResult(0, "14\n", string.Empty, false);

var version = await new PhoneInfo(android).GetAndroidVersionAsync("R58M123");

Assert.That(version, Is.EqualTo("14"));
Assert.That(phone.Calls.Single().Operation, Is.EqualTo(nameof(IAndroidDevice.ExecuteShellAsync)));
```

- **Access starts as `Available`.** `SetAccess` changes it and refuses every operation with the matching
  error, as a real host does. `AddDevice`, `RemoveDevice` and `SetDeviceState` raise the matching events.
- **`FakeAndroidDevice`** records every call in `Calls`. `ShellHandler`, `Battery`, `Screenshot`, `Status`
  and `InstalledPackages` script its answers, and `Failure` makes every operation throw with that code.
- **`DefaultDeviceSerial`** on the manager names the default device; left `null`, `DefaultDevice` is the only
  attached device. `SetLacksUsbPermission` and `SetDeviceMode` change a device's `LacksUsbPermission` and `Mode` and raise
  `DeviceStateChanged`; `SetAdbUnavailable` changes `IsAdbUnavailable` and raises `AccessChanged`. A device removed and added again comes back as the same instance.
- **`StableId`** on a `FakeAndroidDevice` sets `Info.StableId` later, like a host that reads it after the
  device attached. No event is raised.
- **In a `PluginTestHarness`**, `harness.Context.AndroidDevices` is the plugin's manager, both through DI and
  through `context.AndroidDevices`. Its `Access` starts as `Unsupported`, as the harness has always
  reported; call `SetAccess(AndroidDeviceAccess.Available)` and `AddDevice` to script it. A plugin that
  registers its own manager with
  `builder.ConfigureServices((_, services) => services.AddSingleton<IAndroidDeviceManager>(android))` keeps
  it, and `context.AndroidDevices` then returns that one.

### Security

`host:adb` is user control and consent, not a sandbox. A plugin process runs with the user's full
privileges and could start its own `adb` without asking. What the permission gives the user is a
visible, switchable decision about plugins that use Macro Deck's connection. See
[the security model](https://docs.macro-deck.app/policies/security/#permissions-declared-not-enforced).

### See also

- [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#adb) - the `adb` host API on the wire.
- [Manifest](https://docs.macro-deck.app/reference/manifest/#permissions) - the permission vocabulary.
- [Connect over USB](https://docs.macro-deck.app/guide/usb-connection/) - how users set up ADB.
- [Batteries](https://docs.macro-deck.app/features/batteries/) - Android batteries are already in the battery catalog, readable without `host:adb`.

## Batteries

> Source: https://docs.macro-deck.app/features/batteries/
>
> Report battery levels of phones, headphones, controllers and other devices with IBatteryProvider, and read every provider's devices with IIntegrationContext.Batteries - device model, removed and withdrawn devices, stable ids, limits, older hosts, security and testing.

Macro Deck keeps one catalog of battery-powered devices: phones, headphones, controllers, mice, keyboards
and the like. A **battery provider** reports the devices it knows and their charge; Macro Deck shows them
in the Battery widget, gives each one variables, and lets every plugin read the whole catalog.

You publish, Macro Deck never asks. The provider polls or listens however its devices need and pushes
what it finds; there is no host-side polling to answer.

### Quick start

An integration implements `IBatteryProvider` next to its other interfaces. The one below reports the
battery of a wireless headset:

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Batteries;

public sealed class HeadsetIntegration(IHeadsetWatcher watcher) : IPluginIntegration, IBatteryProvider
{
	private IBatteryProviderContext? _batteries;

	public string ProviderName => "Example Headsets";

	public async Task InitializeAsync(IBatteryProviderContext context, CancellationToken cancellationToken = default)
	{
		_batteries = context;
		await context.PublishAsync([.. watcher.Headsets.Select(Describe)], cancellationToken);
		watcher.Changed += OnHeadsetChanged;
	}

	public Task ShutdownAsync(CancellationToken cancellationToken = default)
	{
		watcher.Changed -= OnHeadsetChanged;
		_batteries = null;
		return Task.CompletedTask;
	}

	private void OnHeadsetChanged(object? sender, Headset headset)
		=> _ = _batteries?.PublishAsync(Describe(headset));

	private static BatteryDevice Describe(Headset headset) => new()
	{
		Id = headset.PairingId,
		Name = headset.Name,
		Kind = BatteryDeviceKinds.Headphones,
		LevelPercent = headset.Level,
		ChargeState = headset.IsCharging ? BatteryChargeState.Charging : BatteryChargeState.Discharging,
		IsConnected = headset.IsInRange
	};

	// IPluginIntegration members omitted.
}
```

The headset now appears in the Battery widget's device list, and Macro Deck creates its
`battery_<name>_<hash>_level`, `_charging`, `_connected`, `_state`, `_time_remaining_minutes`,
`_time_to_full_minutes` and `_health` variables under your plugin (see [Variables](#variables)).

Things to know:

- **Order is fixed.** Macro Deck calls `IBatteryProvider.InitializeAsync` after the integration's own
  `InitializeAsync`, and `IBatteryProvider.ShutdownAsync` before the integration stops.
- **The context is yours until `ShutdownAsync` returns.** Keep it and publish whenever something changes.
- **Devices are always published under your plugin or integration.** Nothing in a `BatteryDevice` names
  its owner, so you cannot publish or remove another provider's devices.
- **`ProviderName` is optional.** Left empty, Macro Deck shows your plugin's or integration's name.

### Publishing devices

| `IBatteryProviderContext` member | What it does |
| --- | --- |
| `PublishAsync(device)` | Adds a device, or replaces the one published under the same `Id`. |
| `PublishAsync(devices)` | Adds or replaces several devices in one call. All or nothing: when one is refused, none is applied. An empty list does nothing. |
| `RemoveAsync(deviceId)` | Removes a device for good. Removing an unknown id does nothing. |

`BatteryDevice` is a record with init-only properties. Every property is checked when it is set, so an
instance that exists is always publishable:

| Property | Meaning |
| --- | --- |
| `Id` | Required. Your own stable id for the device - see [Stable ids](#stable-ids). |
| `Name` | Required. The name Macro Deck shows. |
| `Kind` | One of `BatteryDeviceKinds`, `other` by default - see [Kinds](#kinds). |
| `LevelPercent` | 0 to 100, or `null` when the device does not report one. Outside the range throws `ArgumentOutOfRangeException`. |
| `ChargeState` | `Unknown`, `Discharging`, `Charging`, `Full`, or `NotCharging` (on power but not charging). |
| `IsConnected` | Whether the device is reachable right now. `true` by default. |
| `TimeRemaining`, `TimeToFull` | Optional estimates. Negative throws `ArgumentOutOfRangeException`. |
| `Health` | `Unknown`, `Good`, `Overheat`, `Dead`, `OverVoltage`, `Cold` or `Failure`. |

A list that contains `null` or the same id twice throws `ArgumentException`; a publish that would leave you
with more than 64 devices throws `InvalidOperationException` - see [Limits](#limits). The exact bounds are
in
[`BatteryLimits.cs`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/sdk/src/MacroDeck.Sdk/Batteries/BatteryLimits.cs).

Publish a change when it happens and nothing in between: an unchanged device costs a round trip for
nothing.

#### Kinds

`phone`, `tablet`, `laptop`, `headphones`, `watch`, `controller`, `mouse`, `keyboard`, `speaker`, `other`,
as constants on `BatteryDeviceKinds`. The kind picks the icon a reader draws. A reader shows a kind it does
not know as `other`, and a charge state or health it does not know as unknown, so a newer provider keeps
working with an older Macro Deck.

### Connected, withdrawn and removed

A device leaves the catalog in two different ways, and readers treat them differently:

| What happened | Who does it | What readers see |
| --- | --- | --- |
| **Out of reach**: unplugged, out of range, switched off | You publish it with `IsConnected = false` | The device stays, shown as not connected, with its name and last level. Its `_state` reads `disconnected` and both time variables read 0. |
| **Withdrawn**: your provider stopped or was initialized again, the user turned your plugin or integration off, your plugin's session ended, Macro Deck shut down | Macro Deck | The device leaves the list but may come back under the same id. Its variables stay: `_connected` and `_charging` are false, `_state` reads `disconnected`, `_time_remaining_minutes` and `_time_to_full_minutes` read 0, and `_level` and `_health` keep the last reported values; a widget showing it shows its stored name as not available. |
| **Removed for good**: unpaired, forgotten, deleted | You call `RemoveAsync` | The device leaves the list and its id is in `RemovedIds`. Its variables are deleted. |

So keep a device you merely lost contact with published as not connected, and remove it only once it is
gone for good. You never have to clean up on the way out: when your provider stops, Macro Deck withdraws
its devices itself, and the next `InitializeAsync` publishes them again.

**Re-initializing starts from an empty set.** When Macro Deck initializes your provider again while your
plugin stays connected, for example after the user changed its configuration, the devices you published
before are withdrawn first, and the new `InitializeAsync` publishes what the new configuration covers. A
device you no longer report is therefore not left behind, but it is only withdrawn: its variables stay, with
`_connected` false and `_state` reading `disconnected`. Call `RemoveAsync` before the provider stops for a device that is gone for good, such as
one the user removed from your configuration.

### Variables

You write no variable code for your devices. Macro Deck writes the seven variables of every device itself
and files them under the plugin or integration that published it, so they are listed with your other
variables and an Android phone's are listed under the ADB integration. What each one reads is described in
[Battery variables](https://docs.macro-deck.app/guide/concepts/#battery-variables).

- **Do not create these names yourself.** Macro Deck never takes over a variable you created: if yours
  already has a device variable's name, that one variable is not written for the device. `IVariableApi.GetAllAsync` lists them among your variables;
  leave them alone rather than deleting them.
- **They never go stale.** Macro Deck pushes them, so they stay available however long a level stays the
  same, unlike a variable you declare for polling.
- **They follow your devices.** A withdrawn device keeps its variables as not connected, a device you
  remove for good loses them, and they are deleted with the rest of your variables when the user uninstalls
  your plugin.

### Stable ids

`Id` is the device's identity, and readers store it: a Battery widget configured for one device keeps
that device's id, and the device's variable names carry a hash of it. Publishing the same id again
updates the device; a new id is a new device.

- **Derive it from something that stays the same** across restarts and reconnects, such as a pairing id,
  never from a connection handle or a list position.
- **Do not publish a hardware serial or anything else the user would not share.** Every plugin can read
  the id. Hash it with a secret of your own if the stable source is sensitive, the way the
  [ADB provider](#the-adb-provider) does.
- **Readers see a qualified id.** Macro Deck prefixes your id with the provider that published it,
  `<plugin or integration id>:<your id>`, so two providers never collide.

### Reading devices

Every integration reads the whole catalog, whoever published it, through `IIntegrationContext.Batteries`:

| `IBatteryApi` member | What it does |
| --- | --- |
| `Devices` | Every device currently published, as `BatteryDeviceSnapshot`. Empty until Macro Deck has sent the first list. |
| `Find(id)` | The device with that qualified id, or `null`. |
| `Changed` | Raised after `Devices` changed. `RemovedIds` lists the qualified ids removed for good in that change. |

A `BatteryDeviceSnapshot` carries the published fields plus `Id` (qualified), `LocalId`, `ProviderId`,
`ProviderName` and `UpdatedAt`, when Macro Deck last received a report for it.

- **A device absent from `Devices` and not in `RemovedIds` was withdrawn** and may come back under the same
  id. Keep what you stored about it.
- **`RemovedIds` is best effort.** A plugin that was disconnected while a device was removed does not see
  the removal; `Devices` is always complete.
- **Handlers run on a background thread.** One that throws is logged and does not affect the others.
  Handlers subscribed through `IIntegrationContext.Batteries` are released when Macro Deck shuts your
  integration down or initializes it again. In a plugin, `IBatteryApi` can also be taken from dependency
  injection; handlers subscribed there are yours to remove.

A widget that shows the device with the lowest battery, live:

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Batteries;
using MacroDeck.Sdk.Ui;
using MacroDeck.Ui.Components;
using MacroDeck.Ui.Dsl;
using MacroDeck.Ui.Model.Surfaces;
using MacroDeck.Ui.Runtime;

public sealed class LowestBatteryIntegration : IPluginIntegration, IUiProvider
{
	private IBatteryApi _batteries = UnsupportedBatteryApi.Instance;

	public Task InitializeAsync(IIntegrationContext context)
	{
		_batteries = context.Batteries;
		return Task.CompletedTask;
	}

	public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
		[new() { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared }];

	public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
	{
		if (request.Surface.Kind != UiSurfaceKinds.Widget)
		{
			return Task.FromResult<IUiSession?>(null);
		}

		var batteries = _batteries;
		var lowest = new UiState<BatteryDeviceSnapshot?>(Lowest(batteries.Devices));
		void OnChanged(object? sender, BatteryDevicesChangedEventArgs e) => lowest.Value = Lowest(batteries.Devices);
		batteries.Changed += OnChanged;

		var root = new UiStack
		{
			Key = "lowest",
			Children =
			[
				new UiTextRun { Key = "name", Text = UiText.From(() => lowest.Value?.Name ?? string.Empty) },
				new UiTextRun
				{
					Key = "level",
					Text = UiText.From(() => lowest.Value?.LevelPercent is { } level ? $"{level} %" : "--"),
					Size = 0.4
				}
			]
		};

		return Task.FromResult<IUiSession?>(
			new ViewSession(new UiView(request.Surface, root), onDispose: () => batteries.Changed -= OnChanged));
	}

	private static BatteryDeviceSnapshot? Lowest(IReadOnlyList<BatteryDeviceSnapshot> devices)
		=> devices.Where(device => device is { IsConnected: true, LevelPercent: not null })
			.MinBy(device => device.LevelPercent);

	// Other IPluginIntegration members omitted.
}
```

`ViewSession` is the adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example) with one addition: it runs
`onDispose` in `DisposeAsync`, so a closed session stops listening. Writing a `UiState` from the
`Changed` handler is safe on any thread, and only the text that reads it is patched.

### Limits

- **At most 64 devices per provider** at a time (`BatteryLimits.MaxDevicesPerProvider`). A publish that
  would exceed it is refused as a whole; publishing 64 devices in one list is one call.
- **Ids and names** are at most 128 characters, a kind at most 32. Empty or whitespace is refused.
- **A list is all or nothing**, in the SDK and on the host: one invalid device refuses the whole call
  and nothing is applied.
- **Calls count toward your plugin's callback throttle.** The SDK retries a call refused with
  `RATE_LIMITED` once, after a second; a burst beyond that fails. Publish changes, not a timer's every tick.

### In a plugin

`MacroDeck.Plugin.Hosting` declares the `battery-provider` capability for you when an integration
implements `IBatteryProvider`, starts the provider once the plugin is connected and its integration has
initialized, and stops it on shutdown. No permission is needed, to publish or to read.

- **Reconnects are handled.** The SDK remembers the set you published. When the connection drops and the
  session resumes, it resends the whole set in one call, so you publish nothing again. When a new session
  starts instead, Macro Deck initializes your provider again and you publish from scratch.
- **Your devices go with your session.** When your plugin stops or its session ends, Macro Deck withdraws
  the devices that session published. Uninstalling the plugin does the same.
- **A configuration change withdraws too.** Before the SDK initializes your provider again within the
  same session, it asks Macro Deck to withdraw what you published.
- **While the user has turned your plugin off**, what you publish is kept but not shown, and appears again
  when it is turned back on, without a new publish.

### Built-in integrations

A built-in integration implements the same `IBatteryProvider` and reads the same
`IIntegrationContext.Batteries`; nothing crosses a wire. Turning such an integration off stops its
provider and withdraws its devices; turning it on again initializes the provider, which publishes them
again.

#### The ADB provider

Macro Deck's own ADB integration is the reference provider. It reports every Android phone and tablet
that has authorized the computer, while ADB is enabled and the ADB integration is turned on. It uses only
the public SDK: the devices, their connection events and their battery readings come from
`IIntegrationContext.AndroidDevices`, the same `IAndroidDeviceManager` a plugin uses (see
[Android devices](https://docs.macro-deck.app/features/android-devices/)), so it would keep working if it were moved into a plugin.
See
[`AdbBatteryProvider.cs`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/host/src/MacroDeckHost.Integrations/Adb/AdbBatteryProvider.cs).
It shows the rules on this page in practice:

- **A stable id that reveals nothing.** The id is the device's `StableId`, a keyed hash of its hardware
  serial with a key that belongs to this install of Macro Deck, so the same phone keeps its id over USB and
  Wi-Fi and across restarts, while the serial itself is never published or stored. A widget imported from
  another install therefore shows the device's stored name as not available.
- **Out of reach is not removed.** A phone that disconnects stays published with `IsConnected = false`;
  it is connected again as soon as one of its USB or wireless connections returns. The provider never
  calls `RemoveAsync` on a disconnect.
- **Push on change, poll slowly.** It publishes when a device connects or is authorized and refreshes the
  levels every 15 seconds, publishing only devices that changed.

### Older versions of Macro Deck

- **A plugin on an older host.** A Macro Deck that predates battery providers answers a publish with
  `CAPABILITY_UNSUPPORTED`. The SDK logs this once and turns every later publish into a no-op, so your
  provider keeps running without errors. `IIntegrationContext.Batteries` stays empty and never raises
  `Changed`. Set a minimum host version in [`compatibility.macroDeck`](https://docs.macro-deck.app/reference/manifest/#compatibility)
  if batteries are the point of your plugin.
- **An older plugin on a newer host.** A plugin built before battery providers declares no
  `battery-provider` capability and ignores the `batteries` state the host sends to every plugin.
- **An `IIntegrationContext` of your own**, such as a test double, keeps compiling: `Batteries` is a default
  interface member that returns `UnsupportedBatteryApi.Instance`.

### Security

**Every plugin can read every battery device**, including the ones of other plugins and Android phones
reported over ADB, whether or not plugins may use ADB. That is deliberate: a battery level, a name and a
kind are what a deck shows anyway, and gating them would leave widgets of other plugins blank. So publish
nothing in a name or id that you would not show every plugin: no serial numbers, no account names you
would not put on a deck. See [the security model](https://docs.macro-deck.app/policies/security/#battery-devices).

### Testing

`MacroDeck.Plugin.Testing` has a fake for each side:

```csharp
using MacroDeck.Plugin.Testing.Fakes;
using MacroDeck.Sdk.Batteries;

var batteries = new FakeBatteryProviderContext();
await new HeadsetIntegration(new FakeHeadsetWatcher("pad-1", level: 80)).InitializeAsync(batteries);

Assert.That(batteries.Devices["pad-1"].LevelPercent, Is.EqualTo(80));
Assert.That(batteries.Publishes, Has.Count.EqualTo(1));
```

- **`FakeBatteryProviderContext`** keeps the host's rules: publishing a known id replaces the device, a
  list is all or nothing, and more than 64 devices is refused. Assert on `Devices`, `Publishes` and
  `RemovedIds`.
- **`FakeBatteryApi`** is the reader's side. `Set(devices, removedIds)` replaces the catalog and raises
  `Changed`; `SubscriberCount` tells you whether your code still listens.
- **In a `PluginTestHarness`**, `harness.Context.Batteries` is the `FakeBatteryApi` behind
  `IIntegrationContext.Batteries`, and `harness.Context.BatteryProvider` the `FakeBatteryProviderContext`
  your provider publishes into. `InitializeIntegrationsAsync` starts battery providers against it.

See [Testing](https://docs.macro-deck.app/features/testing/#testing-batteries).

### Over the plugin protocol

| Direction | What | Operations |
| --- | --- | --- |
| Plugin to host | `batteries` host API | `publish` (add or replace up to 64 devices), `remove` (remove ids for good), `sync` (replace the plugin's whole set, used after a resumed reconnect), `withdraw` (withdraw the session's devices, used before a provider is initialized again) |
| Host to plugin | `battery-provider` capability kind, version 1 | `describe` (the provider name) |
| Host to every plugin | `host.state` for `batteries` | The whole catalog with a revision and the ids removed since the previous one |

A call without the declared `battery-provider` capability is `CAPABILITY_UNAVAILABLE`; an invalid device or
a set above the limit is `INVALID_PAYLOAD` and nothing is applied. See
[`batteries` in the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#batteries).

### See also

- [Android devices](https://docs.macro-deck.app/features/android-devices/) - Macro Deck's ADB connection for your own operations.
- [Variables](https://docs.macro-deck.app/features/variables/) - how integration variables work.
- [Widget types](https://docs.macro-deck.app/ui/views/widget-types/) - offering a widget of your own.
- [Testing](https://docs.macro-deck.app/features/testing/) - the fakes and the test harness.

## Button icons

> Source: https://docs.macro-deck.app/features/button-icons/
>
> Let an action own an action button's rendered icon with IIconProviderActionDefinition - album art, avatars, weather imagery - by version, reference or bytes.

An icon-provider action supplies the image an action button currently shows, such as album artwork, an
avatar or a weather symbol. It overrides the button's configured icon while it answers, and hands it
back when it doesn't.

### Quick start

```csharp
using MacroDeck.Sdk.Actions;

internal sealed class NowPlayingAction(PlayerClient player) : IActionDefinition, IIconProviderActionDefinition
{
	public string Id => "now-playing";

	public Task<ActionIconSnapshot?> GetActionIconAsync(
		IReadOnlyDictionary<string, object?> parameters,
		CancellationToken cancellationToken)
	{
		var artwork = player.CurrentArtwork; // already held - never fetch here
		ActionIconSnapshot? snapshot = !player.IsConnected ? null
			: artwork is null ? new ActionIconSnapshot { NoIcon = true }
			: new ActionIconSnapshot { Version = artwork.TrackId, MediaType = artwork.MediaType };

		return Task.FromResult(snapshot);
	}

	public Task<ActionIconContent?> GetActionIconContentAsync(
		IReadOnlyDictionary<string, object?> parameters,
		string version,
		CancellationToken cancellationToken)
	{
		var artwork = player.CurrentArtwork;
		return Task.FromResult(artwork?.TrackId == version
			? new ActionIconContent(artwork.Bytes, artwork.MediaType)
			: null);
	}

	// Name, Description, Parameters and CreateExecutor omitted - see Actions.
}
```

A button running **Now playing** shows the current track's cover. Bytes are fetched once per track, and
the button's own icon comes back when the player is disconnected.

Things to know:

- **Three answers.** `null` means "I can't answer", and the button's configured icon is shown. `NoIcon`
  means "deliberately blank". A `Version` means "this image".
- **Bytes follow `Version`.** The host calls `GetActionIconContentAsync` only when `Version` changes, which
  keeps polling cheap.
- **Render-time only.** The button's configured icon is never rewritten, and it reappears the moment the
  provider is removed or disabled.
- **Independent of states.** It is free-standing (it does not extend `IActionDefinition`) and separate
  from [`IStateProviderActionDefinition`](https://docs.macro-deck.app/features/button-states/). Enabling one never enables the
  other.

### Choosing an answer

```csharp
// Can't answer right now - the widget shows its configured icon.
return Task.FromResult<ActionIconSnapshot?>(null);

// Working, and deliberately showing nothing.
return Task.FromResult<ActionIconSnapshot?>(new ActionIconSnapshot { NoIcon = true });

// An icon the host already has - no bytes needed.
return Task.FromResult<ActionIconSnapshot?>(new ActionIconSnapshot
{
	Version = condition,
	Reference = ActionIconReference.IconPack(WeatherIcons.For(condition))
});

// Your own bytes - fetched through GetActionIconContentAsync when Version changes.
return Task.FromResult<ActionIconSnapshot?>(new ActionIconSnapshot { Version = avatarHash, MediaType = "image/png" });
```

| `ActionIconSnapshot` | |
| --- | --- |
| `Version` | Stable identity of the image. The host refetches bytes only when it changes. Empty with `NoIcon`. |
| `Reference` | A host-resolvable icon: `ActionIconReference.IconPack(id)` or `ActionIconReference.PluginIcon(key, name)`. Opaque, and **never a URL** - the host never fetches one on a provider's say-so. |
| `MediaType` | Media type of the bytes, when there is no `Reference`. |
| `NoIcon` | Render nothing. |

`GetActionIconContentAsync` returns the bytes for the `version` asked for. Return `null` when that version
has already moved on, and the host keeps the image it already holds rather than blanking the button. It
is never called for a snapshot with a `Reference` or `NoIcon`. The default implementation returns `null`,
so a reference-only provider does not override it.

### Your own bundled icons

A plugin that [bundles icon packs](https://docs.macro-deck.app/reference/manifest/) can point at one of its own icons by the pack's
key and the icon's name, with no bytes and no pack id:

```csharp
return Task.FromResult<ActionIconSnapshot?>(new ActionIconSnapshot
{
	Version = "spotify",
	Reference = ActionIconReference.PluginIcon("logos", "spotify")
});
```

- **Your packs only.** The host resolves the reference against the calling plugin's own bundled packs, so
  the same key and name from another plugin never reaches yours, and yours never reaches theirs.
- **Unknown means no icon.** A key or name your packs do not hold renders no icon, the same as an unknown
  icon-pack id. `PluginIcon` itself throws `ArgumentException` for a key that is not a valid pack key
  (lowercase letters, digits and inner hyphens) and for a blank name or one containing `/`.
- **Older hosts.** A host that predates bundled icon packs does not know the `plugin-icon` reference type
  and renders no icon.
- **Updates keep it.** Replacing a pack in an update keeps its icons by name, so the reference goes on
  resolving to the new artwork.

### Reading the icon

The rules match [reading state](https://docs.macro-deck.app/features/button-states/#reading-state):

- **Answer for the configured instance**, from `parameters`. The same action on several buttons answers
  for each separately. The user adopts at most one instance as a button's icon provider, from the
  control the button editor shows on each such action or from the offer when one is added, and the host
  resolves it once per button - you own the icon currently rendered, not one icon per
  state.
- **Tolerate a half-filled draft.** It is called once per settled editor draft while the user configures
  the action, so a missing value must not throw.
- **Side-effect free.** Answer from state you already hold, honour the token, never connect or
  authenticate, and never route through `IActionExecutor`.

`IconPollInterval` (default five seconds) is a request, clamped like `StatePollInterval`, and the host
reads less often while nothing displays the button.

### Pushing a change

```csharp
public async Task InitializeAsync(IIntegrationContext context)
{
	_player.TrackChanged += async (_, _) => await context.Widgets.InvalidateIconAsync("now-playing");
	// ...
}
```

`InvalidateIconAsync` makes every button following that action re-read its icon now, instead of at the
next poll. Pass the action's **declared local id**, not a configured instance: the host qualifies it with
your integration, so you can only invalidate your own actions. It is a hint - the host still compares
`Version` before refetching. It does not replace polling, and against a host that predates it the call
does nothing.

### When the provider can't answer

A `null` snapshot, a timeout, an exception, or a missing or disabled block or integration all fall back to
the button's own configured icon. This is the opposite of a state provider, which holds its last state. An
icon has a meaningful default to return to, so a button never shows a stale image.

The **Set Icon** action fails on a button with an assigned icon provider, the same way it fails on a
state-controlled one. This holds even when the provider can't answer right now. In a patch that changes
several properties, only the icon is dropped and the rest still applies.

### Colouring the icon

An action button can draw its icon in one colour: every pixel takes the colour and keeps its own
transparency, so a white icon on a transparent background turns into an icon of that colour. The user sets
it in the button editor, and a flow sets it with the **Set Icon Color** action.

```csharp
await context.Widgets.ApplyAsync(new WidgetAppearanceRequest
{
	WidgetId = widgetId,
	Patch = new WidgetAppearancePatch { IconColor = "#ef4444" },
});
```

`IconColor` takes `#rrggbb`. To return the icon to its own colours, send
`ClearProperties = [WidgetAppearanceProperty.IconColor]` or an empty string. In state mode the colour
belongs to the targeted state, like the icon itself.

- Artwork from an icon provider is never tinted. On a button with a provider the call still succeeds and
  stores the colour, but nothing visible changes until the button falls back to its own icon.
- A host that predates `IconColor` ignores the field, so a patch that changes only the icon colour makes
  `ApplyAsync` return `false` there. `WidgetTargetInfo.AppearanceProperties` lists `IconColor` for a
  button on a host that supports it.

### Choosing the icon's appearance

An icon can have [appearances](https://docs.macro-deck.app/guide/concepts/#icon-appearances), such as a dark or a static version, and
Macro Deck normally picks the one that fits the screen. A button or slider can be pinned to one of them
instead. The user picks it under **Icon appearance** in the editor, and a flow sets it with the **Set Icon
Appearance** action.

```csharp
await context.Widgets.ApplyAsync(new WidgetAppearanceRequest
{
	WidgetId = widgetId,
	Patch = new WidgetAppearancePatch { IconAppearance = "colorScheme=dark;motion=static" },
});
```

`IconAppearance` takes an appearance key, its traits joined by `;`, or `default` for the icon's own image.
A custom appearance a user named, such as Outlined, has the key `variant=outlined`.
To return to automatic selection, send `ClearProperties = [WidgetAppearanceProperty.IconAppearance]` or an
empty string. In state mode the pin belongs to the icon of the targeted state, like the icon itself.

- The pin belongs to the icon, so it needs one: on a widget without an icon the call changes nothing, and
  **Set Icon** with a different icon drops the pin.
- A key that is not a valid appearance key is rejected and `ApplyAsync` returns `false`. A valid key the
  icon has no appearance for is kept, and the icon is shown as if it were not pinned.
- Like **Set Icon**, the call changes nothing on a button with an assigned icon provider, and the action
  fails there.
- A host that predates `IconAppearance` ignores the field, so a patch that changes only the appearance makes
  `ApplyAsync` return `false` there. `WidgetTargetInfo.AppearanceProperties` lists `IconAppearance` for a
  button or slider on a host that supports it.

### Over the plugin protocol

| Operation | SDK member |
| --- | --- |
| `icon` | `GetActionIconAsync` |
| `icon.content` | `GetActionIconContentAsync` |

Test both with `PluginTestHarness.Actions.GetActionIconAsync(localId, parameters)` and
`GetActionIconContentAsync(localId, version, parameters)`.

### See also

- [Actions](https://docs.macro-deck.app/features/actions/) and [Button states](https://docs.macro-deck.app/features/button-states/)
- [Capability parity: the icon-poll window](https://docs.macro-deck.app/reference/capability-parity/#the-icon-poll-window)
- [Devices: fetching a provider-controlled icon](https://docs.macro-deck.app/features/devices/#fetching-a-provider-controlled-icon)

## Button states

> Source: https://docs.macro-deck.app/features/button-states/
>
> Drive an action button's N-state appearance with IStateProviderActionDefinition - declaring states, reporting the active one, default appearances and expected states.

A state-provider action tells a button which states it can be in and which one is current - muted or
unmuted, playing or paused. The button follows along and shows the appearance the user gave each state.

### Quick start

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

internal sealed class MicMuteAction(VoiceClient client) : IActionDefinition, IStateProviderActionDefinition
{
	private static readonly IReadOnlyList<ActionStateDefinition> _states =
	[
		new("unmuted", MacroDeckStrings.States.Unmuted())
		{
			DefaultAppearance = new ActionStateAppearance { BackgroundColor = "#2f855a" }
		},
		new("muted", MacroDeckStrings.States.Muted())
		{
			DefaultAppearance = new ActionStateAppearance { BackgroundColor = "#c53030" }
		},
		new("unavailable", MacroDeckStrings.States.Unavailable())
		{
			DefaultAppearance = new ActionStateAppearance { BackgroundColor = "#4a5568", LabelColor = "#cbd5e0" }
		}
	];

	public string Id => "toggle-mute";

	public Task<ActionStateSnapshot?> GetActionStateAsync(
		IReadOnlyDictionary<string, object?> parameters,
		CancellationToken cancellationToken)
	{
		// Answer from state the client already holds - never connect here.
		var active = client.IsConnected ? client.IsMuted ? "muted" : "unmuted" : "unavailable";
		return Task.FromResult<ActionStateSnapshot?>(new ActionStateSnapshot(_states, active));
	}

	// Name, Description, Parameters and CreateExecutor omitted - see Actions.
}
```

A button running **Toggle mute** can adopt it as its state provider. It starts out green or red with the
labels "Unmuted"/"Muted", and switches whenever the mic does.

The user adopts it in the button editor. The action picker marks actions that provide states, and each
such action in the button's flows has a control to use it as the provider. Adding one to a button also
offers it right away, turning Multi state on if the button had a single state. The provider's states then
replace the button's own: the user still picks each one and styles it (label, colours, font, icon), but
cannot add, rename or delete states, and no state mapping applies. Stopping, or removing the action from
the flows, brings back the states the button had before; Multi state stays on. Changing the action's settings asks it for its
states again, so a different device can bring a different set.

Things to know:

- **Answer for the configured instance.** `parameters` is the instance's configuration. The same
  action can sit on several buttons with different parameters, and each answers for itself.
- **The user picks the provider.** At most one instance drives a button, and only the one the user
  adopted. The action never claims a button for itself.
- **It is free-standing.** `IStateProviderActionDefinition` does not extend `IActionDefinition`. Implement
  both on the same class.
- **Read-only and cheap.** Called while the user is still editing and polled while the button is on
  screen, so see [the rules below](#reading-state).

### Declaring states

```csharp
new ActionStateDefinition("recording", MacroDeckStrings.States.Recording())
{
	DefaultAppearance = new ActionStateAppearance
	{
		Label = "",                   // icon-only
		BackgroundColor = "#c53030",
		LabelColor = "#ffffff"
	}
}
```

A state `Id` is persisted in the user's profile once a button adopts it. Keep it stable lowercase
kebab-case and never rename it.

| `ActionStateAppearance` | Effect | `null` means |
| --- | --- | --- |
| `Label` | Button text in this state. `""` shows no text. | The state's own `Label`. |
| `BackgroundColor` | `#rrggbb`. | The button's default. |
| `LabelColor` | `#rrggbb`. | The button's default. |
| `IconId` | Icon in the host's icon id format. | No icon. |

The appearance is applied **only to a state a button adopts for the first time**. Re-reading the provider
never restyles a state the user has already configured. Set `IconId` only to an id the host can resolve:
an unknown id is stored as given and renders as no icon, which the user then has to clear by hand.

For labels, reuse the `MacroDeckStrings.States` family (`On`, `Off`, `Muted`, `Unmuted`, `Visible`,
`Hidden`, `Recording`, `Streaming`, `Playing`, `Paused`, `Unavailable` and more) instead of shipping your
own copies - see [Reuse `MacroDeckStrings`](https://docs.macro-deck.app/features/localization/#reuse-macrodeckstrings-instead-of-duplicating-common-strings).

### Reading state

```csharp
public Task<ActionStateSnapshot?> GetActionStateAsync(
	IReadOnlyDictionary<string, object?> parameters, CancellationToken cancellationToken)
{
	// Half-typed drafts arrive here too: a missing value is not an error.
	if (parameters.GetValueOrDefault("scene") is not string scene || scene.Length == 0)
	{
		return Task.FromResult<ActionStateSnapshot?>(null);
	}

	var active = _obs.CurrentScene == scene ? "active" : "inactive";
	return Task.FromResult<ActionStateSnapshot?>(new ActionStateSnapshot(_states, active));
}

public TimeSpan StatePollInterval => TimeSpan.FromSeconds(1);
```

`GetActionStateAsync` runs on two cadences. It runs once per settled editor draft while the user
configures the action, with a partial parameter set, so it must not throw. It also runs every
`StatePollInterval` while a button follows the instance.

- **Side-effect free.** Answer from state you already hold, honour the token, and never connect or
  authenticate to produce an answer.
- **`null` means "nothing to report"** - unconfigured, disconnected, gone. `ActiveStateId = null` means
  the set is known but no state is active. A returned snapshot's `States` is never empty.
- **The set may change.** Returning a different set is how live conditions are reported. The host
  re-adopts by id and keeps the appearance of every id that survived.
- **Prefer an `unavailable` state to `null` on a transient failure.** The host turns an exception into a
  `null` snapshot, but a player that is momentarily unreachable still has a known state set. Mapping the
  failure to your own `unavailable` state tells the user more.

`StatePollInterval` (default two seconds) is a request. The host clamps it and reads less often, or not
at all, while nothing displays the button. A button that starts being displayed goes back to the requested
cadence within about a second. See
[the state-poll window](https://docs.macro-deck.app/reference/capability-parity/#the-state-poll-window).

### Bridging the poll delay

```csharp
public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
{
	var wasMuted = _client.IsMuted;
	await _client.SetMutedAsync(!wasMuted, context.CancellationToken);
	return ActionResult.Success(wasMuted ? "unmuted" : "muted");
}
```

A button follows its provider within about one poll interval, not instantly. When the user presses the
button and its own provider action succeeds, the host calls `GetActionStateAsync` again right away
instead of waiting for the next poll. If your target applies the change asynchronously and that read
still sees the old state, the regular poll picks the change up afterwards.

To show the new state even before that read, the executor can return `Success(expectedStateId)` or
`Accepted(message, expectedStateId)` to name the state it expects next. The host may show that state
briefly while it waits for a read to confirm it. The id must be one `GetActionStateAsync` advertises.
Failed results get neither, and a flow the host runs on its own (an `onStateChange` flow, a timer, an
event trigger) keeps normal polling.

### Over the plugin protocol

| Operation | SDK member |
| --- | --- |
| `state` | `GetActionStateAsync` with the instance's parameters |
| `execute` | carries `ExpectedStateId` in the execute result |

A plugin cannot push a state change for one instance, because a configured instance has no wire identity.
A `state.update` for the actions kind only brings the next read forward. Test it with
`PluginTestHarness.Actions.GetActionStateAsync(localId, parameters)`.

### See also

- [Actions](https://docs.macro-deck.app/features/actions/)
- [Button icons](https://docs.macro-deck.app/features/button-icons/) - a separate capability; enabling one never enables the other
- [Capability parity](https://docs.macro-deck.app/reference/capability-parity/#the-state-poll-window)
- [Localization](https://docs.macro-deck.app/features/localization/)

## Calendars

> Source: https://docs.macro-deck.app/features/calendars/
>
> Expose calendar accounts and events with ICalendarProvider - accounts from setup flows, overlap and recurrence rules, all-day events, event details, and what Macro Deck builds on top.

An integration exposes calendars by implementing `ICalendarProvider`. It lists the accounts it can read,
and for each account returns its calendars, the events in a time range and the full details of one event.
Macro Deck merges the accounts of every provider, so the user's widgets, triggers and the **Join Meeting**
action work with your service next to the built-in Google Calendar and Outlook Calendar providers without any
further code.

Connecting an account is not part of this contract. Signing in, storing tokens and asking the user to
sign in again belong to your [setup flow](https://docs.macro-deck.app/features/setup-flows/) and your
[integration issues](https://docs.macro-deck.app/features/integration-issues/). `ICalendarProvider` only reads.

### Quick start

```csharp
using MacroDeck.Plugin.Hosting.Integrations.HostApis; // IPluginCatalogNotifier
using MacroDeck.Plugin.Protocol.Handshake;             // CapabilityKinds
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Calendar;

public sealed class TeamCalendarIntegration(IPluginCatalogNotifier catalog)
	: IPluginIntegration, ICalendarProvider
{
	private Dictionary<string, TeamCalendarClient> _clients = [];
	private IReadOnlyList<CalendarAccount> _accounts = [];

	public IReadOnlyList<IActionDefinition> Actions { get; } = [];

	public async Task InitializeAsync(IIntegrationContext context)
	{
		var clients = new Dictionary<string, TeamCalendarClient>();
		var accounts = new List<CalendarAccount>();

		// One account per config entry your setup flow created.
		foreach (var entry in await context.Config.GetEntriesAsync())
		{
			var id = entry.Id.ToString("N");
			var token = await context.Config.GetSecretAsync(entry.Id, "token");
			clients[id] = new TeamCalendarClient(token);
			accounts.Add(new CalendarAccount { Id = id, DisplayName = entry.Title });
		}

		_clients = clients;
		_accounts = accounts;
		catalog.CatalogChanged(CapabilityKinds.Calendar);
	}

	public Task ShutdownAsync() => Task.CompletedTask;

	public IReadOnlyList<CalendarAccount> GetAccounts() => _accounts;

	public Task<IReadOnlyList<CalendarInfo>> GetCalendarsAsync(string accountId, CancellationToken ct)
		=> Client(accountId).GetCalendarsAsync(ct);

	public Task<IReadOnlyList<CalendarEvent>> GetEventsAsync(
		string accountId, CalendarEventQuery query, CancellationToken ct)
		=> Client(accountId).GetEventsAsync(query.From, query.To, query.CalendarIds, ct);

	public Task<CalendarEvent?> GetEventAsync(
		string accountId, string calendarId, string eventId, CancellationToken ct)
		=> Client(accountId).GetEventAsync(calendarId, eventId, ct);

	// An account this provider no longer knows is a failure, not an empty calendar.
	private TeamCalendarClient Client(string accountId)
		=> _clients.TryGetValue(accountId, out var client)
			? client
			: throw new InvalidOperationException($"Unknown calendar account '{accountId}'.");
}
```

Register it like any integration, with `RegisterIntegration<TeamCalendarIntegration>()` in `Program.cs`.
The SDK sees `ICalendarProvider` and declares the `calendar` capability for you. Add an
`IConfigFlowProvider` with `AllowsMultipleConfigurations` so the user can connect one account per entry.

Things to know:

- **Account ids are local and permanent.** Return the id you chose, not a qualified one. The host
  stores the user's calendar choice as `integrationId::accountId` plus the calendar id, so an id that
  changes on restart silently empties every widget and trigger filter that used it. A config entry id is
  a good choice.
- **`GetAccounts` is synchronous and called often.** Return a cached list, as above.
- **Tell the host when the accounts change.** After adding, removing or renaming an account, call
  `CatalogChanged(CapabilityKinds.Calendar)` on the injected `IPluginCatalogNotifier`. The host then reads
  the accounts again and fetches the events of every account anew. Saving or removing a config entry
  reinitializes your integration, so calling it at the end of `InitializeAsync` covers the usual case.
- **You only read.** The host decides when to read, caches the events and drives every widget, trigger
  and action from that cache.

### The contract

`ICalendarProvider` and its records carry the full rules in their XML docs. The ones that decide whether
your provider behaves correctly:

| Member | Rules |
| --- | --- |
| `GetAccounts()` | Each `Id` is a valid resource local id (non-empty, at most 256 characters, no whitespace and no `::`), unique within the provider and stable across restarts. An account that breaks this is skipped and logged. |
| `GetCalendarsAsync` | The account's calendars. `Id` is opaque to the host but must be unique within the account and stable. `Color` is `#RRGGBB` or `null`; any other format is ignored. |
| `GetEventsAsync` | The events **overlapping** `From` up to, not including, `To`: an event counts when it starts before `To` and ends after `From`. An empty `CalendarIds` means every calendar of the account. |
| `GetEventAsync` | One event with every detail, by the ids `GetEventsAsync` returned. `null` only when the event no longer exists. |

#### Throw, don't return empty

Every read **throws when it fails** and returns an empty list only when there genuinely is nothing. The
host shows the two differently: an empty result is "no events", a failure keeps the account's last
known events on screen and tells the user that some calendars could not be updated. An account id you no
longer know is a failure too. Honour the cancellation token and let `OperationCanceledException`
propagate.

#### Recurring events

Expand recurring events. Return one `CalendarEvent` per occurrence in the range, each with an `Id` of
its own that stays the same across reads and that `GetEventAsync` accepts:

```csharp
new CalendarEvent
{
	Id = $"{series.Id}_{occurrence.Start.UtcDateTime:yyyyMMdd'T'HHmmss'Z'}", // one id per occurrence
	CalendarId = calendarId,
	Title = series.Summary,
	Start = occurrence.Start,
	End = occurrence.End
};
```

The host tells occurrences apart by `CalendarId` and `Id`. Two occurrences with the same id collapse into
one, and a trigger fires once for it.

#### All-day events

Set `IsAllDay` and only the dates of `Start` and `End` count, each in its own offset. The event covers
`Start.Date` up to, but not including, `End.Date`, and Macro Deck places those days in the local time zone
of the computer it runs on. A one-day event on 5 October:

```csharp
new CalendarEvent
{
	Id = "offsite",
	CalendarId = "team",
	Title = "Company offsite",
	Start = new DateTimeOffset(2026, 10, 5, 0, 0, 0, TimeSpan.Zero),
	End = new DateTimeOffset(2026, 10, 6, 0, 0, 0, TimeSpan.Zero),
	IsAllDay = true
};
```

Include an all-day event in `GetEventsAsync` when its days overlap the days `From` and `To` fall on. The
host filters the result again, so an extra event is harmless while a missing one is not.

#### Details

`GetEventsAsync` may return everything, but the host may drop `Description` and `Participants` from that
list and read them through `GetEventAsync` when the user opens one event. Over the plugin protocol it
always does, see [below](#over-the-plugin-protocol). So make `GetEventAsync` return the full event:

| Property | Meaning |
| --- | --- |
| `Title` | Shown everywhere. An empty title shows as "(No title)" in the user's language. |
| `Location` | Free text. Optional. |
| `Description` | Plain text or HTML. The host removes the markup before showing it, so do not rely on markup for meaning. |
| `MeetingUrl` | The link to the online meeting. Only an absolute `http` or `https` URL is used, anything else is ignored. |
| `Participants` | `CalendarParticipant` with `Name`, `Email`, `IsOrganizer` and `Response` (`Unknown`, `NeedsAction`, `Accepted`, `Declined`, `Tentative`). Set at least one of `Name` and `Email`. |

### What Macro Deck builds on it

Implementing `ICalendarProvider` is all it takes for your accounts to appear in everything Macro Deck
offers for calendars. You declare none of it:

- The **Calendar** widget, in its **Agenda** and **Next event** layouts, whose settings list your
  calendars by name, with the account and provider beside them. Pressing it in the Next event layout, or an
  event in the list an Agenda opens, shows a details dialog, filled from `GetEventAsync`, with a **Join meeting** button for its `MeetingUrl`.
- The automation of that widget: press actions, the widget's own **Event Starts Soon**, **Event
  Started** and **Event Ended** triggers for the calendars a widget shows, the **Show Calendar Details**
  action, and widget variables such as `calendar_next_title` and `calendar_next_countdown` for the event
  a widget shows. They work the same for your calendars as for the built-in ones.
- The triggers **Event Starts Soon**, **Event Started** and **Event Ended**, filterable by account and
  calendar, whose event values include the title, times, calendar, account, provider name, location and
  meeting link.
- The **Join Meeting** action, which opens the meeting link of the event that is running or about to start
  on the computer running Macro Deck.
- The **Refresh Calendars** action, which reads every provider's accounts right away instead of waiting
  for the next update.

The [user guide](https://docs.macro-deck.app/guide/concepts/#calendar-widget) describes them from the user's side. Do not
build your own versions of these. If your service offers more, such as accepting an invitation, add
[actions](https://docs.macro-deck.app/features/actions/) of your own.

`ProviderName` is optional. Leave it out and the integration's name (the manifest name for a plugin) is
shown next to the account. Set it when one integration exposes a distinctly branded service.

### Edge cases

- **An account disappears.** Drop it from `GetAccounts` and call `CatalogChanged`. Its events leave the
  widgets with the next refresh; widget and trigger filters naming it simply match nothing.
- **Invalid or duplicate account ids** are skipped and logged. Calendars and events with an empty id are
  ignored, and a repeated id counts once.
- **A read fails.** The account keeps its last events and the widgets say that some calendars could not
  be updated, until a later read succeeds.
- **The same event in two accounts**, such as an invitation seen by two connected accounts, shows once per
  account: the host has no way to know they are one event.
- **A timed event that ends before it starts** is treated as ending when it starts, and an all-day event
  whose end date is not after its start date as lasting one day.

### Over the plugin protocol

Calendars are fully supported out of process, as capability kind `calendar`, version `1`, declared once
at the local id `provider`. Its operations are `describe`, `accounts`, `calendars`, `events` and `event`;
the [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#calendar) lists their arguments and results.

- **The account list is a snapshot.** The host serves `GetAccounts` from the last `describe` or `accounts`
  reply, which is why `CatalogChanged(CapabilityKinds.Calendar)` matters.
- **Events travel as summaries.** An `events` reply carries no `Description` and no `Participants`; the
  details dialog reads them with `event`.
- **Replies are bounded.** `MacroDeck.Plugin.Hosting` cuts long titles, locations and descriptions,
  drops a meeting URL too long to work, keeps at most 100 participants, and, when an `events` reply would
  still exceed its size limit, drops its latest events and marks the reply as truncated. The host logs a
  warning when that happens. The exact limits are in the
  [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#calendar); the host currently asks for one day at a time,
  which keeps an ordinary calendar far below them.
- **Failures stay failures.** An unreachable plugin, a timeout or an exception in your provider reaches
  the host as a failed read, never as an empty calendar.
- **Older hosts.** A Macro Deck that predates calendars rejects the `calendar` declaration non-fatally:
  the session carries on, and your actions, variables and everything else keep working. Your accounts
  simply do not appear.

See [Capability parity](https://docs.macro-deck.app/reference/capability-parity/).

### Testing

`harness.Calendar`, a `CalendarTestClient`, drives the `calendar` capability the way the host does, with
the protocol's argument records from `MacroDeck.Plugin.Protocol.Capabilities.Calendar`:

```csharp
await using var harness = PluginTestHarness.Create(builder =>
	builder.RegisterIntegration<TeamCalendarIntegration>());
var entry = harness.Context.Config.AddEntry("Work");
harness.Context.Config.SeedSecret(entry, "token", "test-token");
await harness.InitializeIntegrationsAsync();

var outcome = await harness.Calendar.GetEventsAsync(new CalendarEventsArguments
{
	AccountId = entry.ToString("N"),
	From = new DateTimeOffset(2026, 10, 5, 0, 0, 0, TimeSpan.FromHours(2)),
	To = new DateTimeOffset(2026, 10, 6, 0, 0, 0, TimeSpan.FromHours(2))
});

Assert.That(outcome.Succeeded, Is.True, outcome.Error?.Message);
Assert.That(outcome.DataAs<CalendarEventsResult>()!.Events.Select(e => e.Title), Is.EqualTo(["Stand-up"]));
```

Here `TeamCalendarClient` talks to a fake of the team service, the one real external boundary.
`DescribeAsync`, `GetAccountsAsync`, `GetCalendarsAsync` and `GetEventAsync` cover the other operations,
and the session `MacroDeckTestHost` returns has the same `Calendar` client over the real wire. What you
get back is what the host gets: event summaries without details, the size limits applied, and an account
id you do not know as a failed outcome. See [Testing](https://docs.macro-deck.app/features/testing/).

### See also

- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - connecting accounts, including OAuth.
- [Integration issues](https://docs.macro-deck.app/features/integration-issues/) - asking the user to sign in again.
- [Events](https://docs.macro-deck.app/features/events/) - triggers of your own beside the built-in calendar ones.
- [Localization](https://docs.macro-deck.app/features/localization/)
- [Testing](https://docs.macro-deck.app/features/testing/)

## Companion devices

> Source: https://docs.macro-deck.app/features/companion-devices/
>
> Read what the phones and tablets connected through the Companion app report, send them commands and take screenshots with ICompanionDeviceApi - the host:companion-devices permission, the user's control, events, results, limits and testing.

A plugin can read what the phones and tablets connected through the Macro Deck Companion app report about
themselves (battery, orientation, brightness, network, model and more), send them commands such as
**Vibrate** or **Set screen brightness**, and capture a screenshot of their deck or their whole screen.
Macro Deck owns the connections: your plugin never connects, pairs or removes a device, and never talks to
the app directly.

### Quick start

Declare the permission in `manifest.json`:

```json
"permissions": ["host:companion-devices"]
```

Then take `ICompanionDeviceApi` from dependency injection:

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Companion;

public sealed class TabletIntegration(ICompanionDeviceApi companion) : IPluginIntegration
{
	public IReadOnlyList<IActionDefinition> Actions => [new DimTabletAction(companion)];

	// Other IPluginIntegration members omitted.
}

internal sealed class DimTabletAction(ICompanionDeviceApi companion) : IActionDefinition
{
	public string Id => "dim-tablet";

	public LocalizedText Name => Strings.Actions.DimTablet();

	public LocalizedText Description => Strings.Actions.DimTabletDescription();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
		[ActionParameter.Text("device", label: Strings.Parameters.Device(), required: true)];

	public IActionExecutor CreateExecutor() => new Executor(companion);

	private sealed class Executor(ICompanionDeviceApi companion) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (companion.Access != CompanionDeviceAccess.Available)
			{
				return ActionResult.Failed(ActionErrorCodes.PermissionDenied, Strings.Errors.CompanionNotAllowed());
			}

			if (context.Parameters.GetValueOrDefault("device") is not string text ||
				!Guid.TryParse(text, out var deviceId) ||
				companion.FindDevice(deviceId) is not { } device)
			{
				return ActionResult.Failed(ActionErrorCodes.NotConnected, Strings.Errors.TabletNotConnected());
			}

			var command = CompanionDeviceCommand.SetBrightness(10);
			if (!device.State.ConfirmsCommands)
			{
				return await companion.SendAsync(deviceId, command, context.CancellationToken)
					? ActionResult.Success()
					: ActionResult.Failed(ActionErrorCodes.NotConnected, Strings.Errors.TabletNotConnected());
			}

			var result = await companion.RequestAsync(deviceId, command, context.CancellationToken);
			return result.Outcome == CompanionDeviceCommandOutcome.Failed
				? ActionResult.Failed(ActionErrorCodes.ProviderError, Strings.Errors.TabletRefused())
				: ActionResult.Success();
		}
	}
}
```

The user gets a **Dim tablet** action that turns the brightness of the device with that id down to 10 %.

Things to know:

- **Resolve it from DI, or read `context.CompanionDevices`.** Take it in a constructor, like any other
  service; the SDK registers it for every plugin. `IIntegrationContext.CompanionDevices` returns the same
  instance, for code that only has the context.
- **Check `Access` before you rely on it.** Whether your plugin may use Companion devices is the user's
  decision, off until they allow it, and can change while your plugin runs - see [Who decides](#who-decides).
- **Macro Deck owns the devices.** A device appears when the app connects and reports its state, and
  disappears when it disconnects or the user removes it.

### Declaring `host:companion-devices`

An installed plugin reaches Companion devices only when its manifest lists `host:companion-devices` in
[`permissions`](https://docs.macro-deck.app/reference/manifest/#permissions). It is one of the two permissions the host enforces,
next to [`host:adb`](https://docs.macro-deck.app/features/android-devices/#declaring-hostadb); every other entry in the vocabulary is
still declared for disclosure only. If plugins are not allowed to use Companion devices when the user
installs the first version of your plugin that declares it, Macro Deck asks the user whether to allow it.
It does not ask again for an update of a version that already declared it.

A plugin you run yourself during development, through a
[developer token](https://docs.macro-deck.app/reference/authentication/#developer-token-headless-enrolment) or
[interactive pairing](https://docs.macro-deck.app/reference/authentication/#self-registering-interactive-pairing), counts as declaring
it, because you admitted it by hand. Declare it anyway: the packaged plugin needs it. The user's switch
still applies to such a plugin.

### Who decides

`Access` is `Available` only when both of these hold:

| Condition | Where the user controls it | `Access` otherwise |
| --- | --- | --- |
| Plugins may use Companion devices | **Settings > Companion App**, **Plugin access**, **Allow plugins to use Companion devices** (off by default) | `NotAllowed` |
| The plugin declares `host:companion-devices` | The installed version's manifest | `NotAllowed` |

The user sees the permission before and after installing: the install dialog says the plugin uses the
devices connected through Macro Deck Companion, and the plugin's page lists **Uses Companion devices**.
When a plugin that declares `host:companion-devices` is installed while **Allow plugins to use Companion
devices** is off, Macro Deck asks the user in a dialog, **A plugin wants to use your Companion devices**, and
keeps the question in its notifications; **Allow** turns the setting on. It asks the same way, once per run
of Macro Deck, when your plugin calls an operation and is refused; a plugin that does not declare
`host:companion-devices` is refused without asking. That switch covers every plugin that declares the
permission, not only yours. The user guide describes all of this in
[Plugins and your Companion devices](https://docs.macro-deck.app/guide/companion-app/tips/#plugins-and-your-companion-devices).

| `CompanionDeviceAccess` | Meaning |
| --- | --- |
| `Unsupported` | The host has not reported access yet, or predates this API. |
| `Available` | This plugin may use Companion devices now. |
| `NotAllowed` | The user has not allowed plugins to use Companion devices, or the manifest does not declare `host:companion-devices`. |

Tell the user what to turn on rather than a generic failure: only the user can change it.
`AccessChanged` is raised whenever the value changes.

### Devices and events

```csharp
private readonly ConcurrentDictionary<Guid, long> _greeted = new();

companion.DeviceReady += (_, e) =>
{
	if (e.Device is { } device && _greeted.GetValueOrDefault(device.Id) != device.ReadySequence)
	{
		_greeted[device.Id] = device.ReadySequence;
		_ = companion.SendAsync(device.Id, CompanionDeviceCommand.Vibrate);
	}
};
```

- **`Devices` lists the connected devices that have reported their state**, and is empty unless `Access`
  is `Available`. `FindDevice(id)` returns one of them, or `null`.
- **A device is a snapshot.** `CompanionDevice` is a record of `Id`, `ReadySequence` and `State`. A new
  report replaces it, so read `FindDevice` again rather than keeping an old instance.
- **`Id`** is the device's id in Macro Deck, a GUID, the same id its deck client and its configuration
  in the built-in Companion integration use.
- **`ReadySequence`** changes every time the device becomes ready again after it was gone, and only then.
  Two `DeviceReady` events with the same value describe the same connection; remember the last value per
  device, as above, to do something once per connection.
- **`DeviceReady`** is raised when a device reports its first state since it connected, and for every
  device in `Devices` when access becomes `Available`.
- **`DeviceChanged`** is raised after a device reported its state, and with `Device` set to `null` when it
  disconnected or was removed, and for every device when access is withdrawn.
- **`WaitForDeviceAsync(id)`** waits for a device that has just connected to report its state. It answers
  `true` at once for a device in `Devices`, and `false` when the device has no open connection or does not
  report within a few seconds.
- **Handlers run on a background thread**, in the order the changes arrived. One that throws is logged and
  does not affect the others.

#### What a device reports

`State` is a `CompanionDeviceState`. A value Macro Deck could not read, or that the device does not
report, is `null`; percentages are 0 to 100 and texts at most 64 characters.

| Property | Meaning |
| --- | --- |
| `BatteryLevelPercent`, `IsCharging` | The battery. |
| `Orientation` | `portrait` or `landscape` (`CompanionOrientations`). |
| `ScreenBrightnessPercent` | The screen brightness. |
| `Model`, `Platform`, `AppVersion` | The device model, its operating system with version (for example `Android 14`), and the Companion app version. |
| `InFocus` | Whether Macro Deck is in front on the device. |
| `NetworkType` | `wifi`, `cellular`, `ethernet`, `vpn` or `none` (`CompanionNetworkTypes`). |
| `NetworkMetered`, `NetworkValidated` | Whether the network is metered, and whether it reaches the internet. |
| `NetworkName` | The Wi-Fi network's name, only with the `networkName` capability. |
| `CpuUsagePercent`, `MemoryUsedPercent` | Only with the `cpu` and `memory` capabilities. |
| `Capabilities` | What the device can do right now. |
| `RequestableCapabilities` | What it can do after asking its user, see [Capabilities and device prompts](#capabilities-and-device-prompts). |
| `ConfirmsCommands` | Whether the device confirms commands, see [Send or request](#send-or-request). |

### Operations

| `ICompanionDeviceApi` member | What it does |
| --- | --- |
| `SendAsync(id, command)` | Sends a command without waiting for the device to carry it out. `false` when the device is not connected or `Access` is not `Available`. |
| `RequestAsync(id, command)` | Sends a command and waits for the device's answer, a `CompanionDeviceCommandResult`. |
| `CaptureScreenshotAsync(id, mode)` | Captures the deck or the whole screen as a PNG, a `CompanionScreenshotResult`. |
| `WaitForDeviceAsync(id)` | Waits for a device that has just connected to report, see [above](#devices-and-events). |

Commands are created with the static members of `CompanionDeviceCommand`:

| Command | What it does | Needs |
| --- | --- | --- |
| `Vibrate` | Vibrates the device. | - |
| `SetBrightness(percent)` | Sets the screen brightness, 0 to 100; anything else throws `ArgumentOutOfRangeException`. | - |
| `SetOrientation(orientation)` | `automatic`, `portrait` or `landscape`; anything else throws `ArgumentException`. | - |
| `ScreenOn` | Turns the screen on and shows this Macro Deck. | `screenOn` |
| `ScreenOff` | Turns the screen off. | `screenOff` |
| `Focus` | Brings Macro Deck to the front on the device. | `focus` |

What each platform supports is in the user guide's
[What Macro Deck can do with a device](https://docs.macro-deck.app/guide/companion-app/tips/#what-macro-deck-can-do-with-a-device).

#### Send or request

`SendAsync` hands the command to the device and returns; it cannot tell whether the device carried it out.
`RequestAsync` waits for the answer, and is the right call only for a device whose `ConfirmsCommands` is
`true`, or for a capability in `RequestableCapabilities`, where the device asks its user first. A device
that does not confirm leaves every request to wait until it times out.

| `CompanionDeviceCommandOutcome` | Meaning |
| --- | --- |
| `Done` | The device confirmed it carried the command out. |
| `Unconfirmed` | The device accepted the command but did not confirm it in time, so it may or may not have run. |
| `Failed` | The command did not run; `Failure` says why. |

The device has a minute to accept a command and a further few seconds to confirm it once accepted.
Cancelling the token withdraws a command the device has not accepted yet and throws
`OperationCanceledException`; once the device accepted it, the request waits for the answer.

#### Capabilities and device prompts

`Capabilities` and `RequestableCapabilities` hold the names in `CompanionDeviceCapabilities`: `screenOn`,
`screenOff`, `focus`, `screenshotDeck`, `screenshotFull`, `networkName`, `cpu` and `memory`. A later Macro
Deck may report names that are not listed; treat an unknown name as one your plugin does not use.

A capability in `RequestableCapabilities` is one the device can use once its user grants a permission on
the device, such as Android's permission to turn the screen off. A request that needs it shows that prompt
on the device and fails with `ConsentDenied` when the user declines. `RequestableCapabilities` never
contains a name that is already in `Capabilities`.

#### Screenshots

```csharp
var shot = await companion.CaptureScreenshotAsync(deviceId, CompanionScreenshotMode.Deck, cancellationToken);
if (shot.Png is { } png)
{
	await File.WriteAllBytesAsync(path, png, cancellationToken);
}
```

- **`Deck`** captures only the deck, without asking the device's user. It needs `screenshotDeck`, and fails
  with `Unavailable` while the deck is not on screen.
- **`FullScreen`** captures the whole screen. It needs `screenshotFull`, which the device grants only after
  its user agreed on the device, so a capture can show a prompt there and fails with `ConsentDenied` when
  the user declines. Allowing plugins in Macro Deck does not change that.
- **A capture waits like a request**, with up to a minute once the device accepted it.
- **`Png` is set exactly when `Failure` is `null`.** A screenshot larger than 8 MiB fails with `Failed` for
  a plugin; it travels in chunks after the reply.

#### Failures

`RequestAsync` and `CaptureScreenshotAsync` do not throw for a refused or failed call; they answer with a
`CompanionDeviceFailure`. Only cancelling your token throws.

| `CompanionDeviceFailure` | Meaning | What to do |
| --- | --- | --- |
| `NotConnected` | The device is not connected or disconnected before it answered, or the host does not offer Companion devices. | Wait for `DeviceReady`. |
| `Removed` | The user removed the device while the request was running. | Forget the device. |
| `TimedOut` | The device did not answer in time. | Retry, or use `SendAsync` for a device that does not confirm. |
| `ConsentDenied` | The device's user declined the permission the request needs. | Tell the user to allow it on the device. |
| `Unavailable` | The device cannot do this right now, such as a deck screenshot while the deck is not on screen. | Retry later. |
| `Failed` | The device tried and failed, or the host refused the call. | Treat as a failure. |
| `NotAllowed` | This plugin may not use Companion devices. | See [Who decides](#who-decides). |

Later versions may add values; treat an unknown one like `Failed`.

### Limits

- **At most four calls in flight per plugin.** A fifth is refused at once rather than queued, which a
  request or screenshot reports as `Failed` and a send as `false`. Calls also count toward the plugin's
  shared callback throttle. Other host APIs keep flowing while a request waits for a device.
- **A screenshot is at most 8 MiB** for a plugin.
- **The SDK gives up after the host's own windows plus a margin**: about 15 seconds for
  `WaitForDeviceAsync`, 20 for `SendAsync`, and two and a half minutes for `RequestAsync` and
  `CaptureScreenshotAsync`. Pass a `CancellationToken` to give up sooner: cancelling also ends the call on
  the host.

### Integrations built into Macro Deck

Macro Deck's own integrations reach Companion devices through the same `ICompanionDeviceApi`, read from
`IIntegrationContext.CompanionDevices` (see [ADR 0107](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0107-built-in-integrations-are-built-as-extractable-plugins.md)).
For them `Access` is always `Available`: they are part of Macro Deck, so neither **Allow plugins to use
Companion devices** nor `host:companion-devices` applies, and `AccessChanged` is never raised. Should such
an integration ever move out of process, it becomes a plugin like any other and needs the permission and
the user's consent.

The built-in Macro Deck Companion integration uses nothing else. Its actions send the commands and
screenshots above, its variables read each device's `State`, and its **device ready** event is published
from `DeviceReady`, once per `ReadySequence`. See
[`CompanionIntegration.cs`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/host/src/MacroDeckHost.Integrations/Companion/CompanionIntegration.cs).

### A configuration entry per device

An integration whose configuration is per device can ask Macro Deck to keep one configuration entry for
each Companion device by implementing the member-less `ICompanionDeviceConfigEntries` next to its config
flow:

```csharp
public sealed class TabletIntegration : IPluginIntegration, IConfigFlowProvider, ICompanionDeviceConfigEntries
{
	// IPluginIntegration and IConfigFlowProvider members omitted.
}
```

What Macro Deck does with it:

- **Creates the entry when a device connects.** When a device running the Companion app connects and has no
  usable entry yet, Macro Deck stores one with the device id as its id, the device's name as its title and
  empty values. Storing it switches the integration on, as any stored entry does, unless the user switched
  the integration off; a switch-off made while the entry is being created is kept.
- **Deletes it when the device is removed** from Macro Deck, without recording that as a switch-off.
- **One owner.** Only one integration gets these entries: the first integration built into Macro Deck that
  implements the interface, or, when there is none, the first plugin that does, in the order they register.
  Macro Deck keeps that choice in memory for as long as it runs and makes it again on every start. While the
  built-in Companion integration is present a plugin never gets them. When the owner is switched off, no
  entry is created for anyone.
- **Your plugin needs access.** A plugin owner also needs `Access` to be `Available` (see
  [Who decides](#who-decides)); without it no entry is created, and entries follow once the user allows it.
- **Prepared like any entry.** If your plugin also implements `IConfigEntryLifecycle`, Macro Deck asks it to
  prepare the entry first, exactly as for an entry the user completes. A refusal leaves the device without an
  entry, and Macro Deck tries again with the device's next report.

On the wire, implementing the interface declares the `companion-device-entries` capability. It is
declarative: its only operation, `describe`, answers without data. A Macro Deck that predates it rejects the
declaration non-fatally and creates no entries for your plugin.

### Older hosts

On a Macro Deck that predates this API, `Access` stays `Unsupported`, `Devices` stays empty, no event is
raised, `SendAsync` and `WaitForDeviceAsync` answer `false`, and `RequestAsync` and
`CaptureScreenshotAsync` fail with `NotConnected`. Nothing throws. An `IIntegrationContext` you implemented
yourself against an older SDK, such as a test double, keeps compiling: `CompanionDevices` is a default
interface member that returns `UnsupportedCompanionDeviceApi.Instance`, which behaves the same way. A
plugin that uses Companion devices for an optional feature keeps working there with that feature off. Set
a minimum host version in [`compatibility.macroDeck`](https://docs.macro-deck.app/reference/manifest/#compatibility) if Companion
devices are the point of your plugin.

### Testing

`MacroDeck.Plugin.Testing` has an in-memory `FakeCompanionDeviceApi`:

```csharp
var companion = new FakeCompanionDeviceApi();
var tablet = Guid.NewGuid();
companion.Connect(tablet, new CompanionDeviceState { ConfirmsCommands = true, BatteryLevelPercent = 80 });

await new TabletDimmer(companion).DimAsync(tablet);

Assert.That(companion.Calls.Single().Command, Is.EqualTo(CompanionDeviceCommand.SetBrightness(10)));
```

- **Access starts as `Available`** with no devices. `SetAccess` changes it and raises `AccessChanged`;
  while it is `NotAllowed`, requests and screenshots fail with `NotAllowed`, as on a real host.
- **`Connect`** adds or reconnects a device with a new `ReadySequence` and raises `DeviceChanged` and
  `DeviceReady`; **`Report`** replaces what it reports and raises `DeviceChanged`; **`Disconnect`** removes
  it and raises `DeviceChanged` with no device. Events are raised synchronously on the calling thread.
- **`OnRequest` and `OnScreenshot`** decide how requests and screenshots end. A request answers `Done`
  and a screenshot fails with `Unavailable` until you set them.
- **`Calls`** records every send, request and screenshot in order, refused ones included.
- **In a `PluginTestHarness`**, `harness.Context.CompanionDevices` is the plugin's fake, both through DI
  and through `context.CompanionDevices`. Its `Access` starts as `Unsupported`, like a host that has not
  reported yet; call `SetAccess(CompanionDeviceAccess.Available)` and `Connect` to script it.

See [Testing](https://docs.macro-deck.app/features/testing/#testing-companion-devices).

### Security

`host:companion-devices` is user control and consent, not a sandbox. A plugin process runs with the
user's full privileges. What the permission gives the user is a visible, switchable decision, off until
they turn it on, about plugins that read their phones' state, send them commands and capture their
screens through Macro Deck. A plugin that is allowed sees everything listed in
[What a device reports](#what-a-device-reports), including the Wi-Fi network's name, and a deck screenshot
shows whatever the deck shows, other plugins' widgets included. A full screen screenshot still needs the
device's own user to agree on the device. See
[the security model](https://docs.macro-deck.app/policies/security/#companion-devices).

### Over the plugin protocol

| Direction | What | Operations |
| --- | --- | --- |
| Plugin to host | `companion-devices` host API | `wait` (a device that just connected), `send` (fire and forget), `request` (wait for the answer), `screenshot` (the PNG follows over `host.asset.*` with kind `companion-screenshot`) |
| Host to plugin | `host.state` for `companion-devices`, per plugin | `access` (`available` or `not-allowed`), the devices when available, and a revision |
| Plugin to host | `companion-device-entries` capability, declared by `ICompanionDeviceConfigEntries` | `describe`, answered without data |

A call while the plugin's access is not `available` is refused with `COMPANION_DEVICES_NOT_ALLOWED`. See
[`companion-devices` in the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#companion-devices).

### See also

- [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#companion-devices) - the `companion-devices` host API on the wire.
- [Manifest](https://docs.macro-deck.app/reference/manifest/#permissions) - the permission vocabulary.
- [Companion app tips](https://docs.macro-deck.app/guide/companion-app/tips/) - what users do with Companion devices.
- [Android devices](https://docs.macro-deck.app/features/android-devices/) - Macro Deck's ADB connection, the other enforced permission.
- [Batteries](https://docs.macro-deck.app/features/batteries/) - battery levels of every device, readable without a permission.

## Deck and clients

> Source: https://docs.macro-deck.app/features/deck/
>
> Navigate folders and profiles with IDeckNavigator, fill pickers, and find out which folder each connected client has open.

`IIntegrationContext.Deck` is an `IDeckNavigator`. It moves clients between folders and profiles, lists
folders and profiles for pickers, and tells you where each connected client currently is.

### Navigate

```csharp
await context.Deck.ChangeFolderAsync(folderId);                 // every client
await context.Deck.ChangeFolderAsync(folderId, originClientId); // one client
await context.Deck.ChangeProfileAsync(profileId, originClientId);
await context.Deck.GoToParentAsync(originClientId);
await context.Deck.GoBackAsync(originClientId);
```

An action receives the pressing client's id in its execution context. Pass it as `originClientId` to
move only that client. A folder or profile that no longer exists is ignored.

`GetFolders()` and `GetProfiles()` return what a folder or profile picker should offer.

### Where each client is

There is no single "current folder": two devices can show different folders of the same profile.
`GetClients()` lists every connected client with the profile and folder it has open, and `ClientChanged`
fires when a client is first seen or moves.

```csharp
public sealed class ScopedHotkeysIntegration : IPluginIntegration
{
	private IDeckNavigator? _deck;

	public Task InitializeAsync(IIntegrationContext context)
	{
		_deck = context.Deck;
		_deck.ClientChanged += OnClientChanged;
		return Task.CompletedTask;
	}

	private void OnClientChanged(object? sender, DeckClientChangedEventArgs e)
	{
		// e.Client.ClientId moved from e.PreviousFolderId to e.Client.FolderId.
	}

	// A hotkey that should only move the client showing folder B.
	private Task NextFromFolderBAsync(string folderB, string folderC)
	{
		var client = _deck!.GetClients().FirstOrDefault(c => c.FolderId == folderB);
		return client is null ? Task.CompletedTask : _deck.ChangeFolderAsync(folderC, client.ClientId);
	}

	// Other IPluginIntegration members omitted; unsubscribe ClientChanged when the integration shuts down.
}
```

A `DeckClient` carries:

| Member | Meaning |
| --- | --- |
| `ClientId` | The id to pass as `originClientId` to navigate this client. |
| `DeviceId` | The paired device behind the client, or `null` for a client that is not a paired device. |
| `ProfileId`, `FolderId` | What the client has open. |

`DeckClientChangedEventArgs` carries the new `Client` plus `PreviousProfileId` and `PreviousFolderId`, both
`null` when the client was not known yet.

#### Rules

- `ClientChanged` fires for a new client and for a move. A client that re-reports the folder it already
  shows, for example after reconnecting, raises nothing.
- A leaving client raises nothing; it just disappears from `GetClients()`. A web or app client leaves
  once its connection has been gone for the same grace period that ends a Client Disconnected event. A
  device connected through a plugin leaves as soon as it goes offline, and comes back when it returns.
- A paired device is listed once. If it reconnects under a new client id, the new id replaces the old
  one.
- The web client keeps one id per browser origin, so two tabs of the same origin share one entry and the
  last one to move wins.
- Client ids of devices connected through a plugin start with `device:`.
- Handlers run synchronously while Macro Deck processes the move, so keep them short and hand longer work
  to a task.

#### In a plugin

In a plugin, client positions arrive with the deck state the host pushes, not as one message per move.

- Handlers run on the plugin connection's receive loop. Keep them short, and hand longer work to a
  task. An exception thrown by a handler is logged and does not affect the connection.
- Quick moves can be coalesced: A to B to C may arrive as a single change from A to C. An integration
  running inside Macro Deck sees every step.
- When the plugin resumes its session, the first push reports the net change since the last state it saw.
  When it opens a new session, for example after the host restarted, `GetClients()` is empty until the
  first push, and that push reports every client as newly seen, with no previous profile or folder.

### Compatibility

`GetClients()` and `ClientChanged` are default interface members, so a type implementing
`IDeckNavigator` against an older SDK still compiles and loads. Against a host that predates client
positions, `GetClients()` returns an empty list and `ClientChanged` never fires. The wire format is
described in the [protocol reference](https://docs.macro-deck.app/reference/protocol/).

## Device providers

> Source: https://docs.macro-deck.app/features/devices/
>
> Bring hardware or a custom client into Macro Deck with IDeviceProvider - register devices, report presence, render the deck and send presses back.

A device provider brings hardware or a custom client into Macro Deck: a control surface, a macro pad, an
ESP32 panel. You discover devices and register them; Macro Deck owns everything else about them -
persistence, global ids, naming, startup profiles and the device settings the user sees.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Devices;

public sealed class MacroPadIntegration(IPadWatcher watcher) : IPluginIntegration, IDeviceProvider
{
	private readonly IPadWatcher _watcher = watcher;

	public string ProviderName => "Macro Pad";

	public async Task InitializeAsync(IDeviceProviderContext context, CancellationToken cancellationToken = default)
	{
		foreach (var pad in _watcher.ConnectedPads())
		{
			await context.RegisterDeviceAsync(Describe(pad), cancellationToken);
		}

		_watcher.Attached += (_, pad) => _ = context.RegisterDeviceAsync(Describe(pad));
		_watcher.Detached += (_, pad) => _ = context.SetDevicePresenceAsync(pad.SerialNumber, DevicePresence.Offline);
		_watcher.Start();
	}

	public Task ShutdownAsync(CancellationToken cancellationToken = default) => _watcher.StopAsync();

	private static DeviceDescriptor Describe(Pad pad)
		=> new(pad.SerialNumber,
			pad.ProductName,
			Model: pad.ProductName,
			Manufacturer: "Example",
			LayoutReference: "com.example.macropad::pad-3x2",
			Capabilities: new DeviceCapabilities { KeyCount = 6, SupportsImages = true });

	// IPluginIntegration members omitted.
}
```

Every connected pad now shows up in Macro Deck's device settings, where the user can name it and give it
a startup profile. Unplugging it takes it offline; plugging it back in is the same device.

Things to know:

- **`DeviceDescriptor.Id` is the device's identity.** Derive it from something the hardware carries (a
  serial number), never from an enumeration index or a connection handle.
- **Every later call takes that provider-local id** - `SetDevicePresenceAsync`, `UpdateDeviceAsync`,
  `UnregisterDeviceAsync`. The host's global id comes back in `DeviceRegistration.DeviceId`.
- **Order is fixed.** The host calls `IDeviceProvider.InitializeAsync` after the integration's own
  `InitializeAsync` (in a plugin, also after its `ILayoutProvider`), and `IDeviceProvider.ShutdownAsync`
  before the integration stops.
- **Registration only is complete.** Rendering a deck on the hardware is opt-in - see
  [Rendering a session](#receiving-and-rendering-a-session).

### Registering a device

| `IDeviceProviderContext` member | What it does |
| --- | --- |
| `RegisterDeviceAsync` | Offers a device, or re-registers a known provider-local id as the same device. Returns `DeviceRegistration(DeviceId, ProviderDeviceId)`. Throws `ArgumentException` for an empty id or name. |
| `UpdateDeviceAsync` | Refreshes a registered device's metadata. Unknown devices are ignored. |
| `SetDevicePresenceAsync` | Reports whether a device is reachable right now. |
| `UnregisterDeviceAsync` | Withdraws a device from this session. The device is retained. |

| `DeviceDescriptor` parameter | Meaning |
| --- | --- |
| `Id` | Stable provider-local id. Non-empty, unique within your provider. |
| `Name` | Proposed name. A name the user has set wins. |
| `Model`, `Manufacturer` | Shown in device settings. |
| `LayoutReference` | The layout the device uses - see [Capabilities and layouts](#capabilities-and-layouts). |
| `Capabilities` | `DeviceCapabilities`: `KeyCount`, `DialCount`, `DisplayCount`, `SupportsImages`, `SupportsText`, plus an `Extra` map for hardware-specific facts. |
| `Presence` | `Online` (default), `Offline` or `Unknown` at registration. |
| `Metadata` | Provider-defined, opaque to the host. |

The context is safe to keep until `ShutdownAsync` returns. The contract is transport- and vendor-agnostic;
no host-internal service crosses the plugin boundary.

### Presence and reconnects

```text
Provider starts   -> registers SERIAL-1        -> host mints a device, or finds the existing one
Hardware away     -> presence Offline, or unregister
Hardware returns  -> registers SERIAL-1 again  -> same device: same global id, name, startup profile
Host restarts     -> registers SERIAL-1 again  -> still the same device
```

Macro Deck resolves `(your plugin id, Id)` to exactly one device. Re-registering keeps its global id, the
user's name and its startup profile; the descriptor refreshes the rest.

**Nothing you do deletes a device.** Unregistering takes it offline and stops offering it; the device stays
so a reconnect is a reuse, not a new row. The same happens when your integration stops or your plugin's
session drops, so you do not have to unregister everything on the way out. Deleting a device for good is
the user's decision, in device settings.

A provider-registered device never signs in: it holds no credential or session, sign-out is not offered,
and its presence is whatever you last reported.

Implement `GetDevices()` to return what you currently offer; the host reads it to recover its view after a
reconnect without waiting for discovery. The default returns an empty list.

### Capabilities and layouts

```csharp
var layout = await layouts.RegisterLayoutAsync(PadLayout, cancellationToken);   // ILayoutProviderContext
await devices.RegisterDeviceAsync(Describe(pad) with { LayoutReference = layout.LayoutId }, cancellationToken);
```

`LayoutReference` is an **opaque string**: the host stores it and hands it back unparsed. Use the qualified
id (`your.plugin.id::layout-name`) that a [layout provider's](https://docs.macro-deck.app/features/layouts/) `RegisterLayoutAsync`
returns. The layout may belong to another plugin. An unresolvable reference is never an error: the device
registers, and its profile stays unconstrained until a layout with that id is registered.

Keep `DeviceCapabilities` to facts a consumer can act on generically; geometry and rendering ability belong
in the layout.

### Receiving and rendering a session

```csharp
private readonly ConcurrentDictionary<string, long> _lastRevisions = new(StringComparer.Ordinal);

public Task OnSessionOpenedAsync(IDeviceSession session, CancellationToken cancellationToken = default)
{
	session.SurfaceChanged += (_, e) => Render(session.ProviderDeviceId, e.Surface);
	session.Closed += (_, e) => StopRendering(session.ProviderDeviceId);

	Render(session.ProviderDeviceId, session.CurrentSurface);
	return Task.CompletedTask;
}

private void Render(string serial, DeviceSurface surface)
{
	if (surface.Revision <= _lastRevisions.GetValueOrDefault(serial))
	{
		return;
	}

	_lastRevisions[serial] = surface.Revision;
	_watcher.Pad(serial).Clear(surface.Layout.Rows, surface.Layout.Columns, surface.Layout.BackgroundColor);

	foreach (var widget in surface.Widgets)
	{
		_watcher.Pad(serial).DrawKey(widget.PositionX, widget.PositionY, widget.Appearance?.Label,
			widget.Appearance?.BackgroundColor);
	}
}
```

The host calls `OnSessionOpenedAsync` once per registered device. Leave it at its default no-op and the
device stays registration-only forever.

- **Every surface is a complete snapshot** - profile, folder, effective layout, every widget - never a diff.
  `CurrentSurface` is the first one; there is no separate "initial" event.
- **`Revision` starts at 1 and increases within this session only.** A reconnect opens a fresh session with
  a new sequence and a full snapshot. Drop any surface whose revision is not strictly greater than the last
  one you applied - it is your only out-of-order signal. Never persist a revision.
- **`Layout` is already resolved:** rows, columns, spacing and border radius come from the folder, then its
  ancestors, then the profile defaults; the background is the folder's own or the profile default.
- **No reflow, clipping or validation.** A 3x2 device given a 5x3 profile gets the full 5x3 grid, positions
  included; paging, scrolling or cropping is yours. `Layout.LayoutReference` echoes your declared reference
  byte for byte.
- **`Widgets`** holds every widget in the folder plus any foreign pinned widget whose scope reaches it, each
  once. Labels are already resolved and localized - render them as-is.
- **A widget with a transparent background arrives without one.** When the user makes a widget's
  background transparent, its `Appearance.BackgroundColor` is null, the same as a widget with no colour of
  its own: draw the folder background behind that key, or your own default where there is none.
  `Layout.BackgroundColor` carries the folder background as the user stored it, which can be a CSS colour
  such as `rgb(...)` or the literal `transparent` rather than `#rrggbb`.
- **Two kinds of colour arrive flattened to an opaque `#rrggbb`:** one that follows a
  [Color variable](https://docs.macro-deck.app/features/variables/#color-variables), resolved to its current value, and one stored as
  translucent, such as `rgba(...)` or `#rrggbbaa` below full opacity, with the alpha dropped. This applies to the layout and widget
  colours alike, and the surface is rebuilt when a referenced variable changes. Every other colour arrives
  exactly as stored.

### Reporting interactions

```csharp
var result = await session.SendInteractionAsync(new DeviceInteraction
{
	Kind = DeviceInteractionKind.Press,
	Target = new DeviceInteractionTarget { WidgetId = widget.Id },
	SurfaceRevision = session.CurrentSurface.Revision
});

if (result.ReasonCode == DeviceSessionReasons.WidgetNotOnSurface)
{
	Render(session.ProviderDeviceId, session.CurrentSurface);
}
```

The host resolves the widget and runs its actions; a provider never sees or executes a flow. A press only
navigates *that* device: a folder change applies to the pressing session, and other devices on the same
profile keep what they show. `SurfaceRevision` lets the host discard a press aimed at a superseded surface.

The widget id must come from the surface you are rendering. A refusal is normal - nothing ran, the session
stays open, the next press works:

| Result | Meaning |
| --- | --- |
| `Accepted` | The host took it. For a `ShortPress` or `LongPress` on a tile a plugin or integration serves, it can mean *queued*: see below. |
| `Rejected` + `WidgetNotOnSurface` | The press raced a surface push. Re-render the newest surface. |
| `Rejected` + `HostLocked` | The host is locked and runs nothing until unlocked. |
| `Rejected` + `TriggerFailed` | The widget was edited or deleted between push and press. |
| `Rejected` + `SessionNotFound` | The host no longer holds the session; `Closed` follows. |
| `NotSupported` | A contract kind with no widget model yet. |

Only `Press`, `Release`, `ShortPress` and `LongPress` execute today; every other `DeviceInteractionKind` is
answered `NotSupported`.

| You send | The host fires |
| --- | --- |
| `Press` | `onTouchStart` immediately, and starts a 600 ms timer. |
| (timer elapses while held) | `onLongPress`. |
| `Release` | `onTouchEnd`, plus `onShortPress` if the long press had not fired. |
| `ShortPress` / `LongPress` | That trigger directly - no synthesis. |

A built-in widget with a Double Tap action changes the `Release` row. The `onShortPress` is held for 400 ms. A second
`Press` in that window that is released before the long press runs `onDoublePress` after its `onTouchEnd`,
and neither tap runs `onShortPress`. If that second press becomes a long press, the held `onShortPress` runs
first, right before `onLongPress`. Navigation, the device going offline and the session closing drop a held
`onShortPress`. Double taps come only from `Press`/`Release` pairs: an explicit `ShortPress` always runs at
once and keeps its verdict, so hardware that reports whole presses never produces `onDoublePress`. A widget
whose only press action is a Double Tap advertises `Press` and `Release` only.

The built-in Countdown and Stopwatch widgets always advertise `Press`, `Release`, `ShortPress` and
`LongPress`, flows or not: a short press starts, pauses, resumes or dismisses the timer and a long press
resets it, and each change runs the widget's own timer flows. Their surface carries the label and colours
only, not the running time.

A widget whose type declares a
[default Short Press action](https://docs.macro-deck.app/ui/views/widget-types/#a-default-short-press-action) advertises `Press`,
`Release`, `ShortPress` and `LongPress` without any flow, and a short press runs that default unless the
user gave the widget a Short Press action of their own. The built-in Weather widget is the exception: its
default opens a dialog, which a hardware deck cannot show, so that default is neither advertised nor run.

A tile that a plugin or integration serves, rather than a built-in one, answers a press from its own UI tree
first, exactly as it does on screen: a [disabled region](https://docs.macro-deck.app/ui/components/modifier/) absorbs the press, and a
control that declares the press receives it instead of the tile's flows. A press the tree does not claim
runs the tile's flows only if its type is registered with
[`SupportsFlows`](https://docs.macro-deck.app/ui/views/widget-types/#running-the-users-actions). Double taps are never recognised on
such a tile: a tree's `double-press` is never sent from a hardware deck, so a button declaring it receives
`press` for every tap, and a Double Tap flow never runs from one. The host asks that tree once per
press and waits at most a second for it; a tree that does not answer in time absorbs the press. Because the
tree may arrive over the same connection your report came in on, the host never holds your report for it:
`Press` and `Release` return at once as always, and a `ShortPress` or `LongPress` whose tree has not answered
yet is answered `Accepted` and runs afterwards, so a failure of that flow no longer comes back as
`Rejected` + `TriggerFailed`. Built-in tiles keep the full verdict.

Press state is tracked **per widget**: releasing one widget never ends another's press, and a second
`Press` for a widget already held is ignored (no timer restart, no second `onTouchStart`). If your hardware
already tells short from long, send `ShortPress`/`LongPress` instead of a `Press`/`Release` pair.

### Fetching icons

```csharp
var appearance = widget.Appearance;
if (appearance?.IconId is { } iconId)
{
	var cached = _icons.GetValueOrDefault((iconId, appearance.IconVersion));
	var image = await session.GetIconAsync(iconId, size: 72, knownETag: cached?.ETag);
	if (image is { NotModified: false })
	{
		_icons[(iconId, appearance.IconVersion)] = image;
	}
}
```

- **`knownETag`** skips an unchanged transfer: the result has `NotModified` set and empty `Content`.
- **Cache by `IconId` and `IconVersion`.** Re-rendering an icon keeps its id; the version says the bytes
  changed.
- **`IconId` names the image to draw.** When the user's icon has
  [appearances](https://docs.macro-deck.app/guide/concepts/#icon-appearances), `IconId` is the GUID of the appearance Macro Deck chose
  for this device, which can differ from the icon id stored on the widget. If your layout declares
  `Visuals` with `AnimatedIcons` false, that is the icon's static appearance when it has one. Fetch it with
  `GetIconAsync` like any other id; it does not appear in icon listings.
- **`size: null`** serves the largest size variant (512 px), which Macro Deck creates from the master when a
  pack arrived without it. An icon no larger than that is served as it is.
- **Too large** throws `DeviceSessionException` with `ReasonCode` `IconTooLarge`; the session stays open.

The bytes travel the `host.asset.*` chunked channel; `GetIconAsync` hides that.

### Fetching a provider-controlled icon

```csharp
if (appearance is { HasProviderIcon: true })
{
	var image = await session.GetWidgetIconAsync(widget.Id, knownETag: cachedETag);
	// null: nothing to serve right now - render label and colour instead.
}
```

An action can own the icon a widget renders (album artwork, an avatar, weather imagery). `IconId` stays
GUID-only forever, so such an icon has none: `HasProviderIcon` is true exactly when the rendered icon comes
from a provider, and `IconId` is then null. `IconVersion` is the content identity of whatever is rendered,
either kind, so a cache keys on the same value.

`GetWidgetIconAsync` addresses the owning widget and otherwise mirrors `GetIconAsync` (`knownETag`, same
channel). It returns null rather than throwing when the provider went inactive, answered blank, or the
widget is not on the current surface. It is default-implemented to return null, and a provider built
before `HasProviderIcon` existed simply renders label and colour, as for an icon-less widget.

### Ending a session

```csharp
await session.DisposeAsync();
```

`DisposeAsync` closes the session on the host too, so you are not pushed to any more. `Closed` is raised
exactly once, whichever side ends it first - your `DisposeAsync`, a host-initiated close, or the device
going away. `DeviceSessionClosedEventArgs.Reason` may be null.

### In a plugin

Declare the `device-provider` capability and `host:devices` in [`manifest.json`](https://docs.macro-deck.app/reference/manifest/).
`MacroDeck.Plugin.Hosting` starts the provider once the plugin is connected and its integration has
initialized, and stops it on shutdown. The provider is always the authenticated plugin: it cannot register
or withdraw a device in another plugin's name.

Sessions need `device-provider` **capability version 2**. The host opens a session only when the negotiated
version is 2 or higher; a plugin that negotiates version 1 keeps registering, updating and unregistering
as before and is never sent a session operation - it degrades to registration only.

### Testing

```csharp
using MacroDeck.Plugin.Testing.Fakes;
using MacroDeck.Sdk.Devices;

[Test]
public async Task A_replugged_pad_is_the_same_device_and_renders_its_surface()
{
	var context = new FakeDeviceProviderContext();
	var integration = new MacroPadIntegration(new FakePadWatcher("SERIAL-1"));

	await integration.InitializeAsync(context);
	var firstId = context.AssignedIdOf("SERIAL-1");

	await context.UnregisterDeviceAsync("SERIAL-1");
	await context.RegisterDeviceAsync(new DeviceDescriptor("SERIAL-1", "Macro Pad"));

	var session = await context.OpenSession(integration, "SERIAL-1");
	session.PushSurface(new DeviceSurface
	{
		Revision = 1,
		Layout = new DeviceSurfaceLayout { Rows = 2, Columns = 3 },
		Widgets = []
	});

	Assert.Multiple(() =>
	{
		Assert.That(context.AssignedIdOf("SERIAL-1"), Is.EqualTo(firstId));
		Assert.That(context.IsOnline("SERIAL-1"), Is.True);
		Assert.That(session.Interactions, Is.Empty);
	});
}
```

`FakeDeviceProviderContext` keeps the host's identity rules: re-registering a known id is the same device,
unregistering retains it and only takes it offline. Assert on `Devices`, `IsOnline`, `AssignedIdOf`,
`Calls` and `Interactions`.

`OpenSession` hands your provider a `FakeDeviceSession` (the device must be registered first). Drive it with
`PushSurface` and `Close`, script the verdict with `NextResult`, and seed `Icons` / `WidgetIcons`; read back
`Interactions`, `IconRequests` and `WidgetIconRequests`.

Against a real plugin process, the harness's `DeviceProvider` client (`PluginTestHarness`,
`PluginSessionView`) invokes `describe`, `devices`, `session.open`, `session.surface` and `session.close`.
See [Testing](https://docs.macro-deck.app/features/testing/).

### Over the plugin protocol

The host-to-provider direction of the `device-provider` capability describes the provider, re-reads its
catalogue after a reconnect and, from capability version 2, drives rendering sessions:

| Operation | Purpose |
| --- | --- |
| `describe` | The provider's declared name and capability version. |
| `devices` | The provider's current device catalogue, re-read after a reconnect. |
| `session.open` | Opens a device's session and hands over the first surface to render. Version 2 only. |
| `session.surface` | Pushes a new, complete surface to an already-open session. Version 2 only. |
| `session.close` | Closes an open session. Version 2 only. |

Registration, interactions and icon fetches travel the other way as the `devices` host API:

| Operation | Purpose |
| --- | --- |
| `register` | Registers a device, or re-registers a known provider-local id as the same device. |
| `update` | Refreshes a registered device's metadata. |
| `presence` | Reports whether a registered device is currently reachable. |
| `unregister` | Withdraws a device from this session; the device itself is retained. |
| `interaction` | Reports a hardware interaction from an open device session. |
| `icon` | Fetches icon bytes referenced by a device's current surface, over the `host.asset.*` pipeline. |
| `widget-icon` | Fetches the bytes behind a widget's currently rendered action-icon-provider icon, over the `host.asset.*` pipeline. |
| `close` | Closes an open device session at the provider's own request. |

### See also

- [Layout providers](https://docs.macro-deck.app/features/layouts/) - the geometry a `LayoutReference` points at.
- [Button icons](https://docs.macro-deck.app/features/button-icons/) - where provider-controlled icons come from.
- [Manifest](https://docs.macro-deck.app/reference/manifest/) - `device-provider` and `host:devices`.
- [WebSocket reference](https://docs.macro-deck.app/reference/websocket/) - the wire format for the tables above.
- [Testing](https://docs.macro-deck.app/features/testing/) - the fakes and the test harness.

## Email inboxes

> Source: https://docs.macro-deck.app/features/email-inboxes/
>
> Expose email inboxes with IEmailInboxProvider - inbox ids, status and counts, the newest messages, change notifications, limits, and what Macro Deck builds on top.

An integration exposes email inboxes by implementing `IEmailInboxProvider`. It lists the inboxes it can
read, and for each inbox returns a snapshot: whether it is connected, how many messages are unread and in
total, and the newest messages with their sender, subject and a short preview. Macro Deck merges the
inboxes of every provider, so the user's email widget, variables and triggers work with your service next to
the built-in IMAP integration without any further code.

Connecting an account is not part of this contract. Signing in, storing passwords or tokens and asking the
user to sign in again belong to your [setup flow](https://docs.macro-deck.app/features/setup-flows/) and your
[integration issues](https://docs.macro-deck.app/features/integration-issues/). `IEmailInboxProvider` only reads, and never the full
body of a message.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Email;

public sealed class TeamMailIntegration : IPluginIntegration, IEmailInboxProvider
{
	private Dictionary<string, TeamMailClient> _clients = [];
	private IReadOnlyList<EmailInbox> _inboxes = [];

	public IReadOnlyList<IActionDefinition> Actions { get; } = [];

	public event EventHandler<EmailInboxChangedEventArgs>? Changed;

	public async Task InitializeAsync(IIntegrationContext context)
	{
		var clients = new Dictionary<string, TeamMailClient>();
		var inboxes = new List<EmailInbox>();

		// One inbox per config entry your setup flow created.
		foreach (var entry in await context.Config.GetEntriesAsync())
		{
			var id = entry.Id.ToString("N");
			var client = new TeamMailClient(await context.Config.GetSecretAsync(entry.Id, "token"));
			client.MailboxChanged += (_, _) => Changed?.Invoke(this, new EmailInboxChangedEventArgs(id));
			clients[id] = client;
			inboxes.Add(new EmailInbox { Id = id, DisplayName = entry.Title, Address = client.Address });
		}

		_clients = clients;
		_inboxes = inboxes;
		Changed?.Invoke(this, new EmailInboxChangedEventArgs(null));
	}

	public Task ShutdownAsync() => Task.CompletedTask;

	public IReadOnlyList<EmailInbox> GetInboxes() => _inboxes;

	public async Task<EmailInboxSnapshot> GetSnapshotAsync(
		string inboxId, EmailMessageQuery query, CancellationToken ct)
	{
		// An inbox this provider no longer knows is a failure, not an empty inbox.
		var client = _clients.TryGetValue(inboxId, out var found)
			? found
			: throw new InvalidOperationException($"Unknown inbox '{inboxId}'.");

		var mailbox = await client.ReadAsync(query.MaxMessages, query.UnreadOnly, ct);

		return new EmailInboxSnapshot
		{
			Status = client.IsConnected ? EmailInboxStatus.Connected : EmailInboxStatus.Disconnected,
			UnreadCount = mailbox.Unread,
			TotalCount = mailbox.Total,
			SyncedAt = mailbox.SyncedAt,
			Messages =
			[
				.. mailbox.Messages.Select(m => new EmailMessage
				{
					Id = m.Id,
					SenderName = m.FromName,
					SenderAddress = m.FromAddress,
					Subject = m.Subject ?? string.Empty,
					Preview = m.Snippet,
					ReceivedAt = m.ReceivedAt,
					IsRead = m.IsRead
				})
			]
		};
	}
}
```

Register it like any integration, with `RegisterIntegration<TeamMailIntegration>()` in `Program.cs`. The
SDK sees `IEmailInboxProvider` and declares the `email-inbox` capability for you. Add an
`IConfigFlowProvider` with `AllowsMultipleConfigurations` so the user can connect one account per entry.

Things to know:

- **Inbox ids are local and permanent.** Return the id you chose, not a qualified one. The host stores the
  user's inbox selection and trigger filters as `integrationId::inboxId`, and names the inbox's variables
  once, the first time it sees the id. An id that changes on restart turns every inbox into a new one: its
  widget selection is lost and it gets new variables. A config entry id is a good choice.
- **`GetInboxes` is synchronous and called often.** Return a cached list, as above.
- **Raise `Changed` when something changed.** With an inbox id when that inbox's messages, counts or status
  changed; with `null` when inboxes were added, removed or renamed. Raise it as often as changes happen:
  bursts are coalesced before anything reads again.
- **You only read.** The host decides when to read, caches the snapshots and drives every widget,
  variable and trigger from that cache. It never marks a message as read or changes the mailbox.

### The contract

`IEmailInboxProvider` and its records carry the full rules in their XML docs. The ones that decide whether
your provider behaves correctly:

| Member | Rules |
| --- | --- |
| `GetInboxes()` | Each `Id` is a valid resource local id (non-empty, at most 256 characters, no whitespace and no `::`), unique within the provider and stable across restarts. An inbox that breaks this is skipped and logged. `DisplayName` is shown to the user; `Address` is optional. No status here: an unreachable inbox stays in the list. |
| `GetSnapshotAsync` | The inbox's `Status`, `UnreadCount` and `TotalCount` for the whole inbox, and at most `query.MaxMessages` messages, **newest first**. `SyncedAt` says when the data was last brought up to date. |
| `EmailMessageQuery` | `MaxMessages` is between 1 and 50 and defaults to 10. With `UnreadOnly`, return the newest **unread** messages wherever they are in the inbox, not the unread ones among the newest. |
| `EmailMessage` | `Id` is unique within the inbox and stable across reads; it is how the host tells new mail from mail it has already seen. `Subject` is empty when the message has none. `Preview` is a short plain-text excerpt or `null`, never the body. |
| `Changed` | `InboxId` set: read that inbox again. `null`: read the inbox list again, then every inbox. May be raised on any thread. |

#### Status, not exceptions, for a known state

`GetSnapshotAsync` reports what you know and throws only when you cannot answer at all:

| Situation | Return |
| --- | --- |
| Connected and the read worked. | `Connected` with current counts and messages. |
| Connecting for the first time, or reconnecting after a short drop. | `Connecting` with the last known data, empty if there is none yet. |
| The server cannot be reached for now. | `Disconnected` with the last known data and a `StatusMessage`. |
| The user has to act, for example the sign-in was refused. | `Error` with the last known data and a `StatusMessage` that says what to do, ideally next to an [integration issue](https://docs.macro-deck.app/features/integration-issues/). |
| The read failed and you have nothing to return, or the inbox id is unknown. | Throw. |

The host shows the inbox's status next to its data, and an Email Inbox widget that shows only this inbox
shows its `StatusMessage` while it is not connected. It fires the **Inbox Connected** and **Inbox
Disconnected** triggers when it changes between connected and not connected; `Connecting` changes neither.
After a thrown read it keeps the last data, marks it as out of date and tries again shortly; only a second
failure in a row counts as disconnected. Write `StatusMessage` in the user's language, see
[Localization](https://docs.macro-deck.app/features/localization/). Honour the cancellation token and let
`OperationCanceledException` propagate.

#### Message ids

The host decides which messages are new by comparing ids between two `Connected` snapshots, and fires
**Email Received** once per new id. The first `Connected` snapshot of an inbox fires nothing, and a snapshot
with any other status never counts as the inbox's contents, so answering `Connecting` with no data does not
make the mail you report afterwards look new. Make the id stable for as long as the message exists, for
example an IMAP UIDVALIDITY and UID pair:

```csharp
new EmailMessage
{
	Id = $"{folder.UidValidity}-{uid}", // stable while the folder keeps its UIDVALIDITY
	SenderAddress = "bob@example.com",
	Subject = "Lunch?",
	ReceivedAt = internalDate
};
```

An id that changes between reads makes old mail look new. If your service ever renumbers every message at
once, as an IMAP UIDVALIDITY change does, the host recognizes that none of the new ids is newer than what it
had and fires nothing.

#### Telling the host about changes

Raising `Changed` is the only push this contract has. In a plugin, `MacroDeck.Plugin.Hosting` forwards it to
the host as a `state.update` for the `email-inbox` kind, after holding it back for 250 ms per inbox so a
burst becomes one message. Calling `CatalogChanged("email-inbox", inboxId)` on the injected
`IPluginCatalogNotifier` yourself has exactly the same effect, and `CatalogChanged("email-inbox")` with no id
is the same as raising `Changed` with `null`.

A provider that never raises `Changed` still works: the host also reads every inbox after a user's
**Refresh Email Inboxes** and on a fallback poll every five minutes. New mail simply shows up that much later.

### What Macro Deck builds on it

Implementing `IEmailInboxProvider` is all it takes for your inboxes to appear in everything Macro Deck
offers for email. You declare none of it:

- The **Email Inbox** widget, which shows the unread count of one or several inboxes, or a list of the
  newest messages with sender, subject, preview and time, and whose settings list your inboxes by name with
  the provider beside them.
- Global variables such as `email_unread_count` and `email_inbox_count`, and per inbox
  `email_<name>_unread_count`, `email_<name>_total_count`, `email_<name>_latest_sender`,
  `email_<name>_latest_subject`, `email_<name>_latest_received_at` and `email_<name>_is_connected`, where
  `<name>` comes from the inbox's display name the first time the host sees it and is kept after a rename.
  At most 40 inboxes get variables. While your integration is disabled, its inboxes keep their variables,
  which read as unavailable.
- The triggers **Email Received**, filterable by inbox and by exact sender and subject, **Unread Count
  Changed**, **Email Read or Unread**, **Inbox Connected** and **Inbox Disconnected**, under the event
  provider `email`. Their payload values are `inbox`, `inboxName`, `sender`, `senderAddress`, `subject`,
  `preview`, `messageId`, `receivedAt`, `unreadCount`, `previousUnreadCount` and `isRead`. **Email
  Received** does not fire for the messages an inbox already has when the host starts or when the inbox first
  appears; mail that arrived while the inbox was unreachable fires once when it is back.
- The **Refresh Email Inboxes** action, which reads every inbox right away instead of waiting for the next
  change.

The [user guide](https://docs.macro-deck.app/guide/concepts/#email-inbox-widget) describes them from the user's side. Do not build your own versions
of these. If your service offers more, such as archiving a message, add [actions](https://docs.macro-deck.app/features/actions/) of
your own.

`ProviderName` is optional. Leave it out and the integration's name (the manifest name for a plugin) is
shown next to the inbox. Set it when one integration exposes a distinctly branded service.

### Edge cases

- **An inbox disappears.** Drop it from `GetInboxes` and raise `Changed` with `null`. It leaves the widgets
  and its variables are removed; widget and trigger filters naming it simply match nothing.
- **Invalid or duplicate inbox ids** are skipped and logged. An id two integrations of one plugin both list
  belongs to the first.
- **A read fails.** The inbox keeps its last data, marked as out of date, until a later read succeeds.
- **The plugin stops or crashes.** Its inboxes keep their last data and show as disconnected until it is
  back.
- **The same mailbox in two providers**, such as one account connected twice, shows twice: the host has no
  way to know they are one inbox.

### Optional abilities later

The contract is read-only on purpose. Abilities such as marking a message as read, archiving or moving it,
reading its full body or listing other folders will be added as separate interfaces a provider may implement
next to `IEmailInboxProvider`, the way `IMusicPlayerDeviceProvider` sits next to `IMusicPlayerProvider`. They
will be optional: a provider that implements none of them keeps working unchanged, and Macro Deck only offers
an ability for the inboxes whose provider has it.

### Over the plugin protocol

Email inboxes are fully supported out of process, as capability kind `email-inbox`, version `1`, declared
once at the local id `provider`. Its operations are `describe`, `inboxes` and `snapshot`; the
[WebSocket reference](https://docs.macro-deck.app/reference/websocket/#email-inbox) lists their arguments and results.

- **The inbox list is a snapshot.** The host serves `GetInboxes` from the last `describe` or `inboxes`
  reply, and reads `inboxes` again after a `state.update` without a local id.
- **A change names the inbox.** A `state.update` whose `localId` is an inbox id makes the host read that
  inbox's `snapshot` again, nothing else: the plugin is not described again and nothing re-registers.
- **The status travels by name.** `status` is the `EmailInboxStatus` member name; a host treats a name it
  does not know as `Disconnected`.
- **Replies are bounded.** `MacroDeck.Plugin.Hosting` keeps at most 32 inboxes, asks your provider for at
  most 50 messages, cuts long subjects, previews, sender names and addresses, and, when a `snapshot` reply
  would still exceed its size limit, drops its oldest messages and marks the reply as truncated. The exact
  limits are in the [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#email-inbox).
- **Failures stay failures.** An unreachable plugin, a timeout or an exception in your provider reaches the
  host as a failed read, never as an empty inbox.
- **Older hosts.** A Macro Deck that predates email inboxes rejects the `email-inbox` declaration
  non-fatally: the session carries on, and your actions, variables and everything else keep working. Your
  inboxes simply do not appear.

See [Capability parity](https://docs.macro-deck.app/reference/capability-parity/).

### Testing

`harness.EmailInbox`, an `EmailInboxTestClient`, drives the `email-inbox` capability the way the host does,
with the protocol's argument records from `MacroDeck.Plugin.Protocol.Capabilities.EmailInbox`:

```csharp
await using var harness = PluginTestHarness.Create(builder =>
	builder.RegisterIntegration<TeamMailIntegration>());
var entry = harness.Context.Config.AddEntry("Work");
harness.Context.Config.SeedSecret(entry, "token", "test-token");
await harness.InitializeIntegrationsAsync();

var outcome = await harness.EmailInbox.GetSnapshotAsync(new EmailInboxSnapshotArguments
{
	InboxId = entry.ToString("N"),
	MaxMessages = 5,
	UnreadOnly = true
});

Assert.That(outcome.Succeeded, Is.True, outcome.Error?.Message);
Assert.That(outcome.DataAs<EmailInboxSnapshotResult>()!.Messages.Select(m => m.Subject), Is.EqualTo(["Lunch?"]));
```

Here `TeamMailClient` talks to a fake of the mail service, the one real external boundary.
`DescribeAsync` and `GetInboxesAsync` cover the other operations, and the session `MacroDeckTestHost`
returns has the same `EmailInbox` client over the real wire, where raising `Changed` shows up in
`host.Messages` as a `state.update`. What you get back is what the host gets: the status as a name, the
field limits applied, and an inbox id you do not know as a failed outcome. In the harness, the 250 ms hold on
`Changed` runs on `harness.Clock`. See [Testing](https://docs.macro-deck.app/features/testing/).

### See also

- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - connecting accounts.
- [Integration issues](https://docs.macro-deck.app/features/integration-issues/) - asking the user to sign in again.
- [Events](https://docs.macro-deck.app/features/events/) - triggers of your own beside the built-in email ones.
- [Localization](https://docs.macro-deck.app/features/localization/)
- [Testing](https://docs.macro-deck.app/features/testing/)

## Events

> Source: https://docs.macro-deck.app/features/events/
>
> Declare events with IEventProvider, publish occurrences with IEventPublisher, and let users filter them with configuration parameters and dynamic options.

An integration tells Macro Deck "this just happened" with events. `IEventProvider` declares which events
exist; `IEventPublisher`, handed to you on the integration context, publishes an occurrence. Users react
to them with triggers.

These events are for the user's automation. To tell other plugins that something happened, publish on
the [message channel](https://docs.macro-deck.app/features/messaging/) instead: its events reach plugins, not triggers.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Events;

public sealed class StreamStudioIntegration : IPluginIntegration, IEventProvider
{
	private StudioClient? _client;

	public IReadOnlyList<EventDefinition> EventDefinitions { get; } =
	[
		new()
		{
			Id = "scene-changed",
			Name = Strings.Events.SceneChanged(),
			Category = Strings.Events.ScenesCategory(),
			ConfigurationParameters =
			[
				ActionParameter.DynamicChoice("sceneId",
					label: Strings.Parameters.Scene(),
					placeholder: Strings.Parameters.AnyScene())
			],
			PayloadParameters =
			[
				ActionParameter.DynamicChoice("sceneId", label: Strings.Parameters.SceneId()),
				ActionParameter.Text("sceneName", label: Strings.Parameters.Scene())
			]
		}
	];

	public Task InitializeAsync(IIntegrationContext context)
	{
		var events = context.Events; // safe to keep for the process lifetime
		_client = new StudioClient();
		_client.SceneChanged += scene => events.Publish("scene-changed", new Dictionary<string, object?>
		{
			["sceneId"] = scene.Id,
			["sceneName"] = scene.Name
		});
		return Task.CompletedTask;
	}

	// Remaining IPluginIntegration members omitted.
}
```

The user now finds "Scene changed" in the trigger editor, can narrow it to one scene, and can use
`sceneId` and `sceneName` in the flow it runs.

Things to know:

- **`Id` is persisted** in every trigger that uses the event. Treat it as a public identity: never
  rename it once shipped. It must be unique within your integration; the host namespaces it as
  `integrationId::eventId`.
- **`Publish` is fire-and-forget.** It never throws into the caller and has no reply, so it is safe to
  call from a socket callback or polling loop. An occurrence nobody subscribed to is simply dropped.
- **Payload keys must match the declaration.** Publish the names you listed in `PayloadParameters` -
  those are what the user can pick and filter on.

### Defining an event

| Property | What it does | Example |
| --- | --- | --- |
| `Id` | Provider-local id, stable across releases. | `"scene-changed"` |
| `Name`, `Description` | Localized text in the event picker. | `Strings.Events.SceneChanged()` |
| `Category` | Groups events in the picker. Optional. | `Strings.Events.ScenesCategory()` |
| `IconName` | An icon the UI already ships. No image data. | `"movie"` |
| `ConfigurationParameters` | What the user authors on the trigger - see below. | `ActionParameter.DynamicChoice("sceneId", ...)` |
| `PayloadParameters` | What an occurrence carries. Never rendered as an input. | `ActionParameter.Text("sceneName", ...)` |
| `DeliveryKind` | `Push` (default): you publish. `Scheduled`: the host produces occurrences from the configuration. | `EventDeliveryKind.Push` |

`ProviderName` on `IEventProvider` is optional; leave it empty and the event picker shows your
integration's name (for a plugin, the `manifest.json` name).

`EventDefinitions` is read whenever the host builds the event catalogue, so it may change after a
reconfigure. An out-of-process plugin must tell the host to re-read it:

```csharp
using MacroDeck.Plugin.Hosting.Integrations.HostApis; // IPluginCatalogNotifier, injected
using MacroDeck.Plugin.Protocol.Handshake;             // CapabilityKinds

catalogNotifier.CatalogChanged(CapabilityKinds.Events);
```

### Configuration parameters vs payload parameters

```csharp
ConfigurationParameters =
[
	ActionParameter.DynamicChoice("trackId", label: Strings.Parameters.Track(), placeholder: Strings.Parameters.AnyTrack())
],
PayloadParameters =
[
	ActionParameter.DynamicChoice("trackId", label: Strings.Parameters.TrackId()),
	ActionParameter.Text("trackName", label: Strings.Parameters.Track()),
	ActionParameter.Toggle("muted", label: Strings.Parameters.Muted())
]
```

Both lists use the ordinary `ActionParameter` schema, so any control the action builder renders is
available.

- **Configuration parameters** are what the user fills in on the trigger. When one shares its name with
  a payload parameter, the host compares the two and only fires the trigger on a match. Left empty, it
  matches any occurrence - "any track" above.
- **Payload parameters** describe what an occurrence carries. They populate the picker that inserts
  `{ "$event": "trackName" }` references into the triggered flow and label values in the live preview.
  When a user writes a condition against `$event`, the comparison value is authored with the control the
  payload parameter's type implies, while the condition still stores the raw value the occurrence
  carries. So declare an enumerable payload value the same way as its matching filter (a `DynamicChoice`
  here): the user picks a track name instead of pasting an id.

### Publishing values

```csharp
_events.Publish("hotkey-pressed", new Dictionary<string, object?>
{
	["key"] = "F3",                                                  // string
	["repeat"] = 2,                                                  // number
	["held"] = false,                                                // boolean
	["combo"] = new { modifiers = new[] { "Ctrl", "Shift" }, key = "F3" } // object
});
```

| Published value | What triggers, templates and conditions see |
| --- | --- |
| string, number, boolean | the value itself |
| object or array | its compact JSON text: `{"modifiers":["Ctrl","Shift"],"key":"F3"}` |

A condition on an object or array value compares that text. Publishing without parameters is fine for
events that carry nothing:

```csharp
_events.Publish("connected");
```

### Keyboard combos

A `KeyboardCombo` or `Hotkey` value is an object with a `key` name and a `modifiers` list:
`{"modifiers":["Ctrl","Shift"],"key":"Minus"}`. The combo editor stores these names, and Press Key,
Key Down and Key Up read them. Publish the same names from a keyboard hook and every trigger the user
set up in the editor matches.

| Key | Name | Means |
| --- | --- | --- |
| Letters | `A` to `Z` | The key labeled with that letter on the active layout: `Z` is the Z key on QWERTZ too. |
| Digits | `0` to `9` | The key in the digit row, also on AZERTY where it types `&`, `é` and so on without Shift. |
| Punctuation | `Minus`, `Equal`, `BracketLeft`, `BracketRight`, `Backslash`, `Semicolon`, `Quote`, `Comma`, `Period`, `Slash`, `Backquote` | A physical position, named after the key at that position on a US keyboard, like the browser's `KeyboardEvent.code`. On German, `Minus` is the `ß` key and `BracketLeft` the `ü` key. |
| ISO key | `IntlBackslash` | The extra key that ISO keyboards have next to left Shift (`<` on German). |
| Other keys | `F1` to `F24`, `Enter`, `Escape`, `Tab`, `Space`, `Backspace`, `Delete`, `Insert`, `CapsLock`, `Home`, `End`, `PageUp`, `PageDown`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`, `PrintScreen`, `ScrollLock`, `Pause`, `NumLock`, `Numpad0` to `Numpad9`, `NumpadAdd`, `NumpadSubtract`, `NumpadMultiply`, `NumpadDivide`, `NumpadDecimal`, `NumpadEnter`, `MediaPlayPause`, `MediaStop`, `MediaTrackNext`, `MediaTrackPrevious`, `AudioVolumeUp`, `AudioVolumeDown`, `AudioVolumeMute` | The same key on every layout. |

Modifiers are `Ctrl`, `Shift`, `Alt` and `Meta` (Command on macOS, Windows key on Windows), plus
`RightCtrl`, `RightShift`, `RightAlt` and `RightMeta` when only the right-hand key counts.

The host also accepts older spellings, and trigger matching treats them as the name they stand for:
`-` for `Minus` (and the other unshifted US characters), `Esc`, `Return`, `Del`, `Ins`, `PgUp`, `PgDn`,
`Up`/`Down`/`Left`/`Right` and `5` as well as `D5` for keys, `Control`, `Cmd`, `Command`, `Win`, `Super`,
`Option` and `AltGr` (which counts as `Alt`) for modifiers. Names are case-insensitive. A name the host
does not know is compared as text, so two plugins can still agree on a key Macro Deck has no name for.

Only configuration parameters of type `KeyboardCombo` or `Hotkey` match this way. A trigger filter or a
flow condition on `$event` compares the published JSON text, as described above.

#### From a native keyboard hook

`MacroDeck.Sdk.Input` turns the codes a keyboard hook delivers into the names above, so a plugin needs no
table of its own:

```csharp
using MacroDeck.Sdk.Input;

KeyCode key = NativeKeys.FromWindows(virtualKey, scanCode, isExtended); // or FromMacOS(code), FromLinux(code)

if (KeyNames.TryGetModifier(key, out var modifier))
{
    held = isKeyDown ? held | modifier : held & ~modifier;   // track the modifier keys yourself
    return;
}

if (isKeyDown && key != KeyCode.None)
{
    events.Publish("hotkey-pressed", new Dictionary<string, object?>
    {
        ["combo"] = new { modifiers = KeyNames.ToModifierNames(held), key = KeyNames.ToName(key) }
    });
}
```

`KeyNames.ToName` returns the one name the editor stores, and `KeyNames.TryParse` and `TryParseModifier` accept
every older spelling listed above. A key without a `KeyCode`, or a number that is no key code, comes back as
`KeyCode.None`: do not publish it. The methods never throw and can be called from any thread.

`ToModifierNames` names a modifier `Ctrl` when the left key is held, alone or together with the right one, and
`RightCtrl` only when just the right key is held, like the editor records it. Trigger matching compares the two
as different modifiers, so a trigger bound as `Ctrl` does not fire for `RightCtrl`.

| Platform | Method | Notes |
| --- | --- | --- |
| Windows | `NativeKeys.FromWindows(virtualKey, scanCode, isExtended)` | Pass the extended flag: it tells `NumpadEnter` from `Enter` and a navigation key from the numpad key that reports the same virtual key while NumLock is off. The scan code (without the extended prefix) names a punctuation key's position exactly. The overload without it reads the foreground window's layout instead. |
| macOS | `NativeKeys.FromMacOS(keyCode)` | Letters are resolved through the active input source, so key code 6 is `Y` on German. A letter position whose key types no Latin letter (Cyrillic) keeps its US letter. Key code 10 is `IntlBackslash` and 50 is `Backquote`, as Safari and the combo editor report them; on ISO Apple keyboards those two are swapped relative to the key's position. Function keys above `F20`, the Fn key and media keys have no key code and return `None`. |
| Linux | `NativeKeys.FromLinux(evdevCode)` | An evdev code is a position, so letters follow US positions on every layout: the Z-labeled key of a German layout is `Y`. |

`FromMacOS` reads the input source with the Text Input Sources API, which Apple documents for the main thread. It
has been exercised from a thread-pool thread, not from an event tap callback.

To send a key the other way, from a `KeyCode` to the native code a synthetic key event needs, the letter,
digit and punctuation keys of the main block have their US position on each platform:

```csharp
if (NativeKeys.IsPositional(key) && NativeKeys.TryGetWindowsScanCode(key, out var scan))
{
	// SendInput with KEYEVENTF_SCANCODE, so the key lands on the same position on any layout
}
```

| Method | Answers |
| --- | --- |
| `NativeKeys.IsPositional(key)` | `true` for the punctuation keys, which type a different character on each layout and are best sent by position |
| `NativeKeys.TryGetWindowsScanCode(key, out scan)` | The PC set-1 scan code; Linux evdev numbers these keys the same way |
| `NativeKeys.TryGetMacOSKeyCode(key, out code)` | The `kVK_*` key code, with WebKit's ISO naming (`IntlBackslash` 10, `Backquote` 50) |
| `NativeKeys.TryFromWindowsScanCode(scan, out key)` | The key at a scan code's US position, the inverse of `TryGetWindowsScanCode` |

Each `TryGet` method returns `false` for keys outside that block (function, navigation, media and modifier
keys), which a hook sends by their virtual key or key code instead.

`GetBindings()` returns values exactly as the editor stored them, so a hook that swallows bound combos has
to accept the older spellings too, not only the names in the table.

### Reading what is bound

A hotkey plugin that wants to swallow a bound combo, or an integration that only subscribes upstream to
what the user actually uses, can read the triggers bound to its own events instead of asking the user
to enter the same values twice:

```csharp
public Task InitializeAsync(IIntegrationContext context)
{
	_events = context.Events;
	_events.BindingsChanged -= ApplyBoundCombos;
	_events.BindingsChanged += ApplyBoundCombos;
	ApplyBoundCombos();
	return Task.CompletedTask;
}

private void ApplyBoundCombos()
{
	var combos = _events.GetBindings()
		.Where(binding => binding.EventId == "hotkey-pressed")
		.Select(binding => binding.Parameters.GetValueOrDefault("combo"))
		.Where(value => value is { Operator: "==", Value.ValueKind: JsonValueKind.Object })
		.Select(value => value!.Value!.Value)
		.ToList();

	_hook.Swallow(combos);
}
```

`InitializeAsync` runs again after a reconnect or a config change, on the same publisher, so remove the
handler before adding it or it fires once per initialization. Remove it in `ShutdownAsync` as well, so a
stopped integration stops reacting.

Each `EventBinding` is one widget flow or one enabled automation triggered by one of your events. You
see only your own events, never which widget or automation holds the trigger.

| Member | Meaning |
| --- | --- |
| `EventId` | Provider-local event id, without the `integrationId::` prefix. |
| `Parameters` | The configuration parameters the user set, by name. A parameter left empty is absent. |
| `EventBindingValue.Value` | The value as the editor stored it: a scalar, an object for a `KeyboardCombo`, or a variable reference the host resolves only when it matches an occurrence. `null` for the state operators. |
| `EventBindingValue.Operator` | `==`, `!=`, `>`, `<`, `>=`, `<=`, or one of `isEmpty`, `isNotEmpty`, `isAvailable`, `isNotAvailable`. |

A trigger can also carry a filter the host evaluates on its own, so a value in `GetBindings()` does not
guarantee the trigger fires for it.

`BindingsChanged` fires on a thread-pool thread after the list changed for your integration, and only
then: moving a widget or editing another plugin's trigger does not raise it. Out of process,
`GetBindings()` serves the host's last `event-bindings` push, so it is empty until the first push
arrives. Against a host that predates this API it stays empty and `BindingsChanged` never fires, so treat
an empty list as "nothing bound", never as an error.

### Dynamic options

```csharp
public sealed class StreamStudioIntegration : IPluginIntegration, IEventProvider, IDynamicEventOptionsProvider
{
	public Task<DynamicOptionsResult> GetEventOptionsAsync(EventOptionsContext context,
		CancellationToken cancellationToken)
	{
		var session = _client?.Session ?? StudioSession.Empty;

		IReadOnlyList<ActionParameterOption> options = context.ParameterName switch
		{
			"sceneId" => session.Scenes.Select(s => new ActionParameterOption { Value = s.Id, Label = s.Name }).ToList(),
			_ => []
		};

		return Task.FromResult(new DynamicOptionsResult
		{
			Options = options,
			AllowsCustomValue = true,
			CacheSeconds = 30
		});
	}
}
```

Implement `IDynamicEventOptionsProvider` when a choice is only known at edit time - a scene list, a
device, a channel. It answers configuration and payload parameters alike and never changes the event
definition itself. `EventOptionsContext` carries:

| Member | Meaning |
| --- | --- |
| `EventId` | Provider-local event id, without the `integrationId::` prefix. |
| `ParameterName` | The parameter being edited. |
| `Filter` | Text the user typed, for a filterable autocomplete. |
| `CurrentParameters` | The other configuration values, so options can depend on an earlier choice. |

The context names only the event and the parameter, so a request for the configuration parameter
`sceneId` looks exactly like one for the payload parameter `sceneId`. Declare the same name in both lists
only where the same options answer for both - as in every example on this page.

### Testing

```csharp
var context = new FakeIntegrationContext();
await integration.InitializeAsync(context);

studio.RaiseSceneChanged(new Scene("s1", "Intro"));

var published = context.Events.Published.Single();
Assert.That(published.EventId, Is.EqualTo("scene-changed"));
Assert.That(published.Parameters!.Value.GetProperty("sceneName").GetString(), Is.EqualTo("Intro"));
```

`FakeEventPublisher` serializes parameters exactly as the wire protocol does, and like the real one it
never throws. `SetBindings(...)` replaces what `GetBindings()` returns and raises
`BindingsChanged`, standing in for a user who binds or edits a trigger. `PluginTestHarness.Events` calls `describe` and `options` over the protocol. See
[testing](https://docs.macro-deck.app/features/testing/).

### Over the plugin protocol

Events are one provider-shaped capability per plugin: `describe` returns the merged catalogue of every
`IEventProvider` in the process, `options` routes to `IDynamicEventOptionsProvider`. The catalogue is
snapshot-backed. Occurrences travel as the fire-and-forget
[`event.publish`](https://docs.macro-deck.app/reference/websocket/#events-logs-and-state) message; the host qualifies the id with
the authenticated plugin id. What the user bound arrives as the push-only
[`host.state`](https://docs.macro-deck.app/reference/websocket/#host-callbacks) api `event-bindings`, scoped to the plugin's own
events and sent on registration and whenever that list changes. See
[capability parity](https://docs.macro-deck.app/reference/capability-parity/).

### See also

- [Actions](https://docs.macro-deck.app/features/actions/) - the `ActionParameter` schema both parameter lists use.
- [Variables](https://docs.macro-deck.app/features/variables/) - for state that is read rather than announced.
- [Localization](https://docs.macro-deck.app/features/localization/#the-generated-api) - where `Strings.*` comes from.
- [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities)

## Integration issues

> Source: https://docs.macro-deck.app/features/integration-issues/
>
> Report problems the user can act on with IIntegrationIssueProvider - severity, localized text, and a resolve button that can reopen setup.

An integration reports a problem the user can understand and fix - wrong endpoint, missing permission,
expired credentials - by implementing `IIntegrationIssueProvider`. Macro Deck shows it as a badge on the
integration list and a box in the integration's detail view, optionally with a button that fixes it.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Issues;

public sealed class StreamStudioIntegration : IPluginIntegration, IIntegrationIssueProvider
{
	private const string WrongEndpointIssueId = "wrong-endpoint";

	private StudioConnection? _connection;

	public Task<IReadOnlyList<IntegrationIssue>> GetIssuesAsync(CancellationToken cancellationToken = default)
	{
		IReadOnlyList<IntegrationIssue> issues = _connection?.NeedsSetup == true
			?
			[
				new IntegrationIssue
				{
					Id = WrongEndpointIssueId,
					Title = Strings.Issues.WrongEndpointTitle(),
					Description = Strings.Issues.WrongEndpointDescription(),
					Severity = IntegrationIssueSeverity.Error,
					ActionLabel = Strings.Issues.OpenSetup()
				}
			]
			: [];

		return Task.FromResult(issues);
	}

	public Task<IssueResolution> ResolveIssueAsync(string issueId, CancellationToken cancellationToken = default)
		=> Task.FromResult(issueId == WrongEndpointIssueId
			? IssueResolution.Ok(followUp: IssueResolutionFollowUp.StartConfigFlow)
			: IssueResolution.Failed(Strings.Issues.UnknownIssue()));

	// IPluginIntegration members omitted.
}
```

While the connection needs setup, the user sees a red badge and an "Open setup" button; clicking it
opens your [configuration flow](https://docs.macro-deck.app/features/setup-flows/). When `NeedsSetup` turns
false, the issue disappears on the next poll.

Things to know:

- **`GetIssuesAsync` is polled** to render badges. Return cached state; never connect, probe or block in
  it. Do the real work in `ResolveIssueAsync`.
- **Issues are for the user, logs are for you.** An issue says what is wrong and what to do; stack
  traces and retries belong in the [log](https://docs.macro-deck.app/features/logging/).
- **Only report what needs the user.** A state that recovers on its own ("the app is not running yet")
  is not an issue - expose it as a variable such as `studio_is_connected` instead.

### What an issue carries

| Property | What it does | Example |
| --- | --- | --- |
| `Id` | Stable id passed back to `ResolveIssueAsync`. Required. | `"wrong-endpoint"` |
| `Title` | Localized headline. Required. | `Strings.Issues.WrongEndpointTitle()` |
| `Description` | Localized detail: what happened and what to do. | `Strings.Issues.WrongEndpointDescription()` |
| `Severity` | `Info`, `Warning` (default) or `Error`. Colours the badge and orders the list. | `IntegrationIssueSeverity.Error` |
| `ActionLabel` | Text of the resolve button. Leave it unset for an informational issue with no button. | `Strings.Issues.OpenSetup()` |

An `Error` issue additionally raises one user notification when it first appears, linking to the
integration. It notifies again only after it has gone away and come back.

### Resolving an issue

```csharp
public async Task<IssueResolution> ResolveIssueAsync(string issueId, CancellationToken cancellationToken = default)
{
	switch (issueId)
	{
		case "reconnect":
			return await _connection.ReconnectAsync(cancellationToken)
				? IssueResolution.Ok()
				: IssueResolution.Failed(Strings.Issues.StillUnreachable());

		case "permission":
			return IssueResolution.Ok(Strings.Issues.GrantInSystemSettings());

		case "credentials-expired":
			return IssueResolution.Ok(followUp: IssueResolutionFollowUp.StartConfigFlow);

		default:
			return IssueResolution.Failed(Strings.Issues.UnknownIssue());
	}
}
```

| Result | What the user sees |
| --- | --- |
| `IssueResolution.Ok()` | The issue list refreshes. |
| `IssueResolution.Ok(message)` | A success toast with the message, then a refresh - for a fix only the user can finish. |
| `Ok(followUp: StartConfigFlow)` | Your configuration flow opens, e.g. to re-enter credentials. A message is not shown. |
| `IssueResolution.Failed(message)` | An error toast with the message, then a refresh. |

The resolve button runs `ResolveIssueAsync` and nothing else - whether the issue is gone is decided by
the next `GetIssuesAsync`, so make the fix change the state that method reads.

### Edge cases

- **Invalid ids are dropped.** An issue id must be usable as a Macro Deck resource id: no `::`,
  whitespace or control characters, at most `MacroDeckId.MaxResourceLocalIdLength` (256). The host logs
  a warning and ignores the issue.
- **The host adds its own.** When an integration fails or times out during start-up, the host shows an
  `Error` issue with a retry button for it, next to yours. Its id is reserved: an issue of yours with the
  same id is hidden.
- **A throwing `GetIssuesAsync` counts as no issues.** The host logs the exception; your badge simply
  vanishes. Return `[]` rather than throwing.
- **Disabled integrations are never asked.**

### Testing

```csharp
var issues = await harness.Issues.GetIssuesAsync();
var resolved = await harness.Issues.ResolveAsync(new IssueResolveArguments { IssueId = "wrong-endpoint" });
```

`PluginTestHarness.Issues` calls `list` and `resolve` the way the host does; the results are
`IssueListResult` and `IssueResolveResult`. See [testing](https://docs.macro-deck.app/features/testing/).

### Over the plugin protocol

Issues are one provider-shaped `issues` capability per plugin. `list` and `resolve` are always live
round trips - there is no snapshot - so an out-of-process `GetIssuesAsync` is called over the WebSocket
on every poll, which is one more reason to keep it cheap. Severity and follow-up travel as their enum
member names. See [capability parity](https://docs.macro-deck.app/reference/capability-parity/) and
[the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities).

### See also

- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - where `StartConfigFlow` sends the user.
- [Logging](https://docs.macro-deck.app/features/logging/) - for diagnostic detail.
- [Localization](https://docs.macro-deck.app/features/localization/#the-generated-api) - where `Strings.*` comes from.

## Integration storage

> Source: https://docs.macro-deck.app/features/integration-storage/
>
> Keep small text documents of your own across restarts with IIntegrationContext.Storage - keys, atomic writes, validators, unreadable documents, where the files live, backups, older hosts and testing.

`IIntegrationContext.Storage` keeps small text documents an integration owns, such as the devices it has
seen or a cache it wants back after a restart. Each document has a key; you decide its format, usually JSON.
Settings the user enters belong in [configuration entries](https://docs.macro-deck.app/features/setup-flows/) instead, and secrets in
their secret fields.

```csharp
private const string DevicesKey = "known-devices.json";

public async Task InitializeAsync(IIntegrationContext context)
{
	var read = await context.Storage.ReadAsync(DevicesKey, IsDeviceList);
	_canSave = read.Status != IntegrationStorageReadStatus.Unreadable;
	_devices = read.Content is { } json ? JsonSerializer.Deserialize<List<Device>>(json)! : [];
	_storage = context.Storage;
}

private async Task SaveAsync()
{
	if (_canSave)
	{
		await _storage.WriteAsync(DevicesKey, JsonSerializer.Serialize(_devices));
	}
}

private static bool IsDeviceList(string json)
{
	try
	{
		return JsonSerializer.Deserialize<List<Device>>(json) is not null;
	}
	catch (JsonException)
	{
		return false;
	}
}
```

### Keys

A key is 1 to 64 characters of lowercase ASCII letters, digits, `.`, `_` and `-`, starts with a letter or a
digit, and does not end in `.tmp` or `.bak`, which storage uses for its own copies. Check one with
`IntegrationStorageKeys.IsValid`; every operation throws `ArgumentException` for an invalid key. Keys are
private to your integration: another integration's `devices.json` is a different document.

### Reading and writing

| Call | What it does |
| --- | --- |
| `ReadAsync(key, isValid)` | Answers an `IntegrationStorageReadResult`: `Found` with the `Content`, `Missing` when nothing was ever stored, or `Unreadable`. |
| `WriteAsync(key, content)` | Replaces the document. `content` must not be empty; use `DeleteAsync` to remove a document. |
| `DeleteAsync(key)` | Removes the document and its copies. A missing key is not an error. |

A write never leaves a half-written document behind. It writes a temporary copy, flushes it to disk, keeps
the previous document as a backup and only then puts the new one in place. A read tries the document, then
a pending temporary copy, then the backup, and answers the first one `isValid` accepts. Without a validator
every copy that is not empty counts, so pass one whenever you can tell a damaged document apart, and keep it
free of side effects: a validator that throws rejects that copy.

`Unreadable` means copies exist but none is valid, for example after a disk error or an edit by hand. Treat
it as "do not touch": keep working with defaults, but do not write the key again in that session, or the
next write replaces the only copies the user could still recover. Storage itself never deletes or repairs
them.

### Where the documents live

- **Built into Macro Deck**: `integration-data/<integration id>/` in Macro Deck's data directory. The folder
  is part of the **Integrations** component of a [backup](https://docs.macro-deck.app/guide/backups/), so restoring it brings the
  documents back together with the integration's configuration.
- **In a plugin**: `integration-data/<plugin id>/` in the data directory the host gives the plugin
  (`PluginHostOptions.DataDirectory`, see [plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/#iintegrationcontext)).
  It survives plugin updates and rollbacks. Storage never crosses the plugin protocol, so it works the same
  on every Macro Deck version. A plugin started without a data directory, such as one run outside the
  supervisor without `MACRO_DECK_PLUGIN_DATA_DIRECTORY`, reads every key as `Missing`, and a write throws
  `InvalidOperationException`.

Documents are files, not a database: keep them small, a few hundred kilobytes at most, and write them when
something changed rather than on a timer. Calls on the same integration's storage run one at a time.

### Older hosts and other implementations

`Storage` is a default interface member. A context from a Macro Deck that predates it, and any
`IIntegrationContext` implementation that does not override it, return `UnavailableIntegrationStorage`:
every read is `Missing`, a delete does nothing and a write throws `InvalidOperationException`. Catch that
exception where saving is optional.

### Testing

`FakeIntegrationContext.Storage` is an in-memory `FakeIntegrationStorage` with the same key rules and read
outcomes. Seed a document with `Set`, make a key hold damaged copies with `SetUnreadable`, and read what the
integration wrote with `Get`:

```csharp
await using var harness = PluginTestHarness.Create(builder => builder.RegisterIntegration<MyIntegration>());
harness.Context.Storage.SetUnreadable("known-devices.json");

await harness.InitializeIntegrationsAsync();

Assert.That(harness.Context.Storage.Get("known-devices.json"), Is.Null);
```

### See also

- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - settings and secrets the user enters.
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - the plugin data directory.
- [Capability parity](https://docs.macro-deck.app/reference/capability-parity/) - how storage differs between built-in integrations and plugins.

## Layout providers

> Source: https://docs.macro-deck.app/features/layouts/
>
> Describe a device's surface with ILayoutProvider - regions, grid geometry and rendering ability - and point devices at it.

A layout provider describes what a device or client surface **is** - its regions, their geometry and what
they can render - never what is on it. Macro Deck uses a registered layout to constrain a profile to real
hardware, so hardware support lives entirely in your plugin with no device-specific code in Macro Deck.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Devices;
using MacroDeck.Sdk.Layouts;

public sealed class MacroPadIntegration : IPluginIntegration, ILayoutProvider, IDeviceProvider
{
	private string? _layoutId;

	public string ProviderName => "Macro Pad";

	public async Task InitializeAsync(ILayoutProviderContext context, CancellationToken cancellationToken = default)
	{
		var registration = await context.RegisterLayoutAsync(
			new LayoutDescriptor(
				"pad-3x2",
				"Macro Pad",
				Regions:
				[
					new LayoutRegion
					{
						Id = "keys",
						Kind = LayoutRegionKinds.Grid,
						Grid = new LayoutGrid { Rows = 2, Columns = 3, KeySize = new LayoutKeySize(72, 72) }
					}
				],
				Capabilities: new LayoutCapabilities
				{
					Visuals = new LayoutVisualCapabilities
					{
						StaticIcons = true, BackgroundColors = true, TextLabels = true
					}
				}),
			cancellationToken);

		_layoutId = registration.LayoutId;
	}

	public async Task InitializeAsync(IDeviceProviderContext context, CancellationToken cancellationToken = default)
	{
		await context.RegisterDeviceAsync(
			new DeviceDescriptor("SERIAL-1", "Macro Pad", LayoutReference: _layoutId),
			cancellationToken);
	}

	public Task ShutdownAsync(CancellationToken cancellationToken = default) => Task.CompletedTask;

	// IPluginIntegration members omitted.
}
```

A profile that is the startup profile of this pad is now locked to 2x3 in the editor, and its spacing and
corner-radius controls are disabled because the layout does not claim them.

Things to know:

- **Register the layout, then use the id it returns.** `LayoutRegistration.LayoutId` is the qualified
  `your.plugin.id::pad-3x2`; that is what `DeviceDescriptor.LayoutReference` must carry.
- **Layouts start before devices.** In a plugin the host initializes `ILayoutProvider` before
  `IDeviceProvider`, both after the integration's own `InitializeAsync`, so `_layoutId` is set in time.
- **There is no `ILayoutProvider.ShutdownAsync`.** Release what you acquired in the integration's own
  `ShutdownAsync`; the host withdraws your layouts when the integration stops.
- **Every visual flag defaults to `false`.** Declare what the surface can actually render.

### Registering a layout

| `ILayoutProviderContext` member | What it does |
| --- | --- |
| `RegisterLayoutAsync` | Registers a layout, or replaces the one under the same provider-local id. Devices referencing it pick up the new descriptor without re-registering. Returns `LayoutRegistration(LayoutId, ProviderId)`. |
| `UnregisterLayoutAsync` | Withdraws a layout by provider-local id. Unknown ids are ignored. |

`RegisterLayoutAsync` throws `ArgumentException` when the id or name is empty, or a region id is empty or
repeated within the layout. The context is safe to keep while the provider runs.

Implement `GetLayouts()` to return what you currently offer; the host reads it to recover its view after a
reconnect. The default returns an empty list. `ProviderName` is optional and falls back to the
integration's name - for a plugin, the `manifest.json` name.

### Id grammar

```text
you register     LayoutDescriptor.Id          "pad-3x2"
host returns     LayoutRegistration.LayoutId  "com.example.macropad::pad-3x2"
device carries   LayoutReference              "com.example.macropad::pad-3x2"
```

`LayoutDescriptor.Id` is provider-local, stable across restarts and unique within your provider - a model
name, not a per-device serial. Never build the qualified string yourself; read it back from the
registration. The prefix is always the authenticated provider's own id, so no plugin can register a layout
into another owner's namespace.

### Declaring regions

```text
+----+----+----+----+
| k  | k  | k  | k  |   "keys"    grid 2x4
+----+----+----+----+
| k  | k  | k  | k  |
+----+----+----+----+
|    touch strip    |   "strip"   touch-strip
+-------------------+
 (o)  (o)  (o)  (o)     "dials"   encoder x4
```

```csharp
Regions:
[
	new LayoutRegion
	{
		Id = "keys", Kind = LayoutRegionKinds.Grid,
		Grid = new LayoutGrid { Rows = 2, Columns = 4, KeySize = new LayoutKeySize(120, 120) }
	},
	new LayoutRegion { Id = "strip", Kind = LayoutRegionKinds.TouchStrip, Count = 1 },
	new LayoutRegion { Id = "dials", Kind = LayoutRegionKinds.Encoder, Count = 4, Name = "Dials" }
]
```

`Kind` is one of `LayoutRegionKinds` - `grid`, `button`, `encoder`, `touch-strip`, `pedal` - but it is an
**open string**: an unknown kind round-trips intact with its `Id`, `Name`, `Count` and `Extra`, so an older
host carries it without dropping the rest of the layout.

Only `grid` carries geometry, in `LayoutRegion.Grid`. Every other kind is a `Count`.

| `LayoutGrid` member | Meaning |
| --- | --- |
| `Rows`, `Columns` | The size right now. On a fixed grid, Macro Deck holds a profile edited for this layout to exactly these. |
| `IsConfigurable` | The user may pick another size. `false` (default) ignores the bounds below. |
| `MinRows`, `MaxRows`, `MinColumns`, `MaxColumns` | Per-axis bounds for a configurable grid. Default 1. |
| `SupportsRuntimeResize` | A resize applies live. When `false`, you may apply it when the device next connects. |
| `KeySize` | Pixel size of one key, where the hardware has a fixed one. |
| `RowsLocked`, `ColumnsLocked` | Derived: fixed, or configurable with min >= max on that axis. |

`LayoutDescriptor.PrimaryGrid` is the one grid Macro Deck renders a deck onto, computed for you. It is null
when the layout has no grid region (a pedal board) or more than one - Macro Deck does not guess.

### Declaring what the surface renders

```csharp
Capabilities: new LayoutCapabilities
{
	Visuals = new LayoutVisualCapabilities
	{
		StaticIcons = true, TextLabels = true, BackgroundColors = true, MaxUpdatesPerSecond = 10
	}
}
```

| `LayoutVisualCapabilities` | Meaning |
| --- | --- |
| `StaticIcons`, `AnimatedIcons`, `Borders`, `BackgroundColors`, `TextLabels`, `Transparency` | What the surface can draw. |
| `WidgetSpacing`, `CornerRadius` | Whether the folder's spacing and corner radius mean anything here. `false` disables those editor controls with a note that they have no effect on this device. |
| `CustomFolderViews` | Whether the surface can show a [folder view](https://docs.macro-deck.app/ui/views/folder-views/) at all. `false` means the choice is not offered for a profile its device claims. Set it on a software client or full display. |
| `MaxUpdatesPerSecond` | Advisory update rate. |

`LayoutVisualCapabilities.Full` sets every flag. A `Visuals` block that sets nothing reads as "renders
nothing". **No `Visuals` block at all** keeps the spacing controls and the folder-view option - saying
nothing is not saying no. A region can override with its own `LayoutRegion.Visuals`; null inherits the
layout's.

### Associating a layout with a device provider

```csharp
new DeviceDescriptor(serial, "Macro Pad", LayoutReference: "com.other.plugin::pad-3x2")
```

A device points at a layout through `DeviceDescriptor.LayoutReference` - see
[device providers](https://docs.macro-deck.app/features/devices/#capabilities-and-layouts). The layout's provider need not be the
device's: a device may reference another plugin's layout. A layout is descriptive metadata, and referencing
one grants nothing over its owner. An unresolvable reference is never an error - the device registers, and
its profile stays unconstrained until that layout appears.

### What happens to profiles

| Startup-profile devices resolve to | Profile |
| --- | --- |
| Exactly one distinct rows x columns pair (one device, or several sharing a layout) | Locked to that grid. |
| Different pairs | Editable, with a warning naming the disagreeing devices. |
| A layout with no `PrimaryGrid` | Not constrained. |

Macro Deck constrains a profile; it never rewrites one. No reflow, pagination, resizing or dropped widgets:
a profile bigger than the device simply shows partially, as a [device session](https://docs.macro-deck.app/features/devices/#receiving-and-rendering-a-session)
does.

The host persists the last resolved layout with the device, not just the reference. `UnregisterLayoutAsync`
and a stopped provider behave the same: the reference is kept, the grid stays constrained, and it refreshes
when the layout is registered again.

### In a plugin

Declare the `layout-provider` capability and `host:layouts` in [`manifest.json`](https://docs.macro-deck.app/reference/manifest/).
`MacroDeck.Plugin.Hosting` starts the provider once the plugin is connected and its integration has
initialized, and stops it on shutdown. The provider is always the authenticated plugin, which keeps the id
grammar true across the wire. See [Capability parity](https://docs.macro-deck.app/reference/capability-parity/).

### Testing

```csharp
using MacroDeck.Plugin.Testing.Fakes;
using MacroDeck.Sdk.Layouts;

[Test]
public async Task The_pad_declares_one_fixed_2x3_grid()
{
	var context = new FakeLayoutProviderContext();

	await new MacroPadIntegration().InitializeAsync(context);

	var grid = context.Layouts["pad-3x2"].PrimaryGrid!.Grid!;
	Assert.Multiple(() =>
	{
		Assert.That((grid.Rows, grid.Columns), Is.EqualTo((2, 3)));
		Assert.That(grid.RowsLocked && grid.ColumnsLocked, Is.True);
	});
}
```

`FakeLayoutProviderContext` keeps the host's rules: re-registering an id replaces it, unregistering an
unknown id is a no-op, and an empty id or name or an empty or repeated region id throws. Assert on
`Layouts` (keyed by local id) and `Calls`. The fake returns the **local** id as `LayoutRegistration.LayoutId`,
not a qualified one, so do not assert on the `::` form.

Against a real plugin process, the harness's `LayoutProvider` client invokes `describe` (`DescribeAsync`)
and `layouts` (`GetLayoutsAsync`). See [Testing](https://docs.macro-deck.app/features/testing/).

### Over the plugin protocol

The host-to-provider direction of the `layout-provider` capability only describes the provider and re-reads
its catalogue after a reconnect:

| Operation | Purpose |
| --- | --- |
| `describe` | The provider's declared name. |
| `layouts` | The provider's current layout catalogue, re-read after a reconnect. |

Registering and withdrawing travel the other way as the `layouts` host API:

| Operation | Purpose |
| --- | --- |
| `register` | Registers a layout, or replaces one already registered under the same provider-local id. |
| `unregister` | Withdraws a layout. Devices still referencing it keep their last-resolved geometry rather than losing their constraint. |

### See also

- [Device providers](https://docs.macro-deck.app/features/devices/) - registering the devices that reference a layout.
- [Folder views](https://docs.macro-deck.app/ui/views/folder-views/) - what `CustomFolderViews` gates.
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/) - how widgets size within a grid.
- [Capability parity](https://docs.macro-deck.app/reference/capability-parity/) - plugin-specific behaviour.

## Localization

> Source: https://docs.macro-deck.app/features/localization/
>
> Translate a plugin with Localization/*.resx - the generated Strings class, placeholders, plurals, fallback, and the MDLOC diagnostics.

You write `Localization/Strings.resx` plus one `Strings.<culture>.resx` per language. The build turns them
into a typed `Strings` class whose members return a `LocalizedString`, and you assign that anywhere the SDK
takes `LocalizedText`. The host resolves it in the reader's language.

### Quick start

`Localization/Strings.resx` - the default language:

```xml
<data name="Actions.LogMessage.Name" xml:space="preserve">
  <value>Write log message</value>
</data>
<data name="Actions.LogMessage.Message.Label" xml:space="preserve">
  <value>Message</value>
</data>
```

`Localization/Strings.de.resx` - German:

```xml
<data name="Actions.LogMessage.Name" xml:space="preserve">
  <value>Log-Nachricht schreiben</value>
</data>
```

The project references the generator and the runtime package (the plugin template already does this):

```xml
<PackageReference Include="MacroDeck.Plugin.Analyzers" PrivateAssets="all" />
<PackageReference Include="MacroDeck.Localization" />
```

Use the generated members:

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

public sealed class LogMessageAction : IActionDefinition
{
	public string Id => "log-message";

	public LocalizedText Name => Strings.Actions.LogMessage.Name();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Text("message", label: Strings.Actions.LogMessage.Message.Label(), required: true),
	];

	// Other members omitted.
}
```

A German reader sees **Log-Nachricht schreiben**; everyone else sees **Write log message**. The label has
no German entry, so German readers get **Message**.

- **The folder and base name matter.** The analyzer globs `Localization/**/*.resx`, and the base name
  `Strings` becomes the class name.
- **`Strings.resx` is always required**, even for a one-language plugin: every translation is checked
  against it, and the fallback chain ends there.
- **A dotted key is a nested class.** `Actions.LogMessage.Name` becomes `Strings.Actions.LogMessage.Name()`.
- **A translation may leave keys out.** A missing key falls back - see
  [Choosing the language](#choosing-the-language).

### Placeholders

```xml
<data name="Status.ConnectedAs" xml:space="preserve">
  <value>Connected as {userName}</value>
</data>
<data name="Status.Retries" xml:space="preserve">
  <value>Retry {attempt} of {limit}</value>
  <comment>[attempt:int][limit:int] Shown while reconnecting.</comment>
</data>
```

```csharp
Strings.Status.ConnectedAs(userName: connection.User);  // Connected as manuel
Strings.Status.Retries(attempt: 2, limit: 5);           // Retry 2 of 5
```

- A placeholder is a bare name in braces, matched by name, not position - a translation may reorder them.
- Parameters come from the **default-language** template only. A translation must use exactly the same
  names ([MDLOC002](#mdloc002)).
- An undeclared placeholder is `LocalizedText`, so a string literal works and a `Strings.*` member can be
  nested - it resolves in the same language as the outer sentence.
- Declare a narrower type as a bracketed prefix on `<comment>`: `string`, `int`, `long`, `double` or
  `bool`. The rest of the comment stays a translator note. A bad type, or a type for a placeholder the
  template does not use, is [MDLOC004](#mdloc004).
- Values are formatted culture-invariantly: no thousands separators, `.` as decimal point, lowercase
  booleans.
- `{{` and `}}` escape to one brace. So a value written as `{{ vars.x }}` reaches the user as `{ vars.x }`.
- A placeholder that gets no value stays literal in the output (`{deviceName}`), not blank.

### Plurals

```xml
<data name="Status.Scenes.One" xml:space="preserve">
  <value>{count} scene</value>
  <comment>[plural]</comment>
</data>
<data name="Status.Scenes.Other" xml:space="preserve">
  <value>{count} scenes</value>
  <comment>[plural]</comment>
</data>
```

```csharp
Strings.Status.Scenes(3);  // one member at the base key, count first
```

| count | en | de (`eine Szene` / `{count} Szenen`) |
| --- | --- | --- |
| `1` | 1 scene | eine Szene |
| `0` | 0 scenes | 0 Szenen |
| `3` | 3 scenes | 3 Szenen |

- **Mark every form** with `[plural]`, not just one. Plural is opt-in, so keys that just happen to end in
  `.One`/`.Other` stay ordinary members.
- `Other` is required and `One` optional. A missing `Other`, a marked key not ending in `One`/`Other`, or a
  base key an ordinary entry already owns is [MDLOC007](#mdloc007).
- A form may leave `{count}` out of its text (`eine Szene`). `count` is always a parameter, and each form
  is checked against the family's placeholders, not the other form's.
- The reference carries the base key (`Status.Scenes`). The reader's side picks the form, and picks it
  again after a language change.

#### Only `One` and `Other`

The rule is `count == 1` for every culture. It is not CLDR: the host, the Angular clients and the
bootstrapper must all pick the same form. The rule is exact for English, German, Italian, Spanish, French,
Dutch and Turkish. Chinese, Japanese, Korean and Indonesian have no plural forms, so `One` and `Other` carry
the same wording. Czech, Polish, Russian, Ukrainian and Arabic need `few`/`many` (and for Arabic `zero`/`two`)
forms that this model does not have, and Brazilian Portuguese and Hindi treat `0` like `1`. For those,
phrase `Other` so that it avoids noun-count agreement: use a count-agnostic label rather than a declined
noun. A language that cannot be phrased that way needs the closed set of forms extended first.

### Adding a language

```
Localization/
  Strings.resx            # default language (manifest: en)
  Strings.de.resx         # German
  Strings.pt-BR.resx      # Portuguese, Brazil
  Strings.zh-Hant-TW.resx # Traditional Chinese, Taiwan
```

- The suffix must be a well-formed BCP-47 name. The check is on its shape, not on whether .NET knows the
  culture, so `Strings.de_DE.resx` fails with [MDLOC005](#mdloc005).
- Every key in a translation must also exist in `Strings.resx` ([MDLOC001](#mdloc001)).
- Nothing else to register - the next build compiles the culture into the generated catalog and adds it to
  the manifest's [`languages`](#the-manifest-languages-field).

### Reuse `MacroDeckStrings` instead of duplicating common strings

```csharp
new UiHeading { Key = "confirm", Text = MacroDeckStrings.Common.Save() };

// "{field} is required" with your own label nested in it
ActionResult.Failed(ActionErrorCodes.InvalidParameter,
	MacroDeckStrings.Validation.Required(Strings.Actions.LogMessage.Message.Label()));
```

Macro Deck ships a reusable catalog, generated the same way into `MacroDeckStrings` and already translated
into every language the app carries: `Common.*` (`Save`, `Cancel`, `Delete`, `Retry`, ...), `States.*`
(`On`, `Off`, `Muted`, `Active`, ...), `Validation.*` and more. Use it for anything generic rather than
adding your own `Save` key. Its entries live in scope `macrodeck`, not `plugin:<your-id>`.

That catalog is a published contract: keys are only ever added. A retired key is marked, not deleted - it
still compiles and resolves, and [MDLOC006](#mdloc006) points to the replacement.

### Localized text in results, issues and flows

```csharp
ActionResult.Failed(ActionErrorCodes.InvalidParameter, Strings.Errors.MissingMessage());
VariableWriteResult.Unavailable(Strings.Errors.NotConnected());
IssueResolution.Failed(Strings.Issues.TokenExpired());

ConfigFlowResult.Complete(title: "Studio PC");  // plain string - not localized
```

Every user-facing SDK member typed `LocalizedText` takes a `Strings.*` member: action and parameter text,
event and issue descriptors, result messages, config-flow text, UI trees. `LocalizedText` also takes a
plain string for text that is already final, such as a device name. A `LocalizedString` does not convert to
`string` - assigning one to a `string` is a compile error.

`ConfigFlowResult.Complete`'s title is the one deliberate exception. The host stores it as the configured
entry's name, which the user can rename. Write it in your default language.

### Choosing the language

The host holds one active language, the one set in Macro Deck. There is no per-client culture, and a plugin
never asks for it. The host resolves each reference by trying the cultures in this order:

| step | `de-AT` reader, plugin default `en` |
| --- | --- |
| 1. requested culture | `de-AT` |
| 2. its neutral culture | `de` |
| 3. the catalog's default language | `en` |
| 4. Macro Deck's default | `en` (duplicate, collapsed) |

A Traditional Chinese request - script `Hant`, or region `TW`, `HK` or `MO` without a script - tries
`zh-Hant` and then `zh-TW` right after the requested culture, before the neutral `zh`. So a `zh-HK` reader
gets your `zh-Hant` or `zh-TW` catalog when you ship one, and your `zh` catalog otherwise. No other regional
culture falls back sideways: a `pt-PT` reader does not reach a `pt-BR` catalog.

A key that no culture carries renders as `[[scope:Key]]`, never blank - for example
`[[plugin:com.example.demo:Status.Scenes]]`. You see this when a key was removed by an update, or when the
plugin's catalog has not reached the host yet.

Against a host older than protocol v3, the SDK resolves descriptor text (action names, labels) in your
default language before sending it. You do not need to handle this case.

### Formatting a time of day

Text you build yourself, such as "Resumes at 3:05 PM" in an issue description, should use the time format
the user chose in Macro Deck, not the culture of your process. Ask `context.Locale` for it each time you
build the text, because the user can change the language, the time format setting or the operating system
clock at any time:

```csharp
var format = await context.Locale.GetTimeOfDayFormatAsync();
var text = Strings.Issues.ResumesAt(time: format.Format(TimeOnly.FromDateTime(resumesAt.LocalDateTime)));
```

`TimeOfDayFormat` (`MacroDeck.Sdk.Locale`) carries the `Culture` of the Macro Deck interface and the
`HourCycle`, `HourCycles.H12` or `HourCycles.H23`: the user's 12-hour or 24-hour setting, or the operating
system's when the setting follows the system. `Format` writes the culture's short time pattern in that hour
cycle; a 12-hour clock in a culture without AM/PM designators is written as `h:mm tt` in the invariant
culture.

A plugin's call crosses as `locale`/`time-of-day-format`. A Macro Deck that predates it, and a context that
does not implement `Locale`, answer the process's current culture with a 24-hour clock. In tests, set
`FakeIntegrationContext.Locale.TimeOfDayFormat`. Times inside your own UI trees need none of this: the
[time component](https://docs.macro-deck.app/ui/components/time/) already follows the reader's language and hour cycle.

### Testing translations

```csharp
using MacroDeck.Localization;

[Test]
public void German_readers_see_german_text()
{
	var registry = new LocalizationCatalogRegistry();
	registry.Register(Strings.LocalizationCatalog);
	registry.Register(MacroDeckStrings.LocalizationCatalog);
	var resolver = new LocalizationResolver(registry);

	Assert.That(resolver.Resolve(Strings.Status.ConnectedAs("manuel"), "de"), Is.EqualTo("Verbunden als manuel"));
	Assert.That(resolver.Resolve(Strings.Status.Scenes(1), "de"), Is.EqualTo("eine Szene"));
	Assert.That(resolver.Resolve(Strings.Status.Scenes(3), "fr"), Is.EqualTo("3 scenes")); // falls back
}
```

Structural mistakes - a missing default key, mismatched placeholders, a broken plural family - are already
build diagnostics, so test the wording that matters, not every key.

For bulk editing, [Rider's Localization
Manager](https://www.jetbrains.com/help/rider/Localizing_Applications.html) shows every key against every
culture in one grid, highlights missing translations, renames a key across all files, and round-trips CSV for
translators. The files are plain `.resx`, so any tool works.

### The manifest `languages` field

```json
"languages": ["en", "de", "pt-BR", "zh-Hant-TW"]
```

`macrodeck-plugin build` and `pack` derive [`languages`](https://docs.macro-deck.app/reference/manifest/#languages) from the resource
set - you do not maintain it.

- An unsuffixed `Strings.resx` contributes `en`; each `Strings.<culture>.resx` contributes its culture,
  whole (`zh-Hans` and `zh-Hant` are never shortened to `zh`).
- A suffix that fails [MDLOC005](#mdloc005) never reaches the manifest.
- A hand-written `languages` is only carried through when packing a payload directory with no
  `Localization/` folder. Culture files are compiled into the generated catalog, not into satellite
  assemblies, so the built output has nothing left to read. If both exist and disagree, the resource files
  win and `pack` reports what it replaced.

### Reference

#### The generated API

| resx | generated member |
| --- | --- |
| `Connect` | `static LocalizedString Connect()` |
| `Status.ConnectedAs` = `Connected as {userName}` | `Status.ConnectedAs(LocalizedText userName)` |
| `Status.Retries`, comment `[attempt:int][limit:int]` | `Status.Retries(int attempt, int limit)` |
| `Status.Scenes.One` / `.Other`, comment `[plural]` | `Status.Scenes(int count)` |
| (class) | `Strings.LocalizationScope` = `"plugin:<manifest id>"` |
| (class) | `Strings.LocalizationCatalog` - the compiled `ILocalizationCatalog` |

`Strings` is a `public static partial class` in your project. It returns a reference, not text, so a
language change never requires rebuilding your UI.

| MSBuild property | default |
| --- | --- |
| `MacroDeckLocalizationScope` | `plugin:<id>`, read from `manifest.json` |
| `MacroDeckLocalizationClassName` | the resource base name, `Strings` |

A plugin owns only `plugin:<its-own-id>`, so it cannot overwrite Macro Deck's catalog or another plugin's.

#### Comment prefixes

| prefix | meaning |
| --- | --- |
| `[name:type]` | Placeholder type: `string`, `int`, `long`, `double`, `bool`. |
| `[plural]` | This entry is one form of a plural family. On every form. |
| `[removed:guidance]` | Retired key: still generated and resolvable, reports [MDLOC006](#mdloc006). |

#### Diagnostics

All reported by the generator that produces `Strings`. None fire without a `Localization/*.resx`.

##### MDLOC001

A key is in a translation but not in `Strings.resx`. Add it to the default file, or remove it from the
translation.

##### MDLOC002

A translation's placeholder names differ from the default language's. Use exactly the same names; order
does not matter.

##### MDLOC003

The same key is declared twice in one file. Rename or delete one.

##### MDLOC004

A declared placeholder type is not `string`, `int`, `long`, `double` or `bool`, or it names a placeholder
the template does not use.

##### MDLOC005

A file's culture suffix is not a well-formed BCP-47 name (`Strings.de_DE.resx`). Rename it, for example to
`de-DE`.

##### MDLOC006

Code uses a `MacroDeckStrings` key retired with `[removed:...]`. Move to the replacement the message names;
see [deprecations](https://docs.macro-deck.app/policies/deprecations/).

```xml
<data name="Common.Submit" xml:space="preserve">
  <value>Submit</value>
  <comment>[removed:Use Common.Save instead.] Retired in 3.1.</comment>
</data>
```

##### MDLOC007

A plural family cannot produce a member: a marked key not ending in `One`/`Other`, no `Other` form, or a
base key an ordinary entry already owns.

##### MDLOC008

A key is also a group other keys nest under (`Filters` beside `Filters.Date`), so it would generate a
method and a class with the same name. Rename one, for example to `FiltersHeading`.

### See also

- [SDK packages](https://docs.macro-deck.app/reference/sdk-packages/) - the `MacroDeck.Localization` package.
- [Analyzers](https://docs.macro-deck.app/reference/analyzers/) - the MDLOC table alongside every other diagnostic.
- [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities) - the `localization` capability kind a remote
  plugin uses to hand its catalog to the host.
- [Theming](https://docs.macro-deck.app/ui/concepts/theming/) - `UiText` and where a view accepts a `LocalizedString`.
- [Manifest reference](https://docs.macro-deck.app/reference/manifest/#languages) - the `languages` field.
- [Compatibility policy](https://docs.macro-deck.app/policies/compatibility/) - what is frozen about localization.

## Logging and health

> Source: https://docs.macro-deck.app/features/logging/
>
> Log with Serilog or ILogger and read the lines in the host's log files and log viewer; what the health endpoints answer and what happens at shutdown.

A plugin logs the normal .NET way. `UseMacroDeckLogging()` forwards every line to the host, where it
lands in the same log files and log viewer as the host's own entries.

### Quick start

```csharp
// Program.cs
var plugin = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<PluginIntegration>()
	.Build();

await plugin.RunAsync();

// PluginIntegration.cs
using Serilog;

public sealed class PluginIntegration(ILogger logger) : IPluginIntegration
{
	private readonly ILogger _logger = logger.ForContext<PluginIntegration>();

	public IReadOnlyList<IActionDefinition> Actions => [];

	public async Task InitializeAsync(IIntegrationContext context)
	{
		try
		{
			var bridge = await HueBridge.ConnectAsync();
			_logger.Information("Connected to {Bridge} with {LightCount} lights", bridge.Name, bridge.Lights.Count);
		}
		catch (HttpRequestException exception)
		{
			_logger.Warning(exception, "Bridge not reachable, retrying in the background");
		}
	}

	public Task ShutdownAsync() => Task.CompletedTask;
}
```

Both lines appear in the host's log file and in the **Logs** tab of the Developer page, attributed to
your plugin, within a few seconds (the plugin flushes every 2 seconds, the viewer tails the file).

- **Any logger works.** An injected Serilog `ILogger`, `ILogger<T>`, the static `Log` API and
  `MacroDeck.Sdk.Logging.IntegrationLog` all route through the same pipeline. The project template
  already calls `UseMacroDeckLogging()`.
- **The host's log files are the only log history.** There is no separate plugin log file.
- **What a user can send you** is the day's log file (see [where the lines end up](#where-the-lines-end-up))
  or entries copied from the log viewer, filtered to your plugin.
- **Lines also go to the console**, so they show in your IDE's run window and in
  [`macrodeck-plugin run`](https://docs.macro-deck.app/cli/run/). Do not add `WriteTo.Console(...)`: every line would print twice.

### Where the lines end up

```text
2026-08-06 10:11:12.345 +02:00 [WRN] [Integration/app.macro-deck.spotify/SpotifyClient] message
```

The host rebuilds each forwarded event as a Serilog event and writes it into its own pipeline: the same
redaction, the same rolling file, the same viewer filters as an in-process integration. "Filter by
plugin" and "filter by integration" are the same filter.

| | Location |
| --- | --- |
| Host log files | `<data directory>/logs/host-<date>.log`, one file per day, 14 kept |
| Data directory, Windows | `%APPDATA%\MacroDeck` |
| Data directory, macOS | `~/Library/Application Support/MacroDeck` |
| Data directory, Linux | `$XDG_DATA_HOME/MacroDeck`, or `~/.local/share/MacroDeck` |
| Log viewer | Developer page, **Logs** tab: every retained day, filterable by level, source and integration |

Newlines inside a message are escaped, so one entry is always one header line.

### Levels and what goes where

```json
{
  "MacroDeck": {
    "Plugin": {
      "Logging": { "MinimumLevel": "Debug" }
    }
  }
}
```

`MinimumLevel` (in `appsettings.json` or any other configuration source) decides what is forwarded
**to the host**. It is independent of the pipeline's own minimum, so a `Debug` line can reach a local file
sink without reaching the host:

```csharp
.UseMacroDeckLogging(cfg => cfg
	.MinimumLevel.Debug()
	.WriteTo.File("plugin.log"))
```

The callback runs **before** the Macro Deck sink is attached, so every Serilog feature works as usual.
Calling `UseMacroDeckLogging` twice is a no-op.

| Level | Use it for |
| --- | --- |
| `Verbose`, `Debug` | Detail for you while developing. Not forwarded by default. |
| `Information` | Things a user would want to see happened: connected, configured, reloaded. |
| `Warning` | Something failed and you recovered or will retry. |
| `Error`, `Fatal` | An operation failed for good, or the plugin is giving up. |

`Warning` and above are never dropped to make room for informational noise.

### Request lines are not logged

The categories that log a line per request start at `Warning`, the same way the host quiets its own request
logging, so the host's health polls and other successful requests do not fill the console and the log viewer:

- `Microsoft.AspNetCore.Hosting.Diagnostics`: `Request starting` and `Request finished`, for every request to
  the plugin, including `/_macrodeck/health`.
- `Microsoft.AspNetCore.Routing.EndpointMiddleware`, `Microsoft.AspNetCore.Http.Result`,
  `Microsoft.AspNetCore.Mvc`, `Microsoft.AspNetCore.Cors.Infrastructure.CorsService` and
  `Microsoft.AspNetCore.StaticFiles`: the endpoint, result and middleware lines of each request.
- `System.Net.Http.HttpClient`: the request and response lines of every `HttpClient` created through
  `IHttpClientFactory`, including the SDK's own calls to the host and your own.

This drops every `Information` line of these categories, not only the `200` ones, so a `404` or a `500` that
did not throw is not logged either. An unhandled exception is still logged at `Error`, and other ASP.NET
categories such as Kestrel or authentication are not affected. To log your own HTTP calls, write the line
yourself.

A lower global minimum does not bring them back, because a category setting is more specific. Override the
category in the callback:

```csharp
.UseMacroDeckLogging(cfg => cfg
	.MinimumLevel.Override("Microsoft.AspNetCore.Hosting.Diagnostics", LogEventLevel.Information))
```

There is no configuration key for this: `MinimumLevel` under `MacroDeck:Plugin:Logging` only decides what
is forwarded to the host.

### Structured properties

```csharp
_logger.Information("Set {Light} to {Brightness} %", light, brightness);
```

Use message templates, not string interpolation: the host shows the rendered message and a live reader
can still filter on properties. Know the limits:

- Properties travel as a flat string-to-string map and **are not written to the log files**, for host and
  plugin lines alike. Do not build a feature on them.
- The rendered message is literal text. A `{Foo}` inside it is never re-parsed on the host.
- Identity is added by the host from the authenticated session. Nothing identifying your plugin is sent,
  and a plugin-supplied property that would collide with it is filtered out, so you cannot log under
  another integration's name.

### Never log secrets

```csharp
_logger.Information("Authenticated as {User}", account.DisplayName); // not the token
```

The host redacts every event once, before any sink, to `***`: values of sensitive keys (`password`,
`token`, `secret`, `api_key`, `authorization`, `client_secret` and similar) in `key=value` or `"key": value`
form, credentials in URLs (`https://user:pass@`), `Bearer`/`Basic`/`Digest` credentials, JWTs and PEM
private keys. That is a safety net, not a licence: a secret in an unrecognised shape is written as-is into
a file users attach to bug reports.

### When the host is unreachable

Logging never blocks. A log call returns immediately, even with no connection.

- `log.publish` has **no acknowledgement and no replay**. A batch the host never received is gone.
- While the host is unreachable, undelivered batches are written to
  `<state directory>/<plugin id>/logs/plugin-fallback.log`. It wraps when full, so a long outage ends with
  the newest entries, and is cleared once the connection works again. It is never sent to the host.
- The default state directory is `%LOCALAPPDATA%\MacroDeck\plugins` on Windows,
  `~/Library/Application Support/MacroDeck/plugins` on macOS and `$XDG_STATE_HOME/macro-deck/plugins`
  (or `~/.local/state/macro-deck/plugins`) on Linux.
- Past the queue capacity, events are dropped, not buffered without bound.

#### Options

Bound from `MacroDeck:Plugin:Logging`:

| Option | Default | What it does |
| --- | --- | --- |
| `MinimumLevel` | `Information` | Minimum level forwarded to the host. |
| `BatchSize` | 64 | Events per `log.publish` batch. Capped at the protocol limit, so only smaller works. |
| `FlushInterval` | 2 seconds | How often a partial batch is sent. |
| `QueueCapacity` | 2000 | Total across the two internal queues (warning and above, everything else). |
| `EnableFallbackFile` | `true` | Write undelivered batches to the fallback file. |
| `FallbackFileMaxBytes` | 1 MiB | Hard cap on that file. |

#### Ingestion limits

The host bounds `log.publish` whatever the plugin sends:

| Limit | Value |
| --- | --- |
| Events per batch | 64 |
| Message length | 4096 characters |
| Properties per event | 32 |
| Property name / value length | 64 / 512 characters |
| Source context length | 128 characters |
| Exception length / nesting depth | 8192 characters / 5 |
| Inbound log queue depth | 256 |
| Events per second, and burst | 20, with a burst of 500 |

The rate limit is keyed **per plugin id, not per session**: reconnecting does not reset it, and a
plugin that crashes and restarts inherits the budget its predecessor left. Logs use their own inbound
queue, separate from capability traffic; excess events are dropped without closing the session.

### Health

```bash
curl http://127.0.0.1:<port>/_macrodeck/ready
```

The SDK serves four routes in your plugin's web application. You do not implement them.

| Route | Answers |
| --- | --- |
| `GET /_macrodeck/health` | Liveness, from the moment the process serves - before startup finishes or a session opens. |
| `GET /_macrodeck/ready` | 200 once a session is open, 503 before. |
| `GET /_macrodeck/info` | Id, name, version, registration mode, protocol version. |
| `GET /_macrodeck/diagnostics` | Connection state, reconnect attempt, in-flight invocations. |

`/_macrodeck` is reserved: mapping your own route under it fails `Build()`, and middleware that tries to
answer one never sees the request. The supervisor probes `/_macrodeck/health`.

#### Tuning the probe

In [`manifest.json`](https://docs.macro-deck.app/reference/manifest/#timing-settings); out-of-range values are clamped, not rejected:

| Setting | Default | Clamped to |
| --- | --- | --- |
| `health.path` | `/_macrodeck/health` | - |
| `health.intervalSeconds` | 15 | 5-120 |
| `health.timeoutSeconds` | 2 | 1-10 |
| `health.unhealthyThreshold` | 3 | 2-10 |

The floor of 2 means a single missed probe never restarts a plugin.

#### Never override your own listener URL

The supervisor binds a loopback port **before** your process starts and passes it as `ASPNETCORE_URLS`.
Setting your own URL in `appsettings.json`, a launch profile or `UseUrls` makes the plugin listen where
nobody probes: the health check fails silently and permanently, because a wrong port and a hung process
look the same. [MDP4002](https://docs.macro-deck.app/reference/analyzers/#mdp4002) catches the statically visible cases.

#### When health matters

- **Activation.** Unless the caller opted out of starting it, activating a version starts the plugin and
  waits for it to be healthy. If it is not, activation is undone: the previous version is restored, the
  failed one deleted, and the previous one restarted.
- **Steady state.** Consecutive failures past `unhealthyThreshold` mark the plugin unhealthy and the
  supervisor restarts it, within a restart budget. A plugin that keeps failing ends in a terminal failed
  state rather than restarting forever.

### Shutdown

The sequence - `session.goodbye`, a `4004` close, the manifest's grace period, then a process-tree kill -
is in [what to expect at shutdown](https://docs.macro-deck.app/reference/plugin-hosting/#what-to-expect-at-shutdown). For logging it
means:

- **Log final messages early.** The shipper flushes on an interval and `log.publish` has no
  acknowledgement, so a line written just before exit may never arrive. The fallback file is not replayed.
- **A hard kill takes queued logs with it.** Keep `ShutdownAsync` fast: stop accepting work, drain what
  is bounded, release.

### See also

- [Testing](https://docs.macro-deck.app/features/testing/) - assert on log lines with `harness.Logs`.
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/) - the builder, the reserved routes, the shutdown sequence.
- [Manifest reference](https://docs.macro-deck.app/reference/manifest/) - the `health` and `shutdown` blocks.
- [WebSocket reference](https://docs.macro-deck.app/reference/websocket/#events-logs-and-state) - the `log.publish` payload.
- [Troubleshooting](https://docs.macro-deck.app/guides/troubleshooting/) - when the probe or the logs do not do what you expect.

## Messaging between plugins

> Source: https://docs.macro-deck.app/features/messaging/
>
> Let plugins and integrations talk to each other by topic with IMessageChannel - events, commands and requests, topic ids, lifecycle, delivery guarantees, limits, older hosts and testing.

A plugin can talk to other plugins and to Macro Deck's built-in integrations without referencing
them. Everyone addresses a **topic**, a stable id such as `obs.scene.changed`, and Macro Deck
delivers the message to whoever listens to that topic. The OBS plugin publishes `obs.scene.changed`; a
lighting plugin subscribes to it and never needs to know which plugin sent it or whether it is
installed.

Macro Deck brokers every message. There is no direct connection between plugins, and every message
it delivers carries the sender's id, stamped by Macro Deck.

### Quick start

`IIntegrationContext.Messages` is the channel. The integration below answers requests for the current
scene and tells everyone when the scene changes:

```csharp
using System.Text.Json;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Messaging;

public sealed class ObsIntegration : IPluginIntegration
{
	private IMessageChannel? _messages;
	private string _scene = "Starting";

	public IReadOnlyList<IActionDefinition> Actions => [];

	public async Task InitializeAsync(IIntegrationContext context)
	{
		_messages = context.Messages;

		await _messages.HandleRequestsAsync<object, SceneInfo>("obs.scene.current",
			(_, _, _) => Task.FromResult(new SceneInfo(_scene)));
	}

	public Task ShutdownAsync() => Task.CompletedTask;

	private async Task OnSceneChangedAsync(string scene)
	{
		_scene = scene;
		await _messages!.PublishAsync("obs.scene.changed", new SceneInfo(scene));
	}
}

public sealed record SceneInfo(string Scene);
```

Another plugin, which has no reference to the OBS plugin, reacts to it:

```csharp
public async Task InitializeAsync(IIntegrationContext context)
{
	await context.Messages.SubscribeAsync<SceneInfo>("obs.scene.changed",
		(scene, message, _) => UpdateLightsAsync(scene!.Scene));

	var current = await context.Messages.RequestAsync<object?, SceneInfo>("obs.scene.current", null);
}
```

The SDK's typed helpers serialize payloads with System.Text.Json using the web defaults (camelCase).
Pass your own `JsonSerializerOptions` when both sides agree on different ones, or work with
`JsonElement` directly through the untyped members of `IMessageChannel`.

### Events, commands and requests

| Kind | Send with | Handle with | Reaches | Answer |
| --- | --- | --- | --- | --- |
| Event | `PublishAsync` | `SubscribeAsync` | every matching subscription | none; `PublishAsync` completes once Macro Deck accepted the event |
| Command | `SendAsync` | `HandleCommandsAsync` | the topic's one handler | completes when the handler finished |
| Request | `RequestAsync` | `HandleRequestsAsync` | the topic's one handler | the handler's return value |

- **Events fan out.** Every subscription whose pattern matches receives the event, including the
  publisher's own. `ChannelMessage.Sender` is your own plugin id for an event you published, so a
  handler can ignore it. Delivery is at most once and in publish order per receiver. A receiver that
  cannot keep up loses events rather than slowing the publisher down.
- **Commands and requests have exactly one handler.** Whoever registers a handler for a topic first
  keeps it until they dispose the registration or go away. A second participant that tries to handle the
  same topic gets `TopicAlreadyHandled`, and `MessageChannelException.HandlerOwner` names who has it.
  Nothing reserves a topic for its "real" owner, so prefix your topics with something only you use, such
  as your product name.
- **Handlers run on thread-pool threads.** An exception thrown by a command or request handler fails the
  call with `HandlerFailed`; its message is logged in your plugin and never sent to the caller. Put an
  error the caller should see into the reply payload instead. A subscription that throws is logged and
  does not affect other subscriptions.

### Topics

A topic is two or more dot-separated segments of lowercase letters, digits, `-` and `_`, each starting
and ending with a letter or digit, at most 128 characters: `obs.scene.changed`,
`home-assistant.light_1.state`. `MessageTopic.IsValidTopic` checks one.

A subscription takes a topic or a prefix wildcard. `obs.*` receives every topic below `obs`, such as
`obs.scene.changed` and `obs.stream.started`, but not `obs` itself and not `obsidian.note`. There are no
other wildcards, and command and request handlers always name one exact topic.

Topics are part of your plugin's public contract once other plugins use them. Keep them stable, and
keep the payload shapes compatible the way you would for a public API: add fields rather than rename
them.

### Lifecycle

Registrations made through `IIntegrationContext.Messages` belong to the integration's current
initialization. Macro Deck releases them when it shuts the integration down, and when it initializes
it again, which also happens after the user changed its configuration or the plugin reconnected to a
restarted Macro Deck. Register everything in `InitializeAsync` and you never have to dispose anything
yourself. While your integrations shut down and initialize again, Macro Deck keeps your command and
request topics for you, so re-registering them in the next `InitializeAsync` cannot fail because
another plugin took them in between.

A registration made through an `IMessageChannel` taken from dependency injection lasts until you dispose
it, across re-initializations. Use it from code that lives outside an integration, such as a hosted
service.

When your plugin disconnects, its handlers stay registered for the one minute Macro Deck waits for it to
resume; a command or request sent to it in that time fails with `HandlerUnavailable`, which is worth
retrying. Once that window has passed, or the plugin stopped, Macro Deck removes everything it
registered the next time it tidies up its sessions, and the topics are free; until then the answer
stays `HandlerUnavailable`. When your plugin reconnects without resuming, it registers everything
again, and another participant may have taken a topic in the gap.

### Failures and limits

Every operation throws `MessageChannelException`. `ErrorCode` says why:

| Code | Meaning |
| --- | --- |
| `Unsupported` | This Macro Deck has no message channel. |
| `NotConnected` | Your plugin is not connected to Macro Deck right now. Registrations are kept and sent once it is. |
| `InvalidTopic` | The topic or pattern does not follow the topic grammar. |
| `PayloadTooLarge` | The payload or reply is larger than 64 KiB once serialized. |
| `NoHandler` | Nothing handles the topic. |
| `HandlerUnavailable` | The handler is temporarily unreachable. Retry later. |
| `TopicAlreadyHandled` | Another participant already handles the topic; see `HandlerOwner`. |
| `HandlerFailed` | The handler threw or failed. |
| `Timeout` | The handler did not answer in time. |
| `RateLimited` | Too many messages in quick succession. Retry later. |

- A command or request waits at most 30 seconds for its handler, which is also the default. Pass a
  shorter `timeout` when you have a better idea of how long an answer is worth waiting for.
- A plugin can publish, send and request about 50 messages a second, with bursts of up to 100.
- A plugin can wait on at most 16 commands and requests at once. A handler receives at most 8 at once;
  more are refused with `RateLimited` rather than queued.
- A plugin can register at most 256 subscriptions, 256 command topics and 256 request topics.

### Permission

Declare `host:messaging` in `manifest.json` so that people installing your plugin can see it talks to
other plugins:

```json
"permissions": ["host:messaging"]
```

Macro Deck does not enforce it today. What you receive over the channel comes from other plugins: check
`Sender` when it matters who asked, and validate payloads like any other input.

### Built-in integrations

Macro Deck's own integrations get the same `IIntegrationContext.Messages` and share the same topics
with plugins. A plugin cannot tell whether a topic is handled by a plugin or by Macro Deck itself. One
difference: a built-in integration's topics are released as soon as it shuts down, so another participant
can take them before it initializes again.

### Older versions of Macro Deck

A Macro Deck without the message channel does not offer it, and your plugin then does not declare it.
`IMessageChannel` calls throw `MessageChannelException` with `Unsupported`; catch it where messaging is
optional for your plugin. The same applies to a custom `IIntegrationContext` implementation written
before the channel existed: its `Messages` member reports `Unsupported`.

On a Macro Deck that offers the channel, a plugin built on this SDK declares one more capability,
`messaging`, even when it never uses it. Tests that assert your plugin's exact list of declared
capabilities see it; see [Testing](https://docs.macro-deck.app/features/testing/).

### Testing

`FakeIntegrationContext.Messages` is a `FakeMessageChannel`. It routes your plugin's own messages the
way Macro Deck would, records everything your plugin publishes, sends and requests, and lets a test play
the other participants:

```csharp
var context = new FakeIntegrationContext();
context.Messages.RespondTo("obs.scene.current", _ => JsonSerializer.SerializeToElement(new { scene = "Live" }));

await integration.InitializeAsync(context);
var reply = await context.Messages.DeliverRequestAsync("lights.state", sender: "com.example.deck");

Assert.That(context.Messages.Published.Select(message => message.Topic), Does.Contain("lights.changed"));
```

In `PluginTestHarness` the same fake is `harness.Context.Messages` and is also what an injected
`IMessageChannel` resolves to; deliver through it rather than through raw capability invocations. Against
`MacroDeckTestHost`, `host.Messaging` records what a hosted plugin sends and subscribes to and answers
its commands and requests from `RespondTo` stubs, and `session.Messaging` delivers events, commands and
requests to it over the wire.

### On the wire

The channel uses the `messaging` host API and the `messaging` capability kind; see the
[WebSocket reference](https://docs.macro-deck.app/reference/websocket/#messaging).

## Music players

> Source: https://docs.macro-deck.app/features/music-players/
>
> Expose a music player with IMusicPlayerProvider and IMusicPlayer - instances, playback state, artwork, per-widget options, the standard actions, library browsing and device switching.

An integration exposes a music player by implementing `IMusicPlayerProvider`. It lists one
`MusicPlayerInstance` per configured account and resolves each one to an `IMusicPlayer`. Macro Deck
reads the state and sends the commands; how you talk to the player stays inside your integration.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.MusicPlayer;
using MacroDeck.Sdk.MusicPlayer.Actions;

public sealed class JukeboxIntegration : IPluginIntegration, IMusicPlayerProvider
{
	private const string InstanceId = "default";

	private readonly JukeboxPlayer _player = new(new JukeboxClient("http://localhost:9090"));

	public JukeboxIntegration()
	{
		// Play, pause, toggle, next, previous, refresh, volume, seek, shuffle and repeat.
		Actions = MusicPlayerActions.Common(ResolvePlayer, GetInstances);
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

	public IReadOnlyList<MusicPlayerInstance> GetInstances()
		=> [new MusicPlayerInstance(InstanceId, "Jukebox")];

	public IMusicPlayer? GetPlayer(string instanceId)
		=> instanceId == InstanceId ? _player : null;

	// An empty id means "first available player" - the actions' default.
	private IMusicPlayer? ResolvePlayer(string? instanceId)
		=> GetPlayer(string.IsNullOrEmpty(instanceId) ? InstanceId : instanceId);

	// IPluginIntegration members omitted.
}
```

The user can now pick "Jukebox" in the **Music Player widget**, which shows the track, artists and
artwork, and control it with the ten standard music-player actions.

Things to know:

- **The interface lights up the widget, not the actions.** Actions come from `MusicPlayerActions`, and
  variables such as `{{ vars.jukebox_track }}` from your own [`IVariableProvider`](https://docs.macro-deck.app/features/variables/).
  Implementing `IMusicPlayerProvider` alone gives you neither.
- **Instance ids are local.** Return `"default"`, not a qualified id. The host stores it as
  `integrationId::default`, and it ends up in saved widgets, so keep it stable.
- **The host polls.** It calls `GetStateAsync` regularly for each instance, so keep it cheap. You never
  push state.

### Implementing the player

```csharp
using MacroDeck.Sdk.MusicPlayer;

internal sealed class JukeboxPlayer(JukeboxClient client) : IMusicPlayer
{
	public async Task<MusicPlayerState> GetStateAsync(CancellationToken cancellationToken = default)
	{
		if (!client.IsConfigured)
		{
			return MusicPlayerState.Disconnected;
		}

		JukeboxStatus status;
		try
		{
			status = await client.GetStatusAsync(cancellationToken);
		}
		catch (HttpRequestException)
		{
			return MusicPlayerState.Unavailable("Jukebox offline");
		}

		return new MusicPlayerState
		{
			IsConnected = true,
			PlaybackState = status.IsPlaying ? PlaybackState.Playing : PlaybackState.Paused,
			TrackName = status.Title,
			Artists = status.Artists,
			AlbumName = status.Album,
			ArtworkId = status.CoverHash,
			Position = TimeSpan.FromSeconds(status.PositionSeconds),
			Duration = TimeSpan.FromSeconds(status.LengthSeconds),
			VolumePercent = status.Volume,
			ShuffleEnabled = status.Shuffle,
			RepeatMode = status.RepeatOne ? RepeatMode.Track : RepeatMode.Off
		};
	}

	public async Task<MusicPlayerArtwork?> GetArtworkAsync(string artworkId,
		CancellationToken cancellationToken = default)
	{
		var bytes = await client.GetCoverAsync(artworkId, cancellationToken);
		return bytes is null ? null : new MusicPlayerArtwork(bytes, "image/jpeg");
	}

	public Task PlayAsync(CancellationToken cancellationToken = default) => client.SendAsync("play", cancellationToken);

	public Task PauseAsync(CancellationToken cancellationToken = default) => client.SendAsync("pause", cancellationToken);

	public Task TogglePlayPauseAsync(CancellationToken cancellationToken = default)
		=> client.SendAsync("toggle", cancellationToken);

	public Task NextAsync(CancellationToken cancellationToken = default) => client.SendAsync("next", cancellationToken);

	public Task PreviousAsync(CancellationToken cancellationToken = default)
		=> client.SendAsync("previous", cancellationToken);

	public Task SeekAsync(TimeSpan position, CancellationToken cancellationToken = default)
		=> client.SeekAsync(position, cancellationToken);

	public Task SetVolumeAsync(int volumePercent, CancellationToken cancellationToken = default)
		=> client.SetVolumeAsync(volumePercent, cancellationToken);

	public Task SetShuffleAsync(bool enabled, CancellationToken cancellationToken = default)
		=> client.SetShuffleAsync(enabled, cancellationToken);

	public Task SetRepeatModeAsync(RepeatMode mode, CancellationToken cancellationToken = default)
		=> client.SetRepeatAsync(mode != RepeatMode.Off, cancellationToken);
}
```

Return a state, don't throw one. `MusicPlayerState.Disconnected` means there is nothing to reach (not
set up, signed out). `MusicPlayerState.Unavailable(message)` means the player is set up but can't answer
right now (rate limit, outage). The widget shows the message in place of the artist line, so keep it to a
few words. The two look different on purpose: an outage that reads "Not connected" looks as if the player
had gone.

`ArtworkId` is an opaque key that the host passes back to `GetArtworkAsync`, never a URL. The UI only
ever asks the host for artwork.

#### Source and badge

The widget's header shows where playback is happening on a second line under the player's name, and a
short badge of yours at the right, beside the playback icon:

```csharp
return new MusicPlayerState
{
	IsConnected = true,
	PlaybackState = PlaybackState.Playing,
	TrackName = track.Title,
	Artists = [track.Artist],
	DeviceName = session.AppName,               // "Firefox"
	Badge = $"{index + 1}/{sessions.Count}"     // "2/3"
};
```

- Both show only while `IsConnected` is true. A disconnected or unavailable state shows neither.
- `DeviceName` is left out when the player's name in the header already contains it as a whole word,
  so an instance named "SinusBot (Kitchen)" with the device "Kitchen" does not say it twice. A name that
  comes from `ProviderName` as a localized string is never compared.
- Keep `Badge` to a few characters. The widget reserves room for about 8, then shrinks and cuts off longer
  text. `null` or blank shows nothing.
- Users can hide both with the widget's **Source** option. The now-playing screen saver never shows them.
- A host older than `Badge` ignores it, so setting it is safe on every host. Don't put the badge into
  `Artists` or `TrackName` as a fallback: it would be read as part of the metadata by variables and triggers.

#### Showing the cover in your own UI

The deck's music player widget fetches artwork from the host on its own. When your plugin also draws the
cover in a tree of its own, `GetArtworkAsUiResourceAsync` resolves the artwork and registers it as a
[UI resource](https://docs.macro-deck.app/ui/reference/resources/#registering-your-own-images) in one call:

```csharp
UiResource? cover = await player.GetArtworkAsUiResourceAsync(
	context.UiResources,
	resourceName: "now-playing-cover",
	artworkId: state.ArtworkId,
	cancellationToken);
```

- It returns `null` when `artworkId` is null or empty or `GetArtworkAsync` has none. Nothing is registered
  or removed then, so the name keeps the previous cover until you drop it from the tree.
- Use one fixed name per place the cover appears, not one per track. Registering the name again replaces
  its bytes, while a name per track keeps every cover in your quota for the whole session.
- The registry's rules apply to the artwork. An invalid name, empty data, more than 2 MiB, or a media type
  Macro Deck does not accept is an `ArgumentException`. Only PNG, JPEG, WebP and GIF are accepted, so SVG
  is refused. The deck widget copes with some of these by re-encoding on the host, so a cover that shows
  there can still be refused here.
- Exceptions from your own `GetArtworkAsync`, including an `OperationCanceledException`, reach the caller
  unchanged.
- Await one call before starting the next for the same name. Two overlapping calls can finish out of
  order, and the older cover would then replace the newer one.
- An [in-process integration](https://docs.macro-deck.app/reference/capability-parity/) has no `UiResources`; the call throws
  `UiResourceException` with `Unsupported`.

#### Showing another player's cover

`GetArtworkAsUiResourceAsync` needs an `IMusicPlayer` of your own. To show the cover of a player that
belongs to another integration, ask Macro Deck to register it for you with `UiResources.RegisterMusicPlayerArtworkAsync`:

```csharp
UiResource? cover = await context.UiResources.RegisterMusicPlayerArtworkAsync(
	name: "now-playing-cover",
	instanceId: "net.example.jukebox::default",
	artworkId: "c0ffee",
	cancellationToken);
```

- **Where the two ids come from.** The instance id is the `Id` of a player in
  [`MusicPlayers.Instances`](#reading-every-providers-players). Both ids also appear in
  the URL that a player's `*-album-art-url` variable holds, for example
  `/api/music-player/artwork/c0ffee?instanceId=net.example.jukebox%3A%3Adefault`: the last path segment is
  the `artworkId` and the `instanceId` query value is the qualified instance id, both URL-encoded, so decode
  them first. A plugin that parses text the user writes, with such a variable in it, reads the pair from
  there. For an integration that allows only one configuration, `integrationId::default` resolves to its
  first player.
- **What you get.** The handle of the current artwork registered under `name`, as if you had registered the
  bytes yourself: it counts against the [quota](https://docs.macro-deck.app/ui/reference/resources/#registering-your-own-images), is
  released with the session, and registering the name again replaces it. Macro Deck may re-encode the image,
  so the media type can differ from the player's. Use one fixed name per place the cover is shown.
- **Size.** Pass `maxSize`, the size in pixels the cover is shown at, to get a smaller image:
  `RegisterMusicPlayerArtworkAsync(name, instanceId, artworkId, maxSize: 256, cancellationToken)`. Macro
  Deck keeps every cover at full size, at most 640 pixels on its longer side, and as 128 and 256 pixel
  copies when it is larger than those, and registers the smallest copy at least `maxSize` pixels, or the
  full-size cover when no copy is. Without `maxSize`, and on a Macro Deck that predates it, you get the
  full-size cover, so a smaller image is a saving, never a requirement.
- **`null`** when Macro Deck knows no such player or the player has no artwork for that id. Nothing is
  registered or removed then, so the name keeps its previous picture.
- **Errors.** `ArgumentException` for an invalid name and `ArgumentOutOfRangeException` for a `maxSize` that
  is not positive, before anything is sent. `UiResourceException` with
  `QuotaExceeded`; `RateLimited`, because this call has a tighter budget than other registrations and at most
  four run at once; `Unsupported` on a Macro Deck that predates it; or `Failed`. `Failed` covers a player that does
  not answer within 20 seconds, where retrying can succeed, and artwork larger than `maxUiResourceBytes` or
  of a media type Macro Deck does not accept, where it cannot.
- Any plugin can ask for the artwork of any player, the same images the deck shows to every client. To list
  the players, read [`MusicPlayers`](#reading-every-providers-players).

In tests, `FakeUiResourceRegistry.AddMusicPlayerArtwork(instanceId, artworkId, bytes, mediaType)` seeds what
the call finds, and `MacroDeckTestHost` answers it over the wire as a Macro Deck without other players.

#### `MusicPlayerState`

| Property | Meaning |
| --- | --- |
| `IsConnected` | There is a usable session. |
| `IsUnavailable`, `StatusMessage` | Configured but unreachable right now, and a short reason. |
| `PlaybackState` | `Stopped`, `Playing` or `Paused`. |
| `TrackName`, `Artists`, `AlbumName` | What is playing. `Artists` defaults to empty. |
| `ArtworkId` | Opaque id resolved through `GetArtworkAsync`. |
| `Position`, `Duration` | Playback position and track length. `null` when unknown. |
| `VolumePercent` | 0-100, or `null` when the player does not report it. |
| `ShuffleEnabled`, `RepeatMode` | `RepeatMode` is `Off`, `Track` or `Context` (album, playlist or queue). |
| `DeviceName`, `DeviceType` | Where playback is happening. The widget shows `DeviceName` as the source. |
| `Badge` | Short text beside the playback badge, such as `2/3`. See [Source and badge](#source-and-badge). |

### Actions

```csharp
Actions =
[
	.. MusicPlayerActions.Common(ResolvePlayer, GetInstances),
	MusicPlayerActions.PlayTrack(IntegrationId, ResolvePlayer, GetInstances),
	MusicPlayerActions.PlayPlaylist(IntegrationId, ResolvePlayer, GetInstances),
	MusicPlayerActions.PlayOnDevice(IntegrationId, ResolvePlayer, GetInstances),
	MusicPlayerActions.TransferPlayback(IntegrationId, ResolvePlayer, GetInstances)
];
```

Every action has an `instance` parameter (`MusicPlayerActions.InstanceParameterName`) filled from
`GetInstances`. Left empty, the action gets the first available player through your resolver. If the
command throws, the action reports a failed result and the rest of the flow keeps running.

`IntegrationId` is your integration's id, which for a plugin is the `id` in
[`manifest.json`](https://docs.macro-deck.app/reference/manifest/). The item and device actions use it to build the qualified
instance id when they ask the triggering client to pick a track, playlist or device at run time.

### Browsing and playing the library

```csharp
internal sealed class JukeboxPlayer(JukeboxClient client) : ICatalogMusicPlayer
{
	public async Task<IReadOnlyList<MusicPlayerCatalogItem>> GetCatalogAsync(
		string instanceId,
		MusicPlayerCatalogItemKind kind,
		string? filter,
		CancellationToken cancellationToken)
	{
		// Throws on failure: the picker shows "could not load, retry" instead of "no tracks".
		var songs = await client.SearchAsync(kind == MusicPlayerCatalogItemKind.Playlist, filter, cancellationToken);

		return songs
			.Select(s => new MusicPlayerCatalogItem(s.Id, s.Title, kind, Subtitle: s.Artist, ArtworkId: s.CoverHash))
			.ToList();
	}

	public async Task PlayItemAsync(MusicPlayerCatalogItem item, CancellationToken cancellationToken = default)
	{
		try
		{
			await client.PlayAsync(item.Id, cancellationToken);
		}
		catch (HttpRequestException ex)
		{
			_logger.Warning(ex, "Could not play {ItemId}", item.Id);
		}
	}

	// IMusicPlayer members as above.
}
```

`ICatalogMusicPlayer` is `IMusicPlayer` plus `IMusicPlayerCatalogProvider`. It powers the
**Play Track** and **Play Playlist** action pickers when the user configures an action, and the pick
dialog when the action runs with nothing selected. The host finds it by casting the object `GetPlayer`
returns.

Reads and commands fail in opposite ways:

| Member | On failure | Why |
| --- | --- | --- |
| `GetCatalogAsync` | **Throw.** Return empty only for an empty library. | Empty renders "no tracks", a throw renders "retry". |
| `PlayItemAsync` | **Log and return.** | A command failure must not abort the user's action flow. |

Let `OperationCanceledException` propagate from both. `GetCatalogAsync` is only called from a REST
request and may take as long as the library needs, but its token is the only thing that ends a request
the remote service never answers.

### Switching playback devices

```csharp
internal sealed class JukeboxPlayer(JukeboxClient client) : IMusicPlayer, IMusicPlayerDeviceProvider
{
	public async Task<IReadOnlyList<MusicPlayerDevice>> GetDevicesAsync(CancellationToken cancellationToken)
		=> (await client.GetOutputsAsync(cancellationToken))
			.Select(o => new MusicPlayerDevice(o.Id, o.Name, Type: "Speaker", IsActive: o.IsCurrent))
			.ToList();

	public async Task TransferPlaybackAsync(string deviceId, bool startPlayback, CancellationToken cancellationToken)
	{
		try
		{
			await client.SwitchOutputAsync(deviceId, startPlayback, cancellationToken);
		}
		catch (HttpRequestException ex)
		{
			_logger.Warning(ex, "Could not switch to {DeviceId}", deviceId);
		}
	}

	// IMusicPlayer members as above.
}
```

`IMusicPlayerDeviceProvider` powers **Play on Device** and **Transfer Playback**. It takes no instance id
because the object is already one instance. `MusicPlayerDevice.Type` is a free-form display string
("Computer", "Speaker"), not an enum. The failure rules are the same as for the library: `GetDevicesAsync`
throws on failure, and `TransferPlaybackAsync` logs and returns. A player without this interface fails
the device actions with `Unavailable`.

### Per-widget options

An instance can declare options that each Music Player widget sets for itself. One widget can then cycle
through the apps that are playing every 10 seconds while another widget on the same deck follows the app
the system calls current, without a second instance cluttering the player picker.

```csharp
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.MusicPlayer;

public IReadOnlyList<MusicPlayerInstance> GetInstances()
	=>
	[
		new MusicPlayerInstance("any", "Any app")
		{
			Options =
			[
				ActionParameter.Toggle("cycle", "Cycle between apps", defaultValue: false),
				ActionParameter.Number("cycleSeconds", "Cycle every (seconds)", min: 5, max: 60, defaultValue: 10)
			]
		},
		.. _sessions.Select(app => new MusicPlayerInstance(app.Id, app.Name))
	];

public IMusicPlayer? GetPlayerWithOptions(MusicPlayerOptionsRequest request)
{
	if (request.InstanceId != "any" || request.Options["cycle"] is not true)
	{
		return GetPlayer(request.InstanceId);
	}

	var seconds = (double)request.Options["cycleSeconds"];
	return new CyclingPlayer(_sessions, TimeSpan.FromSeconds(seconds));
}
```

The widget editor shows the options of the picked player below the player picker, and each widget stores
its own values. The host resolves the player with `GetPlayerWithOptions` and polls it separately from the
plain instance, so two widgets with different values show different tracks and covers.

- **Supported kinds.** `String`, `Number` (with `Min`, `Max`, `Step` and the slider), `Boolean`, and
  `Choice` with static `Options`. Any other kind, a `Choice` with dynamic options, an invalid name or a
  duplicate name is skipped with a warning in the host log. A kind the host does not know at all, from a
  newer SDK, is skipped as well.
- **Names.** 1 to 64 letters, digits, hyphens or underscores, starting with a letter or digit. The name is
  the key in the widget's stored data, so keep it stable.
- **Labels.** `Label` and `Description` are shown, localized like any other `LocalizedText`. Set a label:
  without one, the editor shows the raw name. `VisibleWhen`, `Required` and `Placeholder` are ignored.
- **Values.** `request.Options` always has one entry per supported option: the widget's value, or your
  default when the widget stored none or an invalid one. Values are `string` for String and Choice,
  `double` for Number (clamped to `Min` and `Max`), and `bool` for Boolean. A Choice value is always one of
  your option values.
- **Only for instances with options.** `GetPlayerWithOptions` is called only for an instance that declares
  options, and only for a widget that picked that instance. A widget set to "Active player" uses
  `GetPlayer`. The Now Playing screen saver has no option fields and shows the instance with your defaults.
- **Keep it cheap.** The host may call `GetPlayerWithOptions` for the same values again and again, and it
  never tells you when a set of values is no longer shown. Return a cached or lightweight object, and derive
  time-based behaviour such as cycling from the clock when `GetStateAsync` runs, not from a timer per set of
  values.
- **Display only.** The host reads state and artwork from this player and sends it no commands. Actions in
  a widget's flows keep addressing the instance through their own `instance` parameter, so a Next action on
  a cycling widget acts on the plain "Any app" player.
- **Artwork ids.** The host caches covers by instance and artwork id, shared across option values. An
  artwork id must name the same image whichever values produced it.
- **Default.** `GetPlayerWithOptions` defaults to `GetPlayer(request.InstanceId)`. Providers without options
  do not implement it.
- **Older hosts** ignore `Options` and show the plain instance.

### Volume and position variables

```csharp
VariableDefinition.Eager("jukebox_volume", VariableType.Numeric) with
{
	Id = "volume",
	Unit = "%",
	SemanticKind = VariableSemanticKinds.Percentage,
	Write = MusicPlayerVariableWrites.Volume
},
VariableDefinition.Eager("jukebox_position", VariableType.Numeric, refreshInterval: TimeSpan.FromSeconds(1)) with
{
	Id = "position",
	SemanticKind = VariableSemanticKinds.Duration,
	Write = MusicPlayerVariableWrites.Position
}

public ValueTask<VariableWriteResult> SetValueAsync(string localId, object? value,
	CancellationToken cancellationToken = default)
	=> localId switch
	{
		"volume" => MusicPlayerVariableWrites.SetVolumeAsync(GetPlayer(InstanceId), value, cancellationToken),
		"position" => MusicPlayerVariableWrites.SeekAsync(GetPlayer(InstanceId), value, cancellationToken),
		_ => ValueTask.FromResult(VariableWriteResult.NotWritable())
	};
```

#### Reading every provider's players

`IIntegrationContext.MusicPlayers` lists the players of every enabled provider, other plugins' and Macro
Deck's own included, and tells you the colour of each one's cover:

| `IMusicPlayerApi` member | What it does |
| --- | --- |
| `Instances` | Every player as `MusicPlayerInstanceSnapshot`: `Id` (`providerId::instanceId`), `ProviderId`, `ProviderName` and `DisplayName`. Empty until Macro Deck has sent the first list. |
| `InstancesChanged` | Raised after `Instances` changed. |
| `GetAlbumColorAsync(instanceId)` | The average colour of the player's cover as lowercase `#rrggbb`, the value of its `music_player_<name>_album_color` variable. |

```csharp
public async Task InitializeAsync(IIntegrationContext context)
{
	foreach (var player in context.MusicPlayers.Instances)
	{
		var color = await context.MusicPlayers.GetAlbumColorAsync(player.Id);
		_logger.Information("{Player} shows {Color}", player.DisplayName, color ?? "no cover");
	}

	context.MusicPlayers.InstancesChanged += (_, _) => RefreshPicker();
}
```

- **No permission is needed.** Any plugin may read any provider's players, just as any plugin may already
  register any player's cover with `RegisterMusicPlayerArtworkAsync`. The list holds what the deck shows every
  client: ids, provider names and display names, never playback state or account details.
- **The colour** is derived from the cover Macro Deck already holds and cached per cover, so asking again for
  the same cover is cheap. While a player shows no cover, is not connected, or its cover cannot be read, you
  get the last colour derived for that player. `null` when there is none, when Macro Deck knows no such
  player, and when it could not answer, including a Macro Deck that predates the call. The first call for a
  new cover may fetch it from its provider, so it can take a few seconds; in a plugin it counts towards the
  four artwork lookups that may run at once and is refused as `RateLimited` beyond that, which the SDK
  reports as `null`.
- **Handlers run on a background thread.** One that throws is logged and does not affect the others.
  Handlers subscribed through `IIntegrationContext.MusicPlayers` are released when Macro Deck shuts your
  integration down or initializes it again. In a plugin, `IMusicPlayerApi` can also be taken from dependency
  injection; handlers subscribed there are yours to remove.
- **Older Macro Deck and older SDK.** A context from a Macro Deck without the list, and any
  `IIntegrationContext` implementation compiled before it existed, reports no players, never raises the event
  and answers `null` for every colour. A plugin built against an older SDK never asks and ignores the push.

In tests, `FakeIntegrationContext.MusicPlayers` is a `FakeMusicPlayerApi`: `Set(players)` replaces the list and
raises `InstancesChanged`, and `SetAlbumColor(instanceId, color)` sets what `GetAlbumColorAsync` answers.
`PluginTestHarness` also registers it as the plugin's `IMusicPlayerApi`.

`MusicPlayerVariableWrites` gives a bound Slider the same write behaviour as the built-in players:
volume streams while the user drags, position commits on release, values are clamped, and a missing
player answers `Unavailable`. See [Writable variables](https://docs.macro-deck.app/features/variables/#writable-variables).

### Edge cases

- **An instance disappears.** Drop it from `GetInstances` and return `null` from `GetPlayer`. Widgets
  pointing at it show as disconnected, and they come back if the id returns.
- **Invalid or duplicate ids** from `GetInstances` are skipped and logged.
- **`ProviderName`** is optional. Leave it out and the integration's name (the manifest name for a plugin)
  is used.
- **A disabled integration** has no instances.
- **Options change.** Widgets pick up a changed `Options` list on their own; an editor that is already open
  shows the new fields when it is opened again. Values a widget stored for an option that no longer exists
  are ignored.

### Over the plugin protocol

Music players are fully supported out of process (capability kind `music-player`). Reading every
provider's players is the separate `music-players` host api: the list arrives as a revisioned `host.state`
push and the colour as `music-players`/`album-color`, see
[the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#music-players). The instance list is
a snapshot, so after `GetInstances` changes (an account was added in your config flow, or an instance's
`Options` changed), call `CatalogChanged(CapabilityKinds.MusicPlayer)` on an injected `IPluginCatalogNotifier`.
Options travel as optional fields within `music-player` version 1: the instance list carries them, and
only the `state` and `artwork` operations carry a widget's values. State reads from
an unreachable plugin degrade to unavailable. Library and device failures stay real failures, so an
unreachable plugin never looks like an empty library. See
[Capability parity](https://docs.macro-deck.app/reference/capability-parity/) and
[the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities).

### See also

- [Variables](https://docs.macro-deck.app/features/variables/) - track, artist and playback variables.
- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - adding accounts, and so instances.
- [Actions](https://docs.macro-deck.app/features/actions/)
- [Virtual profiles](https://docs.macro-deck.app/features/virtual-profiles/) - ship a ready-made layout with a Music Player widget.
- [Testing](https://docs.macro-deck.app/features/testing/)

## Notifications

> Source: https://docs.macro-deck.app/features/notifications/
>
> Show toasts and dialogs on every connected Macro Deck client, keep an entry in the notification list, and get the user's answer back with INotificationService.

A plugin shows a short message, or asks a question, on the screens Macro Deck is running on: the desktop
app, the web client and the Companion app. `IIntegrationContext.NotificationService` is the one API for all of
it. The older `IIntegrationContext.Notifications` (`IUserNotifier`) still works and only adds an entry to the
notification list.

A message for the person at the computer itself, shown by the operating system as a Windows toast, a macOS
notification or a Linux desktop notification, goes through `IIntegrationContext.DesktopNotifications`
instead; see [Desktop notifications](#desktop-notifications).

| To | Use |
| --- | --- |
| Show a toast or dialog on the Macro Deck clients, or ask and wait for an answer | `NotificationService` (`INotificationService`) |
| Leave an entry in Macro Deck's notification list | `NotificationService` with `Inbox`, or the older `Notifications` (`IUserNotifier`) |
| Show a notification from the computer's operating system | `DesktopNotifications` (`IDesktopNotifier`) |

### Example

```csharp
public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
{
    var result = await _context.NotificationService.ShowForResultAsync(
        new NotificationOptions
        {
            Title = MyStrings.DeleteRecordingTitle(),
            Message = MyStrings.DeleteRecordingMessage(),
            Severity = NotificationSeverity.Warning,
            Popup = NotificationPopup.Dialog,
            Actions =
            [
                new NotificationAction { Id = "delete", Label = MyStrings.Delete(), Style = NotificationActionStyle.Danger },
                new NotificationAction { Id = "keep", Label = MyStrings.Keep() },
            ],
        },
        context.CancellationToken);

    return result.ActionId == "delete" ? await DeleteAsync() : ActionResult.Success();
}
```

The first valid answer from any targeted client wins. Macro Deck closes the popup on every other client and
`ShowForResultAsync` returns once, with the id of the pressed action and who pressed it.

### What a notification is

| Member | Meaning |
| --- | --- |
| `Title`, `Message` | `LocalizedText`. Every client resolves it in its own language. The title is required, at most 200 characters for literal text; the message at most 1000. |
| `Severity` | `Info`, `Success`, `Warning`, `Error`. |
| `Popup` | `None`, `Toast` (the default) or `Dialog`. A notification has at most one popup, so a toast and a dialog cannot be combined. |
| `Inbox` | Also keeps an entry in the notification list. It is independent of the popup: closing the popup never removes the entry, and dismissing the entry never closes the popup. At least one of `Popup` and `Inbox` must be set. A notification with `Popup = None` and no `Progress` is only an entry: it is complete as soon as it is added, with `Programmatic` as its reason, and cannot be updated. |
| `Duration` | How long the popup stays. A toast defaults to 6 seconds. A dialog stays until answered. Macro Deck clamps it to between 1 second and one hour and closes every popup after one hour at the latest, with the reason `Timeout`, also a dialog you are waiting on. |
| `Dismissible` | Whether the user can close the popup without choosing an action. A dialog needs an action, `Dismissible`, or a `Duration`. |
| `Target` | `NotificationTarget.All` (the default), `NotificationTarget.AdminUi` (the desktop app and administrator sessions) or `NotificationTarget.Devices(...)`. Devices are named by their device id, which Macro Deck takes from the authenticated connection. |
| `Actions` | Up to four buttons. Only the declared ids are accepted as a response. |
| `Content` | A static Macro Deck UI tree for a dialog, see [Forms](#forms). |
| `Progress` | A progress bar, determinate with a `Total` or indeterminate without. Change it with `UpdateAsync`. |

Macro Deck decides where a notification comes from. Every client shows the source (Macro Deck, an integration
or a plugin, plus its name) and a plugin cannot present itself as anything else.

### Updating and dismissing

`ShowAsync` returns an `INotificationHandle` as soon as the notification is open.

```csharp
var handle = await context.NotificationService.ShowAsync(
    new NotificationOptions { Title = "Exporting", Inbox = true, Progress = new NotificationProgress(0, 40) });

for (var done = 1; done <= 40; done++)
{
    await ExportNextAsync();
    await handle.UpdateAsync(new NotificationUpdate { Progress = new NotificationProgress(done, 40) });
}

await handle.UpdateAsync(new NotificationUpdate { Title = "Export finished", Severity = NotificationSeverity.Success });
await handle.DismissAsync();
```

`NotificationUpdate` changes the title, message, severity, progress, actions or content. A member left `null`
keeps its value. Every update restarts the duration of a toast, so a toast that reports progress stays up while
it keeps being updated; the maximum lifetime still ends it. The popup kind, target and duration are fixed when it is shown. Only the integration that
showed a notification can update or dismiss it. `handle.Completion` completes exactly once, whatever closed
the notification.

### How it ends

`NotificationResult.CloseReason`:

| Reason | When |
| --- | --- |
| `Action` | A client pressed one of the actions. `ActionId`, `ClientId` and `Values` are set. |
| `Dismissed` | A client closed the popup without choosing an action. |
| `Timeout` | The duration, or the maximum lifetime, elapsed. |
| `Programmatic` | The owner called `DismissAsync`. |
| `OwnerGone` | The owner went away, for example the plugin was unloaded. |
| `HostUnavailable` | The host restarted or could not be reached, so the outcome is unknown. Notifications live in memory and do not survive a host restart. |

`ClientId` is the device id of the responding client, or the literal `admin` for the desktop app and
administrator sessions, which have no device id.

Cancelling the token of `ShowForResultAsync` dismisses the notification and throws
`OperationCanceledException`.

### Forms

`Content` lets a dialog ask for values. It is a Macro Deck UI tree in the widget profile that Macro Deck
renders as it renders any other tree, with no session and no event round trip: the tree is a snapshot.

A `ui.text-field`, `ui.toggle`, `ui.slider` or `ui.segmented` node that declares a `change` or `adjust` event
is an input and its node id is the field name. `NotificationResult.Values` contains every input of the tree:
what the user entered, or the value the tree started with when they did not touch it.

| Component | Value | Accepted |
| --- | --- | --- |
| `ui.text-field` | JSON string | At most 1000 characters |
| `ui.toggle` | JSON boolean | |
| `ui.slider` | JSON number | 0 to 1 |
| `ui.segmented` | JSON integer | 0 up to the number of segments minus one |

Macro Deck rejects a response with an unknown field or a value outside these limits, tells the client, and
keeps the dialog open. The widget profile has no `required` flag or pattern: check the returned values
yourself and ask again with another notification if they are not good enough.

```csharp
var result = await context.NotificationService.ShowForResultAsync(new NotificationOptions
{
    Title = "Name this scene",
    Popup = NotificationPopup.Dialog,
    Actions = [new NotificationAction { Id = "save", Label = "Save", Style = NotificationActionStyle.Primary }],
    Content = Form.Build(), // a UiNode with a text field whose Id is "name"
});

var name = result.Values["name"].GetString();
```

A dialog tree may hold up to 200 nodes, nested at most 12 levels, and 32 KiB in all.

### Limits

| Limit | Value |
| --- | --- |
| Open notifications per plugin | 20 |
| Open notifications in total | 50 |
| Content of all open notifications | 64 KiB per plugin, 256 KiB in total |
| Notifications shown per minute | 30 per plugin |
| Updates per second | 20 per plugin |

A call over a limit throws `NotificationException` with `NotificationErrorCode.LimitExceeded`. Macro Deck
sends updates to the clients at most four times a second per notification, so a burst of progress updates
costs nothing on the screens.

### Reconnecting clients

A client that connects while a popup is open gets it, and a client that was away learns what closed in the
meantime: Macro Deck sends the list of open popups to every client when it connects. A queued popup that the
host closed or that timed out disappears even if it was never shown.

### Notification list

The desktop app shows the list. Entries are unread until the user reads them, and the list keeps the
newest 100, dropping the oldest read entry first. The list stays on the host's machine and is not kept over
a restart. Entries are written in the host's language, while a popup is shown in each client's own. Only
the desktop app and administrator sessions see the list, also when the popup was sent to a device.

### From an action

Users get the same thing without code: the System integration has the action **Show Macro Deck
notification** with title, message, severity, how to show it and a timeout, and it renders template
variables like any other action parameter. See [Notifications](https://docs.macro-deck.app/guide/concepts/#notifications) in the user
guide.

### Over the plugin protocol

A plugin that uses the SDK needs nothing else. On the wire, `host.invoke` against the `notifications` api
has the operations `show`, `update` and `close` next to the older `notify` and `dismiss`. `show` answers
with the notification id as soon as it is open, never when somebody answers, because a person is not bound
by the request deadline. How the notification ended arrives later as a `ui` / `notification.result`
`capability.invoke`, exactly once per notification. A result the plugin cannot take while it is detached is
kept and sent when it reattaches. A host that predates these operations answers `CAPABILITY_UNSUPPORTED`, which
the SDK reports as `NotificationErrorCode.Unsupported`; a plugin written before them keeps working
unchanged. See the [WebSocket reference](https://docs.macro-deck.app/reference/websocket/).

### Desktop notifications

```csharp
if (_context.DesktopNotifications.IsSupported)
{
    await _context.DesktopNotifications.ShowAsync(MyStrings.RecordingStopped(), MyStrings.SavedTo(path), cancellationToken);
}
```

`IDesktopNotifier.ShowAsync` hands a title and a message to the operating system of the computer Macro Deck
runs on. Macro Deck shows it through its own app first, so the notification carries Macro Deck's name and
icon, and falls back to the operating system's own tool when the app is not running. The System integration's
**Send notification** action uses the same path.

- **Best effort.** The call never throws because a notification could not be shown: while `IsSupported` is
  `false`, or when Macro Deck refuses or fails, it completes without showing anything. The operating system
  can still hide it, for example under a focus mode, and nothing is reported back. Only cancellation throws.
- **`IsSupported`** is `false` on a computer without desktop notifications, such as Linux without
  `notify-send`, and for a plugin that may not show them.
- **Plugins declare `host:desktop-notifications`.** An installed plugin without it cannot show desktop
  notifications; a session registered with a developer token or pairing counts as declaring it. An
  integration built into Macro Deck always may. See [the manifest](https://docs.macro-deck.app/reference/manifest/) and
  [the security model](https://docs.macro-deck.app/policies/security/#desktop-notifications).
- **Older Macro Deck versions.** A plugin learns `IsSupported` when it registers. Macro Deck before
  desktop notifications reports nothing, so `IsSupported` stays `false` and `ShowAsync` shows nothing. An
  `IIntegrationContext` implemented against an older SDK inherits the same behaviour from
  `UnsupportedDesktopNotifier`.

On the wire this is the [`desktop-notifications`](https://docs.macro-deck.app/reference/websocket/#desktop-notifications) host API. In
`MacroDeck.Plugin.Testing`, `FakeIntegrationContext.DesktopNotifications` is a `FakeDesktopNotifier` that
records what it showed in `Shown`; set `IsSupported` to `false` to test the other case.

### Testing

`FakeIntegrationContext.NotificationService` in `MacroDeck.Plugin.Testing` is a `FakeNotificationService`:
it records what a plugin showed and a test answers it with `Respond` or `Close`.

```csharp
var context = new FakeIntegrationContext();
var asking = plugin.AskAsync(context);

context.NotificationService.Open.Single().Respond("delete");
await asking;
```

## Settings migrations

> Source: https://docs.macro-deck.app/features/settings-migrations/
>
> Take a plugin's buttons, connections and credentials over from another application such as Macro Deck 2 with IMigrationProvider and IIntegrationMigration.

An integration implements `IMigrationProvider` so someone arriving from Macro Deck 2 keeps the buttons and
connections they already had. This page is about another application's setup; for upgrading your plugin
to a newer SDK or protocol, see [SDK and protocol migrations](https://docs.macro-deck.app/policies/migrations/).

### Quick start

```csharp
using System.Text.Json;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Migration;

public sealed class ObsIntegration : IPluginIntegration, IMigrationProvider
{
	public IReadOnlyList<IIntegrationMigration> Migrations { get; } = [new ObsMacroDeck2Migration()];

	// IPluginIntegration members omitted.
}

internal sealed class ObsMacroDeck2Migration : IIntegrationMigration
{
	private const string IntegrationId = "com.example.obs"; // the id in your manifest.json

	public MigrationSource Source => MigrationSource.MacroDeck2;

	// Macro Deck 2 names the assembly an action type lives in.
	public IReadOnlyList<string> ClaimedActionSources { get; } = ["OBS-WebSocket Plugin"];

	// Macro Deck 2's settings file name: "<author>_<plugin name>", lowercased.
	public IReadOnlyList<string> ClaimedSettingsSources { get; } = ["macro deck_obs-websocket plugin"];

	public Task<ActionMigrationResult?> MigrateActionAsync(ForeignAction action, CancellationToken cancellationToken)
		=> Task.FromResult(action.TypeName switch
		{
			"SuchByte.OBSWebSocketPlugin.Actions.SetSceneAction" => MigrateSetScene(action),
			_ => null
		});

	public Task<IReadOnlyList<MigratedConfiguration>> MigrateConfigurationAsync(
		ForeignPluginSettings settings, CancellationToken cancellationToken)
		=> Task.FromResult<IReadOnlyList<MigratedConfiguration>>([]);

	private static ActionMigrationResult? MigrateSetScene(ForeignAction action)
	{
		var scene = ReadString(action.Configuration, "SceneName");
		if (string.IsNullOrWhiteSpace(scene))
		{
			return null;
		}

		return new ActionMigrationResult(IntegrationId, "set-scene", action.DisplayName ?? "Set OBS scene",
			new Dictionary<string, JsonElement> { ["scene"] = JsonSerializer.SerializeToElement(scene) });
	}

	private static string? ReadString(string? json, string name) { /* parse leniently, null on failure */ }
}
```

Every Macro Deck 2 "Set scene" button now arrives as your `set-scene` action with its scene filled in.
Every other OBS button arrives as a placeholder carrying its original configuration.

Things to know:

- **`Migrations` is a list, one entry per source application.** An integration commonly reads several
  (`MigrationSource.MacroDeck2`, `TouchPortal`, `Deckboard`); two entries never share a `Source`.
- **You claim, the host reads.** Finding the foreign installation, reading its files and decrypting its
  credentials is the host's work. It then asks whoever claims what it found.
- **Action and settings claims are separate lists.** `ClaimedActionSources` matches what the source uses
  to say which plugin an action came from; `ClaimedSettingsSources` matches its stored per-plugin
  settings and credentials. An application need not name a plugin the same way in both.

### Translating actions

```csharp
private static ActionMigrationResult? MigrateChatMode(ForeignAction action, string mode)
{
	var method = ReadEnumIndex(action.Configuration, "Method"); // 0 = on, 1 = off, 2 = toggle
	if (method is not (0 or 1))
	{
		return null; // "toggle" has no equivalent: this plugin's action only sets a fixed value
	}

	return new ActionMigrationResult(IntegrationId, "set-chat-mode", action.DisplayName ?? "Set chat mode",
		new Dictionary<string, JsonElement>
		{
			["mode"] = JsonSerializer.SerializeToElement(mode),
			["enabled"] = JsonSerializer.SerializeToElement(method == 0)
		});
}
```

`ForeignAction` is the action as the source stored it: `TypeName`, `ActionSource`, `DisplayName`, and an
opaque `Configuration` string you parse yourself. Switch on `TypeName`.

**`null` is a normal answer, not a failure.** Return it when there is no equivalent, or when the
configuration cannot be read - never throw, because one unreadable button must not end a migration. The
host keeps the action as a placeholder with its original configuration, which is better than an action
that quietly does something else.

`Parameters` carries only the values the source knew. Type, label and options come from your action's
own definition, so a migration never restates them.

### Migrating configuration and credentials

```csharp
public Task<IReadOnlyList<MigratedConfiguration>> MigrateConfigurationAsync(
	ForeignPluginSettings settings, CancellationToken cancellationToken)
{
	var results = new List<MigratedConfiguration>();

	foreach (var credentials in settings.Credentials)
	{
		if (!credentials.TryGetValue("host", out var host) || string.IsNullOrWhiteSpace(host))
		{
			continue; // no host: this entry would look configured and never connect
		}

		var title = credentials.TryGetValue("name", out var name) && name.Length > 0 ? name : "OBS Connection";
		var values = new Dictionary<string, JsonElement> { ["host"] = JsonSerializer.SerializeToElement(host) };

		var secrets = new Dictionary<string, MigratedSecret>();
		if (credentials.TryGetValue("password", out var password) && password.Length > 0)
		{
			secrets["password"] = new MigratedSecret(password, MigratedSecretKind.Secret);
		}

		results.Add(new MigratedConfiguration(IntegrationId, title, values, secrets));
	}

	return Task.FromResult<IReadOnlyList<MigratedConfiguration>>(results);
}
```

`ForeignPluginSettings` holds the plugin's stored `Settings`, its already-decrypted `Credentials`, and
every one of its `Actions` the source found - because an application need not keep all of a plugin's
configuration in its settings file (Macro Deck 2 stored the SinusBot login there, but the bot instance
in each button).

**`Credentials` may be empty.** The user can decline to decrypt them, and an application that ties
credentials to the machine that wrote them cannot open a folder copied off another one. Return nothing
rather than an entry that looks configured but cannot work.

Put secret values in `Secrets`, never in `Values`: the host stores each in its secret store and leaves only
a reference in the entry. `MigratedSecretKind.Password` is a password the user chose and may be shown
again; `Secret` is a token or key they never typed.

### Reporting warnings

```csharp
return new ActionMigrationResult(IntegrationId, "set-scene", action.DisplayName ?? "Set OBS scene",
	parameters,
	Warnings: [Strings.Migration.ConnectionNotMigrated(name: connectionName)]);
```

Anything a translation could not carry across exactly goes in `Warnings`. A partial translation is useful
as long as it is honest about what it dropped. Warnings are `LocalizedText`, so a generated
[`Strings` member](https://docs.macro-deck.app/features/localization/#the-generated-api) reads in the language of whoever opens the
migration wizard.

### Edge cases

- **Any failure over the protocol counts as "no equivalent".** An unreachable plugin, a timeout or a
  malformed result costs one placeholder, not the migration. See
  [capability parity](https://docs.macro-deck.app/reference/capability-parity/).
- **Unknown sources are ignored.** A source name the host does not recognise is dropped from the
  declaration rather than refused, so a plugin built against a later SDK stays usable.
- **Both members are asynchronous** because an out-of-process plugin answers over its connection. Pure
  in-process work returns `Task.FromResult` and costs nothing.

### Over the plugin protocol

The `migration` capability kind, declared at the single local id `provider`; the source application
travels in each invocation's arguments.

| Operation | Purpose |
| --- | --- |
| `describe` | Every source this plugin migrates from, with its claimed action and settings sources. |
| `migrate-action` | Translate one foreign action. `translated: false` is the "no equivalent" answer. |
| `migrate-configuration` | Turn a foreign plugin's settings and credentials into configuration entries. Secrets travel separately from plain values. |

See [the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities).

### See also

- [Actions](https://docs.macro-deck.app/features/actions/) - the action ids and parameters a translation targets
- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - the configuration entries a migration creates
- [Localization](https://docs.macro-deck.app/features/localization/) - generating `Strings` for warnings
- [SDK and protocol migrations](https://docs.macro-deck.app/policies/migrations/) - upgrading your plugin, not the user's setup

## Setup flows

> Source: https://docs.macro-deck.app/features/setup-flows/
>
> Guide users through connecting an integration with IConfigFlowProvider - steps, fields, validation errors, secrets, OAuth, reconfiguring an entry and optional settings.

A setup flow (config flow) walks the user through connecting your integration: a few form steps, then a
saved **config entry** your integration reads at runtime. Implement `IConfigFlowProvider` and return a
fresh `IConfigFlow` for each setup session.

Action flows - the automations users build out of actions - are a different thing; see
[Actions](https://docs.macro-deck.app/features/actions/).

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.ConfigFlow;
using MacroDeck.Localization;

public sealed class MediaServerIntegration : IPluginIntegration, IConfigFlowProvider
{
	public IConfigFlow CreateConfigFlow() => new MediaServerConfigFlow();

	// IPluginIntegration members omitted.
}

public sealed class MediaServerConfigFlow : IConfigFlow
{
	public Task<ConfigFlowResult> StartAsync(IConfigFlowContext context, CancellationToken cancellationToken)
		=> Task.FromResult(ConfigFlowResult.Step(ConnectionStep()));

	public async Task<ConfigFlowResult> SubmitAsync(
		string stepId,
		IReadOnlyDictionary<string, object?> input,
		IConfigFlowContext context,
		CancellationToken cancellationToken)
	{
		var serverUrl = (input.GetValueOrDefault("server_url") as string ?? string.Empty).Trim();
		var apiKey = input.GetValueOrDefault("api_key") as string ?? string.Empty;

		if (!await MediaServerClient.CanConnectAsync(serverUrl, apiKey, cancellationToken))
		{
			return ConfigFlowResult.Error(ConnectionStep(), Strings.Setup.CannotConnect());
		}

		// Both form fields are persisted automatically; api_key is encrypted because it is a Secret field.
		return ConfigFlowResult.Complete("Media server");
	}

	private static ConfigFlowStep ConnectionStep() => new()
	{
		StepId = "connection",
		Title = Strings.Setup.ConnectionTitle(),
		Fields =
		[
			ActionParameter.Url("server_url", label: Strings.Setup.ServerUrl(),
				placeholder: "http://192.168.1.20:8096", required: true),
			ActionParameter.Secret("api_key", label: Strings.Setup.ApiKey(), required: true)
		]
	};
}
```

The user can now set up the integration from its page: they fill in the step, you check the connection,
and the host saves a config entry titled "Media server".

Things to know:

- **One `IConfigFlow` per session.** The host calls `CreateConfigFlow` for every setup session, so
  keeping per-session state in instance fields is fine.
- **`input` holds every value collected so far**, keyed by field name, with secrets already decrypted to
  plaintext for validation. Never log them or put them in an error message.
- **Expected failures are `Error`, not exceptions.** Validate credentials or connectivity on the step
  where the user types them - a field error now beats an [integration issue](https://docs.macro-deck.app/features/integration-issues/)
  later.
- **More than one entry is allowed by default.** Return `false` from `AllowsMultipleConfigurations` when
  a second one makes no sense (a single account).
- **A flow has to be completed before the integration runs.** Until the user saves an entry, the
  integration is off, shown as needing setup, and turning it on opens the flow. For a flow that only
  changes settings with defaults, see [Optional settings](#optional-settings).

### Outcomes

Every `StartAsync` and `SubmitAsync` returns a `ConfigFlowResult`:

| Factory | What the host does |
| --- | --- |
| `Step(step)` | Shows `step`. |
| `Error(step, message, fieldErrors)` | Shows `step` again with a general message and/or per-field messages keyed by field name. Values from this submit are discarded. |
| `External(url, resumeStepId)` | Opens `url` in the browser, waits for the redirect callback, then submits `resumeStepId`. See [OAuth](#oauth). |
| `Complete(title, values)` | Saves the entry: all collected form values plus the extra `values`. |
| `CompleteWithoutEntry()` | Closes the dialog and stores nothing. See [Completing without an entry](#completing-without-an-entry). |

### Multi-step flows

```csharp
public async Task<ConfigFlowResult> SubmitAsync(string stepId, IReadOnlyDictionary<string, object?> input,
	IConfigFlowContext context, CancellationToken cancellationToken)
	=> stepId switch
	{
		"connection" => await SubmitConnection(input, cancellationToken), // returns Step(InstanceStep(...))
		"instance" => SubmitInstance(input),                            // returns Complete(...)
		_ => ConfigFlowResult.Error(ConnectionStep(), Strings.Setup.UnknownStep())
	};

private static ConfigFlowStep InstanceStep(IReadOnlyList<BotInstance> instances) => new()
{
	StepId = "instance",
	Title = Strings.Setup.InstanceTitle(),
	Fields =
	[
		ActionParameter.Choice("instance_id",
			options: instances.Select(i => new ActionParameterOption { Value = i.Id, Label = i.Name }).ToList(),
			label: Strings.Setup.Instance(),
			required: true)
	]
};
```

Branch on `stepId`, and use an earlier step's answer to build the next one - here, the instances the
server reported. The built-in SinusBot integration works exactly like this.

The dialog offers a Back button once a step has been submitted, so `SubmitAsync` can arrive for an
earlier step id than the one you returned last, with the values the user corrected. Do not assume
steps arrive in order: dispatch on `stepId` and overwrite whatever state that step derives.
When the user goes back, the host drops everything the steps after that one collected, so `input`
and the saved entry only hold values from the path the user actually took. Flows that serve a
config UI tree (`IUiConfigFlow`) get no Back button, because their steps live in the tree.

### Steps and fields

```csharp
new ConfigFlowStep
{
	StepId = "credentials",
	Title = Strings.Setup.ConnectTitle(),
	Description = Strings.Setup.ConnectDescription(),
	Instructions =
	[
		new ConfigFlowInstruction { Text = Strings.Setup.CreateAppInstruction() },
		new ConfigFlowInstruction
		{
			Text = Strings.Setup.AddRedirectUriInstruction(),
			Values = [new ConfigFlowCopyValue { Label = Strings.Setup.RedirectUri(), Value = context.OAuth.RedirectUri }]
		}
	],
	Links = [new ConfigFlowLink { Label = Strings.Setup.Dashboard(), Url = "https://developer.example.com" }],
	Fields = [ActionParameter.Text("client_id", label: Strings.Setup.ClientId(), required: true)],
	AdvancedFields = [ActionParameter.Url("api_base", label: Strings.Setup.CustomEndpoint())]
};
```

| Member | Rendered as |
| --- | --- |
| `Title`, `Description` | Heading and the sentence introducing the step. |
| `Values` | `ConfigFlowCopyValue`s - labelled, monospaced values with a copy button. |
| `Instructions` | A numbered list; never number the text yourself. Each can carry its own copy values. |
| `Links` | Labelled links, such as a developer portal. |
| `Fields` | The form. |
| `AdvancedFields` | Hidden behind an "Advanced configuration" switch. Never `Required`. |

Fields are `ActionParameter`s, so they render with the same controls as action parameters: `Text`, `Url`,
`Number`, `Choice`, `Toggle`, `Secret` and the rest. Keep `AdvancedFields` for escape hatches - an own
OAuth client id, a non-default endpoint - not for normal setup. The section opens by itself when one of its
fields already has a value.

`OnlyWhen` works on step fields the way it does on [action parameters](https://docs.macro-deck.app/features/actions/#declaring-parameters):
a field shows only while the named field of the same step holds one of the listed values (compared
case-insensitively), and the dialog re-evaluates as the user picks, without a step round trip. A field whose
named field is still empty stays hidden.

```csharp
Fields =
[
	ActionParameter.Choice("brand", brands, label: Strings.Setup.Brand(), required: true),
	ActionParameter.Choice("razerModel", razerModels, label: Strings.Setup.Model(), required: true)
		.OnlyWhen("brand", "razer"),
	ActionParameter.Choice("logitechModel", logitechModels, label: Strings.Setup.Model(), required: true)
		.OnlyWhen("brand", "logitech")
]
```

Continue is gated on the fields that are shown: neither a closed advanced section nor a required field hidden
by `OnlyWhen` blocks it. A hidden field keeps its value and is still submitted, so read the field that
decides, not the presence of a value. Hosts up to 3.0.0-beta.4 ignore `OnlyWhen` here and show every field.

`ActionParameter.WidgetTarget` works here too, with the same picker actions use. A flow belongs to an
integration rather than a widget, so "This widget" (`$self`) is not offered and the field yields a
concrete widget id. Pass `WidgetTargetOptions` with `WidgetTypes` to limit the choice.

### Secrets

```csharp
ActionParameter.Secret("api_key", label: Strings.Setup.ApiKey(), required: true)

// Values that were never form fields:
return ConfigFlowResult.Complete(title, new Dictionary<string, ConfigFlowValue>
{
	["access_token"] = ConfigFlowValue.Secret(token.AccessToken),
	["refresh_token"] = ConfigFlowValue.Secret(token.RefreshToken),
	["display_name"] = ConfigFlowValue.Plain(profile.DisplayName)
});
```

- A `Secret` or `Password` field is stored encrypted by the host. You receive the plaintext in `input`.
- `Complete` can add values the user never saw, such as tokens from an OAuth exchange. `Secret` values are
  encrypted, `Plain` values stored as they are. A secret with an empty value is skipped.
- Secrets never belong in logs or in user-visible errors - log the failure type, not the value.

### Reading the entry at runtime

```csharp
public async Task InitializeAsync(IIntegrationContext context)
{
	foreach (var entry in await context.Config.GetEntriesAsync())
	{
		var serverUrl = await context.Config.GetStringAsync(entry.Id, "server_url");
		var apiKey = await context.Config.GetSecretAsync(entry.Id, "api_key");
		// Connect one client per entry. entry.Title is the name the user sees.
	}
}
```

`IIntegrationContext.Config` is an `IIntegrationConfig`. Secrets are only decrypted when you ask with
`GetSecretAsync`. `SetStringAsync` and `SetSecretAsync` write back to an entry - use `SetSecretAsync` for
rotating credentials such as a refreshed OAuth access token.

### OAuth

```csharp
// Step 1: collect the client id, then hand the user off to the provider.
var url = $"https://auth.example.com/authorize?client_id={Uri.EscapeDataString(clientId)}" +
	$"&redirect_uri={Uri.EscapeDataString(context.OAuth.RedirectUri)}" +
	$"&state={Uri.EscapeDataString(context.OAuth.State)}&response_type=code";
return ConfigFlowResult.External(url, resumeStepId: "authorize");

// Step 2: the host submits "authorize" once the callback arrives.
var code = context.OAuth.AuthorizationCode;
if (string.IsNullOrEmpty(code))
{
	return ConfigFlowResult.Error(WaitingStep(), Strings.Setup.AuthorizationNotCompleted());
}

var token = await ExchangeCodeAsync(clientId, clientSecret, code, context.OAuth.RedirectUri, cancellationToken);
return ConfigFlowResult.Complete("Example", new Dictionary<string, ConfigFlowValue>
{
	["access_token"] = ConfigFlowValue.Secret(token.AccessToken),
	["refresh_token"] = ConfigFlowValue.Secret(token.RefreshToken)
});
```

Macro Deck owns the redirect endpoint and matches the callback to your flow through `State`. You build the
provider's authorize URL and exchange the code; `AuthorizationCode` is `null` until the callback has
arrived. Show `RedirectUri` as a copy value when the user has to register it with the provider. Do not
start your own callback listener. The built-in Spotify integration is a complete example.

A flow that talks to the service while it runs, to test a connection or exchange a code, should send the
User-Agent the user configured: `context.Http.UserAgent`, the same value as `IIntegrationContext.Http`, also
before the integration was ever initialized. See
[Outgoing HTTP requests](https://docs.macro-deck.app/reference/plugin-hosting/#outgoing-http-requests).

### Reconfiguring an entry

```csharp
private static List<ActionParameter> Fields(IConfigFlowContext context)
{
	var fields = new List<ActionParameter>();
	if ((context as IConfigFlowEntryContext)?.EntryTitle is null)
	{
		// Creating a new entry: ask for a name. Editing: the entry already has one.
		fields.Add(ActionParameter.Text("name", label: Strings.Setup.ConfigurationName(), required: true));
	}

	fields.Add(ActionParameter.Text("host", label: Strings.Setup.Host(), required: true));
	fields.Add(ActionParameter.Secret("password", label: Strings.Setup.Password()));
	return fields;
}
```

When the user edits an existing entry, the same flow runs again, pre-filled with the stored values:

- **`IConfigFlowEntryContext.EntryTitle`** is the existing or host-requested entry name; `null` means the
  flow chooses a title for a new entry. The context is optional - always cast with `as`, and keep working
  with a plain `IConfigFlowContext` (older hosts and plugins omit it).
- **An existing entry keeps its title.** The title passed to `Complete` is used only for a new entry that
  has none.
- **A secret field left empty keeps its stored secret**, and a `ConfigFlowValue.Secret` for that field is
  ignored unless the user typed a new one.

### Optional settings

A flow can also be the settings page of an integration that already works without it: a few switches
that are off by default, an interval with a sensible default. Return `false` from
`RequiresConfiguration`, and `false` from `AllowsMultipleConfigurations` so there is only ever one
settings entry:

```csharp
public sealed class SystemMediaIntegration : IPluginIntegration, IConfigFlowProvider
{
	public bool RequiresConfiguration => false;

	public bool AllowsMultipleConfigurations => false;

	public IConfigFlow CreateConfigFlow() => new SystemMediaSettingsFlow();

	public async Task InitializeAsync(IIntegrationContext context)
	{
		var entry = (await context.Config.GetEntriesAsync()).FirstOrDefault();
		var cycleApps = entry is not null &&
			await context.Config.GetStringAsync(entry.Id, "cycle_apps") is "true";
		// No entry yet: run with the defaults.
	}

	// Other IPluginIntegration members omitted.
}
```

With `RequiresConfiguration` set to `false`:

- **The integration runs with no config entry.** It starts enabled like any integration without a flow,
  unless its metadata opts out of that. `GetEntriesAsync` returns an empty list until the user saves the
  flow, so read your defaults then. Nothing creates an entry for you.
- **It is never shown as needing setup.** Turning it on just turns it on, its actions and variables are
  available right away, and the flow stays on the integration page to change the settings.
- **Saving the flow enables and reinitializes the integration**, as it does for every flow, so
  `InitializeAsync` reads the new values. That also turns it back on if the user had turned it off.
- **Removing the entry keeps the integration running** and reinitializes it, so it falls back to the
  defaults. A required flow instead turns the integration off when its last entry goes.
- **Several entries are possible if you allow them.** With `AllowsMultipleConfigurations` left at `true`
  the user can add more than one, and `GetEntriesAsync` returns all of them; for settings that is rarely
  what you want.

`RequiresConfiguration` is read when the integration is discovered, so keep it side-effect free. Hosts up
to 3.0.0-beta.14 ignore it and treat every flow as required, so on those the integration still waits for
the flow to be completed once.

### Completing without an entry

Some integrations create their entries themselves, for example one per device as each device connects, so
the dialog has nothing to store. Finish such a flow with `CompleteWithoutEntry()`:

```csharp
public Task<ConfigFlowResult> SubmitAsync(string stepId,
	IReadOnlyDictionary<string, object?> input,
	IConfigFlowContext context,
	CancellationToken cancellationToken)
	=> Task.FromResult(ConfigFlowResult.CompleteWithoutEntry());
```

The result's `Kind` is `Complete` and `StoresEntry` is `false`. Macro Deck closes the dialog, discards the
collected values, creates or changes no entry and does not initialize the integration again. A flow that
edits an existing entry leaves that entry as it is. If the user switched the integration off and it has no
usable entry, completing the flow removes that stored choice: going through setup counts as wanting the
integration again. An integration with a usable entry the user switched off stays off.

A Macro Deck that predates `CompleteWithoutEntry` treats it like `Complete` without a title: it stores an
entry from the collected values under the integration's name, enables the integration and initializes it
again. If such an entry would break your integration, refuse it in `PrepareEntryAsync` or report it as not
usable with `IsEntryUsableAsync`.

### Taking part in storing an entry

A flow decides what an entry holds. To also decide whether it may be stored, report how each stored entry
is doing, or apply a change without being initialized again, implement `IConfigEntryLifecycle` on the
integration. Every member has a default, so override only what you need:

```csharp
public sealed class ServersIntegration : IPluginIntegration, IConfigFlowProvider, IConfigEntryLifecycle
{
	public Task<ConfigEntryPreparationResult> PrepareEntryAsync(ConfigEntryPreparation preparation,
		CancellationToken cancellationToken = default)
	{
		var key = KeyFor(preparation.Title, preparation.Siblings);
		if (key is null)
		{
			return Task.FromResult(ConfigEntryPreparationResult.Refuse(Strings.Setup.NameTaken()));
		}

		var values = new Dictionary<string, JsonElement>(preparation.Values)
		{
			["key"] = JsonSerializer.SerializeToElement(key)
		};
		return Task.FromResult(ConfigEntryPreparationResult.Accept(values,
			[VariableDefinition.Eager($"server_{key}_status", VariableType.Text)]));
	}

	public Task<ConfigEntryStatus> GetEntryStatusAsync(StoredConfigEntry entry,
		CancellationToken cancellationToken = default)
		=> Task.FromResult(_connections.TryGetValue(entry.Id, out var connection) && connection.IsOpen
			? ConfigEntryStatus.Connected
			: ConfigEntryStatus.Disconnected);

	public async Task<bool> ReloadEntriesAsync(CancellationToken cancellationToken = default)
	{
		await ReconnectChangedEntriesAsync(cancellationToken);
		return true;
	}

	// Other members omitted.
}
```

Macro Deck handles one change at a time per integration, in this order:

1. **`PrepareEntryAsync`** sees the entry about to be stored: its id, title and values, the stored entry when
   it is an edit, the other entries, and whether the title changed. Return the values to store, or refuse
   with a message the user sees. `ReservedVariables` names the global variables the entry will create:
   Macro Deck holds those names until the change ends and refuses the entry with its own message when
   another integration's variable or another entry's preparation already has one. A variable your
   integration already owns under the same id and type is not a conflict, so saving an entry again works.
2. The entry is stored.
3. **`ReloadEntriesAsync`** applies the change in the running integration. Return `true` when you did;
   `false`, the default, makes Macro Deck shut the integration down and initialize it again.
4. **`SynchronizeEntriesAsync`** receives every stored entry, for example to create the variables of a new
   entry and delete those of a removed one.
5. **`ReleasePreparationAsync`** ends the preparation, whether or not the entry was stored.

#### Synchronizing while the integration is off

Entries change while an integration is off too: the user can delete one, and an entry can be created before
the integration was ever initialized. Override the overload that takes the integration's own `IVariableApi`
and use it instead of `context.Variables`; it works whether or not the integration is initialized:

```csharp
public async Task SynchronizeEntriesAsync(IReadOnlyList<StoredConfigEntry> entries,
	IVariableApi variables,
	CancellationToken cancellationToken)
{
	var keys = entries.Select(KeyOf).OfType<string>().ToHashSet();
	foreach (var variable in await variables.GetAllAsync())
	{
		if (EntryKeyOf(variable.DefinitionId) is { } key && !keys.Contains(key))
		{
			await variables.DeleteAsync(variable.Id);
		}
	}

	foreach (var key in keys)
	{
		await variables.CreateAsync(VariableDefinition.Eager($"server_{key}_status", VariableType.Text));
	}
}
```

Macro Deck calls this overload; its default calls the overload without `variables`, so an integration written
before it keeps working unchanged. A Macro Deck that predates the overload calls the one without `variables`.
Out of process, `MacroDeck.Plugin.Hosting` passes the plugin's own variable api.

#### Choosing another name when one is taken

A name in `ReservedVariables` can be taken by a variable you cannot see from `Siblings`, such as a user
variable. By default Macro Deck then refuses the entry with its own message. To pick another name instead,
set `RetryOnConflict` on the result. Macro Deck then prepares the entry again, with every name it could not
hold so far in `RejectedVariableNames`:

```csharp
var rejected = preparation.RejectedVariableNames.ToHashSet();
var key = Candidates(preparation.Title)
	.FirstOrDefault(candidate => !rejected.Contains($"server_{candidate}_status"));
if (key is null)
{
	return Task.FromResult(ConfigEntryPreparationResult.Refuse(Strings.Setup.NoFreeName()));
}

return Task.FromResult(ConfigEntryPreparationResult.Accept(values,
	[VariableDefinition.Eager($"server_{key}_status", VariableType.Text)]) with { RetryOnConflict = true });
```

`RejectedVariableNames` is empty on the first attempt and only grows within the same change, so the
integration keeps no state of its own. Macro Deck stops after 32 attempts, or when an attempt adds no new
rejected name, and refuses the entry with its own message. Refuse it yourself first when you run out of
candidates, so the user sees your message. A Macro Deck that predates `RetryOnConflict` ignores it and
refuses the entry on the first conflict.

`GetEntryStatusAsync` is what the integration page shows next to each entry, and `IsEntryUsableAsync` says
whether an entry can be used as it is. An integration whose flow is required is turned off when none of its
entries is usable, and renaming an unusable entry stores the new title without running `PrepareEntryAsync`.
A secret field of a `StoredConfigEntry` holds the reference to the encrypted value, not the value; read it
with `GetSecretAsync`.

A plugin that implements the interface declares the `config-entries` capability. A Macro Deck that predates
it rejects the declaration and never calls these members, and a plugin that cannot be reached while an entry
is stored gets the defaults: the entry is stored as the flow completed it and the integration is
initialized again.

### Rendering the flow as a UI tree

Implement `IUiConfigFlowProvider` on the integration and `IUiConfigFlow` on the flow to draw the flow as a
Macro Deck UI tree; `describe` then reports `servesConfigUiTree`. The declared steps are still served
either way, `SubmitAsync` is still the only way values are accepted, and the tree cannot tell the host
which of its values are secret - return those as `ConfigFlowValue.Secret` on completion. See
[Serving a configuration view](https://docs.macro-deck.app/ui/views/configuration/).

### Over the plugin protocol

A config flow is one `config-flow` capability, driven by `flow.start`, `flow.submit` and `flow.abandon`.
Its `describe` result carries `allowsMultipleConfigurations`, `servesConfigUiTree` and
`requiresConfiguration`; a plugin that sends no `requiresConfiguration` has a required flow.
`MacroDeck.Plugin.Hosting` keeps one `IConfigFlow` per host-minted session id, resolves secrets to
plaintext before `flow.submit`, and forwards OAuth state and `EntryTitle`. `PluginTestHarness.ConfigFlow`
drives the same operations in tests - see [Testing](https://docs.macro-deck.app/features/testing/) and
[the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities).

`IConfigEntryLifecycle` is the separate `config-entries` capability, driven by `prepare`, `status`,
`usable`, `reload`, `synchronize` and `release`. The first integration of the plugin that implements it
answers them. `prepare` carries the optional `rejectedVariableNames` and its result the optional
`retryOnConflict`; a `Complete` result of `flow.submit` carries `withoutEntry: true` for
`CompleteWithoutEntry()`. All three are left out when unused. `PluginTestHarness.ConfigEntries` drives the
same operations in tests.

### See also

- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/)
- [Authentication](https://docs.macro-deck.app/reference/authentication/)
- [Serving a configuration view](https://docs.macro-deck.app/ui/views/configuration/)
- [Localization](https://docs.macro-deck.app/features/localization/)
- [Integration issues](https://docs.macro-deck.app/features/integration-issues/)

## Testing plugins

> Source: https://docs.macro-deck.app/features/testing/
>
> Test actions, variables, events, configuration and devices in process with PluginTestHarness and the MacroDeck.Plugin.Testing fakes, then run the conformance suite.

`MacroDeck.Plugin.Testing` runs your plugin's own code against a fake host, with no Macro Deck
installation and no socket. The project template's test project already references it and uses NUnit;
the package works with any test framework.

### Quick start

```csharp
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

public sealed class PluginIntegrationTests
{
	private static PluginTestHarness CreateHarness() =>
		PluginTestHarness.Create(builder => builder
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<PluginIntegration>());

	[Test]
	public async Task The_example_action_writes_the_message_to_the_log()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var outcome = await harness.Actions.ExecuteAsync(
			"log-message",
			new Dictionary<string, object?> { ["message"] = "Hello from a test" });

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(harness.Logs.Events.Any(e => e.Message.Contains("Hello from a test")), Is.True);
	}
}
```

`dotnet test` builds the plugin, runs the `log-message` action the way the host would and checks both
the result and the log line.

- **`Create` builds but does not start.** Call `InitializeIntegrationsAsync()` before invoking anything;
  an exception from an integration's `InitializeAsync` propagates to the test.
- **`harness.Context` is the fake host.** It replaces `IIntegrationContext`, and `harness.Clock` replaces
  `TimeProvider`. Neither substitution can be turned off.
- **Identity is generated.** Without a `PluginTestManifest` the harness writes one with a fresh, unique
  reverse-domain id, the name `Test Plugin` and version `1.0.0`. Pass your own only when the id, name,
  version, description or icon is what you test.
- **Logs are collected, not forwarded.** The harness replaces the Serilog pipeline, `UseMacroDeckLogging`
  included, with `harness.Logs`.

### Testing actions

```csharp
var outcome = await harness.Actions.ExecuteAsync("log-message",
	new Dictionary<string, object?> { ["message"] = "   " });

Assert.That(outcome.Succeeded, Is.False);
Assert.That(outcome.Error, Is.Not.Null);
```

Every client call returns a `CapabilityInvocationOutcome`: `Succeeded`, `Error`, `Data` (read it with
`DataAs<T>()`), `CorrelationId` and `Elapsed`. The harness enforces the invocation deadline but skips
concurrency limiting and idempotency replay. `harness.Actions` also has `GetOptionsAsync`,
`GetActionStateAsync` and `GetActionIconAsync`.

### Testing variables

```csharp
await harness.Actions.ExecuteAsync("ring", new Dictionary<string, object?>());

var reading = (await harness.Variables.GetAsync("rings")).DataAs<VariableReadingDto>();
Assert.That(reading!.Value.Number, Is.EqualTo(1));
```

`GetAsync` and `SetAsync` take the local id, not the variable name. `DiscoverAsync`, `ResolveAsync` and
`SubscribeAsync` cover [the catalog](https://docs.macro-deck.app/features/variables/#the-variable-catalog); a push-capable catalog
is attached to `harness.Context.VariableValues` during `InitializeIntegrationsAsync`.

### Testing events

```csharp
await harness.Actions.ExecuteAsync("ring", new Dictionary<string, object?>());

var published = harness.Context.Events.Published.Single();
Assert.That(published.EventId, Is.EqualTo("rang"));
Assert.That(published.Parameters!.Value.GetProperty("count").GetInt32(), Is.EqualTo(1));
```

`FakeEventPublisher` records every `Publish` in order and never throws, matching the real publisher's
fire-and-forget contract. Parameters are serialized with the protocol's own JSON options, so `Parameters`
is what the host would receive.

### Testing messaging

```csharp
harness.Context.Messages.RespondTo("obs.scene.current", _ => JsonSerializer.SerializeToElement("Live"));
await harness.InitializeIntegrationsAsync();

var reply = await harness.Context.Messages.DeliverRequestAsync("lights.state", sender: "com.example.deck");
Assert.That(harness.Context.Messages.Published.Select(message => message.Topic), Does.Contain("lights.changed"));
```

`harness.Context.Messages` is a `FakeMessageChannel`, and an injected `IMessageChannel` resolves to the same
instance. It routes the plugin's own messages the way Macro Deck does, answers everything else from
`RespondTo` stubs or with `NoHandler`, and records what the plugin publishes, sends and requests.
Deliver messages from other participants with its `Deliver*Async` methods rather than raw capability
invocations. Over the wire, `MacroDeckTestHost.Messaging` records and answers the hosted plugin's
messages, and `session.Messaging` delivers to it. On a host that offers the channel a plugin declares
the `messaging` capability too, so an assertion on its exact `Declared` list includes it. See
[Messaging between plugins](https://docs.macro-deck.app/features/messaging/#testing).

### Testing configuration

```csharp
await using var harness = CreateHarness();
var entry = harness.Context.Config.AddEntry("Front door");
harness.Context.Config.SeedString(entry, "room", "Hallway");

await harness.InitializeIntegrationsAsync();
```

Seed entries before `InitializeIntegrationsAsync` to test what the integration does with an existing
configuration; `SeedSecret` does the same for secrets. To drive the [setup flow](https://docs.macro-deck.app/features/setup-flows/)
itself, use `harness.ConfigFlow.StartAsync`, `SubmitAsync` and `AbandonAsync`.

### Testing log output

```csharp
Assert.That(harness.Logs.WithProperty("Room", "Hallway"), Has.Count.EqualTo(1));
Assert.That(harness.Logs.AtLeast(LogLevels.Warning), Is.Empty);
```

Property values are rendered as strings. `WaitForAsync` waits for a line logged from background work.

### Testing devices

```csharp
var devices = new FakeDeviceProviderContext();
var provider = new LightpadProvider();

await provider.InitializeAsync(devices);
var first = devices.AssignedIdOf("pad-1");
await provider.InitializeAsync(devices);

Assert.That(devices.AssignedIdOf("pad-1"), Is.EqualTo(first));
```

`FakeDeviceProviderContext` keeps the host's identity rules: registering again under a known
provider-local id is the same device, and unregistering keeps the device and only takes it offline.
`OpenSession` hands your provider a `FakeDeviceSession` to push surfaces to and read interactions from.
`InitializeIntegrationsAsync` does not initialize device providers, so call `InitializeAsync` yourself.

### Testing screensavers

```csharp
var screenSavers = new FakeScreenSaverProviderContext();
var provider = new PhotoIntegration();

await provider.InitializeAsync(screenSavers);

Assert.That(screenSavers.ScreenSavers.ContainsKey("photos"), Is.True);
Assert.That(screenSavers.Calls.Last().Kind, Is.EqualTo(ScreenSaverProviderCallKind.Register));
```

`FakeScreenSaverProviderContext` keeps the host's identity rules: registering again under a known
provider-local id replaces the screensaver, and unregistering an unknown id is a silent no-op. `Calls`
records every `ScreenSaverProviderCall` in order. `harness.Context.ScreenSavers` is the same fake behind a
whole harness, and `harness.ScreenSaverProvider`, a `ScreenSaverProviderTestClient`, drives the `screensaver-provider`
capability with `GetScreenSaversAsync`, the way the host reads your catalog after a reconnect. See [Screensavers](https://docs.macro-deck.app/ui/views/screensavers/).

### Testing video streams

```csharp
var videoStreams = new FakeVideoStreamProviderContext();
await new DoorCameraIntegration(server).InitializeAsync(videoStreams);

Assert.That(videoStreams.Providers.ContainsKey("door-cameras"), Is.True);
Assert.That(videoStreams.Calls.Last().Kind, Is.EqualTo(VideoStreamProviderCallKind.Register));
```

`FakeVideoStreamProviderContext` applies the SDK's and the host's rules: an invalid or duplicate provider
id, a seventeenth provider, and a stream or metadata value past a
[documented bound](https://docs.macro-deck.app/features/video-streams/#limits) throw `ArgumentException`, and unregistering an unknown
id is a silent no-op. `Calls` records every `VideoStreamProviderCall` in order, including the session
updates and closes your provider reports. The fake opens no sessions: in a harness,
`harness.VideoStreamProvider`, a `VideoStreamProviderTestClient`, drives the `video-stream-provider`
capability the way the host does, with `DescribeAsync`, `GetStreamsAsync`, `OpenSessionAsync`,
`SuspendSessionAsync`, `ResumeSessionAsync` and `CloseSessionAsync`, while
`harness.Context.VideoStreams` records what the plugin sends back. Neither fetches the URL your provider
returns: Macro Deck's relay does that, and the harness has none. Use a fresh session id per open; a
refusal is a failed outcome whose `details.reason` is a `video_stream_` reason. See
[Video streams](https://docs.macro-deck.app/features/video-streams/#testing).

### Testing batteries

```csharp
var batteries = new FakeBatteryProviderContext();
await new HeadsetIntegration(watcher).InitializeAsync(batteries);

Assert.That(batteries.Devices["pad-1"].LevelPercent, Is.EqualTo(80));
```

`FakeBatteryProviderContext` keeps the host's rules: publishing a known id replaces the device, a list is
applied all or nothing, and a provider holds at most 64 devices. `Devices`, `Publishes` and `RemovedIds`
record what your provider did. `FakeBatteryApi` is the reading side: `Set` replaces the catalog and raises
`Changed`, and `SubscriberCount` shows whether your code still listens. In a harness,
`harness.Context.Batteries` serves `IIntegrationContext.Batteries` and `harness.Context.BatteryProvider` is
what `InitializeIntegrationsAsync` starts your battery provider against. See
[Batteries](https://docs.macro-deck.app/features/batteries/#testing).

### Testing weather notices

```csharp
await harness.InitializeIntegrationsAsync();

Assert.That(harness.Context.WeatherProvider.SnapshotNotices, Is.EqualTo(1));
```

`FakeWeatherProviderApi` counts what a weather provider reports through
`IIntegrationContext.WeatherProvider`; in a harness it is `harness.Context.WeatherProvider`. Over the wire,
`MacroDeckTestHost` answers `weather`/`snapshots-changed` the way Macro Deck does, refusing it with
`CAPABILITY_UNAVAILABLE` when the plugin's `weather` capability was not negotiated. See
[Weather](https://docs.macro-deck.app/features/weather/#telling-macro-deck-the-weather-changed).

### Testing Companion devices

```csharp
var companion = new FakeCompanionDeviceApi();
var tablet = Guid.NewGuid();
companion.Connect(tablet, new CompanionDeviceState { ConfirmsCommands = true });
companion.OnRequest = (_, _) => CompanionDeviceCommandResult.Failed(CompanionDeviceFailure.ConsentDenied);

await new TabletDimmer(companion).DimAsync(tablet);

Assert.That(companion.Calls.Single().Kind, Is.EqualTo(FakeCompanionDeviceCallKind.Request));
```

`FakeCompanionDeviceApi` starts with access `Available` and no devices. `Connect`, `Report` and `Disconnect`
script the devices and raise the matching events, each connection with a new `ReadySequence`; `SetAccess`
changes access, and while it is `NotAllowed` requests and screenshots fail with `NotAllowed`. `OnRequest` and
`OnScreenshot` decide how requests and screenshots end, and `Calls` records every send, request and
screenshot. In a harness, `harness.Context.CompanionDevices` serves both `IIntegrationContext.CompanionDevices`
and an injected `ICompanionDeviceApi`, starting at `Unsupported` until the test calls `SetAccess`. See
[Companion devices](https://docs.macro-deck.app/features/companion-devices/#testing).

### Testing music player readers

`harness.Context.MusicPlayers` is a `FakeMusicPlayerApi` serving both `IIntegrationContext.MusicPlayers` and an
injected `IMusicPlayerApi`. `Set(players)` replaces the players and raises `InstancesChanged`,
`SetAlbumColor(instanceId, color)` sets what `GetAlbumColorAsync` answers, and `SubscriberCount` shows whether
your code still listens. See
[Reading every provider's players](https://docs.macro-deck.app/features/music-players/#reading-every-providers-players).

### Storage, time format and User-Agent

`harness.Context.Storage` is a `FakeIntegrationStorage` with Macro Deck's key rules and read outcomes:
`Set` seeds a document, `SetUnreadable` makes a key hold damaged copies, and `Get` reads what your
integration wrote - see [Integration storage](https://docs.macro-deck.app/features/integration-storage/#testing).
`harness.Context.Locale.TimeOfDayFormat` sets the time format `IIntegrationContext.Locale` answers, by default
the invariant culture with a 24-hour clock, and `harness.Context.Http.UserAgent` the User-Agent
`IIntegrationContext.Http` and an injected `IHostHttp` report.

### Testing calendars

```csharp
var outcome = await harness.Calendar.GetEventAsync(new CalendarEventArguments
{
	AccountId = accountId, CalendarId = "team", EventId = "standup"
});

Assert.That(outcome.DataAs<CalendarEventResult>()!.Event!.Participants, Has.Count.EqualTo(3));
```

`harness.Calendar`, a `CalendarTestClient`, drives the `calendar` capability the way the host does, with
`DescribeAsync`, `GetAccountsAsync`, `GetCalendarsAsync`, `GetEventsAsync` and `GetEventAsync`. The account
being read is in each call's arguments, a record from `MacroDeck.Plugin.Protocol.Capabilities.Calendar`.
Results are what the host receives: `events` returns summaries without description and participants, with
the reply limits applied, and an account id the plugin does not know is a failed outcome. See
[Calendars](https://docs.macro-deck.app/features/calendars/#testing).

### Testing email inboxes

```csharp
var outcome = await harness.EmailInbox.GetSnapshotAsync(new EmailInboxSnapshotArguments
{
	InboxId = inboxId, MaxMessages = 5, UnreadOnly = true
});

Assert.That(outcome.DataAs<EmailInboxSnapshotResult>()!.UnreadCount, Is.EqualTo(2));
```

`harness.EmailInbox`, an `EmailInboxTestClient`, drives the `email-inbox` capability the way the host does,
with `DescribeAsync`, `GetInboxesAsync` and `GetSnapshotAsync`. The inbox being read is in the arguments, a
record from `MacroDeck.Plugin.Protocol.Capabilities.EmailInbox`. Results are what the host receives: the
status as a name, at most the requested number of messages, newest first, with the reply limits applied, and
an inbox id the plugin does not know is a failed outcome. Raising `Changed` sends a `state.update` 250 ms
later, on `harness.Clock` in the harness and in `host.Messages` over the wire. See
[Email inboxes](https://docs.macro-deck.app/features/email-inboxes/#testing).

### Testing configuration entries

```csharp
var outcome = await harness.ConfigEntries.PrepareAsync(new ConfigEntryPrepareArguments
{
	EntryId = Guid.NewGuid(), Title = "Home", Values = new Dictionary<string, JsonElement>()
});

Assert.That(outcome.DataAs<ConfigEntryPrepareResult>()!.Success, Is.True);
```

`harness.ConfigEntries`, a `ConfigEntriesTestClient`, drives the `config-entries` capability the way the host
does while it stores an entry, with `PrepareAsync`, `GetStatusAsync`, `IsUsableAsync`, `ReloadAsync`,
`SynchronizeAsync` and `ReleaseAsync`. Set `RejectedVariableNames` on the arguments to test a repeated
`prepare`, and read `RetryOnConflict` from the result. `SynchronizeAsync` calls the `SynchronizeEntriesAsync`
overload that takes a variable api, backed by `harness.Context.Variables`, also when the integration was never
initialized. See
[Taking part in storing an entry](https://docs.macro-deck.app/features/setup-flows/#taking-part-in-storing-an-entry).

### Testing what a session shows on the pressing client

Pass a `FakeUiEventOrigin` to your session's `Dispatch(UiEvent, IUiEventOrigin)` and read `ReportedFailures`
and `OpenedModals`. Set `IsAttached = false` to test what happens once the client left, and `ModalAnswer` to
answer a dialog. `MacroDeckTestHost` has no clients, so over the wire it answers an origin's calls as Macro
Deck answers them for a client that is no longer attached.

### Testing previews

`session.Ui`, a `UiTestClient` on the session `MacroDeckTestHost` returns, lists the plugin's
[`[UiPreview]`](https://docs.macro-deck.app/ui/views/developer-preview/) scenarios and opens them the way Developer Tools does:

```csharp
var previews = await session.Ui.GetPreviewsAsync();
var outcome = await session.Ui.OpenPreviewAsync(previews[0].Id, previews[0].Profile);

Assert.That(outcome.Accepted, Is.True, outcome.FailureReason);
Assert.That(outcome.Tree!.Value.GetProperty("root").GetProperty("id").GetString(), Is.EqualTo("station"));

await session.Ui.CloseAsync(outcome.SessionId!);
```

`OpenPreviewAsync` waits for the first full tree. A scenario that throws, or an id the plugin does not
declare, comes back with `Accepted` false and the plugin's reason in `FailureReason`. Later patches are not
applied. `FindResource` returns the bytes of a resource the plugin registered, by the `resourceId` a tree
references. The host side of the tree exists only for sessions this client opens: a plugin that pushes a tree
on its own is still refused, as before. `macrodeck-plugin preview render` is built on this.

### Time and waiting

```csharp
harness.Clock.Advance(TimeSpan.FromSeconds(30));
await Wait.UntilAsync(() => harness.Context.Events.Published.Count > 0, because: "the poll should fire");
```

Advance the manual clock instead of sleeping. `Wait.UntilAsync` throws `PluginTestTimeoutException` at
its deadline instead of hanging.

### Protocol and process tests

| Tool | Use it for |
| --- | --- |
| `PluginTestHarness` | Everything above: fast, in process, no socket. Start here. |
| `MacroDeckTestHost.HostAsync` | The real protocol over loopback, plugin in process: serialization, reconnection, cancellation, timeouts, host callback round trips. |
| `MacroDeckTestHost.LaunchAsync` | A built executable or packed `.macroDeckPlugin`: startup, graceful shutdown, environment handoff, manifest loading. Keep these few. |

`PluginTestHarness.ProblemsOf(configure)` returns every configuration problem without throwing.

### The conformance run

```bash
macrodeck-plugin test --project src/Demo
```

```text
Macro Deck plugin conformance report (suite 1.3.0)
Plugin: com.example.demo 1.0.0
Passed: 25, Failed: 0, Skipped: 24
Conformant: yes
```

The [conformance suite](https://docs.macro-deck.app/reference/conformance/) checks the generic plugin contract, so do not repeat it
in your own tests. Test what is specific to your plugin, with fakes only at real external boundaries
(provider APIs, the file system). Options, filters and exit codes are in
[`macrodeck-plugin test`](https://docs.macro-deck.app/cli/test/).

### See also

- [Conformance suite](https://docs.macro-deck.app/reference/conformance/) - every check and the report format.
- [Logging and health](https://docs.macro-deck.app/features/logging/) - what the lines you assert on look like in production.
- [Sample plugins](https://docs.macro-deck.app/introduction/samples-and-template/) - complete test projects.
- [Debugging](https://docs.macro-deck.app/guides/debugging/) - run the plugin under an IDE against the stub or a real host.

## Variables

> Source: https://docs.macro-deck.app/features/variables/
>
> Declare variables with IVariableProvider - read-only and writable eager variables, attributes, testing, and the on-demand catalog.

An integration exposes variables by implementing `IVariableProvider`. For most plugins that means two
members: a list of `VariableDefinition`s and a `ReadAsync` that returns the current value of one of them.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Variables;

public sealed class MusicPlayerIntegration : IPluginIntegration, IVariableProvider
{
	private readonly PlaybackEngine _engine = new();

	public IReadOnlyList<VariableDefinition> Variables { get; } =
	[
		VariableDefinition.Eager("music_track", VariableType.Text) with { Id = "track" },
		VariableDefinition.Eager("music_is_playing", VariableType.Boolean) with { Id = "is-playing" },
		VariableDefinition.Eager("music_position", VariableType.Numeric, refreshInterval: TimeSpan.FromSeconds(1))
			with { Id = "position", Unit = "s", SemanticKind = VariableSemanticKinds.Duration }
	];

	public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
		=> ValueTask.FromResult(localId switch
		{
			"track" => VariableReading.Of(_engine.CurrentTrack.Title),
			"is-playing" => VariableReading.Of(_engine.IsPlaying),
			"position" => VariableReading.Of(_engine.PositionSeconds),
			_ => VariableReading.Unavailable
		});

	// IPluginIntegration members omitted.
}
```

The user now has `{{ vars.music_track }}`, `{{ vars.music_is_playing }}` and `{{ vars.music_position }}`.
The host calls `ReadAsync` for each variable on its own refresh interval - you never push eager values.

Three things to know:

- **`Name` is what the user types**, `music_track`. Lowercase, `[a-z0-9_]`, and prefix it with your
  plugin so it does not collide with another one.
- **`Id` is what `ReadAsync` receives** and what ends up in saved profiles. Leave it out and the host
  derives one from the name - but setting it explicitly keeps your `switch` readable and lets you rename
  the variable later without breaking anyone's configuration.
- **A value is a `string`, a number or a `bool`.** Anything else, and `VariableReading.Unavailable`, is
  shown as "not available" - use that for "no value right now" (not connected, not configured) rather
  than returning `""` or `0`.

### Defining a variable

`VariableDefinition.Eager(name, type, decimalPlaces, refreshInterval)` covers the common case; add
anything else with `with { ... }`.

| Property | What it does | Example |
| --- | --- | --- |
| `Name` | Variable name in templates. | `"weather_temperature"` |
| `Id` | Local id passed to `ReadAsync` / `SetValueAsync`. Stable once shipped. | `"temperature"` |
| `Type` | `Text`, `Numeric`, `Boolean` or `Color` - see [Color variables](#color-variables). | `VariableType.Numeric` |
| `DisplayName`, `Description` | Localized text shown in the variable picker. | `Strings.Variables.Temperature()` |
| `Unit` | Symbol shown next to the value, reachable as `vars.x.unit`. | `"°C"`, `"%"`, `"GB"` |
| `SemanticKind` | How the host formats it - see below. | `VariableSemanticKinds.Percentage` |
| `DecimalPlaces` | Digits shown for a numeric value. | `1` |
| `RefreshInterval` | How often the host calls `ReadAsync`. Host default when `null`. | `TimeSpan.FromSeconds(5)` |
| `Write` | Makes the variable writable - see [Writable variables](#writable-variables). | `new VariableWriteCapability()` |
| `Attributes` | Free-form strings, readable as `vars.x.<key>`. Not interpreted by the host. | `new Dictionary<string, string> { ["room"] = "office" }` |
| `Configuration` | Groups the variable under one configured instance (two OBS connections). | `new VariableConfiguration(entryId, "Studio PC")` |
| `IsShareable` | `false` keeps the variable on this Macro Deck: the user cannot share it with other Macro Decks, and one shared earlier is no longer served. Defaults to `true`. | `false` for a variable that mirrors another Macro Deck |

`SemanticKind` tells the host how to render a number; `Unit` is what it shows next to it:

| `SemanticKind` | `Unit` | stored | rendered |
| --- | --- | --- | --- |
| `duration` | `s` | `187` | `03:07` |
| `percentage` | `%` | `12.5` | `12.5 %` |
| `bytes` | `B` | `1536` | `1.5 KB` |
| `bytesPerSecond` | `B/s` | `3670016` | `3.5 MB/s` |
| `none` | `fps` | `60` | `60 fps` |

An unknown kind renders as a plain number with its unit, so naming a newer one is never an error. A host
built before `bytesPerSecond` existed shows such a value as `3670016 B/s`, which is why the unit is still
declared. Use
`bytes` only for a value that really is in bytes - a value already in GB is `none` with a `GB` unit.

A provider may declare at most `VariableLimits.MaxEagerVariablesPerProvider` (256) eager variables; the
host keeps the first 256 and logs an error. More than that belongs in [the catalog](#the-variable-catalog).

### Color variables

`VariableType.Color` holds a color. Its value is text, lowercase `#rrggbb` when opaque or `#rrggbbaa` with
alpha: return it from `ReadAsync` as a string, and expect one in `SetValueAsync`. The host also accepts
`#rgb`, `#rgba`, `rgb(...)` and `rgba(...)` from you and stores the canonical form; anything else is
invalid. Over the protocol the value travels as a `text` value, like any string.

Users can bind a widget's colors, folder and profile backgrounds, the accent color and action color
parameters to a Color variable. See [Colors from a variable](https://docs.macro-deck.app/guide/tips/#colors-from-a-variable) for
what they see.

A Macro Deck release from before `Color` drops a definition that declares it, with the rest of your
variables unaffected.

A script input can be a color too, `ScriptInputType.Color` with a value in the same format. A plugin built
on this SDK announces that it knows the type and sees such an input as `color`; an older plugin sees it as
`text` carrying the hex value.

#### Resolving colours yourself

Two places hand you colours already resolved: a `Color` [action parameter](https://docs.macro-deck.app/features/actions/) when the
action runs, and the widget data Macro Deck gives your widget's session. Anywhere else a colour may be a
reference string such as `{{ vars.primary | color | color_darken: 20 }}`: your own settings, a config or
setup flow, or a view of your own with
[`AllowVariables`](https://docs.macro-deck.app/ui/views/widget-configuration/#offering-a-colour-variable). Resolve those through
`IIntegrationContext.Colors`, an `IColorApi`:

```csharp
var color = await context.Colors.ResolveAsync(settings.LightColor) ?? "#ffffff";

_colorWatch = await context.Colors.WatchAsync(settings.LightColor, async (color, ct) =>
	await _lights.SetColorAsync(color ?? "#ffffff", ct));

// later, to stop:
await _colorWatch.DisposeAsync();
```

- Both take a fixed colour or a reference and return lowercase `#rrggbb` or `#rrggbbaa`, or `null` for "no
  colour, use your default": the variable is missing, unavailable or not a `Color`. Pass a `widgetId` to let
  that widget's own variables shadow global ones; an unknown widget gives `null`.
- `ColorReference.IsReference(value)` tells a reference from a fixed colour without asking the host.
- A watch's callback receives the current colour once, then again only when it changes, including to
  `null`. Watches survive reconnects and are released when the integration is shut down or initialized
  again; dispose one to stop it earlier. Callbacks run on thread-pool threads.
- A plugin may hold at most `ProtocolLimits.MaxColorWatches` (1024) watches across its integrations;
  `WatchAsync` throws `InvalidOperationException` above that.
- A reference is at most `ProtocolLimits.MaxColorReferenceLength` (1024) characters with at most
  `MaxColorReferenceSteps` (32) modifiers. A longer value is not a reference.
- On a Macro Deck release without colour resolution, a fixed colour still resolves locally, a reference
  gives `null`, and a watch delivers its value once.

In tests, `PluginTestHarness`'s `Context.Colors` is a `FakeColorApi`: seed a value with `Set(value, color)`,
which also notifies matching watches, and check `ActiveWatchCount`. Over the wire, `MacroDeckTestHost.Colors`
does the same with `SetAsync`, and `WatchesOf(pluginId)` lists a plugin's watches. Unseeded, a fixed colour
resolves to its canonical form and a reference to `null`.

```csharp
await harness.Context.Colors.Set("{{ vars.primary | color }}", "#3366ff");
```

### Writable variables

A writable variable is how a **Slider widget** gets two-way binding: the slider writes through
`SetValueAsync` and reads the real value back through `ReadAsync`. Declare `Write` and implement
`SetValueAsync`:

```csharp
public IReadOnlyList<VariableDefinition> Variables { get; } =
[
	VariableDefinition.Eager("music_volume", VariableType.Numeric) with
	{
		Id = "volume",
		Unit = "%",
		SemanticKind = VariableSemanticKinds.Percentage,
		Write = new VariableWriteCapability()
	}
];

public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
	=> ValueTask.FromResult(localId switch
	{
		// min, max and step give a bound Slider its range.
		"volume" => VariableReading.Of(_engine.VolumePercent, 0, 100, 1),
		_ => VariableReading.Unavailable
	});

public ValueTask<VariableWriteResult> SetValueAsync(string localId, object? value,
	CancellationToken cancellationToken = default)
{
	if (value is not (double or int or long))
	{
		return ValueTask.FromResult(VariableWriteResult.InvalidValue());
	}

	_engine.SetVolume((int)Convert.ToDouble(value, CultureInfo.InvariantCulture)); // clamps to 0-100
	return ValueTask.FromResult(VariableWriteResult.Applied());
}
```

- The host only calls `SetValueAsync` for a variable that declares `Write`; every other write is refused
  before it reaches you, so there is no need to check `localId` against a read-only list.
- `Applied` means you applied it. The host does not echo the requested value - the next `ReadAsync` is
  the truth, so clamping or rounding needs no extra work.
- The other results are `NotWritable`, `NotFound`, `Unavailable` (can write, just not right now - e.g.
  disconnected), `InvalidValue` and `Failed`. Never declare `Write` and then answer `NotWritable`: that is
  a slider that silently does nothing, and conformance check [MDC0314](https://docs.macro-deck.app/reference/conformance/) fails it.
- Set `Write = new VariableWriteCapability { CommitOnRelease = true }` when every intermediate value of a
  drag would be disruptive (seeking a track). Leave it off for volume, where live feedback is the point.

`Min`, `Max` and `Step` come from the reading rather than the definition because they can change - a
seek bar's maximum is the current track's length.

`Step` is the slider's default grid, not a guarantee: a user can give a bound slider a custom step, so
`SetValueAsync` may receive a value that is not a multiple of your step. It is always within `Min` and
`Max`. Round or reject it the way your target needs.

### Variables that depend on configuration

`Variables` may change with configuration. After the configuration changed, tell the host to read it
again with `context.Variables.NotifyDeclarationsChangedAsync()`. For a plugin this sends the same
`state.update` for the `variables` kind that `CatalogChanged(CapabilityKinds.Variables)` on an injected
`IPluginCatalogNotifier` sends, so it works with every Macro Deck version - the
[weather sample](https://docs.macro-deck.app/introduction/samples-and-template/) does this after its config flow. It is about the
declared eager set only; a catalog announces a changed set of resources with `InvalidateCatalogAsync`
(see [Push instead of poll](#push-instead-of-poll)).

### Reading again now

Macro Deck reads each eager variable at its `RefreshInterval`. When something changed what `ReadAsync`
would answer - a connection came up, a device reported new state - ask for every declared variable to be
read on the next poll instead:

```csharp
await context.Variables.RequestRefreshAsync(cancellationToken);
```

Requests made while one is still on its way are merged into one, so calling it from every callback of an
event stream is fine. It is best effort: it never throws because the request could not be delivered, and a
Macro Deck that predates it treats it as a no-op, so the variables are still read at their interval.
Pushed catalog resources are unaffected; publish those through the sink.

When a change affects only a few variables, name them by definition id so the rest keep their cadence:

```csharp
await context.Variables.RequestDefinitionRefreshAsync(["volume-percent", "muted"], cancellationToken);
```

Ids you do not declare are ignored and an empty list asks for nothing. Reading more than asked for is always
allowed: a pending request for every variable covers pending requests for some, and an `IVariableApi` that
does not override the member, or a Macro Deck that predates it, reads every declared variable instead.

### Names

A canonical variable name matches `^[a-z][a-z0-9_]*$`. `VariableNames.IsValid` checks one, and
`VariableNames.Sanitize` derives one from any text the way Macro Deck does: `vars.` is dropped, accents are
removed, letters are lowercased, every other character becomes `_`, runs of `_` collapse, and a leading digit
gets a `v_` prefix. The same text always gives the same name, so a name derived from a stable label stays
stable:

```csharp
var name = VariableNames.Sanitize($"{machineName} fps"); // "gaming_pc_fps"
```

`DeclaredVariables` is what the host shows for an integration that is not configured yet. It defaults to
`Variables`; override it only when `Variables` is empty until something is configured, and set
`VariablesDependOnConfiguration` when its names contain a `VariableNameTemplate` placeholder for a
per-instance segment.

### History of your own variables

```csharp
await using var window = await context.Variables.OpenHistoryAsync("weather_berlin_temperature", 40, cancellationToken);
window.Changed += (_, _) => Redraw(window.Values);
```

`OpenHistoryAsync` opens a rolling window on one of your own global numeric variables, for example to draw a
graph in a widget. Macro Deck samples the variable once per second while a window on it is open, so the
values are evenly spaced and the graph advances whether the value changes or not. `Values` holds at most the
requested number of samples, oldest first, and is empty until the variable first reads as a number. The
window may be opened before the variable exists. Dispose it when the graph is no longer shown.

A name that belongs to someone else throws a `VariableHistoryException` with `NotOwned`, and too many open
windows `LimitExceeded`. A Macro Deck that predates variable history, or an `IVariableApi` that does not
implement it, throws `Unsupported`; catch it and draw without a graph.

### Testing

`PluginTestHarness` reads and writes variables the way the host does:

```csharp
await using var harness = /* your harness setup */;
await harness.InitializeIntegrationsAsync();

var track = (await harness.Variables.GetAsync("track")).DataAs<VariableReadingDto>();
Assert.That(track!.Value.Text, Is.EqualTo("Intro"));

var written = (await harness.Variables.SetAsync("volume",
	new VariableValueDto { Kind = "number", Number = 35 })).DataAs<VariableSetResult>();
Assert.That(written!.Status, Is.EqualTo("Applied"));
```

`GetAsync` and `SetAsync` take the local id, not the name. The
[sample plugins](https://docs.macro-deck.app/introduction/samples-and-template/) test every variable they declare this way.

`FakeIntegrationContext.Variables` counts `RequestRefreshAsync` and `NotifyDeclarationsChangedAsync` calls in
`RefreshRequests` and `DeclarationChanges`, lists the ids of each `RequestDefinitionRefreshAsync` call in
`DefinitionRefreshRequests`, and keeps what `BindAsync` recorded in `Bindings`. `RecordSample` adds a sample to every history window open on a
name, and `OpenHistoryWindows` counts the windows that are not disposed yet.

### Templates

A variable is `{{ vars.<name> }}` in any template; its static attributes are suffixes on the same
reference: `{{ vars.cpu.unit }}`, `{{ vars.room_sensor.room }}`.

`vars.<name>.state` is computed by the host and tells an unavailable variable apart from an empty one:

| member | true when |
| --- | --- |
| `state.is_available` | the reference resolved to a value |
| `state.is_not_available` | it did not - unknown name, or a provider that went quiet |
| `state.is_empty` | it resolved **and** renders as zero characters |
| `state.is_not_empty` | it resolved **and** renders as at least one character |

```liquid
{% if vars.music_artist.state.is_not_empty %}By {{ vars.music_artist }}{% endif %}
```

Color filters derive a shade from a color. The value piped in must be a `Color` variable or a color
literal; a `Text` variable is refused even when it holds a hex value. `color` reads the value as it is, and
the result of every filter is `#rrggbb` or `#rrggbbaa`:

```liquid
{{ vars.primary | color | color_darken: 20 | color_opacity: 70 }}
{{ "#ff0000" | color_darken: 10 }}
```

| filter | argument |
| --- | --- |
| `color_lighten`, `color_darken` | percent of lightness to add or remove |
| `color_saturate`, `color_desaturate` | percent of saturation to add or remove |
| `color_opacity` | the alpha to set, in percent |
| `color_increase_opacity`, `color_reduce_opacity` | percent to move the alpha toward opaque, or to reduce it by |
| `color_hue` | degrees to rotate the hue |
| `color_mix` | another color (`"#ffffff"` or a Color variable such as `vars.other`) and the percent of it to blend in |

A missing, unavailable or invalid color renders as an empty string, which a color field treats as unset.

Because `state` is resolved first, an `Attributes` key named `state` is unreachable. `state` works on
`vars` references only, not on `event` parameters or script inputs.

### The variable catalog

Use the catalog when your variables are a runtime resource space too large to declare up front - Home
Assistant entities, OBS sources, MQTT topics. Nothing is registered until the user picks a resource in
the variable browser; only then does it become an ordinary `{{ vars.name }}` variable. A provider can
have eager variables and a catalog at the same time.

```csharp
public sealed class Foobar2000Integration : IPluginIntegration, IVariableProvider
{
	private readonly Foobar2000Client _client;

	public IReadOnlyList<VariableDefinition> Variables { get; } = [];

	public bool SupportsCatalog => true;

	public bool SupportsSearch => true;

	public string CatalogName => "foobar2000";

	public async ValueTask<VariableCatalogPage> DiscoverAsync(
		VariableCatalogQuery query,
		CancellationToken cancellationToken = default)
	{
		if (!_client.IsConnected)
		{
			return VariableCatalogPage.Empty;
		}

		// The client's cursor is handed straight through as the continuation token.
		var page = await _client.GetCustomTagsAsync(query.Search, query.PageSize, query.ContinuationToken,
			cancellationToken);

		return new VariableCatalogPage
		{
			Items = page.Tags
				.Select(tag => VariableDefinition.OnDemand(tag.Name, VariableType.Text) with
				{
					Name = $"foobar_{tag.Name}",
				})
				.ToList(),
			ContinuationToken = page.NextCursor,
		};
	}

	// A tag typed by hand or read from an old profile is still valid - resolve it.
	public ValueTask<VariableDefinition?> ResolveAsync(
		string localId,
		CancellationToken cancellationToken = default)
		=> ValueTask.FromResult(Foobar2000Tags.IsValidName(localId)
			? VariableDefinition.OnDemand(localId, VariableType.Text)
			: null);

	public async ValueTask<VariableReading> ReadAsync(
		string localId,
		CancellationToken cancellationToken = default)
		=> _client.IsConnected
			? VariableReading.Of(await _client.GetCustomTagValueAsync(localId, cancellationToken))
			: VariableReading.Unavailable;
}
```

#### Catalog rules

- **Ids.** A catalog id may contain anything except `::`, whitespace and control characters, up to
  `MacroDeckId.MaxResourceLocalIdLength` - `sensor.office_temperature` and GUIDs are fine. Encode names
  with spaces (`Main Camera` → `Main_Camera`) and decode them in `ResolveAsync`; an item with an invalid
  `Id` is dropped. Ids are local: the host adds and strips your integration's prefix.
- **Paging.** Return one page per `DiscoverAsync` call, at most `MaxVariableCatalogPageSize` items, and
  put your source's own cursor in `ContinuationToken`. It is opaque and never persisted.
- **Hierarchy.** `query.ParentId` is `null` for the roots, otherwise the node being opened. Set
  `IsContainer` on nodes with children and `IsBindable = false` on pure grouping nodes. A flat provider
  ignores `ParentId`.
- **Search.** Leave `SupportsSearch` off unless you honor `query.Search`; the host then shows no search
  box rather than filtering a single page.
- **`CatalogEntryCount`.** Return a total only when it is cheap; `null` otherwise. Without a total the
  host shows how many entries it has loaded so far, or no count at all when `SupportsSearch` is on,
  because a searchable catalog is only loaded as the user expands or searches it.
- **`ResolveAsync` returns `null` only for an invalid id.** A resource that is merely gone right now (an
  unplugged device, a disconnected integration) must still resolve: the binding then shows as unavailable
  and resumes on its own, while `null` makes it a broken reference the user has to fix. A plugin that is
  offline appears as unresolvable until it reconnects, whatever your code returns.

#### Push instead of poll

By default the host polls every bound resource with `ReadAsync`. A provider backed by an event stream
sets `SupportsPush => true` and publishes instead:

1. `OnAttachedAsync(sink)` hands you an `IVariableSink` once (only when both `SupportsCatalog` and
   `SupportsPush` are `true`).
2. `SubscribeAsync(localIds)` is called with the **complete** set of bound ids every time it changes (an
   empty set means "watch nothing"). Return the current values you already have, or an empty list.
3. Call `sink.PublishAsync` with values for ids in the latest set; others are dropped. Call
   `InvalidateCatalogAsync` when the set of resources itself changed.

Push applies to the catalog only - eager variables are always polled.

#### Resource lifetime

A resource that disappears keeps its binding and variable; it just reads as unavailable and resumes
without re-binding once it can be resolved and read again.

#### Recording bindings yourself

The user binds catalog resources in the variables view. An integration can record bindings itself, for
example to carry variables over from an older version that created them another way:

```csharp
var outcomes = await context.Variables.BindAsync(
[
	new VariableBindingRequest("entity/light.kitchen/state", "ha_light_kitchen", VariableType.Text)
	{
		MigratedFrom = "my-plugin/watched-entities-v1"
	}
], cancellationToken);
```

- The bindings always belong to the calling integration, and are recorded together or not at all.
- A resource the integration already has a binding for answers `AlreadyBound` and keeps its binding, even
  when the user renamed its variable since. Running the same migration twice is therefore safe.
- Every name must satisfy `VariableNames.IsValid` and every resource id must be a valid resource id;
  otherwise `ArgumentException` is thrown and nothing is recorded. A plugin sends at most 512 per call.
- Recording does not create the variables right away. Macro Deck creates them when it restores bindings,
  at the latest on its next start; a requested name another variable holds by then is replaced with one
  derived from it, as for any binding.
- `InvalidOperationException` means the bindings could not be stored. The default implementation, and a
  Macro Deck that predates the member, throw `NotSupportedException`. Keep the data you migrate from until a
  call succeeds, so the next start can try again.

### Over the plugin protocol

Each **eager** variable is declared as one capability, like an action. Catalog ids are never declared -
they travel in the operation arguments, which keeps a large catalog under `MaxDeclaredCapabilities`. A
provider with only a catalog or only on-demand variables therefore declares nothing; Macro Deck asks it for
`describe` when it connects and offers its variables from then on, so it needs no announcement. See
[the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities) for the
`describe`/`get`/`set`/`discover`/`resolve`/`subscribe` operations, the `variables`/`refresh` host operation
behind `RequestRefreshAsync` and `RequestDefinitionRefreshAsync` (with an optional `definitionIds` list), the
`variables`/`bind` operation behind `BindAsync`, the `variables`/`history.open`, `history.read` and `history.close` operations
behind `OpenHistoryAsync` (a plugin's window reads its samples once per second and ends with the
connection), and the `variable-values` host API.
Declare `host:variable-values` in [`manifest.json`](https://docs.macro-deck.app/reference/manifest/) when you use it.
`MacroDeckTestHost` drives all six operations; see [conformance](https://docs.macro-deck.app/reference/conformance/) for MDC0311, MDC0314,
MDC0315 and MDC0403, which also check a plugin whose variables come only from a catalog or on demand.

### Writing a user variable

To write a variable the **user** owns instead of declaring your own, use the user-variable API on
`IIntegrationContext`: `CreateAsync` creates one, `ApplyAsync` changes an existing one. Pass an owner
widget id (from `ActionExecutionContext.OwnerWidgetId`) to make it local to that widget, where it shadows
a global of the same name; the host refuses an unknown widget id.

`ApplyAsync`'s `Set` also works on provider variables that declare `Write`; `NotEditable` for the rest.
`Add`, `Toggle` and `Append` are user-variable only, because they compute from the last value the host
saw. A `Color` user variable takes `Set` only, with a value in the formats above. `Unavailable` means the owner accepts writes but could not take this one - retry later.

A user variable can read its value from a file. Without **Allow write-back** it is read-only: every
operation answers `NotEditable` and the file is left alone. With write-back it behaves like any other
user variable, and Macro Deck also writes the new value to the file. This needs no new SDK: a plugin built
against an older one gets the same `NotEditable` it already handles for read-only variables. A user
variable that renders a template is read-only the same way: every operation answers `NotEditable`, and
its value changes only when a variable its template reads changes. `CreateAsync` always creates a
variable that holds its own value.

## Video streams

> Source: https://docs.macro-deck.app/features/video-streams/
>
> Offer live video to Macro Deck with IVideoStreamIntegration and IVideoStreamProvider - streams and their state, sessions, the relay that carries the media, updates, limits, reconnects, older hosts, security and testing.

A video stream provider offers live video to Macro Deck: the scenes of an OBS instance, the cameras of
a video recorder, a capture device. You list the streams you have; when a consumer wants to show one,
Macro Deck opens a **session** on your provider, and you answer with the URL where the stream can be
fetched, as HLS or as MJPEG.

Macro Deck fetches the media itself and relays it to the consumer. The consumer only ever talks to Macro
Deck, never to your source: your URL never leaves the computer, so your source can listen on `127.0.0.1`
only, needs no firewall rule, has no address to guess per consumer and mints no credentials for clients.
Macro Deck also opens every session for the consumer and makes sure each one you opened is closed
exactly once.

### Quick start

An integration implements `IVideoStreamIntegration` and registers one `IVideoStreamProvider` per source
it talks to. The provider below offers two cameras over HLS:

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk;
using MacroDeck.Sdk.VideoStreams;

public sealed class DoorCameraIntegration(CameraServer server) : IPluginIntegration, IVideoStreamIntegration
{
	public Task InitializeAsync(IVideoStreamProviderContext context, CancellationToken cancellationToken = default)
		=> context.RegisterProviderAsync(new DoorCameras(server), cancellationToken);

	// IPluginIntegration members omitted.
}

public sealed class DoorCameras(CameraServer server) : IVideoStreamProvider
{
	public string Id => "door-cameras";

	public LocalizedText Name => Strings.Providers.DoorCameras();

	public Task<IReadOnlyList<VideoStreamDescriptor>> GetStreamsAsync(CancellationToken cancellationToken)
		=> Task.FromResult<IReadOnlyList<VideoStreamDescriptor>>(
		[
			new("front", LocalizedText.FromLiteral("Front door"), Width: 1920, Height: 1080),
			new("garage", LocalizedText.FromLiteral("Garage"), Width: 1280, Height: 720, HasAudio: true,
				State: server.IsOnline("garage") ? VideoStreamState.Connected : VideoStreamState.Disconnected)
		]);

	public Task<VideoStreamSessionDescription> OpenAsync(
		VideoStreamOpenRequest request,
		CancellationToken cancellationToken)
	{
		if (!request.AcceptedTransports.Contains("hls"))
		{
			throw new VideoStreamException(VideoStreamErrorCode.TransportNotAccepted, "Only HLS is served.");
		}

		// The server listens on 127.0.0.1 only: Macro Deck, not the consumer, fetches this URL.
		return Task.FromResult(
			VideoStreamSessionDescription.Hls($"http://127.0.0.1:{server.Port}/{request.StreamId}/index.m3u8"));
	}

	public Task CloseAsync(string sessionId, VideoStreamSessionReason reason, CancellationToken cancellationToken)
		=> Task.CompletedTask;
}
```

Things to know:

- **Order is fixed.** Macro Deck calls `IVideoStreamIntegration.InitializeAsync` after the integration's
  own `InitializeAsync`. Register what is configured then, and register or withdraw more later as the
  configuration changes; the context stays valid for as long as the integration runs.
- **A provider is a plain object**, not the integration. One integration can register several, for
  example one per OBS instance.
- **Every `OpenAsync` that returned a description gets exactly one `CloseAsync`.** Release what a session
  holds there and nowhere else - see [Sessions](#sessions).
- **Refuse with `VideoStreamException`.** Its `VideoStreamErrorCode` reaches the consumer; its message is
  diagnostic only and is not shown to anyone.

### Registering providers

| `IVideoStreamProviderContext` member | What it does |
| --- | --- |
| `RegisterProviderAsync` | Registers a provider. Returns `VideoStreamProviderRegistration(QualifiedId, ProviderId)`; the qualified id is `plugin.id::provider-id`. Throws `ArgumentException` for an invalid or duplicate id, or a seventeenth provider. |
| `UnregisterProviderAsync` | Withdraws a provider. Its open sessions are closed first, each with one `CloseAsync` and `ProviderRemoved`; a session whose open is still running is closed as soon as the open returns. Unknown ids are ignored. |
| `NotifyStreamsChangedAsync` | Tells Macro Deck the provider's streams changed. Macro Deck calls `GetStreamsAsync` again. |
| `UpdateSessionAsync`, `CloseSessionAsync` | Session calls from your side - see [Updates from the provider](#updates-from-the-provider). |

| `IVideoStreamProvider` member | Meaning |
| --- | --- |
| `Id` | Stable, unique among every provider your plugin registers across all its integrations. A resource local id: non-empty, at most 256 characters, no whitespace and no `::`. Consumers store it. |
| `Name`, `Description` | Shown in pickers, in the reader's own language. `Description` is optional. |

Registering again under the same id after unregistering is a new registration: Macro Deck closes every
session it had opened on the earlier one, even if both happened so quickly that it only saw the result.

Only providers of enabled integrations are listed and can be opened.

### Streams and their state

`GetStreamsAsync` returns the provider's streams right now, as `VideoStreamDescriptor` records:

| Parameter | Meaning |
| --- | --- |
| `Id` | Stable, unique within the provider: 1 to 256 characters, no control characters. Spaces are allowed, so a source's own name, such as an OBS scene name, can serve as the id. Consumers store it. |
| `Name`, `Description` | The stream as a picker shows it. |
| `Width`, `Height` | Native size in pixels, when known. Consumers use them to reserve the right aspect ratio before the first frame. |
| `HasAudio` | Whether the stream carries audio. |
| `State` | `Connected` (can be opened, the default), `Connecting`, `Disconnected` (the provider has no connection to its source) or `Unavailable` (the source does not offer it right now). |
| `Metadata` | Provider-defined, opaque to Macro Deck. |

Call `NotifyStreamsChangedAsync` whenever a stream is added or removed, or a stream's metadata or state
changes. The notification carries nothing: Macro Deck reads `GetStreamsAsync` again, and several
notifications in quick succession are coalesced into one read. A stream's `State` describes the source,
independent of any session; a consumer that shows it re-reads the list when it changes.

### Sessions

A session is one consumer showing one stream. Macro Deck mints its id and passes it to `OpenAsync` in
`VideoStreamOpenRequest.SessionId`; every later call for the session names it.

| Call | When | Your answer |
| --- | --- | --- |
| `OpenAsync` | A consumer starts showing a stream. | A `VideoStreamSessionDescription` whose transport is one of `AcceptedTransports`, or a `VideoStreamException`. |
| `SuspendAsync` | The consumer stopped showing the stream for now, for example because its page is hidden. | Pause whatever is expensive. The default does nothing and keeps the session running. |
| `ResumeAsync` | The consumer shows a suspended stream again. | A new description, or null when the previous one still works (the default). |
| `CloseAsync` | The session ended. | Release everything the session holds. |

**Exactly one close.** Every `OpenAsync` that returned a description is followed by exactly one
`CloseAsync` for that session id, unless you ended the session yourself with `CloseSessionAsync`. That
holds when the consumer went away while your `OpenAsync` was still running: the close then follows the
open's return. An `OpenAsync` that threw gets no `CloseAsync`.

`CloseAsync` tells you why in its `VideoStreamSessionReason`:

| Reason | Meaning |
| --- | --- |
| `ConsumerClosed` | The consumer closed the session. |
| `LeaseExpired` | The consumer stopped renewing the session, for example because it crashed. |
| `ConsumerDisconnected` | The consumer's connection to Macro Deck ended. |
| `ProviderRemoved` | You withdrew the provider, or the integration stopped, was disabled or is initializing again. |
| `HostDisconnected` | Your plugin lost its connection to Macro Deck; the session was opened on the earlier connection. |
| `HostShutdown` | Macro Deck is shutting down. |
| `Failed` | The session failed, for example because Macro Deck refused a description you returned. |

Calls for different sessions can run concurrently. Macro Deck bounds every call by a timeout, the
capability invoke timeout for a plugin and ten seconds for a built-in integration, and treats one that
times out as failed. A late `OpenAsync` that returns after its timeout still gets its
`CloseAsync`.

#### Choosing a transport

A consumer lists the transports it can play in `AcceptedTransports`, most preferred first: `hls` when its
device plays HLS natively, and `mjpeg` always. Pick the first one you serve, or refuse with
`TransportNotAccepted`. Macro Deck refuses any other transport the same way.

Build the description with a factory:

| Factory | Meaning |
| --- | --- |
| `VideoStreamSessionDescription.Hls(url)` | The URL of an HLS playlist. Every segment, key and map the playlist names must be on the same origin as the playlist. |
| `VideoStreamSessionDescription.Mjpeg(url)` | The URL of a `multipart/x-mixed-replace` stream of JPEG frames. |
| `VideoStreamSessionDescription.FromUrl(transport, url)` | Any transport delivered from a URL. Macro Deck plays `hls` and `mjpeg` only. |

The `Url` is an absolute `http` or `https` URL of at most 2048 characters, with no user info and no encoded
slash (`%2F`) in its path. It is required for `hls` and `mjpeg`; a `null` Url is reserved for source kinds
added later, and the description can gain members without breaking a plugin built against an earlier SDK.
A description that breaks a rule throws `ArgumentException` when you build it.

**Serve `mjpeg` as well.** It is the one transport every device Macro Deck supports can play, old tablets
included. Desktop browsers do not play HLS natively, so a stream that offers only HLS shows "cannot be
played on this device" there. See [What Macro Deck's clients play](#what-macro-decks-clients-play).

### The relay

Macro Deck fetches your URL and passes the bytes on. Consumers get a URL on Macro Deck itself, of the form
`/api/video-streams/relay/<token>/...`, so they never learn where your source is. What to rely on:

- **Bind to `127.0.0.1`.** The fetch starts on the computer that runs Macro Deck. Nothing needs to be
  reachable from the network, and there is no consumer address to work out.
- **The origin of your URL is pinned.** Macro Deck fetches only from that origin, using `GET` and `HEAD`. A
  redirect is followed only within the origin, at most three times; one to another origin fails.
- **HLS playlists are rewritten.** Every URI in a playlist, such as segments, `EXT-X-MAP` and `EXT-X-KEY`, is
  resolved against the playlist's own URL and sent through the relay, so relative, root-relative and
  absolute URIs all work. A URI on another origin fails the request with a 502, and so does the same host
  spelled differently, such as `localhost` in the playlist and `127.0.0.1` in your URL. Only `data:` and
  `skd:` URIs pass through untouched; any other scheme, such as `file:` or `javascript:`, fails the request
  with a 502.
- **Content types are checked.** A response that does not fit the session's transport fails with a 502:
  `multipart/x-mixed-replace` or `image/jpeg` for `mjpeg`; a playlist, `video/mp2t`, `video/mp4`,
  `video/iso.segment`, `audio/*`, `text/vtt` or `application/octet-stream` for `hls`. A playlist is found by
  its `.m3u8` path, its `mpegurl` type or, for a response typed `application/octet-stream`, `text/plain` or
  not at all, by `#EXTM3U` as its first line; it must start with that line and stay under 1 MiB, or the
  request fails with a 502. An error status from your source passes through, without its body, only when
  its content type is acceptable or missing. Responses carry `Cache-Control: no-store`,
  `X-Content-Type-Options: nosniff` and a sandboxing Content-Security-Policy.
- **Timeouts.** Your source has 15 seconds to start a response (a 504 otherwise), and media is cut when it
  sends nothing for 30 seconds; a playlist is exempt from the 30 seconds, because a live playlist may wait
  before it answers. A paused, static camera that sends no frame for that long is disconnected, and the
  client reconnects on its own; keep-alive frames avoid that.
- **Malformed requests never reach your source.** A path with an encoded slash or backslash (`%2F`,
  `%5C`, and a double-encoded `%252F`), a literal backslash or a control character gets a 404, as does a
  query with a raw line break or NUL, and so does a URL whose session has ended or is suspended. Your source
  is not contacted for any of them. Macro Deck's web server collapses dot segments (`.` and `..`) before the
  relay sees the path, so they cannot climb above your origin; a percent-encoded line break in a query is
  ordinary data and is forwarded as written.
- **Bounded concurrency.** At most 8 relayed requests run at once per session and 64 in all; beyond that
  the client is refused and retries.
- **One URL per session.** It stays the same while you change the URL or transport with
  `UpdateSessionAsync` or `ResumeAsync`, and stops working the moment the session ends or is suspended,
  which also aborts any request in flight.

**Browser connection limit.** Macro Deck's own listener speaks HTTP/1.1, and a browser opens about six
connections to one origin. Every live MJPEG widget holds one for as long as it plays, so a page with more
than a handful of live streams can starve its other requests. Streams that are scrolled out of sight or
covered suspend and release theirs. Serving Macro Deck over HTTPS lifts the limit, because HTTP/2 shares
one connection.

### Updates from the provider

Sources drop out. Report that on the sessions it affects, and the consumer can show it instead of a frozen
frame:

```csharp
await context.UpdateSessionAsync(sessionId, VideoStreamSessionState.Reconnecting,
	reason: VideoStreamSessionReason.ProviderReconnecting,
	message: Strings.Status.ObsReconnecting());

// Once the source is back, optionally with a new description Macro Deck fetches from instead:
await context.UpdateSessionAsync(sessionId, VideoStreamSessionState.Active, freshDescription,
	VideoStreamSessionReason.SourceRecovered);
```

`Reconnecting` means the session is interrupted and you are recovering it; `Active` means the consumer can
play again. Use `SourceLost` when the source stopped delivering and `SourceRecovered` when it delivers
again. `message` is text the consumer may show, in the reader's own language. An update for a session that
is no longer open is ignored. A new description is checked like the one from `OpenAsync`: a transport the
consumer did not accept, or a URL Macro Deck refuses, closes the session with `Failed`.

`CloseSessionAsync` ends a session from your side, with `ProviderClosed` unless you name another reason.
Macro Deck does not call `CloseAsync` for a session you closed yourself.

Updates you send while `OpenAsync` is still running are held and delivered in order after the open
returns. At most 64 are held per session; beyond that the session fails.

### Showing a stream in Macro Deck UI

Put a [`macrodeck.video-stream`](https://docs.macro-deck.app/ui/components/video-stream/) in any tree you draw - a widget type, a folder
view, a modal - and name the stream by your provider's qualified id and the stream's id:

```csharp
new UiVideoStream
{
    Key = "preview",
    Stream = UiValue.Of(new UiVideoStreamReference { Provider = registration.QualifiedId, Id = "Preview" }),
    Fill = true,
}
```

The client that draws the tree opens, suspends and closes the session itself. The view can name any
provider's stream, not only your own.

### What Macro Deck's clients play

Macro Deck's web client and desktop app, and the Companion app, offer two transports, most preferred first:

| Transport | Offered when | What the client does |
| --- | --- | --- |
| `hls` | The engine plays HLS natively and inline: Safari, iPhone and iPad, and the Android player. Desktop Chrome and Firefox do not. | Plays the relayed playlist in a muted video element. No HLS library is loaded. |
| `mjpeg` | Always | Shows the relayed stream as an image that keeps updating. |

**Every client resolves the relay URL against the origin it already uses for Macro Deck.** The `url` a
client receives is host-relative (or absolute) and never your URL, so a client implementer must not assume
a full address. The [Companion app](https://docs.macro-deck.app/guide/companion-app/) has to resolve it against its host address
for video to play on a phone.

A client that cannot play the transport you picked, for example because autoplay is blocked, closes the
session and opens a new one without that transport. Clients play every stream without sound, and a
client stops downloading as soon as it suspends, so your `SuspendAsync` can release what is expensive on
your side. A suspend can reach you up to about a minute late, or not at all when the session is closed
first.

### Limits

The SDK rejects a value past a bound with an `ArgumentException` before it is sent, and Macro Deck
refuses one that arrives anyway. The bounds are in
[`VideoStreamLimits`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/protocol/src/MacroDeck.Plugin.Protocol/Limits/VideoStreamLimits.cs);
the ones you are most likely to meet:

- At most **16 providers** per plugin.
- At most **256 streams** per provider. Macro Deck keeps the first 256 of a longer list and logs a warning.
- `Metadata`: at most **32 entries**, keys up to 64 and values up to 2048 characters.
- A description's `Url` up to **2048** characters.

Macro Deck also bounds what it asks of one plugin at once. Opens, suspends, resumes and stream reads run
at most eight at a time per plugin, and up to 256 more wait, each for at most the capability invoke
timeout; beyond that, the consumer is told the provider is busy. Closes have their own slots and are never
dropped. `video-streams` calls from your plugin have their own rate limit, apart from other host calls, so
a burst of updates cannot delay a button press. When Macro Deck rate limits a `RegisterProviderAsync`,
`NotifyStreamsChangedAsync`, `UpdateSessionAsync` or `CloseSessionAsync`, the SDK retries it a few times
over about a second and a half, keeping the session's messages in order, and then throws a
`VideoStreamException` with `Busy`. A session accepts no further updates once you call
`CloseSessionAsync`; if that close throws `Busy`, call it again to retry the close. The relay has its own
bounds, listed in [The relay](#the-relay).

### Errors

| `VideoStreamErrorCode` | Meaning | Worth retrying |
| --- | --- | --- |
| `Unsupported` | This Macro Deck, or this provider, does not support the operation. | No |
| `UnknownProvider`, `UnknownStream` | No provider or stream with that id. | No |
| `UnknownSession` | No session with that id is open, or it was already closed. | No |
| `StreamUnavailable` | The stream exists but cannot be served right now. | Yes |
| `TransportNotAccepted` | You serve none of the transports the consumer accepts, or Macro Deck does not play the one you returned. | No |
| `CapacityReached` | You cannot open another session right now. | Yes |
| `Busy` | You are busy. | Yes |
| `Failed` | Anything else. | No |

A session closed with `ProviderRemoved` can be opened again once the provider is listed again; consumers
treat that reason as retryable.

### Lifecycle

Your sessions end whenever the thing they depend on goes away:

| What happens | Your provider sees | The consumer sees |
| --- | --- | --- |
| You call `UnregisterProviderAsync` | `CloseAsync(ProviderRemoved)` per session | The session closed with `ProviderRemoved` |
| The integration stops, is disabled, or initializes again, for example after the user saved its configuration or after a reconnect that did not resume | `CloseAsync(ProviderRemoved)` per session, then every provider is withdrawn; a re-initialization registers them again | The session closed with `ProviderRemoved`; the provider returns once it is registered again |
| Your plugin loses its connection to Macro Deck | `CloseAsync(HostDisconnected)` per session | The session closed with `ProviderRemoved`, and the provider is not listed until the plugin is back |
| The plugin is uninstalled | `CloseAsync(ProviderRemoved)` per session | The session closed with `ProviderRemoved` |
| Macro Deck shuts down | `CloseAsync(HostShutdown)` per session, for at most two seconds | - |

Whenever a session ends, the relay URL stops working and any media still flowing for it is cut.

**Sessions do not survive a reconnect**, not even one that resumes the same plugin session. Your
registrations survive a resumed one: the SDK keeps your providers registered, and Macro Deck reads them back
once your plugin is connected again. A reconnect that does not resume initializes your integrations again,
which registers them afresh. Either way consumers open new sessions, so a provider never has to reconcile
a session across a connection it did not see end.

### Security

Any client that is signed in to Macro Deck, the desktop app or a paired device, can list your streams and
open a session on them, and then receives the media through the relay. So:

- Whatever your source serves is shown to every such client. Do not serve anything you would not show them.
- The client never sees your URL, so credentials in its query string stay with Macro Deck. Put a short-lived
  token in a URL only when your source needs one, scoped to the session and revoked in `CloseAsync`; never
  the source's own password or API key. Macro Deck never logs a description.
- The relay reaches whatever your URL points at, including other services on the computer or the local
  network. Point it only at your own source. See [the security model](https://docs.macro-deck.app/policies/security/#video-streams).

Declare `host:video-streams` in `manifest.json` so that people installing your plugin can see it offers
video streams:

```json
"permissions": ["host:video-streams"]
```

Macro Deck does not enforce it today.

### Built-in integrations

Macro Deck's own integrations implement the same `IVideoStreamIntegration` and `IVideoStreamProvider` and
are listed beside plugins; a consumer cannot tell them apart. There is no connection to lose in process, so
a built-in provider's sessions end with `ProviderRemoved`, `HostShutdown` or a consumer reason, never with
`HostDisconnected`. See [Capability parity](https://docs.macro-deck.app/reference/capability-parity/#video-stream-sessions).

### Older versions of Macro Deck

A Macro Deck that predates video streams rejects the `video-stream-provider` capability, and your plugin is
reported [partially incompatible](https://docs.macro-deck.app/policies/deprecations/) there: everything else it offers keeps working.
Nothing throws. `RegisterProviderAsync` returns a registration whose ids are both empty, and every other
context call does nothing, so one build of your plugin serves old and new hosts alike.

### Testing

`FakeVideoStreamProviderContext` applies the same registration and size rules as the SDK and Macro Deck,
and records every call:

```csharp
var context = new FakeVideoStreamProviderContext();
await new DoorCameraIntegration(server).InitializeAsync(context);

Assert.That(context.Providers.ContainsKey("door-cameras"), Is.True);
Assert.That(context.Calls.Last().Kind, Is.EqualTo(VideoStreamProviderCallKind.Register));
```

It does not open sessions. Drive them the way Macro Deck does, through `harness.VideoStreamProvider`, a
`VideoStreamProviderTestClient`:

```csharp
await harness.InitializeIntegrationsAsync();

var open = await harness.VideoStreamProvider.OpenSessionAsync("session-1", "door-cameras", "front", ["hls"]);
Assert.That(open.DataAs<VideoStreamSessionOpenResult>()!.Description.Transport, Is.EqualTo("hls"));

await harness.VideoStreamProvider.CloseSessionAsync("session-1", "door-cameras");
```

Use a fresh session id per open: an id that was closed before is refused, as it would be by Macro Deck.
A refusal arrives as a failed outcome whose `details.reason` is one of the `video_stream_` reasons.
`harness.Context.VideoStreams` is the fake behind the harness; it records what your plugin reports, such as
`SessionUpdate` and `SessionClose`. The harness does not relay anything: it shows the description you
returned, not what a client would fetch. See [Testing](https://docs.macro-deck.app/features/testing/#testing-video-streams).

### Over the plugin protocol

The capability kind is `video-stream-provider`, version 1, declared at local id `provider` by a plugin
whose integration implements `IVideoStreamIntegration`, and by no other. Macro Deck is the only writer of
its copy of your providers and streams: it reads them with the kind's operations, and your side only tells
it when to read again.

| Direction | Name | Operations |
| --- | --- | --- |
| Host to plugin | `video-stream-provider` capability | `describe`, `streams`, `session.open`, `session.suspend`, `session.resume`, `session.close` |
| Plugin to host | `video-streams` host API | `providers-changed`, `streams-changed`, `session-update`, `session-close` |

Failures are `CAPABILITY_UNSUPPORTED` for `Unsupported`, and otherwise `CAPABILITY_UNAVAILABLE` refined by
a `video_stream_` reason. Payloads, reasons and rules are in the
[WebSocket reference](https://docs.macro-deck.app/reference/websocket/#video-streams).

### At a glance

| Member | Package | What it is |
| --- | --- | --- |
| `IVideoStreamIntegration` | SDK | Implemented by an integration that offers video streams. |
| `IVideoStreamProvider` | SDK | One source of streams: lists them and serves sessions. |
| `IVideoStreamProviderContext` | SDK | Registers providers and reports streams, session updates and closes. |
| `VideoStreamDescriptor`, `VideoStreamState` | SDK | One stream and its state at the source. |
| `VideoStreamOpenRequest` | SDK | What `OpenAsync` receives: session id, stream id and accepted transports. |
| `VideoStreamSessionDescription` | SDK | Where Macro Deck fetches a session's media: `Hls`, `Mjpeg` or `FromUrl`. |
| `VideoStreamSessionState`, `VideoStreamSessionReason` | SDK | A session's state and why it changed or closed. |
| `VideoStreamException`, `VideoStreamErrorCode` | SDK | Refusing an operation. |
| `VideoStreamLimits` | Protocol | Every size bound. |
| `PluginPermissions.HostVideoStreams` | Packaging | The `host:video-streams` manifest permission. |
| `FakeVideoStreamProviderContext`, `VideoStreamProviderTestClient` | Plugin testing | See [Testing](#testing). |

## Virtual profiles

> Source: https://docs.macro-deck.app/features/virtual-profiles/
>
> Ship ready-made, read-only profiles with IProfileProvider - fixed layouts, folders, widgets and routed widget interactions.

:::note
Out-of-process plugins get **partial** support: profile catalogs and widget interactions work, but the
catalog is snapshot-backed and interactions are fire-and-forget. See
[Capability parity](https://docs.macro-deck.app/reference/capability-parity/).
:::

An integration ships ready-made profiles by implementing `IProfileProvider`. Macro Deck shows them next
to the user's own profiles, read-only and with a fixed layout, and it creates no profile file for them.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Profiles;

public sealed class StreamKitIntegration : IPluginIntegration, IProfileProvider
{
	private readonly StreamClient _stream = new();

	public IReadOnlyList<IActionDefinition> Actions { get; } = [];

	public IReadOnlyList<VirtualProfileDescriptor> GetProfiles() =>
	[
		new VirtualProfileDescriptor("stream-kit", "Stream Kit", ProfileLayout.Grid(rows: 2, columns: 4),
		[
			new VirtualFolderDescriptor("main", "Main",
			[
				new VirtualWidgetDescriptor("go-live", "ActionButton", PositionX: 0, PositionY: 0),
				new VirtualWidgetDescriptor("now-playing", "MusicPlayer", PositionX: 1, PositionY: 0, Width: 2)
			])
		])
	];

	public Task HandleWidgetInteractionAsync(string profileId, string folderId, string widgetId,
		WidgetInteraction interaction)
		=> widgetId == "go-live" && interaction.TriggerType == "press"
			? _stream.GoLiveAsync()
			: Task.CompletedTask;

	// IPluginIntegration members omitted.
}
```

The user now has a "Stream Kit" profile with a 2 x 4 grid they can't edit. Pressing "go-live" calls your
integration.

Things to know:

- **Ids are local.** The host prefixes profile, folder and widget ids as `integrationId::localId`. Don't
  use `::` in your ids, or the profile, folder or widget is skipped.
- **Interactions are routed to you, not executed.** Virtual widgets aren't stored by the host, so a
  trigger on one reaches `HandleWidgetInteractionAsync`. The default implementation does nothing.
- **Don't rely on `profileId`.** The host currently passes an empty string. Identify the widget by
  `folderId` and `widgetId`, which arrive as your local ids.

### Describing a profile

| Type | Members |
| --- | --- |
| `VirtualProfileDescriptor` | `Id`, `Name`, `Layout`, `Folders` |
| `ProfileLayout` | `Kind`, `Rows`, `Columns`, `RowsLocked`, `ColumnsLocked`. Create one with `ProfileLayout.Grid(rows, columns, locked = true)`. |
| `VirtualFolderDescriptor` | `Id`, `Name`, `Widgets`, `ParentId = null`, `Order = 0` |
| `VirtualWidgetDescriptor` | `Id`, `Type`, `PositionX`, `PositionY`, `Width = 1`, `Height = 1`, `Data = null` |

`LayoutKind.Grid` is the only layout today. Every folder uses the profile's rows and columns, and
`RowsLocked`/`ColumnsLocked` switch off the matching grid controls in the editor. Nest folders with
`ParentId`, and sort them with `Order`.

`Type` is a widget type name such as `"ActionButton"`, `"MusicPlayer"` or `"Slider"`. `Data` is the same
JSON payload a stored widget of that type carries. A type whose provider hasn't connected yet is passed
through unchanged rather than becoming a button, so it appears once that provider is available.

### Handling interactions

```csharp
public async Task HandleWidgetInteractionAsync(string profileId, string folderId, string widgetId,
	WidgetInteraction interaction)
{
	if (interaction.TriggerType != "press")
	{
		return;
	}

	switch ((folderId, widgetId))
	{
		case ("main", "go-live"):
			await _stream.GoLiveAsync();
			break;
		case ("main", "end"):
			await _stream.EndAsync();
			break;
	}
}
```

`TriggerType` uses the action button's trigger names, such as `"press"` and `"release"`. The host routes
action button triggers on a virtual widget here. A trigger for a widget id that isn't yours, or from a
disabled integration, reports a failed trigger to the client.

### Changing the profiles

`GetProfiles` is read every time the host lists profiles or opens a virtual folder, so returning a new
list is enough in process. Keep it cheap and side-effect free, and build it from state you already hold.
An out-of-process plugin must tell the host to read it again with
`CatalogChanged(CapabilityKinds.VirtualProfiles)` on an injected `IPluginCatalogNotifier`.

### Edge cases

- **A disabled integration's profiles disappear** from the list, along with their folders.
- **A profile id that `GetProfiles` no longer returns** opens with no folders.
- **Read-only means read-only.** The user can't move, add or edit widgets in a virtual profile. Offer
  configuration through your integration instead.
- **`ProviderName`** is optional. Leave it out and the integration's name (the manifest name for a plugin)
  is used.

### Over the plugin protocol

Capability kind `virtual-profiles`, with the `profiles` and `widget-interaction` operations. The profile
list is served from the last snapshot the plugin sent (see
[Snapshot-backed state](https://docs.macro-deck.app/reference/capability-parity/#snapshot-backed-state)). An interaction is
delivered fire-and-forget: the client is told the trigger succeeded once it is routed, whatever your
handler does. See [the WebSocket reference](https://docs.macro-deck.app/reference/websocket/#capabilities).

### See also

- [Music players](https://docs.macro-deck.app/features/music-players/) - the `MusicPlayer` widget a profile can include.
- [Actions](https://docs.macro-deck.app/features/actions/)
- [Capability parity](https://docs.macro-deck.app/reference/capability-parity/)
- [Testing](https://docs.macro-deck.app/features/testing/)

## Weather

> Source: https://docs.macro-deck.app/features/weather/
>
> Expose weather stations with IWeatherProvider and IWeatherStation - cached snapshots, forecasts, units and unavailability.

An integration exposes weather by implementing `IWeatherProvider`. It lists one
`WeatherStationInstance` per configured location and resolves each one to an `IWeatherStation` that
returns a `WeatherSnapshot`. Map your source's own condition codes and fields onto that snapshot; the
source itself stays inside your integration.

### Quick start

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Weather;

public sealed class RooftopWeatherIntegration : IPluginIntegration, IWeatherProvider
{
	private readonly RooftopStation _station = new(new RooftopClient("http://192.168.1.40"));

	public IReadOnlyList<IActionDefinition> Actions { get; } = [];

	public IReadOnlyList<WeatherStationInstance> GetInstances()
		=> [new WeatherStationInstance("rooftop", "Rooftop")];

	public IWeatherStation? GetStation(string instanceId)
		=> instanceId == "rooftop" ? _station : null;

	public Task InitializeAsync(IIntegrationContext context)
	{
		_station.Start();
		return Task.CompletedTask;
	}

	public Task ShutdownAsync() => _station.StopAsync();
}
```

The user can now pick "Rooftop" as the location of a **Weather widget**.

Things to know:

- **The interface gives you the widget only.** Variables such as `{{ vars.rooftop_temperature }}` come
  from your own [`IVariableProvider`](https://docs.macro-deck.app/features/variables/). The built-in Weather integration declares
  its `weather_*` variables itself, and its **Weather details** action lists only its own locations.
- **Return a cached snapshot.** The host reads every station about once a minute. Refresh on your own,
  slower schedule instead of fetching on every call.
- **Instance ids are local** (`"rooftop"`). The host qualifies them as `integrationId::rooftop` and saves
  them in widgets, so keep them stable.

### Pressing the widget

A Weather widget without a flow of its own opens details when pressed, if the station it shows comes
from a provider that names a details action. Declare one of your own actions as `DetailsAction`:

```csharp
public WeatherDetailsAction? DetailsAction { get; } = new("show-station", StationParameter: "station");
```

- The host resolves the station the widget shows: the station saved in the widget, or, when none is saved,
  the same first station the widget draws. It then runs that station's provider's action on the pressing
  client, with the station's qualified id (`integrationId::rooftop`) in `StationParameter`.
- Leave `DetailsAction` at its default `null` and pressing the widget runs nothing until the user adds a
  flow. The built-in Weather integration declares its **Weather details** action, which opens a dialog
  for its own locations.
- Only clients with a screen run it; a hardware deck does not. A flow the user added to the widget always
  wins.
- An action that shows a dialog opens it with `context.Ui.ShowModalAsync` and serves it from your own
  [`IUiProvider`](https://docs.macro-deck.app/ui/views/modal/), as the built-in Weather integration does.
- Out of process the action travels in the `weather` capability's `describe` result. A host older than
  this member ignores it, and a plugin built against an older SDK declares no details action.

### Implementing the station

```csharp
using MacroDeck.Sdk.Weather;

internal sealed class RooftopStation(RooftopClient client) : IWeatherStation
{
	private readonly CancellationTokenSource _stop = new();
	private volatile WeatherSnapshot _current = WeatherSnapshot.Unavailable("Rooftop");
	private Task _loop = Task.CompletedTask;

	public Task<WeatherSnapshot> GetSnapshotAsync(CancellationToken ct) => Task.FromResult(_current);

	public void Start() => _loop = Task.Run(() => RefreshLoopAsync(_stop.Token));

	public async Task StopAsync()
	{
		await _stop.CancelAsync();
		await _loop;
	}

	private async Task RefreshLoopAsync(CancellationToken ct)
	{
		using var timer = new PeriodicTimer(TimeSpan.FromMinutes(10));
		do
		{
			try
			{
				var r = await client.GetReadingAsync(ct);
				_current = new WeatherSnapshot
				{
					IsAvailable = true,
					LocationName = "Rooftop",
					Unit = TemperatureUnit.Celsius,
					Temperature = r.TemperatureC,
					Condition = r.IsRaining ? WeatherCondition.Rain : WeatherCondition.Clear,
					IsDay = r.IsDaylight,
					Humidity = r.HumidityPercent,
					WindSpeed = r.WindKmh,
					WindDirection = r.WindDegrees
				};
			}
			catch (HttpRequestException)
			{
				// Keep the last good snapshot. It stays unavailable only if we never had one.
			}
		}
		while (await WaitAsync(timer, ct));
	}

	private static async Task<bool> WaitAsync(PeriodicTimer timer, CancellationToken ct)
	{
		try
		{
			return await timer.WaitForNextTickAsync(ct);
		}
		catch (OperationCanceledException)
		{
			return false;
		}
	}
}
```

`WeatherSnapshot.Unavailable(locationName)` is the "no data" answer: `IsAvailable = false`, with only the
location name set. Start with it and keep the last good snapshot when a refresh fails, as the built-in
Open-Meteo station does. A brief outage then doesn't blank the widget.

### Telling Macro Deck the weather changed

Macro Deck reads your stations about once a minute on its own. After a station fetched new data, tell it
so, and Weather widgets show the new conditions at once instead of up to a minute later. If your
integration also declares weather variables, ask for those to be read again at the same moment, so a
widget whose states follow them never disagrees with the Weather widget.

```csharp
// at the end of each refresh, with the IIntegrationContext from InitializeAsync
_ = context.WeatherProvider.NotifySnapshotsChangedAsync();
_ = context.Variables.RequestRefreshAsync();
```

- `NotifySnapshotsChangedAsync` is best effort and never throws. Notices that arrive while one is pending
  are merged into one read, so calling it once per refresh is enough.
- It covers changed snapshots only. A changed list of stations is still a catalog change (see
  [Over the plugin protocol](#over-the-plugin-protocol)).
- A Macro Deck older than this member ignores the notice and keeps reading the stations once a minute.

### The snapshot

```csharp
new WeatherSnapshot
{
	IsAvailable = true,
	LocationName = "Berlin",
	Unit = TemperatureUnit.Celsius,
	Temperature = 18.4,
	ApparentTemperature = 17.1,
	Condition = WeatherCondition.PartlyCloudy,
	IsDay = true,
	Days = [new WeatherForecastDay(new DateOnly(2026, 9, 13), WeatherCondition.Rain, Min: 11, Max: 17)],
	Hours = [new WeatherHour(DateTimeOffset.Now, WeatherCondition.RainShowers, 16.2, PrecipitationProbability: 70)]
};
```

| Property | Meaning |
| --- | --- |
| `IsAvailable` | `false` when there is no data (network error, not loaded yet). |
| `LocationName` | Shown on the widget. |
| `Unit` | `Celsius` or `Fahrenheit`. Every temperature in the snapshot is already in this unit. |
| `Temperature`, `ApparentTemperature` | Current and "feels like". `null` when unknown. |
| `Condition` | A `WeatherCondition`, used to pick the icon. |
| `IsDay` | Picks the day or night icon variant. |
| `Days` | `WeatherForecastDay(Date, Condition, Min, Max)`, one per day. |
| `Hours` | `WeatherHour(Time, Condition, Temperature, PrecipitationProbability)` from the current hour on. May be empty. |
| `WindSpeed` | km/h with `Celsius`, mph with `Fahrenheit`. |
| `WindDirection` | Degrees the wind blows **from**: 0 = north, 90 = east. |
| `Humidity` | Relative humidity, 0-100. |
| `Precipitation` | This hour: mm with `Celsius`, inches with `Fahrenheit`. |
| `Sunrise`, `Sunset` | Today, with the location's own offset. |

Everything past `Days` is optional. Leave out what your source does not report, and consumers treat it
as missing. `WeatherCondition` values: `Unknown`, `Clear`, `MainlyClear`, `PartlyCloudy`, `Overcast`,
`Fog`, `Drizzle`, `Rain`, `FreezingRain`, `Snow`, `SnowGrains`, `RainShowers`, `SnowShowers`,
`Thunderstorm`. Map anything you can't place to `Unknown`.

### Edge cases

- **A station disappears.** Drop it from `GetInstances` and return `null` from `GetStation`. Widgets
  pointing at it show as unavailable.
- **The list is briefly empty** while your integration re-initialises. The host keeps showing the last
  stations and checks again shortly before blanking anything.
- **Invalid or duplicate ids** from `GetInstances` are skipped and logged.
- **Cancellation.** Honour the token in `GetSnapshotAsync` if you ever do real work there. Returning a
  cached value, as above, never blocks.
- **`ProviderName`** is optional. Leave it out and the integration's name (the manifest name for a plugin)
  is used.

### Over the plugin protocol

Weather is fully supported out of process (capability kind `weather`). An unreachable plugin's stations
read as an unavailable snapshot. The station list is a snapshot, so after your configuration adds or
removes a location, call `CatalogChanged(CapabilityKinds.Weather)` on an injected
`IPluginCatalogNotifier`. The [weather sample](https://docs.macro-deck.app/introduction/samples-and-template/) does exactly this.
See [Capability parity](https://docs.macro-deck.app/reference/capability-parity/).

`context.WeatherProvider.NotifySnapshotsChangedAsync()` sends the `weather` host api's `snapshots-changed`
operation (see [WebSocket protocol](https://docs.macro-deck.app/reference/websocket/#weather)). Macro Deck accepts it only from a
plugin whose `weather` capability was negotiated and answers `CAPABILITY_UNAVAILABLE` otherwise; an older
Macro Deck answers `CAPABILITY_UNSUPPORTED`. The SDK swallows both, so the call stays safe everywhere.

### See also

- [Variables](https://docs.macro-deck.app/features/variables/) - temperature and condition variables for templates.
- [Setup flows](https://docs.macro-deck.app/features/setup-flows/) - asking the user for a location.
- [Localization](https://docs.macro-deck.app/features/localization/)
- [Testing](https://docs.macro-deck.app/features/testing/)
