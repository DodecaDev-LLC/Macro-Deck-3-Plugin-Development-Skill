# Macro Deck 3 plugin cheatsheet

The code shapes you need most, distilled from the bundled docs and samples. Each section names the doc page
with the full rules; read it before relying on anything not shown here.

## Contents

1. Which interface for which goal
2. Project files
3. Program.cs and the integration
4. Actions (parameters, results, dynamic options)
5. Button states
6. Variables
7. Events
8. Setup flows and reading configuration
9. Integration issues
10. Telling the host a catalogue changed
11. Host APIs on IIntegrationContext
12. Localization
13. Logging
14. Testing
15. Macro Deck UI in one screen
16. CLI
17. Manifest

## 1. Which interface for which goal

Implement the interface on the integration class (the one passed to `RegisterIntegration<T>()`) unless the
row says otherwise. Doc paths below name a docs page by its site path: `features/actions.md` is the `## Actions`
section of `references/docs/features.md`, `ui/views/...` pages are in `ui-views.md`, `ui/components/...` in
`ui-components.md`, other `ui/...` pages in `ui.md`, `reference/...` in `reference.md`, and so on.
`references/INDEX.md` maps every page to its file. Samples are `references/samples/<name>.md`.

| User wants to... | Contract | Doc | Sample |
| --- | --- | --- | --- |
| Do something on a button press or in a flow | `IActionDefinition` + `IActionExecutor` (listed in `Actions`) | `features/actions.md` | all |
| Fill a dropdown from live data | `IDynamicOptionsActionDefinition` on the action | `features/actions.md` | all |
| Show on/off, muted, playing on a button | `IStateProviderActionDefinition` on the action | `features/button-states.md` | music player |
| Draw album art or images on a button | `IIconProviderActionDefinition` on the action | `features/button-icons.md` | |
| Configure an action with a rich UI | `IUiConfigurableActionDefinition` on the action | `ui/views/configuration.md` | |
| Expose `{{ vars.x }}` values / two-way sliders | `IVariableProvider` | `features/variables.md` | weather |
| Let users trigger automations | `IEventProvider` (+ `IDynamicEventOptionsProvider`) | `features/events.md` | weather, music |
| Ask for credentials, URLs, OAuth | `IConfigFlowProvider` returning an `IConfigFlow` | `features/setup-flows.md` | REST API |
| Tell the user what is broken and offer a fix | `IIntegrationIssueProvider` | `features/integration-issues.md` | REST API |
| Talk to other plugins | `IIntegrationContext.Messages` | `features/messaging.md` | |
| Navigate folders and profiles | `IIntegrationContext.Deck` | `features/deck.md` | virtual profile |
| Drive the Music Player widget | `IMusicPlayerProvider` | `features/music-players.md` | music player |
| Supply weather stations | `IWeatherProvider` | `features/weather.md` | weather |
| Supply calendar events | `ICalendarProvider` | `features/calendars.md` | |
| Offer generated profiles | `IProfileProvider` | `features/virtual-profiles.md` | virtual profile |
| Add a new deck widget type | `IWidgetTypeProvider` + `IUiProvider` | `ui/views/widget-types.md` | |
| Replace a folder's grid | `IFolderViewProvider` + `IUiProvider` | `ui/views/folder-views.md` | |
| Show a screensaver | `IScreenSaverProvider` + `IUiProvider` | `ui/views/screensavers.md` | |
| Open a modal from an action | `ActionExecutionContext.Ui` | `ui/views/modal.md` | |
| Connect hardware or a custom client | `IDeviceProvider` (+ `ILayoutProvider`) | `features/devices.md`, `features/layouts.md` | |
| Use Android devices over ADB | `IAndroidDeviceManager` from DI | `features/android-devices.md` | |
| Offer cameras or OBS scenes as video | `IVideoStreamIntegration`, `IVideoStreamProvider` | `features/video-streams.md` | |
| Import a user's Macro Deck 2 settings | `IMigrationProvider` | `features/settings-migrations.md` | |

## 2. Project files

