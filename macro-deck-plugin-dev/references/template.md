# Plugin template

The official Macro Deck 3 plugin template (what `macrodeck-plugin new` / `dotnet new macrodeck-plugin` generates), one `## File: <path>` section per file. To write a project by hand, recreate these files and rename `MacroDeck.PluginTemplate` everywhere (project, namespace, `AssemblyName`, manifest entrypoints). The template's agent rulebook is in `references/agent-rules.md`.

Files:

- `src/MacroDeck.PluginTemplate/Assets/icon.svg`
- `src/MacroDeck.PluginTemplate/Localization/Strings.resx`
- `src/MacroDeck.PluginTemplate/LogMessageAction.cs`
- `src/MacroDeck.PluginTemplate/MacroDeck.PluginTemplate.csproj`
- `src/MacroDeck.PluginTemplate/PluginIntegration.cs`
- `src/MacroDeck.PluginTemplate/Program.cs`
- `src/MacroDeck.PluginTemplate/Properties/launchSettings.json`
- `src/MacroDeck.PluginTemplate/macrodeck-build.json`
- `src/MacroDeck.PluginTemplate/manifest.json`
- `tests/MacroDeck.PluginTemplate.Tests/MacroDeck.PluginTemplate.Tests.csproj`
- `tests/MacroDeck.PluginTemplate.Tests/PluginIntegrationTests.cs`
- `Directory.Build.props`
- `Directory.Packages.props`
- `NuGet.config`
- `.gitignore`
- `README.md`

## File: src/MacroDeck.PluginTemplate/Assets/icon.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
	<circle cx="24" cy="23" r="12" fill="#F5A623" />
	<path d="M18 44h27a10 10 0 0 0 1-19.9A14 14 0 0 0 19 20.6 12 12 0 0 0 18 44z" fill="#4A90D9" />
</svg>
```

## File: src/MacroDeck.PluginTemplate/Localization/Strings.resx

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <!-- The default-language file. Every translation is checked against it and the fallback chain ends
       here, so it is required even for a plugin that ships one language. Add a language by adding
       Localization/Strings.<culture>.resx beside it (Strings.de.resx, Strings.pt-BR.resx).
       A dotted key becomes a nested class: Actions.LogMessage.Name is Strings.Actions.LogMessage.Name(). -->
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
  <data name="Actions.LogMessage.Name" xml:space="preserve">
    <value>Write log message</value>
  </data>
  <data name="Actions.LogMessage.Description" xml:space="preserve">
    <value>Writes a message to the Macro Deck log.</value>
  </data>
  <data name="Actions.LogMessage.Message.Label" xml:space="preserve">
    <value>Message</value>
  </data>
  <data name="Actions.LogMessage.Message.Description" xml:space="preserve">
    <value>The text to write to the log.</value>
  </data>
  <data name="Actions.LogMessage.Message.Placeholder" xml:space="preserve">
    <value>Hello from my plugin</value>
  </data>
</root>
```

## File: src/MacroDeck.PluginTemplate/LogMessageAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using Serilog;

namespace MacroDeck.PluginTemplate;

/// <summary>
/// The one example action. Every string a user reads - the action's name and description, its
/// parameter's label, description and placeholder, and the error it can fail with - comes from
/// <see cref="Strings"/> rather than a literal, which is what makes the plugin translatable.
/// </summary>
public sealed class LogMessageAction : IActionDefinition
{
	private const string MessageParameter = "message";

	private readonly ILogger _logger;

	public LogMessageAction(ILogger logger) => _logger = logger.ForContext<LogMessageAction>();

	public string Id => "log-message";

	public LocalizedText Name => Strings.Actions.LogMessage.Name();

	public LocalizedText Description => Strings.Actions.LogMessage.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Text(
			MessageParameter,
			label: Strings.Actions.LogMessage.Message.Label(),
			description: Strings.Actions.LogMessage.Message.Description(),
			placeholder: Strings.Actions.LogMessage.Message.Placeholder(),
			required: true),
	];

	public MacroDeckPlatform Platforms => MacroDeckPlatform.All;

	public IActionExecutor CreateExecutor() => new Executor(_logger);

	private sealed class Executor : IActionExecutor
	{
		private readonly ILogger _logger;

		public Executor(ILogger logger) => _logger = logger;

		public Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			var message = context.Parameters.TryGetValue(MessageParameter, out var value)
				? value.ToString()
				: null;

			// The parameter is required, but the host still sends whatever the user configured, so the
			// executor is the only place that can decide the action did not do what it claims.
			if (string.IsNullOrWhiteSpace(message))
			{
				return Task.FromResult(ActionResult.Failed(
					ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.LogMessage.Message.Label())));
			}

			_logger.Information("{Message}", message);
			return ActionResult.SucceededTask;
		}
	}
}
```

## File: src/MacroDeck.PluginTemplate/MacroDeck.PluginTemplate.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <!-- Pinned rather than taken from the project file name: manifest.json declares this executable
             name, and the generated Strings class lives in this namespace, so renaming the .csproj later
             must neither rename the built executable nor move Strings out from under the code. -->
        <AssemblyName>MacroDeck.PluginTemplate</AssemblyName>
        <RootNamespace>MacroDeck.PluginTemplate</RootNamespace>
        <IsPackable>false</IsPackable>
        <UserSecretsId>MacroDeck.PluginTemplate-PluginDevelopment</UserSecretsId>
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

## File: src/MacroDeck.PluginTemplate/PluginIntegration.cs

```csharp
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using Serilog;

