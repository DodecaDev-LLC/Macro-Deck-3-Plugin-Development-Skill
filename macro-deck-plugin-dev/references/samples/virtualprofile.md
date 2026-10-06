# Sample: MacroDeck.SampleVirtualProfilePlugin

The `MacroDeck.SampleVirtualProfilePlugin` sample plugin and its tests, one `## File: <path>` section per file. See `samples/README.md` for what each sample demonstrates.

Files:

- `src/MacroDeck.SampleVirtualProfilePlugin/Actions/AnnounceAction.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Actions/NavigateDeckAction.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Actions/RunScriptAction.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Actions/SetSceneAction.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Actions/StyleWidgetAction.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Assets/icon.svg`
- `src/MacroDeck.SampleVirtualProfilePlugin/ControlRoomIntegration.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Localization/Strings.resx`
- `src/MacroDeck.SampleVirtualProfilePlugin/MacroDeck.SampleVirtualProfilePlugin.csproj`
- `src/MacroDeck.SampleVirtualProfilePlugin/Profiles/ControlRoomProfile.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Program.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/Properties/launchSettings.json`
- `src/MacroDeck.SampleVirtualProfilePlugin/README.md`
- `src/MacroDeck.SampleVirtualProfilePlugin/Scenes/ControlRoomScenes.cs`
- `src/MacroDeck.SampleVirtualProfilePlugin/macrodeck-build.json`
- `src/MacroDeck.SampleVirtualProfilePlugin/manifest.json`
- `tests/MacroDeck.SampleVirtualProfilePlugin.Tests/ControlRoomIntegrationTests.cs`
- `tests/MacroDeck.SampleVirtualProfilePlugin.Tests/ControlRoomOverTheWireTests.cs`
- `tests/MacroDeck.SampleVirtualProfilePlugin.Tests/LocalizationTests.cs`
- `tests/MacroDeck.SampleVirtualProfilePlugin.Tests/MacroDeck.SampleVirtualProfilePlugin.Tests.csproj`

## File: src/MacroDeck.SampleVirtualProfilePlugin/Actions/AnnounceAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Notifications;

namespace MacroDeck.SampleVirtualProfilePlugin.Actions;

/// <summary>
/// Notifies the user through <c>IUserNotifier</c>. Notifying under a key replaces the previous
/// notification with that key instead of stacking a new one, which is also how a plugin expresses
/// progress - there is no separate progress contract.
/// </summary>
internal sealed class AnnounceAction(ControlRoomIntegration integration) : IActionDefinition
{
	public string Id => "announce";

	public LocalizedText Name => Strings.Actions.Announce.Name();

	public LocalizedText Description => Strings.Actions.Announce.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Text("title", label: Strings.Actions.Announce.Title.Label(), required: true, maxLength: 60),
		ActionParameter.MultilineText("message",
			label: Strings.Actions.Announce.Message.Label(),
			placeholder: Strings.Actions.Announce.Message.Placeholder()),
		ActionParameter.Choice("level",
			[
				new ActionParameterOption
				{
					Value = nameof(UserNotificationLevel.Info),
					Label = Strings.NotificationLevels.Info()
				},
				new ActionParameterOption
				{
					Value = nameof(UserNotificationLevel.Warning),
					Label = Strings.NotificationLevels.Warning()
				},
				new ActionParameterOption
				{
					Value = nameof(UserNotificationLevel.Error),
					Label = Strings.NotificationLevels.Error()
				}
			],
			label: Strings.Actions.Announce.Level.Label(),
			defaultValue: nameof(UserNotificationLevel.Info)),
		ActionParameter.Text("key",
			label: Strings.Actions.Announce.Key.Label(),
			description: Strings.Actions.Announce.Key.Description())
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	private sealed class Executor(ControlRoomIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (integration.Context is not { } integrationContext)
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.Unavailable,
					Strings.Errors.NotInitialized()));
			}

			if (context.Parameters.GetValueOrDefault("title") is not string { Length: > 0 } title)
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.Announce.Title.Label())));
			}

			// Notifying is fire-and-forget: it never throws, even with no connection, so there is nothing
			// to await and nothing to report back. Title and Message are plain strings on the request -
			// this text is what the user typed, already in its final form.
			integrationContext.Notifications.Notify(new UserNotificationRequest
			{
				Title = title,
				Message = context.Parameters.GetValueOrDefault("message") as string,
				Level = Enum.TryParse<UserNotificationLevel>(context.Parameters.GetValueOrDefault("level") as string, out var level)
					? level
					: UserNotificationLevel.Info,
				Key = context.Parameters.GetValueOrDefault("key") as string
			});

			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Actions/NavigateDeckAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Plugin.Hosting.Transport;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleVirtualProfilePlugin.Actions;

/// <summary>
/// Drives the deck of the client that pressed the button, through <c>IDeckNavigator</c>. The target
/// field only appears for the two kinds that need one, and its options come from the same host-pushed
/// cache <c>GetFolders()</c>/<c>GetProfiles()</c> read.
/// </summary>
internal sealed class NavigateDeckAction(ControlRoomIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	private const string FolderKind = "folder";
	private const string ProfileKind = "profile";
	private const string ParentKind = "parent";
	private const string BackKind = "back";

	public string Id => "navigate-deck";

	public LocalizedText Name => Strings.Actions.NavigateDeck.Name();

	public LocalizedText Description => Strings.Actions.NavigateDeck.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Choice("kind",
			[
				new ActionParameterOption { Value = FolderKind, Label = Strings.NavigationKinds.Folder() },
				new ActionParameterOption { Value = ProfileKind, Label = Strings.NavigationKinds.Profile() },
				new ActionParameterOption { Value = ParentKind, Label = Strings.NavigationKinds.Parent() },
				new ActionParameterOption { Value = BackKind, Label = Strings.NavigationKinds.Back() }
			],
			label: Strings.Actions.NavigateDeck.Kind.Label(),
			defaultValue: FolderKind,
			required: true),
		ActionParameter.DynamicChoice("targetId", label: Strings.Actions.NavigateDeck.TargetId.Label())
			.OnlyWhen("kind", FolderKind, ProfileKind)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	/// <summary>A folder's or profile's label is the name the user gave it, so it stays a literal.</summary>
	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		var deck = integration.Context?.Deck;
		var options = context.CurrentParameters.GetValueOrDefault("kind") as string == ProfileKind
			? deck?.GetProfiles().Select(profile => new ActionParameterOption { Value = profile.Id, Label = profile.Label })
			: deck?.GetFolders().Select(folder => new ActionParameterOption { Value = folder.Id, Label = folder.Label });

		return Task.FromResult(new DynamicOptionsResult { Options = [.. options ?? []] });
	}

	private sealed class Executor(ControlRoomIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (integration.Context is not { } integrationContext)
			{
				return ActionResult.Failed(ActionErrorCodes.Unavailable, Strings.Errors.NotInitialized());
			}

			var kind = context.Parameters.GetValueOrDefault("kind") as string ?? FolderKind;
			var targetId = context.Parameters.GetValueOrDefault("targetId") as string;

			if (kind is FolderKind or ProfileKind && string.IsNullOrWhiteSpace(targetId))
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					Strings.Actions.NavigateDeck.MissingTarget());
			}

			try
			{
				// OriginClientId names the client that pressed the button; navigating without it would move
				// every connected deck.
				var deck = integrationContext.Deck;
				await (kind switch
				{
					FolderKind => deck.ChangeFolderAsync(targetId!, context.OriginClientId, context.CancellationToken),
					ProfileKind => deck.ChangeProfileAsync(targetId!, context.OriginClientId, context.CancellationToken),
					ParentKind => deck.GoToParentAsync(context.OriginClientId, context.CancellationToken),
					_ => deck.GoBackAsync(context.OriginClientId, context.CancellationToken)
				});

				return ActionResult.Success();
			}
			catch (HostInvocationException exception)
			{
				return ActionResult.Failed(ActionErrorCodes.NotConnected, exception.Message);
			}
		}
	}
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Actions/RunScriptAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Plugin.Hosting.Transport;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleVirtualProfilePlugin.Actions;

