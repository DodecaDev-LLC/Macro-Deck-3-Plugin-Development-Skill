# Sample: MacroDeck.SampleWeatherPlugin

The `MacroDeck.SampleWeatherPlugin` sample plugin and its tests, one `## File: <path>` section per file. See `samples/README.md` for what each sample demonstrates.

Files:

- `src/MacroDeck.SampleWeatherPlugin/Actions/RefreshWeatherAction.cs`
- `src/MacroDeck.SampleWeatherPlugin/Actions/SetAlertThresholdAction.cs`
- `src/MacroDeck.SampleWeatherPlugin/Actions/SetConditionAction.cs`
- `src/MacroDeck.SampleWeatherPlugin/Assets/icon.svg`
- `src/MacroDeck.SampleWeatherPlugin/ConfigFlow/LocationConfigFlow.cs`
- `src/MacroDeck.SampleWeatherPlugin/Localization/Strings.de.resx`
- `src/MacroDeck.SampleWeatherPlugin/Localization/Strings.resx`
- `src/MacroDeck.SampleWeatherPlugin/MacroDeck.SampleWeatherPlugin.csproj`
- `src/MacroDeck.SampleWeatherPlugin/Program.cs`
- `src/MacroDeck.SampleWeatherPlugin/Properties/launchSettings.json`
- `src/MacroDeck.SampleWeatherPlugin/README.md`
- `src/MacroDeck.SampleWeatherPlugin/Weather/SyntheticWeatherStation.cs`
- `src/MacroDeck.SampleWeatherPlugin/WeatherIntegration.cs`
- `src/MacroDeck.SampleWeatherPlugin/macrodeck-build.json`
- `src/MacroDeck.SampleWeatherPlugin/manifest.json`
- `tests/MacroDeck.SampleWeatherPlugin.Tests/LocalizationTests.cs`
- `tests/MacroDeck.SampleWeatherPlugin.Tests/MacroDeck.SampleWeatherPlugin.Tests.csproj`
- `tests/MacroDeck.SampleWeatherPlugin.Tests/WeatherIntegrationTests.cs`
- `tests/MacroDeck.SampleWeatherPlugin.Tests/WeatherOverTheWireTests.cs`
- `tests/MacroDeck.SampleWeatherPlugin.Tests/WeatherProcessTests.cs`

## File: src/MacroDeck.SampleWeatherPlugin/Actions/RefreshWeatherAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleWeatherPlugin.Actions;

/// <summary>
/// The plain action of the three: no parameters, no dynamic behavior. Advances the sample's
/// synthetic weather reading by one tick, which republishes the <c>weather-refreshed</c> event and
/// updates the temperature variable and the weather snapshot - the one button that ties every other
/// capability in this sample together.
/// </summary>
internal sealed class RefreshWeatherAction(WeatherIntegration integration) : IActionDefinition
{
	public string Id => "refresh-weather";

	public LocalizedText Name => Strings.Actions.RefreshWeather.Name();

	public LocalizedText Description => Strings.Actions.RefreshWeather.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } = [];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	private sealed class Executor(WeatherIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			integration.Station.Tick();
			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleWeatherPlugin/Actions/SetAlertThresholdAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleWeatherPlugin.Actions;

/// <summary>
/// Sets the temperature above which the next <c>weather-refreshed</c> event reports <c>isAlert</c>. A
/// Slider widget binds the writable <c>sample_alert_threshold_celsius</c> variable instead, which reads
/// the threshold back for two-way binding.
/// </summary>
internal sealed class SetAlertThresholdAction(WeatherIntegration integration) : IActionDefinition
{
	internal const double Min = -10;
	internal const double Max = 40;

	public string Id => "set-alert-threshold";

	public LocalizedText Name => Strings.Actions.SetAlertThreshold.Name();

	public LocalizedText Description => Strings.Actions.SetAlertThreshold.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Slider("thresholdCelsius",
			Min,
			Max,
			label: Strings.Actions.SetAlertThreshold.Threshold.Label(),
			step: 1,
			defaultValue: 30)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	private sealed class Executor(WeatherIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("thresholdCelsius") is not double threshold)
			{
				// Generic validation wording comes from Macro Deck's own catalog rather than from a key of
				// this plugin's, so a translator never re-translates a sentence the app already ships.
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.InvalidValue(Strings.Actions.SetAlertThreshold.Threshold.Label())));
			}

			integration.AlertThresholdCelsius = threshold;
			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleWeatherPlugin/Actions/SetConditionAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.Weather;

namespace MacroDeck.SampleWeatherPlugin.Actions;