namespace MacroDeck.PluginTemplate;

/// <summary>
/// The plugin's one integration. It declares a single example action: add more to <see cref="Actions"/>,
/// and opt into a capability by implementing its interface here (<c>IVariableProvider</c>,
/// <c>IEventProvider</c>, <c>IConfigFlowProvider</c>, and so on).
/// </summary>
public sealed class PluginIntegration : IPluginIntegration
{
	private readonly ILogger _logger;

	// Built by DI, so anything the container knows can be taken here: IHttpClientFactory, IOptions<T>,
	// PluginMetadata, IPluginCatalogNotifier.
	public PluginIntegration(ILogger logger)
	{
		_logger = logger.ForContext<PluginIntegration>();
		Actions = [new LogMessageAction(logger)];
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

	/// <summary>
	/// Runs once the session is established, and again after a non-resume reconnect or a configuration
	/// change, so it has to be safe to run repeatedly against an already-initialized process.
	/// </summary>
	public Task InitializeAsync(IIntegrationContext context)
	{
		_logger.Information("Initialized.");
		return Task.CompletedTask;
	}

	public Task ShutdownAsync() => Task.CompletedTask;
}
```

## File: src/MacroDeck.PluginTemplate/Program.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Serilog;
using MacroDeck.PluginTemplate;

// Identity, description and icon are not set here: they come from manifest.json at the content root.
// Strings is generated from Localization/*.resx, so UseLocalization is what makes every LocalizedString
// below resolve in the user's language rather than falling back to its key.
var plugin = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<PluginIntegration>()
	.Build();

await plugin.RunAsync();
```

## File: src/MacroDeck.PluginTemplate/Properties/launchSettings.json

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

## File: src/MacroDeck.PluginTemplate/macrodeck-build.json

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish", "MacroDeck.PluginTemplate.csproj",
        "-c", "Release",
        "-r", "win-x64",
        "--self-contained", "false",
        "-p:UseAppHost=false",
        "-o", "bin/publish/win-x64"
      ],
      "output": "bin/publish/win-x64"
    },
    "osx-arm64": {
      "executable": "dotnet",
      "arguments": [
        "publish", "MacroDeck.PluginTemplate.csproj",
        "-c", "Release",
        "-r", "osx-arm64",
        "--self-contained", "false",
        "-p:UseAppHost=false",
        "-o", "bin/publish/osx-arm64"
      ],
      "output": "bin/publish/osx-arm64"
    },
    "linux-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish", "MacroDeck.PluginTemplate.csproj",
        "-c", "Release",
        "-r", "linux-x64",
        "--self-contained", "false",
        "-p:UseAppHost=false",
        "-o", "bin/publish/linux-x64"
      ],
      "output": "bin/publish/linux-x64"
    }
  }
}
```

## File: src/MacroDeck.PluginTemplate/manifest.json

```json
{
  "$schema": "https://schemas.macro-deck.app/plugin-manifest-v1.schema.json",
  "manifestVersion": 1,
  "id": "app.macro-deck.template",
  "name": "Macro Deck Plugin Template",
  "version": "1.0.0",
  "description": "A minimal Macro Deck 3 plugin.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": { "executable": "runtimes/win-x64/MacroDeck.PluginTemplate.dll", "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" } },
    "osx-arm64": { "executable": "runtimes/osx-arm64/MacroDeck.PluginTemplate.dll", "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" } },
    "linux-x64": { "executable": "runtimes/linux-x64/MacroDeck.PluginTemplate.dll", "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" } }
  },
  "publisher": {
    "name": "Example Publisher"
  },
  "license": "MIT",
  "repository": "https://github.com/example/my-plugin",
  "compatibility": {
    "macroDeck": ">=3.0.0-0"
  }
}
```

## File: tests/MacroDeck.PluginTemplate.Tests/MacroDeck.PluginTemplate.Tests.csproj

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
        <ProjectReference Include="..\..\src\MacroDeck.PluginTemplate\MacroDeck.PluginTemplate.csproj" />
    </ItemGroup>

</Project>
```

## File: tests/MacroDeck.PluginTemplate.Tests/PluginIntegrationTests.cs