/// <summary>
/// Runs one of the user's own scripts through <c>IScriptApi</c>. The option list comes from
/// <c>GetScripts()</c>, which is served from a host-pushed cache rather than a round trip - so it is
/// empty for a moment right after connecting, and that is expected rather than an error.
/// </summary>
internal sealed class RunScriptAction(ControlRoomIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "run-script";

	public LocalizedText Name => Strings.Actions.RunScript.Name();

	public LocalizedText Description => Strings.Actions.RunScript.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("scriptId", label: Strings.Actions.RunScript.Script.Label(), required: true)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	/// <summary>A script's name is the one the user gave it, so the option label is a literal.</summary>
	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		var scripts = integration.Context?.Scripts.GetScripts() ?? [];
		return Task.FromResult(new DynamicOptionsResult
		{
			Options = [.. scripts.Select(script => new ActionParameterOption { Value = script.Id, Label = script.Name })]
		});
	}

	private sealed class Executor(ControlRoomIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (integration.Context is not { } integrationContext)
			{
				return ActionResult.Failed(ActionErrorCodes.Unavailable, Strings.Errors.NotInitialized());
			}

			if (context.Parameters.GetValueOrDefault("scriptId") is not string { Length: > 0 } scriptId)
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.RunScript.Script.Label()));
			}

			try
			{
				// The script's own result is this action's result: a failing script must not look like a
				// successful button press.
				// ownerWidgetId is what a script declaring RunsOnWidget resolves "this widget" to, so passing
				// the triggering widget through is what makes such a script runnable from a deck button.
				return await integrationContext.Scripts.RunAsync(scriptId,
					originClientId: context.OriginClientId,
					ownerWidgetId: context.OwnerWidgetId,
					cancellationToken: context.CancellationToken);
			}
			catch (HostInvocationException exception)
			{
				return ActionResult.Failed(ActionErrorCodes.NotConnected, exception.Message);
			}
		}
	}
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Actions/SetSceneAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.SampleVirtualProfilePlugin.Scenes;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleVirtualProfilePlugin.Actions;

/// <summary>
/// The action counterpart to pressing a scene button in the virtual profile: both end in
/// <see cref="ControlRoomIntegration.ApplySceneAsync"/>, so a deck button and the profile cannot drift
/// apart.
/// </summary>
internal sealed class SetSceneAction(ControlRoomIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "set-scene";

	public LocalizedText Name => Strings.Actions.SetScene.Name();

	public LocalizedText Description => Strings.Actions.SetScene.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("scene", label: Strings.Actions.SetScene.Scene.Label(), required: true)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
		=> Task.FromResult(new DynamicOptionsResult
		{
			Options =
			[
				.. ControlRoomScenes.All.Select(scene => new ActionParameterOption
				{
					Value = scene.Id,
					Label = ControlRoomScenes.DisplayName(scene)
				})
			]
		});

	private sealed class Executor(ControlRoomIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("scene") is not string sceneId ||
				ControlRoomScenes.Find(sceneId) is not { } scene)
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.InvalidValue(Strings.Actions.SetScene.Scene.Label()));
			}

			await integration.ApplySceneAsync(scene, source: "action", context.CancellationToken);
			return ActionResult.Success();
		}
	}
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Actions/StyleWidgetAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Plugin.Hosting.Transport;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Widgets;

namespace MacroDeck.SampleVirtualProfilePlugin.Actions;

/// <summary>
/// Writes back to a widget the user owns, through <c>IWidgetApi</c>. The widget target parameter
/// defaults to <c>$self</c>, so the action styles the button it was triggered from unless another one
/// was picked, and an empty colour clears the override rather than setting one.
/// </summary>
internal sealed class StyleWidgetAction(ControlRoomIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	private const string WidgetParameter = "widget";
	private const string StateParameter = "state";

	public string Id => "style-widget";

	public LocalizedText Name => Strings.Actions.StyleWidget.Name();

	public LocalizedText Description => Strings.Actions.StyleWidget.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.WidgetTarget(WidgetParameter, label: Strings.Actions.StyleWidget.Widget.Label()),
		ActionParameter.Text("label", label: Strings.Actions.StyleWidget.LabelText.Label(), maxLength: 40),
		ActionParameter.Color("backgroundColor", label: Strings.Actions.StyleWidget.Background.Label(), supportsReset: true),
		ActionParameter.Icon("icon", label: Strings.Actions.StyleWidget.Icon.Label()),
		// The states a widget has are the widget's own, so they cannot be listed at declaration time -
		// GetDynamicOptionsAsync reads them off the target the user picked.
		ActionParameter.DynamicChoice(StateParameter,
			label: Strings.Actions.StyleWidget.State.Label(),
			placeholder: Strings.WidgetStates.Current())
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	/// <summary>
	/// The two sentinels every widget accepts, followed by whatever states this particular widget
	/// declares. A widget with a single appearance reports none, and then only the sentinels are offered.
	/// </summary>
	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		List<ActionParameterOption> options =
		[
			new() { Value = WidgetStates.Current, Label = Strings.WidgetStates.Current() },
			new() { Value = WidgetStates.All, Label = Strings.WidgetStates.All() }
		];

		var target = context.CurrentParameters.GetValueOrDefault(WidgetParameter) as string;
		var widget = integration.Context?.Widgets.GetWidgets()
			.FirstOrDefault(candidate => string.Equals(candidate.Id, target, StringComparison.Ordinal));

		// A state's label is the one the deck author gave it, so it stays a literal.
		options.AddRange(widget?.States.Select(state => new ActionParameterOption
		{
			Value = state.Id,
			Label = state.Label
		}) ?? []);

		return Task.FromResult(new DynamicOptionsResult { Options = options });
	}

	private sealed class Executor(ControlRoomIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (integration.Context is not { } integrationContext)
			{
				return ActionResult.Failed(ActionErrorCodes.Unavailable, Strings.Errors.NotInitialized());
			}

			var target = context.Parameters.GetValueOrDefault(WidgetParameter) as string;
			var widgetId = WidgetTargets.IsSelf(target) || string.IsNullOrWhiteSpace(target)
				? context.OwnerWidgetId
				: target;

			if (widgetId is null)
			{
				// $self only resolves for a widget-triggered run; a script or an automation has no owner.
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter, Strings.Actions.StyleWidget.NoWidget());
			}

			var background = context.Parameters.GetValueOrDefault("backgroundColor") as string;
			var clear = WidgetAppearanceValues.IsReset(background)
				? new[] { WidgetAppearanceProperty.BackgroundColor }
				: [];

			// StateIds, not the deprecated State selector: a widget's states are addressed by their own
			// stable ids now, and the two sentinels cover "whichever it shows" and "all of them".
			var stateId = context.Parameters.GetValueOrDefault(StateParameter) as string;
			var request = new WidgetAppearanceRequest
			{
				WidgetId = widgetId,
				StateIds = [string.IsNullOrWhiteSpace(stateId) ? WidgetStates.Current : stateId],
				ClearProperties = clear,
				Patch = new WidgetAppearancePatch
				{
					Label = context.Parameters.GetValueOrDefault("label") as string,
					BackgroundColor = clear.Length == 0 ? background : null,
					IconId = context.Parameters.GetValueOrDefault("icon") as string
				}
			};

			try
			{
				var applied = await integrationContext.Widgets.ApplyAsync(request, context.CancellationToken);
				return applied
					? ActionResult.Success()
					: ActionResult.Failed(ActionErrorCodes.NotFound,
						Strings.Actions.StyleWidget.UnknownWidget(widgetId));
			}
			catch (HostInvocationException exception)
			{
				return ActionResult.Failed(ActionErrorCodes.NotConnected, exception.Message);
			}
		}
	}
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Assets/icon.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
	<rect x="8" y="10" width="22" height="20" rx="4" fill="#D0021B" />
	<rect x="34" y="10" width="22" height="20" rx="4" fill="#4A4A4A" />
	<rect x="8" y="34" width="22" height="20" rx="4" fill="#4A4A4A" />
	<rect x="34" y="34" width="22" height="20" rx="4" fill="#4A4A4A" />
