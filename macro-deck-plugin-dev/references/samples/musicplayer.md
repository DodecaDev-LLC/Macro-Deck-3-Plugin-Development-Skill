# Sample: MacroDeck.SampleMusicPlayerPlugin

The `MacroDeck.SampleMusicPlayerPlugin` sample plugin and its tests, one `## File: <path>` section per file. See `samples/README.md` for what each sample demonstrates.

Files:

- `src/MacroDeck.SampleMusicPlayerPlugin/Actions/PlayCatalogItemAction.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Actions/SetVolumeAction.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Actions/TogglePlaybackAction.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Actions/TransferPlaybackAction.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Assets/icon.svg`
- `src/MacroDeck.SampleMusicPlayerPlugin/Localization/Strings.resx`
- `src/MacroDeck.SampleMusicPlayerPlugin/MacroDeck.SampleMusicPlayerPlugin.csproj`
- `src/MacroDeck.SampleMusicPlayerPlugin/MusicPlayerIntegration.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Player/LibraryMusicPlayer.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Player/MusicLibrary.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Player/PlaybackEngine.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Player/PlayerState.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Player/SpeakerMusicPlayer.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Program.cs`
- `src/MacroDeck.SampleMusicPlayerPlugin/Properties/launchSettings.json`
- `src/MacroDeck.SampleMusicPlayerPlugin/README.md`
- `src/MacroDeck.SampleMusicPlayerPlugin/macrodeck-build.json`
- `src/MacroDeck.SampleMusicPlayerPlugin/manifest.json`
- `tests/MacroDeck.SampleMusicPlayerPlugin.Tests/LocalizationTests.cs`
- `tests/MacroDeck.SampleMusicPlayerPlugin.Tests/MacroDeck.SampleMusicPlayerPlugin.Tests.csproj`
- `tests/MacroDeck.SampleMusicPlayerPlugin.Tests/MusicPlayerIntegrationTests.cs`
- `tests/MacroDeck.SampleMusicPlayerPlugin.Tests/MusicPlayerOverTheWireTests.cs`

## File: src/MacroDeck.SampleMusicPlayerPlugin/Actions/PlayCatalogItemAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.SampleMusicPlayerPlugin.Player;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.MusicPlayer;

namespace MacroDeck.SampleMusicPlayerPlugin.Actions;

/// <summary>
/// Dynamic options that depend on another parameter: the item list is filtered by the chosen kind,
/// which the host passes back in <see cref="DynamicOptionsContext.CurrentParameters"/>. Leaving the
/// item empty pops the host's own item picker instead of failing.
/// </summary>
internal sealed class PlayCatalogItemAction(MusicPlayerIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "play-catalog-item";

	public LocalizedText Name => Strings.Actions.PlayCatalogItem.Name();

	public LocalizedText Description => Strings.Actions.PlayCatalogItem.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		// An option's Value is the wire identity the executor parses back, so it stays the enum name;
		// only its Label is localized.
		ActionParameter.Choice("kind",
			[
				new ActionParameterOption
				{
					Value = nameof(MusicPlayerCatalogItemKind.Track),
					Label = Strings.CatalogKinds.Track()
				},
				new ActionParameterOption
				{
					Value = nameof(MusicPlayerCatalogItemKind.Playlist),
					Label = Strings.CatalogKinds.Playlist()
				}
			],
			label: Strings.Fields.Kind.Label(),
			defaultValue: nameof(MusicPlayerCatalogItemKind.Track),
			required: true),
		ActionParameter.DynamicChoice("item",
			label: Strings.Fields.Item.Label(),
			description: Strings.Actions.PlayCatalogItem.Item.Description()),
		ActionParameter.Toggle("shuffle", label: Strings.Actions.PlayCatalogItem.Shuffle.Label())
			// Shuffling a single track means nothing, so the toggle only shows for a playlist.
			.OnlyWhen("kind", nameof(MusicPlayerCatalogItemKind.Playlist))
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		var kind = ParseKind(context.CurrentParameters.GetValueOrDefault("kind"));
		var items = MusicLibrary.CatalogItems(kind, context.Filter);

		// A track title is content, not UI text: it is already in its final form and stays a literal.
		return Task.FromResult(new DynamicOptionsResult
		{
			Options = [.. items.Select(item => new ActionParameterOption { Value = item.Id, Label = item.Title })],
			CacheSeconds = 30
		});
	}

	private static MusicPlayerCatalogItemKind ParseKind(object? value)
		=> value is string text && Enum.TryParse<MusicPlayerCatalogItemKind>(text, out var kind)
			? kind
			: MusicPlayerCatalogItemKind.Track;

	private sealed class Executor(MusicPlayerIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			var kind = ParseKind(context.Parameters.GetValueOrDefault("kind"));

			if (context.Parameters.GetValueOrDefault("item") is not string { Length: > 0 } itemId)
			{
				// A picker request is only accepted while this execution is still running, and it is
				// fire-and-forget: the user's choice arrives as a later execution, not as a return value.
				// The prompt is a plain string because IActionInteractions types it as one.
				context.Interactions?.RequestItemPicker(context.OriginClientId,
					MusicPlayerIntegration.LibraryInstanceId,
					kind,
					prompt: "Pick something to play");

				return Task.FromResult(ActionResult.Accepted(Strings.Actions.PlayCatalogItem.PickerRequested()));
			}

			var item = kind == MusicPlayerCatalogItemKind.Playlist
				? MusicLibrary.FindPlaylist(itemId) is { } playlist
					? new MusicPlayerCatalogItem(playlist.Id, playlist.Title, MusicPlayerCatalogItemKind.Playlist)
					: null
				: MusicLibrary.FindTrack(itemId) is { } track
					? new MusicPlayerCatalogItem(track.Id, track.Title, MusicPlayerCatalogItemKind.Track)
					: null;

			if (item is null)
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.NotFound,
					Strings.Errors.CatalogItemNotFound(itemId)));
			}

			var engine = integration.Library.Engine;
			engine.SetShuffle(context.Parameters.GetValueOrDefault("shuffle") is true);
			engine.PlayItem(item);

			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Actions/SetVolumeAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleMusicPlayerPlugin.Actions;

/// <summary>
/// Sets one player's volume from a button. A Slider widget binds the writable <c>sample_music_volume</c>
/// variable instead, which reads the volume the player actually has back.
/// </summary>
internal sealed class SetVolumeAction(MusicPlayerIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	private const double Min = 0;
	private const double Max = 100;

	public string Id => "set-volume";

	public LocalizedText Name => Strings.Actions.SetVolume.Name();

	public LocalizedText Description => Strings.Actions.SetVolume.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("player", label: Strings.Fields.Player.Label(), required: true),
		ActionParameter.Slider("volume", Min, Max, label: Strings.Fields.Volume.Label(), step: 1, defaultValue: 60)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
		=> Task.FromResult(new DynamicOptionsResult { Options = integration.InstanceOptions() });

	private sealed class Executor(MusicPlayerIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("player") is not string instanceId ||
				integration.EngineOf(instanceId) is not { } engine)
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.InvalidValue(Strings.Fields.Player.Label())));
			}

			if (context.Parameters.GetValueOrDefault("volume") is not double volume)
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.InvalidValue(Strings.Fields.Volume.Label())));
			}

			engine.SetVolume((int)volume);
			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Actions/TogglePlaybackAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleMusicPlayerPlugin.Actions;