```csharp
using MacroDeck.Plugin.Testing;
using NUnit.Framework;

namespace MacroDeck.PluginTemplate.Tests;

/// <summary>
/// Behaviour tests through <see cref="PluginTestHarness"/>: the plugin's own capability handlers run,
/// but nothing crosses a socket. This is where you test what your integration does.
/// </summary>
[TestFixture]
public sealed class PluginIntegrationTests
{
	private static PluginTestHarness CreateHarness() =>
		PluginTestHarness.Create(builder => builder
			.UseLocalization(Strings.LocalizationCatalog)
			.RegisterIntegration<PluginIntegration>());

	[Test]
	public async Task The_plugin_builds_and_initializes()
	{
		await using var harness = CreateHarness();

		Assert.DoesNotThrowAsync(harness.InitializeIntegrationsAsync);
	}

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

	[Test]
	public async Task The_example_action_fails_when_the_message_is_blank()
	{
		await using var harness = CreateHarness();
		await harness.InitializeIntegrationsAsync();

		var outcome = await harness.Actions.ExecuteAsync(
			"log-message",
			new Dictionary<string, object?> { ["message"] = "   " });

		Assert.That(outcome.Succeeded, Is.False);
	}
}

/// <summary>
/// The localization set is generated from <c>Localization/*.resx</c>, so these guard the wiring rather
/// than any wording: a missing catalog registration leaves every label showing its raw key.
/// </summary>
[TestFixture]
public sealed class LocalizationTests
{
	[Test]
	public void The_catalog_is_scoped_to_the_plugin_id()
	{
		Assert.That(Strings.LocalizationCatalog.Scope, Is.EqualTo("plugin:app.macro-deck.template"));
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
		Assert.That(Strings.LocalizationCatalog.KeysOf("en"), Does.Contain("Actions.LogMessage.Name"));
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
}
```

## File: Directory.Build.props

```xml
<Project>

    <PropertyGroup>
        <TargetFramework>net10.0</TargetFramework>
        <Nullable>enable</Nullable>
        <ImplicitUsings>true</ImplicitUsings>
        <AnalysisLevel>latest-recommended</AnalysisLevel>
        <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
        <WarningsAsErrors>CS8602</WarningsAsErrors>
    </PropertyGroup>

</Project>
```

## File: Directory.Packages.props

```xml
<Project>

    <PropertyGroup>
        <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
        <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
        <!-- The Macro Deck packages float to the newest published version, so no release version is
             pinned anywhere in this repository. -->
        <CentralPackageFloatingVersionsEnabled>true</CentralPackageFloatingVersionsEnabled>
        <!-- One knob for every Macro Deck package, so a build against a locally packed SDK is
             `dotnet build -p:MacroDeckSdkVersion=<version>` and nothing else - see README.md. -->
        <MacroDeckSdkVersion Condition="'$(MacroDeckSdkVersion)' == ''">3.0.0-*</MacroDeckSdkVersion>
    </PropertyGroup>

    <ItemGroup>
        <PackageVersion Include="MacroDeck.Localization" Version="$(MacroDeckSdkVersion)" />
        <PackageVersion Include="MacroDeck.Plugin.Analyzers" Version="$(MacroDeckSdkVersion)" />
        <PackageVersion Include="MacroDeck.Plugin.Hosting" Version="$(MacroDeckSdkVersion)" />
        <PackageVersion Include="MacroDeck.Plugin.Serilog" Version="$(MacroDeckSdkVersion)" />
        <PackageVersion Include="MacroDeck.Plugin.Testing" Version="$(MacroDeckSdkVersion)" />
        <PackageVersion Include="MacroDeck.Sdk" Version="$(MacroDeckSdkVersion)" />
    </ItemGroup>

    <ItemGroup>
        <PackageVersion Include="Microsoft.NET.Test.Sdk" Version="17.14.0" />
        <PackageVersion Include="NUnit" Version="4.3.2" />
        <PackageVersion Include="NUnit.Analyzers" Version="4.7.0" />
        <PackageVersion Include="NUnit3TestAdapter" Version="5.0.0" />
    </ItemGroup>

</Project>
```

## File: NuGet.config

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
    <packageSources>
        <clear />
        <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
        <!-- Empty in a fresh clone. `dotnet pack` the SDK into it to build against an unreleased
             version - see "Building against a local SDK build" in README.md. -->
        <add key="local" value="./local-feed" />
    </packageSources>
</configuration>
```

## File: .gitignore

```
# IDEs and editors
.idea/
.project
.classpath
.c9/
*.launch
.settings/
*.sublime-workspace
*.iml
*.ipr
*.iws
.claude/
.gemini/
.agents/
.playwright-mcp/
skills-lock.json
graphify-out
wiki-vault

# Visual Studio Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.history/*

# System files
.DS_Store
Thumbs.db
*~
*.swp
*.swo

# Compiled output
[Bb]in/
[Oo]bj/
[Bb]uild/
[Dd]ist/
out/
out-tsc/
bazel-out/
target/
coverage/
node_modules/

.angular/
typings/

# Logs and temporary files
.data/
# Root-anchored: an unanchored `logs/` also matched source folders (and matches
# case-insensitively on macOS/Windows), which silently swallowed a committed
# `Ui/Transport/Messages/Logs/`. Runtime log directories live under bin/ or
# outside the repo, and stray log files are still covered by *.log below.
/logs/
*.log
npm-debug.log
yarn-error.log
libpeerconnection.log
testem.log
.fuse_hidden*
.directory
.Trash-*
.nfs*
hs_err_pid*
.sass-cache/
connect.lock

# Packages
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Maven
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar
.flattened-pom.xml

# .NET
keys/
*.user
*.suo

# Local credentials persisted by the real-host launch profile
**/.macrodeck-dev-state/

# Test servers
test-servers/

# OS generated files
# General
.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two 
Icon

# Thumbnails
._*

# Files that might appear in the- root of a volume
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

# Windows thumbnail cache files
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db

# Dump file
*.stackdump

# Folder config file
[Dd]esktop.ini

