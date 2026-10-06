# Macro Deck UI: views and surfaces

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Views and surfaces: https://docs.macro-deck.app/ui/views/
- Serving a configuration view: https://docs.macro-deck.app/ui/views/configuration/
- Custom views: https://docs.macro-deck.app/ui/views/custom/
- Developer preview: https://docs.macro-deck.app/ui/views/developer-preview/
- Folder views: https://docs.macro-deck.app/ui/views/folder-views/
- Modal views: https://docs.macro-deck.app/ui/views/modal/
- Screensavers: https://docs.macro-deck.app/ui/views/screensavers/
- Serving a view: https://docs.macro-deck.app/ui/views/sessions/
- Configuring a widget: https://docs.macro-deck.app/ui/views/widget-configuration/
- Widget types: https://docs.macro-deck.app/ui/views/widget-types/
- Deck widget views: https://docs.macro-deck.app/ui/views/widget/

## Views and surfaces

> Source: https://docs.macro-deck.app/ui/views/
>
> What a view and a surface are, the surface kinds Macro Deck offers, session modes, and which representation a client renders.

A view is rendered inside a host-owned **session**, against one **surface** - a place in the app a tree can
appear.

### Example

```csharp
public sealed class WeatherUiProvider : IUiProvider
{
    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
    [
        new() { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared },
        new() { Kind = UiSurfaceKinds.Folder, SessionMode = UiSessionModes.Shared },
        new() { Kind = UiSurfaceKinds.Config, SessionMode = UiSessionModes.Exclusive },
    ];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
        => Task.FromResult<IUiSession?>(null); // one branch per kind - see Serving a view
}
```

### Surface kinds