/// <summary>
/// The relationship between a provider capability and an ordinary action: the host's own media widget
/// drives <c>IMusicPlayer.TogglePlayPauseAsync</c>, and this action reaches the same state so a plain
/// button can do it too.
/// </summary>
internal sealed class TogglePlaybackAction(MusicPlayerIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "toggle-playback";

	public LocalizedText Name => Strings.Actions.TogglePlayback.Name();

	public LocalizedText Description => Strings.Actions.TogglePlayback.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("player", label: Strings.Fields.Player.Label(), required: true)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
		=> Task.FromResult(new DynamicOptionsResult { Options = integration.InstanceOptions() });

	private sealed class Executor(MusicPlayerIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("player") is not string instanceId ||
				integration.EngineOf(instanceId) is not { } engine)
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.InvalidValue(Strings.Fields.Player.Label())));
			}

			engine.Toggle();
			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Actions/TransferPlaybackAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleMusicPlayerPlugin.Actions;

/// <summary>
/// Moves playback to another output device, with the device picker as the fallback when none was
/// configured - the device-shaped counterpart to <see cref="PlayCatalogItemAction"/>.
/// </summary>
internal sealed class TransferPlaybackAction(MusicPlayerIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "transfer-playback";

	public LocalizedText Name => Strings.Actions.TransferPlayback.Name();

	public LocalizedText Description => Strings.Actions.TransferPlayback.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("device",
			label: Strings.Fields.Device.Label(),
			description: Strings.Actions.TransferPlayback.Device.Description()),
		ActionParameter.Toggle("startPlayback",
			label: Strings.Actions.TransferPlayback.StartPlayback.Label(),
			defaultValue: true)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	public async Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		var devices = await integration.Library.GetDevicesAsync(cancellationToken);

		// A device name comes from the device itself, so it is already in its final form: a literal.
		return new DynamicOptionsResult
		{
			Options = [.. devices.Select(device => new ActionParameterOption { Value = device.Id, Label = device.Name })]
		};
	}

	private sealed class Executor(MusicPlayerIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			var startPlayback = context.Parameters.GetValueOrDefault("startPlayback") is not false;

			if (context.Parameters.GetValueOrDefault("device") is not string { Length: > 0 } deviceId)
			{
				context.Interactions?.RequestDevicePicker(context.OriginClientId,
					MusicPlayerIntegration.LibraryInstanceId,
					startPlayback,
					prompt: "Pick an output device");

				return ActionResult.Accepted(Strings.Actions.TransferPlayback.PickerRequested());
			}

			var devices = await integration.Library.GetDevicesAsync(context.CancellationToken);
			if (!devices.Any(device => string.Equals(device.Id, deviceId, StringComparison.Ordinal)))
			{
				return ActionResult.Failed(ActionErrorCodes.NotFound, Strings.Errors.DeviceNotFound(deviceId));
			}

			await integration.Library.TransferPlaybackAsync(deviceId, startPlayback, context.CancellationToken);
			return ActionResult.Success();
		}
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Assets/icon.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
	<path d="M44 12 24 17v25.5a9 9 0 1 0 5 8V26l15-3.8z" fill="#BD10E0" />
	<circle cx="44" cy="19" r="8" fill="#50E3C2" />
</svg>
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Localization/Strings.resx

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
  <data name="Fields.Player.Label" xml:space="preserve">
    <value>Player</value>
  </data>
  <data name="Fields.Track.Label" xml:space="preserve">
    <value>Track</value>
  </data>
  <data name="Fields.Artist.Label" xml:space="preserve">
    <value>Artist</value>
  </data>
  <data name="Fields.Volume.Label" xml:space="preserve">
    <value>Volume (%)</value>
  </data>
  <data name="Fields.Device.Label" xml:space="preserve">
    <value>Device</value>
  </data>
  <data name="Fields.Item.Label" xml:space="preserve">
    <value>Item</value>
  </data>
  <data name="Fields.Kind.Label" xml:space="preserve">
    <value>Kind</value>
  </data>
  <data name="Actions.TogglePlayback.Name" xml:space="preserve">
    <value>Play/pause</value>
  </data>
  <data name="Actions.TogglePlayback.Description" xml:space="preserve">
    <value>Toggles playback on one of the sample players.</value>
  </data>
  <data name="Actions.SetVolume.Name" xml:space="preserve">
    <value>Set volume</value>
  </data>
  <data name="Actions.SetVolume.Description" xml:space="preserve">
    <value>Sets the volume of one of the sample players.</value>
  </data>
  <data name="Actions.PlayCatalogItem.Name" xml:space="preserve">
    <value>Play from library</value>
  </data>
  <data name="Actions.PlayCatalogItem.Description" xml:space="preserve">
    <value>Plays a track or playlist from the sample library.</value>
  </data>
  <data name="Actions.PlayCatalogItem.Item.Description" xml:space="preserve">
    <value>Leave empty to pick one on the client that pressed the button.</value>
  </data>
  <data name="Actions.PlayCatalogItem.Shuffle.Label" xml:space="preserve">
    <value>Shuffle the playlist</value>
  </data>
  <data name="Actions.PlayCatalogItem.PickerRequested" xml:space="preserve">
    <value>Asked the client to pick an item.</value>
  </data>
  <data name="Actions.TransferPlayback.Name" xml:space="preserve">
    <value>Transfer playback</value>
  </data>
  <data name="Actions.TransferPlayback.Description" xml:space="preserve">
    <value>Moves playback of the sample library to another device.</value>
  </data>
  <data name="Actions.TransferPlayback.Device.Description" xml:space="preserve">
    <value>Leave empty to pick one on the client that pressed the button.</value>
  </data>
  <data name="Actions.TransferPlayback.StartPlayback.Label" xml:space="preserve">
    <value>Start playing after the transfer</value>
  </data>
  <data name="Actions.TransferPlayback.PickerRequested" xml:space="preserve">
    <value>Asked the client to pick a device.</value>
  </data>
  <data name="CatalogKinds.Track" xml:space="preserve">
    <value>Track</value>
  </data>
  <data name="CatalogKinds.Playlist" xml:space="preserve">
    <value>Playlist</value>
  </data>
  <data name="Events.TrackChanged.Name" xml:space="preserve">
    <value>Track changed</value>
  </data>
  <data name="Events.TrackChanged.Description" xml:space="preserve">
    <value>Raised when a player moves to another track.</value>
  </data>
  <data name="Errors.CatalogItemNotFound" xml:space="preserve">
    <value>The sample library has no item with id {itemId}.</value>
  </data>
  <data name="Errors.DeviceNotFound" xml:space="preserve">
    <value>The sample library has no device with id {deviceId}.</value>
  </data>
</root>
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/MacroDeck.SampleMusicPlayerPlugin.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <IsPackable>false</IsPackable>
        <UserSecretsId>MacroDeck.SampleMusicPlayerPlugin-PluginDevelopment</UserSecretsId>
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

## File: src/MacroDeck.SampleMusicPlayerPlugin/MusicPlayerIntegration.cs