</svg>
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/ControlRoomIntegration.cs

```csharp
using MacroDeck.Plugin.Hosting.Integrations;
using MacroDeck.Plugin.Hosting.Integrations.HostApis;
using MacroDeck.Plugin.Hosting.Transport;
using MacroDeck.Plugin.Protocol.Handshake;
using MacroDeck.SampleVirtualProfilePlugin.Actions;
using MacroDeck.SampleVirtualProfilePlugin.Profiles;
using MacroDeck.SampleVirtualProfilePlugin.Scenes;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Events;
using MacroDeck.Sdk.Notifications;
using MacroDeck.Sdk.Profiles;
using MacroDeck.Sdk.Variables;
using Serilog;

namespace MacroDeck.SampleVirtualProfilePlugin;

/// <summary>
/// A virtual profile the plugin owns, plus the callbacks that go the other way: a plugin does not only
/// answer the host, it drives the deck, styles widgets, runs scripts, writes variables and notifies the
/// user. Pressing a scene button in the profile and running the "set scene" action end in the same
/// place, so the two directions stay visibly consistent.
/// </summary>
public sealed class ControlRoomIntegration : IPluginIntegration, IProfileProvider, IVariableProvider, IEventProvider
{
	internal const string SceneChangedEventId = "scene-changed";

	private const string SceneVariableName = "sample_control_room_scene";

	private readonly IPluginCatalogNotifier _catalogNotifier;
	private readonly ILogger _logger;

	private IIntegrationContext? _context;

	public ControlRoomIntegration(IPluginCatalogNotifier catalogNotifier, ILogger logger)
	{
		_catalogNotifier = catalogNotifier;
		_logger = logger.ForContext<ControlRoomIntegration>();
		Actions =
		[
			new SetSceneAction(this),
			new StyleWidgetAction(this),
			new AnnounceAction(this),
			new RunScriptAction(this),
			new NavigateDeckAction(this)
		];
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

	internal ControlRoomScene ActiveScene { get; private set; } = ControlRoomScenes.Default;

	/// <summary>Null before <see cref="InitializeAsync"/> and after <see cref="ShutdownAsync"/>. Actions
	/// treat that as "not ready" rather than dereferencing it.</summary>
	internal IIntegrationContext? Context => _context;

	public Task InitializeAsync(IIntegrationContext context)
	{
		_context = context;
		return Task.CompletedTask;
	}

	public Task ShutdownAsync()
	{
		_context = null;
		return Task.CompletedTask;
	}

	public IReadOnlyList<VirtualProfileDescriptor> GetProfiles() => [ControlRoomProfile.Build(ActiveScene)];

	/// <summary>
	/// A press on one of the profile's own widgets. Fire-and-forget by contract - there is nothing to
	/// reply with - so it does its work and swallows nothing else.
	/// </summary>
	public async Task HandleWidgetInteractionAsync(
		string profileId,
		string folderId,
		string widgetId,
		WidgetInteraction interaction)
	{
		if (ControlRoomProfile.SceneOf(widgetId) is not { } scene)
		{
			return;
		}

		_logger.Information("Widget {WidgetId} requested scene {Scene} ({Trigger}).", widgetId, scene.Id, interaction.TriggerType);
		await ApplySceneAsync(scene, source: "widget", CancellationToken.None);
	}

	/// <summary>
	/// The one path that changes the scene, whether a widget or an action asked for it: it updates the
	/// state, tells the host the profile catalogue is stale so the buttons redraw, pushes the new value
	/// into a host variable and publishes the event.
	/// </summary>
	internal async Task ApplySceneAsync(ControlRoomScene scene, string source, CancellationToken cancellationToken)
	{
		ActiveScene = scene;

		// A virtual profile is a synchronous catalogue, so the host is serving a cached describe until
		// it is told otherwise - without this, the buttons keep the previous scene's colours.
		_catalogNotifier.CatalogChanged(CapabilityKinds.VirtualProfiles, reason: $"scene changed to {scene.Id}");

		if (_context is not { } context)
		{
			return;
		}

		context.Events.Publish(SceneChangedEventId, new Dictionary<string, object?>
		{
			["scene"] = scene.Id,
			["isLive"] = scene.IsLive,
			["source"] = source
		});

		// A pushed variable update, as opposed to the polled ProvidedVariables below: the host owns this
		// variable, and the plugin writes it when something happens rather than waiting to be asked.
		try
		{
			var existing = await context.Variables.GetByNameAsync(SceneVariableName);
			if (existing is null)
			{
				await context.Variables.CreateAsync(SceneVariableName, VariableType.Text, scene.Name);
			}
			else
			{
				await context.Variables.SetValueAsync(existing.Id, scene.Name);
			}
		}
		catch (HostInvocationException exception)
		{
			// Every round-trip callback can fail on the wire - rate limited, timed out, or no live
			// connection - which an in-process integration never has to handle.
			_logger.Warning(exception, "Could not write the scene variable.");
		}

		context.Notifications.Notify(new UserNotificationRequest
		{
			Title = $"Scene: {scene.Name}",
			Level = scene.IsLive ? UserNotificationLevel.Warning : UserNotificationLevel.Info,
			Key = "control-room-scene"
		});
	}

	public IReadOnlyList<VariableDefinition> Variables { get; } =
	[
		VariableDefinition.Eager("sample_control_room_active_scene", VariableType.Text) with { Id = "active-scene" },
		VariableDefinition.Eager("sample_control_room_is_live", VariableType.Boolean) with { Id = "is-live" }
	];

	public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
		=> ValueTask.FromResult(localId switch
		{
			"active-scene" => VariableReading.Of(ActiveScene.Name),
			"is-live" => VariableReading.Of(ActiveScene.IsLive),
			_ => VariableReading.Unavailable
		});

	public IReadOnlyList<EventDefinition> EventDefinitions { get; } =
	[
		new EventDefinition
		{
			Id = SceneChangedEventId,
			Name = Strings.Events.SceneChanged.Name(),
			Description = Strings.Events.SceneChanged.Description(),
			PayloadParameters =
			[
				ActionParameter.Text("scene", Strings.Events.SceneChanged.Scene.Label()),
				ActionParameter.Toggle("isLive", Strings.Events.SceneChanged.IsLive.Label()),
				ActionParameter.Text("source", Strings.Events.SceneChanged.Source.Label())
			]
		}
	];
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Localization/Strings.resx

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <!-- The default-language file. Every translation is checked against it and the fallback chain ends
       here, so it is required even for a plugin that ships one language. Add a language by adding
       Localization/Strings.<culture>.resx beside it (Strings.de.resx, Strings.pt-BR.resx).
       A dotted key becomes a nested class: Actions.Foo.Name is Strings.Actions.Foo.Name(). -->
  <resheader name="resmimetype">
    <value>text/microsoft-resx</value>
  </resheader>
  <resheader name="version">
    <value>2.0</value>
  </resheader>
  <resheader name="reader">
    <value>System.Resources.ResXResourceReader, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>
  </resheader>
  <resheader name="writer">
    <value>System.Resources.ResXResourceWriter, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>
  </resheader>
  <data name="Actions.SetScene.Name" xml:space="preserve">
    <value>Set scene</value>
  </data>
  <data name="Actions.SetScene.Description" xml:space="preserve">
    <value>Switches the sample control room to another scene.</value>
  </data>
  <data name="Actions.SetScene.Scene.Label" xml:space="preserve">
    <value>Scene</value>
  </data>
  <data name="Actions.StyleWidget.Name" xml:space="preserve">
    <value>Style widget</value>
  </data>
  <data name="Actions.StyleWidget.Description" xml:space="preserve">
    <value>Applies a label and colours to a widget, or resets them.</value>
  </data>
  <data name="Actions.StyleWidget.Widget.Label" xml:space="preserve">
    <value>Widget</value>
  </data>
  <data name="Actions.StyleWidget.LabelText.Label" xml:space="preserve">
    <value>Label</value>
  </data>
  <data name="Actions.StyleWidget.Background.Label" xml:space="preserve">
    <value>Background</value>
  </data>
  <data name="Actions.StyleWidget.Icon.Label" xml:space="preserve">
    <value>Icon</value>
  </data>
  <data name="Actions.StyleWidget.State.Label" xml:space="preserve">
    <value>Apply to</value>
  </data>
  <data name="Actions.StyleWidget.NoWidget" xml:space="preserve">
    <value>Pick a widget: this run has no widget of its own to style.</value>
  </data>
  <data name="Actions.StyleWidget.UnknownWidget" xml:space="preserve">
    <value>The host does not know widget {widgetId}.</value>
  </data>
  <data name="WidgetStates.Current" xml:space="preserve">
    <value>Current state</value>
  </data>
  <data name="WidgetStates.All" xml:space="preserve">
    <value>All states</value>
  </data>
  <data name="Actions.Announce.Name" xml:space="preserve">
    <value>Announce</value>
  </data>
  <data name="Actions.Announce.Description" xml:space="preserve">
    <value>Shows a notification in the Macro Deck app.</value>
  </data>
  <data name="Actions.Announce.Title.Label" xml:space="preserve">
    <value>Title</value>
  </data>
  <data name="Actions.Announce.Message.Label" xml:space="preserve">
    <value>Message</value>
  </data>
  <data name="Actions.Announce.Message.Placeholder" xml:space="preserve">
    <value>Optional details</value>
  </data>
  <data name="Actions.Announce.Level.Label" xml:space="preserve">
    <value>Level</value>
  </data>
  <data name="Actions.Announce.Key.Label" xml:space="preserve">
    <value>Replace key</value>
  </data>
  <data name="Actions.Announce.Key.Description" xml:space="preserve">
    <value>Notifications sharing a key replace each other instead of piling up.</value>
  </data>
  <data name="NotificationLevels.Info" xml:space="preserve">
    <value>Info</value>
  </data>
  <data name="NotificationLevels.Warning" xml:space="preserve">
    <value>Warning</value>
  </data>
  <data name="NotificationLevels.Error" xml:space="preserve">
    <value>Error</value>
  </data>
  <data name="Actions.RunScript.Name" xml:space="preserve">
    <value>Run script</value>
  </data>
  <data name="Actions.RunScript.Description" xml:space="preserve">
    <value>Runs a script configured in Macro Deck.</value>
  </data>
  <data name="Actions.RunScript.Script.Label" xml:space="preserve">
    <value>Script</value>
  </data>
  <data name="Actions.NavigateDeck.Name" xml:space="preserve">
    <value>Navigate deck</value>
  </data>
  <data name="Actions.NavigateDeck.Description" xml:space="preserve">
    <value>Opens a folder or profile on the client that triggered the action.</value>
  </data>
  <data name="Actions.NavigateDeck.Kind.Label" xml:space="preserve">
    <value>Target</value>
  </data>
  <data name="Actions.NavigateDeck.TargetId.Label" xml:space="preserve">
    <value>Folder or profile</value>
  </data>
  <data name="Actions.NavigateDeck.MissingTarget" xml:space="preserve">
    <value>Pick the folder or profile to open.</value>
  </data>
  <data name="NavigationKinds.Folder" xml:space="preserve">
    <value>Open folder</value>
  </data>
  <data name="NavigationKinds.Profile" xml:space="preserve">
    <value>Switch profile</value>
  </data>
  <data name="NavigationKinds.Parent" xml:space="preserve">
    <value>Go to parent</value>
  </data>
  <data name="NavigationKinds.Back" xml:space="preserve">
    <value>Go back</value>
  </data>
  <data name="Scenes.Live" xml:space="preserve">
    <value>Live</value>
  </data>
  <data name="Scenes.Standby" xml:space="preserve">
    <value>Standby</value>
  </data>
  <data name="Scenes.Break" xml:space="preserve">
    <value>Break</value>
  </data>
  <data name="Scenes.Offline" xml:space="preserve">
    <value>Offline</value>
  </data>
  <data name="Events.SceneChanged.Name" xml:space="preserve">
    <value>Scene changed</value>
  </data>
  <data name="Events.SceneChanged.Description" xml:space="preserve">
    <value>Raised when the control room switches to another scene.</value>
  </data>
  <data name="Events.SceneChanged.Scene.Label" xml:space="preserve">
    <value>Scene</value>
  </data>
  <data name="Events.SceneChanged.IsLive.Label" xml:space="preserve">
    <value>On air</value>
  </data>
  <data name="Events.SceneChanged.Source.Label" xml:space="preserve">
    <value>Triggered by</value>
  </data>
  <data name="Errors.NotInitialized" xml:space="preserve">
    <value>The integration is not initialized.</value>
  </data>
</root>
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/MacroDeck.SampleVirtualProfilePlugin.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <IsPackable>false</IsPackable>
        <UserSecretsId>MacroDeck.SampleVirtualProfilePlugin-PluginDevelopment</UserSecretsId>
    </PropertyGroup>

    <!-- Microsoft.NET.Sdk plus this framework reference, not Microsoft.NET.Sdk.Web: a plugin is a
         headless process, and the framework reference is what supplies the hosting surface
         MacroDeck.Plugin.Hosting builds on. -->
    <ItemGroup>
        <FrameworkReference Include="Microsoft.AspNetCore.App" />
    </ItemGroup>

    <ItemGroup>
        <!-- Build-time only: compile-time diagnostics for plugin authors, the [MacroDeckSdkUsage]
             attribute the host reads to report real deprecation usage, and the source generator that
             turns Localization/*.resx into the typed Strings class. Never shipped in the output. -->
        <PackageReference Include="MacroDeck.Plugin.Analyzers" PrivateAssets="all" />
        <!-- Referenced directly rather than relied on transitively through the SDK: LocalizedText and
             the generated Strings class are part of this project's own source. -->
        <PackageReference Include="MacroDeck.Localization" />
        <PackageReference Include="MacroDeck.Plugin.Hosting" />
        <PackageReference Include="MacroDeck.Plugin.Serilog" />
        <PackageReference Include="MacroDeck.Sdk" />
    </ItemGroup>

    <!-- The SDK reads the manifest from the content root at startup and resolves the icon path against
         that same root, so both have to land next to the built executable. -->
    <ItemGroup>
        <Content Include="manifest.json" CopyToOutputDirectory="PreserveNewest" />
        <Content Include="Assets\icon.svg" CopyToOutputDirectory="PreserveNewest" />
    </ItemGroup>

</Project>
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Profiles/ControlRoomProfile.cs

```csharp
using System.Text.Json;
using MacroDeck.SampleVirtualProfilePlugin.Scenes;
using MacroDeck.Sdk.Profiles;

