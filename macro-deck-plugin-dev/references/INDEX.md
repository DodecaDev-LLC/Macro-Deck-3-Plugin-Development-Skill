# Macro Deck 3 plugin docs index

Every plugin-development page of docs.macro-deck.app, merged into topic files under `references/docs/`.
Each page is an `## <Page title>` section of the file shown, with its live URL. Links inside the pages
point at the live site; to read one locally, find its URL in this table.

Search everything: `grep -rn "<Type or term>" references/`.

| File | Page | What it covers | Live URL |
| --- | --- | --- | --- |
| `docs/introduction.md` | Your first action | Add an action with a parameter to the template plugin, trigger it, and show its state on the button. | https://docs.macro-deck.app/introduction/first-action/ |
| `docs/introduction.md` | Project setup | Every file of a Macro Deck plugin project, written by hand - the project file, manifest, entrypoint, integration and build recipe - and how to run it. | https://docs.macro-deck.app/introduction/manual-setup/ |
| `docs/introduction.md` | Quickstart | Create, run and package your first Macro Deck plugin in about five minutes, without Macro Deck installed. | https://docs.macro-deck.app/introduction/quickstart/ |
| `docs/introduction.md` | Samples and template | What the plugin template generates, which sample plugins exist and what each one demonstrates, and how to run one. | https://docs.macro-deck.app/introduction/samples-and-template/ |
| `docs/features.md` | Features | Every feature a Macro Deck plugin can add, the SDK contract behind it, and where it is documented. | https://docs.macro-deck.app/features/ |
| `docs/features.md` | Actions | Expose actions with IActionDefinition and IActionExecutor - parameters, truthful ActionResults, dynamic options, UI-tree configuration, and how an action behaves inside an action flow. | https://docs.macro-deck.app/features/actions/ |
| `docs/features.md` | Android devices | Work with Android devices through Macro Deck's own ADB connection with IAndroidDeviceManager - the host:adb permission, the user's control, operations, errors, limits and testing. | https://docs.macro-deck.app/features/android-devices/ |
| `docs/features.md` | Button icons | Let an action own an action button's rendered icon with IIconProviderActionDefinition - album art, avatars, weather imagery - by version, reference or bytes. | https://docs.macro-deck.app/features/button-icons/ |
| `docs/features.md` | Button states | Drive an action button's N-state appearance with IStateProviderActionDefinition - declaring states, reporting the active one, default appearances and expected states. | https://docs.macro-deck.app/features/button-states/ |
| `docs/features.md` | Calendars | Expose calendar accounts and events with ICalendarProvider - accounts from setup flows, overlap and recurrence rules, all-day events, event details, and what Macro Deck builds on top. | https://docs.macro-deck.app/features/calendars/ |
| `docs/features.md` | Deck and clients | Navigate folders and profiles with IDeckNavigator, fill pickers, and find out which folder each connected client has open. | https://docs.macro-deck.app/features/deck/ |
| `docs/features.md` | Device providers | Bring hardware or a custom client into Macro Deck with IDeviceProvider - register devices, report presence, render the deck and send presses back. | https://docs.macro-deck.app/features/devices/ |
| `docs/features.md` | Events | Declare events with IEventProvider, publish occurrences with IEventPublisher, and let users filter them with configuration parameters and dynamic options. | https://docs.macro-deck.app/features/events/ |
| `docs/features.md` | Integration issues | Report problems the user can act on with IIntegrationIssueProvider - severity, localized text, and a resolve button that can reopen setup. | https://docs.macro-deck.app/features/integration-issues/ |
| `docs/features.md` | Layout providers | Describe a device's surface with ILayoutProvider - regions, grid geometry and rendering ability - and point devices at it. | https://docs.macro-deck.app/features/layouts/ |
| `docs/features.md` | Localization | Translate a plugin with Localization/*.resx - the generated Strings class, placeholders, plurals, fallback, and the MDLOC diagnostics. | https://docs.macro-deck.app/features/localization/ |
| `docs/features.md` | Logging and health | Log with Serilog or ILogger and read the lines in the host's log files and log viewer; what the health endpoints answer and what happens at shutdown. | https://docs.macro-deck.app/features/logging/ |
| `docs/features.md` | Messaging between plugins | Let plugins and integrations talk to each other by topic with IMessageChannel - events, commands and requests, topic ids, lifecycle, delivery guarantees, limits, older hosts and testing. | https://docs.macro-deck.app/features/messaging/ |
| `docs/features.md` | Music players | Expose a music player with IMusicPlayerProvider and IMusicPlayer - instances, playback state, artwork, per-widget options, the standard actions, library browsing and device switching. | https://docs.macro-deck.app/features/music-players/ |
| `docs/features.md` | Settings migrations | Take a plugin's buttons, connections and credentials over from another application such as Macro Deck 2 with IMigrationProvider and IIntegrationMigration. | https://docs.macro-deck.app/features/settings-migrations/ |
| `docs/features.md` | Setup flows | Guide users through connecting an integration with IConfigFlowProvider - steps, fields, validation errors, secrets, OAuth, reconfiguring an entry and optional settings. | https://docs.macro-deck.app/features/setup-flows/ |
| `docs/features.md` | Testing plugins | Test actions, variables, events, configuration and devices in process with PluginTestHarness and the MacroDeck.Plugin.Testing fakes, then run the conformance suite. | https://docs.macro-deck.app/features/testing/ |
| `docs/features.md` | Variables | Declare variables with IVariableProvider - read-only and writable eager variables, attributes, testing, and the on-demand catalog. | https://docs.macro-deck.app/features/variables/ |
| `docs/features.md` | Video streams | Offer live video to Macro Deck with IVideoStreamIntegration and IVideoStreamProvider - streams and their state, sessions, the relay that carries the media, updates, limits, reconnects, older hosts, security and testing. | https://docs.macro-deck.app/features/video-streams/ |
| `docs/features.md` | Virtual profiles | Ship ready-made, read-only profiles with IProfileProvider - fixed layouts, folders, widgets and routed widget interactions. | https://docs.macro-deck.app/features/virtual-profiles/ |
| `docs/features.md` | Weather | Expose weather stations with IWeatherProvider and IWeatherStation - cached snapshots, forecasts, units and unavailability. | https://docs.macro-deck.app/features/weather/ |
| `docs/ui.md` | Macro Deck UI | A general framework for declarative UI, rendered across every surface Macro Deck offers - configuration, deck widgets, folder views and modals. | https://docs.macro-deck.app/ui/ |
| `docs/ui.md` | Events | Handling events, validating input, and the rule that a component offers only the interaction its node declares. | https://docs.macro-deck.app/ui/concepts/events/ |
| `docs/ui.md` | Reactive updates | How the runtime turns a state change into a patch, and the threading rules that make concurrent writes to a view safe. | https://docs.macro-deck.app/ui/concepts/reactive-updates/ |
| `docs/ui.md` | Sizing | Every length in a Macro Deck UI tree is a fraction of the view's size, so one tree is correct at every box size. | https://docs.macro-deck.app/ui/concepts/sizing/ |
| `docs/ui.md` | State and bindings | UiState, the binding kinds a property accepts, and how conditional and repeated content stay part of the tree. | https://docs.macro-deck.app/ui/concepts/state-and-bindings/ |
| `docs/ui.md` | Theming | Theme roles versus literal colours, and how text carries localization and typeface across a Macro Deck UI tree. | https://docs.macro-deck.app/ui/concepts/theming/ |
| `docs/ui.md` | The UI model | The transport-neutral tree, keys and identity, and how a client and a provider agree on a model version. | https://docs.macro-deck.app/ui/concepts/ui-model/ |
| `docs/ui.md` | Compatibility | The three packages as versioned contracts, why the model major moved to 3, and why 4 did not move the floor with it. | https://docs.macro-deck.app/ui/reference/compatibility/ |
| `docs/ui.md` | Patches | How a tree changes without a full resend, and the revision rule that keeps a patch attributable to the state it was computed from. | https://docs.macro-deck.app/ui/reference/patches/ |
| `docs/ui.md` | Resources | The resource handle a tree references instead of carrying bytes, and the limit that bounds what it can promise. | https://docs.macro-deck.app/ui/reference/resources/ |
| `docs/ui-views.md` | Views and surfaces | What a view and a surface are, the surface kinds Macro Deck offers, session modes, and which representation a client renders. | https://docs.macro-deck.app/ui/views/ |
| `docs/ui-views.md` | Serving a configuration view | Rendering a config flow or an action's configuration as a Macro Deck UI tree beside the declared fields it never replaces. | https://docs.macro-deck.app/ui/views/configuration/ |
| `docs/ui-views.md` | Custom views | A complete "now playing" folder view, from composed components through a served surface to a headless test. | https://docs.macro-deck.app/ui/views/custom/ |
| `docs/ui-views.md` | Developer preview | Registering [UiPreview] scenarios so Developer Tools can render a view in states that are hard to reach live. | https://docs.macro-deck.app/ui/views/developer-preview/ |
| `docs/ui-views.md` | Folder views | Replacing a folder's whole surface with a Macro Deck UI view, and what Macro Deck keeps for itself. | https://docs.macro-deck.app/ui/views/folder-views/ |
| `docs/ui-views.md` | Modal views | Opening a dialog from an action, how it is sized, which node completes it, and what bounds the wait. | https://docs.macro-deck.app/ui/views/modal/ |
| `docs/ui-views.md` | Screensavers | Offering what a device shows after it has sat idle, and what Macro Deck does with the touch that wakes it. | https://docs.macro-deck.app/ui/views/screensavers/ |
| `docs/ui-views.md` | Serving a view | IUiProvider, the session lifecycle every surface shares, the protocol limits, and what a refused update looks like. | https://docs.macro-deck.app/ui/views/sessions/ |
| `docs/ui-views.md` | Configuring a widget | Describing a widget's configuration as two named regions Macro Deck lays out, and reaching the editors the app already ships. | https://docs.macro-deck.app/ui/views/widget-configuration/ |
| `docs/ui-views.md` | Widget types | Offering your own deck widget - registering the type, drawing it, and configuring it. | https://docs.macro-deck.app/ui/views/widget-types/ |
| `docs/ui-views.md` | Deck widget views | The widget surface - what it carries, and how a provider is handed one. | https://docs.macro-deck.app/ui/views/widget/ |
| `docs/ui-components.md` | Components | Every node type the UI framework ships, and which page documents it. | https://docs.macro-deck.app/ui/components/ |
| `docs/ui-components.md` | Button | A pressable tile that lays out its children like a stack and adds artwork, a ring and a press. | https://docs.macro-deck.app/ui/components/button/ |
| `docs/ui-components.md` | Chart | Draws a normalised series as a line with the area beneath it filled. | https://docs.macro-deck.app/ui/components/chart/ |
| `docs/ui-components.md` | Dial | A rotary level the user turns, the interactive counterpart of the gauge. | https://docs.macro-deck.app/ui/components/dial/ |
| `docs/ui-components.md` | First fit | Offer several layouts for the same content and let the reader draw the first one whose text fits, measured in the viewer's own font. | https://docs.macro-deck.app/ui/components/first-fit/ |
| `docs/ui-components.md` | Gauge | A read-only level drawn along an arc, or around a full ring. | https://docs.macro-deck.app/ui/components/gauge/ |
| `docs/ui-components.md` | Grid | A container laying its children out in equal columns and rows, with column and row spans. | https://docs.macro-deck.app/ui/components/grid/ |
| `docs/ui-components.md` | Icon | One glyph of Macro Deck's built-in icon set, drawn by name in one colour, with no resource to upload. | https://docs.macro-deck.app/ui/components/icon/ |
| `docs/ui-components.md` | Image | Draws a resource handle, fitted into a square box and never cropped. | https://docs.macro-deck.app/ui/components/image/ |
| `docs/ui-components.md` | List | A scrolling container for dialogs that asks for more children as the user reaches its end. | https://docs.macro-deck.app/ui/components/list/ |
| `docs/ui-components.md` | Modifier | Background, border, radius, accessibility, disabled and gestures on any node, and padding, opacity, clip, mask and frame through a wrapper. | https://docs.macro-deck.app/ui/components/modifier/ |
| `docs/ui-components.md` | Progress | Draws a moving playback position as a bar or a time readout, advanced by the reader's own clock. | https://docs.macro-deck.app/ui/components/progress/ |
| `docs/ui-components.md` | Range bar | A read-only horizontal track with one gradient-filled span and an optional point marker. | https://docs.macro-deck.app/ui/components/range-bar/ |
| `docs/ui-components.md` | Responsive | Different layouts for different box sizes - a widget at 1x1, 2x1 or 1x2, a folder view on a phone or a tablet - chosen by the reader without a round-trip. | https://docs.macro-deck.app/ui/components/responsive/ |
| `docs/ui-components.md` | Segmented | A row of segments the user chooses one of, reporting the chosen index. | https://docs.macro-deck.app/ui/components/segmented/ |
| `docs/ui-components.md` | Shape | A filled and stroked rectangle, rounded rectangle, circle, capsule or path, drawn from the tree alone. | https://docs.macro-deck.app/ui/components/shape/ |
| `docs/ui-components.md` | Slider | A draggable level on a rounded track, the interactive counterpart of the range bar. | https://docs.macro-deck.app/ui/components/slider/ |
| `docs/ui-components.md` | Stack and layer | A stack lays children beside each other along one axis; a layer draws them on top of each other. | https://docs.macro-deck.app/ui/components/stack-and-layer/ |
| `docs/ui-components.md` | Text field | A single line of text the user types, for dialogs. | https://docs.macro-deck.app/ui/components/text-field/ |
| `docs/ui-components.md` | Text | A single run of text, sized as a fraction of the view basis. | https://docs.macro-deck.app/ui/components/text/ |
| `docs/ui-components.md` | Time and clock | Draws the current time, digitally or as an analogue face, advanced by the reader's own clock. | https://docs.macro-deck.app/ui/components/time/ |
| `docs/ui-components.md` | Toggle | An on/off switch the user flips, reporting the new state as a boolean. | https://docs.macro-deck.app/ui/components/toggle/ |
| `docs/ui-components.md` | Transform | Rotates, scales and shifts its children together about a pivot, so a needle turns by patching one number. | https://docs.macro-deck.app/ui/components/transform/ |
| `docs/ui-components.md` | Video stream | Shows a live video stream from a video stream provider, played from a session the reader opens, suspends and closes itself. | https://docs.macro-deck.app/ui/components/video-stream/ |
| `docs/cli.md` | Plugin CLI | macrodeck-plugin: scaffold, build, validate, inspect, pack, merge, bundle icon packs, run, preview, test and sign a Macro Deck plugin without installing a host. | https://docs.macro-deck.app/cli/ |
| `docs/cli.md` | macrodeck-plugin build | Build every runtime identifier the manifest declares, stage them into one payload, and package the result. | https://docs.macro-deck.app/cli/build/ |
| `docs/cli.md` | CI and automation | A GitHub Actions workflow that builds, validates and conformance-tests a plugin on every platform, gated on exit codes. | https://docs.macro-deck.app/cli/ci/ |
| `docs/cli.md` | macrodeck-plugin icon-pack | Bundle icon packs with a plugin project, list the bundled packs and remove them again. | https://docs.macro-deck.app/cli/icon-pack/ |
| `docs/cli.md` | macrodeck-plugin inspect | Describe what installing an artifact or version directory would find, without a running host. | https://docs.macro-deck.app/cli/inspect/ |
| `docs/cli.md` | macrodeck-plugin merge | Merge single-platform packages built on different machines into one multi-platform package. | https://docs.macro-deck.app/cli/merge/ |
| `docs/cli.md` | macrodeck-plugin new | Scaffold a new plugin project from the official template, interactively or from a script. | https://docs.macro-deck.app/cli/new/ |
| `docs/cli.md` | macrodeck-plugin pack | Build a .macroDeckPlugin artifact from a payload directory, validating the manifest first. | https://docs.macro-deck.app/cli/pack/ |
| `docs/cli.md` | macrodeck-plugin preview | Render a plugin's widget previews to PNG files without a running Macro Deck, for store images and release automation. | https://docs.macro-deck.app/cli/preview/ |
| `docs/cli.md` | macrodeck-plugin run | Launch a plugin with the environment the supervisor would give it, against the running host or a disposable stub. | https://docs.macro-deck.app/cli/run/ |
| `docs/cli.md` | Signing packages | keygen, sign and verify: creator key pairs, embedded package signatures, and private-key handling. | https://docs.macro-deck.app/cli/signing/ |
| `docs/cli.md` | macrodeck-plugin test | Run the conformance suite against a project, executable or artifact and write a text, JSON or Markdown report. | https://docs.macro-deck.app/cli/test/ |
| `docs/cli.md` | macrodeck-plugin validate | Check a manifest, version directory or packed artifact and report every problem in one run. | https://docs.macro-deck.app/cli/validate/ |
| `docs/guides.md` | Debugging plugins | Hit a breakpoint in a .NET plugin from Rider, Visual Studio or VS Code, against the desktop app or a disposable stub host. | https://docs.macro-deck.app/guides/debugging/ |
| `docs/guides.md` | Publishing to the Store | How a plugin reaches the Macro Deck Store - checks before you publish, the release workflow, signing and updates. | https://docs.macro-deck.app/guides/publishing/ |
| `docs/guides.md` | Troubleshooting | Symptom-driven fixes for the failures a Macro Deck plugin actually hits - build, packaging, connection, runtime and installation - each tied to a real diagnostic. | https://docs.macro-deck.app/guides/troubleshooting/ |
| `docs/reference.md` | Analyzers | Roslyn diagnostics provided by MacroDeck.Plugin.Analyzers, each with a snippet that triggers it and the fix. | https://docs.macro-deck.app/reference/analyzers/ |
| `docs/reference.md` | Authentication | How a plugin obtains a credential, exchanges it for a session token, presents that token on REST and on the WebSocket, and what it must never do with either. | https://docs.macro-deck.app/reference/authentication/ |
| `docs/reference.md` | Capability parity | Where out-of-process plugins behave differently from in-process integrations, and what that means for your code. | https://docs.macro-deck.app/reference/capability-parity/ |
| `docs/reference.md` | Conformance suite | The fixed set of protocol-level checks any plugin can be run against, in any language, without a Macro Deck installation. | https://docs.macro-deck.app/reference/conformance/ |
| `docs/reference.md` | Manifest reference | Every field of a Macro Deck plugin manifest.json - types, required-ness, patterns, defaults and clamped ranges - with a complete worked example. | https://docs.macro-deck.app/reference/manifest/ |
| `docs/reference.md` | Plugin hosting | Build and run an out-of-process .NET plugin with MacroDeck.Plugin.Hosting. | https://docs.macro-deck.app/reference/plugin-hosting/ |
| `docs/reference.md` | Plugin protocol | The versioned HTTP and WebSocket contract for out-of-process plugins - envelope, negotiation, errors, limits, backpressure and reconnection. | https://docs.macro-deck.app/reference/protocol/ |
| `docs/reference.md` | SDK overview | The packages a Macro Deck plugin builds against, the integration model they share, and where each area is documented. | https://docs.macro-deck.app/reference/sdk-packages/ |
| `docs/reference.md` | Store links | The address every Store entry can be shared under, the macrodeck:// link that opens it in the app, where it works, and what it refuses. | https://docs.macro-deck.app/reference/store-links/ |
| `docs/reference.md` | WebSocket reference | The envelope, the full message catalogue with direction and payload, correlation and cancellation rules, error handling and the unknown-message-type rule. | https://docs.macro-deck.app/reference/websocket/ |
| `docs/creator-portal.md` | Creator Portal | Publish plugins and icon packs to the Macro Deck Store through the Creator Portal. | https://docs.macro-deck.app/creator-portal/ |
| `docs/creator-portal.md` | Conformance report | What the conformance status of a build means, every warning the Creator Portal shows about it, and how to fix each one. | https://docs.macro-deck.app/creator-portal/conformance/ |
| `docs/creator-portal.md` | Projects and Store listing | Create a Project in the Creator Portal and fill in the Store listing. | https://docs.macro-deck.app/creator-portal/projects/ |
| `docs/creator-portal.md` | Publish an icon pack | Create a version, upload the .macroDeckIconPack and submit it for review. | https://docs.macro-deck.app/creator-portal/publish-icon-pack/ |
| `docs/creator-portal.md` | Publish a plugin | Connect a GitHub repository, add the release workflow, publish a GitHub release and submit the build for review. | https://docs.macro-deck.app/creator-portal/publish-plugin/ |
| `docs/creator-portal.md` | Release workflow reference | Inputs, permissions and error responses of the Macro Deck plugin publishing workflow. | https://docs.macro-deck.app/creator-portal/release-workflow/ |
| `docs/creator-portal.md` | Review and release | What happens after you submit - review statuses, change requests, manual release, updates and unlisting. | https://docs.macro-deck.app/creator-portal/review/ |
| `docs/creator-portal.md` | Testers | Let up to ten people install a plugin build in Macro Deck before it is reviewed. | https://docs.macro-deck.app/creator-portal/testers/ |
| `docs/policies.md` | Compatibility policy | Which Macro Deck plugin surfaces are frozen, what counts as a breaking change, how contracts are evolved additively, and how protocol majors are negotiated. | https://docs.macro-deck.app/policies/compatibility/ |
| `docs/policies.md` | Deprecations | The lifecycle for deprecating and removing a Macro Deck SDK API, how the host reports confirmed usage, and the compatibility states shown to a plugin's users. | https://docs.macro-deck.app/policies/deprecations/ |
| `docs/policies.md` | Migrations | Migration guides between Macro Deck SDK and protocol majors - what changed, what to use instead, and how long the previous version stays negotiable. | https://docs.macro-deck.app/policies/migrations/ |
| `docs/policies.md` | Security model | The trust boundary around a Macro Deck plugin, what the host does and does not guarantee, how credentials and artifacts are handled, and the limits of the model. | https://docs.macro-deck.app/policies/security/ |