```
MyPlugin/
  MyPlugin.slnx
  Directory.Build.props        net10.0, nullable, analyzers, warnings as errors where set
  Directory.Packages.props     one MacroDeckSdkVersion for every MacroDeck.* package
  src/MyPlugin/
    manifest.json              identity, icon, entrypoints per platform
    macrodeck-build.json       one publish target per entrypoint
    MyPlugin.csproj
    Program.cs
    PluginIntegration.cs
    Localization/Strings.resx  (+ Strings.<culture>.resx)
    Assets/icon.svg
    Properties/launchSettings.json   "Macro Deck - Real Host" profile
  tests/MyPlugin.Tests/        NUnit + MacroDeck.Plugin.Testing
```

`.csproj` essentials (versions come from `Directory.Packages.props`):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <AssemblyName>MyPlugin</AssemblyName>      <!-- must match manifest entrypoints -->
    <RootNamespace>MyPlugin</RootNamespace>    <!-- where the generated Strings class lives -->
  </PropertyGroup>
  <ItemGroup>
    <FrameworkReference Include="Microsoft.AspNetCore.App" />  <!-- not Microsoft.NET.Sdk.Web -->
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="MacroDeck.Plugin.Analyzers" PrivateAssets="all" />
    <PackageReference Include="MacroDeck.Localization" />
    <PackageReference Include="MacroDeck.Plugin.Hosting" />
    <PackageReference Include="MacroDeck.Plugin.Serilog" />
    <PackageReference Include="MacroDeck.Sdk" />
  </ItemGroup>
  <ItemGroup>  <!-- both required: the SDK reads them from the content root -->
    <Content Include="manifest.json" CopyToOutputDirectory="PreserveNewest" />
    <Content Include="Assets\icon.svg" CopyToOutputDirectory="PreserveNewest" />
  </ItemGroup>
</Project>
```

Add `MacroDeck.Ui` for UI views. Test project: `MacroDeck.Plugin.Testing`, NUnit (the template's choice).

## 3. Program.cs and the integration

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Serilog;

var builder = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<PluginIntegration>();

// Optional: ordinary ASP.NET Core DI before Build().
builder.Services.AddHttpClient<LightClient>(c => c.BaseAddress = new Uri("http://192.168.1.20/"));

var plugin = builder.Build();   // validates everything, throws one PluginConfigurationException
await plugin.RunAsync();
```

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using Serilog;

public sealed class PluginIntegration : IPluginIntegration
{
	private readonly ILogger _logger;

	// Built by DI: IHttpClientFactory, typed clients, IOptions<T>, IPluginCatalogNotifier, ILogger...
	public PluginIntegration(ILogger logger, LightClient client)
	{
		_logger = logger.ForContext<PluginIntegration>();
		Actions = [new SetBrightnessAction(client)];   // no I/O here
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

	// After a session exists; again after reconnects and config changes. Idempotent.
	public Task InitializeAsync(IIntegrationContext context) => Task.CompletedTask;

	public Task ShutdownAsync() => Task.CompletedTask;   // fast: stop work, release resources
}
```

Lifecycle: `connect -> session -> InitializeAsync`; session lost -> `ShutdownAsync` -> new session ->
`InitializeAsync`; shutdown -> `ShutdownAsync` -> exit. Invocations run concurrently, each in its own DI
scope. Details: `reference/plugin-hosting.md`.

## 4. Actions

```csharp
using System.Globalization;
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

internal sealed class SetBrightnessAction(LightClient client) : IActionDefinition
{
	public string Id => "set-brightness";                     // persisted; never rename
	public LocalizedText Name => Strings.Actions.SetBrightness.Name();
	public LocalizedText Description => Strings.Actions.SetBrightness.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Text("light", label: Strings.Actions.SetBrightness.Light.Label(), required: true),
		ActionParameter.Slider("brightness", 0, 100,
			label: Strings.Actions.SetBrightness.Brightness.Label(), defaultValue: 100),
	];

	public IActionExecutor CreateExecutor() => new Executor(client);

	private sealed class Executor(LightClient client) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (!client.IsConnected)
				return ActionResult.Failed(ActionErrorCodes.NotConnected, Strings.Errors.BridgeOffline());