# Recycle Bin used on file shares
$RECYCLE.BIN/

# Windows Installer files
*.cab
*.msi
*.msix
*.msm
*.msp

# Windows shortcuts
*.lnk

testresults.trx
TestResults
publish

# Locally packed Macro Deck SDK packages - see "Building against a local SDK build" in README.md
local-feed/*
!local-feed/.gitkeep
```

## File: README.md

````markdown
# Macro Deck plugin template

A starting point for an out-of-process Macro Deck 3 plugin: one integration with a single localized
example action, and the developer tooling wired up. The action exists to show the shape - the manifest,
the resource file, the executor contract - and is meant to be replaced rather than grown.

Looking for worked examples of each capability instead? The
[sample plugins repository](https://github.com/Macro-Deck-App/Macro-Deck-Sample-Plugins) has one
coherent plugin per area: actions and variables, a music player, a REST API with a multi-step config
flow, a virtual profile.

## Getting started

Either install the template and generate a project:

```bash
dotnet new install MacroDeck.Plugin.Templates@*-*
```

`@*-*` installs the newest published version. The floating form is what you want while the 3.0
template is in preview: `dotnet new install` picks stable versions by default, and there is no stable
release yet.

```bash
dotnet new macrodeck-plugin -n Acme.LightControl --pluginId com.acme.light-control --pluginName "Acme Light Control" \
  --publisher "Acme Inc" --repository https://github.com/acme/light-control \
  --platforms win-x64 --platforms osx-arm64 --platforms linux-x64
```

| Parameter | Default | What it sets |
| --- | --- | --- |
| `-n`, `--name` | `MacroDeckPlugin` | The project, namespace, solution and the executable names in `manifest.json` |
| `--pluginId` | `com.example.my-plugin` | The manifest `id`: reverse-domain, lowercase, at least two dot-joined kebab segments |
| `--pluginName` | `My Plugin` | The display name Macro Deck shows |
| `--publisher` | `Example Publisher` | `publisher.name` |
| `--description` | `A minimal Macro Deck 3 plugin.` | `description` |
| `--license` | `MIT` | `license`, as an SPDX identifier |
| `--repository` | `https://github.com/example/my-plugin` | `repository`: the GitHub repository the plugin is built from. The Store refuses the placeholder |
| `--homepage` | *(omitted)* | `homepage`. Left out of the manifest entirely when not supplied |
| `--platforms` | `win-x64`, `osx-arm64`, `linux-x64` | Which runtime identifiers land in `entrypoints` and `macrodeck-build.json`. Repeat the option per platform; `win-arm64`, `osx-x64` and `linux-arm64` are also available |

`--homepage` is omitted rather than written empty on purpose: the manifest schema requires an absolute
`http`/`https` URL, so `""` would fail validation. `repository` is always written, because the Macro
Deck Store refuses an upload without it: set it to the repository the plugin is built in.

The `macrodeck-plugin new` wizard collects the same values and passes them straight through, so
`dotnet new` and the CLI produce the same project.

Or clone this repository and rename by hand - the two are the same content. If you clone, change the
`id`, `name`, `version` and `description` in `src/MacroDeck.PluginTemplate/manifest.json`, then rename
the projects, the solution file and the namespace. The plugin project pins its `AssemblyName` and
`RootNamespace`. The `AssemblyName` is the executable name the manifest's `entrypoints` declare: change
both together, or they stop matching.

Either way, replace `Assets/icon.svg`. It is your plugin's icon: the manifest's `icon` path is the
single source of truth and the host reads that file directly, so there is no code to change.

## Requirements

- .NET SDK 10.0
- A running Macro Deck desktop app for [interactive debugging](#run-and-debug-against-macro-deck)

## Quick start

```bash
dotnet build
```

```bash
dotnet test
```

Build and tests need no Macro Deck installation. For an interactive session, use the checked-in
**Macro Deck - Real Host** launch profile after the one-time setup below.

## Building against a local SDK build

The template tracks the SDK's *published* packages and floats to the newest one, so a plain
`dotnet build` always resolves the latest release. While a change is still unreleased, pack the SDK
from a Macro Deck 3 checkout into this repository's `local-feed/` and build against that version:

```bash
dotnet pack MacroDeck.slnx -c Release -p:Version=3.0.0-local.1 -o <path-to-this-repo>/local-feed
```

```bash
dotnet build -p:MacroDeckSdkVersion=3.0.0-local.1
```

`NuGet.config` already lists `local-feed/` as a package source, and `MacroDeckSdkVersion` sets the
version for every Macro Deck package at once (see `Directory.Packages.props`). Nothing in the
repository pins the local version, so a plain `dotnet build` goes back to the published one.

Pick a version that cannot collide with a real release - `3.0.0-local.N` rather than reusing a
published preview version, which would put a hand-built package into the global NuGet cache under the
name of a published one.

## How a plugin is put together

### Project layout

```
src/MacroDeck.PluginTemplate/
  Program.cs             the host builder - a few lines and a RunAsync
  manifest.json          identity, icon and per-platform entrypoints
  macrodeck-build.json   how `macrodeck-plugin build` publishes each platform
  PluginIntegration.cs   the integration: lifecycle and capability opt-ins
  LogMessageAction.cs    the example action, localized end to end
  Localization/Strings.resx   the default-culture strings, one file per language
  Assets/icon.svg        the icon the manifest declares
  Properties/launchSettings.json   the shared real-host debug profile
tests/MacroDeck.PluginTemplate.Tests/
  PluginIntegrationTests.cs   the plugin builds, the action runs, the catalog is wired
```

### The entry point

`MacroDeckPlugin.CreatePlugin(args)` wraps `WebApplication.CreateBuilder`, so everything an ASP.NET
Core application has is available - configuration, options binding, `IHttpClientFactory`, hosted
services, dependency injection:

```csharp
var plugin = MacroDeckPlugin.CreatePlugin(args)
    .UseMacroDeckLogging()
    .UseLocalization(Strings.LocalizationCatalog)
    .RegisterIntegration<PluginIntegration>()
    .Build();

await plugin.RunAsync();
```

`RegisterIntegration<T>()` is the one door: it registers the integration's actions plus a capability
handler for every SDK interface the type implements. The integration is built by DI, so it can take
`IHttpClientFactory`, `IOptions<T>`, Serilog's `ILogger`, `PluginMetadata` or `IPluginCatalogNotifier`
in its constructor. `UseMacroDeckLogging()` routes your log output to the host's log viewer.

Anything the container needs beyond that goes on `builder.Services` before `Build()`.

### The manifest

`manifest.json` is the plugin's identity, read from the content root at startup. `Build()` validates it
and fails fast on an invalid id, a missing name or version, or an unreadable icon.

```json
{
  "manifestVersion": 1,
  "id": "app.macro-deck.template",
  "name": "Macro Deck Plugin Template",
  "version": "1.0.0",
  "description": "A minimal Macro Deck 3 plugin.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": {
      "executable": "runtimes/win-x64/MacroDeck.PluginTemplate.dll",
      "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" }
    },
    "osx-arm64": {
      "executable": "runtimes/osx-arm64/MacroDeck.PluginTemplate.dll",
      "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" }
    },
    "linux-x64": {
      "executable": "runtimes/linux-x64/MacroDeck.PluginTemplate.dll",
      "runtime": { "kind": "FrameworkDependent", "dotnetVersion": "10.0" }
    }
  },
  "publisher": { "name": "Example Publisher" },
  "license": "MIT",
  "compatibility": { "macroDeck": ">=3.0.0-0" }
}
```

Only `manifestVersion`, `id`, `name`, `version` and `entrypoints` are required; `description`, `icon`,
`license`, `publisher.name` and `compatibility` are what publishing to the store additionally needs. A
manifest may also declare `permissions`, `dependencies`, `conflicts`, `iconPacks`, `languages` and
`files[]` - `macrodeck-plugin inspect` reports all of them, and `pack` recomputes `files[]` and
`languages` for you. Never hand-maintain those two.

Each entrypoint lives under `runtimes/<rid>/` so a multi-platform artifact cannot collide with itself.

The template is **framework-dependent**: each entrypoint names the `.dll` and carries a `runtime`
block, and `macrodeck-build.json` publishes with `--self-contained false` and `-p:UseAppHost=false`.
Macro Deck ships a .NET 10 runtime, including ASP.NET Core, with the host (from 3.0.0) and starts a
framework-dependent plugin on it, so the artifact carries only your own assemblies - about 0.7 MB per
platform for this template instead of about 43 MB self-contained. Because the process is the shared
`dotnet` executable running your `.dll`, the plugin shows up as `dotnet` in Task Manager, Activity
Monitor or `ps`, not under its own name.

**Self-contained** is still supported, and is what an entrypoint without a `runtime` block means. Choose
it when the plugin needs a runtime Macro Deck does not ship, such as another .NET major version. Switch
all three places together, per platform: drop the `runtime` block, point `executable` at the apphost
(`MacroDeck.PluginTemplate.exe` on Windows, `MacroDeck.PluginTemplate` elsewhere), and publish with
`--self-contained true` without `-p:UseAppHost=false`. Mixing the two pairings fails validation.

`win-arm64` falls back to `win-x64` and `osx-arm64` falls back to `osx-x64`; there is no `"any"` key,
and `linux-musl-*` resolves no fallback at all.

### The build configuration

`macrodeck-build.json` sits beside the manifest and tells `macrodeck-plugin build` how to produce each
runtime identifier the manifest declares:

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish", "MacroDeck.PluginTemplate.csproj",
        "-c", "Release",
        "-r", "win-x64",
        "--self-contained", "false",
        "-p:UseAppHost=false",
        "-o", "bin/publish/win-x64"
      ],
      "output": "bin/publish/win-x64"
    }
  }
}
```

`executable` plus `arguments` rather than a shell string, and one `output` directory per target. The
shape carries no .NET assumptions - the values do - so a plugin built with another toolchain replaces
the values and keeps the keys. A target is required for every runtime identifier the manifest
declares; adding a platform means adding it in both files.

### Capabilities

`PluginIntegration` implements `IPluginIntegration` - lifecycle and actions - and **opts into**
everything else by implementing that capability's interface. The host discovers each one by filtering
on the interface, so you only implement what you need. Identity and the icon are not on this list:
they come from the manifest.

| Capability | Interface |
| --- | --- |
| Actions | `IActionDefinition`, in `Actions` |
| Config flow | `IConfigFlowProvider` |
| Variables | `IVariableProvider` |
| Events | `IEventProvider` |
| Issues | `IIntegrationIssueProvider` |
| Music players | `IMusicPlayerProvider` |
| Weather | `IWeatherProvider` |
| Virtual profiles | `IProfileProvider` |

An integration that provides a config flow starts **disabled** until the user configures it; everything
else defaults to enabled.

Capability ids are namespaced by the host as `integrationId::localId`, so you declare provider-local
ids and never the qualified form.

The [sample plugins](https://github.com/Macro-Deck-App/Macro-Deck-Sample-Plugins) are the worked
examples for each of these.

## Localization

Every string a user reads comes from `Localization/Strings.resx`, not from a literal. The
`MacroDeck.Plugin.Analyzers` source generator turns that folder into a typed `Strings` class whose
members return a `LocalizedString` - a *reference*, not text - and
`UseLocalization(Strings.LocalizationCatalog)` in `Program.cs` hands the catalog to the host. The host
resolves each reference for whoever is reading it, so a language change takes effect without the plugin
rebuilding anything.

```csharp
public LocalizedText Name => Strings.Actions.LogMessage.Name();

public IReadOnlyList<ActionParameter> Parameters { get; } =
[
    ActionParameter.Text(
        "message",
        label: Strings.Actions.LogMessage.Message.Label(),
        description: Strings.Actions.LogMessage.Message.Description(),
        placeholder: Strings.Actions.LogMessage.Message.Placeholder(),
        required: true),
];
```

A dotted key becomes a nested class, so `Actions.LogMessage.Name` in the resource file is
`Strings.Actions.LogMessage.Name()` in code. Name keys after where they are used, so a translator can
place a string without reading the source.

Anywhere the SDK takes a `LocalizedText` takes one of these: action names and descriptions, parameter
labels, descriptions and placeholders, `ActionStateDefinition` labels, config flow step titles and field
labels, event and variable metadata, issue text, and the message on `ActionResult.Failed`. A plain
`string` also converts, and stays untranslated - which is what makes a missed one easy to spot once a
second language exists.

One field is deliberately *not* localized: `ConfigFlowResult.Complete(title, …)` takes a plain `string`,
because the host stores that title as the configured entry's name and the user can rename it.

### Reuse Macro Deck's own strings

`MacroDeckStrings` is the catalog Macro Deck already ships translated - `Common.*`, `Validation.*`,
`Connection.*`, `Settings.*`. Use it instead of declaring your own copy of a generic string; the example
action composes one with a key of its own:

```csharp
ActionResult.Failed(
    ActionErrorCodes.InvalidParameter,
    MacroDeckStrings.Validation.Required(Strings.Actions.LogMessage.Message.Label()));
```

### Adding a key

1. Add a `<data name="..."><value>...</value></data>` entry to `Localization/Strings.resx`.
2. Build. The generator adds the matching `Strings.*` member.
3. Use it wherever the SDK asks for a `LocalizedText`.

Placeholders are named and substituted by name, not by argument order:

```xml
<data name="Actions.Ping.Result" xml:space="preserve">
  <value>Reached {host} in {milliseconds} ms.</value>
  <comment>[milliseconds:int] Round-trip time.</comment>
</data>
```

The generator turns each into a method parameter, so forgetting one is a compile error. A placeholder is
a `string` unless a bracketed prefix on the `<comment>` narrows it to `int`, `long`, `double` or `bool`;
the rest of the comment stays the note a translator reads.

A count-dependent sentence is one key with `[plural]` on every form and keys suffixed `.One` and
`.Other` (`Other` is required). The two entries generate a single member taking the count first. The rule
is `count == 1` for every language - deliberately not CLDR - so phrase `Other` to stay grammatical for
languages that need forms this model has no room for.

### Adding a language

Add `Localization/Strings.<culture>.resx` beside the default file, using a well-formed BCP-47 name:
`Strings.de.resx`, `Strings.pt-BR.resx`, `Strings.zh-Hant-TW.resx`. Full tags only - `zh-Hans` and
`zh-Hant` are different languages and both would collapse onto `zh`. An underscore (`Strings.de_DE.resx`)
is a build error rather than a culture nobody ever reaches.

A translation needs only the keys it actually translates. Resolution tries the requested culture, its
neutral culture, the catalog's default language, then `en`, so a half-finished translation degrades to
English. A key no culture carries renders as a conspicuous `[[plugin:<id>:Key]]` rather than blank.
There is nothing to register per language - `Strings.LocalizationCatalog` already carries every culture
in the folder.

`macrodeck-plugin build` and `pack` derive the manifest's `languages` array from this folder. Do not
maintain it by hand.

The generator reports its own diagnostics while you type - a key only a translation has, a placeholder
set that disagrees with the default language, a malformed culture suffix, a broken plural family
(`MDLOC001`-`MDLOC008`).

### Editing translations

`.resx` is the canonical format because [JetBrains Rider's Localization
Manager](https://www.jetbrains.com/help/rider/Localizing_Applications.html) reads it: every key as a
row, every culture as a column, missing translations highlighted, CSV export for handing a translator a
spreadsheet, and renames applied across every culture at once. Nothing requires Rider - these are plain
`.resx` files - but that is the workflow the format was chosen to unlock.

The full reference, including every diagnostic, is the
[localization guide](https://docs.macro-deck.app/sdk/localization/).

## Run and debug against Macro Deck

The project contains exactly one interactive launch profile: **Macro Deck - Real Host**. It launches
the plugin project directly, so Rider and Visual Studio attach the debugger to plugin code without a
wrapper or child-process attach. The profile connects in self-registering mode to the installed Macro
Deck desktop app at `http://127.0.0.1:8193`.

For the first run:

1. Start Macro Deck.
2. Open **Developer Tools → Plugin tokens**, create a token and copy it. It is shown only once.
3. Store the token in the source project's **.NET User Secrets** using one of the methods below. The
   project is already initialized; do not run `dotnet user-secrets init`.
4. Select **Macro Deck - Real Host** and start it with **Debug**.
5. Once enrollment succeeds, remove the token from User Secrets.

### Set the token in Rider or Visual Studio

In Rider, right-click `MacroDeck.PluginTemplate` in the Solution Explorer and select
**Tools → .NET User Secrets**. In Visual Studio, right-click the same source project and select
**Manage User Secrets**. Do not select the `.Tests` project.

The IDE opens a `secrets.json` file stored in your user profile, outside this repository. Replace its
contents with:

```json
{
  "MacroDeck:Plugin:EnrollmentToken": "<paste the one-time token here>"
}
```

Save the file, then start **Macro Deck - Real Host**. After enrollment, reopen `secrets.json` and
remove the `MacroDeck:Plugin:EnrollmentToken` entry.

### Set the token from a terminal

From the repository root on macOS or Linux, use the following form. It reads the token without echoing
it and does not put the value in shell history or process arguments:

```bash
project="src/MacroDeck.PluginTemplate/MacroDeck.PluginTemplate.csproj"
printf "Enrollment token: "
read -rs md_enrollment_token
printf '\n'
printf '{"MacroDeck:Plugin:EnrollmentToken":"%s"}\n' "$md_enrollment_token" |
  dotnet user-secrets set --project "$project"
unset md_enrollment_token
```

After the first successful profile launch, remove the one-time token:

```bash
dotnet user-secrets remove "MacroDeck:Plugin:EnrollmentToken" --project "$project"
```

With PowerShell 7, use the equivalent masked-input form:

```powershell
$project = "src/MacroDeck.PluginTemplate/MacroDeck.PluginTemplate.csproj"
$token = Read-Host "Enrollment token" -MaskInput
@{ "MacroDeck:Plugin:EnrollmentToken" = $token } |
  ConvertTo-Json -Compress |
  dotnet user-secrets set --project $project
Remove-Variable token
```

Then remove it after enrollment:

```powershell
dotnet user-secrets remove "MacroDeck:Plugin:EnrollmentToken" --project $project
```

The profile persists the exchanged plugin credential under
`src/MacroDeck.PluginTemplate/.macrodeck-dev-state/`, which is ignored by Git and excluded from the
template package. Later profile launches reuse that credential. The User Secrets id is renamed with a
generated project, so each plugin gets a separate local secret store.

User Secrets are local-only but not encrypted. Never put the enrollment token in `launchSettings.json`,
a shared IDE configuration, a literal command argument or a commit. If you intentionally clear the
local state, create a fresh token and repeat the User Secrets step. Self-registration only works
against a host on the same machine. See the official
[Rider User Secrets guide](https://www.jetbrains.com/help/rider/Manage_NET_user_secrets.html) and
[.NET Secret Manager guide](https://learn.microsoft.com/aspnet/core/security/app-secrets?view=aspnetcore-10.0)
for more background.

## The developer CLI

`macrodeck-plugin` validates, inspects, packs and conformance-tests a plugin. Interactive starts use the
launch profile above.

```bash
dotnet tool install --global MacroDeck.Plugin.Cli --prerelease
```

`--prerelease` is required while the 3.0 SDK is in preview: only preview versions are published, and
`dotnet tool install` picks stable ones by default. Drop it once 3.0 ships.

The tool needs the **ASP.NET Core shared framework**, not just the .NET runtime - its stub host is a
real Kestrel server.

| Command | What it does |
| --- | --- |
| `new` | Scaffolds a project from this template, prompting for the values `dotnet new` takes as parameters. |
| `build` | Publishes every runtime identifier the manifest declares using `macrodeck-build.json`, then packs the result. |
| `validate` | Checks a manifest, version directory or artifact against the real manifest reader, the JSON Schema, the permission vocabulary and declared file digests. |
| `inspect` | Reports what installing an artifact would find - entrypoints, permissions, dependencies, conflicts, compatibility, signature shape, size. |
| `pack` | Builds a `.macroDeckPlugin` artifact, validating the manifest first and recomputing `files[]` digests. |
| `run` | Launches the plugin against a real host or a disposable stub one, streaming its output. |
| `test` | Runs the conformance suite and writes a text, JSON or Markdown report. |
| `sign`, `verify`, `keygen` | Creator signing for a packed artifact. |

### Running without a host

```bash
macrodeck-plugin run --project src/MacroDeck.PluginTemplate --stub-host
```

`--stub-host` starts a disposable in-process host, so this needs no Macro Deck installation: the plugin
registers, negotiates the protocol and initializes, and its log output is streamed until you interrupt
it. `--artifact <file>` does the same for a packed artifact, which is what proves an entrypoint path in
the manifest matches what `build` actually wrote. Drop `--stub-host` to attach to the running desktop
app instead; for debugging with breakpoints, use the launch profile above rather than this.

### Packing a release

`build` is the whole path: it reads `macrodeck-build.json`, publishes each declared platform into its
`runtimes/<rid>/` slot and packs the artifact.

```bash
macrodeck-plugin build --source src/MacroDeck.PluginTemplate --output ./artifacts
```

```bash
macrodeck-plugin build --source src/MacroDeck.PluginTemplate --rid win-x64 --output ./artifacts
```

The second form builds one platform, which is what a CI matrix job wants.

```bash
macrodeck-plugin inspect --artifact ./artifacts/<id>-<version>.macroDeckPlugin
```

Packing validates before it writes, so a bad manifest never becomes an artifact. It discards whatever
`files[]` the source manifest declared and recomputes every digest from disk, and fills in `languages`
from `Localization/`. It cannot sign anything: sign *after* packing, against the packed manifest, or the
digest will not match.

A plain `dotnet build -c Release` does not produce a packable layout - the manifest points at
`runtimes/<rid>/`, which only `build` assembles. Use `validate` against a built artifact or a version
directory rather than against `bin/Release/net10.0`.

### Conformance

```bash
macrodeck-plugin test --project src/MacroDeck.PluginTemplate --report markdown --output conformance.md
```

The suite drives a real session against your plugin: capability contracts, invocation and cancellation
semantics, reconnect and resume behaviour, the reserved `/_macrodeck/*` endpoints, and logging limits.
Checks are Required or Recommended, each with a stable id (`MDC0401`, …) you can select with `--check`
or `--category`. A check can report `SKIP` with a reason when your plugin gives it nothing to observe -
which is most of them until you add capabilities.

Exit codes make it usable as a CI gate - `0` conformant, `1` the plugin is wrong, `2` usage error, `3`
input unreadable, `4` cancelled. `1` and `3` are deliberately distinct: a missing file is an
environment problem, not a verdict about the plugin.

## Testing

```bash
dotnet test
```

The test project references `MacroDeck.Plugin.Testing`, which provides a loopback test host, fakes and
assertions for testing a plugin without a running Macro Deck. `PluginTestHarness.Create` builds your
plugin from the same `Action<PluginHostBuilder>` `Program.cs` uses - no socket, no host, no built
executable - with a `ManualTimeProvider` for the clock and a `FakeIntegrationContext` you can seed and
assert against:

```csharp
await using var harness = PluginTestHarness.Create(builder => builder.RegisterIntegration<PluginIntegration>());
await harness.InitializeIntegrationsAsync();
```

Drive capabilities through the typed clients it exposes (`harness.Actions`, `harness.Variables`, …)
rather than calling an executor directly, so parameter binding is under test too.
`MacroDeckTestHost.HostAsync` puts the wire itself under test, and `MacroDeckTestHost.LaunchAsync`
runs a real child process.

The conformance suite above covers the protocol contract; these tests are for your own behaviour.

## Contributing to the template

The template repository's root *is* the `dotnet new` content, so changing the template is an ordinary
change to the plugin in `src/`. How the package is built and released is documented in
[`packaging/README.md`](https://github.com/Macro-Deck-App/Macro-Deck-Plugin-Template/blob/main/packaging/README.md).

## License

MIT - see [LICENSE](LICENSE). Macro Deck itself is licensed under Apache 2.0.

A generated project carries this MIT `LICENSE` file whatever `--license` you passed: the parameter sets
the manifest's `license` field only. If you chose something else, replace `LICENSE` to match.

## Further reading

- [Plugin development docs](https://github.com/Macro-Deck-App/Macro-Deck-3/tree/main/docs/plugin-development)
- [Sample plugins](https://github.com/Macro-Deck-App/Macro-Deck-Sample-Plugins) - a worked example per capability
- [`plugin-hosting.md`](https://github.com/Macro-Deck-App/Macro-Deck-3/blob/main/docs/plugin-development/plugin-hosting.md) - the builder API, registration modes, the artifact format and every `MACRO_DECK_PLUGIN_*` variable
- [`sdk-reference.md`](https://github.com/Macro-Deck-App/Macro-Deck-3/blob/main/docs/plugin-development/sdk-reference.md) - every interface and record you build against
- [`cli.md`](https://github.com/Macro-Deck-App/Macro-Deck-3/blob/main/docs/plugin-development/cli.md) - every CLI command and option
- [`testing-plugins.md`](https://github.com/Macro-Deck-App/Macro-Deck-3/blob/main/docs/plugin-development/testing-plugins.md) - the test harness, the fakes and the manual clock
- [`conformance.md`](https://github.com/Macro-Deck-App/Macro-Deck-3/blob/main/docs/plugin-development/conformance.md) - the conformance suite and its check ids
- [`analyzers.md`](https://github.com/Macro-Deck-App/Macro-Deck-3/blob/main/docs/plugin-development/analyzers.md) - the compile-time diagnostics
````