/// <summary>
/// The dynamic-options action of the three: <see cref="Parameters"/> declares its one field with no
/// options attached, and <see cref="GetDynamicOptionsAsync"/> supplies them itself rather than through
/// a named options source - see <see cref="IDynamicOptionsActionDefinition"/>. Forces the condition
/// the next synthetic reading reports, so a demo deck can show every icon the Weather widget knows
/// without waiting on the sine wave to get there.
/// </summary>
internal sealed class SetConditionAction(WeatherIntegration integration) : IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "set-condition";

	public LocalizedText Name => Strings.Actions.SetCondition.Name();

	public LocalizedText Description => Strings.Actions.SetCondition.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("condition",
			label: Strings.Actions.SetCondition.Condition.Label(),
			required: true)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	/// <summary>An option's <c>Value</c> is the wire identity the executor parses back, so it stays the
	/// enum name; only its <c>Label</c> is localized.</summary>
	public Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
		=> Task.FromResult(new DynamicOptionsResult
		{
			Options =
			[
				.. WeatherIntegration.SelectableConditions
					.Select(condition => new ActionParameterOption
					{
						Value = condition.ToString(),
						Label = ConditionLabel(condition)
					})
			]
		});

	private static LocalizedText ConditionLabel(WeatherCondition condition) => condition switch
	{
		WeatherCondition.Clear => Strings.Conditions.Clear(),
		WeatherCondition.PartlyCloudy => Strings.Conditions.PartlyCloudy(),
		WeatherCondition.Overcast => Strings.Conditions.Overcast(),
		WeatherCondition.Rain => Strings.Conditions.Rain(),
		WeatherCondition.Thunderstorm => Strings.Conditions.Thunderstorm(),
		WeatherCondition.Snow => Strings.Conditions.Snow(),

		// Unreachable while SelectableConditions is the only caller, and deliberately not a throw: an
		// enum value added to that list without a resource should show its name, not break the picker.
		_ => condition.ToString()
	};

	private sealed class Executor(WeatherIntegration integration) : IActionExecutor
	{
		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("condition") is not string text ||
				!Enum.TryParse<WeatherCondition>(text, out var condition))
			{
				return Task.FromResult(ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.InvalidValue(Strings.Actions.SetCondition.Condition.Label())));
			}

			integration.Station.SetForcedCondition(condition);
			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.SampleWeatherPlugin/Assets/icon.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
	<circle cx="24" cy="23" r="12" fill="#F5A623" />
	<path d="M18 44h27a10 10 0 0 0 1-19.9A14 14 0 0 0 19 20.6 12 12 0 0 0 18 44z" fill="#4A90D9" />
</svg>
```

## File: src/MacroDeck.SampleWeatherPlugin/ConfigFlow/LocationConfigFlow.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.ConfigFlow;

namespace MacroDeck.SampleWeatherPlugin.ConfigFlow;

/// <summary>
/// A single-step flow collecting the location the station reports for - deliberately the contract's
/// minimum. See the REST API sample for a multi-step flow with secrets and an external step.
/// </summary>
internal sealed class LocationConfigFlow : IConfigFlow
{
	/// <summary>Also the config entry key <see cref="WeatherIntegration.InitializeAsync"/> reads back: a
	/// step's fields are persisted under their own names, with nothing to echo into
	/// <see cref="ConfigFlowResult.Complete"/>.</summary>
	internal const string LocationFieldName = "location";

	private const string StepId = "location";

	public Task<ConfigFlowResult> StartAsync(IConfigFlowContext context, CancellationToken cancellationToken)
		=> Task.FromResult(ConfigFlowResult.Step(BuildStep()));

	public Task<ConfigFlowResult> SubmitAsync(
		string stepId,
		IReadOnlyDictionary<string, object?> input,
		IConfigFlowContext context,
		CancellationToken cancellationToken)
	{
		if (!string.Equals(stepId, StepId, StringComparison.Ordinal))
		{
			return Task.FromResult(ConfigFlowResult.Error(BuildStep(), Strings.ConfigFlow.Location.UnknownStep()));
		}

		if (input.GetValueOrDefault(LocationFieldName) is not string { Length: > 0 } location)
		{
			var required = MacroDeckStrings.Validation.Required(Strings.ConfigFlow.Location.LocationName.Label());

			return Task.FromResult(ConfigFlowResult.Error(BuildStep(),
				required,
				new Dictionary<string, LocalizedText> { [LocationFieldName] = required }));
		}

		// Deliberately a plain string, not a LocalizedText: the host stores the entry title as its name
		// and the user renames it from there, so it is written once in the plugin's own language.
		return Task.FromResult(ConfigFlowResult.Complete($"Weather ({location})"));
	}

	private static ConfigFlowStep BuildStep() => new()
	{
		StepId = StepId,
		Title = Strings.ConfigFlow.Location.Title(),
		Description = Strings.ConfigFlow.Location.Description(),
		Fields =
		[
			ActionParameter.Text(LocationFieldName,
				label: Strings.ConfigFlow.Location.LocationName.Label(),
				defaultValue: "Berlin, Germany",
				required: true)
		]
	};
}
```