```csharp
using System.Globalization;
using MacroDeck.SampleMusicPlayerPlugin.Actions;
using MacroDeck.SampleMusicPlayerPlugin.Player;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Events;
using MacroDeck.Sdk.MusicPlayer;
using MacroDeck.Sdk.Variables;

namespace MacroDeck.SampleMusicPlayerPlugin;

/// <summary>
/// Two synthetic players over one shared library: a full-surface one with catalogue and devices, and a
/// transport-only one. Actions, variables and the track-changed event all read the same playback
/// state, so what a widget shows and what a variable says cannot disagree.
/// </summary>
public sealed class MusicPlayerIntegration : IPluginIntegration, IMusicPlayerProvider, IVariableProvider,
	IEventProvider, IDynamicEventOptionsProvider
{
	internal const string LibraryInstanceId = "library";
	internal const string SpeakerInstanceId = "speaker";

	internal const string TrackChangedEventId = "track-changed";

	private readonly LibraryMusicPlayer _library;
	private readonly SpeakerMusicPlayer _speaker;

	private IIntegrationContext? _context;

	public MusicPlayerIntegration(TimeProvider timeProvider)
	{
		_library = new LibraryMusicPlayer(new PlaybackEngine(timeProvider, engine => PublishTrackChanged(LibraryInstanceId, engine)));
		_speaker = new SpeakerMusicPlayer(new PlaybackEngine(timeProvider, engine => PublishTrackChanged(SpeakerInstanceId, engine)));

		Actions =
		[
			new TogglePlaybackAction(this),
			new SetVolumeAction(this),
			new PlayCatalogItemAction(this),
			new TransferPlaybackAction(this)
		];
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

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

	public IReadOnlyList<MusicPlayerInstance> GetInstances() =>
	[
		new(LibraryInstanceId, "Sample library"),
		new(SpeakerInstanceId, "Sample speaker")
	];

	public IMusicPlayer? GetPlayer(string instanceId) => instanceId switch
	{
		LibraryInstanceId => _library,
		SpeakerInstanceId => _speaker,
		_ => null
	};

	internal LibraryMusicPlayer Library => _library;

	internal PlaybackEngine? EngineOf(string instanceId) => instanceId switch
	{
		LibraryInstanceId => _library.Engine,
		SpeakerInstanceId => _speaker.Engine,
		_ => null
	};

	public IReadOnlyList<VariableDefinition> Variables { get; } =
	[
		VariableDefinition.Eager("sample_music_track", VariableType.Text) with { Id = "track" },
		VariableDefinition.Eager("sample_music_artist", VariableType.Text) with { Id = "artist" },
		VariableDefinition.Eager("sample_music_is_playing", VariableType.Boolean) with { Id = "is-playing" },
		// Writable, so a Slider widget bound to it drives the volume and reads the real one back. Volume is
		// cheap to apply continuously, so the drag is not deferred to release.
		VariableDefinition.Eager("sample_music_volume", VariableType.Numeric) with
		{
			Id = "volume",
			Unit = "%",
			SemanticKind = VariableSemanticKinds.Percentage,
			Write = new VariableWriteCapability()
		}
	];

	/// <summary>Reports the library instance, addressed by local id. An id this provider does not know
	/// reads as unavailable, which the host renders as an empty value rather than an error.</summary>
	public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
	{
		var engine = _library.Engine;
		return ValueTask.FromResult(localId switch
		{
			"track" => VariableReading.Of(engine.CurrentTrack.Title),
			"artist" => VariableReading.Of(engine.CurrentTrack.Artist),
			"is-playing" => VariableReading.Of(engine.IsPlaying),
			"volume" => VariableReading.Of(engine.VolumePercent, 0, 100, 1),
			_ => VariableReading.Unavailable
		});
	}

	/// <summary>Only called for "volume", the one variable declaring a write. The engine clamps, and the
	/// clamped value arrives on the next read.</summary>
	public ValueTask<VariableWriteResult> SetValueAsync(string localId, object? value, CancellationToken cancellationToken = default)
	{
		if (value is not (double or int or long))
		{
			return ValueTask.FromResult(VariableWriteResult.InvalidValue());
		}

		_library.Engine.SetVolume((int)Convert.ToDouble(value, CultureInfo.InvariantCulture));
		return ValueTask.FromResult(VariableWriteResult.Applied());
	}

	public IReadOnlyList<EventDefinition> EventDefinitions { get; } =
	[
		new EventDefinition
		{
			Id = TrackChangedEventId,
			Name = Strings.Events.TrackChanged.Name(),
			Description = Strings.Events.TrackChanged.Description(),
			// A configuration parameter narrows what the user subscribes to; its options come from
			// GetEventOptionsAsync below rather than being fixed at declaration time.
			ConfigurationParameters =
			[
				ActionParameter.DynamicChoice("player", label: Strings.Fields.Player.Label(), required: true)
			],
			PayloadParameters =
			[
				ActionParameter.Text("player", Strings.Fields.Player.Label()),
				ActionParameter.Text("track", Strings.Fields.Track.Label()),
				ActionParameter.Text("artist", Strings.Fields.Artist.Label())
			]
		}
	];

	public Task<DynamicOptionsResult> GetEventOptionsAsync(EventOptionsContext context, CancellationToken cancellationToken)
		=> Task.FromResult(new DynamicOptionsResult { Options = InstanceOptions() });

	/// <summary>An instance's display name is a plain string on the provider contract - it names a
	/// configured account, not UI text - so it travels into the option as a literal.</summary>
	internal IReadOnlyList<ActionParameterOption> InstanceOptions()
		=> [.. GetInstances().Select(instance => new ActionParameterOption { Value = instance.Id, Label = instance.DisplayName })];

	private void PublishTrackChanged(string instanceId, PlaybackEngine engine)
		=> _context?.Events.Publish(TrackChangedEventId, new Dictionary<string, object?>
		{
			["player"] = instanceId,
			["track"] = engine.CurrentTrack.Title,
			["artist"] = engine.CurrentTrack.Artist
		});
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Player/LibraryMusicPlayer.cs

```csharp
using MacroDeck.Sdk.MusicPlayer;

namespace MacroDeck.SampleMusicPlayerPlugin.Player;