			if (context.Parameters.GetValueOrDefault("light") is not string { Length: > 0 } light)
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.SetBrightness.Light.Label()));

			var brightness = Convert.ToDouble(context.Parameters.GetValueOrDefault("brightness") ?? 100,
				CultureInfo.InvariantCulture);

			await client.SetBrightnessAsync(light, brightness, context.CancellationToken);
			return ActionResult.Success();
		}
	}
}
```

- Parameter factories: `Text`, `MultilineText`, `Number`, `Slider`, `Toggle`, `Password`, `Secret`, `Choice`,
  `DynamicChoice`, `Autocomplete`, `MultiSelect`, `Color`, `File`, `Folder`, `Hotkey`, `Duration`, `DateTime`,
  `Json`, `Code`, `KeyValue`, `Object`, `Array`, `IpAddress`, `Url`, `Icon`, `Image`, `KeyboardSequence`,
  `KeyboardCombo`, `WidgetTarget`. Read values by name from `context.Parameters`; numbers may arrive as
  `int`, `long`, `double` or string, so convert with `CultureInfo.InvariantCulture`.
- `.OnlyWhen("auth", "header")` hides a field; hidden values are **still sent**. Validate combinations.
- Results: `Success()` / `Success(expectedStateId)`, `ActionResult.SucceededTask` (sync executors),
  `Failed(code, localizedMessage)`, `Accepted(localizedMessage)` only when completion cannot be confirmed.
- `ActionErrorCodes`: `NotConfigured`, `NotConnected`, `PermissionDenied`, `ProviderError`,
  `ProviderRejected`, `InvalidParameter`, `NotFound`, `Timeout`, `Unavailable`.
- `ActionExecutionContext`: `Parameters`, `CancellationToken`, `OwnerWidgetId`, `OriginClientId`,
  `Interactions`, `Ui` (the last two can be `null`: no one to ask), `CallDepth`.
- `Platforms` only when the action cannot exist elsewhere (`MacroDeckPlatform.All` by default).
- Bounded waits only; never poll unbounded inside an executor.

Dynamic options:

```csharp
internal sealed class JoinChannelAction(ChatClient client) : IDynamicOptionsActionDefinition
{
	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("channelId", label: Strings.Parameters.Channel(), required: true),
	];

	public async Task<DynamicOptionsResult> GetDynamicOptionsAsync(
		DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		if (!client.IsConnected)   // explain an empty list instead of returning nothing
			return new DynamicOptionsResult { Options = [], Error = Strings.Errors.NotRunning() };

		var channels = await client.GetChannelsAsync(cancellationToken);
		return new DynamicOptionsResult
		{
			Options = [.. channels.Select(c => new ActionParameterOption { Value = c.Id, Label = c.Name })],
			CacheSeconds = 15,
		};
	}
	// Id, Name, Description, CreateExecutor as usual.
}
```

`context.ParameterName` says which list; `CurrentParameters` holds the rest of the draft; `Filter` the typed
text. `AllowsCustomValue` permits values outside the list. Give an optional dynamic choice a `placeholder`.

## 5. Button states

```csharp
internal sealed class MicMuteAction(VoiceClient client) : IActionDefinition, IStateProviderActionDefinition
{
	private static readonly IReadOnlyList<ActionStateDefinition> States =
	[
		new("unmuted", MacroDeckStrings.States.Unmuted()) { DefaultAppearance = new ActionStateAppearance { BackgroundColor = "#2f855a" } },
		new("muted", MacroDeckStrings.States.Muted()) { DefaultAppearance = new ActionStateAppearance { BackgroundColor = "#c53030" } },
		new("unavailable", MacroDeckStrings.States.Unavailable()),
	];

	public Task<ActionStateSnapshot?> GetActionStateAsync(
		IReadOnlyDictionary<string, object?> parameters, CancellationToken cancellationToken)
	{
		var active = !client.IsConnected ? "unavailable" : client.IsMuted ? "muted" : "unmuted";
		return Task.FromResult<ActionStateSnapshot?>(new ActionStateSnapshot(States, active));
	}

	public TimeSpan StatePollInterval => TimeSpan.FromSeconds(1);   // a request; default 2 s
	// IActionDefinition members; the executor may return ActionResult.Success("muted").
}
```

Called with half-filled drafts (never throw) and polled while visible (never connect). `null` = nothing to
report. State ids are persisted. Prefer an `unavailable` state to `null` for transient failures. A plugin
cannot push a state; the host polls. Doc: `features/button-states.md`.

## 6. Variables

```csharp
using MacroDeck.Sdk.Variables;