## File: src/MacroDeck.SampleWeatherPlugin/Localization/Strings.de.resx

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
  <data name="Actions.RefreshWeather.Name" xml:space="preserve">
    <value>Wetter aktualisieren</value>
  </data>
  <data name="Actions.RefreshWeather.Description" xml:space="preserve">
    <value>Berechnet den synthetischen Wetterwert des Beispiels neu und veröffentlicht ihn erneut.</value>
  </data>
  <data name="Actions.SetAlertThreshold.Name" xml:space="preserve">
    <value>Warnschwelle festlegen</value>
  </data>
  <data name="Actions.SetAlertThreshold.Description" xml:space="preserve">
    <value>Legt die Temperatur (°C) fest, ab der weather-refreshed-Ereignisse isAlert melden.</value>
  </data>
  <data name="Actions.SetAlertThreshold.Threshold.Label" xml:space="preserve">
    <value>Warnschwelle (°C)</value>
  </data>
  <data name="Actions.SetCondition.Name" xml:space="preserve">
    <value>Wetterlage erzwingen</value>
  </data>
  <data name="Actions.SetCondition.Description" xml:space="preserve">
    <value>Überschreibt die Wetterlage, die der nächste synthetische Messwert meldet.</value>
  </data>
  <data name="Actions.SetCondition.Condition.Label" xml:space="preserve">
    <value>Wetterlage</value>
  </data>
  <data name="Conditions.Clear" xml:space="preserve">
    <value>Klar</value>
  </data>
  <data name="Conditions.PartlyCloudy" xml:space="preserve">
    <value>Teilweise bewölkt</value>
  </data>
  <data name="Conditions.Overcast" xml:space="preserve">
    <value>Bedeckt</value>
  </data>
  <data name="Conditions.Rain" xml:space="preserve">
    <value>Regen</value>
  </data>
  <data name="Conditions.Thunderstorm" xml:space="preserve">
    <value>Gewitter</value>
  </data>
  <data name="Conditions.Snow" xml:space="preserve">
    <value>Schnee</value>
  </data>
  <data name="Events.WeatherRefreshed.Name" xml:space="preserve">
    <value>Wetter aktualisiert</value>
  </data>
  <data name="Events.WeatherRefreshed.Description" xml:space="preserve">
    <value>Wird ausgelöst, sobald sich der synthetische Wetterwert des Beispiels ändert.</value>
  </data>
  <data name="Events.WeatherRefreshed.Temperature.Label" xml:space="preserve">
    <value>Temperatur (°C)</value>
  </data>
  <data name="Events.WeatherRefreshed.Condition.Label" xml:space="preserve">
    <value>Wetterlage</value>
  </data>
  <data name="Events.WeatherRefreshed.IsAlert.Label" xml:space="preserve">
    <value>Über der Warnschwelle</value>
  </data>
  <data name="ConfigFlow.Location.Title" xml:space="preserve">
    <value>Beispielort</value>
  </data>
  <data name="ConfigFlow.Location.Description" xml:space="preserve">
    <value>Wähle den Ort, für den die synthetische Wetterstation des Beispiels meldet.</value>
  </data>
  <data name="ConfigFlow.Location.LocationName.Label" xml:space="preserve">
    <value>Ortsname</value>
  </data>
  <data name="ConfigFlow.Location.UnknownStep" xml:space="preserve">
    <value>Unbekannter Schritt.</value>
  </data>
</root>
```

## File: src/MacroDeck.SampleWeatherPlugin/Localization/Strings.resx

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
  <data name="Actions.RefreshWeather.Name" xml:space="preserve">
    <value>Refresh weather</value>
  </data>
  <data name="Actions.RefreshWeather.Description" xml:space="preserve">
    <value>Advances the sample's synthetic weather reading and republishes it.</value>
  </data>
  <data name="Actions.SetAlertThreshold.Name" xml:space="preserve">
    <value>Set alert threshold</value>
  </data>
  <data name="Actions.SetAlertThreshold.Description" xml:space="preserve">
    <value>Sets the temperature (°C) above which weather-refreshed events report isAlert.</value>
  </data>
  <data name="Actions.SetAlertThreshold.Threshold.Label" xml:space="preserve">
    <value>Alert threshold (°C)</value>
  </data>
  <data name="Actions.SetCondition.Name" xml:space="preserve">
    <value>Force weather condition</value>
  </data>
  <data name="Actions.SetCondition.Description" xml:space="preserve">
    <value>Overrides the condition the next synthetic reading reports.</value>
  </data>
  <data name="Actions.SetCondition.Condition.Label" xml:space="preserve">
    <value>Condition</value>
  </data>
  <data name="Conditions.Clear" xml:space="preserve">
    <value>Clear</value>
  </data>
  <data name="Conditions.PartlyCloudy" xml:space="preserve">
    <value>Partly cloudy</value>
  </data>
  <data name="Conditions.Overcast" xml:space="preserve">
    <value>Overcast</value>
  </data>
  <data name="Conditions.Rain" xml:space="preserve">
    <value>Rain</value>
  </data>
  <data name="Conditions.Thunderstorm" xml:space="preserve">
    <value>Thunderstorm</value>
  </data>
  <data name="Conditions.Snow" xml:space="preserve">
    <value>Snow</value>
  </data>
  <data name="Events.WeatherRefreshed.Name" xml:space="preserve">
    <value>Weather refreshed</value>
  </data>
  <data name="Events.WeatherRefreshed.Description" xml:space="preserve">
    <value>Raised whenever the sample's synthetic weather reading changes.</value>
  </data>
  <data name="Events.WeatherRefreshed.Temperature.Label" xml:space="preserve">
    <value>Temperature (°C)</value>
  </data>
  <data name="Events.WeatherRefreshed.Condition.Label" xml:space="preserve">
    <value>Condition</value>
  </data>
  <data name="Events.WeatherRefreshed.IsAlert.Label" xml:space="preserve">
    <value>Above alert threshold</value>
  </data>
  <data name="ConfigFlow.Location.Title" xml:space="preserve">
    <value>Sample location</value>
  </data>
  <data name="ConfigFlow.Location.Description" xml:space="preserve">
    <value>Pick the location the sample's synthetic weather station reports for.</value>
  </data>
  <data name="ConfigFlow.Location.LocationName.Label" xml:space="preserve">
    <value>Location name</value>
  </data>
  <data name="ConfigFlow.Location.UnknownStep" xml:space="preserve">
    <value>Unknown step.</value>
  </data>
</root>
```