/// <summary>
/// The full-surface instance: transport, catalogue browsing and output devices. The host reads the
/// last two off the player object itself (<c>HasCatalog</c>/<c>HasDevices</c> on the instance
/// descriptor), which is why they are implemented here rather than on the provider - see
/// <see cref="SpeakerMusicPlayer"/> for an instance that only supports transport.
/// </summary>
// ICatalogMusicPlayer rather than IMusicPlayer + IMusicPlayerCatalogProvider: browsing a catalogue and
// being able to play something out of it are two different capabilities, and play-item is only offered
// to a player that declares the second one.
internal sealed class LibraryMusicPlayer(PlaybackEngine engine)
	: ICatalogMusicPlayer, IMusicPlayerDeviceProvider
{
	private readonly List<MusicPlayerDevice> _devices =
	[
		new("device-living-room", "Living room", "speaker", IsActive: true, VolumePercent: 60),
		new("device-kitchen", "Kitchen", "speaker"),
		new("device-headphones", "Headphones", "headphones")
	];

	internal PlaybackEngine Engine { get; } = engine;

	public Task<MusicPlayerState> GetStateAsync(CancellationToken cancellationToken = default)
		=> Task.FromResult(PlayerState.From(Engine, ActiveDevice));

	public Task<MusicPlayerArtwork?> GetArtworkAsync(string artworkId, CancellationToken cancellationToken = default)
		=> Task.FromResult(MusicLibrary.Artwork(artworkId));

	public Task PlayAsync(CancellationToken cancellationToken = default)
	{
		Engine.Play();
		return Task.CompletedTask;
	}

	public Task PlayItemAsync(MusicPlayerCatalogItem item, CancellationToken cancellationToken = default)
	{
		Engine.PlayItem(item);
		return Task.CompletedTask;
	}

	public Task PauseAsync(CancellationToken cancellationToken = default)
	{
		Engine.Pause();
		return Task.CompletedTask;
	}

	public Task TogglePlayPauseAsync(CancellationToken cancellationToken = default)
	{
		Engine.Toggle();
		return Task.CompletedTask;
	}

	public Task NextAsync(CancellationToken cancellationToken = default)
	{
		Engine.Next();
		return Task.CompletedTask;
	}

	public Task PreviousAsync(CancellationToken cancellationToken = default)
	{
		Engine.Previous();
		return Task.CompletedTask;
	}

	public Task SeekAsync(TimeSpan position, CancellationToken cancellationToken = default)
	{
		Engine.Seek(position);
		return Task.CompletedTask;
	}

	public Task SetVolumeAsync(int volumePercent, CancellationToken cancellationToken = default)
	{
		Engine.SetVolume(volumePercent);
		return Task.CompletedTask;
	}

	public Task SetShuffleAsync(bool enabled, CancellationToken cancellationToken = default)
	{
		Engine.SetShuffle(enabled);
		return Task.CompletedTask;
	}

	public Task SetRepeatModeAsync(RepeatMode mode, CancellationToken cancellationToken = default)
	{
		Engine.SetRepeatMode(mode);
		return Task.CompletedTask;
	}

	/// <summary>An empty result here means the catalogue really is empty. A read that fails has to throw,
	/// so the UI can offer a retry instead of showing "nothing found" - see capability-parity.md.</summary>
	public Task<IReadOnlyList<MusicPlayerCatalogItem>> GetCatalogAsync(
		string instanceId,
		MusicPlayerCatalogItemKind kind,
		string? filter,
		CancellationToken cancellationToken)
		=> Task.FromResult(MusicLibrary.CatalogItems(kind, filter));

	public Task<IReadOnlyList<MusicPlayerDevice>> GetDevicesAsync(CancellationToken cancellationToken)
		=> Task.FromResult<IReadOnlyList<MusicPlayerDevice>>([.. _devices]);

	public Task TransferPlaybackAsync(string deviceId, bool startPlayback, CancellationToken cancellationToken)
	{
		var target = _devices.FindIndex(device => string.Equals(device.Id, deviceId, StringComparison.Ordinal));
		if (target < 0)
		{
			return Task.CompletedTask;
		}

		for (var i = 0; i < _devices.Count; i++)
		{
			_devices[i] = _devices[i] with { IsActive = i == target };
		}

		if (startPlayback)
		{
			Engine.Play();
		}

		return Task.CompletedTask;
	}

	internal MusicPlayerDevice? ActiveDevice => _devices.FirstOrDefault(device => device.IsActive);
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Player/MusicLibrary.cs

```csharp
using System.Globalization;
using System.Text;
using MacroDeck.Sdk.MusicPlayer;

namespace MacroDeck.SampleMusicPlayerPlugin.Player;

/// <summary>A fixed catalogue of made-up tracks and playlists, so the sample needs no music service.</summary>
internal static class MusicLibrary
{
	internal static IReadOnlyList<LibraryTrack> Tracks { get; } =
	[
		new("track-solar-drift", "Solar Drift", "Nova Fields", "Orbital", TimeSpan.FromSeconds(214), "#F5A623"),
		new("track-night-transit", "Night Transit", "Nova Fields", "Orbital", TimeSpan.FromSeconds(187), "#4A90D9"),
		new("track-paper-lanterns", "Paper Lanterns", "Halcyon Row", "Slow Light", TimeSpan.FromSeconds(243), "#7ED321"),
		new("track-quiet-machines", "Quiet Machines", "Halcyon Row", "Slow Light", TimeSpan.FromSeconds(198), "#BD10E0"),
		new("track-harbour-lights", "Harbour Lights", "Ash & Ivory", "Tide", TimeSpan.FromSeconds(226), "#50E3C2")
	];

	internal static IReadOnlyList<LibraryPlaylist> Playlists { get; } =
	[
		new("playlist-focus", "Focus", ["track-solar-drift", "track-quiet-machines", "track-harbour-lights"]),
		new("playlist-evening", "Evening", ["track-night-transit", "track-paper-lanterns"])
	];

	internal static LibraryTrack? FindTrack(string id)
		=> Tracks.FirstOrDefault(track => string.Equals(track.Id, id, StringComparison.Ordinal));

	internal static LibraryPlaylist? FindPlaylist(string id)
		=> Playlists.FirstOrDefault(playlist => string.Equals(playlist.Id, id, StringComparison.Ordinal));

	/// <summary>Resolves a playlist to its tracks, skipping ids the library no longer knows.</summary>
	internal static IReadOnlyList<LibraryTrack> TracksOf(LibraryPlaylist playlist)
		=> [.. playlist.TrackIds.Select(FindTrack).OfType<LibraryTrack>()];

	internal static IReadOnlyList<MusicPlayerCatalogItem> CatalogItems(MusicPlayerCatalogItemKind kind, string? filter)
	{
		var items = kind switch
		{
			MusicPlayerCatalogItemKind.Playlist => Playlists.Select(playlist => new MusicPlayerCatalogItem(
				playlist.Id,
				playlist.Title,
				MusicPlayerCatalogItemKind.Playlist,
				Subtitle: $"{playlist.TrackIds.Count} tracks")),
			_ => Tracks.Select(track => new MusicPlayerCatalogItem(
				track.Id,
				track.Title,
				MusicPlayerCatalogItemKind.Track,
				Subtitle: track.Artist,
				ArtworkId: track.Id,
				Duration: track.Duration))
		};

		if (!string.IsNullOrWhiteSpace(filter))
		{
			items = items.Where(item => item.Title.Contains(filter, StringComparison.OrdinalIgnoreCase));
		}

		return [.. items];
	}

	/// <summary>
	/// Cover art, drawn here rather than shipped as files. A real integration downloads the artwork its
	/// service reports; what matters for the contract is that the bytes and the MIME type match the
	/// <c>ArtworkId</c> the state reported.
	/// </summary>
	internal static MusicPlayerArtwork? Artwork(string artworkId)
	{
		if (FindTrack(artworkId) is not { } track)
		{
			return null;
		}

		var initials = string.Concat(track.Title.Split(' ', StringSplitOptions.RemoveEmptyEntries)
			.Take(2)
			.Select(word => char.ToUpper(word[0], CultureInfo.InvariantCulture)));

		var svg = $"""
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
				<rect width="64" height="64" rx="8" fill="{track.Color}" />
				<text x="32" y="40" text-anchor="middle" font-family="sans-serif" font-size="22" fill="#FFFFFF">{initials}</text>
			</svg>
			""";

		return new MusicPlayerArtwork(Encoding.UTF8.GetBytes(svg), "image/svg+xml");
	}
}

internal sealed record LibraryTrack(
	string Id,
	string Title,
	string Artist,
	string Album,
	TimeSpan Duration,
	string Color);

internal sealed record LibraryPlaylist(string Id, string Title, IReadOnlyList<string> TrackIds);
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Player/PlaybackEngine.cs

```csharp
using MacroDeck.Sdk.MusicPlayer;

namespace MacroDeck.SampleMusicPlayerPlugin.Player;

/// <summary>
/// The playback state machine both player instances run on. It owns no SDK contract - the players
/// adapt it - so the transport rules stay readable in one place.
///
/// Position is derived from <see cref="TimeProvider"/> rather than a timer: a paused player reports the
/// position it stopped at, a playing one reports elapsed time since it started, and a test advancing a
/// <c>ManualTimeProvider</c> sees the same progression a real clock would produce.
/// </summary>
internal sealed class PlaybackEngine(TimeProvider timeProvider, Action<PlaybackEngine> trackChanged)
{
	private readonly Lock _gate = new();

	private IReadOnlyList<LibraryTrack> _queue = MusicLibrary.Tracks;
	private int _index;
	private TimeSpan _offset;
	private DateTimeOffset? _playingSince;

	internal LibraryTrack CurrentTrack
	{
		get
		{
			lock (_gate)
			{
				return _queue[_index];
			}
		}
	}

	internal bool IsPlaying
	{
		get
		{
			lock (_gate)
			{
				return _playingSince is not null;
			}
		}
	}

	internal int VolumePercent { get; private set; } = 60;

	internal bool ShuffleEnabled { get; private set; }

	internal RepeatMode RepeatMode { get; private set; } = RepeatMode.Off;

	internal TimeSpan Position
	{
		get
		{
			lock (_gate)
			{
				var position = _playingSince is { } since
					? _offset + (timeProvider.GetUtcNow() - since)
					: _offset;
				var duration = _queue[_index].Duration;
				return position > duration ? duration : position;
			}
		}
	}

	internal void Play()
	{
		lock (_gate)
		{
			_playingSince ??= timeProvider.GetUtcNow();
		}
	}

	internal void Pause()
	{
		lock (_gate)
		{
			if (_playingSince is not { } since)
			{
				return;
			}

			_offset += timeProvider.GetUtcNow() - since;
			_playingSince = null;
		}
	}

	internal void Toggle()
	{
		if (IsPlaying)
		{
			Pause();
		}
		else
		{
			Play();
		}
	}

	internal void Next() => Move(1);

	internal void Previous() => Move(-1);

	internal void Seek(TimeSpan position)
	{
		lock (_gate)
		{
			var duration = _queue[_index].Duration;
			_offset = position < TimeSpan.Zero ? TimeSpan.Zero : position > duration ? duration : position;
			if (_playingSince is not null)
			{
				_playingSince = timeProvider.GetUtcNow();
			}
		}
	}

	internal void SetVolume(int volumePercent) => VolumePercent = Math.Clamp(volumePercent, 0, 100);

	internal void SetShuffle(bool enabled) => ShuffleEnabled = enabled;

	internal void SetRepeatMode(RepeatMode mode) => RepeatMode = mode;

	/// <summary>Replaces the queue with one item's tracks and starts at its first track.</summary>
	internal void PlayItem(MusicPlayerCatalogItem item)
	{
		var tracks = item.Kind == MusicPlayerCatalogItemKind.Playlist
			? MusicLibrary.FindPlaylist(item.Id) is { } playlist ? MusicLibrary.TracksOf(playlist) : []
			: MusicLibrary.FindTrack(item.Id) is { } track ? [track] : [];

		if (tracks.Count == 0)
		{
			return;
		}

		lock (_gate)
		{
			_queue = tracks;
			_index = 0;
			_offset = TimeSpan.Zero;
			_playingSince = timeProvider.GetUtcNow();
		}

		trackChanged(this);
	}

	private void Move(int direction)
	{
		lock (_gate)
		{
			_index = (_index + direction + _queue.Count) % _queue.Count;
			_offset = TimeSpan.Zero;
			if (_playingSince is not null)
			{
				_playingSince = timeProvider.GetUtcNow();
			}
		}

		trackChanged(this);
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Player/PlayerState.cs

```csharp
using MacroDeck.Sdk.MusicPlayer;

namespace MacroDeck.SampleMusicPlayerPlugin.Player;

/// <summary>Projects the engine onto the state contract, so both player instances report the same shape.</summary>
internal static class PlayerState
{
	internal static MusicPlayerState From(PlaybackEngine engine, MusicPlayerDevice? device)
	{
		var track = engine.CurrentTrack;
		return new MusicPlayerState
		{
			IsConnected = true,
			PlaybackState = engine.IsPlaying ? PlaybackState.Playing : PlaybackState.Paused,
			TrackName = track.Title,
			Artists = [track.Artist],
			AlbumName = track.Album,
			ArtworkId = track.Id,
			Position = engine.Position,
			Duration = track.Duration,
			VolumePercent = engine.VolumePercent,
			ShuffleEnabled = engine.ShuffleEnabled,
			RepeatMode = engine.RepeatMode,
			DeviceName = device?.Name,
			DeviceType = device?.Type
		};
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Player/SpeakerMusicPlayer.cs

```csharp
using MacroDeck.Sdk.MusicPlayer;

namespace MacroDeck.SampleMusicPlayerPlugin.Player;

/// <summary>
/// A transport-only instance: no catalogue, no devices. It implements <see cref="IMusicPlayer"/> and
/// nothing else, so the host reports <c>HasCatalog</c>/<c>HasDevices</c> as false for it and never
/// offers the corresponding operations - the same way a real service supports browsing on some
/// accounts but not others.
/// </summary>
internal sealed class SpeakerMusicPlayer(PlaybackEngine engine) : IMusicPlayer
{
	internal PlaybackEngine Engine { get; } = engine;

	public Task<MusicPlayerState> GetStateAsync(CancellationToken cancellationToken = default)
		=> Task.FromResult(PlayerState.From(Engine, device: null));

	public Task<MusicPlayerArtwork?> GetArtworkAsync(string artworkId, CancellationToken cancellationToken = default)
		=> Task.FromResult(MusicLibrary.Artwork(artworkId));

	public Task PlayAsync(CancellationToken cancellationToken = default)
	{
		Engine.Play();
		return Task.CompletedTask;
	}

	/// <summary>Reachable even without a catalogue: the host can still hand an item another instance
	/// browsed, so the operation stays supported.</summary>
	public Task PlayItemAsync(MusicPlayerCatalogItem item, CancellationToken cancellationToken = default)
	{
		Engine.PlayItem(item);
		return Task.CompletedTask;
	}

	public Task PauseAsync(CancellationToken cancellationToken = default)
	{
		Engine.Pause();
		return Task.CompletedTask;
	}

	public Task TogglePlayPauseAsync(CancellationToken cancellationToken = default)
	{
		Engine.Toggle();
		return Task.CompletedTask;
	}

	public Task NextAsync(CancellationToken cancellationToken = default)
	{
		Engine.Next();
		return Task.CompletedTask;
	}

	public Task PreviousAsync(CancellationToken cancellationToken = default)
	{
		Engine.Previous();
		return Task.CompletedTask;
	}

	public Task SeekAsync(TimeSpan position, CancellationToken cancellationToken = default)
	{
		Engine.Seek(position);
		return Task.CompletedTask;
	}

	public Task SetVolumeAsync(int volumePercent, CancellationToken cancellationToken = default)
	{
		Engine.SetVolume(volumePercent);
		return Task.CompletedTask;
	}

	public Task SetShuffleAsync(bool enabled, CancellationToken cancellationToken = default)
	{
		Engine.SetShuffle(enabled);
		return Task.CompletedTask;
	}

	public Task SetRepeatModeAsync(RepeatMode mode, CancellationToken cancellationToken = default)
	{
		Engine.SetRepeatMode(mode);
		return Task.CompletedTask;
	}
}
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Program.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Serilog;
using MacroDeck.SampleMusicPlayerPlugin;

// Identity, description and icon are not set here: they come from manifest.json at the content root.
// Strings is generated from Localization/*.resx, so UseLocalization is what makes every LocalizedText
// this plugin hands the host resolve in the reader's language rather than falling back to its key.
var plugin = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<MusicPlayerIntegration>()
	.Build();

await plugin.RunAsync();
```

## File: src/MacroDeck.SampleMusicPlayerPlugin/Properties/launchSettings.json

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

## File: src/MacroDeck.SampleMusicPlayerPlugin/README.md

````markdown
# Sample Music Player plugin

The complete music-player surface, on a made-up library rather than a real service: transport
controls, artwork, catalogue browsing, output devices and two instances with deliberately different
capabilities. Read it when your plugin drives something that plays media.

## Read these first

- **`MusicPlayerIntegration.cs`** - the provider: two instances over one library, plus the variables and
  the `track-changed` event, and `IDynamicEventOptionsProvider` so a subscription can name a player.
- **`Player/PlaybackEngine.cs`** - the state machine both instances run on. Position is derived from
  `TimeProvider` rather than a timer, so a paused player reports where it stopped and a test with a
  manual clock sees the same progression a real one would.
- **`Player/LibraryMusicPlayer.cs`** - the full instance: `IMusicPlayer` plus `IMusicPlayerCatalogProvider`
  and `IMusicPlayerDeviceProvider`. The host reads those two off the player object itself, which is why
  they live here and not on the provider.
- **`Player/SpeakerMusicPlayer.cs`** - the transport-only instance. It implements `IMusicPlayer` and
  nothing else, so the host reports `HasCatalog`/`HasDevices` as false for it and never offers those
  operations - the same way a real service supports browsing on some accounts but not others.
- **`Actions/PlayCatalogItemAction.cs`** - dynamic options that depend on another parameter, plus the
  item picker: leaving the item empty asks the client that pressed the button to choose one.
- **`Actions/TransferPlaybackAction.cs`** - the device-shaped counterpart, with the device picker.
- **`Actions/SetVolumeAction.cs`** - sets the selected player's volume from a button. A Slider widget
  binds the writable `sample_music_volume` variable instead, which reads the actual volume back.

Catalogue and device reads are the one place a failure must *throw* rather than degrade to an empty
result: "nothing found" and "could not load" have to look different in the UI. Everything else here
degrades - see the parity matrix.
- **`Localization/Strings.resx`** - every string a user reads. The `Fields.*` group is shared by
  several actions and the event rather than repeated per action, and a track title, playlist name or
  device name stays a literal: it is content, already in its final form.

## Running it against a local host

Use this project's **Macro Deck - Real Host** launch profile as described in the repository's
[run and debug guide](../../README.md#run-and-debug-against-macro-deck). Then add the "Sample library"
instance to a Music Player widget. Playback, artwork, the catalogue and the device list all work
without any account.

## Testing it

```bash
dotnet test tests/MacroDeck.SampleMusicPlayerPlugin.Tests
```

`MusicPlayerIntegrationTests` drives the capability directly and advances `harness.Clock` to prove the
position tracks the clock; `MusicPlayerOverTheWireTests` covers what changes shape on the wire - the
position, the enums and the artwork bytes.

## Packaging it

`macrodeck-build.json` names one self-contained `dotnet publish` per platform, and the manifest's
entrypoints name what that publish actually produces:

```bash
macrodeck-plugin build --output ./artifacts
```

```bash
macrodeck-plugin validate --artifact ./artifacts/app.macro-deck.sample-music-player-1.0.0.macroDeckPlugin --level Publication
```
````

## File: src/MacroDeck.SampleMusicPlayerPlugin/macrodeck-build.json

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleMusicPlayerPlugin.csproj",
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
        "MacroDeck.SampleMusicPlayerPlugin.csproj",
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
        "MacroDeck.SampleMusicPlayerPlugin.csproj",
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
        "MacroDeck.SampleMusicPlayerPlugin.csproj",
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

## File: src/MacroDeck.SampleMusicPlayerPlugin/manifest.json

```json
{
  "$schema": "https://schemas.macro-deck.app/plugin-manifest-v1.schema.json",
  "manifestVersion": 1,
  "id": "app.macro-deck.sample-music-player",
  "name": "Sample Music Player",
  "version": "1.0.0",
  "description": "Synthetic music player: transport controls, artwork, catalogue browsing, output devices, two instances, plus actions, variables and events on the same playback state.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": {
      "executable": "runtimes/win-x64/MacroDeck.SampleMusicPlayerPlugin.exe"
    },
    "osx-arm64": {
      "executable": "runtimes/osx-arm64/MacroDeck.SampleMusicPlayerPlugin"
    },
    "osx-x64": {
      "executable": "runtimes/osx-x64/MacroDeck.SampleMusicPlayerPlugin"
    },
    "linux-x64": {
      "executable": "runtimes/linux-x64/MacroDeck.SampleMusicPlayerPlugin"
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
    "host:variables",
    "events:publish"
  ]
}
```

## File: tests/MacroDeck.SampleMusicPlayerPlugin.Tests/LocalizationTests.cs

```csharp
using NUnit.Framework;

namespace MacroDeck.SampleMusicPlayerPlugin.Tests;

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
		Assert.That(Strings.LocalizationCatalog.Scope, Is.EqualTo("plugin:app.macro-deck.sample-music-player"));
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
		Assert.That(Strings.LocalizationCatalog.KeysOf("en"), Does.Contain("Actions.TogglePlayback.Name"));
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

## File: tests/MacroDeck.SampleMusicPlayerPlugin.Tests/MacroDeck.SampleMusicPlayerPlugin.Tests.csproj

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
        <ProjectReference Include="..\..\src\MacroDeck.SampleMusicPlayerPlugin\MacroDeck.SampleMusicPlayerPlugin.csproj" />
    </ItemGroup>

</Project>
```

## File: tests/MacroDeck.SampleMusicPlayerPlugin.Tests/MusicPlayerIntegrationTests.cs

```csharp
using MacroDeck.Plugin.Protocol.Capabilities.Actions;
using MacroDeck.Plugin.Protocol.Capabilities.Events;
using MacroDeck.Plugin.Protocol.Capabilities.MusicPlayer;
using MacroDeck.Plugin.Protocol.Capabilities.Variables;
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.SampleMusicPlayerPlugin.Tests;

[TestFixture]
public sealed class MusicPlayerIntegrationTests
{
	private const string LibraryId = "library";
	private const string SpeakerId = "speaker";

	private static readonly string[] _eveningOnly = ["Evening"];
	private static readonly string[] _playlistIds = ["playlist-focus", "playlist-evening"];
	private static readonly string[] _instanceIds = [LibraryId, SpeakerId];

	[Test]
	public async Task Only_the_instance_that_implements_them_advertises_catalog_and_devices()
	{
		await using var harness = await CreateAsync();

		var instances = (await harness.MusicPlayer.GetInstancesAsync()).DataAs<MusicPlayerInstancesResult>();

		var library = instances!.Instances.Single(instance => instance.Id == LibraryId);
		var speaker = instances.Instances.Single(instance => instance.Id == SpeakerId);

		Assert.That(library.HasCatalog, Is.True);
		Assert.That(library.HasDevices, Is.True);
		Assert.That(speaker.HasCatalog, Is.False);
		Assert.That(speaker.HasDevices, Is.False);
	}

	[Test]
	public async Task Toggling_starts_playback_and_toggling_again_stops_it()
	{
		await using var harness = await CreateAsync();

		await harness.MusicPlayer.ToggleAsync(Instance(LibraryId));
		Assert.That((await StateAsync(harness, LibraryId)).PlaybackState, Is.EqualTo("Playing"));

		await harness.MusicPlayer.ToggleAsync(Instance(LibraryId));
		Assert.That((await StateAsync(harness, LibraryId)).PlaybackState, Is.EqualTo("Paused"));
	}

	[Test]
	public async Task Position_follows_the_clock_while_playing_and_holds_while_paused()
	{
		await using var harness = await CreateAsync();

		await harness.MusicPlayer.PlayAsync(Instance(LibraryId));
		harness.Clock.Advance(TimeSpan.FromSeconds(30));
		Assert.That((await StateAsync(harness, LibraryId)).PositionSeconds, Is.EqualTo(30).Within(0.5));

		await harness.MusicPlayer.PauseAsync(Instance(LibraryId));
		harness.Clock.Advance(TimeSpan.FromSeconds(30));
		Assert.That((await StateAsync(harness, LibraryId)).PositionSeconds, Is.EqualTo(30).Within(0.5));
	}

	[Test]
	public async Task Seeking_past_the_end_stops_at_the_track_length()
	{
		await using var harness = await CreateAsync();

		var duration = (await StateAsync(harness, LibraryId)).DurationSeconds;
		await harness.MusicPlayer.SeekAsync(new MusicPlayerSeekArguments
		{
			InstanceId = LibraryId,
			PositionSeconds = duration!.Value + 600
		});

		Assert.That((await StateAsync(harness, LibraryId)).PositionSeconds, Is.EqualTo(duration));
	}

	[Test]
	public async Task Skipping_moves_to_another_track_and_publishes_it()
	{
		await using var harness = await CreateAsync();

		var before = await StateAsync(harness, LibraryId);
		await harness.MusicPlayer.NextAsync(Instance(LibraryId));
		var after = await StateAsync(harness, LibraryId);

		Assert.That(after.TrackName, Is.Not.EqualTo(before.TrackName));

		var published = harness.Context.Events.Published[^1];
		Assert.That(published.EventId, Is.EqualTo("track-changed"));
		Assert.That(published.Parameters!.Value.GetProperty("player").GetString(), Is.EqualTo(LibraryId));
		Assert.That(published.Parameters.Value.GetProperty("track").GetString(), Is.EqualTo(after.TrackName));
	}

	[Test]
	public async Task The_two_instances_play_independently()
	{
		await using var harness = await CreateAsync();

		await harness.MusicPlayer.PlayAsync(Instance(LibraryId));

		Assert.That((await StateAsync(harness, LibraryId)).PlaybackState, Is.EqualTo("Playing"));
		Assert.That((await StateAsync(harness, SpeakerId)).PlaybackState, Is.EqualTo("Paused"));
	}

	[Test]
	public async Task The_variables_report_what_the_player_is_playing()
	{
		await using var harness = await CreateAsync();

		await harness.MusicPlayer.SetVolumeAsync(new MusicPlayerVolumeArguments { InstanceId = LibraryId, VolumePercent = 35 });
		await harness.MusicPlayer.PlayAsync(Instance(LibraryId));

		var state = await StateAsync(harness, LibraryId);
		var track = (await harness.Variables.GetAsync("track")).DataAs<VariableReadingDto>();
		var playing = (await harness.Variables.GetAsync("is-playing")).DataAs<VariableReadingDto>();
		var volume = (await harness.Variables.GetAsync("volume")).DataAs<VariableReadingDto>();

		Assert.That(track!.Value.Text, Is.EqualTo(state.TrackName));
		Assert.That(playing!.Value.Boolean, Is.True);
		Assert.That(volume!.Value.Number, Is.EqualTo(35));
	}

	[Test]
	public async Task A_volume_outside_the_range_is_clamped_rather_than_rejected()
	{
		await using var harness = await CreateAsync();

		await harness.MusicPlayer.SetVolumeAsync(new MusicPlayerVolumeArguments { InstanceId = LibraryId, VolumePercent = 140 });

		Assert.That((await StateAsync(harness, LibraryId)).VolumePercent, Is.EqualTo(100));
	}

	[Test]
	public async Task Browsing_the_catalog_filters_by_kind_and_text()
	{
		await using var harness = await CreateAsync();

		var tracks = (await harness.MusicPlayer.GetCatalogAsync(new MusicPlayerCatalogArguments
		{
			InstanceId = LibraryId,
			Kind = "Track"
		})).DataAs<MusicPlayerCatalogResult>();

		var playlists = (await harness.MusicPlayer.GetCatalogAsync(new MusicPlayerCatalogArguments
		{
			InstanceId = LibraryId,
			Kind = "Playlist",
			Filter = "even"
		})).DataAs<MusicPlayerCatalogResult>();

		Assert.That(tracks!.Items, Is.Not.Empty);
		Assert.That(tracks.Items.Select(item => item.Kind), Is.All.EqualTo("Track"));
		Assert.That(playlists!.Items.Select(item => item.Title), Is.EqualTo(_eveningOnly));
	}

	[Test]
	public async Task Playing_a_playlist_starts_its_first_track()
	{
		await using var harness = await CreateAsync();

		var played = await harness.MusicPlayer.PlayItemAsync(new MusicPlayerPlayItemArguments
		{
			InstanceId = LibraryId,
			Item = new MusicPlayerCatalogItemDto { Id = "playlist-evening", Title = "Evening", Kind = "Playlist" }
		});

		// Asserted, not assumed: a player that does not declare ICatalogMusicPlayer is refused play-item
		// outright, and reading only the state afterwards would report that as "started the wrong track".
		Assert.That(played.Succeeded, Is.True);

		var state = await StateAsync(harness, LibraryId);
		Assert.That(state.TrackName, Is.EqualTo("Night Transit"));
		Assert.That(state.PlaybackState, Is.EqualTo("Playing"));
	}

	[Test]
	public async Task Artwork_is_served_for_the_id_the_state_reported()
	{
		await using var harness = await CreateAsync();

		var state = await StateAsync(harness, LibraryId);
		var artwork = (await harness.MusicPlayer.GetArtworkAsync(new MusicPlayerArtworkArguments
		{
			InstanceId = LibraryId,
			ArtworkId = state.ArtworkId!
		})).DataAs<MusicPlayerArtworkResult>();

		Assert.That(artwork!.MimeType, Is.EqualTo("image/svg+xml"));
		Assert.That(artwork.Data, Is.Not.Null.And.Not.Empty);
	}

	[Test]
	public async Task Transferring_playback_makes_the_target_device_the_active_one()
	{
		await using var harness = await CreateAsync();

		await harness.MusicPlayer.TransferAsync(new MusicPlayerTransferArguments
		{
			InstanceId = LibraryId,
			DeviceId = "device-kitchen",
			StartPlayback = true
		});

		var devices = (await harness.MusicPlayer.GetDevicesAsync(Instance(LibraryId))).DataAs<MusicPlayerDevicesResult>();
		var state = await StateAsync(harness, LibraryId);

		Assert.That(devices!.Devices.Single(device => device.IsActive).Id, Is.EqualTo("device-kitchen"));
		Assert.That(state.DeviceName, Is.EqualTo("Kitchen"));
		Assert.That(state.PlaybackState, Is.EqualTo("Playing"));
	}

	[Test]
	public async Task The_transport_action_reaches_the_same_state_the_capability_does()
	{
		await using var harness = await CreateAsync();

		await harness.Actions.ExecuteAsync("toggle-playback", new Dictionary<string, object?> { ["player"] = LibraryId });

		Assert.That((await StateAsync(harness, LibraryId)).PlaybackState, Is.EqualTo("Playing"));
	}

	[Test]
	public async Task An_action_naming_an_unknown_player_fails()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("toggle-playback",
			new Dictionary<string, object?> { ["player"] = "kitchen-radio" });

		Assert.That(outcome.Succeeded, Is.False);
	}

	[Test]
	public async Task The_volume_action_only_changes_the_selected_player()
	{
		await using var harness = await CreateAsync();

		await harness.Actions.ExecuteAsync("set-volume",
			new Dictionary<string, object?> { ["player"] = SpeakerId, ["volume"] = 25.0 });

		Assert.That((await StateAsync(harness, SpeakerId)).VolumePercent, Is.EqualTo(25));
		Assert.That((await StateAsync(harness, LibraryId)).VolumePercent, Is.EqualTo(60), "the other player is untouched");
	}

	[Test]
	public async Task A_slider_writing_the_volume_variable_sets_the_library_volume()
	{
		await using var harness = await CreateAsync();

		var written = (await harness.Variables.SetAsync("volume",
			new VariableValueDto { Kind = "number", Number = 35 })).DataAs<VariableSetResult>();
		var volume = (await harness.Variables.GetAsync("volume")).DataAs<VariableReadingDto>();

		Assert.That(written!.Status, Is.EqualTo("Applied"));
		Assert.That(volume!.Value.Number, Is.EqualTo(35));
		Assert.That((await StateAsync(harness, LibraryId)).VolumePercent, Is.EqualTo(35));
	}

	[Test]
	public async Task A_read_only_variable_refuses_a_write()
	{
		await using var harness = await CreateAsync();

		var written = (await harness.Variables.SetAsync("track",
			new VariableValueDto { Kind = "text", Text = "Anything" })).DataAs<VariableSetResult>();

		Assert.That(written!.Status, Is.EqualTo("NotWritable"));
	}

	[Test]
	public async Task Item_options_follow_the_kind_that_is_already_selected()
	{
		await using var harness = await CreateAsync();

		var options = (await harness.Actions.GetOptionsAsync("play-catalog-item",
			"item",
			currentParameters: new Dictionary<string, object?> { ["kind"] = "Playlist" })).DataAs<DynamicOptionsResultDto>();

		Assert.That(options!.Options.Select(option => option.Value), Is.EquivalentTo(_playlistIds));
	}

	// A picker request is fire-and-forget and leaves no result to read, so what these two assert is the
	// half a caller can observe: the run is accepted rather than failed, and nothing was played or
	// transferred on a guess.
	[Test]
	public async Task Leaving_the_item_empty_asks_the_client_to_pick_one()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("play-catalog-item",
			new Dictionary<string, object?> { ["kind"] = "Track" },
			originClientId: "client-7");

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(outcome.DataAs<ActionExecuteResult>()!.Accepted, Is.True);
		Assert.That((await StateAsync(harness, LibraryId)).PlaybackState, Is.EqualTo("Paused"));
	}

	[Test]
	public async Task Leaving_the_device_empty_asks_the_client_to_pick_one()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("transfer-playback",
			new Dictionary<string, object?> { ["startPlayback"] = false },
			originClientId: "client-7");

		var devices = (await harness.MusicPlayer.GetDevicesAsync(Instance(LibraryId))).DataAs<MusicPlayerDevicesResult>();

		Assert.That(outcome.DataAs<ActionExecuteResult>()!.Accepted, Is.True);
		Assert.That(devices!.Devices.Single(device => device.IsActive).Id, Is.EqualTo("device-living-room"));
	}

	[Test]
	public async Task Transferring_to_an_unknown_device_fails_rather_than_doing_nothing_quietly()
	{
		await using var harness = await CreateAsync();

		var outcome = await harness.Actions.ExecuteAsync("transfer-playback",
			new Dictionary<string, object?> { ["device"] = "device-garden" });

		Assert.That(outcome.Succeeded, Is.False);
	}

	[Test]
	public async Task Event_options_offer_the_players_a_subscription_can_name()
	{
		await using var harness = await CreateAsync();

		var options = (await harness.Events.GetOptionsAsync(new EventOptionsArguments
		{
			EventId = "track-changed",
			ParameterName = "player"
		})).DataAs<DynamicOptionsResultDto>();

		Assert.That(options!.Options.Select(option => option.Value), Is.EquivalentTo(_instanceIds));
	}

	private static async Task<PluginTestHarness> CreateAsync()
	{
		var harness = PluginTestHarness.Create(builder => builder
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<MusicPlayerIntegration>());
		await harness.InitializeIntegrationsAsync();
		return harness;
	}

	private static MusicPlayerInstanceArguments Instance(string instanceId) => new() { InstanceId = instanceId };

	private static async Task<MusicPlayerStateDto> StateAsync(PluginTestHarness harness, string instanceId)
		=> (await harness.MusicPlayer.GetStateAsync(Instance(instanceId))).DataAs<MusicPlayerStateDto>()!;
}
```

## File: tests/MacroDeck.SampleMusicPlayerPlugin.Tests/MusicPlayerOverTheWireTests.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Protocol.Capabilities.MusicPlayer;
using MacroDeck.Plugin.Serilog;
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.SampleMusicPlayerPlugin.Tests;

/// <summary>
/// The music player over a real socket. State, catalogue items and artwork are the three shapes whose
/// serialization is worth proving - a <c>TimeSpan</c> position, an enum and a byte payload all change
/// form on the way across.
/// </summary>
[TestFixture]
public sealed class MusicPlayerOverTheWireTests
{
	[Test]
	public async Task Playback_state_survives_the_trip()
	{
		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.HostAsync(Builder());
		var session = await host.WaitForSessionAsync();

		await session.MusicPlayer.PlayAsync(new MusicPlayerInstanceArguments { InstanceId = "library" });
		var state = (await session.MusicPlayer.GetStateAsync(new MusicPlayerInstanceArguments { InstanceId = "library" }))
			.DataAs<MusicPlayerStateDto>();

		Assert.That(state!.PlaybackState, Is.EqualTo("Playing"));
		Assert.That(state.RepeatMode, Is.EqualTo("Off"));
		Assert.That(state.DurationSeconds, Is.GreaterThan(0));
	}

	[Test]
	public async Task The_catalog_and_its_artwork_survive_the_trip()
	{
		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.HostAsync(Builder());
		var session = await host.WaitForSessionAsync();

		var catalog = (await session.MusicPlayer.GetCatalogAsync(new MusicPlayerCatalogArguments
		{
			InstanceId = "library",
			Kind = "Track"
		})).DataAs<MusicPlayerCatalogResult>();

		var first = catalog!.Items[0];
		var artwork = (await session.MusicPlayer.GetArtworkAsync(new MusicPlayerArtworkArguments
		{
			InstanceId = "library",
			ArtworkId = first.ArtworkId!
		})).DataAs<MusicPlayerArtworkResult>();

		Assert.That(first.DurationSeconds, Is.GreaterThan(0));
		// Small artwork travels inline as base64 rather than through the asset pipeline.
		Assert.That(artwork!.Data, Is.Not.Null.And.Not.Empty);
	}

	[Test]
	public async Task Browsing_an_instance_without_a_catalog_is_refused_rather_than_answered_empty()
	{
		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.HostAsync(Builder());
		var session = await host.WaitForSessionAsync();

		var outcome = await session.MusicPlayer.GetCatalogAsync(new MusicPlayerCatalogArguments
		{
			InstanceId = "speaker",
			Kind = "Track"
		});

		// "Empty" has to mean genuinely empty for a catalogue, so an instance that cannot browse fails
		// instead of answering with no items.
		Assert.That(outcome.Succeeded, Is.False);
	}

	private static PluginHostBuilder Builder()
		=> MacroDeckPlugin.CreatePlugin()
			.UseMacroDeckLogging()
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<MusicPlayerIntegration>();
}
```