public IReadOnlyList<VariableDefinition> Variables { get; } =
[
	VariableDefinition.Eager("acme_light_level", VariableType.Numeric) with
	{
		Id = "light-level",                         // what ReadAsync receives; stable
		Unit = "%",
		SemanticKind = VariableSemanticKinds.Percentage,
		DisplayName = Strings.Variables.LightLevel(),
		Write = new VariableWriteCapability(),      // only if SetValueAsync really applies it
	},
	VariableDefinition.Eager("acme_light_on", VariableType.Boolean) with { Id = "light-on" },
];

public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
	=> ValueTask.FromResult(localId switch
	{
		"light-level" => VariableReading.Of(_state.Level, 0, 100, 1),   // min, max, step for sliders
		"light-on" => VariableReading.Of(_state.IsOn),
		_ => VariableReading.Unavailable,
	});

public ValueTask<VariableWriteResult> SetValueAsync(string localId, object? value, CancellationToken cancellationToken = default)
{
	if (value is not (double or int or long)) return ValueTask.FromResult(VariableWriteResult.InvalidValue());
	_state.SetLevel(Convert.ToDouble(value, CultureInfo.InvariantCulture));
	return ValueTask.FromResult(VariableWriteResult.Applied());
}
```

- `Name` (`acme_light_level`) is what users type: lowercase `[a-z0-9_]`, prefixed with your plugin.
- Values are `string`, number or `bool`; use `VariableReading.Unavailable` for "no value now", not `""`/`0`.
- The host polls eager variables; you never push them. Max 256 eager per provider; beyond that, or for a
  runtime resource space (entities, sources, topics), use the catalog (`SupportsCatalog`, `DiscoverAsync`,
  `ResolveAsync`, optional push via `SupportsPush`). Doc: `features/variables.md`.
- Write results: `Applied`, `NotWritable`, `NotFound`, `Unavailable`, `InvalidValue`, `Failed`. Never declare
  `Write` and answer `NotWritable` (MDC0314).

## 7. Events

```csharp
using MacroDeck.Sdk.Events;

public IReadOnlyList<EventDefinition> EventDefinitions { get; } =
[
	new()
	{
		Id = "scene-changed",                                         // persisted in triggers
		Name = Strings.Events.SceneChanged.Name(),
		ConfigurationParameters = [ActionParameter.DynamicChoice("sceneId", label: Strings.Parameters.Scene(),
			placeholder: Strings.Parameters.AnyScene())],                // filter; empty = any
		PayloadParameters =
		[
			ActionParameter.DynamicChoice("sceneId", label: Strings.Parameters.SceneId()),
			ActionParameter.Text("sceneName", label: Strings.Parameters.Scene()),
		],
	},
];

public Task InitializeAsync(IIntegrationContext context)
{
	var events = context.Events;   // safe to keep
	_client.SceneChanged -= OnSceneChanged;   // InitializeAsync runs repeatedly
	_client.SceneChanged += OnSceneChanged;
	_events = events;
	return Task.CompletedTask;
}

private void OnSceneChanged(Scene scene) => _events?.Publish("scene-changed", new Dictionary<string, object?>
{
	["sceneId"] = scene.Id,
	["sceneName"] = scene.Name,   // keys must match PayloadParameters
});
```

`Publish` is fire-and-forget and never throws. A configuration parameter with the same name as a payload
parameter filters occurrences. For plugin-to-plugin signals use messaging, not events. Doc: `features/events.md`.

## 8. Setup flows and reading configuration

```csharp
using MacroDeck.Sdk.ConfigFlow;

public sealed class PluginIntegration : IPluginIntegration, IConfigFlowProvider
{
	public IConfigFlow CreateConfigFlow() => new ServerConfigFlow();   // one per setup session
	public bool AllowsMultipleConfigurations => false;                  // default true
	// public bool RequiresConfiguration => false;  // optional settings; integration runs without an entry

	public async Task InitializeAsync(IIntegrationContext context)
	{
		foreach (var entry in await context.Config.GetEntriesAsync())
		{
			var url = await context.Config.GetStringAsync(entry.Id, "server_url");
			var key = await context.Config.GetSecretAsync(entry.Id, "api_key");
			// connect one client per entry
		}
	}
	// Actions, ShutdownAsync...
}