## File: src/MacroDeck.SampleWeatherPlugin/MacroDeck.SampleWeatherPlugin.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <IsPackable>false</IsPackable>
        <UserSecretsId>MacroDeck.SampleWeatherPlugin-PluginDevelopment</UserSecretsId>
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

## File: src/MacroDeck.SampleWeatherPlugin/Program.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Serilog;
using MacroDeck.SampleWeatherPlugin;

// Identity, description and icon are not set here: they come from manifest.json at the content root.
// Strings is generated from Localization/*.resx, so UseLocalization is what makes every LocalizedText
// this plugin hands the host resolve in the reader's language rather than falling back to its key.
var plugin = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<WeatherIntegration>()
	.Build();

await plugin.RunAsync();
```

## File: src/MacroDeck.SampleWeatherPlugin/Properties/launchSettings.json

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

## File: src/MacroDeck.SampleWeatherPlugin/README.md

````markdown
# Sample Weather plugin

The smallest complete plugin: one integration covering actions, variables, an event, a config flow and
a provider capability, with everything reading the same synthetic weather reading. Start here if you
have not written a Macro Deck plugin before, then read
[hosting guide](https://docs.macro-deck.app/sdk/hosting/)
for the builder API and the registration modes this assumes.

It needs no external service: the station computes its reading from a running counter, so the plugin
builds, runs and tests without credentials or network access.

## Read these first

- **`WeatherIntegration.cs`** - the integration: `IPluginIntegration` plus `IVariableProvider`,
  `IEventProvider`, `IConfigFlowProvider` and `IWeatherProvider`. It holds the two pieces of state
  everything else reads, and `InitializeAsync` is where a plugin's config-flow story completes - the
  configured location is read back out of `IIntegrationContext.Config` there, not in the flow.
- **`Weather/SyntheticWeatherStation.cs`** - the provider capability. `GetSnapshotAsync` hands back a
  cached reading rather than fetching one, which is the shape `IWeatherStation` asks for.
- **`Actions/RefreshWeatherAction.cs`** - the plain action, and the one button that makes everything
  else in the sample visibly move.
- **`Actions/SetAlertThresholdAction.cs`** - sets the alert threshold from a button. A Slider widget
  binds the writable `sample_alert_threshold_celsius` variable instead (`Write` on its
  `VariableDefinition`, applied in `SetValueAsync`), so it shows the threshold that is actually set.
- **`Actions/SetConditionAction.cs`** - the dynamic-options action: its field has no static options and
  `GetDynamicOptionsAsync` supplies them.
- **`ConfigFlow/LocationConfigFlow.cs`** - deliberately the contract's floor: one step, one required
  field. See the REST API sample for a multi-step flow with secrets and OAuth.
- **`Assets/icon.svg`** - declared by `manifest.json`; the plugin's own code never touches it.
- **`Localization/Strings.resx`** and **`Localization/Strings.de.resx`** - every string a user reads.
  This is the one sample that ships a translation, so it is also where the fallback chain and the
  manifest's derived `languages` field are visible.

## Running it against a local host

Use this project's **Macro Deck - Real Host** launch profile as described in the repository's
[run and debug guide](../../README.md#run-and-debug-against-macro-deck). It then shows up as "Sample
Weather" with three actions, a config flow, a weather station and three variables. Configure a location,
add the station to a Weather widget, and press "Refresh weather" to watch the location, the temperature
and the event move together.

Self-registering mode only works against a host on the same machine - plugin endpoints are local-only
by design.

## Testing it

[`tests/MacroDeck.SampleWeatherPlugin.Tests`](../../tests/MacroDeck.SampleWeatherPlugin.Tests) uses all
three levels of `MacroDeck.Plugin.Testing`: `PluginTestHarness` for behaviour, `MacroDeckTestHost` for
the wire, and one `LaunchAsync` test that starts the built executable as a real process.

```bash
dotnet test tests/MacroDeck.SampleWeatherPlugin.Tests
```

```bash
macrodeck-plugin test --project src/MacroDeck.SampleWeatherPlugin
```

## Packaging it

`macrodeck-build.json` names one self-contained `dotnet publish` per platform, and the manifest's
entrypoints name what that publish actually produces:

```bash
macrodeck-plugin build --output ./artifacts
```

```bash
macrodeck-plugin validate --artifact ./artifacts/app.macro-deck.sample-weather-1.0.0.macroDeckPlugin --level Publication
```
````

## File: src/MacroDeck.SampleWeatherPlugin/Weather/SyntheticWeatherStation.cs

```csharp
using MacroDeck.Sdk.Weather;

namespace MacroDeck.SampleWeatherPlugin.Weather;

/// <summary>
/// The sample's single station. <see cref="Tick"/> computes a plausible reading and caches it;
/// <see cref="GetSnapshotAsync"/> hands the cached value back, which is the shape
/// <see cref="IWeatherStation"/> asks for - a widget reading the station never waits on I/O.
/// </summary>
internal sealed class SyntheticWeatherStation(WeatherIntegration integration) : IWeatherStation
{
	private int _tickCount;
	private WeatherCondition? _forcedCondition;

	/// <summary>The most recent reading, exposed synchronously so the temperature variable echoes exactly
	/// what <see cref="GetSnapshotAsync"/> serves.</summary>
	internal WeatherSnapshot LastSnapshot { get; private set; } = WeatherSnapshot.Unavailable();

	public Task<WeatherSnapshot> GetSnapshotAsync(CancellationToken ct) => Task.FromResult(LastSnapshot);