namespace MacroDeck.SampleVirtualProfilePlugin.Profiles;

/// <summary>
/// Builds the profile the plugin owns. A virtual profile is described, never stored: the host has no
/// copy to edit, so the descriptors are rebuilt from the current scene every time they are asked for -
/// which is what makes the active scene's button visibly light up.
/// </summary>
internal static class ControlRoomProfile
{
	internal const string ProfileId = "control-room";
	internal const string ScenesFolderId = "scenes";
	internal const string StatusFolderId = "status";

	private const string WidgetIdPrefix = "scene-";
	private const string InactiveColor = "#20242B";

	internal static VirtualProfileDescriptor Build(ControlRoomScene activeScene) => new(
		ProfileId,
		"Sample Control Room",
		// Locked, because the layout is the plugin's to decide - a user cannot add a row to a folder
		// whose contents this plugin regenerates.
		ProfileLayout.Grid(rows: 2, columns: 4),
		[
			new VirtualFolderDescriptor(ScenesFolderId, "Scenes",
				[.. ControlRoomScenes.All.Select((scene, index) => SceneWidget(scene, index, activeScene))]),
			new VirtualFolderDescriptor(StatusFolderId, "Status",
				[
					new VirtualWidgetDescriptor("status-clock", "Clock", PositionX: 0, PositionY: 0, Width: 2, Height: 1)
				],
				ParentId: ScenesFolderId,
				Order: 1)
		]);