internal sealed class ServerConfigFlow : IConfigFlow
{
	public Task<ConfigFlowResult> StartAsync(IConfigFlowContext context, CancellationToken ct)
		=> Task.FromResult(ConfigFlowResult.Step(Step()));

	public async Task<ConfigFlowResult> SubmitAsync(string stepId, IReadOnlyDictionary<string, object?> input,
		IConfigFlowContext context, CancellationToken ct)
	{
		var url = (input.GetValueOrDefault("server_url") as string ?? "").Trim();
		var key = input.GetValueOrDefault("api_key") as string ?? "";   // plaintext here; never log it
		if (!await ServerClient.CanConnectAsync(url, key, ct))
			return ConfigFlowResult.Error(Step(), Strings.Setup.CannotConnect());
		return ConfigFlowResult.Complete("Media server");   // plain string by design; fields persist automatically
	}

	private static ConfigFlowStep Step() => new()
	{
		StepId = "connection",
		Title = Strings.Setup.ConnectionTitle(),
		Fields =
		[
			ActionParameter.Url("server_url", label: Strings.Setup.ServerUrl(), required: true),
			ActionParameter.Secret("api_key", label: Strings.Setup.ApiKey(), required: true),   // stored encrypted
		],
	};
}
```

- Outcomes: `Step(step)`, `Error(step, message, fieldErrors)`, `External(url, resumeStepId)` (OAuth; use
  `context.OAuth.RedirectUri`, `.State`, `.AuthorizationCode`), `Complete(title, extraValues)` with
  `ConfigFlowValue.Secret(...)` / `.Plain(...)`.
- Dispatch on `stepId`; the Back button can resubmit earlier steps.
- A flow with a required configuration keeps the integration off until completed.
- Reconfigure: `(context as IConfigFlowEntryContext)?.EntryTitle`; empty secret field keeps the stored one.
- Write back with `SetStringAsync` / `SetSecretAsync` (rotated tokens). Doc: `features/setup-flows.md`.

## 9. Integration issues

```csharp
using MacroDeck.Sdk.Issues;

public Task<IReadOnlyList<IntegrationIssue>> GetIssuesAsync(CancellationToken ct = default)   // polled: cached state only
	=> Task.FromResult<IReadOnlyList<IntegrationIssue>>(_authExpired
		? [new IntegrationIssue
		{
			Id = "credentials-expired",
			Title = Strings.Issues.CredentialsExpired.Title(),
			Description = Strings.Issues.CredentialsExpired.Description(),
			Severity = IntegrationIssueSeverity.Error,
			ActionLabel = Strings.Issues.OpenSetup(),
		}]
		: []);

public Task<IssueResolution> ResolveIssueAsync(string issueId, CancellationToken ct = default)
	=> Task.FromResult(issueId == "credentials-expired"
		? IssueResolution.Ok(followUp: IssueResolutionFollowUp.StartConfigFlow)
		: IssueResolution.Failed(Strings.Issues.Unknown()));
```

Only report what needs the user; self-healing states belong in a variable. Never throw from
`GetIssuesAsync`. Doc: `features/integration-issues.md`.

## 10. Telling the host a catalogue changed

```csharp
using MacroDeck.Plugin.Hosting.Integrations.HostApis;   // IPluginCatalogNotifier (inject it)
using MacroDeck.Plugin.Protocol.Handshake;              // CapabilityKinds