	/// <summary>Overrides the condition the next <see cref="Tick"/> reports.</summary>
	internal void SetForcedCondition(WeatherCondition condition) => _forcedCondition = condition;

	/// <summary>
	/// Advances the reading by one step, caches it and republishes the <c>weather-refreshed</c> event.
	/// A real provider would poll its API on its own interval and cache the result here instead.
	/// </summary>
	internal void Tick()
	{
		_tickCount++;

		// A sine wave rather than randomness, so a demo deck shows a believable rise and fall and the
		// sample's own tests get a deterministic reading.
		var temperature = Math.Round(15 + 6 * Math.Sin(_tickCount * 0.5), 1);
		var condition = _forcedCondition ?? (temperature switch
		{
			< 0 => WeatherCondition.Snow,
			< 12 => WeatherCondition.Overcast,
			< 20 => WeatherCondition.PartlyCloudy,
			_ => WeatherCondition.Clear
		});

		var today = DateOnly.FromDateTime(DateTime.UtcNow);
		LastSnapshot = new WeatherSnapshot
		{
			IsAvailable = true,
			LocationName = integration.LocationName,
			Temperature = temperature,
			ApparentTemperature = temperature - 1,
			Condition = condition,
			IsDay = DateTimeOffset.UtcNow.Hour is >= 6 and < 20,
			Unit = TemperatureUnit.Celsius,
			Days = [new WeatherForecastDay(today, condition, temperature - 4, temperature + 4)]
		};

		integration.PublishWeatherRefreshed(LastSnapshot, isAlert: temperature >= integration.AlertThresholdCelsius);
	}
}
```

## File: src/MacroDeck.SampleWeatherPlugin/WeatherIntegration.cs

```csharp
using System.Globalization;
using MacroDeck.Plugin.Hosting.Integrations;
using MacroDeck.Plugin.Hosting.Integrations.HostApis;
using MacroDeck.Plugin.Protocol.Handshake;
using MacroDeck.SampleWeatherPlugin.Actions;
using MacroDeck.SampleWeatherPlugin.ConfigFlow;
using MacroDeck.SampleWeatherPlugin.Weather;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.ConfigFlow;
using MacroDeck.Sdk.Events;
using MacroDeck.Sdk.Variables;
using MacroDeck.Sdk.Weather;
using Serilog;

namespace MacroDeck.SampleWeatherPlugin;