	/// <summary>The scene a widget id stands for, or null for a widget that is not a scene button.</summary>
	internal static ControlRoomScene? SceneOf(string widgetId)
		=> widgetId.StartsWith(WidgetIdPrefix, StringComparison.Ordinal)
			? ControlRoomScenes.Find(widgetId[WidgetIdPrefix.Length..])
			: null;

	private static VirtualWidgetDescriptor SceneWidget(ControlRoomScene scene, int index, ControlRoomScene activeScene)
	{
		var isActive = string.Equals(scene.Id, activeScene.Id, StringComparison.Ordinal);

		// The same JSON payload a stored widget of this type would carry.
		var data = JsonSerializer.Serialize(new
		{
			mode = "single",
			label = scene.Name,
			offState = new
			{
				label = scene.Name,
				backgroundColor = isActive ? scene.Color : InactiveColor,
				labelColor = "#FFFFFF"
			}
		});

		return new VirtualWidgetDescriptor(WidgetIdPrefix + scene.Id, "ActionButton", PositionX: index, PositionY: 0, Data: data);
	}
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Program.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Serilog;
using MacroDeck.SampleVirtualProfilePlugin;

// Identity, description and icon are not set here: they come from manifest.json at the content root.
// Strings is generated from Localization/*.resx, so UseLocalization is what makes every LocalizedText
// this plugin hands the host resolve in the reader's language rather than falling back to its key.
var plugin = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<ControlRoomIntegration>()
	.Build();

await plugin.RunAsync();
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/Properties/launchSettings.json

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

## File: src/MacroDeck.SampleVirtualProfilePlugin/README.md

````markdown
# Sample Control Room plugin

Two things that have no other worked example: a virtual profile the plugin owns, and the callbacks
that go from the plugin to the host. Read it when your plugin wants to *present* a deck of its own, or
to drive the app rather than only answer it.

The plugin models a small control room with four scenes. Pressing one of its own profile buttons and
running its "set scene" action end in the same method, so the two directions stay visibly consistent.

## Read these first

- **`Profiles/ControlRoomProfile.cs`** - the profile is described, never stored: the host has no copy to
  edit, so the descriptors are rebuilt from the current scene every time they are asked for. That is
  what makes the active scene's button change colour.
- **`ControlRoomIntegration.cs`** - `IProfileProvider.HandleWidgetInteractionAsync` for the presses, and
  `ApplySceneAsync` for everything that follows: invalidating the profile catalogue so the buttons
  redraw, publishing the event, writing a host variable and notifying the user.
- **`Actions/StyleWidgetAction.cs`** - `IWidgetApi`: the widget target defaults to `$self`, so the action
  styles the button it was triggered from, and an empty colour clears the override instead of setting
  one. Which appearance to change is addressed through `StateIds` by the widget's own stable state ids,
  read off `WidgetTargetInfo.States` at edit time, plus the `$current` and `$all` sentinels - not the
  deprecated fixed `WidgetStateSelector`.
- **`Actions/NavigateDeckAction.cs`** - `IDeckNavigator`, with the target field only shown for the kinds
  that need one. Its options come from a host-pushed cache, which is empty for a moment right after
  connecting - expected, not an error.
- **`Actions/RunScriptAction.cs`** - `IScriptApi`: the script's own result becomes the action's result,
  so a failing script does not look like a successful button press.
- **`Actions/AnnounceAction.cs`** - `IUserNotifier`, including what a key is for: notifications sharing
  one replace each other, which is also how a plugin expresses progress.

## Callbacks can fail

Every round-trip callback here is wrapped: over the wire a `host.invoke` can be rate limited, time out,
or find no live connection, and throws `HostInvocationException` into the calling integration. An
in-process integration never has to handle that - it is the one genuinely new failure mode a plugin
gets, and ignoring it is the most common way a plugin breaks in the field.
- **`Localization/Strings.resx`** - every string a user reads. `ControlRoomScenes.DisplayName` shows
  where the line falls: an action's option label is a reference, while the same scene's name inside a
  virtual widget's JSON payload, a host variable's value or a notification title stays a literal,
  because those contracts take a plain string.

## Running it against a local host

Use this project's **Macro Deck - Real Host** launch profile as described in the repository's
[run and debug guide](../../README.md#run-and-debug-against-macro-deck), then switch to the "Sample
Control Room" profile. Its buttons are the plugin's, not the user's: pressing one changes the scene,
recolours the grid and updates the `sample_control_room_scene` variable.

## Testing it

```bash
dotnet test tests/MacroDeck.SampleVirtualProfilePlugin.Tests
```

The harness tests seed the fake deck, widgets and scripts and then assert on what the plugin asked the
host to do; the wire test proves a widget interaction - the one operation with no reply - actually
arrived, by reading the profile back afterwards.

## Packaging it

`macrodeck-build.json` names one self-contained `dotnet publish` per platform, and the manifest's
entrypoints name what that publish actually produces:

```bash
macrodeck-plugin build --output ./artifacts
```

```bash
macrodeck-plugin validate --artifact ./artifacts/app.macro-deck.sample-virtual-profile-1.0.0.macroDeckPlugin --level Publication
```
````

## File: src/MacroDeck.SampleVirtualProfilePlugin/Scenes/ControlRoomScenes.cs

```csharp
using MacroDeck.Localization;

namespace MacroDeck.SampleVirtualProfilePlugin.Scenes;

/// <summary>The scenes the sample control room can be in. Everything else - the virtual profile, the
/// variables, the event - is derived from whichever one is active.</summary>
internal static class ControlRoomScenes
{
	internal static IReadOnlyList<ControlRoomScene> All { get; } =
	[
		new("live", "Live", "#D0021B", IsLive: true),
		new("standby", "Standby", "#F5A623", IsLive: false),
		new("break", "Break", "#4A90D9", IsLive: false),
		new("offline", "Offline", "#4A4A4A", IsLive: false)
	];

	internal static ControlRoomScene Default => All[3];

	internal static ControlRoomScene? Find(string id)
		=> All.FirstOrDefault(scene => string.Equals(scene.Id, id, StringComparison.Ordinal));

	/// <summary>
	/// The scene's name for a surface that resolves a reference in the reader's language - an action's
	/// option label, an event's payload. <see cref="ControlRoomScene.Name"/> stays beside it for the
	/// surfaces that cannot take one: a virtual widget's JSON payload, a host variable's value and a
	/// notification title are all plain strings on their contracts.
	/// </summary>
	internal static LocalizedText DisplayName(ControlRoomScene scene) => scene.Id switch
	{
		"live" => Strings.Scenes.Live(),
		"standby" => Strings.Scenes.Standby(),
		"break" => Strings.Scenes.Break(),
		"offline" => Strings.Scenes.Offline(),
		_ => scene.Name
	};
}

internal sealed record ControlRoomScene(string Id, string Name, string Color, bool IsLive);
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/macrodeck-build.json

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleVirtualProfilePlugin.csproj",
        "-c",
        "Release",
        "-r",
        "win-x64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/win-x64"
      ],
      "output": "bin/publish/win-x64"
    },
    "osx-arm64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleVirtualProfilePlugin.csproj",
        "-c",
        "Release",
        "-r",
        "osx-arm64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/osx-arm64"
      ],
      "output": "bin/publish/osx-arm64"
    },
    "osx-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleVirtualProfilePlugin.csproj",
        "-c",
        "Release",
        "-r",
        "osx-x64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/osx-x64"
      ],
      "output": "bin/publish/osx-x64"
    },
    "linux-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleVirtualProfilePlugin.csproj",
        "-c",
        "Release",
        "-r",
        "linux-x64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/linux-x64"
      ],
      "output": "bin/publish/linux-x64"
    }
  }
}
```

## File: src/MacroDeck.SampleVirtualProfilePlugin/manifest.json

```json
{
  "$schema": "https://schemas.macro-deck.app/plugin-manifest-v1.schema.json",
  "manifestVersion": 1,
  "id": "app.macro-deck.sample-virtual-profile",
  "name": "Sample Control Room",
  "version": "1.0.0",
  "description": "A plugin-owned virtual profile with widget interactions, plus the host callback APIs: deck navigation, widget appearance, scripts, variables and notifications.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": {
      "executable": "runtimes/win-x64/MacroDeck.SampleVirtualProfilePlugin.exe"
    },
    "osx-arm64": {
      "executable": "runtimes/osx-arm64/MacroDeck.SampleVirtualProfilePlugin"
    },
    "osx-x64": {
      "executable": "runtimes/osx-x64/MacroDeck.SampleVirtualProfilePlugin"
    },
    "linux-x64": {
      "executable": "runtimes/linux-x64/MacroDeck.SampleVirtualProfilePlugin"
    }
  },
  "publisher": {
    "name": "Macro Deck",
    "id": "app.macro-deck",
    "url": "https://macro-deck.app"
  },
  "license": "MIT",
  "homepage": "https://docs.macro-deck.app/introduction/samples-and-template/",
  "repository": "https://github.com/Macro-Deck-App/Macro-Deck-Sample-Plugins",
  "compatibility": {
    "macroDeck": ">=3.0.0-0"
  },
  "permissions": [
    "host:deck",
    "host:widgets",
    "host:scripts",
    "host:variables",
    "host:notifications",
    "host:action-interactions",
    "events:publish"
  ]
}
```

## File: tests/MacroDeck.SampleVirtualProfilePlugin.Tests/ControlRoomIntegrationTests.cs

```csharp
using MacroDeck.Plugin.Protocol.Capabilities.Actions;
using MacroDeck.Plugin.Protocol.Capabilities.Variables;
using MacroDeck.Plugin.Protocol.Capabilities.VirtualProfiles;
using MacroDeck.Plugin.Testing;
using MacroDeck.Plugin.Testing.Fakes;
using MacroDeck.Sdk.Decks;
using MacroDeck.Sdk.Scripts;
using MacroDeck.Sdk.Widgets;
using NUnit.Framework;

namespace MacroDeck.SampleVirtualProfilePlugin.Tests;

[TestFixture]
public sealed class ControlRoomIntegrationTests
{
	private static readonly string[] _sceneWidgetIds = ["scene-live", "scene-standby", "scene-break", "scene-offline"];
	private static readonly string[] _breakOnly = ["scene-break"];
	private static readonly string[] _scriptNames = ["Start stream", "Broken"];
	private static readonly string[] _onState = ["on"];
	private static readonly string[] _currentState = [WidgetStates.Current];

	[Test]
	public async Task The_profile_offers_one_button_per_scene()
	{
		await using var harness = await CreateAsync();

		var profiles = (await harness.VirtualProfiles.GetProfilesAsync()).DataAs<VirtualProfilesResult>();
		var scenes = profiles!.Profiles.Single().Folders.Single(folder => folder.Id == "scenes");

		Assert.That(scenes.Widgets.Select(widget => widget.Id), Is.EquivalentTo(_sceneWidgetIds));
		Assert.That(scenes.Widgets.Select(widget => widget.Type), Is.All.EqualTo("ActionButton"));
	}

	[Test]
	public async Task The_layout_is_locked_because_the_plugin_owns_it()
	{
		await using var harness = await CreateAsync();

		var layout = (await harness.VirtualProfiles.GetProfilesAsync())
			.DataAs<VirtualProfilesResult>()!.Profiles.Single().Layout;

		Assert.That(layout.RowsLocked, Is.True);
		Assert.That(layout.ColumnsLocked, Is.True);
	}

	[Test]
	public async Task Pressing_a_scene_button_switches_the_scene_everywhere()
	{
		await using var harness = await CreateAsync();

		await harness.VirtualProfiles.SendWidgetInteractionAsync(Press("scene-live"));

		var active = (await harness.Variables.GetAsync("active-scene")).DataAs<VariableReadingDto>();
		var isLive = (await harness.Variables.GetAsync("is-live")).DataAs<VariableReadingDto>();
		var published = harness.Context.Events.Published[^1];

		Assert.That(active!.Value.Text, Is.EqualTo("Live"));
		Assert.That(isLive!.Value.Boolean, Is.True);
		Assert.That(published.EventId, Is.EqualTo("scene-changed"));
		Assert.That(published.Parameters!.Value.GetProperty("source").GetString(), Is.EqualTo("widget"));
	}

	[Test]
	public async Task The_pressed_scene_is_the_one_the_profile_marks_as_active()
	{
		await using var harness = await CreateAsync();

		await harness.VirtualProfiles.SendWidgetInteractionAsync(Press("scene-break"));

		var scenes = (await harness.VirtualProfiles.GetProfilesAsync())
			.DataAs<VirtualProfilesResult>()!.Profiles.Single().Folders.Single(folder => folder.Id == "scenes");

		// The active scene is the one drawn in its own colour; the rest share the inactive one.
		var highlighted = scenes.Widgets
			.Where(widget => !widget.Data!.Contains("#20242B", StringComparison.Ordinal))
			.Select(widget => widget.Id)
			.ToArray();

		Assert.That(highlighted, Is.EqualTo(_breakOnly));
	}

	[Test]
	public async Task The_scene_is_written_into_a_host_variable_the_plugin_owns()
	{
		await using var harness = await CreateAsync();

		await harness.VirtualProfiles.SendWidgetInteractionAsync(Press("scene-standby"));

		var created = harness.Context.Variables.Created.Single();
		var current = await harness.Context.Variables.GetByNameAsync("sample_control_room_scene");

		Assert.That(created.Name, Is.EqualTo("sample_control_room_scene"));
		Assert.That(current!.Value, Is.EqualTo("Standby"));
	}

	[Test]
	public async Task Switching_twice_updates_the_variable_instead_of_creating_a_second_one()
	{
		await using var harness = await CreateAsync();

		await harness.VirtualProfiles.SendWidgetInteractionAsync(Press("scene-standby"));
		await harness.VirtualProfiles.SendWidgetInteractionAsync(Press("scene-live"));

		Assert.That(harness.Context.Variables.Created, Has.Count.EqualTo(1));
		Assert.That((await harness.Context.Variables.GetByNameAsync("sample_control_room_scene"))!.Value, Is.EqualTo("Live"));
	}

	[Test]
	public async Task A_press_on_a_widget_that_is_not_a_scene_button_changes_nothing()
	{
		await using var harness = await CreateAsync();
		await harness.VirtualProfiles.SendWidgetInteractionAsync(Press("scene-live"));
		var eventsBefore = harness.Context.Events.Published.Count;

		var outcome = await harness.VirtualProfiles.SendWidgetInteractionAsync(
			Press("status-clock", folderId: "status"));

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(harness.Context.Events.Published, Has.Count.EqualTo(eventsBefore));
		Assert.That((await harness.Variables.GetAsync("active-scene")).DataAs<VariableReadingDto>()!.Value.Text, Is.EqualTo("Live"));
	}

	[Test]
	public async Task The_action_and_the_button_reach_the_same_scene()
	{
		await using var harness = await CreateAsync();

		await harness.Actions.ExecuteAsync("set-scene", new Dictionary<string, object?> { ["scene"] = "break" });

		var active = (await harness.Variables.GetAsync("active-scene")).DataAs<VariableReadingDto>();
		Assert.That(active!.Value.Text, Is.EqualTo("Break"));
		Assert.That(harness.Context.Events.Published[^1].Parameters!.Value.GetProperty("source").GetString(),
			Is.EqualTo("action"));
	}

	[Test]
	public async Task An_unknown_scene_fails_rather_than_switching_to_a_default()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("set-scene", new Dictionary<string, object?> { ["scene"] = "party" });

		Assert.That(outcome.Succeeded, Is.False);
		Assert.That((await harness.Variables.GetAsync("active-scene")).DataAs<VariableReadingDto>()!.Value.Text, Is.EqualTo("Offline"));
	}

	[Test]
	public async Task Styling_falls_back_to_the_widget_that_triggered_the_run()
	{
		await using var harness = await CreateAsync();
		harness.Context.Widgets.Seed(new WidgetTargetInfo
		{
			Id = "widget-1",
			Label = "On air",
			Location = "Main",
			Type = "ActionButton"
		});

		var outcome = await harness.Actions.ExecuteAsync("style-widget",
			new Dictionary<string, object?> { ["label"] = "ON AIR", ["backgroundColor"] = "#D0021B" },
			ownerWidgetId: "widget-1");

		var applied = harness.Context.Widgets.LastApplied["widget-1"];

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(applied.Patch.Label, Is.EqualTo("ON AIR"));
		Assert.That(applied.Patch.BackgroundColor, Is.EqualTo("#D0021B"));
	}

	[Test]
	public async Task Styling_a_widget_the_host_does_not_know_fails()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("style-widget",
			new Dictionary<string, object?> { ["widget"] = "widget-404", ["label"] = "Nope" });

		Assert.That(outcome.Succeeded, Is.False);
	}

	[Test]
	public async Task Styling_without_a_widget_to_fall_back_on_fails_rather_than_guessing()
	{
		await using var harness = await CreateAsync();

		// No owner widget: the same shape a script or an automation runs an action with.
		var outcome = await harness.Actions.ExecuteAsync("style-widget",
			new Dictionary<string, object?> { ["label"] = "Nope" });

		Assert.That(outcome.Succeeded, Is.False);
		Assert.That(harness.Context.Widgets.LastApplied, Is.Empty);
	}

	[Test]
	public async Task Styling_targets_a_state_by_its_own_id()
	{
		await using var harness = await CreateAsync();
		harness.Context.Widgets.Seed(new WidgetTargetInfo
		{
			Id = "widget-1",
			Label = "On air",
			Location = "Main",
			Type = "ActionButton",
			States = [new WidgetStateInfo("on", "On"), new WidgetStateInfo("off", "Off")],
			CurrentStateId = "off"
		});

		// The picker offers the two sentinels every widget accepts plus this widget's own states.
		var options = (await harness.Actions.GetOptionsAsync("style-widget",
			"state",
			currentParameters: new Dictionary<string, object?> { ["widget"] = "widget-1" }))
			.DataAs<DynamicOptionsResultDto>();

		Assert.That(options!.Options.Select(option => option.Value),
			Is.EqualTo(new[] { WidgetStates.Current, WidgetStates.All, "on", "off" }));

		var outcome = await harness.Actions.ExecuteAsync("style-widget", new Dictionary<string, object?>
		{
			["widget"] = "widget-1",
			["state"] = "on",
			["label"] = "LIVE"
		});

		var applied = harness.Context.Widgets.LastApplied["widget-1"];

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(applied.ResolveStateIds(), Is.EqualTo(_onState));
	}

	[Test]
	public async Task Styling_without_a_state_means_whichever_one_the_widget_shows()
	{
		await using var harness = await CreateAsync();
		harness.Context.Widgets.Seed(new WidgetTargetInfo
		{
			Id = "widget-1",
			Label = "On air",
			Location = "Main",
			Type = "ActionButton"
		});

		await harness.Actions.ExecuteAsync("style-widget",
			new Dictionary<string, object?> { ["widget"] = "widget-1", ["label"] = "Studio" });

		Assert.That(harness.Context.Widgets.LastApplied["widget-1"].ResolveStateIds(), Is.EqualTo(_currentState));
	}

	[Test]
	public async Task The_reset_colour_clears_the_override_instead_of_setting_one()
	{
		await using var harness = await CreateAsync();
		harness.Context.Widgets.Seed(new WidgetTargetInfo
		{
			Id = "widget-1",
			Label = "On air",
			Location = "Main",
			Type = "ActionButton"
		});

		await harness.Actions.ExecuteAsync("style-widget", new Dictionary<string, object?>
		{
			["widget"] = "widget-1",
			["label"] = "Studio",
			["backgroundColor"] = WidgetAppearanceValues.Reset
		});

		var applied = harness.Context.Widgets.LastApplied["widget-1"];

		Assert.That(applied.ClearProperties, Does.Contain(WidgetAppearanceProperty.BackgroundColor));
		Assert.That(applied.Patch.BackgroundColor, Is.Null);
	}

	[Test]
	public async Task Announcing_replaces_the_previous_notification_under_the_same_key()
	{
		await using var harness = await CreateAsync();

		await harness.Actions.ExecuteAsync("announce",
			new Dictionary<string, object?> { ["title"] = "First", ["key"] = "studio" });
		await harness.Actions.ExecuteAsync("announce",
			new Dictionary<string, object?> { ["title"] = "Second", ["key"] = "studio", ["level"] = "Warning" });

		var current = harness.Context.Notifications.Current.Single(notification => notification.Key == "studio");

		Assert.That(current.Title, Is.EqualTo("Second"));
		Assert.That(current.Level, Is.EqualTo(Sdk.Notifications.UserNotificationLevel.Warning));
	}

	[Test]
	public async Task Announcing_without_a_title_fails()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("announce", new Dictionary<string, object?> { ["message"] = "Body only" });

		Assert.That(outcome.Succeeded, Is.False);
	}

	[Test]
	public async Task Running_a_script_reports_what_the_script_reported()
	{
		await using var harness = await CreateAsync();
		harness.Context.Scripts.Seed(new Script { Id = "script-1", Name = "Start stream" });
		harness.Context.Scripts.Seed(new Script { Id = "script-2", Name = "Broken" },
			() => Sdk.Actions.ActionResult.Failed("PROVIDER_ERROR", "The script threw."));

		var options = (await harness.Actions.GetOptionsAsync("run-script", "scriptId")).DataAs<DynamicOptionsResultDto>();
		var succeeded = await harness.Actions.ExecuteAsync("run-script", new Dictionary<string, object?> { ["scriptId"] = "script-1" });
		var failed = await harness.Actions.ExecuteAsync("run-script", new Dictionary<string, object?> { ["scriptId"] = "script-2" });

		// A script's name is the one the user gave it, so it stays a literal all the way onto the wire.
		Assert.That(options!.Options.Select(option => option.Label?.Literal), Is.EquivalentTo(_scriptNames));
		Assert.That(succeeded.Succeeded, Is.True);
		Assert.That(harness.Context.Scripts.Ran, Does.Contain("script-1"));
		Assert.That(failed.Succeeded, Is.False);
	}

	[Test]
	public async Task Navigating_targets_the_client_that_pressed_the_button()
	{
		await using var harness = await CreateAsync();
		harness.Context.Deck.SeedFolders(new DeckFolder { Id = "folder-1", Label = "Studio" });

		var options = (await harness.Actions.GetOptionsAsync("navigate-deck",
			"targetId",
			currentParameters: new Dictionary<string, object?> { ["kind"] = "folder" })).DataAs<DynamicOptionsResultDto>();

		var outcome = await harness.Actions.ExecuteAsync("navigate-deck",
			new Dictionary<string, object?> { ["kind"] = "folder", ["targetId"] = "folder-1" },
			originClientId: "client-3");

		var call = harness.Context.Deck.Calls.Single();

		// A folder label is the user's own text, so it travels as a literal rather than as a reference
		// a client would resolve - which is exactly what Literal reads back.
		Assert.That(options!.Options.Single().Label?.Literal, Is.EqualTo("Studio"));
		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(call.Id, Is.EqualTo("folder-1"));
		Assert.That(call.OriginClientId, Is.EqualTo("client-3"));
	}

	[Test]
	public async Task Navigating_back_needs_no_target()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("navigate-deck", new Dictionary<string, object?> { ["kind"] = "back" });

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(harness.Context.Deck.Calls.Single().Kind, Is.EqualTo(DeckNavigationKind.GoBack));
	}

	[Test]
	public async Task Opening_a_folder_without_naming_one_fails_before_the_host_is_called()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("navigate-deck", new Dictionary<string, object?> { ["kind"] = "folder" });

		Assert.That(outcome.Succeeded, Is.False);
		Assert.That(harness.Context.Deck.Calls, Is.Empty);
	}

	private static WidgetInteractionArguments Press(string widgetId, string folderId = "scenes") => new()
	{
		ProfileId = "control-room",
		FolderId = folderId,
		WidgetId = widgetId,
		TriggerType = "onShortPress"
	};

	private static async Task<PluginTestHarness> CreateAsync()
	{
		var harness = PluginTestHarness.Create(builder => builder
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<ControlRoomIntegration>());
		await harness.InitializeIntegrationsAsync();
		return harness;
	}
}
```

## File: tests/MacroDeck.SampleVirtualProfilePlugin.Tests/ControlRoomOverTheWireTests.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Protocol.Capabilities.VirtualProfiles;
using MacroDeck.Plugin.Serilog;
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.SampleVirtualProfilePlugin.Tests;

/// <summary>
/// Virtual profiles over a real socket, including the one operation with no reply: a widget
/// interaction is fire-and-forget, so what proves it arrived is the profile that comes back next.
/// </summary>
[TestFixture]
public sealed class ControlRoomOverTheWireTests
{
	[Test]
	public async Task A_widget_interaction_arrives_and_the_next_profile_read_shows_it()
	{
		var builder = MacroDeckPlugin.CreatePlugin()
			.UseMacroDeckLogging()
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<ControlRoomIntegration>();

		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.HostAsync(builder);
		var session = await host.WaitForSessionAsync();

		var outcome = await session.VirtualProfiles.SendWidgetInteractionAsync(new WidgetInteractionArguments
		{
			ProfileId = "control-room",
			FolderId = "scenes",
			WidgetId = "scene-live",
			TriggerType = "onShortPress"
		});
		Assert.That(outcome.Succeeded, Is.True);

		await host.Events.WaitForAsync("scene-changed", TimeSpan.FromSeconds(5));

		var profiles = (await session.VirtualProfiles.GetProfilesAsync()).DataAs<VirtualProfilesResult>();
		var live = profiles!.Profiles.Single()
			.Folders.Single(folder => folder.Id == "scenes")
			.Widgets.Single(widget => widget.Id == "scene-live");

		Assert.That(live.Data, Does.Contain("#D0021B"));
	}
}
```

## File: tests/MacroDeck.SampleVirtualProfilePlugin.Tests/LocalizationTests.cs

```csharp
using NUnit.Framework;

namespace MacroDeck.SampleVirtualProfilePlugin.Tests;

/// <summary>
/// The localization set is generated from <c>Localization/*.resx</c>, so these guard the wiring rather
/// than any wording: a missing catalog registration leaves every label showing its raw key, and a key
/// present in a translation but not in the default-language file can never resolve at all.
/// </summary>
[TestFixture]
public sealed class LocalizationTests
{
	[Test]
	public void The_catalog_is_scoped_to_the_plugin_id()
	{
		Assert.That(Strings.LocalizationCatalog.Scope, Is.EqualTo("plugin:app.macro-deck.sample-virtual-profile"));
	}

	[Test]
	public void English_is_the_default_culture()
	{
		Assert.That(Strings.LocalizationCatalog.DefaultCulture, Is.EqualTo("en"));
		Assert.That(Strings.LocalizationCatalog.Cultures, Does.Contain("en"));
	}

	[Test]
	public void The_action_strings_come_from_the_catalog()
	{
		Assert.That(Strings.LocalizationCatalog.KeysOf("en"), Does.Contain("Actions.SetScene.Name"));
	}

	[Test]
	public void Every_key_the_default_culture_declares_resolves_to_text()
	{
		foreach (var key in Strings.LocalizationCatalog.KeysOf("en"))
		{
			Assert.That(Strings.LocalizationCatalog.TryGetTemplate("en", key, out var text), Is.True);
			Assert.That(text, Is.Not.Empty);
		}
	}

	/// <summary>
	/// Every culture the plugin ships carries every key the default language declares. MDLOC001 catches
	/// the other direction at build time - a key only a translation has - but a translation that is
	/// simply behind is not a build error, and this is what makes it a visible one.
	/// </summary>
	[Test]
	public void Every_culture_carries_every_key_the_default_language_declares()
	{
		var catalog = Strings.LocalizationCatalog;
		var expected = catalog.KeysOf(catalog.DefaultCulture);

		foreach (var culture in catalog.Cultures)
		{
			Assert.That(catalog.KeysOf(culture), Is.EquivalentTo(expected), $"culture '{culture}'");
		}
	}
}
```

## File: tests/MacroDeck.SampleVirtualProfilePlugin.Tests/MacroDeck.SampleVirtualProfilePlugin.Tests.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <IsPackable>false</IsPackable>
        <IsTestProject>true</IsTestProject>
        <!-- Underscored test names, like the Macro Deck repository's own test projects. -->
        <NoWarn>$(NoWarn);CA1707</NoWarn>
    </PropertyGroup>

    <ItemGroup>
        <PackageReference Include="MacroDeck.Plugin.Testing" />
        <PackageReference Include="Microsoft.NET.Test.Sdk" />
        <PackageReference Include="NUnit" />
        <PackageReference Include="NUnit.Analyzers" PrivateAssets="all" />
        <PackageReference Include="NUnit3TestAdapter" />
    </ItemGroup>

    <ItemGroup>
        <ProjectReference Include="..\..\src\MacroDeck.SampleVirtualProfilePlugin\MacroDeck.SampleVirtualProfilePlugin.csproj" />
    </ItemGroup>

</Project>
```