_catalogNotifier.CatalogChanged(CapabilityKinds.Variables, reason: "config applied");
```

Needed when `Variables`, `EventDefinitions`, instances or profiles change outside a host call (after reading
config in `InitializeAsync`, a device appearing). The host describes concurrently with `InitializeAsync`, so
call it after config reads. Kinds include `Variables`, `Events`, `Weather`; see the weather sample.

## 11. Host APIs on IIntegrationContext

`Events` (publish, bindings), `Config` (entries, strings, secrets), `Variables` / `UserVariables`, `Deck`
(navigation, client positions), `Scripts`, `Widgets`, `Notifications` (`Notify(new UserNotificationRequest
{...})`), `Messages`. Each crosses the protocol: no hot loops. Round-trip calls can throw
`HostInvocationException` (rate limit, timeout, no connection); `Publish`, `Notify` and `CatalogChanged` never
throw. Cached getters (`Deck.GetFolders()`, `Scripts.GetScripts()`, `Widgets.GetWidgets()`) are empty until the
first push. `IAndroidDeviceManager` comes from DI instead. Docs: `features/index.md`, `features/deck.md`,
`features/messaging.md`, `reference/capability-parity.md`.

## 12. Localization

`Localization/Strings.resx` (required), dotted keys become nested members:

```xml
<data name="Actions.SetBrightness.Name" xml:space="preserve"><value>Set brightness</value></data>
<data name="Status.ConnectedAs" xml:space="preserve"><value>Connected as {userName}</value></data>
<data name="Status.Retries" xml:space="preserve">
  <value>Retry {attempt} of {limit}</value>
  <comment>[attempt:int][limit:int] Shown while reconnecting.</comment>
</data>
<data name="Status.Scenes.One" xml:space="preserve"><value>{count} scene</value><comment>[plural]</comment></data>
<data name="Status.Scenes.Other" xml:space="preserve"><value>{count} scenes</value><comment>[plural]</comment></data>
```

```csharp
Strings.Actions.SetBrightness.Name();
Strings.Status.ConnectedAs(userName: user);
Strings.Status.Retries(attempt: 2, limit: 5);
Strings.Status.Scenes(3);
MacroDeckStrings.Validation.Required(Strings.Actions.SetBrightness.Light.Label());
```

Translations: `Strings.de.resx`, `Strings.pt-BR.resx` (BCP-47, hyphen, never underscore). A key that is also a
group (`Filters` beside `Filters.Date`) is MDLOC008. `languages` in the manifest is generated. Missing
catalog at runtime shows `[[plugin:<id>:Key]]`. Doc: `features/localization.md`.

## 13. Logging

Inject Serilog `ILogger`, call `.ForContext<T>()`, use message templates (`"Set {Light} to {Level}"`). Lines
reach the host log viewer via `UseMacroDeckLogging()` and the console; never add a console sink. Never log
secrets. Forwarding minimum: `MacroDeck:Plugin:Logging:MinimumLevel`. Rate limit: 20 events/s per plugin
(burst 500). Health routes `/_macrodeck/health|ready|info|diagnostics` are served for you. Doc:
`features/logging.md`.

## 14. Testing

```csharp
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

private static PluginTestHarness CreateHarness() =>
	PluginTestHarness.Create(b => b
		.UseLocalization(Strings.LocalizationCatalog)
		.RegisterIntegration<PluginIntegration>());

[Test]
public async Task Set_brightness_fails_when_bridge_offline()
{
	await using var harness = CreateHarness();
	harness.Context.Config.SeedString(harness.Context.Config.AddEntry("Bridge"), "server_url", "http://x");  // before init
	await harness.InitializeIntegrationsAsync();

	var outcome = await harness.Actions.ExecuteAsync("set-brightness",
		new Dictionary<string, object?> { ["light"] = "desk", ["brightness"] = 40 });

	Assert.That(outcome.Succeeded, Is.False);
}
```

- `harness.Actions`: `ExecuteAsync`, `GetOptionsAsync`, `GetActionStateAsync`, `GetActionIconAsync`.
- `harness.Variables.GetAsync("local-id")` -> `.DataAs<VariableReadingDto>()`; `SetAsync(id, new VariableValueDto { Kind = "number", Number = 35 })`.
- `harness.Context.Events.Published`, `harness.ConfigFlow.StartAsync/SubmitAsync/AbandonAsync`,
  `harness.Issues.GetIssuesAsync/ResolveAsync`, `harness.Logs.Events / WithProperty / AtLeast`.
- Time: `harness.Clock.Advance(...)`, `Wait.UntilAsync(() => ..., because: "...")`. No `Task.Delay`.
- Over the wire: `MacroDeckTestHost.HostAsync` (protocol in process), `LaunchAsync` (built artifact).
- Do not re-test what the conformance suite checks. Doc: `features/testing.md`.

## 15. Macro Deck UI in one screen

Package `MacroDeck.Ui` (+ `MacroDeck.Ui.Testing`). An `IUiProvider` declares surfaces and creates a session
per request; `ViewSession` (the *Serving a view* section of `references/docs/ui-views.md`) adapts a reactive `UiView` to `IUiSession`.

```csharp
public sealed class CounterUiProvider : IUiProvider
{
	private readonly UiState<int> _count = new(0);