/// <summary>
/// One integration wiring actions, variables, an event, a config flow and a weather provider to the
/// same synthetic reading, so the pieces demonstrate how they fit together rather than standing alone.
/// </summary>
public sealed class WeatherIntegration : IPluginIntegration, IVariableProvider, IEventProvider,
	IConfigFlowProvider, IWeatherProvider
{
	internal const string StationId = "primary";

	internal const string WeatherRefreshedEventId = "weather-refreshed";

	/// <summary>The conditions the "force weather condition" action offers, curated down from every
	/// <see cref="WeatherCondition"/> value so the picker stays short.</summary>
	internal static readonly IReadOnlyList<WeatherCondition> SelectableConditions =
	[
		WeatherCondition.Clear, WeatherCondition.PartlyCloudy, WeatherCondition.Overcast,
		WeatherCondition.Rain, WeatherCondition.Thunderstorm, WeatherCondition.Snow
	];

	private readonly IPluginCatalogNotifier _catalogNotifier;
	private readonly ILogger _logger;

	private IIntegrationContext? _context;

	// Constructor injection: the integration is registered through RegisterIntegration<T>() (Program.cs)
	// and built by DI, so anything the container knows can be taken here.
	public WeatherIntegration(IPluginCatalogNotifier catalogNotifier, ILogger logger)
	{
		_catalogNotifier = catalogNotifier;
		_logger = logger.ForContext<WeatherIntegration>();
		Station = new SyntheticWeatherStation(this);
		Actions = [new RefreshWeatherAction(this), new SetAlertThresholdAction(this), new SetConditionAction(this)];
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

	/// <summary>The configured location, reported by both the weather snapshot and the location variable.</summary>
	internal string LocationName { get; private set; } = "Berlin, Germany";

	/// <summary>The temperature above which a refresh reports an alert, set by the slider action.</summary>
	internal double AlertThresholdCelsius { get; set; } = 30;

	internal SyntheticWeatherStation Station { get; }

	public async Task InitializeAsync(IIntegrationContext context)
	{
		_context = context;

		// Where a plugin's config-flow story completes: the flow persisted the location, this reads it back.
		var entries = await context.Config.GetEntriesAsync();
		if (entries.Count > 0)
		{
			var stored = await context.Config.GetStringAsync(entries[0].Id, LocationConfigFlow.LocationFieldName);
			if (!string.IsNullOrWhiteSpace(stored))
			{
				LocationName = stored;
			}
		}

		Station.Tick();

		_logger.Information("Initialized with location {Location} and alert threshold {ThresholdCelsius}°C.",
			LocationName,
			AlertThresholdCelsius);

		// The host describes capabilities concurrently with this method, so a first describe can capture
		// the default location before the config read above finished. Telling the host both catalogues
		// are stale is what makes the widget, the variable and the config card agree.
		_catalogNotifier.CatalogChanged(CapabilityKinds.Weather, reason: "location config applied");
		_catalogNotifier.CatalogChanged(CapabilityKinds.Variables, reason: "location config applied");
	}

	public Task ShutdownAsync()
	{
		_context = null;
		return Task.CompletedTask;
	}

	public IReadOnlyList<VariableDefinition> Variables { get; } =
	[
		VariableDefinition.Eager("sample_location", VariableType.Text) with { Id = "location" },
		VariableDefinition.Eager("sample_temperature_celsius", VariableType.Numeric, decimalPlaces: 1)
			with { Id = "temperature-celsius", Unit = "°C" },
		// Writable, so a Slider widget bound to it sets the threshold and reads the real one back.
		VariableDefinition.Eager("sample_alert_threshold_celsius", VariableType.Numeric)
			with { Id = "alert-threshold-celsius", Unit = "°C", Write = new VariableWriteCapability() }
	];

	public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
		=> ValueTask.FromResult(localId switch
		{
			"location" => VariableReading.Of(LocationName),
			"temperature-celsius" => VariableReading.Of(Station.LastSnapshot.Temperature),
			"alert-threshold-celsius" => VariableReading.Of(AlertThresholdCelsius, SetAlertThresholdAction.Min,
				SetAlertThresholdAction.Max, 1),
			_ => VariableReading.Unavailable
		});

	/// <summary>Only called for the threshold, the one variable declaring a write.</summary>
	public ValueTask<VariableWriteResult> SetValueAsync(string localId, object? value, CancellationToken cancellationToken = default)
	{
		if (value is not (double or int or long))
		{
			return ValueTask.FromResult(VariableWriteResult.InvalidValue());
		}

		AlertThresholdCelsius = Math.Clamp(Convert.ToDouble(value, CultureInfo.InvariantCulture), SetAlertThresholdAction.Min, SetAlertThresholdAction.Max);
		return ValueTask.FromResult(VariableWriteResult.Applied());
	}

	// ProviderName is deliberately not implemented: the host falls back to the manifest name, so the one
	// place this plugin states its name stays manifest.json.
	public IReadOnlyList<EventDefinition> EventDefinitions { get; } =
	[
		new EventDefinition
		{
			Id = WeatherRefreshedEventId,
			Name = Strings.Events.WeatherRefreshed.Name(),
			Description = Strings.Events.WeatherRefreshed.Description(),
			PayloadParameters =
			[
				ActionParameter.Number("temperatureCelsius", Strings.Events.WeatherRefreshed.Temperature.Label()),
				ActionParameter.Text("condition", Strings.Events.WeatherRefreshed.Condition.Label()),
				ActionParameter.Toggle("isAlert", Strings.Events.WeatherRefreshed.IsAlert.Label())
			]
		}
	];

	/// <summary>Publishing is fire-and-forget by contract, so this never throws. The context is only null
	/// before <see cref="InitializeAsync"/> or after <see cref="ShutdownAsync"/>.</summary>
	internal void PublishWeatherRefreshed(WeatherSnapshot snapshot, bool isAlert)
		=> _context?.Events.Publish(WeatherRefreshedEventId, new Dictionary<string, object?>
		{
			["temperatureCelsius"] = snapshot.Temperature,
			["condition"] = snapshot.Condition.ToString(),
			["isAlert"] = isAlert
		});

	public IConfigFlow CreateConfigFlow() => new LocationConfigFlow();

	public bool AllowsMultipleConfigurations => false;

	public IReadOnlyList<WeatherStationInstance> GetInstances() => [new WeatherStationInstance(StationId, LocationName)];

	public IWeatherStation? GetStation(string instanceId)
		=> string.Equals(instanceId, StationId, StringComparison.Ordinal) ? Station : null;
}
```

## File: src/MacroDeck.SampleWeatherPlugin/macrodeck-build.json

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleWeatherPlugin.csproj",
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
        "MacroDeck.SampleWeatherPlugin.csproj",
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
        "MacroDeck.SampleWeatherPlugin.csproj",
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
        "MacroDeck.SampleWeatherPlugin.csproj",
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

## File: src/MacroDeck.SampleWeatherPlugin/manifest.json

```json
{
  "$schema": "https://schemas.macro-deck.app/plugin-manifest-v1.schema.json",
  "manifestVersion": 1,
  "id": "app.macro-deck.sample-weather",
  "name": "Sample Weather",
  "version": "1.0.0",
  "description": "Synthetic weather plugin: plain and dynamic-options actions, writable variables, an event, a config flow and a weather provider on one shared reading.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": {
      "executable": "runtimes/win-x64/MacroDeck.SampleWeatherPlugin.exe"
    },
    "osx-arm64": {
      "executable": "runtimes/osx-arm64/MacroDeck.SampleWeatherPlugin"
    },
    "osx-x64": {
      "executable": "runtimes/osx-x64/MacroDeck.SampleWeatherPlugin"
    },
    "linux-x64": {
      "executable": "runtimes/linux-x64/MacroDeck.SampleWeatherPlugin"
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
    "host:config",
    "host:variables",
    "events:publish"
  ]
}
```

## File: tests/MacroDeck.SampleWeatherPlugin.Tests/LocalizationTests.cs

```csharp
using NUnit.Framework;

namespace MacroDeck.SampleWeatherPlugin.Tests;

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
		Assert.That(Strings.LocalizationCatalog.Scope, Is.EqualTo("plugin:app.macro-deck.sample-weather"));
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
		Assert.That(Strings.LocalizationCatalog.KeysOf("en"), Does.Contain("Actions.RefreshWeather.Name"));
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

## File: tests/MacroDeck.SampleWeatherPlugin.Tests/MacroDeck.SampleWeatherPlugin.Tests.csproj

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
        <ProjectReference Include="..\..\src\MacroDeck.SampleWeatherPlugin\MacroDeck.SampleWeatherPlugin.csproj" />
    </ItemGroup>

</Project>
```

## File: tests/MacroDeck.SampleWeatherPlugin.Tests/WeatherIntegrationTests.cs

```csharp
using System.Text.Json;
using MacroDeck.Plugin.Protocol.Capabilities.Actions;
using MacroDeck.Plugin.Protocol.Capabilities.Variables;
using MacroDeck.Plugin.Protocol.Capabilities.Weather;
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.SampleWeatherPlugin.Tests;

/// <summary>
/// Behaviour tests through <see cref="PluginTestHarness"/>: the plugin's own capability handlers run,
/// but nothing crosses a socket. This is where a plugin author tests what their integration does.
/// </summary>
[TestFixture]
public sealed class WeatherIntegrationTests
{
	private const string StationInstanceId = "primary";

	[Test]
	public async Task The_configured_location_is_what_the_station_and_the_variable_report()
	{
		await using var harness = CreateHarness();

		var entryId = harness.Context.Config.AddEntry("Sample");
		harness.Context.Config.SeedString(entryId, "location", "Reykjavík, Iceland");

		await harness.InitializeIntegrationsAsync();

		var instances = (await harness.Weather.GetInstancesAsync()).DataAs<WeatherInstancesResult>();
		var location = (await harness.Variables.GetAsync("location")).DataAs<VariableReadingDto>();

		Assert.That(instances!.Instances.Single().DisplayName, Is.EqualTo("Reykjavík, Iceland"));
		Assert.That(location!.Value.Text, Is.EqualTo("Reykjavík, Iceland"));
	}

	[Test]
	public async Task An_unconfigured_plugin_still_reports_a_reading()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var snapshot = await SnapshotAsync(harness);

		Assert.That(snapshot.IsAvailable, Is.True);
		Assert.That(snapshot.Temperature, Is.Not.Null);
	}

	[Test]
	public async Task Refreshing_changes_the_reading_and_publishes_it()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var before = await SnapshotAsync(harness);
		var outcome = await harness.Actions.ExecuteAsync("refresh-weather");
		var after = await SnapshotAsync(harness);

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(after.Temperature, Is.Not.EqualTo(before.Temperature));

		var published = harness.Context.Events.Published[^1];
		Assert.That(published.EventId, Is.EqualTo("weather-refreshed"));
		Assert.That(Payload(published.Parameters).GetProperty("temperatureCelsius").GetDouble(), Is.EqualTo(after.Temperature));
		Assert.That(Payload(published.Parameters).GetProperty("condition").GetString(), Is.EqualTo(after.Condition));
	}

	[Test]
	public async Task The_temperature_variable_agrees_with_the_station()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		await harness.Actions.ExecuteAsync("refresh-weather");

		var snapshot = await SnapshotAsync(harness);
		var temperature = (await harness.Variables.GetAsync("temperature-celsius")).DataAs<VariableReadingDto>();

		Assert.That(temperature!.Value.Number, Is.EqualTo(snapshot.Temperature));
	}

	[Test]
	public async Task The_threshold_variable_reads_back_what_the_action_set()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		await harness.Actions.ExecuteAsync("set-alert-threshold",
			new Dictionary<string, object?> { ["thresholdCelsius"] = 12.0 });

		var threshold = (await harness.Variables.GetAsync("alert-threshold-celsius")).DataAs<VariableReadingDto>();

		Assert.That(threshold!.Value.Number, Is.EqualTo(12));
	}

	[Test]
	public async Task A_slider_writing_the_threshold_variable_is_clamped_to_the_range()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var written = (await harness.Variables.SetAsync("alert-threshold-celsius",
			new VariableValueDto { Kind = "number", Number = 99 })).DataAs<VariableSetResult>();
		var threshold = (await harness.Variables.GetAsync("alert-threshold-celsius")).DataAs<VariableReadingDto>();

		Assert.That(written!.Status, Is.EqualTo("Applied"));
		Assert.That(threshold!.Value.Number, Is.EqualTo(40));
	}

	[Test]
	public async Task A_threshold_that_is_not_a_number_fails_rather_than_being_ignored()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var outcome = await harness.Actions.ExecuteAsync("set-alert-threshold",
			new Dictionary<string, object?> { ["thresholdCelsius"] = "warm" });

		Assert.That(outcome.Succeeded, Is.False);
	}

	[Test]
	public async Task The_alert_flag_follows_the_configured_threshold()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		// Below every reading the synthetic station can produce, so the next refresh has to report an alert.
		await harness.Actions.ExecuteAsync("set-alert-threshold",
			new Dictionary<string, object?> { ["thresholdCelsius"] = -50.0 });
		await harness.Actions.ExecuteAsync("refresh-weather");

		var payload = Payload(harness.Context.Events.Published[^1].Parameters);
		Assert.That(payload.GetProperty("isAlert").GetBoolean(), Is.True);
	}

	[Test]
	public async Task A_forced_condition_is_what_the_next_reading_reports()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var options = (await harness.Actions.GetOptionsAsync("set-condition", "condition")).DataAs<DynamicOptionsResultDto>();
		Assert.That(options!.Options.Select(option => option.Value), Does.Contain("Rain"));

		await harness.Actions.ExecuteAsync("set-condition", new Dictionary<string, object?> { ["condition"] = "Rain" });
		await harness.Actions.ExecuteAsync("refresh-weather");

		Assert.That((await SnapshotAsync(harness)).Condition, Is.EqualTo("Rain"));
	}

	[Test]
	public async Task An_unknown_condition_fails_rather_than_forcing_something_else()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var outcome = await harness.Actions.ExecuteAsync("set-condition",
			new Dictionary<string, object?> { ["condition"] = "Sandstorm" });

		Assert.That(outcome.Succeeded, Is.False);
	}

	[Test]
	public async Task An_instance_the_provider_never_declared_has_no_station()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var outcome = await harness.Weather.GetSnapshotAsync(new WeatherInstanceArguments { InstanceId = "second-station" });

		// The plugin says "no such station"; it is the host's adapter that turns that into an
		// unavailable snapshot rather than an error reaching a widget.
		Assert.That(outcome.Succeeded, Is.False);
		Assert.That(outcome.Error!.Code, Is.EqualTo("CAPABILITY_UNAVAILABLE"));
	}

	/// <summary>UseLocalization registers the catalog generated from Localization/*.resx. Without it the
	/// plugin still runs, but every LocalizedText it produces resolves to its bare key.</summary>
	private static PluginTestHarness CreateHarness() =>
		PluginTestHarness.Create(builder => builder
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<WeatherIntegration>());

	private static JsonElement Payload(JsonElement? parameters) => parameters!.Value;

	private static async Task<WeatherSnapshotDto> SnapshotAsync(PluginTestHarness harness)
	{
		var outcome = await harness.Weather.GetSnapshotAsync(new WeatherInstanceArguments { InstanceId = StationInstanceId });
		return outcome.DataAs<WeatherSnapshotDto>()!;
	}
}
```

## File: tests/MacroDeck.SampleWeatherPlugin.Tests/WeatherOverTheWireTests.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Protocol.Capabilities.Actions;
using MacroDeck.Plugin.Protocol.Capabilities.Weather;
using MacroDeck.Plugin.Serilog;
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.SampleWeatherPlugin.Tests;

/// <summary>
/// The same plugin over a real WebSocket against a real host implementation. What is under test here
/// is not the integration's logic - the harness tests cover that - but that it survives the trip:
/// registration, serialization and the event batches.
/// </summary>
[TestFixture]
public sealed class WeatherOverTheWireTests
{
	private static readonly string[] _expectedActionIds = ["refresh-weather", "set-alert-threshold", "set-condition"];

	[Test]
	public async Task The_plugin_registers_its_actions_and_serves_a_snapshot()
	{
		var builder = MacroDeckPlugin.CreatePlugin()
			.UseMacroDeckLogging()
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<WeatherIntegration>();

		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.HostAsync(builder);
		var session = await host.WaitForSessionAsync();

		var actions = (await session.Actions.DescribeAsync()).DataAs<ActionCatalogPayload>();
		Assert.That(actions!.Actions.Select(action => action.LocalId), Is.EquivalentTo(_expectedActionIds));

		var snapshot = (await session.Weather.GetSnapshotAsync(new WeatherInstanceArguments { InstanceId = "primary" }))
			.DataAs<WeatherSnapshotDto>();
		Assert.That(snapshot!.IsAvailable, Is.True);
	}

	[Test]
	public async Task Refreshing_reaches_the_host_as_a_published_event()
	{
		var builder = MacroDeckPlugin.CreatePlugin()
			.UseMacroDeckLogging()
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<WeatherIntegration>();

		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.HostAsync(builder);
		var session = await host.WaitForSessionAsync();

		var outcome = await session.Actions.ExecuteAsync("refresh-weather");
		Assert.That(outcome.Succeeded, Is.True);

		// Publishing crosses the socket asynchronously, so this is awaited rather than read.
		await host.Events.WaitForAsync("weather-refreshed", TimeSpan.FromSeconds(5));
	}
}
```