| Kind | What it is | Who opens it | Session mode | Page |
| --- | --- | --- | --- | --- |
| `config` | An integration's config flow, a configured action instance, a folder's view settings, a widget's settings, or a device's screensaver settings | The user, from a configuration dialog | exclusive | [Serving a configuration view](https://docs.macro-deck.app/ui/views/configuration/), [Configuring a widget](https://docs.macro-deck.app/ui/views/widget-configuration/) |
| `widget` | A deck widget | Every client showing the deck | shared | [Deck widget views](https://docs.macro-deck.app/ui/views/widget/) |
| `preview` | A read-only rendering of a widget's unsaved draft, such as in the editor or the widget picker | The widget editor | shared | [Deck widget views](https://docs.macro-deck.app/ui/views/widget/) |
| `folder` | A whole folder that selected a custom view | Every client showing the folder | shared | [Folder views](https://docs.macro-deck.app/ui/views/folder-views/) |
| `screensaver` | What a device shows after sitting idle | The device itself, when its idle timer fires | shared | [Screensavers](https://docs.macro-deck.app/ui/views/screensavers/) |
| `dialog` | A modal an action opened | The action | exclusive | [Modal views](https://docs.macro-deck.app/ui/views/modal/) |
| `developer-preview` | One `[UiPreview]` scenario | Developer Tools | exclusive | [Developer preview](https://docs.macro-deck.app/ui/views/developer-preview/) |

- **shared** - several clients may be attached at once, such as the same widget on two devices. You never
  address one client, except through an event's `clientId`.
- **exclusive** - one client owns the session, so another client's attach cannot reset entered values in
  a `dialog` or `config` tree.

The tree, the patch and the session are transport-neutral `MacroDeck.Ui.Model` vocabulary. The surface
kind is Macro Deck's own and is open, like node types: decline a kind you do not recognise by returning
`null` - that is correct, not an error.

### Which representation a client renders

| Surface | When the tree is declined or fails |
| --- | --- |
| `config` for a config flow or an action | The client renders your declared `ConfigFlowStep.Fields` or `IActionDefinition.Parameters` instead. |
| `config` for a widget | Only the editor's JSON mode is left - see [Configuring a widget](https://docs.macro-deck.app/ui/views/widget-configuration/#declining). |
| `widget`, `folder`, `dialog` | Nothing is rendered. There is no non-tree fallback. |

A client renders one representation, never a mix. It negotiates the UI model version locally before a
session is opened, so a client that cannot render your tree costs you no session and no slot.

### See also

- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/) - the session lifecycle every kind shares
- [The UI model](https://docs.macro-deck.app/ui/concepts/ui-model/)

## Serving a configuration view

> Source: https://docs.macro-deck.app/ui/views/configuration/
>
> Rendering a config flow or an action's configuration as a Macro Deck UI tree beside the declared fields it never replaces.

Serve a tree for an integration's config flow or one configured action instance, beside the declared
fields it never replaces.

### Example

A config flow whose step is also drawn as a tree. The input keys match the declared field names:

```csharp
public sealed class MediaServerIntegration : IPluginIntegration, IUiConfigFlowProvider
{
    public IReadOnlyList<IActionDefinition> Actions { get; } = [new ToggleAction()];

    public IConfigFlow CreateConfigFlow() => new MediaServerConfigFlow();

    public Task InitializeAsync(IIntegrationContext context) => Task.CompletedTask;

    public Task ShutdownAsync() => Task.CompletedTask;
}

public sealed class MediaServerConfigFlow : IUiConfigFlow
{
    private static ConfigFlowStep ConnectionStep() => new()
    {
        StepId = "connection",
        Title = Strings.Setup.ConnectionTitle(),
        Fields =
        [
            ActionParameter.Secret("api_key", label: Strings.Setup.ApiKey(), required: true),
            ActionParameter.Number("poll_seconds", label: Strings.Setup.PollInterval(), min: 5, max: 3600,
                defaultValue: 30),
        ],
    };

    public Task<ConfigFlowResult> StartAsync(IConfigFlowContext context, CancellationToken cancellationToken)
        => Task.FromResult(ConfigFlowResult.Step(ConnectionStep()));

    public async Task<ConfigFlowResult> SubmitAsync(string stepId, IReadOnlyDictionary<string, object?> input,
        IConfigFlowContext context, CancellationToken cancellationToken)
    {
        var apiKey = input.GetValueOrDefault("api_key") as string ?? string.Empty;

        return await MediaServerClient.CanConnectAsync(apiKey, cancellationToken)
            ? ConfigFlowResult.Complete("Media server")
            : ConfigFlowResult.Error(ConnectionStep(), Strings.Setup.CannotConnect());
    }

    public Task<IUiSession?> CreateUiSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        var apiKey = new UiState<string>(string.Empty);
        var pollSeconds = new UiState<double>(30);

        var root = new UiConfigStack
        {
            Key = "root",
            Children =
            [
                new UiSecretInput
                {
                    Key = "api_key",
                    Label = Strings.Setup.ApiKey(),
                    Required = true,
                    Binding = Bind.To(apiKey),
                },
                new UiNumberInput
                {
                    Key = "poll_seconds",
                    Label = Strings.Setup.PollInterval(),
                    Description = Strings.Setup.PollIntervalHint(),
                    Min = 5,
                    Max = 3600,
                    ShowSlider = true,
                    Binding = Bind.To(pollSeconds),
                },
            ],
        };

        return Task.FromResult<IUiSession?>(new ViewSession(new UiView(request.Surface, root)));
    }
}
```

`ViewSession` is the adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example).

### The tree renders a transaction it does not own

```csharp
// Declared fields stay - they are the fallback and they mark secrets.
ActionParameter.Secret("api_key", label: Strings.Setup.ApiKey(), required: true)

// The tree's top-level input with the same key feeds the same submit.
new UiSecretInput { Key = "api_key", Label = Strings.Setup.ApiKey(), Binding = Bind.To(apiKey) }
```

A configuration tree never completes a flow and never persists a parameter. `SubmitAsync` stays the only
way a flow accepts values, and the ordinary save path the only way an action instance is written - which
keeps secret encryption, OAuth and entry replacement unchanged
([ADR 0050](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0050-ui-sessions-are-host-brokered.md)).

- **Keep serving the declared fields.** `ConfigFlowStep.Fields` and `IActionDefinition.Parameters` are
  still required: they are the fallback, and for a config flow they tell Macro Deck which submitted values
  are secret.
- **Name top-level inputs after their fields.** A top-level input's node id is the field key it submits.

For a config flow, Macro Deck draws the dialog's Continue and Cancel buttons itself, so the tree needs no
submit control of its own:

- **Continue submits what the tree shows.** When the user presses it, the current value of each input whose
  id is a declared field name is sent to `SubmitAsync`, including a value the user typed and one you patched
  in. Inputs whose id is not a declared field name are not picked up this way.
- **`UiFlow.CanSubmit` gates Continue when you set it.** Leave it unset and Continue is enabled once every
  visible required declared field has a value in the tree. Either way, a `ConfigFlowResult.Error` from
  `SubmitAsync` is shown in the dialog.
- **The tree is not seeded from the stored entry.** On a reconfigure your flow is not handed the existing
  values, so the tree shows - and Continue submits - whatever you built it with. Seed it from your own live
  configuration if a reconfigure should start from the current values.

### From a config flow

```csharp
public sealed class MediaServerIntegration : IPluginIntegration, IUiConfigFlowProvider { /* ... */ }

public sealed class MediaServerConfigFlow : IUiConfigFlow
{
    public Task<IUiSession?> CreateUiSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
        => Task.FromResult<IUiSession?>(new ViewSession(new UiView(request.Surface, BuildTree())));
}
```

`IUiConfigFlowProvider` goes on the integration; `describe` then reports `servesConfigUiTree`.
`IUiConfigFlow` goes on the flow object itself, so the tree's state and `SubmitAsync`'s state are one
thing. Macro Deck relays the tree without inspecting it, so it cannot tell which tree values are secret:
**a flow serving a tree classifies its own secrets** by returning them as `ConfigFlowValue.Secret` from
`Complete`.

`CreateUiSessionAsync` can be called more than once for the same flow: Macro Deck opens a new session after
a session ended with a retryable error, and after .NET Hot Reload updated your plugin. Build each session
from state the flow holds, not from anything the previous session kept. The user's unsaved edits reach the
new session as `change` events, the same way they reached the first one.

### From an action

```csharp
public sealed class ToggleAction : IUiConfigurableActionDefinition
{
    public string Id => "toggle";

    public LocalizedText Name => Strings.Toggle.Name();

    public LocalizedText Description => Strings.Toggle.Description();

    public IReadOnlyList<ActionParameter> Parameters { get; } =
    [
        ActionParameter.Text("target", label: Strings.Toggle.Target(), required: true),
        ActionParameter.Text("mode", label: Strings.Toggle.Mode(), defaultValue: "toggle"),
    ];

    public IActionExecutor CreateExecutor() => new ToggleExecutor();

    public Task<IUiSession?> CreateConfigurationSessionAsync(ActionConfigurationRequest request,
        CancellationToken cancellationToken)
    {
        var target = new UiState<string>(Read(request, "target") ?? string.Empty);
        var mode = new UiState<string>(Read(request, "mode") ?? "toggle");

        var root = new UiConfigStack
        {
            Key = "root",
            Children =
            [
                new UiStringInput { Key = "target", Label = Strings.Toggle.Target(), Required = true, Binding = Bind.To(target) },
                new UiChoiceInput
                {
                    Key = "mode",
                    Label = Strings.Toggle.Mode(),
                    Segmented = true,
                    Binding = Bind.To(mode),
                    Options = UiValue.Of<IReadOnlyList<UiOption>>([
                        UiOption.Of("on", Strings.Toggle.ModeOn()),
                        UiOption.Of("off", Strings.Toggle.ModeOff()),
                        UiOption.Of("toggle", Strings.Toggle.ModeToggle()),
                    ]),
                },
            ],
        };

        return Task.FromResult<IUiSession?>(new ViewSession(new UiView(request.Session.Surface, root)));
    }

    private static string? Read(ActionConfigurationRequest request, string name)
        => request.Parameters.TryGetValue(name, out var value) && value.ValueKind == JsonValueKind.String
            ? value.GetString()
            : null;
}
```

One session is created per open configuration surface, so several can be live for the same action at
once - keep state on the session, never on the definition. `request.Parameters` holds the instance's
stored values, keyed by parameter name. `Secret` and `Password` parameters arrive **masked**
(`UiConfigSurfaceAttributes.MaskedSecretValue`, `"$masked"`), because opening a configuration surface is
not an intent to reveal a secret. You get the real value the ordinary way, when the user submits.

### Letting the user pick a file, folder or image

For a path, use a path input rather than a `UiStringInput`, so the user can browse instead of typing:

```csharp
var folder = new UiState<string>(string.Empty);
var placeholder = new UiState<string>(string.Empty);

new UiConfigStack
{
    Key = "root",
    Children =
    [
        new UiFolderInput { Key = "folder", Label = Strings.Frame.Folder(), Required = true, Binding = Bind.To(folder) },
        new UiImageInput
        {
            Key = "placeholder",
            Label = Strings.Frame.Placeholder(),
            Description = Strings.Frame.PlaceholderHint(),
            FileExtensions = UiValue.Of<IReadOnlyList<string>>(["png", "jpg", "webp"]),
            Binding = Bind.To(placeholder),
        },
    ],
}
```

| Node type | DSL element | Value |
| --- | --- | --- |
| `folder` | `UiFolderInput` | A folder path |
| `file` | `UiFileInput` | A file path, optionally limited to `FileExtensions` |
| `image` | `UiImageInput` | An image file path, limited to image formats unless `FileExtensions` says otherwise |

The value is a plain path string on the computer that runs Macro Deck, not on the device the user is
looking from. The path inputs work in every configuration surface on this page, including widget, folder
view and screensaver configuration.

- **`FileExtensions` are bare extensions, without the dot**: `["png", "jpg"]`, not `[".png"]`. They narrow
  what browsing and dropping offer. Leave them unset and a file input accepts any file, while an image
  input offers the image formats the renderer can draw (PNG, JPEG, GIF, WebP, SVG). Setting them on an
  image input replaces that list rather than adding to it.
- **Macro Deck does not check the path.** The user can type or paste any value, including one outside
  `FileExtensions`, and a file can be moved or deleted after it was picked. Handle a missing file where you
  read it.
- `Label`, `Description` and `Placeholder` apply as on any input, and `Required` marks the label. Without a
  `Placeholder`, the renderer shows its own hint for the kind of path.

The Macro Deck desktop editor draws each as a text field with a Browse button. In the desktop app, Browse
opens the operating system's file or folder dialog; where that is not available, it opens Macro Deck's
own file browser. A file or folder dropped onto the field fills it in, if it matches the input. The image
input shows no preview of the picked file.

In a declared field list, the counterparts are `ActionParameter.File` (with `fileExtensions`),
`ActionParameter.Folder` and `ActionParameter.Image`, which takes no extensions and always offers the
image formats.

### Letting the user set colour thresholds

A `UiThresholdsInput` works in a config flow and an action's configuration as it does in a
[widget configuration](https://docs.macro-deck.app/ui/views/widget-configuration/#colour-thresholds): a bar of coloured bands with draggable
boundaries, whose value arrives in your binding as a `UiThresholds`.

### Showing what governs a setting

`UiStatus` is a compact, framed line for "this setting is currently controlled by something else": an
optional leading `Icon`, a muted `Label` and the emphasized `Value` it introduces. Its children are drawn
trailing the text; an icon-only `UiConfigButton` there becomes a borderless control, typically the one that
stops what the line names.

```csharp
var stop = new UiConfigButton
{
    Key = "stop",
    Label = "Stop using",
    Icon = "x",
    Events = [UiEventHandler.On(UiConfigEvents.Activate, StopUsingProvider)],
};

new UiStatus
{
    Key = "provider",
    Icon = "zap",
    Label = "Provided by",
    Value = "Mute / Unmute",
    Children = [stop],
    Fallback = new UiConfigStack
    {
        Key = "provider-fallback",
        Children = [new UiProse { Key = "provider-text", Text = "Provided by Mute / Unmute" }, stop with { Key = "stop-text", Icon = default }],
    },
}
```

A renderer that predates `status` declines it like any unknown type and draws the `Fallback`, so give it one
built from a `UiProse` and the same button where the line matters.

### Asking before a button acts

A `UiConfigButton` can ask first. With `ConfirmMessage` set, the renderer shows a dialog (`ConfirmTitle`,
`ConfirmLabel`, and `ConfirmDanger` for a destructive action) and raises `activate` only when the user
accepts. With `PromptValue` set, the dialog asks for text instead, starting from that value with
`Placeholder` as its hint, and `activate` carries the entered text as a string payload:

```csharp
new UiConfigButton
{
    Key = "rename",
    Label = "Rename",
    ConfirmLabel = "Save",
    PromptValue = UiValue.From(() => current.Value),
    Events = [UiEventHandler.On(UiConfigEvents.Activate, data =>
    {
        if (data.TryGetString(out var name) && name.Trim().Length > 0)
        {
            current.Value = name.Trim();
        }
    })],
}
```

A renderer that predates these properties raises `activate` at once and without a payload, so a handler
has to tolerate a missing answer, and an action that cannot be undone should not rely on the question alone.

### Grouping actions in a menu

`UiConfigMenu` is a compact trigger (`Icon`, with `Label` as its accessible name) that opens a list of its
child `UiConfigButton`s, each drawn with its icon and label and each asking first if it declares a question.
A renderer that predates `menu` declines it and draws the node's `Fallback`.

### Putting a question to the user

`UiConfigDialog` is a modal dialog shown for as long as the node is in the tree, so a provider opens it by
adding it inside a `UiWhen` and closes it by removing it. `Title` is the heading and `Text` the message; child
`UiConfigButton`s are the answers, drawn in order with the last one as the primary answer (or as a warning
when it declares `ConfirmDanger`), and other children such as boolean inputs are the dialog's body. Closing the
dialog without answering raises `cancel` on it:

```csharp
new UiWhen
{
    Key = "stop-when",
    Condition = () => asking.Value,
    Content = () => new UiConfigDialog
    {
        Key = "stop",
        Title = "Stop using this provider?",
        Text = "Your own states come back.",
        Events = [UiEventHandler.On(UiConfigEvents.Cancel, () => asking.Value = false)],
        Children =
        [
            new UiConfigButton { Key = "keep", Label = "Cancel", Events = [UiEventHandler.On(UiConfigEvents.Activate, () => asking.Value = false)] },
            new UiConfigButton { Key = "stop-now", Label = "Stop using", ConfirmDanger = true, Events = [UiEventHandler.On(UiConfigEvents.Activate, Stop)] },
        ],
    },
}
```

A renderer that predates `dialog` declines it and draws its fallback in place.

### Declining and fallback

```csharp
public Task<IUiSession?> CreateUiSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    => Task.FromResult<IUiSession?>(null); // the client renders the declared fields
```

| What happens | What the user gets |
| --- | --- |
| You return `null` | The declared fields. Not an error. |
| The provider times out, disconnects or trips a session limit | The declared fields, never an error. |
| The client cannot render your UI model version | The declared fields. Negotiated before any session opens - no session, no slot. |

A client renders one representation, never a mix of both.

### Entry points

A `config` surface names its entry point in `UiConfigSurfaceAttributes.EntryPoint`:

| `UiConfigEntryPoints` | Attributes | Served by |
| --- | --- | --- |
| `IntegrationConfig` (`integration-config`) | `IntegrationId`, `ConfigFlowSessionId` | `IUiConfigFlow.CreateUiSessionAsync` |
| `ActionConfig` (`action-config`) | `ActionId`, `Parameters` | `IUiConfigurableActionDefinition.CreateConfigurationSessionAsync` |
| `FolderViewConfig` (`folder-view-config`) | `FolderId`, `FolderViewId`, `FolderViewConfiguration` | Your `IUiProvider` - see [Folder views](https://docs.macro-deck.app/ui/views/folder-views/) |
| `ScreenSaverConfig` (`screensaver-config`) | `DeviceId`, `ScreenSaverId`, `ScreenSaverConfiguration` | Your `IUiProvider` - see [Screensavers](https://docs.macro-deck.app/ui/views/screensavers/#configuration) |
| `WidgetConfig` (`widget-config`) | `WidgetId`, `WidgetType`, `WidgetData`, `WidgetWidth`, `WidgetHeight` | Your `IUiProvider` - see [Configuring a widget](https://docs.macro-deck.app/ui/views/widget-configuration/) |

Out of process, `MacroDeck.Plugin.Hosting` routes `integration-config` and `action-config` to the flow or
action first; if that target does not exist, serves no tree or declines, it falls through to your
`IUiProvider`s. Folder views and widgets have no declared field list, so their rules differ - see their
pages.

### See also

- [Setup flows](https://docs.macro-deck.app/features/setup-flows/)
- [Actions](https://docs.macro-deck.app/features/actions/)
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)
- [Configuring a widget](https://docs.macro-deck.app/ui/views/widget-configuration/)

## Custom views

> Source: https://docs.macro-deck.app/ui/views/custom/
>
> A complete "now playing" folder view, from composed components through a served surface to a headless test.

A "now playing" folder view, end to end: the view, the provider that serves it, previews and a test.

### Example

```csharp
public static class NowPlayingView
{
    public static UiElement Build(INowPlayingService service)
    {
        var track = service.CurrentTrack; // UiState<TrackInfo?>, owned by the service

        return new UiStack
        {
            Key = "now-playing",
            Padding = 0.06,
            Gap = 0.04,
            Children =
            [
                new UiImage { Key = "art", Source = UiValue.From(() => track.Value?.Artwork!), Size = 0.6 },
                new UiTextRun { Key = "title", Text = UiText.From(() => track.Value?.Title), Size = 0.12 },
                new UiProgressBar
                {
                    Key = "progress",
                    Value = UiValue.From(() => track.Value?.Progress!),
                    Thickness = 0.05,
                },
                new UiButton
                {
                    Key = "skip",
                    Justify = "center",
                    Events = [UiEventHandler.OnAsync(UiComponentEvents.Press, service.SkipAsync)],
                    Children = [new UiTextRun { Key = "label", Text = Strings.NowPlaying.Skip(), Size = 0.12 }],
                },
            ],
        };
    }
}
```

`Progress` is a `UiProgressReference` (for example `UiProgressReference.Advancing(positionMs, anchor,
durationMs)`): each reader advances it against its own clock, so you push no patch every second. That is
why the bar is `macrodeck.progress-bar` rather than a `ui.*` component - see
[The progress family](https://docs.macro-deck.app/ui/components/progress/) and [the UI overview](https://docs.macro-deck.app/ui/).

### Serving it on a folder surface

```csharp
public sealed class NowPlayingUiProvider : IUiProvider
{
    private readonly INowPlayingService _service;

    public NowPlayingUiProvider(INowPlayingService service) => _service = service;

    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
        [new() { Kind = UiSurfaceKinds.Folder, SessionMode = UiSessionModes.Shared }];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        if (request.Surface.Kind != UiSurfaceKinds.Folder)
        {
            return Task.FromResult<IUiSession?>(null);
        }

        var view = new UiView(request.Surface, NowPlayingView.Build(_service));
        return Task.FromResult<IUiSession?>(new ViewSession(view));
    }
}
```

`ViewSession` forwards `BuildTree`, `DrainPatches`, `Changed`, `Faulted` and `Dispatch` to the `UiView`
and disposes the view when the session closes, which matters here: the service's state outlives every
session, and an undisposed view reading it would never be released - see
[Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example) for it, the lifecycle and the limits. A folder only
opens this surface once your integration has registered the view through `IFolderViewProvider`; when you
offer more than one folder view, check `UiFolderSurfaceAttributes.ViewId` and decline the others. See
[Folder views](https://docs.macro-deck.app/ui/views/folder-views/).

### Previewing it

```csharp
internal static class NowPlayingViewPreviews
{
    [UiPreview("Playing", Profile = UiPreviewProfiles.Widget)]
    public static UiElement Playing() => NowPlayingView.Build(new MockNowPlayingService
    {
        CurrentTrack = new UiState<TrackInfo?>(new TrackInfo(
            "Nightcall",
            Artwork: null,
            UiProgressReference.Advancing(42_000, DateTimeOffset.UtcNow, durationMs: 215_000))),
    });

    [UiPreview("Between tracks", Profile = UiPreviewProfiles.Widget)]
    public static UiElement BetweenTracks() => NowPlayingView.Build(new MockNowPlayingService());
}
```

See [Developer preview](https://docs.macro-deck.app/ui/views/developer-preview/) for the rules a `[UiPreview]` method follows and how
scenarios group.

### Testing it

```csharp
[Fact]
public async Task Pressing_skip_invokes_the_service()
{
    var service = new MockNowPlayingService();
    var host = UiTestHost.Render(NowPlayingView.Build(service));

    host.ById("skip").Raise(UiComponentEvents.Press);
    await host.SettleAsync();

    Assert.True(service.SkipWasCalled);
}

[Fact]
public void Title_shows_the_current_track()
{
    var service = new MockNowPlayingService
    {
        CurrentTrack = new UiState<TrackInfo?>(new TrackInfo(
            "Nightcall", Artwork: null, UiProgressReference.Halted(0, DateTimeOffset.UtcNow, durationMs: 215_000))),
    };
    var host = UiTestHost.Render(NowPlayingView.Build(service));

    Assert.NotEmpty(host.ByText("Nightcall"));
}
```

`MacroDeck.Ui.Testing` renders a view with no browser and no running host.

| Task | `UiTestHost` / `UiTestNode` |
| --- | --- |
| Query rendered nodes | `ById`, `FindById`, `ByType`, `SingleByType`, `ByText` |
| Choose the box a [responsive](https://docs.macro-deck.app/ui/components/responsive/) view is drawn in | `SetBox(widthCells, heightCells)` - `ByType`, `SingleByType` and `ByText` then see only the layout drawn for it, `ById` still reaches every layout |
| Simulate events | `Raise(name)`, `Change(value)`, `Activate()`, `Submit()` |
| Wait for async handlers and loads | `SettleAsync()` |
| Inspect the tree and emitted patches | `Tree`, `Revision`, `Patches`, `LastPatch`, `Describe()`, `DescribePatches()` |
| Snapshot public view state | `ToCanonicalJson()` |

Test observable UI behaviour, not the internals of dependency tracking.

### See also

- [Folder views](https://docs.macro-deck.app/ui/views/folder-views/)
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)
- [Developer preview](https://docs.macro-deck.app/ui/views/developer-preview/)
- [Testing](https://docs.macro-deck.app/features/testing/)

## Developer preview

> Source: https://docs.macro-deck.app/ui/views/developer-preview/
>
> Registering [UiPreview] scenarios so Developer Tools can render a view in states that are hard to reach live.

Mark static methods with `[UiPreview]` and Developer Tools renders your view in states that are hard to
reach live.

### Example

```csharp
using MacroDeck.Ui.Dsl;
using MacroDeck.Ui.Previews;

internal static class WeatherViewPreviews
{
    [UiPreview("Sunny", Profile = UiPreviewProfiles.Widget)]
    public static UiElement Sunny() => WeatherView.Build(new MockWeatherService { City = "Vienna" });

    [UiPreview("Offline", Profile = UiPreviewProfiles.Widget)]
    public static UiElement Offline() => WeatherView.Build(new MockWeatherService { Offline = true });

    [UiPreview("Long city name", Profile = UiPreviewProfiles.Widget)]
    public static UiElement LongName()
        => WeatherView.Build(new MockWeatherService { City = "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch" });
}
```

Developer Tools lists the three scenarios under `WeatherView`, renders each through the same renderer the
app uses, and lets you resize the surface freely while it re-lays-out. Good candidates: disconnected,
empty, mid-load, failing, and a translation three times longer than the English.

### Writing a scenario

```csharp
[UiPreview("Offline")]
public static UiElement Offline() => WeatherView.Build(new MockWeatherService { Offline = true });
```

The method must be `static`, take no parameters, and return a `UiElement`, a `UiView` or a `UiPreview`.
Nothing is injected: a scenario builds its own mocks, and nothing reaches the real service.

A returned `UiView` belongs to the preview, which disposes it when the preview ends. Build a new one on
every call rather than returning a cached instance, or the next open gets a view that ignores every event.

### Grouping and profile

```csharp
[UiPreview("Long text", View = "WeatherDetailsView", Profile = UiPreviewProfiles.Config)]
```

| Member | Default | Meaning |
| --- | --- | --- |
| `Scenario` (constructor) | - | The scenario's name. Required, not blank. |
| `View` | The declaring type's name without a trailing `Previews` (`WeatherViewPreviews` becomes `WeatherView`) | The view the scenario groups under. |
| `Profile` | `UiPreviewProfiles.Config` (`config`) | The component namespace the tree is authored in: `config` or `widget`. It only sets up the canvas before the first tree arrives; the tree decides how it renders. |

### Releasing what a mock owns

```csharp
[UiPreview("Live feed", Profile = UiPreviewProfiles.Widget)]
public static UiPreview LiveFeed()
{
    var feed = new MockWeatherFeed();

    return UiPreview.Of(WeatherView.Build(feed), feed);
}
```

Opening, switching, refreshing and closing a preview each end the previous session. Hand anything that
must be stopped - a timer, a subscription, a fake connection - to `UiPreview.Of` as an `IDisposable` or
`IAsyncDisposable`, and Macro Deck disposes it when the preview ends. A scenario that only builds a tree
from plain data returns the element and never mentions `UiPreview`.

### What a preview cannot affect

| Fact | Consequence |
| --- | --- |
| Discovery reads metadata only. | A scenario runs only when someone opens it; declaring one costs a running host nothing. |
| A preview renders on its own `developer-preview` surface. | No provider you wrote for `config`, `widget`, `dialog` or `folder` is ever asked to serve one. |
| A malformed `[UiPreview]` method (not static, takes parameters, wrong return type) is skipped and reported in Developer Tools. | Discovery never fails, so one bad preview cannot take down your real surfaces. |
| A scenario that throws when opened fails only that preview. | Other previews and sessions carry on. |
| Listing and opening previews require an admin session. | Previews are not reachable by deck clients. |

### Iterating on a preview

Open a scenario once and leave it open while you change the code. Developer Tools keeps it on screen and brings
it back after a reload.

| You change | What updates | How |
| --- | --- | --- |
| A plugin scenario or view, under `dotnet watch` or your IDE's Hot Reload | The open preview, in place | The SDK rebuilds the scenario and sends its new tree. No restart, and the preview keeps its session. |
| Any plugin code, under `dotnet watch` or your IDE's Hot Reload | Every other open view of the plugin: deck widgets, widget, action and integration configuration, folder views, screensavers | Macro Deck opens each view again and your provider builds it with the new code. A configuration editor keeps the unsaved changes. See [Real views](#real-views). |
| A plugin change Hot Reload cannot apply, or a plain rebuild and restart | The open preview, once the plugin is back | The last tree stays on screen, dimmed, with a notice that the plugin is not connected. The preview reopens by itself when the plugin reconnects. |
| A scenario that no longer exists (renamed or removed) | A notice instead of the preview | Pick the scenario again from the list, which refreshes by itself. |
| A built-in Macro Deck view | The open preview, after the host restarts | The preview reopens once Macro Deck is back. |
| Nothing, but the same scenario is opened in a second window | The second window | The first window says the preview was closed. Refresh takes it back. Different scenarios can stay open side by side. |

The selected scenario and the canvas size are part of the Developer Tools address, so reloading the window
brings you back to the same scenario at the same size.

A component view on the canvas is laid out the way a deck tile is: each preset cell is one deck cell, so a
[`UiResponsive`](https://docs.macro-deck.app/ui/components/responsive/) switches layouts at the same sizes it does on the deck. A folder
view or a dialog in the app is laid out in CSS pixels instead, 120 of them to a cell, so check its thresholds
there too.

`macrodeck-plugin run --project <path> --watch` sets this loop up against the running Macro Deck; see
[Watching for changes](https://docs.macro-deck.app/cli/run/#watching-for-changes). `dotnet watch run` with the
[debugging launch profile](https://docs.macro-deck.app/guides/debugging/#live-reload-while-you-work) does the same from your IDE.

A reload rebuilds the scenario from its code, so what the scenario creates starts over: its mock data, and
anything you typed or selected inside the preview. Put the state you want to look at into the scenario itself.

A plugin whose first-ever scenario is added by Hot Reload does not declare a UI yet, so that scenario appears
after the next restart.

### Rendering previews to PNG

`macrodeck-plugin preview render --project <path> --size 200x200 --output previews` draws every widget
scenario to a PNG without a running Macro Deck, which is how store images are regenerated after a redesign. See
[`preview`](https://docs.macro-deck.app/cli/preview/). Configuration views are not drawn.

### Real views

A preview is not the only view that follows Hot Reload. Every view your plugin serves in the running app is
opened again after each update, whichever code changed, so you can work on a widget or a configuration view
with real data instead of a scenario:

- In the desktop app, and for widgets on a deck, the view keeps showing its last tree until the new one
  arrives. A folder view or screensaver in the web client shows its loading state in between.
- A widget, action or integration configuration editor keeps the unsaved changes: Macro Deck opens the new
  session with the draft it holds, or, for an integration's setup, sends the new session a `change` event for
  each field the user edited.
- State that lives in the old session is gone, such as the open tab. State your provider keeps outside the
  session survives.
- An open dialog is left alone, because ending it would cancel the action waiting for its answer. The next
  dialog uses the new code.
- A view whose new code throws while it is created shows as unavailable after a few attempts. Open it again
  once the code is fixed.
- A view that was still being created while the update landed may keep the old code. Open it again.
- If `dotnet watch` reports `Failed to load type` warnings for an update, restart the plugin (Ctrl+R in
  `dotnet watch`, or restart it from your IDE). Hot Reload still reports success, but the process can no longer
  build views reliably, so views stop updating or stay empty.

### Over the plugin protocol

`describe` lists your scenarios in `previews`. `MacroDeck.Plugin.Hosting` scans the assemblies of your
registered integrations plus the entry assembly, lazily. A `developer-preview` surface names one scenario
by id in its attributes; the SDK builds that scenario ahead of every production path and never consults
`IUiProvider`. See [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#over-the-plugin-protocol).

When .NET Hot Reload updates the plugin, `MacroDeck.Plugin.Hosting` builds every open preview's scenario
again, sends the new tree as an unrequested `ui/snapshot`, and sends `state.update` for `ui` so the host
re-reads `describe` and the list picks up new or removed scenarios. A scenario that throws on rebuild faults
only its own preview. Every other open session except a `dialog` gets a `ui/reload` (see
[Host callbacks](https://docs.macro-deck.app/reference/websocket/#ui)), and the host ends it so that clients open it again. Nothing
changes for a plugin that is not being hot reloaded.

### See also

- [`macrodeck-plugin preview`](https://docs.macro-deck.app/cli/preview/) - render the widget scenarios to PNG
- [Custom views](https://docs.macro-deck.app/ui/views/custom/) - a view with previews and tests
- [Views and surfaces](https://docs.macro-deck.app/ui/views/)

## Folder views

> Source: https://docs.macro-deck.app/ui/views/folder-views/
>
> Replacing a folder's whole surface with a Macro Deck UI view, and what Macro Deck keeps for itself.

A folder view replaces a folder's widget grid with your own tree - a dashboard, a mixer, a monitoring
panel.

### Example

```csharp
public sealed class MonitorIntegration : IPluginIntegration, IFolderViewProvider, IUiProvider
{
    private string? _dashboard;

    public string ProviderName => "System monitor";

    public async Task InitializeAsync(IFolderViewProviderContext context, CancellationToken cancellationToken = default)
    {
        var registration = await context.RegisterFolderViewAsync(
            new FolderViewDescriptor(
                "dashboard",
                MyStrings.DashboardName(),
                MyStrings.DashboardDescription(),
                HasConfiguration: true),
            cancellationToken);

        _dashboard = registration.FolderViewId; // "com.example.monitor::dashboard"
    }

    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
    [
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Folder, SessionMode = UiSessionModes.Shared },
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Config, SessionMode = UiSessionModes.Exclusive },
    ];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        var surface = request.Surface;
        var attributes = surface.Attributes;

        UiElement? root = surface.Kind switch
        {
            UiSurfaceKinds.Folder
                when attributes[UiFolderSurfaceAttributes.ViewId].GetString() == _dashboard
                => Dashboard(attributes[UiFolderSurfaceAttributes.Configuration]),
            UiSurfaceKinds.Config
                when attributes[UiConfigSurfaceAttributes.EntryPoint].GetString() == UiConfigEntryPoints.FolderViewConfig
                && attributes[UiConfigSurfaceAttributes.FolderViewId].GetString() == _dashboard
                => DashboardConfig(attributes[UiConfigSurfaceAttributes.FolderViewConfiguration]),
            _ => null,
        };

        return Task.FromResult<IUiSession?>(root is null ? null : new ViewSession(new UiView(surface, root)));
    }

    private static UiStack Dashboard(JsonElement configuration) => new()
    {
        Key = "dashboard",
        Direction = UiComponentDirections.Horizontal,
        Gap = 0.04,
        Padding = 0.04,
        Children =
        [
            new UiClockDial { Key = "clock", Value = UiValue.Of(UiTimeReference.InZone("Europe/Berlin")), Fill = true },
            Card("cpu", "CPU"),
            Card("gpu", "GPU"),
        ],
    };

    // IPluginIntegration members, Card and DashboardConfig omitted.
}
```

*[Image: A wide folder view dashboard with three cards: an analogue clock, a CPU history graph at 42 % and a GPU history graph at 67 %]*

`ViewSession` is the adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example). A folder stays an ordinary
folder: its view is part of its configuration, picked like its name and changeable later without
touching anything else. Macro Deck's built-in view is the widget grid.

### Registering the view

```csharp
var registration = await context.RegisterFolderViewAsync(descriptor, cancellationToken);
// registration.FolderViewId == "com.example.monitor::dashboard"
```

The qualified id is what a folder stores. **Keep it stable across releases** - renaming it strands every
folder already using the view.

Registration is a push: register when you are ready, withdraw when you are not. `GetFolderViews()` only
lets Macro Deck recover its catalog after a reconnect, and is optional. There is no `ShutdownAsync` here:
release what `InitializeAsync` acquired in your integration's own `ShutdownAsync`, and Macro Deck
withdraws your views itself.

### Drawing the folder

```csharp
var viewId = attributes[UiFolderSurfaceAttributes.ViewId].GetString();
var configuration = attributes[UiFolderSurfaceAttributes.Configuration];
```

A `folder` surface carries `folderId`, `folderName`, `viewId` and `configuration`. The configuration
travels with the request because you cannot read Macro Deck's stored folders. Decline a view you do not
serve rather than guessing from the configuration's shape.

The tree is built from the same [components](https://docs.macro-deck.app/ui/components/) as a deck widget, with two consequences:

- **A folder view does not scroll.** Everything has to fit the box you are given.
- **Lengths are fractions of the box's smaller side.** A folder view is usually far wider than tall, so
  sizes track its height - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).
- **A different layout per screen** - a phone in portrait, a tablet in landscape - comes from
  [`UiResponsive`](https://docs.macro-deck.app/ui/components/responsive/), which chooses by the folder view's own box.

### Configuration

```csharp
UiSurfaceKinds.Config
    when attributes[UiConfigSurfaceAttributes.EntryPoint].GetString() == UiConfigEntryPoints.FolderViewConfig
```

With `HasConfiguration`, picking your view opens a `config` surface with the `folder-view-config` entry
point, inside the folder's own dialog rather than as a flow of its own. Build it with the
[configuration view](https://docs.macro-deck.app/ui/views/configuration/). It carries `folderId`, `folderViewId` and
`folderViewConfiguration`; `folderViewId` is the view being configured, which is not always the one the
folder currently stores - the user is choosing. The values are stored with the folder and handed back on
every later `folder` surface.

To let the user choose a folder of files for the view, use a
[path input](https://docs.macro-deck.app/ui/views/configuration/#letting-the-user-pick-a-file-folder-or-image).

### Navigation is Macro Deck's

```csharp
new FolderViewDescriptor("mixer", "Mixer", Navigation: FolderViewNavigation.Hidden);
```

Macro Deck draws the back button and it always drives Macro Deck's own navigation stack - you cannot
redirect it and need not draw one. `Hidden` says your view has its own way out; it is a preference, not a
guarantee. Macro Deck still shows its button when the view is the only thing on screen and there is
somewhere to go back to, so a broken view can never trap anyone. At a root folder it draws no button,
whatever you asked for.

### When your integration is not running

```csharp
await context.UnregisterFolderViewAsync("dashboard", cancellationToken);
```

A folder keeps its view id and configuration whether or not anything provides them. Macro Deck renders a
placeholder naming the missing view, with links to the integrations page and the folder's settings. Nothing
is cleared, so re-enabling your integration brings the folder back exactly as it was - including after an
archive import on a machine without your plugin. Unregistering only stops the view being offered.

### Where a folder view can be chosen

The choice appears - in a folder's context menu and when creating one - only when more than one view is on
offer and the device claiming the profile can render one (`LayoutVisualCapabilities.CustomFolderViews`, see
[Layout providers](https://docs.macro-deck.app/features/layouts/)). A profile no device claims keeps the choice. So a registered view
may not be an option on some profile; nothing selects it there, so nothing opens a session for it.

### Over the plugin protocol

Registration is driven from the plugin side, so the host-to-provider direction of the
`folder-view-provider` capability only has to describe the provider and re-read its catalog after a
reconnect:

| Operation | Purpose |
| --- | --- |
| `describe` | The provider's declared name and its current catalog. |
| `folder-views` | The provider's current folder view catalog, re-read after a reconnect. |

Registering and withdrawing a view travels the other way as the `folder-views` host API:

| Operation | Purpose |
| --- | --- |
| `register` | Registers a folder view, or replaces one already registered under the same provider-local id. |
| `unregister` | Withdraws a folder view. Folders still using it keep their stored id and configuration and show a placeholder until it returns. |

The views themselves are served over the `ui` capability, like every other Macro Deck UI surface.

### See also

- [Widget types](https://docs.macro-deck.app/ui/views/widget-types/) - the same registration shape, one level down.
- [Layout providers](https://docs.macro-deck.app/features/layouts/)
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)
- [Components](https://docs.macro-deck.app/ui/components/)

## Modal views

> Source: https://docs.macro-deck.app/ui/views/modal/
>
> Opening a dialog from an action, how it is sized, which node completes it, and what bounds the wait.

An action can put a dialog on the client that ran it and, when it needs one, wait for the answer.

### Example

```csharp
public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
{
    if (context.Ui is null)
    {
        return ActionResult.Success();
    }

    var result = await context.Ui.ShowModalAsync<string>(
        context.OriginClientId,
        new ModalDefinition { ViewId = "device-picker", Title = MyStrings.SelectDevice() },
        context.CancellationToken);

    if (result.Cancelled)
    {
        return ActionResult.Success();
    }

    await TransferAsync(result.Value!, context.CancellationToken);
    return ActionResult.Success();
}
```

The dialog itself comes from your `IUiProvider`:

```csharp
public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
[
    new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Dialog, SessionMode = UiSessionModes.Exclusive },
];

public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
{
    var surface = request.Surface;
    if (surface.Kind != UiSurfaceKinds.Dialog
        || surface.Attributes[UiDialogSurfaceAttributes.ViewId].GetString() != "device-picker")
    {
        return Task.FromResult<IUiSession?>(null);
    }

    var picker = new UiList
    {
        Key = "devices",
        Gap = UiSize.FromBasis(0.015),
        Children = [.. _devices.Select(device => new UiButton
        {
            Key = device.Id,
            Answer = UiValue.Of(device.Id),
            Events = [UiEventHandler.On(UiComponentEvents.Press, () => { })],
            Children =
            [
                new UiTextRun { Key = "name", Text = device.Name, Size = UiSize.FromBasis(0.038) },
                new UiTextRun { Key = "detail", Text = device.Detail, Size = UiSize.FromBasis(0.03), Role = UiComponentTextRoles.Secondary },
            ],
        })],
    };

    return Task.FromResult<IUiSession?>(new ViewSession(new UiView(surface, picker)));
}
```

*[Image: A device picker dialog: a list of three button rows, each with a device icon, a name and a grey status line]*

`ViewId` names one of your dialogs; Macro Deck opens a `dialog` surface for it against your provider.
`ViewSession` is the adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example). A `null` `context.Ui` means
the run was started by the backend - there is nobody to ask, which is not a failure.

### The dialog surface

A `dialog` surface carries `modalId`, `viewId` and whatever `Data` the action passed
(`UiDialogSurfaceAttributes`). Decline a `viewId` you do not serve rather than guessing. A dialog is
`exclusive`: it belongs to one client, so unlike a deck widget its tree may carry entered values.

### Completing a modal

```csharp
Answer = UiValue.Of(device.Id),
Events = [UiEventHandler.On(UiComponentEvents.Press, () => { })],
```

A pressed container that carries an `Answer` settles the dialog with that string. The client settles it
directly, so your session never sees that press. `Answer` works on any container that declares `press`;
it is an identifier, not a payload, so look anything else up on your side by it. At the protocol level,
a tree event named `modal.complete` also settles the dialog, with its payload as the value. Every other
event is routed to your session as usual.

`ShowModalAsync<T>` deserializes the value into `T`; a value that does not fit `T` is logged and reads as
a cancellation.

### Showing without waiting

```csharp
var opened = await context.Ui.ShowModalAsync(
    context.OriginClientId,
    new ModalDefinition
    {
        ViewId = "now-playing",
        Data = new Dictionary<string, JsonElement> { ["track"] = JsonSerializer.SerializeToElement("Nightcall") },
    },
    context.CancellationToken);
```

The non-generic overload is for a modal that shows something rather than asks something. It returns as
soon as the modal is open, with `true` if it opened.

### How a dialog is sized

Lengths are fractions of the box Macro Deck hands the dialog - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). The box
is a fixed size and does not grow to your tree, because a box that grew would feed the content's height
back into the basis it is measured against. A tree taller than its box scrolls vertically. It never
scrolls sideways: a tree wider than its box is an authoring mistake, and Macro Deck clips it.

The box differs between a desktop window and a phone. [`UiResponsive`](https://docs.macro-deck.app/ui/components/responsive/) lets a
dialog lay itself out differently in a narrow box.

### What bounds the wait

Check `Cancelled` before touching `Value`. **Everything that is not an explicit completion is a
cancellation** - the user dismissing it, the client disconnecting, the flow being cancelled, the session
faulting, the run reaching Macro Deck's maximum flow duration. So awaiting a modal cannot hang, and you
never have to tell "cancelled" from "never answered".

A flow that runs longer than a few seconds detaches and keeps running, which is what makes waiting on a
person viable. It still occupies one of the host's concurrent run slots while its modal is open, and a
client can only show a few modals at once. Do not hold a modal open as a substitute for a deck widget.

### See also

- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/) - including the `modal.result` protocol operation.
- [List](https://docs.macro-deck.app/ui/components/list/)
- [Button](https://docs.macro-deck.app/ui/components/button/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)

## Screensavers

> Source: https://docs.macro-deck.app/ui/views/screensavers/
>
> Offering what a device shows after it has sat idle, and what Macro Deck does with the touch that wakes it.

A screensaver is a Macro Deck UI tree a device shows in place of its deck after it has sat idle for the
time its settings name - a clock, the current track, a photo frame. The first touch brings the deck back.

### Example

```csharp
public sealed class PhotoIntegration : IPluginIntegration, IScreenSaverProvider, IUiProvider
{
    private string? _photos;

    public string ProviderName => "Photo frame";

    public async Task InitializeAsync(IScreenSaverProviderContext context, CancellationToken cancellationToken = default)
    {
        var registration = await context.RegisterScreenSaverAsync(
            new ScreenSaverDescriptor(
                "photos",
                MyStrings.PhotosName(),
                MyStrings.PhotosDescription(),
                HasConfiguration: true),
            cancellationToken);

        _photos = registration.ScreenSaverId; // "com.example.photos::photos"
    }

    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
    [
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.ScreenSaver, SessionMode = UiSessionModes.Shared },
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Config, SessionMode = UiSessionModes.Exclusive },
    ];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        var surface = request.Surface;
        var attributes = surface.Attributes;

        UiElement? root = surface.Kind switch
        {
            UiSurfaceKinds.ScreenSaver
                when attributes[UiScreenSaverSurfaceAttributes.ScreenSaverId].GetString() == _photos
                => Photos(attributes[UiScreenSaverSurfaceAttributes.Configuration]),
            UiSurfaceKinds.Config
                when attributes[UiConfigSurfaceAttributes.EntryPoint].GetString() == UiConfigEntryPoints.ScreenSaverConfig
                && attributes[UiConfigSurfaceAttributes.ScreenSaverId].GetString() == _photos
                => PhotosConfig(attributes[UiConfigSurfaceAttributes.ScreenSaverConfiguration]),
            _ => null,
        };

        return Task.FromResult<IUiSession?>(root is null ? null : new ViewSession(new UiView(surface, root)));
    }

    private UiStack Photos(JsonElement configuration)
    {
        var album = configuration.TryGetProperty("album", out var value) ? value.GetString() : null;

        return new UiStack
        {
            Key = "photos",
            Justify = UiComponentJustify.Center,
            Align = UiComponentAlignments.Center,
            Children = [new UiImage { Key = "photo", Source = UiValue.Of(NextPhoto(album)), Size = 0.9 }],
        };
    }

    // IPluginIntegration members, NextPhoto and PhotosConfig omitted.
}
```

`ViewSession` is the adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example). The shape is
[folder views](https://docs.macro-deck.app/ui/views/folder-views/) one level up: a provider registers descriptors to be listed in a
device's settings, and serves the screensaver through its `IUiProvider` when a device opens the surface.
Macro Deck ships a clock and a now-playing screensaver through the very same contract.

### Registering a screensaver

```csharp
var registration = await context.RegisterScreenSaverAsync(descriptor, cancellationToken);
// registration.ScreenSaverId == "com.example.photos::photos"
```

The qualified id is what a device stores. **Keep it stable across releases** - renaming it strands every
device already using the screensaver. Registration is a push: register when you are ready, withdraw when
you are not. `GetScreenSavers()` only lets Macro Deck recover its catalog after a reconnect, and is
optional. There is no `ShutdownAsync` here: release what `InitializeAsync` acquired in your integration's
own `ShutdownAsync`, and Macro Deck withdraws your screensavers itself.

Against a host older than this capability the registration answers with an empty `ScreenSaverId` and
nothing is offered; the call does not throw, so the rest of your integration starts as usual.

### Drawing the screensaver

```csharp
var screenSaverId = attributes[UiScreenSaverSurfaceAttributes.ScreenSaverId].GetString();
var configuration = attributes[UiScreenSaverSurfaceAttributes.Configuration];
```

A `screensaver` surface carries `deviceId`, `screenSaverId` and `configuration`. The configuration travels
with the request because you cannot read Macro Deck's stored devices. Decline a screensaver you do not
serve rather than guessing from the configuration's shape. The tree fills the whole display; lengths are
fractions of the display's smaller side, so a full-screen clock is drawn with the same numbers as a
widget-sized one - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). For a different arrangement in portrait and landscape,
use [`UiResponsive`](https://docs.macro-deck.app/ui/components/responsive/) with aspect conditions.

**Movement has to be cheap.** A screensaver often runs on a tablet or a Raspberry Pi for hours. Move
things by rewriting one bound property every minute, which is one small patch, rather than animating;
let time advance through a [time reference](https://docs.macro-deck.app/ui/components/time/), which costs no patch at all.

### Input

By default a screensaver is inert: the first touch, click or key press dismisses it, and Macro Deck
swallows that input so it never presses the button that happens to be under the finger. Nothing reaches
your tree.

```csharp
new ScreenSaverDescriptor("player", MyStrings.PlayerName(), Interactive: true);
```

With `Interactive`, a press on a node that claims it - a `ui.button`, a slider - is delivered to your
session as an event; input anywhere else still dismisses the screensaver, and so does Escape.

### Configuration

With `HasConfiguration`, a device's screensaver settings offer an Options button for your screensaver. It
opens a `config` surface with the `screensaver-config` entry point in its own dialog. Build it with the [configuration view](https://docs.macro-deck.app/ui/views/configuration/). It
carries `deviceId`, `screenSaverId` and `screenSaverConfiguration`; the values are stored with the device
and handed back on every later `screensaver` surface.

### Device settings, and the idle timer

A user turns the screensaver on per device, picks the idle time and the screensaver. New devices start
with it off, so nothing changes for an existing setup. The idle timer runs on the device, never on the
host: the host stores the settings and serves the surface, so a network hiccup can neither delay waking
up nor start a screensaver on its own. The web client keeps the display awake while a screensaver shows.

### When your integration is not running

A device keeps its screensaver id and configuration whether or not anything provides them. Macro Deck
shows its built-in clock instead, so a device is never left on a blank screen, and re-enabling your
integration restores the selection exactly as it was. Withdrawing only stops the screensaver being offered.

### Over the plugin protocol

Registration is driven from the plugin side, so the host-to-provider direction of the
`screensaver-provider` capability only has to describe the provider and re-read its catalog after a
reconnect:

| Operation | Purpose |
| --- | --- |
| `describe` | The provider's declared name and its current catalog. |
| `screensavers` | The provider's current screensaver catalog, re-read after a reconnect. |

Registering and withdrawing a screensaver travels the other way as the `screensavers` host API:

| Operation | Purpose |
| --- | --- |
| `register` | Registers a screensaver, or replaces one already registered under the same provider-local id. |
| `unregister` | Withdraws a screensaver. Devices still using it keep their stored id and configuration and show the clock until it returns. |

The screensavers themselves are served over the `ui` capability, like every other Macro Deck UI surface.
The manifest permission for the host API is `host:screensavers`.

### At a glance

| Member | Package | What it is |
| --- | --- | --- |
| `IScreenSaverProvider` | SDK | Implemented by an integration that offers screensavers. |
| `ScreenSaverDescriptor` | SDK | One screensaver: `Id`, `Name`, `Description`, `HasConfiguration`, `Interactive`, `Metadata`. |
| `IScreenSaverProviderContext` | SDK | `RegisterScreenSaverAsync` and `UnregisterScreenSaverAsync`. |
| `ScreenSaverRegistration` | SDK | What registering returns: the qualified `ScreenSaverId` and its owner. |
| `UiSurfaceKinds.ScreenSaver` | UI model | The `screensaver` surface kind to declare. |
| `UiScreenSaverSurfaceAttributes` | UI model | `DeviceId`, `ScreenSaverId` and `Configuration` on a `screensaver` surface. |
| `UiConfigEntryPoints.ScreenSaverConfig` | UI model | The `screensaver-config` entry point of a `config` surface. |
| `UiConfigSurfaceAttributes.ScreenSaverId`, `.ScreenSaverConfiguration`, `.DeviceId` | UI model | Which screensaver is being configured and its current values. `DeviceId` is informational: never authorize anything by it. |
| `PluginPermissions.HostScreenSavers` | Packaging | The `host:screensavers` manifest permission. |
| `FakeScreenSaverProviderContext`, `ScreenSaverProviderTestClient` | Plugin testing | See [Testing screensavers](https://docs.macro-deck.app/features/testing/#testing-screensavers). |

### See also

- [Folder views](https://docs.macro-deck.app/ui/views/folder-views/) - the same registration shape, for a whole folder.
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)
- [Components](https://docs.macro-deck.app/ui/components/)

## Serving a view

> Source: https://docs.macro-deck.app/ui/views/sessions/
>
> IUiProvider, the session lifecycle every surface shares, the protocol limits, and what a refused update looks like.

Implement `MacroDeck.Sdk.Ui.IUiProvider` to serve a view; Macro Deck owns the session it renders in.

### Example

A deck widget that counts presses, shared by every device showing it:

```csharp
using MacroDeck.Sdk.Ui;
using MacroDeck.Ui.Components;
using MacroDeck.Ui.Dsl;
using MacroDeck.Ui.Model.Events;
using MacroDeck.Ui.Model.Nodes;
using MacroDeck.Ui.Model.Patches;
using MacroDeck.Ui.Model.Surfaces;
using MacroDeck.Ui.Runtime;

public sealed class CounterUiProvider : IUiProvider
{
    private readonly UiState<int> _count = new(0);

    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
        [new() { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared }];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        if (request.Surface.Kind != UiSurfaceKinds.Widget)
        {
            return Task.FromResult<IUiSession?>(null);
        }

        var root = new UiButton
        {
            Key = "counter",
            Events = [UiEventHandler.On(UiComponentEvents.Press, () => _count.Value++)],
            Children = [new UiTextRun { Key = "value", Text = UiText.From(() => _count.Value.ToString()), Size = 0.4 }],
        };

        return Task.FromResult<IUiSession?>(new ViewSession(new UiView(request.Surface, root)));
    }
}

public sealed class ViewSession : IUiSession
{
    private readonly UiView _view;

    public ViewSession(UiView view)
    {
        _view = view;
        _view.Changed += (_, _) => Changed?.Invoke(this, EventArgs.Empty);
        _view.HandlerFaulted += (_, fault)
            => Faulted?.Invoke(this, new UiSessionFaultedEventArgs(fault.Exception.Message, fault.Exception));
    }

    public event EventHandler? Changed;

    public event EventHandler<UiSessionFaultedEventArgs>? Faulted;

    public UiTree BuildTree() => _view.Tree;

    public IReadOnlyList<UiPatch> DrainPatches() => _view.DrainPatches();

    public void Dispatch(UiEvent uiEvent) => _view.Dispatch(uiEvent);

    public ValueTask DisposeAsync()
    {
        _view.Dispose();
        return ValueTask.CompletedTask;
    }
}
```

`ViewSession` is the whole adapter between a `MacroDeck.Ui` `UiView` and `IUiSession`; the other pages
in this section reuse it. `IUiSession` itself speaks only `MacroDeck.Ui.Model` terms, so a provider can
serve a tree without the DSL.

Disposing the view is what lets a closed session go. `_count` belongs to the provider and outlives every
session, and a state keeps each view that reads it alive and flushes into it on every write. A session that
skips `_view.Dispose()` stays in memory for as long as the plugin runs, and so does every patch queued for
it. See [Disposing](https://docs.macro-deck.app/ui/concepts/reactive-updates/#disposing).

### Declaring surfaces

```csharp
public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
[
    new() { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared },
    new() { Kind = UiSurfaceKinds.Config, SessionMode = UiSessionModes.Exclusive },
];
```

Macro Deck reads `Surfaces` before anything is initialized, so it must be side-effect free and must not
depend on a live connection. Declaring a surface does not commit you to every session for it: return
`null` from `CreateSessionAsync` to decline one. The kind vocabulary is open (see
[Views and surfaces](https://docs.macro-deck.app/ui/views/)), so declining a kind you do not recognise is correct, not an error.

### The lifecycle every surface shares

| Step | What happens | Your side |
| --- | --- | --- |
| Open | The host asks for a session for one surface, carrying the UI model version it speaks (`request.UiModelVersion`). | Return a session or `null`. The session id is host-issued. |
| Snapshot | The host asks for a full tree when a client attaches and whenever it must resynchronise. | `BuildTree()` must describe the revision your emitted patches have reached. |
| Patches | You raise `Changed`; the host drains. | Coalescing several changes into one raise is fine - the host drains rather than counts. A patch dropped in `DrainPatches` is lost to every attached client. |
| Events | `Dispatch` delivers a client event, never concurrently for one session. | Reject an event by producing no patch. A throw faults the session. |
| Close | The host disposes the session - at any time: a client leaving for good, a limit trip, a fault, or .NET Hot Reload updating your plugin, after which clients open a new session. | Release what the session holds in `DisposeAsync`, including disposing its `UiView`. |

You never see who is attached, how many clients there are, or when one attaches: one code path serves one
deck or several.

The host relays your bytes, not your objects. A tree or patch is bounded and forwarded verbatim, so unknown
members, member order and number formatting reach the client exactly as you produced them.

### Limits

The `maxUi*` values are listed with every other protocol limit in
[Plugin WebSocket protocol](https://docs.macro-deck.app/reference/websocket/#limits-and-timeouts). The host advertises them in the
protocol descriptor and the session response - read them from there, never hard-code them.

| Limit | Measured as |
| --- | --- |
| Tree and patch size | UTF-8 bytes of the serialized payload. |
| Node count | Every node, including `fallback` subtrees. |
| Update rate and burst | Per session, not per provider - one busy view cannot starve another. |
| `maxUiResourceBytes` | Both a `UiResource`'s declared `byteLength` in a plugin's tree and the bytes the host's resource store accepts for one resource a plugin registers. A `byteLength` of `null` is accepted. |
| `maxUiResourceBytesPerPlugin` / `maxUiResourcesPerPlugin` | The bytes and the number of [resources](https://docs.macro-deck.app/ui/reference/resources/#registering-your-own-images) one plugin may have registered at once. |

### What a refused update looks like

Nothing is dropped silently - no client is ever left on a revision that will never advance.

| You send | The host | The client sees |
| --- | --- | --- |
| A patch over the byte limit, or too fast | Refuses it and asks you for a fresh tree. | That tree. |
| A patch whose `fromRevision` does not match the session | Refuses it and resyncs the same way. | Your current revision, through a full tree. |
| A patch with no operations, or one that does not advance the revision | Refuses it with `INVALID_PAYLOAD`. No resync - the revision never moved. | Nothing; it is not stale. |
| A tree over the byte, node or declared-resource limit | Ends the session with `PAYLOAD_TOO_LARGE`. Nothing smaller can supersede a tree. | The session ended. |
| Sustained overload after a resync | Ends the session with `RATE_LIMITED`. | The session ended; retryable. |

Out of process, each refusal is an error on that call's own `host.result` - the reply to the `host.invoke`
that carried the payload - so it is always attributable to the update that caused it.

### Over the plugin protocol

Out of process, the same contract is the `ui` capability kind. `MacroDeck.Plugin.Hosting` maps it onto
`IUiProvider`: register an integration that implements it and the SDK declares the kind, answers
`describe` from your `Surfaces`, and drives the snapshot, patch and fault callbacks from your session.
There is no capability handler to write.

Like the other provider-shaped capabilities, `ui` declares the single local id `provider` - the capability
*is* the plugin's one UI provider. The host invokes `kind: "ui", localId: "provider"`.

| Operation | Purpose |
| --- | --- |
| `describe` | The surfaces this provider serves, the UI model version it speaks, and the [preview scenarios](https://docs.macro-deck.app/ui/views/developer-preview/) it declares. `previews` is optional: a plugin built against an SDK that predates it omits the key, and the host reads that as none. |
| `session.open` | Open a session for one surface. The session id is host-issued; a provider never mints one. |
| `session.open` (config) | A `config` surface names its entry point in its surface attributes - `integration-config` with the config flow session, `action-config` with the action id and the instance's stored parameters, `folder-view-config` with the folder and its view, or `widget-config` with the widget id, type and stored configuration. `MacroDeck.Plugin.Hosting` routes `integration-config` and `action-config` to `IUiConfigFlow`/`IUiConfigurableActionDefinition` before it consults `IUiProvider`. |
| `session.open` (developer preview) | A `developer-preview` surface names one registered scenario in its surface attributes. `MacroDeck.Plugin.Hosting` builds that scenario and never consults `IUiProvider`, so a production provider is unreachable from a preview. |
| `session.snapshot` | Produce the current full tree. The tree does not return on the result - it arrives as a separate `host.invoke ui/snapshot`, so a first attach and a resync share one delivery path. A provider may also send `ui/snapshot` unasked to replace its whole tree, at any revision; later patches continue from that tree's revision. |
| `session.event` | A client acted on a node. `clientId` says which one, and is meaningful only for a shared session. A `pointer-move` still waiting to be sent is replaced by a newer one for the same node from the same client, and one the plugin could not take because it was busy or slow is dropped; see [Pointer streams and taps](https://docs.macro-deck.app/ui/components/modifier/#pointer-streams-and-taps). |
| `session.close` | The host is ending this session. |
| `modal.result` | How a modal this plugin opened ended. Host-to-plugin because a person, not a timeout, bounds the wait - see [Modal views](https://docs.macro-deck.app/ui/views/modal/). |

Trees, patches and faults travel the other way through the [`ui` host api](https://docs.macro-deck.app/reference/websocket/#host-callbacks).

### See also

- [Views and surfaces](https://docs.macro-deck.app/ui/views/)
- [Patches](https://docs.macro-deck.app/ui/reference/patches/)
- [Resources](https://docs.macro-deck.app/ui/reference/resources/)
- [Plugin hosting](https://docs.macro-deck.app/reference/plugin-hosting/)

## Configuring a widget

> Source: https://docs.macro-deck.app/ui/views/widget-configuration/
>
> Describing a widget's configuration as two named regions Macro Deck lays out, and reaching the editors the app already ships.

A widget's configuration is a `config` surface tree under the `widget-config` entry point, made of two
named regions Macro Deck lays out.

### Example

```csharp
public sealed class GaugeWidgetUiProvider : IUiProvider
{
    private const string GaugeWidgetType = "example.gauge";

    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
    [
        new() { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared },
        new() { Kind = UiSurfaceKinds.Config, SessionMode = UiSessionModes.Exclusive },
    ];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        var attributes = request.Surface.Attributes;
        if (request.Surface.Kind != UiSurfaceKinds.Config ||
            !attributes.TryGetValue(UiConfigSurfaceAttributes.EntryPoint, out var entryPoint) ||
            entryPoint.GetString() != UiConfigEntryPoints.WidgetConfig ||
            !attributes.TryGetValue(UiConfigSurfaceAttributes.WidgetType, out var widgetType) ||
            widgetType.GetString() != GaugeWidgetType)
        {
            return Task.FromResult<IUiSession?>(null);
        }

        attributes.TryGetValue(UiConfigSurfaceAttributes.WidgetData, out var data);
        var root = GaugeConfigView.Build(data);

        return Task.FromResult<IUiSession?>(new ViewSession(new UiView(request.Surface, root)));
    }
}

public static class GaugeConfigView
{
    public static UiElement Build(JsonElement data)
    {
        var label = new UiState<string>(ReadString(data, "label") ?? string.Empty);
        var variable = new UiState<string>(ReadString(data, "variable") ?? string.Empty);
        var maximum = new UiState<double>(100);
        var flows = new UiState<JsonElement>(data.ValueKind == JsonValueKind.Object &&
            data.TryGetProperty("flows", out var f) ? f : JsonSerializer.SerializeToElement(Array.Empty<object>()));

        return new UiWidgetConfiguration
        {
            Key = "root",
            Properties = new UiWidgetProperties
            {
                Key = "properties",
                Children =
                [
                    new UiStringInput { Key = "label", Label = Strings.Gauge.Label(), Binding = Bind.To(label) },
                    new UiVariablePickerInput
                    {
                        Key = "variable",
                        Label = Strings.Gauge.Variable(),
                        VariableTypes = UiValue.Of<IReadOnlyList<string>>(["Integer", "Float"]),
                        Binding = Bind.To(variable),
                    },
                    new UiNumberInput { Key = "maximum", Label = Strings.Gauge.Maximum(), Min = 1, Binding = Bind.To(maximum) },
                    UiWidgetAppearance.Section(data, UiWidgetAppearanceFields.BackgroundColor | UiWidgetAppearanceFields.Border),
                ],
            },
            Editor = new UiWidgetEditor
            {
                Key = "editor",
                Children = [new UiActionsListEditor { Key = "flows", Binding = Bind.To(flows), CanRun = true }],
            },
        };
    }

    private static string? ReadString(JsonElement data, string key)
        => data.ValueKind == JsonValueKind.Object && data.TryGetProperty(key, out var v) &&
           v.ValueKind == JsonValueKind.String ? v.GetString() : null;
}
```

A `UiState<JsonElement>` must hold a defined value: `default(JsonElement)` has no JSON form, so building the
view throws a `UiViewException` that names the node and property. Start from an empty array, as above.

`ViewSession` is the adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example). The built-in Clock widget
(`host/src/MacroDeckHost.Widgets/Clock/ClockWidgetConfigView.cs`) is a complete, larger example.

### The two regions

```csharp
new UiWidgetConfiguration
{
    Key = "root",
    Properties = new UiWidgetProperties { Key = "properties", Children = [/* fields */] },
    Editor = new UiWidgetEditor { Key = "editor", Children = [/* room for a big editor */] }, // optional
};
```

- `Properties` is the ordinary field list; the desktop editor draws it beside the preview.
- `Editor` is room a field list would not fit in, and is **optional**. Without it the editor is a single
  pane, not a split with an empty half.

You supply the fields. Macro Deck supplies the widget preview, the split layout and its narrow-window
drawer, the visual and JSON modes, scrolling, saving and the unsaved-changes prompt. Which side each region
lands on is the renderer's decision, and nothing in the contract names a renderer - a future native client
draws the same tree.

### An input's id is the data key it configures

```csharp
new UiStringInput { Key = "label" }                 // writes "label"
new UiObjectInput { Key = "border", Children =
    [new UiColorInput { Key = "color" }] }          // writes "border.color"
new UiArrayInput { Key = "states" /* ... */ }       // writes a JSON array
```

A region opens no input-id scope, so a top-level input's id is the widget data key it writes - in both
regions, which share one namespace. `UiObjectInput` and `UiArrayInput` do open a scope. Address array
items by their own stable key, never by position: a positional id loses focus and in-flight edits on
every reorder.

### The tree edits a draft it does not own

```csharp
attributes.TryGetValue(UiConfigSurfaceAttributes.WidgetData, out var data); // stored configuration
```

Nothing your tree does persists anything. Macro Deck accumulates the edits and writes them through the
ordinary widget save path on save, which keeps schema validation, JSON mode and the unsaved-changes prompt
working
([ADR 0050](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0050-ui-sessions-are-host-brokered.md)).
A plugin cannot read the host's stored widgets, so the configuration arrives on the surface. A key your
tree never mentions survives a save untouched, so a partial configuration drops nothing.

| `UiConfigSurfaceAttributes` | Value |
| --- | --- |
| `WidgetId` | The widget being configured. |
| `WidgetType` | Its type id. Check it before serving. |
| `WidgetData` | Its stored configuration. |
| `WidgetWidth`, `WidgetHeight` | Its size on the deck. That belongs to the deck: never part of `WidgetData`, never written back. |

### Reaching an editor Macro Deck already has

```csharp
new UiActionsListEditor { Key = "flows", Binding = Bind.To(flows), CanRun = true }
```

| Node type | DSL element | Configures |
| --- | --- | --- |
| `actions-list-editor` | `UiActionsListEditor` | The list of action flows, with triggers, ordering and nesting |
| `action-picker` | `UiActionPickerInput` | One action from the catalog of everything installed |
| `variable-picker` | `UiVariablePickerInput` | One variable, optionally narrowed to types (`VariableTypes`) or writable ones (`WritableOnly`). In the widget editor it lists global variables and the edited widget's own widget variables, never another widget's |
| `device-picker` | `UiDevicePickerInput` | One connected device |
| `integration-picker` | `UiIntegrationPickerInput` | One integration, or one of its configuration entries |
| `icon` | `UiIconReferenceInput` | One icon, as a typed provider reference |
| `icon-display` | `UiIconDisplayInput` | An icon's framing (fit, zoom, offset, opacity) over a preview of `Icon` at `AspectRatio` against `Background`; with `Tint` set, the preview draws the icon in that colour, keeping its transparency |
| `thresholds` | `UiThresholdsInput` | A range divided into coloured bands, edited on a bar with a draggable handle between each pair - see [Colour thresholds](#colour-thresholds) |

Each renderer maps these onto the editors it already ships; a plugin ships no renderer code for them.

To preselect one of your plugin's [bundled icons](https://docs.macro-deck.app/ui/reference/resources/#icons-from-your-bundled-icon-packs)
in the `icon` picker, give the input a plugin-icon default:

```csharp
new UiIconReferenceInput
{
    Key = "icon",
    Binding = Bind.To(icon),
    DefaultValue = UiIconReference.PluginIcon("logos", "spotify"),
}
```

Macro Deck resolves the reference against your own bundled packs and replaces it with the matching
`icon-pack` reference before the form reaches a client, so the picker shows the icon and the user can
change it like any other. The value that comes back to your plugin, and the one that is saved, is therefore
an `icon-pack` reference, never a `plugin-icon` one. A key or name your packs do not hold arrives as no
default. There is no separate "suggested value": the default is how a form proposes an icon. The picker
lists your bundled packs, read-only, alongside the user's own packs.

For a file, folder or image path, use the
[path inputs](https://docs.macro-deck.app/ui/views/configuration/#letting-the-user-pick-a-file-folder-or-image), which work in both
regions like any other input.

`UiActionsListEditor.Triggers` names the trigger tabs the editor offers, such as `["onDoublePress"]` for a
single Double Tap tab. Leave it unset for the default press tabs: Short Press, Long Press, Touch Start, Touch
End and Double Tap. Event triggers, which run a flow when an integration or Macro Deck event fires, are
offered alongside those tabs either way. The host runs a widget's event flows only from the top-level
`flows` key of its stored configuration, so bind the editor there, as in the example above, for them to
fire. Press flows run only for built-in widgets and for a widget type registered with
[`SupportsFlows`](https://docs.macro-deck.app/ui/views/widget-types/#running-the-users-actions).

- **`device-picker`** only populates where the viewer holds admin scope, because the device list is an
  administrative endpoint. The desktop editor does; prefer another picker where you have the choice.
- **A renderer without such an editor declines the type** like any unknown node type, and draws the node's
  `Fallback`. To stay configurable there, give the node a fallback built from primitives - a `json` input
  over the same value is usually enough.

#### Letting the user adopt a provider action

A widget that follows an action's state or icon, like the Action Button, can let the user adopt one of the
actions in its own flows as that provider, right from the action list:

```csharp
new UiActionsListEditor
{
    Key = "flows",
    Binding = Bind.To(flows),
    OffersStateProvider = true,
    OffersIconProvider = true,
    StateProviderBlockId = UiValue.From(() => stateProvider.Value?.BlockId ?? string.Empty),
    Events = [UiEventHandler.OnAsync(UiConfigEvents.Provide, (data, _) => AdoptAsync(data))],
}
```

| Property | Meaning |
| --- | --- |
| `OffersStateProvider`, `OffersIconProvider` | The renderer marks actions that can provide states or an icon, and puts a control on each such action in the list. |
| `StateProviderBlockId`, `IconProviderBlockId` | The block the widget currently uses, so that control shows as active. Empty means none. |

Using a control raises `provide` on the node, with the payload
`{ "capability": "state" | "icon", "blockId": "...", "enabled": true | false }`. It is a request: your handler
decides whether to adopt, switch or stop, and the two block id properties report the result. The offer
properties do nothing unless the node also handles `provide`, so a renderer never shows a control that
cannot answer. A renderer or host that predates these properties and the event ignores them, and the action
list looks the way it always did. To show which action currently provides, the Action Button uses a
[status line](https://docs.macro-deck.app/ui/views/configuration/#showing-what-governs-a-setting).

### Standard appearance fields

```csharp
Properties = new UiWidgetProperties
{
    Key = "properties",
    Children =
    [
        new UiStringInput { Key = "variable", Label = Strings.Gauge.Variable(), Binding = Bind.To(variable) },
        UiWidgetAppearance.Section(data, UiWidgetAppearanceFields.All),
    ],
},
```

`UiWidgetAppearance.Section` builds Macro Deck's own appearance fields, already translated: background
colour, label, label colour, accent colour, font (face, size, alignment, position) and border. Pick the groups
with `UiWidgetAppearanceFields`, named after the `WidgetAppearanceProperty` values a
[widget type declares](https://docs.macro-deck.app/ui/views/widget-types/#standard-appearance), so declare the same ones there for the
appearance actions to reach them.

- The fields write the [documented keys](https://docs.macro-deck.app/ui/views/widget-types/#standard-appearance) and own them as input
  ids, together with the heading keys `appearance-heading` and `border-heading`: do not use those ids for
  inputs of your own.
- Saving without touching a field leaves its key as it was stored. An empty label or border colour is
  removed rather than stored empty.
- The font field lists the host's fonts from the `macrodeck.fonts` option source. The desktop editor
  resolves that source for your tree; it is the only host source it resolves for a provider's tree. The
  list includes fonts the user imported and can change while the host runs, so do not cache it.
- A choice whose options carry a `fontFaceId` entry in `Metadata` is drawn by the desktop editor as a
  searchable list that shows each option in that face, loaded once the row scrolls into view. It is a
  rendering hint only: the stored value is still the option's `Value`, and a client that does not know the
  key draws an ordinary choice.
- On a Macro Deck release older than these fields, the font list stays empty and the field labels show as
  `[[macrodeck:...]]` keys, because Macro Deck resolves the `macrodeck` catalog from its own copy.
- Transparency is opt-in. Add `UiWidgetAppearanceFields.TransparentBackground` next to `BackgroundColor`
  and the background field also offers **Transparent**, which stores the literal `transparent`. Add it only
  when your view passes that value on to its root node (see
  [widget types](https://docs.macro-deck.app/ui/views/widget-types/#standard-appearance)). `All` does not include it, and on its own it
  builds nothing.

### Offering a transparent colour

```csharp
new UiColorInput
{
    Key = "backgroundColor",
    Label = Strings.Background(),
    Binding = Bind.To(background),
    SupportsReset = true,
    DefaultValue = "",
    AllowTransparent = true,
}
```

`AllowTransparent` puts a **Transparent** swatch after the picker's colours. Choosing it stores the literal
`transparent` instead of a `#rrggbb` value. Set it only for a value your widget knows how to read: a stack or
button `background` accepts it, a modifier's does not. Without the flag, or on a Macro Deck release that
does not know it, the picker offers colours only and the node is serialised exactly as before.

### Colour thresholds

```csharp
UiThresholds.TryParse(data.TryGetProperty("thresholds", out var raw) ? raw : default, out var stored);
var thresholds = new UiState<UiThresholds>(stored!); // null until the user edits

new UiThresholdsInput
{
    Key = "thresholds",
    Label = Strings.ColourThresholds(),
    Binding = Bind.To(thresholds),
    Min = 0,
    Max = 100,
    Step = 1,
    Unit = "%",
    DefaultValue = new UiThresholds([
        new UiThresholdBand("ok", "#34c759"),
        new UiThresholdBand("busy", "#ffcc00", 60),
        new UiThresholdBand("hot", "#ff3b30", 85),
    ]),
    SupportsReset = true,
}
```

The editor draws a bar from `Min` to `Max`, coloured band by band, with a draggable handle on every boundary;
the selected handle shows its value in `Unit`, and every band lists its range below the bar. Clicking the bar
adds a boundary at that point, and the user recolours and removes bands from the list; on a focused range, `+`
splits it and `Delete` removes it. The Slider, History Graph and Gauges widgets use the same editor for their own
colour thresholds. It works in a [config flow](https://docs.macro-deck.app/ui/views/configuration/) as well as in a widget
configuration.

The value is a `UiThresholds`, stored and sent as:

```json
{ "bands": [
  { "id": "ok", "color": "#34c759" },
  { "id": "busy", "color": "#ffcc00", "from": 60 },
  { "id": "hot", "color": "#ff3b30", "from": 85 }
] }
```

Each band runs from its `from` up to the next band's. The first band has no `from` and covers everything
below the second. Later starts are finite and strictly increasing, so handles never cross. A value carries 1
to 64 bands with unique, non-empty ids and `#rgb` or `#rrggbb` colours, normalised to lowercase `#rrggbb`. The
`UiThresholds` constructor throws on anything else, and a `change` that breaks a rule is rejected before it
reaches your binding.

| Property | Meaning |
| --- | --- |
| `Min`, `Max` | The bar's extent. A boundary outside it widens the bar instead of being moved. |
| `Step` | What a handle moves by, and the narrowest a band can be dragged. |
| `Unit` | Drawn after every value. A `UiText`, so a word unit can be localized. |
| `DefaultValue` | The bands shown while the value is null, and what reset returns to. |
| `SupportsReset` | Offers a reset while the value differs from the defaults. Reset writes **null**, not a copy of the defaults. |
| `Disabled` | Read-only: the bar and list show, nothing can be changed. |
| `FixedCount` | No adding or removing: the number of bands stays the default's. Handles still move and colours still change. |
| `FixedColors` | No recolouring and no new band. Handles still move and bands can still be removed. |
| `MaxCount` | Caps adding. A stored value already above it stays editable. |

- **Null means "use the defaults".** Bind a null until the user edits and give your defaults as
  `DefaultValue`, so a widget whose defaults depend on another setting keeps following that setting. Read the
  stored value with `UiThresholds.TryParse`, which never throws, and fall back to your defaults:

  ```csharp
  var colour = (stored ?? defaults).ColorAt(reading); // "#ffcc00" for 70 in the example above
  ```

- **The modes are enforced on your binding only.** A change that breaks `Disabled`, `FixedCount`,
  `FixedColors` or `MaxCount` never reaches a writable binding. A read-only binding paired with your own
  `change` handler receives every change unchecked. A widget's stored configuration is drafted by the client
  and can hold any value that is valid in shape, so read it with `TryParse` and tolerate any band count.
- **A Macro Deck release that predates `thresholds`** declines the node and draws its `Fallback`, or shows the
  field as unsupported without one. A `json` input cannot stand in for it, because its value is text.

### Declining

```csharp
if (widgetType.GetString() != GaugeWidgetType)
{
    return Task.FromResult<IUiSession?>(null);
}
```

Returning `null` declines and is not an error. But unlike an action or a config flow, a widget has **no
declared field list to fall back to**: a declined widget configuration leaves the user with JSON mode only.
Decline only widgets you genuinely do not configure, and check `WidgetType` rather than assuming the
surface is yours.

### See also

- [Serving a configuration view](https://docs.macro-deck.app/ui/views/configuration/)
- [Deck widget views](https://docs.macro-deck.app/ui/views/widget/)
- [Widget types](https://docs.macro-deck.app/ui/views/widget-types/)
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)

## Widget types

> Source: https://docs.macro-deck.app/ui/views/widget-types/
>
> Offering your own deck widget - registering the type, drawing it, and configuring it.

A widget type is a kind of tile a user can add to a deck, next to Macro Deck's six built-in ones.

### Example

```csharp
public sealed class GaugeIntegration : IPluginIntegration, IWidgetTypeProvider, IUiProvider
{
    private const string GaugeSchema = """
        {"type":"object","properties":{"unit":{"type":"string"}},"required":["unit"]}
        """;

    private string? _gaugeType;

    public string ProviderName => "Gauges";

    public async Task InitializeAsync(IWidgetTypeProviderContext context, CancellationToken cancellationToken = default)
    {
        var registration = await context.RegisterWidgetTypeAsync(
            new WidgetTypeDescriptor(
                "gauge",
                MyStrings.GaugeName(),
                MyStrings.GaugeDescription(),
                DefaultData: """{"unit":"km/h"}""",
                DataSchema: GaugeSchema,
                HasConfiguration: true),
            cancellationToken);

        _gaugeType = registration.WidgetTypeId; // "com.example.gauges::gauge"
    }

    public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
    [
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared },
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Preview, SessionMode = UiSessionModes.Shared },
        new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Config, SessionMode = UiSessionModes.Exclusive },
    ];

    public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
    {
        var surface = request.Surface;
        var attributes = surface.Attributes;

        UiElement? root = surface.Kind switch
        {
            UiSurfaceKinds.Widget or UiSurfaceKinds.Preview
                when attributes[UiWidgetSurfaceAttributes.WidgetType].GetString() == _gaugeType
                => GaugeView(70, attributes[UiWidgetSurfaceAttributes.Data].GetProperty("unit").GetString()!),
            UiSurfaceKinds.Config
                when attributes[UiConfigSurfaceAttributes.EntryPoint].GetString() == UiConfigEntryPoints.WidgetConfig
                && attributes[UiConfigSurfaceAttributes.WidgetType].GetString() == _gaugeType
                => GaugeConfig(attributes[UiConfigSurfaceAttributes.WidgetData]),
            _ => null,
        };

        return Task.FromResult<IUiSession?>(root is null ? null : new ViewSession(new UiView(surface, root)));
    }

    // IPluginIntegration members, GaugeView and GaugeConfig omitted.
}
```

*[Image: A gauge widget tile with the reading 70 km/h above a half-circle gauge and its needle]*

`GaugeView` builds the dial from a [transform](https://docs.macro-deck.app/ui/components/transform/); `ViewSession` is the
adapter from [Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example). Decline a type you do not serve rather than
guessing from the data's shape. A widget of your type is placed, moved, resized, exported and imported
like a built-in one, and drawn by the same UI runtime.

### Registering the type

```csharp
var registration = await context.RegisterWidgetTypeAsync(descriptor, cancellationToken);
// registration.WidgetTypeId == "com.example.gauges::gauge"
```

The qualified id is what every widget stores as its type. **Keep it stable across releases** - renaming it
strands every widget already on a deck - and never reuse it for a different widget.

Registration is a push: register when you are ready, and register again under the same local id to change
the name, default data, schema or configuration flag; placed widgets pick the new descriptor up untouched.
`GetWidgetTypes()` only lets Macro Deck recover its catalog after a reconnect, and is optional. There is no
`ShutdownAsync` here: release what `InitializeAsync` acquired in your integration's own `ShutdownAsync`,
and Macro Deck withdraws your types itself.

### Default data and schema

```csharp
DefaultData: """{"unit":"km/h"}""",
DataSchema: GaugeSchema,
```

`DefaultData` is the stored configuration a new widget starts with, as a JSON object; absent reads as
`{}`. `DataSchema` is a JSON Schema Macro Deck validates every save against, so configuration cannot write
a shape you cannot read back. It is optional for fixed data and **required when `HasConfiguration` is
true**. There is no icon: the picker draws a live sample instead.

### Drawing each tile

One session is opened per widget per viewer, so each tile sees only its own `data`. Push patches on the
session to update it; events its tree declares come back to that same session. Saved and draft data
arrive the same way, because you cannot read Macro Deck's stored widgets. By default a press runs nothing on
the host - a tile whose tree declares no events does nothing when pressed - unless the type
[runs the user's actions](#running-the-users-actions) or has a
[default Short Press action](#a-default-short-press-action).

### The picker card

```csharp
UiSurfaceKinds.Preview // with attributes["sample"] == true
```

A picker card is a live `preview` surface with `sample: true`: draw a representative sample without
reading anything live. Serving it is optional - declining gets a card naming the type, and the type stays
pickable either way.

### Configuration

```csharp
UiSurfaceKinds.Config
    when attributes[UiConfigSurfaceAttributes.EntryPoint].GetString() == UiConfigEntryPoints.WidgetConfig
```

With `HasConfiguration`, editing a widget opens a `config` surface with the `widget-config` entry point.
Build it with the [widget configuration view](https://docs.macro-deck.app/ui/views/widget-configuration/), whose two regions Macro
Deck lays out around your tree. What the user enters is stored with the widget and handed back on every
later `widget` surface. No second contract is needed - one more surface on the same `IUiProvider`.

Without `HasConfiguration`, no `config` surface is ever opened for your type: editing one of its widgets
shows the preview and the JSON view, and nothing else.

### Running the user's actions

```csharp
new WidgetTypeDescriptor("battery", MyStrings.BatteryName(), DataSchema: BatterySchema, HasConfiguration: true)
{
    SupportsFlows = true,
}
```

A widget that only shows information can still work like a button. With `SupportsFlows`, Macro Deck runs the
widget's own action flows when its tile is pressed, the way it does for its built-in widgets: Short Press,
Long Press, Double Tap, Touch Start and Touch End each run the flow bound to that trigger. The flows come
from the top-level `flows` key of the widget's stored data, so give the user the actions editor bound
there in your configuration tree, and let your `DataSchema` allow the key:

```csharp
new UiActionsListEditor { Key = "flows", Binding = Bind.To(flows), CanRun = true }
```

```json
{"type":"object","properties":{"flows":{"type":"array"}}}
```

The [widget configuration view](https://docs.macro-deck.app/ui/views/widget-configuration/#reaching-an-editor-macro-deck-already-has)
covers the editor. Your tree keeps priority: a press that one of its controls declares is sent to that
control, as without the flag, and runs no flow.

- **Hardware decks never produce a Double Tap** for a widget of your type, only for built-in ones: a
  Double Tap flow runs from the desktop app and the web client. Set `UiActionsListEditor.Triggers` to the
  press tabs you want if that would confuse your users.
- **An older Macro Deck ignores the flag**, and presses of your widget run nothing there, as before.
- **While your type is not registered** - your plugin stopped or not installed - Macro Deck cannot tell
  that the type opted in, and a press of its widget is refused as it is for any unknown type.

The default is `false`, and a type that leaves it unset behaves exactly as described above.

### A default Short Press action

```csharp
new WidgetTypeDescriptor("lamp", MyStrings.LampName())
{
    DefaultShortPressAction = new WidgetDefaultAction("toggle",
        new Dictionary<string, string> { ["room"] = "kitchen" }),
}
```

A widget can come with a useful primary interaction before the user configures anything. With
`DefaultShortPressAction`, Macro Deck runs one of your own actions when the widget is short-pressed and the
user has not given it a Short Press action of their own. The built-in Weather widget works this way: a short
press opens its details.

- **The user's action wins.** The default runs only while the widget's Short Press flow is missing, empty
  or has every action disabled. A type without `SupportsFlows` has no such flow, so its default always runs.
  A press that your tree claims goes to the tree and never runs the default.
- **Only your own action.** `ActionId` names an action your plugin declares; another integration's action
  cannot be named, because a default runs without the user choosing it. A blank `ActionId` gets the type
  rejected at registration.
- **Parameters are text**, typed from the action's declared parameters and rendered like a value the user
  stored, so a template in one is resolved. A parameter you leave out gets its declared default.
- **The action runs like one from the widget's own flow**: `ActionExecutionContext.OwnerWidgetId` names the
  pressed widget and `OriginClientId` the client that pressed it, so the default can open a
  [modal](https://docs.macro-deck.app/ui/views/modal/) on that screen.
- **Every client runs it**: the desktop app, the web client, the Companion app and hardware decks. A
  hardware deck is offered a press for a tile of your type even when the widget has no flow. It has no screen
  for a modal, so keep a default that opens one for widgets meant for a screen: the built-in Weather default
  is the one exception Macro Deck makes itself, and it does not run from a hardware deck.
- **Nothing runs** while your plugin is disabled or does not declare the action.
- **An older Macro Deck ignores the property**, and short presses of your widget run nothing there, as before.

### Standard appearance

```csharp
new WidgetTypeDescriptor("frame", MyStrings.FrameName(), DataSchema: FrameSchema, HasConfiguration: true)
{
    AppearanceProperties =
    [
        WidgetAppearanceProperty.BackgroundColor, WidgetAppearanceProperty.Label,
        WidgetAppearanceProperty.LabelColor, WidgetAppearanceProperty.Font,
    ],
}
```

A widget of your type can share the appearance settings of Macro Deck's own widgets. Every type gets a
**border**: Macro Deck draws the ring around the tile from the `border` key of the widget's stored data, and
the Set Border action writes it, with or without a declaration. `AppearanceProperties` adds any of
`BackgroundColor`, `Label`, `LabelColor`, `Font` and `AccentColor`. For each one you list, the widget appearance
actions (Set Background Color, Set Label, Set Label Color, Set Label Font, Set Accent Color) accept a widget of your
type and write the value to the stored data, under these keys:

| Key | Property | Value |
| --- | --- | --- |
| `border` | `Border`, `BorderColor` | `{ "style": "...", "color": "#rrggbb" }`. `style` is `off`, `static`, `heartbeat`, `breathing`, `blink`, `comet`, `ants`, `hue-shift` or `rgb`; without `color` the ring uses its default colour |
| `backgroundColor` | `BackgroundColor` | `#rrggbb`, or `transparent` |
| `label` | `Label` | The text as entered |
| `labelColor` | `LabelColor` | `#rrggbb` |
| `fontFaceId` | `Font` | A face id from the host's font catalogue (the `macrodeck.fonts` option source) |
| `fontSize` | `Font` | Size as a whole-number percentage |
| `textAlign` | `Font` | `left`, `center` or `right` |
| `labelPosition` | `Font` | `top`, `center` or `bottom` |
| `accentColor` | `AccentColor` | `#rrggbb` |

`UiWidgetAppearanceKeys` holds the names. Clearing a setting removes its key. Other values of
`WidgetAppearanceProperty`, such as `Icon`, are ignored for a provider's type.

Macro Deck draws only the border. Draw the rest yourself: the change reopens your widget's session with the
new data, and `UiWidgetAppearance.Read` gives you the values:

```csharp
attributes.TryGetValue(UiWidgetSurfaceAttributes.Data, out var data);
var appearance = UiWidgetAppearance.Read(data);

var root = new UiButton
{
    Key = "frame",
    Background = appearance.BackgroundColor ?? "#1f2937",
    Children = [new UiTextRun { Key = "caption", Text = appearance.Label ?? string.Empty, Color = appearance.LabelColor ?? "#ffffff" }],
};
```

Your `DataSchema` has to allow the keys you declare. A property is offered for a widget only if the schema
accepts a plain sample value under its keys (`#000000`, `Label`, a font id with size 12, `center`), so keep
patterns, enums and ranges on these keys permissive, and a value your schema rejects, such as a label that fails a `pattern`, makes the action fail
instead of storing data your configuration could no longer save:

```json
{
  "type": "object",
  "properties": {
    "border": { "type": "object" },
    "backgroundColor": { "type": "string" },
    "label": { "type": "string" },
    "labelColor": { "type": "string" },
    "fontFaceId": { "type": "string" },
    "fontSize": { "type": "number" },
    "textAlign": { "type": "string" },
    "labelPosition": { "type": "string" },
    "accentColor": { "type": "string" }
  }
}
```

The [widget configuration view](https://docs.macro-deck.app/ui/views/widget-configuration/#standard-appearance-fields) has ready-made
fields for the same keys.

- **A background can be `transparent`.** The Set Background Color action stores whatever value it is given,
  and the configuration field offers Transparent when you opt in with
  [`TransparentBackground`](https://docs.macro-deck.app/ui/views/widget-configuration/#standard-appearance-fields). Pass the value to
  your root `ui.stack` or `ui.button` `background` as it is: when the root node's background is
  `transparent`, Macro Deck also leaves out the tile's own face and shadow, so the folder background shows
  through. The border ring is still drawn. A background of `transparent` on any node below the root, or a
  root that is not a stack or button, keeps the tile face.
- **The label is stored as entered.** It may contain a `{{ ... }}` variable template, which Macro Deck
  renders only for its own Action Button. Show the text as it is, or render it yourself.
- **Hardware devices read these keys too.** A device plugin receives `label`, `labelColor`,
  `backgroundColor`, `fontSize`, `textAlign` and `labelPosition` for every widget, but not the font face.
- **Every change reopens your widget's session** with the new data, so a flow that changes an appearance
  setting every second rebuilds your tree every second.
- **While your type is not registered** - your plugin stopped, or still starting - its widgets offer the
  border only, and the other actions fail for them.
- **An older Macro Deck ignores the declaration** and offers the border only, as before.

### When your integration is not running

```csharp
await context.UnregisterWidgetTypeAsync("gauge", cancellationToken);
```

A widget keeps its type and data whether or not anything provides them - stored, exported and re-imported
unchanged, including on a machine where your plugin is not installed yet. When the type comes back, every
widget of it returns exactly as it was. Unregistering only stops the type being offered in the picker.
Macro Deck keeps your catalog entry across a mere disconnect, so a restarting plugin does not leave its
widgets nameless; the entry goes only when the integration is uninstalled or stopped.

### Over the plugin protocol

Registration is driven from the plugin side, so the host-to-provider direction of the
`widget-type-provider` capability only has to describe the provider and re-read its catalog after a
reconnect:

| Operation | Purpose |
| --- | --- |
| `describe` | The provider's declared name and its current catalog. |
| `widget-types` | The provider's current widget type catalog, re-read after a reconnect. |

Registering and withdrawing a type travels the other way as the `widget-types` host API:

| Operation | Purpose |
| --- | --- |
| `register` | Registers a widget type, or replaces one already registered under the same provider-local id. |
| `unregister` | Withdraws a widget type. Widgets already using it keep their stored type and data and wait for it to return. |

The widgets themselves are drawn, previewed and configured over the `ui` capability, like every other
Macro Deck UI surface.

### See also

- [Deck widget views](https://docs.macro-deck.app/ui/views/widget/) - the attribute keys in full.
- [Configuring a widget](https://docs.macro-deck.app/ui/views/widget-configuration/) - the two-region configuration tree.
- [Folder views](https://docs.macro-deck.app/ui/views/folder-views/) - the same registration shape, one level up.
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)

## Deck widget views

> Source: https://docs.macro-deck.app/ui/views/widget/
>
> The widget surface - what it carries, and how a provider is handed one.

A deck widget is a tile on the deck drawn from your tree, served over a `widget` surface.

### Example

```csharp
public IReadOnlyList<UiSurfaceDeclaration> Surfaces { get; } =
[
    new UiSurfaceDeclaration { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared },
];

public Task<IUiSession?> CreateSessionAsync(UiSessionRequest request, CancellationToken cancellationToken)
{
    if (request.Surface.Kind != UiSurfaceKinds.Widget)
    {
        return Task.FromResult<IUiSession?>(null);
    }

    var data = request.Surface.Attributes[UiWidgetSurfaceAttributes.Data];
    var city = data.TryGetProperty("city", out var value) ? value.GetString() : null;

    var view = new UiView(request.Surface, Weather(city ?? "Berlin"));
    return Task.FromResult<IUiSession?>(new ViewSession(view));
}

private UiStack Weather(string city) => new()
{
    Key = "weather",
    Justify = UiComponentJustify.SpaceBetween,
    Children =
    [
        new UiStack
        {
            Key = "current",
            Direction = UiComponentDirections.Horizontal,
            Justify = UiComponentJustify.SpaceBetween,
            Children =
            [
                new UiStack
                {
                    Key = "labels",
                    Children =
                    [
                        new UiTextRun { Key = "location", Text = city, Size = 0.09 },
                        new UiTextRun { Key = "temp", Text = UiText.From(() => $"{_forecast.Value.Temperature}°"), Size = 0.26 },
                    ],
                },
                new UiImage { Key = "icon", Source = _sun, Size = 0.26 },
            ],
        },
        new UiTextRun
        {
            Key = "condition",
            Text = UiText.From(() => _forecast.Value.Condition),
            Size = 0.08,
            Role = UiComponentTextRoles.Secondary,
        },
        new UiRangeBar { Key = "range", MainSize = 0.06, Start = 0.2, End = 0.6, Marker = 0.45 },
    ],
};
```

*[Image: A two-by-two weather widget: Berlin, 21°, a sun icon, the caption Sunny and a temperature range bar]*

To offer a widget in the picker, register a [widget type](https://docs.macro-deck.app/ui/views/widget-types/) - that page covers
registration, the picker card and configuration. The same vocabulary also draws a
[folder view](https://docs.macro-deck.app/ui/views/folder-views/) and an [action modal](https://docs.macro-deck.app/ui/views/modal/).

### Forwarding to a UiView

`ViewSession`, the adapter between a `UiView` and `IUiSession` used on every view page, is defined on
[Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example).

### What the surface carries

| Attribute (`UiWidgetSurfaceAttributes`) | Meaning |
| --- | --- |
| `widgetId` | The widget being drawn. |
| `widgetType` | Its qualified widget type id. |
| `data` | Its stored configuration, as JSON. |
| `cornerRadius` | The tile's corner radius. |
| `sample` | `true` when the picker asks for a representative sample. |
| `ghost` | `true` when drawing the drag ghost of a widget that is also drawn live. |

The surface carries no size: a widget is resized on the deck without asking you. To lay a 2x1 or 1x2 tile
out differently from a 1x1 one, use [`UiResponsive`](https://docs.macro-deck.app/ui/components/responsive/), which the reader resolves
against the tile.

The stored configuration travels with the request rather than being looked up, so a provider outside
the host can serve a widget. A provider that ignores `sample` or `ghost` keeps behaving exactly as it
did.

For a type that declares [standard appearance](https://docs.macro-deck.app/ui/views/widget-types/#standard-appearance),
`UiWidgetAppearance.Read(data)` returns the background, label, colours and font the user or an action set.

### Previews, samples and ghosts

```csharp
var attributes = request.Surface.Attributes;
var isSample = attributes.TryGetValue(UiWidgetSurfaceAttributes.Sample, out var sample)
    && sample.ValueKind == JsonValueKind.True;
var isGhost = attributes.TryGetValue(UiWidgetSurfaceAttributes.Ghost, out var ghost)
    && ghost.ValueKind == JsonValueKind.True;
```

An editor preview arrives as a `preview` surface carrying draft configuration instead. A `preview` with
`sample: true` is a picker card: draw it without reading anything live - nothing is connected, bound or
configured while someone is choosing a widget type. `ghost` exists because two surfaces for one widget are
otherwise identical, and without it the ghost and the tile would share a session.

### Artwork

`_sun` above is a [resource handle](https://docs.macro-deck.app/ui/reference/resources/). Get one for your own image from
`IIntegrationContext.UiResources` and register a name again to change the picture; see
[Registering your own images](https://docs.macro-deck.app/ui/reference/resources/#registering-your-own-images).

### See also

- [Widget types](https://docs.macro-deck.app/ui/views/widget-types/)
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)
- [Components](https://docs.macro-deck.app/ui/components/)