	public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
		[new() { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared }];

	public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken ct)
	{
		if (request.Surface.Kind != UiSurfaceKinds.Widget) return Task.FromResult<IUiSession?>(null);  // decline
		var root = new UiButton
		{
			Key = "counter",
			Events = [UiEventHandler.On(UiComponentEvents.Press, () => _count.Value++)],
			Children = [new UiTextRun { Key = "value", Text = UiText.From(() => _count.Value.ToString()), Size = 0.4 }],
		};
		return Task.FromResult<IUiSession?>(new ViewSession(new UiView(request.Surface, root)));
	}
}
```

- Surface kinds: `config`, `widget`, `preview`, `folder`, `screensaver`, `dialog`, `developer-preview`.
  Return `null` for anything you do not serve.
- Keys become node ids: stable, never index-based. Dispose the view when the session ends.
- Config trees never replace declared `Fields`/`Parameters` (they stay the fallback and mark secrets);
  top-level input keys must equal field names.
- Iterate with `[UiPreview]` scenarios and `dotnet watch` (Hot Reload). Docs: `ui/index.md`,
  `ui/views/*.md`, `ui/components/*.md`, `ui/concepts/*.md`.

## 16. CLI

| Command | Use |
| --- | --- |
| `macrodeck-plugin new --name ... --id ... --publisher ... --project-name ... --yes` | Scaffold |
| `macrodeck-plugin run --project src/X --stub-host` | Run without Macro Deck ("Session established") |
| `macrodeck-plugin run --project src/X [--watch]` | Run against the desktop app (pairing prompt, Developer Mode) |
| `macrodeck-plugin test --project src/X [--report markdown --output c.md]` | Conformance suite |
| `macrodeck-plugin build --output ../../artifacts [--rid osx-arm64]` | Build all platforms and pack (from the manifest's directory) |
| `macrodeck-plugin validate --artifact f.macroDeckPlugin [--level publication]` | Validate |
| `macrodeck-plugin inspect --artifact f.macroDeckPlugin` | What an install would find |
| `macrodeck-plugin preview ...` | Render widget previews to PNG for Store images |
| `macrodeck-plugin icon-pack ...` | Bundle icon packs |

Exit codes: 0 ok, 1 subject wrong, 2 usage, 3 unreadable input, 4 cancelled, 70 unexpected. Docs: `cli/*.md`.

## 17. Manifest

```json
{
  "$schema": "https://schemas.macro-deck.app/plugin-manifest-v1.schema.json",
  "manifestVersion": 1,
  "id": "com.acme.light-control",
  "name": "Acme Light Control",
  "version": "1.0.0",
  "description": "Control Acme lights from Macro Deck.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": { "executable": "runtimes/win-x64/Acme.LightControl.dll", "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" } },
    "osx-arm64": { "executable": "runtimes/osx-arm64/Acme.LightControl.dll", "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" } },
    "linux-x64": { "executable": "runtimes/linux-x64/Acme.LightControl.dll", "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" } }
  },
  "publisher": { "name": "acme" },
  "license": "MIT",
  "repository": "https://github.com/acme/light-control",
  "compatibility": { "macroDeck": ">=3.0.0-0" },
  "ai": { "interaction": false, "generatedContent": false, "generatedAssets": false }
}
```

- Runtime-required: `manifestVersion`, `id`, `name`, `version`, `entrypoints`. Publication-required:
  `description`, `icon`, `publisher`, `license`, `repository`, `compatibility`.
- Id: `^[a-z][a-z0-9]*(-[a-z0-9]+)*(\.[a-z][a-z0-9]*(-[a-z0-9]+)*)+$`, max 128.
- Declare `ai` explicitly (all `false` means "uses no AI"; omitted reads as "not declared").
- Host APIs that need it are declared in `permissions` (for example `host:variable-values`, `host:adb`).
- Generated by tooling, never hand-written: `files`, `signature`, `languages`.
- Each entrypoint needs a matching `macrodeck-build.json` target. Doc: `reference/manifest.md`.