## File: tests/MacroDeck.SampleWeatherPlugin.Tests/WeatherProcessTests.cs

```csharp
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.SampleWeatherPlugin.Tests;

/// <summary>
/// The end-to-end level: a real child process, launched the way the supervisor launches an installed
/// plugin. Worth one test rather than a suite - what it proves is that the built artifact starts,
/// registers and shuts down cleanly, which no in-process subject can show.
/// </summary>
[TestFixture]
public sealed class WeatherProcessTests
{
	[Test]
	public async Task The_built_plugin_starts_registers_and_stops_cleanly()
	{
		// The plugin project is a ProjectReference, so its executable and its manifest.json sit next to
		// the test assembly - the content root the SDK reads its identity from.
		var executable = Path.Combine(AppContext.BaseDirectory,
			OperatingSystem.IsWindows() ? "MacroDeck.SampleWeatherPlugin.exe" : "MacroDeck.SampleWeatherPlugin");

		await using var host = await MacroDeckTestHost.StartAsync();
		await using var plugin = await host.LaunchAsync(PluginLaunchSpec.ForExecutable(executable));

		var session = await host.WaitForSessionAsync(TimeSpan.FromSeconds(30));
		var outcome = await session.Actions.ExecuteAsync("refresh-weather");
		Assert.That(outcome.Succeeded, Is.True);

		var report = await plugin.StopGracefullyAsync(TimeSpan.FromSeconds(10));
		Assert.That(report.ExitedWithinGrace, Is.True);
		Assert.That(report.Killed, Is.False);
	}
}
```
