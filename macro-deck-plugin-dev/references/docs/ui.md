# Macro Deck UI: overview, concepts and reference

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Macro Deck UI: https://docs.macro-deck.app/ui/
- Events: https://docs.macro-deck.app/ui/concepts/events/
- Reactive updates: https://docs.macro-deck.app/ui/concepts/reactive-updates/
- Sizing: https://docs.macro-deck.app/ui/concepts/sizing/
- State and bindings: https://docs.macro-deck.app/ui/concepts/state-and-bindings/
- Theming: https://docs.macro-deck.app/ui/concepts/theming/
- The UI model: https://docs.macro-deck.app/ui/concepts/ui-model/
- Compatibility: https://docs.macro-deck.app/ui/reference/compatibility/
- Patches: https://docs.macro-deck.app/ui/reference/patches/
- Resources: https://docs.macro-deck.app/ui/reference/resources/

## Macro Deck UI

> Source: https://docs.macro-deck.app/ui/
>
> A general framework for declarative UI, rendered across every surface Macro Deck offers - configuration, deck widgets, folder views and modals.

Macro Deck UI lets a plugin describe what a person sees and can act on - once, as a tree of keyed
elements - and Macro Deck renders that tree wherever it is needed: a config flow, an action's
configuration, a deck widget, a folder view or a modal dialog. The vocabulary is the same on every
surface; only the box it is drawn in changes.

### Install

```xml
<!-- Plugin project -->
<PackageReference Include="MacroDeck.Ui" Version="3.0.0" />

<!-- Test project -->
<PackageReference Include="MacroDeck.Ui.Testing" Version="3.0.0" />
```

| Package | What it is |
| --- | --- |
| `MacroDeck.Ui` | The declarative C# DSL and the reactive runtime. Use it to author a view. |
| `MacroDeck.Ui.Model` | The transport-neutral tree, event and patch contract. Use it directly only when you need the low-level contracts. |
| `MacroDeck.Ui.Testing` | Renders and asserts against a view headlessly. |

### A small view, end to end

```csharp
var muted = new UiState<bool>(false);

var tile = new UiButton
{
    Key = "mute",
    Justify = UiComponentJustify.Center,
    Background = UiValue.From(() => muted.Value ? "#ff3b30" : "#2c2c2e"),
    Events = [UiEventHandler.On(UiComponentEvents.Press, () => muted.Value = !muted.Value)],
    Children = [new UiTextRun { Key = "label", Text = UiText.From(() => muted.Value ? "Muted" : "Mute"), Size = 0.14 }],
};

var view = new UiView(request.Surface, tile);
```

*[Image: A red button tile with a crossed-out microphone icon and the label Mute centred beneath it]*

A press flips `muted`; the button's face and label read it, so the view emits a patch for just those two
properties. `UiView` keeps the tree reactive; `UiViewBuilder.Build(surface, root)` makes a one-time tree
instead. Handing the view to Macro Deck is a separate step - see [Serving a view](https://docs.macro-deck.app/ui/views/sessions/). The
picture adds artwork to the same button - see [Button](https://docs.macro-deck.app/ui/components/button/).

### One vocabulary, two namespaces

Every node type is `ui.*` or `macrodeck.*`. A component is `macrodeck.*` when a reader cannot draw it from
the tree alone, because it must resolve a Macro Deck-defined reference - a time or a media position -
against its own clock. Everything else is `ui.*`, however Macro Deck-flavoured its styling. See
[ADR 0064](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0064-components-are-a-registry-over-two-namespaces.md).

### Where to go next

*[Image: A two-by-two weather widget: Berlin, 21°, a sun icon, the caption Sunny and a temperature range bar]*

- **[Components](https://docs.macro-deck.app/ui/components/)** - the full `ui.*`/`macrodeck.*` catalog, one page per family.
- **[Views](https://docs.macro-deck.app/ui/views/)** - the surfaces a tree renders on: sessions, configuration, deck widgets, folder
  views, modals and the developer preview.
- **[Concepts](https://docs.macro-deck.app/ui/concepts/ui-model/)** - the tree/patch model, state and bindings, events, reactive
  updates, sizing and theming.
- **[Reference](https://docs.macro-deck.app/ui/reference/patches/)** - patch operations, resource handles and the compatibility
  contract across the three packages.

### See also

- [SDK reference](https://docs.macro-deck.app/reference/sdk-packages/)
- [Capabilities](https://docs.macro-deck.app/features/)
- [Testing plugins](https://docs.macro-deck.app/features/testing/)
- [ADR 0038](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0038-ui-model-and-declarative-dsl.md)
- [ADR 0065](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0065-the-component-profile-authoring-contracts.md)

## Events

> Source: https://docs.macro-deck.app/ui/concepts/events/
>
> Handling events, validating input, and the rule that a component offers only the interaction its node declares.

A node lists the events it handles; a reader sends only those, and each lands in one handler.

### Example

```csharp
new UiSlider
{
    Key = "level",
    Level = UiValue.From(() => volume.Value),
    Events =
    [
        UiEventHandler.On(UiComponentEvents.Adjust, e =>
        {
            if (e.TryGetDouble(out var level)) volume.Value = level;
        }),
        UiEventHandler.On(UiComponentEvents.Change, e =>
        {
            if (e.TryGetDouble(out var level)) { volume.Value = level; muted.Value = level == 0; }
        }),
    ],
}
```

```json
{ "id": "volume.level", "type": "ui.slider", "properties": { "events": ["adjust", "change"], "level": 0.4 } }
```

The reader follows the drag with `adjust` and ends it with `change`. Each dispatch writes state; the runtime
turns the writes into one patch. Handlers update state or call your own logic - never rebuild the view.

### Reading the payload

```csharp
UiEventHandler.On(UiComponentEvents.Reveal, e =>
{
    if (e.TryGetDouble(out var index) && index >= songs.Peek().Count - 5)
    {
        LoadMore();
    }
}),
```

`UiEventData` offers `TryGetString`, `TryGetBoolean`, `TryGetDouble` and the verbatim `Raw` JSON, plus
`TryGetPointerDown`, `TryGetPointerSamples`, `TryGetPointerUp` and `TryGetTap` for the
[pointer family](https://docs.macro-deck.app/ui/components/modifier/#pointer-streams-and-taps). A payload is
unvalidated client data, so a getter for the wrong JSON kind returns `false` rather than throwing. Read state
with `Peek()` inside a handler so the handler does not subscribe to it.

### Declining an event

```csharp
UiEventHandler.On(UiComponentEvents.Press, _ => name.Peek().Length == 0
    ? UiEventOutcome.Rejected("Enter a name first.")
    : UiEventOutcome.Accepted),
```

A declined event is a rejected dispatch carrying your reason, which a renderer can show the user. It is not
a fault. Whatever the handler wrote before declining is still flushed, so a validation message arrives with
the refusal. A handler that throws also rejects the dispatch, and is reported on `UiView.HandlerFaulted`.

Keep validation next to the field that can fix the problem, using the input constraints and
[validation rules](https://docs.macro-deck.app/ui/views/configuration/) the DSL exposes.

### Async work

```csharp
UiEventHandler.OnAsync(UiComponentEvents.Press, async ct =>
{
    busy.Value = true;
    try { await SkipAsync(ct); }
    finally { busy.Value = false; }
}),

view.HandlerFaulted += (_, e) => Console.Error.WriteLine($"{e.NodeId}/{e.EventName}: {e.Exception}");
await view.WhenIdleAsync(); // in a test: wait for every async handler and load
```

`Dispatch` stays synchronous: an async handler is started and tracked as pending work, and the dispatch is
accepted before it finishes. Its outcome cannot reach that dispatch, so an async rejection is visible only
through the state it writes - use the synchronous overload when the refusal must be the answer. Honour the
cancellation token, and keep network or provider policy (for option loading, say) in plugin code rather than
in the UI runtime.

### What a dispatch answers

```csharp
var result = view.Dispatch(new UiEvent { NodeId = "volume.level", Name = "press" });
// Ignored: The node 'volume.level' does not accept the event 'press'.
```

| Outcome | When | Example reason |
|---|---|---|
| `Accepted` | A handler (or a writable binding) took it. Everything it changed is in one patch; a no-op advances nothing. | - |
| `Ignored` | Unknown node id, or a name the node does not accept. Never fatal - it is what a newer reader looks like to an older plugin. | `No node with id 'nope' is in the tree at revision 2.` |
| `Rejected` | Meant for this node but refused: wrong payload kind, a read-only binding, a handler that declined or threw. | `A JSON Number payload cannot be written to a 'String' value.` |

A dispatch is one batch and runs under the view's serialization, so a concurrent state write lands wholly
before or after it. A synchronous handler must therefore not block on work that writes the same view from
another thread. `Change` on a bound input needs no handler: the binding is the write path.

### Interaction only where declared

```csharp
new UiButton { Key = "idle" } // drawn, but accepts nothing
```

```json
{ "id": "idle", "type": "ui.button", "properties": {}, "children": [] }
```

The names in `Events` are exactly what the node advertises under `events`, and a reader sends an event only
where that list names it. Declaring nothing *is* disabled, and declaring some names says the rest are not
yours to receive. A modifier's `Disabled` is shorthand for exactly that - the DSL stops the subtree
declaring events - plus a dimmed look; see [Modifier](https://docs.macro-deck.app/ui/components/modifier/#disabled).

A component's own list of names is documentation, not a gate - the wire format does not stop a slider from
declaring any name. It is the reader's contract to send only what a node declared. A reader never infers
`press` from a `press-start`/`press-end` pair and never sends an undeclared name because the component type
happens to support it.

Structurally absent and hidden fields differ too: an absent field's value no longer exists or submits; a
hidden one keeps and submits its value. See [Conditional content](https://docs.macro-deck.app/ui/concepts/state-and-bindings/#conditional-content).

### Every event name

| Name | Constant | Declared by | Fires | Payload |
|---|---|---|---|---|
| `change` | `UiComponentEvents.Change` | `ui.slider`, `ui.dial`, `ui.text-field`, `ui.toggle`, `ui.segmented` | The value the user settled on - released the drag, left the field, pressed Enter, flipped the switch, chose a segment. Always sent when an interaction ends, even if equal to the last `adjust` - except on a slider with `interaction: relative`, where an interaction that never moved the level, such as a tap, sends nothing. | The value: a number, the level fraction (slider, dial); a string (text field); a boolean, the new state, read with `TryGetBoolean` (toggle); a number, the zero-based segment index, read with `TryGetDouble` (segmented) |
| `adjust` | `UiComponentEvents.Adjust` | `ui.slider`, `ui.dial`, `ui.text-field` | Continuously while the user works the control - every drag step or keystroke. At most ten a second, never after the `change` that ended it. | Same as `change` |
| `press` | `UiComponentEvents.Press` | `ui.button` | A press completed without being held past the long-press threshold. The primary name a reader implements first. | None |
| `long-press` | `UiComponentEvents.LongPress` | `ui.button` | The press was still held after 600 ms. At most once per interaction, never together with `press`. | None |
| `press-start` | `UiComponentEvents.PressStart` | `ui.button` | The press began. | None |
| `press-end` | `UiComponentEvents.PressEnd` | `ui.button` | The press ended, however it ended. Exactly one follows each `press-start`, including a cancelled gesture or the pointer leaving the element. | None |
| `double-press` | `UiComponentEvents.DoublePress` | `ui.slider`, `ui.button` | Two taps completed in quick succession. On a slider, each tap without a drag, sent after the second tap's `change`, never instead of it - on its own on a relative slider, whose taps send no `change`. On a button, or any node declaring a press name, it replaces both taps' `press`, which is held for 400 ms after each tap while it is declared. See [Button](https://docs.macro-deck.app/ui/components/button/#reader-behaviour). | None |
| `reveal` | `UiComponentEvents.Reveal` | `ui.list` | The user scrolled further down the list. At most twice a second, and only for an index beyond the furthest already sent for that list's current content; a list that loses children or has its rows replaced starts over. | Index of the furthest child in view, a number |
| `drag` | `UiComponentEvents.Drag` | any node | The pointer moved past the slop. At most ten a second. | `{"x":n,"y":n}`, translation since the start in basis fractions |
| `drag-end` | `UiComponentEvents.DragEnd` | any node | Once on release, after a `drag` began; not if the node left the tree or became disabled meanwhile. | As `drag`, the final translation |
| `swipe` | `UiComponentEvents.Swipe` | any node | On release, after a quick travel along one axis. | `"left"`, `"right"`, `"up"` or `"down"` |
| `pinch` | `UiComponentEvents.Pinch` | any node | While two pointers move. At most ten a second. | The scale since the start, a number |
| `pinch-end` | `UiComponentEvents.PinchEnd` | any node | Once, when the pinch ends; not if the node left the tree or became disabled meanwhile. | As `pinch`, the final scale |
| `pointer-down` | `UiComponentEvents.PointerDown` | any node | A finger, pen or primary mouse button went down on the node. | `{"id","x","y","t","width","height"}`, read with `TryGetPointerDown` |
| `pointer-move` | `UiComponentEvents.PointerMove` | any node | Pointers moved. At most every 16 ms, apart from the waiting samples sent at once before any other event of the family; a newer one may replace one still waiting to be delivered. | `{"samples":[{"id","x","y","t"}, ...]}`, read with `TryGetPointerSamples` |
| `pointer-up` | `UiComponentEvents.PointerUp` | any node | A pointer lifted or was cancelled. One per `pointer-down` while the node still declares it, is enabled and is in the tree. | `{"id","x","y","t"}`, plus `"cancelled":true`, read with `TryGetPointerUp` |
| `tap` | `UiComponentEvents.Tap` | any node | After the last `pointer-up` of a quick touch that did not move, with one or more fingers. | `{"pointers":n}`, read with `TryGetTap` |

The thresholds and which of two nested nodes gets a gesture are on [Modifier](https://docs.macro-deck.app/ui/components/modifier/#gestures),
and the pointer family's rules on [Pointer streams and taps](https://docs.macro-deck.app/ui/components/modifier/#pointer-streams-and-taps).

Configuration inputs use `change` from `UiConfigEvents`. An action list that lets the user adopt a provider
action also raises `provide`; see [Widget configuration](https://docs.macro-deck.app/ui/views/widget-configuration/#letting-the-user-adopt-a-provider-action). See the [component reference](https://docs.macro-deck.app/ui/components/) for
each component's geometry and semantics, and [Modal views](https://docs.macro-deck.app/ui/views/modal/) for `modal.complete`, the one
event that is not a component interaction but the answer that ends a dialog.

#### Links

A `UiLink` with an external `http` or `https` URL is opened by the host in the user's default browser,
never inside the surface, whether or not the link declares `activate`. Declaring `activate` only tells your
plugin that the link was followed: the event arrives in addition to the host opening the URL, so a handler
must not open the URL itself. A link to the app's own origin, or to any other scheme, is not opened this
way.

:::caution[Behaviour change in hosts released after 3.0.0-beta.6]
Up to 3.0.0-beta.6, the desktop app opened a link that declared `activate` only inside the integration setup
dialog. Anywhere else the plugin received the event and nothing opened. If your handler opened the URL
itself to work around that, remove that code: the host now opens it and the handler would open a second
tab.
:::

### See also

- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)
- [Reactive updates](https://docs.macro-deck.app/ui/concepts/reactive-updates/)
- [Button](https://docs.macro-deck.app/ui/components/button/)
- [Slider](https://docs.macro-deck.app/ui/components/slider/)

## Reactive updates

> Source: https://docs.macro-deck.app/ui/concepts/reactive-updates/
>
> How the runtime turns a state change into a patch, and the threading rules that make concurrent writes to a view safe.

Write state; the view compiles each change into the smallest patch that describes it.

### Example

```csharp
var view = new UiView(surface, root); // the volume view from State and bindings, at revision 0
view.Changed += (_, _) => Send(view.DrainPatches());

volume.Value = 0.55;
```

```json
[{ "fromRevision": 0, "toRevision": 1, "operations": [
  { "op": "set-properties", "nodeId": "volume.readout", "properties": { "text": "55%" } },
  { "op": "set-properties", "nodeId": "volume.level", "properties": { "level": 0.55 } } ] }]
```

Only the two cells that read `volume` re-evaluated. Each emits one `set-properties` listing only the keys
whose value changed. Update state rather than keeping a diff layer of your own.

### Property changes

```csharp
muted.Value = true;
```

```json
{ "op": "set-properties", "nodeId": "volume.readout", "properties": { "text": "Muted" } }
```

- One `set-properties` per affected node, listing only changed keys; a value turned absent is listed in
  `removedProperties`.
- Only the spine from the root to the changed nodes is rebuilt; every untouched subtree stays the same
  `UiNode` instance, never re-allocated or re-serialized.
- A write that changes nothing - an equal value, or a re-evaluation producing the same output - enqueues
  nothing and advances no revision. An empty patch would be inapplicable.

### Structural changes

```csharp
// before: [t1 Intro, t2 Verse, t3 Outro]
tracks.Value = [("t3", "Outro"), ("t1", "Intro"), ("t4", "Bridge")];
showHeader.Value = false;
```

```json
[{ "fromRevision": 0, "toRevision": 1, "operations": [
   { "op": "remove-node", "nodeId": "queue.t2" },
   { "op": "move-node", "nodeId": "queue.t3", "parentId": "queue", "index": 1 },
   { "op": "insert-node", "nodeId": "queue.t4", "parentId": "queue",
     "node": { "id": "queue.t4", "type": "ui.text", "properties": { "text": "Bridge" }, "children": [] } } ] },
 { "fromRevision": 1, "toRevision": 2, "operations": [
   { "op": "remove-node", "nodeId": "queue.header" } ] }]
```

A `UiWhen` that flipped or a `UiRepeat` whose list was replaced re-materializes only the run of its parent's
children it owns, and diffs that run by id:

| Operation | Emitted for |
|---|---|
| `remove-node` | The top-most node of each removed subtree. |
| `move-node` | A surviving node that changed position. |
| `insert-node` | New content, at its rendered index (omitted index = append). |
| `replace-node` | A node whose type changed. |
| `set-properties` | Each surviving node whose properties differ. |

A surviving node keeps its id, and with it focus and in-flight edits. A condition that re-evaluates to the
same boolean, or an item list that is still the same instance, emits nothing. See
[Patches](https://docs.macro-deck.app/ui/reference/patches/) for how a reader applies each operation.

### Batching

```csharp
using (view.Batch())
{
    volume.Value = 0.8;
    muted.Value = false;
}
```

```json
[{ "fromRevision": 2, "toRevision": 3, "operations": [
  { "op": "set-properties", "nodeId": "volume.level", "properties": { "level": 0.8 } },
  { "op": "set-properties", "nodeId": "volume.readout", "properties": { "text": "80%" } } ] }]
```

Without the batch, the same two writes produce two patches and two revisions. A batch coalesces everything
written inside it into one patch, one revision and one `Changed`. Batches nest, and only the outermost one
flushes. Two writes that must land together belong in one batch.

A batch belongs to the view, not to the thread that opened it: concurrent batches on one view coalesce into
a single patch, one thread's open batch defers the other's flush, and the scope may be disposed on another
thread. Every `Dispatch` is already one batch.

### Draining

```csharp
view.Changed += (_, _) =>
{
    foreach (var patch in view.DrainPatches()) Send(patch);
};
```

Each flush that changed something advances `Revision` by one and queues one patch. `DrainPatches` returns
everything queued since the last call and clears the queue; it is safe from any thread and from inside
`Changed`, and two concurrent calls neither lose nor duplicate a patch. `view.Tree` is the current tree.
When serving a session, the host drains for you - see [Serving a view](https://docs.macro-deck.app/ui/views/sessions/).

### Threads

Write state from whatever thread your work finished on. A timer, a `ConfigureAwait(false)` continuation and a
client's dispatch may all reach one view at once; the runtime serializes a view together with every state it
reads and every other view those states reach, so you need no lock of your own around `UiState.Set`,
`Dispatch` or `DrainPatches`. Views that share no state run in parallel, so a slow provider in one session
does not hold up another.

- **Value providers, conditions, templates, synchronous handlers and `Bind.Custom` setters run under that
  serialization.** They must return promptly and must never block on work that has to write the same view
  from another thread - that deadlocks. Put asynchronous work in a state a synchronous provider reads.
- **`Changed` and `HandlerFaulted` are raised on the thread that did the work**, not on a pump, after the
  patch is queued. A subscriber may read the tree, drain, write state and dispatch again; marshal to your own
  thread if you need one.
- **A write can run another view's flush on your thread before it returns** when a shared state connects the
  two views, so any lock you hold across `Set` is a lock a value provider runs under.

### Disposing

```csharp
view.Dispose();
```

A state keeps every view that reads it reachable. When the state outlives the view - it belongs to your
provider or service, or several sessions share it - the view stays in memory after its session closed, and
every later write still re-evaluates its values and queues a patch nobody drains. `Dispose` detaches the view
from every state it reads. Dispose the view when the session that serves it closes; `ViewSession` in
[Serving a view](https://docs.macro-deck.app/ui/views/sessions/#example) does it in `DisposeAsync`.

- **Idempotent and safe from any thread,** including from a handler, a value provider or a `Changed`
  subscriber. Called while another view's work runs on your thread, the release happens as soon as that
  work returns.
- **Nothing throws afterwards.** `Dispatch` ignores every event, `DrainPatches` returns nothing, and `Tree` and
  `Revision` keep the last tree, so a host racing a dispatch against closing the session needs no guard.
- **Nothing is raised afterwards.** `Changed` and `HandlerFaulted` stop, including for an asynchronous handler
  that faults later, and `WhenIdleAsync` no longer waits for work still running.
- **Other views are unaffected.** A view that shares the state keeps receiving its patches.

A live view also lets go of a state once none of its values read it any more, for example when the content
that read it is removed. A state read directly by a `UiWhen` condition or content, or by a `UiRepeat` item
list or template, stays attached until that conditional or repeat is itself removed or the view is disposed.
`WhenIdleAsync` does not wait for a `UiAsyncState` load the view is not reading; once the view reads that
state again, it waits for a load still running.

### See also

- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [Patches](https://docs.macro-deck.app/ui/reference/patches/)
- [Serving a view](https://docs.macro-deck.app/ui/views/sessions/)

## Sizing

> Source: https://docs.macro-deck.app/ui/concepts/sizing/
>
> Every length in a Macro Deck UI tree is a fraction of the view's size, so one tree is correct at every box size.

Every length is a fraction of the view's **basis** - the smaller side of its content box - so one tree is
correct at any size and a resize never costs a round-trip. (For device layout descriptors, see
[Layout providers](https://docs.macro-deck.app/features/layouts/).)

### Example

```csharp
new UiStack
{
    Key = "card",
    Justify = UiComponentJustify.SpaceBetween,
    Padding = safeArea,
    Children =
    [
        new UiStack
        {
            Key = "header",
            Direction = UiComponentDirections.Horizontal,
            Children =
            [
                new UiTextRun { Key = "room", Text = "Office", Size = 0.1, Fill = true },
                new UiTextRun { Key = "time", Text = "14:05", Size = 0.1, MainSize = 0.3, Align = UiComponentAlignments.End },
            ],
        },
        new UiTextRun { Key = "value", Text = "21.5°", Size = 0.3, Weight = UiComponentTextWeights.Bold },
        new UiTextRun { Key = "caption", Text = "Humidity 48 %", Size = UiSize.Capped(0.1, 12) },
    ],
}
```

*[Image: A one-cell tile: Office and 14:05 across the top, a large bold 21.5° in the middle, Humidity 48 % at the foot]*

A bare `double` is a fraction of the basis: `Size = 0.3` is a font 0.3 times the basis.

### One tree at three sizes

*[Image: The same tile two cells wide: the text keeps its size and the header spreads to both edges]*

*[Image: The same tile two cells by two: every text doubles except the capped caption, which stays the size it was on one cell]*

The same tree at 2x1 and 2x2. A 2x1 tile has the same basis as a 1x1 one, so only the filling header
grows. At 2x2 the basis doubles and so does every length - except the caption, whose cap stops it at 12
reference units.

### Capping a length

```csharp
Size = UiSize.FromBasis(0.144, 1.2)   // min(0.144 x basis, 1.2 x the stack's cross extent)
Size = UiSize.Capped(0.11, 13)        // min(0.11 x basis, 13 reference units)
```

`FromBasis(basis, maxOfCross)` stops a length outgrowing the row or column it sits in, such as a forecast
row's text once many rows share the height. `Capped(basis, extent)` stops it growing past a fixed size, so
a caption reads the same on a one-cell widget and a nine-cell one. A length carrying both caps resolves to
the smallest of the three.

The cap unit is `UiLength.Cell` (`120`): one deck cell in the reference space a deck widget is laid out in.
It is a definition, not a measurement - a reader lays the widget out in that space and scales the result to
the real cell - so it only has to agree across the wire, never with any device's pixels.

### Relative to the containing box

A fraction of the widget cannot size a part of a widget whose box depends on the widget's shape: a ring in a
grid of rings, whose stroke, icon and percentage have to scale with the ring. `UiLength.OfParent` is a
fraction of the **containing box** instead - the smaller side of the box the node's parent lays it out
within.

```csharp
new UiGrid
{
    Key = "rings",
    Columns = 4,                              // what a reader that cannot choose draws
    MinCellSize = UiLength.OfBasis(0.25),     // the reader chooses the columns
    Children = devices.Select(device => new UiLayer
    {
        Key = $"ring.{device.Id}",
        Children =
        [
            new UiGauge { Key = $"gauge.{device.Id}", Level = device.Level, Thickness = UiLength.OfParent(0.085, 0.01) },
            new UiIcon { Key = $"icon.{device.Id}", Icon = "battery", Size = UiLength.OfParent(0.3, 0.05) },
            new UiTextRun { Key = $"percent.{device.Id}", Text = $"{device.Percent} %", Size = UiLength.OfParent(0.18, 0.03) },
        ],
    }).ToArray(),
}
```

One tree draws the same rings at any widget size and shape, each device once: the plugin never learns the
size, and a resize costs no round-trip.

The containing box is, per parent:

| Parent | Containing box of its child |
|---|---|
| Grid | The cells the child spans, with the gaps between them |
| Layer, transform, responsive, first fit | The parent's own box |
| Stack | The stack's content box: its box minus its padding |
| Modifier | The modifier's frame box minus its padding |
| List | None - the scroll axis is open |

A length is `ParentFraction x min(width, height)` of that box in place of the `Basis` term, and
`MaxOfCross` and `MaxOfCell` still clamp the result. At the root of a view, a missing box counts as the
basis square.

**When the box is not definite.** Both sides of the containing box must be known. A child of a stack that
has neither `MainSize` nor `Fill` sits in an open main extent, so its children have no definite box; the
same goes for a list's children, and a grid under such a child. There the length resolves from `Basis`
against the widget instead, in measuring and in drawing alike. Give the node `MainSize` or `Fill` when a
length relative to its box is to work inside it.

**What older readers draw.** A reader that does not know `ofParent` ignores it and resolves `Basis` against
the widget, so pass the value that reads acceptably there as the second argument of
`UiLength.OfParent(fraction, fallbackBasis)`. The one-argument form uses the fraction itself, which on a part
of a small cell is far too large. There is no way to ask a reader whether it knows the member; for a real
older-reader picture, give the node a `Fallback` with a component version, as
[stack overflow](https://docs.macro-deck.app/ui/components/stack-and-layer/) does. When a helper copies a length, use `with` rather than
rebuilding it member by member, or the member is dropped.

### Sharing a row: `Fill` and `MainSize`

```csharp
new UiTextRun { Key = "name", Text = "Living room", Size = 0.14, Fill = true },
new UiTextRun { Key = "temp", Text = "21°", Size = 0.14, MainSize = 0.3, Align = UiComponentAlignments.End },
```

*[Image: Wrong: without MainSize the temperature is pushed to the edge and cut to 2...]*

*[Image: Right: with MainSize = 0.3 the temperature has its own slot and reads 21°]*

`MainSize` is a child's extent along its parent's main axis; `Fill` takes whatever the siblings leave,
split evenly between filling children, and a child with a `MainSize` ignores `Fill`. A child with neither
is measured without a font: an image is its `Size`, a text is its line height across the stack and
**nothing along it**. So give every text in a row its own `MainSize` whenever a sibling fills - top
picture without it, bottom with it.

`Size` (the font) and `MainSize` (the slot) are different properties; set both on a text in a row.

### When the children do not fit

A stack whose children ask for more than its box shrinks them to share the shortfall, so nothing leaves
the box. A stack that should keep its newest children whole instead - a chat feed, a log - sets
`Overflow = UiComponentOverflows.ClipStart`: its children keep their natural size, `Fill` on them is
ignored, and the first ones are cut off at the start. It still reports the sum of its children as its own
size, so give it `Fill` or a `MainSize` from its parent. It needs component version 2 and a fallback - see
[Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/#keeping-the-newest-children-at-the-end).

### Gap and padding

```csharp
new UiStack { Key = "card", Padding = UiSize.FromBasis(0.06), Gap = UiSize.FromBasis(0.03), Children = [title, body] }
```

`Padding` insets every edge, `Gap` separates neighbours. Both are lengths like any other; absent means none.

### Frames and wrapping

```csharp
new UiModifier
{
    Key = "art",
    Fill = true,
    Frame = new UiFrame { MaxWidth = UiLength.OfBasis(0.6), AspectRatio = 1 },
    Child = new UiImage { Key = "cover", Source = cover },
}
```

A [modifier](https://docs.macro-deck.app/ui/components/modifier/) with a `Frame` fixes or clamps its own box and centres it in the
space it is given; `Padding` on a modifier insets its one child. Wrapping moves the child's slot to the
wrapper: `MainSize`, `Fill`, `ColumnSpan` and `RowSpan` go on the `UiModifier`, and a wrapped child that
sets them is rejected when the view is built. A filling wrapper's maximum clamps only its own size - the
space it gives up is not redistributed to its siblings.

### Changing the layout with the size

Everything above scales one layout. When a 2x1 tile should put the icon beside the text instead of above it,
or a folder view should show more on a tablet than on a phone, give each size its own layout with
[`UiResponsive`](https://docs.macro-deck.app/ui/components/responsive/): the reader draws the one whose condition holds for the box, and
switches when the box changes. To choose by what the text needs rather than by the box, use
[`UiFirstFit`](https://docs.macro-deck.app/ui/components/first-fit/): the reader draws the first layout whose texts fit.

### Reference

| Length | Resolves to |
|---|---|
| `0.2` / `UiSize.FromBasis(0.2)` / `UiLength.OfBasis(0.2)` | `0.2 x basis` |
| `UiSize.FromBasis(0.2, 0.5)` | `min(0.2 x basis, 0.5 x containing stack's cross extent)` |
| `UiSize.Capped(0.2, 20)` | `min(0.2 x basis, 20 reference units)` - `MaxOfCell = 20 / UiLength.Cell` |
| `UiLength.OfParent(0.1, 0.01)` / `UiSize.FromParent(0.1, 0.01)` | `0.1 x` the smaller side of the containing box; `0.01 x basis` where that box is not definite or the reader does not know the member |
| `UiSize.From(() => ...)` / `UiSize.Optional(...)` | computed each evaluation / may be absent |

| Property | On | Meaning |
|---|---|---|
| `Size` | text, image, time and progress text | Font size, or an image's extent. `MinSize` is the floor a text may shrink to before it ellipsizes. |
| `MainSize` | every element | Extent along the parent stack's main axis. Wins over `Fill`. |
| `Fill` | every element | Takes an even share of the parent's leftover main-axis space. |
| `Gap`, `Padding` | stack, button, list | Space between children, and inside every edge. |
| `Padding`, `Frame` | modifier | Inset of the one child, and the wrapper's own fixed or clamped box. |
| `Thickness` | slider, range and progress bar | Extent on the cross axis. |

Reader rules:

- A reader that cannot determine the containing stack's cross extent ignores `MaxOfCross` rather than
  guessing.
- A reader that cannot determine a definite containing box, or whose parent is a list, resolves `ParentFraction`
  from `Basis` against the widget, and does so in measuring as well as in drawing.
- `MaxOfCell` only means something where a deck cell grid exists. A reader laying a view out on anything
  else - a folder view, a browser window, a dialog - ignores it.
- `MainSize` and `Fill` mean nothing on a [layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)'s children: each gets the
  whole box.

### See also

- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [Text](https://docs.macro-deck.app/ui/components/text/) - `Digits`, `MinSize`, wrapping
- [Chart](https://docs.macro-deck.app/ui/components/chart/) - normalised points and `PlotTop`
- [Theming](https://docs.macro-deck.app/ui/concepts/theming/)

## State and bindings

> Source: https://docs.macro-deck.app/ui/concepts/state-and-bindings/
>
> UiState, the binding kinds a property accepts, and how conditional and repeated content stay part of the tree.

Put mutable values in `UiState<T>`, read them inside the view, and the runtime keeps the tree in step.

### Example

```csharp
var volume = new UiState<double>(0.4);
var muted = new UiState<bool>(false);

var root = new UiStack
{
    Key = "volume",
    Gap = 0.04,
    Children =
    [
        new UiTextRun
        {
            Key = "readout",
            Text = UiText.From(() => muted.Value ? "Muted" : $"{volume.Value * 100:0}%"),
        },
        new UiSlider
        {
            Key = "level",
            Level = UiValue.From(() => volume.Value),
            Events =
            [
                UiEventHandler.On(UiComponentEvents.Adjust, e =>
                {
                    if (e.TryGetDouble(out var level)) volume.Value = level;
                }),
                UiEventHandler.On(UiComponentEvents.Change, e =>
                {
                    if (e.TryGetDouble(out var level)) { volume.Value = level; muted.Value = level == 0; }
                }),
            ],
        },
    ],
};

var view = new UiView(surface, root);
```

The readout reads `volume` and `muted`, so it re-evaluates when either changes; the slider's level reads
only `volume`. Dragging the slider to `0.55` produces exactly this patch:

```json
{ "fromRevision": 0, "toRevision": 1, "operations": [
  { "op": "set-properties", "nodeId": "volume.readout", "properties": { "text": "55%" } },
  { "op": "set-properties", "nodeId": "volume.level", "properties": { "level": 0.55 } } ] }
```

### Reading and writing state

```csharp
var name = new UiState<string>(string.Empty);
var tag = new UiState<string>(string.Empty, StringComparer.OrdinalIgnoreCase);

string shown = name.Value;   // inside the view: records a dependency
string current = name.Peek(); // in a handler: reads without subscribing
name.Value = "Studio";       // same as name.Set("Studio")
```

- **Reading `Value` during a build records a dependency.** Writing invalidates only the parts of the view
  that read it.
- **Use `Peek()` in handlers and tests.** Reading `Value` there would subscribe whichever cell happens to
  be evaluating.
- **An equal write is free**, compared with the state's comparer (the default, or one you pass): nothing
  re-evaluates, no revision advances, no `Changed` fires.
- **Attachment is lazy.** A state no view has read yet just updates in place.
- **Any thread may read or write.** See [Threads](https://docs.macro-deck.app/ui/concepts/reactive-updates/#threads).

### Derived values

```csharp
Level = UiValue.From(() => volume.Value),
Text = UiText.From(() => muted.Value ? "Muted" : $"{volume.Value * 100:0}%"),
Background = UiValue.Optional(() => accent.Value is { } colour ? colour : UiValue.None<string>()),
```

| Factory | Produces |
|---|---|
| a plain value, or `UiValue.Of(value)` | A constant. Use `Of` when `T` is an interface. |
| `UiValue.From(() => ...)` | A value re-evaluated whenever a state it read changes. |
| `UiValue.Optional(() => ...)` | A value whose presence is decided on each evaluation. |
| `UiValue.None<T>()` / `default` | An absent property - omitted from the node. |
| `UiText.From`, `UiText.FromLocalized`, `UiText.Optional` | The same for text, including localized strings. |

An absent property and an explicit JSON `null` are different states. When an optional value turns absent the
runtime removes the key:

```json
{ "op": "set-properties", "nodeId": "card", "removedProperties": ["background"] }
```

### Binding an input

```csharp
new UiConfigStack
{
    Key = "settings",
    Children =
    [
        new UiStringInput { Key = "label", Label = "Label", Binding = Bind.To(label) },
        new UiStringInput
        {
            Key = "host",
            Label = "Host",
            Binding = Bind.Custom(() => settings["host"], value => settings["host"] = value),
        },
        new UiStringInput { Key = "id", Label = "Id", Binding = Bind.ReadOnly(UiValue.Of("abc-123")) },
    ],
}
```

```json
{ "id": "label", "type": "string", "properties": { "events": ["change"], "label": "Label", "value": "Volume" } }
{ "id": "host",  "type": "string", "properties": { "events": ["change"], "label": "Host", "value": "localhost" } }
{ "id": "id",    "type": "string", "properties": { "label": "Id", "value": "abc-123" } }
```

| Binding | Reads | Writes |
|---|---|---|
| `Bind.To(state)` | `state.Value` | `state.Value = v` |
| `Bind.Custom(get, set)` | `get()` | `set(v)` - for a value backed by another source |
| `Bind.ReadOnly(value)` | `value` | Nothing. The node advertises no `change`, and a `change` sent anyway is rejected. |

A writable binding is the input's write path, so a `change` event needs no handler. Bindings belong to
configuration inputs (`UiInput<T>`); a component such as `UiSlider` or `UiTextField` takes a value plus
[events](https://docs.macro-deck.app/ui/concepts/events/) instead.

### Conditional content

```csharp
new UiWhen
{
    Key = "header-when",
    Condition = () => showHeader.Value,
    Content = () => new UiTextRun { Key = "header", Text = "Up next" },
}
```

When the condition turns false the content leaves the tree (`remove-node`); a condition re-evaluated to the
value it already had emits nothing. `UiWhen` adds no id segment of its own.

Use `UiWhen` when content should not exist at all. Use an input's `VisibleWhen` when a field should stay in
the tree and keep, and submit, its value while hidden.

### Repeated content

```csharp
new UiRepeat<(string Id, string Title)>
{
    Key = "tracks",
    Items = UiValue.From(() => tracks.Value),
    KeySelector = track => track.Id,
    Template = (track, key) => new UiTextRun { Key = key, Text = track.Title },
}
```

`KeySelector` must identify the logical item across inserts, removals and reordering - never its position.
`Template` receives the composed item key; use it as the element's `Key`. An absent `Items` renders nothing,
and assigning the same list instance again emits nothing. See
[Reactive updates](https://docs.macro-deck.app/ui/concepts/reactive-updates/#structural-changes) for the patch a reorder produces.

### See also

- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [Reactive updates](https://docs.macro-deck.app/ui/concepts/reactive-updates/)
- [The UI model](https://docs.macro-deck.app/ui/concepts/ui-model/#node-ids-from-keys)

## Theming

> Source: https://docs.macro-deck.app/ui/concepts/theming/
>
> Theme roles versus literal colours, and how text carries localization and typeface across a Macro Deck UI tree.

Name a **role** for anything the theme owns, and send a literal `#rrggbb` only for a colour that is data.

### Example

```csharp
new UiStack
{
    Key = "status",
    Justify = UiComponentJustify.Center,
    Gap = 0.03,
    Padding = safeArea,
    Children =
    [
        new UiTextRun { Key = "name", Text = "Studio mic", Size = 0.12, Weight = UiComponentTextWeights.SemiBold },
        new UiTextRun { Key = "state", Text = "Live", Size = 0.1, Color = "#34c759" },
        new UiTextRun { Key = "source", Text = "Input 2 - USB interface", Size = 0.08, Role = UiComponentTextRoles.Secondary },
        new UiTextRun { Key = "updated", Text = "Updated 2 min ago", Size = 0.07, Role = UiComponentTextRoles.Muted },
        new UiSlider { Key = "level", Level = 0.6, MainSize = 0.16, Thickness = UiSize.FromBasis(0.06) },
    ],
}
```

*[Image: A dark tile: Studio mic in white, Live in green, two lines of grey detail and a blue slider]*

*[Image: The same tree in the light theme: the text roles and the background invert, Live stays green and the slider stays blue]*

The same tree in the dark and light theme. Roles repaint with no help from your view; the literal green
does not; the slider has no `LevelColor`, so it paints the reader's own accent colour.

### Roles

| Role | Dark | Light | For |
|---|---|---|---|
| `UiComponentTextRoles.Primary` (`primary`) | `#ffffff` | `#121212` | The most prominent text. The default. |
| `UiComponentTextRoles.Secondary` (`secondary`) | `#a0a0a0` | `#666666` | Supporting detail. |
| `UiComponentTextRoles.Muted` (`muted`) | `#666666` | `#999999` | Incidental detail. |
| Accent (no role name - omit the colour) | user's choice | user's choice | The same in both themes. |

Values are the built-in themes' current tokens, shown for orientation: a reader resolves roles against its
own live theme, so do not copy them into your tree. Resolving the accent to hex and sending that would
freeze it against the reader's theme.

### Literal colours

```csharp
Color = "#34c759"        // accepted
Color = "#34c759b3"      // accepted: 70 % opaque
Color = "#3c5"           // rejected: treated as absent
Color = "green"          // rejected: treated as absent
```

Send a literal only where the colour is data - a value's colour, or one a person picked - which must not
change when the reader switches theme. A reader accepts exactly `#` plus six hex digits, or eight with the
alpha last (`#rrggbbaa`, wherever the table below says `#rrggbb`), and rejects any other spelling rather than
passing it to its styling layer, so the property behaves as if omitted. A reader from before eight digits,
such as an older Companion app, treats them as absent, so send one only where the theme's colour is an
acceptable fallback.

| Property | Takes | Omitted means |
|---|---|---|
| `UiTextRun.Role` | a role | `primary` |
| `UiTextRun.Color` | `#rrggbb`, overrides `Role` | the role decides |
| `UiStack.Background`, `UiList.Background` | `#rrggbb` | paints nothing |
| `UiButton.Background` | `#rrggbb` | the reader's accent colour |
| `UiButton.BorderColor` | `#rrggbb` | the border style supplies its own colour |
| `UiSlider.LevelColor` | `#rrggbb` | the reader's accent colour |
| `UiGauge.LevelColor` | `#rrggbb` | the reader's accent colour |
| `UiGauge.TrackColor` | `#rrggbb` | the reader's tertiary surface colour |
| `UiChart.Color` | `#rrggbb` | the reader's accent colour |
| `UiProgressBar.StartColor`, `.EndColor` | `#rrggbb` | the reader's accent colour, each end on its own |
| `UiRangeBar.StartColor`, `.EndColor` | `#rrggbb` | no fill; the span needs both |
| `UiDynamicText.Role` / `.Color`, `UiProgressText.Role` | as `UiTextRun` | as `UiTextRun` |
| `UiClockDial.Color` | `#rrggbb` for the text-coloured marks | the marks keep the theme colours |
| `UiModifier.Background` | `#rrggbb`, or a linear or radial gradient of `#rrggbb` stops | the node's own background |
| `UiModifier.BorderColor` | `#rrggbb` | the reader's choice |

A gradient is data like any other literal: each stop is `#rrggbb` and none of them follows the theme.

A view paints no background unless a stack, list, button or modifier sets one; the surface behind it
belongs to the reader and follows its theme.

### Text

```csharp
new UiTextRun { Key = "title", Text = localizedTitle, Wrap = true, FontFace = fontId }
```

`Text` should be a localization reference, not a resolved string: `UiText` accepts a `LocalizedString`
and each client resolves it in its own language, so one shared session serves clients in different
languages and a language change is a client-side re-render.

Without `Wrap` a run stays on one line and ellipsizes, which is also what a reader that does not know the
key does. `FontFace` names a face in Macro Deck's font catalogue - an identifier, not a resource handle.
The catalogue holds the fonts installed on the host's computer and the fonts the user imported, and an
imported face can be removed while the host runs.
A reader holds the run back until the face is usable instead of swapping from a fallback, and shows it in
its default face if the face never arrives or cannot be resolved.

### See also

- [Localization](https://docs.macro-deck.app/features/localization/) - the catalogues `LocalizedString` draws from
- [Resources](https://docs.macro-deck.app/ui/reference/resources/) - how a `FontFace` identifier differs from a `UiResource`
- [Text](https://docs.macro-deck.app/ui/components/text/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## The UI model

> Source: https://docs.macro-deck.app/ui/concepts/ui-model/
>
> The transport-neutral tree, keys and identity, and how a client and a provider agree on a model version.

Every Macro Deck view is a tree of plain JSON nodes; the C# DSL is one way to produce it.

### Example

```csharp
var surface = new UiSurface { Kind = UiSurfaceKinds.Widget, SessionMode = UiSessionModes.Shared };
var volume = new UiState<double>(0.4);

var root = new UiStack
{
    Key = "volume",
    Gap = 0.04,
    Children =
    [
        new UiTextRun { Key = "readout", Text = UiText.From(() => $"{volume.Value * 100:0}%") },
        new UiSlider
        {
            Key = "level",
            Level = UiValue.From(() => volume.Value),
            Events = [UiEventHandler.On(UiComponentEvents.Change, e =>
            {
                if (e.TryGetDouble(out var level)) volume.Value = level;
            })],
        },
    ],
};

UiTree tree = UiViewBuilder.Build(surface, root);
string json = UiCanonicalJson.Serialize(tree);
```

```json
{
  "revision": 0,
  "surface": { "kind": "widget", "sessionMode": "shared", "attributes": {} },
  "root": {
    "id": "volume",
    "type": "ui.stack",
    "properties": { "gap": { "basis": 0.04 } },
    "children": [
      { "id": "volume.readout", "type": "ui.text", "properties": { "text": "40%" }, "children": [] },
      { "id": "volume.level", "type": "ui.slider", "properties": { "events": ["change"], "level": 0.4 }, "children": [] }
    ]
  }
}
```

Keys became dot-joined ids, every value was read once, and the handler became nothing more than the name
`change` in the node's `events`. `UiViewBuilder.Build` gives a one-off tree at revision 0; use a
[`UiView`](https://docs.macro-deck.app/ui/concepts/reactive-updates/) for a tree that keeps up with its state.

### A node

```csharp
new UiSlider
{
    Key = "level",
    Level = UiValue.From(() => volume.Value),
    RequiredComponentVersion = 2,
    Fallback = new UiTextRun { Key = "level-text", Text = UiText.From(() => $"{volume.Value * 100:0}%") },
    Events = [/* change handler as above */],
}
```

```json
{
  "id": "volume.level",
  "type": "ui.slider",
  "requiredComponentVersion": 2,
  "properties": { "events": ["change"], "level": 0.4 },
  "children": [],
  "fallback": { "id": "volume.level-text", "type": "ui.text", "properties": { "text": "40%" }, "children": [] }
}
```

| Member | Meaning |
|---|---|
| `id` | Stable, unique across the whole tree, including inside `fallback` subtrees. |
| `type` | The component name, an open vocabulary (`ui.stack`, `macrodeck.progress-bar`, ...). The core model declares and validates none. |
| `requiredComponentVersion` | The component version the node needs. Omitted means `1`; the DSL emits it only when you set `RequiredComponentVersion`. |
| `properties` | Arbitrary, unvalidated JSON for the type to interpret. Always written, even when empty. |
| `children` | In render order. Always written, even when empty. |
| `fallback` | What a reader draws instead when it does not support `type`. Omitted when absent. |

- **Unknown types never fail.** A reader that does not recognise a type, or whose declared range for it does
  not cover `requiredComponentVersion` exactly (never clamped), renders `fallback`, negotiating it in turn.
  With no fallback it renders nothing for that node and its children and carries on with the rest of the
  tree. This is what lets the vocabulary grow without breaking older renderers or plugins.
- **Properties are unvalidated.** Check a value's JSON kind before reading it: `"37.5"` can arrive where a
  number belongs. A property explicitly set to `null` is not the same as an absent one; a patch removes a
  key through `removedProperties`.
- **An input's id is the field name it submits as**, so submission stays keyed by name whichever path
  rendered it.

### Node ids from keys

```csharp
new UiStack
{
    Key = "queue",
    Children =
    [
        new UiWhen { Key = "header-when", Condition = () => showHeader.Value,
                     Content = () => new UiTextRun { Key = "header", Text = "Up next" } },
        new UiRepeat<(string Id, string Title)>
        {
            Key = "tracks",
            Items = UiValue.From(() => tracks.Value),
            KeySelector = track => track.Id,
            Template = (track, key) => new UiTextRun { Key = key, Text = track.Title },
        },
    ],
}
```

```text
queue            ui.stack
├─ queue.header  ui.text   "Up next"
├─ queue.t1      ui.text   "Intro"
├─ queue.t2      ui.text   "Verse"
└─ queue.t3      ui.text   "Outro"
```

Keys are public behaviour: supply stable ones yourself.

- A structural node's id is the dot-joined path of keys from the root, including the root's own key.
- `UiWhen` and `UiFragment` are transparent: no node, no path segment. Wrapping an element never changes
  its id - `header-when` and `tracks` appear nowhere above.
- `UiRepeat` is transparent too; each item takes its `KeySelector` key as if it stood directly at the
  repeat's position. Use a stable item key, never an index.
- A top-level input's id is its bare key with no prefix (`label`, not `settings.label`), so submission
  matches field-based configuration. Inside an object or array input container the id is
  `containerId.key`, and nesting composes.
- Every composed id is validated as an identifier, and must be unique across the tree. A failure or a
  duplicate throws `UiViewException` naming the id (and, for a duplicate, both declaration paths).

Never derive ids from position. Reordering must keep surviving items' ids so focus, in-flight edits and
`move-node` patches stay meaningful.

### Revisions

```json
{ "fromRevision": 0, "toRevision": 1, "operations": [ { "op": "set-properties", "nodeId": "volume.readout", "properties": { "text": "55%" } } ] }
```

A tree is built at revision 0, and every accepted patch advances it by exactly one. A patch applies only when
the reader's current revision equals `fromRevision`, `toRevision` is greater, and `operations` is non-empty.
It applies atomically: if any operation cannot apply, the reader discards the whole patch and asks for a full
tree - a resync, never an exception or a closed session. See [Patches](https://docs.macro-deck.app/ui/reference/patches/).

### The three packages

| Package | Use it for |
|---|---|
| `MacroDeck.Ui.Model` | The tree, patch, event and resource contracts on this page. Depend on it alone to build or patch a tree by hand. |
| `MacroDeck.Ui` | The C# DSL and reactive runtime that produce and patch a tree from `UiState`. See [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/). |
| `MacroDeck.Ui.Testing` | A headless renderer and test host for either. See [Custom views](https://docs.macro-deck.app/ui/views/custom/#testing-it). |

All three are public NuGet contracts; see [Compatibility](https://docs.macro-deck.app/ui/reference/compatibility/).

### Model-version negotiation

```csharp
var result = UiCapabilityNegotiator.NegotiateModelVersion(new UiCapabilities
{
    UiProtocol = new UiVersionRange { Minimum = 3, Maximum = 9 },
    SupportsAllComponents = true,
});
// IsSupported = true, NegotiatedVersion = 4
// with Minimum = 1, Maximum = 2: IsSupported = false, FallbackReason = "No overlapping UI model version."
```

The negotiated version is `min(reader max, UiModelVersions.Current)`, and negotiation fails when that falls
below `max(reader min, UiModelVersions.Minimum)`. Today `Minimum` is 3 and `Current` is 4.

A client negotiates the model version with the host **before** any session is opened, not per tree. Declining
is therefore cheap: no session is opened and no slot is held, and the client falls back to the surface's
non-tree representation (declared fields for configuration, the built-in grid for a folder). The host opens
each session at `Current` and honours whatever version the provider negotiates down to. Failure is never
fatal. See [Serving a view](https://docs.macro-deck.app/ui/views/sessions/) for the session lifecycle, and
[Compatibility](https://docs.macro-deck.app/ui/reference/compatibility/) for the version history.

### See also

- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)
- [Reactive updates](https://docs.macro-deck.app/ui/concepts/reactive-updates/)
- [Patches](https://docs.macro-deck.app/ui/reference/patches/)

## Compatibility

> Source: https://docs.macro-deck.app/ui/reference/compatibility/
>
> The three packages as versioned contracts, why the model major moved to 3, and why 4 did not move the floor with it.

`MacroDeck.Ui`, `MacroDeck.Ui.Model`, and `MacroDeck.Ui.Testing` are public NuGet contracts. Existing
keys, component meanings, patch semantics, and public API members must follow the normal
[compatibility policy](https://docs.macro-deck.app/policies/compatibility/).

### Why the floor is 3 and the ceiling is 4

The UI model's `Minimum` is 3 and its `Current` is 4, and the gap between them is the difference between
a rename and a widening.

The floor moved to 3 because the component vocabulary was renamed outright rather than extended: every
`widget.*` node type became either `ui.*` or `macrodeck.*`, with no alias kept for the old spelling. A
tree built against the old vocabulary is not representable under the new one, so a package that no longer
understands a single `widget.*` type must not advertise the majors in which those were the only spelling.

The ceiling moved to 4 because an `icon` property may now carry a typed `{"type":…,"reference":…}`
provider reference where it previously always carried a bare icon-pack reference string - the same shape
as the move to 2, where a text property gained the option of carrying a localization reference. A producer
built against 3 emits only the string form and one built against 4 may emit either, so the two are not
interchangeable and the version has to say which a session speaks. The floor stayed where it was because
nothing was renamed: a reader at 4 accepts both readings, so it still reads every tree a producer at 3
emits, and `UiIconInput` is unchanged.

Either way a client and a provider negotiate the model version as they always have - before a session is
opened - and a mismatch produces the same graceful decline, never a tree the reader cannot parse.

### Additions that moved no version

New component types and new properties are additive and leave the model version alone; the component
profile's rule decides which of the two a new feature is. [Modifiers](https://docs.macro-deck.app/ui/components/modifier/) add both:

| Addition | Shape | An older reader |
|---|---|---|
| `modifiers` (background, radius, border, accessibility text, `disabled`) | A property on any node | Ignores it and draws the node plainer. A disabled subtree still offers none of its own events, because the DSL stopped it declaring them, but the reader does not know the region absorbs the tile's press, so a deck tile's own flows still run there. |
| `drag`, `drag-end`, `swipe`, `pinch`, `pinch-end` | Event names | Never sends a name it does not implement. |
| `pointer-down`, `pointer-move`, `pointer-up`, `tap` | Event names | Never sends them, and does not claim the pointer for a node that declares only these: a deck tile's own press flow still runs when the node is pressed there. |
| `offersStateProvider`, `offersIconProvider`, `stateProviderBlockId`, `iconProviderBlockId` on `actions-list-editor`, and the `provide` config event | Properties and an event name | Ignores the properties, never sends `provide`, and shows the action list without provider controls. |
| `status` (`UiStatus`), `menu` (`UiConfigMenu`) and `dialog` (`UiConfigDialog`) | Configuration types | Declines them and draws the node's `fallback`. |
| `confirmTitle`, `confirmMessage`, `confirmLabel`, `confirmDanger`, `promptValue` on `button` | Properties | Raises `activate` at once, without asking and without a payload. |
| `interaction` on `ui.slider` (`relative`) | A property | Ignores it and keeps the absolute drag: a press jumps the level to the pointer, and a tap sends `change`. |
| `ui.modifier` (padding, opacity, clip, mask, frame), component version 1 | A type | Draws the node's explicit `fallback`; without one, none of the wrapped content (Macro Deck's renderer shows a faint placeholder box). No fallback is invented for you. |
| `trackColor` on `ui.gauge` | A property | Ignores it and draws the theme's track colour, so the ring still reads. |
| `shadow`, `strokeColor` and `strokeWidth` on `ui.text` | Properties | Ignores them: keeps its own legibility shadow and draws no outline, so the text still reads. |
| `spans` on `ui.text` | A property | Ignores it and draws `text`, which the producer keeps the plain equivalent of the spans: the same words, each image as its alt text, on one font and colour. |
| `overflow` on `ui.stack` (`clip-start`), component version 2 | A property, gated by a component version | Draws the node's `fallback`, because a producer using `clip-start` asks for version 2. Without that ask a version 1 reader ignores the key and shrinks every child into the box. |
| `anchor` on `ui.list` (`end`), component version 3 | A property, gated by a component version | Draws the node's `fallback`, because a producer using `end` asks for version 3. Without that ask a version 2 reader ignores the key and leaves the view where the user put it, so new rows at the end stay below the fold. |
| `ui.responsive` and its `variants` property, component version 1 | A type | Draws the node's `fallback`. Unlike `ui.modifier`, one is invented when you set none: a copy of the default layout. When it decides whether the tile's own press belongs to a control, it walks every layout, not only the one it would have drawn - see [Responsive](https://docs.macro-deck.app/ui/components/responsive/#older-readers). |
| `ui.first-fit`, component version 1 | A type | Draws the node's `fallback`. One is invented when you set none: a copy of the last layout, the one that is always acceptable. When it decides whether the tile's own press belongs to a control, it walks every layout - see [First fit](https://docs.macro-deck.app/ui/components/first-fit/#older-readers-and-readers-that-cannot-measure). |
| `macrodeck.video-stream` and its `stream` property, component version 1 | A type | Draws the node's `fallback`, and opens no session. See [Video stream](https://docs.macro-deck.app/ui/components/video-stream/#older-readers). |
| `transparent` as the `background` of `ui.stack` and `ui.button` | A value | Treats it as no background: a stack draws the tile face behind it, a button its accent colour. The tile face stays, so the folder background does not show through. |
| `allowTransparent` on `color` | A property | Ignores it and offers no Transparent swatch; a stored `transparent` still shows as the input's value. |
| `thresholds` (`UiThresholdsInput`) and its `unit`, `fixedCount`, `fixedColors` and `maxCount` properties | A configuration type | Declines it and draws the node's `fallback`, or shows the field as unsupported. |
| `allowVariables` on `color` and `thresholds` | A property | Ignores it and offers fixed colours only. |
| `ofParent` on a length (`UiLength.OfParent`) | A member of an existing value | Ignores it and resolves `basis` against the widget, which is why `basis` is always sent. Pass the fallback you want as the second argument. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/#relative-to-the-containing-box). |
| `minCellSize` on `ui.grid` | A property | Ignores it and draws `columns` by `rows`, hiding the children that do not fit those rows. Set both to the arrangement an older reader should draw. See [Grid](https://docs.macro-deck.app/ui/components/grid/#choosing-the-columns). |
| `#rrggbbaa` wherever a `#rrggbb` colour is accepted | A value | Rejects it like any other unknown spelling: the property counts as omitted and the theme colour is drawn. |

See [ADR 0064](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0064-components-are-a-registry-over-two-namespaces.md)
for why the vocabulary is organized as a registry over the `ui.*`/`macrodeck.*` namespaces rather than one
flat list, and [The UI model](https://docs.macro-deck.app/ui/concepts/ui-model/#model-version-negotiation) for where negotiation
sits in a session's lifecycle.

### Behaviour changes that moved no version

These change what an existing plugin observes without a new model version. Each is a deliberate
exception to the [compatibility policy](https://docs.macro-deck.app/policies/compatibility/), listed here so you can check your plugin
against it.

| Change | Hosts | What an existing plugin sees |
|---|---|---|
| A plugin built on the SDK with the message channel declares the `messaging` capability kind, at local id `provider`, whenever the host lists it in `capabilityKinds` - also when the plugin never uses the channel | Released after 3.0.0-beta.11 | A test that asserts a plugin's exact declared capabilities, against `MacroDeckTestHost`, `PluginTestHarness` or a real host, sees one more entry. Nothing changes on a host without the kind. See [Messaging between plugins](https://docs.macro-deck.app/features/messaging/#older-versions-of-macro-deck). |
| `UiView` implements `IDisposable`, and `UiPreviewInstance.DisposeAsync` disposes its view - including a `UiView` a preview scenario returned itself | Released after 3.0.0-beta.7 | A plugin that never disposes a view behaves as before. A preview scenario that returns a cached `UiView` gets a disposed view that ignores every event from the second open on; build a new one per call. A plugin that builds with CA1001 as an error may see it on a type that creates a `UiView` in a field without being disposable. See [Disposing](https://docs.macro-deck.app/ui/concepts/reactive-updates/#disposing). |
| A `link` with an external `http` or `https` URL is opened by the host in the default browser on every surface, whether or not it declares `activate` | Released after 3.0.0-beta.6 | A link that declares `activate` still receives it exactly once, and is now opened by the host outside the integration setup dialog too. A handler that opened the URL itself opens a second tab; remove that code. See [Links](https://docs.macro-deck.app/ui/concepts/events/#links). |
| `IUiConfigFlow.CreateUiSessionAsync` can be called again for the same flow instance, after its previous session ended with a retryable error or was reloaded for .NET Hot Reload | Released after 3.0.0-beta.13 | A flow that assumed one session per flow instance gets a second call. Build each session from state the flow holds; the user's unsaved edits arrive as `change` events. See [From a config flow](https://docs.macro-deck.app/ui/views/configuration/#from-a-config-flow). |
| A device provider receives a null `DeviceSurfaceAppearance.BackgroundColor` for a widget whose stored background is `transparent`, instead of the literal | Released after 3.0.0-beta.14 | A provider that drew the stored string sees no colour for that key, like a widget without a background; one that parsed the literal as a colour no longer fails on it. See [Devices](https://docs.macro-deck.app/features/devices/). |
| Under .NET Hot Reload, a plugin built on this SDK ends every open session except dialogs with `ui/reload`, and Macro Deck opens each one again | SDK released after 3.0.0-beta.13; on an older host the SDK sends `ui/fault` instead | A provider is asked for new sessions for views that are already open, each time Hot Reload applies a change. A plugin that is not being hot reloaded sees nothing new. See [Real views](https://docs.macro-deck.app/ui/views/developer-preview/#real-views). |
| `PackageSigner` and `PackageVerifier` refuse an icon pack with more than 30,000 archive entries, counting the signature files, with `too-many-entries`; an icon pack's `pack.json` may be up to 32 MiB instead of 8 MiB | SDK released after 3.0.0-beta.13 | Signing a pack that would exceed 30,000 entries now fails. No host ever imported more than 10,000 entries, so no signed pack that installs is affected. Plugin, profile and template manifests keep the 8 MiB bound. See [Publish an icon pack](https://docs.macro-deck.app/creator-portal/publish-icon-pack/#size-limits). |
| An exported icon pack, profile or widget carries one master image per icon and no smaller sizes; Macro Deck creates the sizes it serves from the master when an icon is first shown, and ignores size files in packs it imports | Released after 3.0.0-beta.13 | An icon pack bundled from a newer export has half to a quarter of the files. Macro Deck 3.0.0-beta.13 and older import it but show its full-size masters at every size. A bundled pack exported by an older version still imports; its size files are not used. See [Publish an icon pack](https://docs.macro-deck.app/creator-portal/publish-icon-pack/#size-limits). |
| Icons can have [appearances](https://docs.macro-deck.app/guide/concepts/#icon-appearances). An exported icon pack's `pack.json` and a profile or widget archive nest them under their icon and list their masters as extra files. For such an icon, a plugin icon handle's `resourceId` carries a marker, and a device surface's `IconId` is the GUID of the appearance chosen for that device | Released after 3.0.0-beta.15 | A pack bundled from a newer export has one more file per appearance; Macro Deck versions without appearances import it and show the default images, and an `icon-pack add` from an older CLI accepts it. A plugin that treats `resourceId` as opaque sees no difference. A device provider gets a GUID it may not find in icon listings; `GetIconAsync` serves it. Icons without appearances behave as before. See [Publish an icon pack](https://docs.macro-deck.app/creator-portal/publish-icon-pack/) and [Devices](https://docs.macro-deck.app/features/devices/). |
| An icon can have appearances with the trait `variant` (key `variant=outlined`), named by the user and picked manually. The **Set Icon Appearance** action's `iconAppearance` parameter is now a dynamic choice listing them, instead of a fixed list | Released after 3.0.0-beta.15 | Stored values and key syntax are unchanged; a client that cannot load options still shows the stored value. A pack with `variant` appearances imports in any version that has appearances, and older versions show the default image. A `variant` appearance never matches a viewer context, so it is never selected automatically. See [Button icons](https://docs.macro-deck.app/features/button-icons/). |
| Turning an integration off withdraws everything its providers registered - widget types, layouts, folder views, screensavers - and takes its devices offline. While it is off, registering one of those is validated and answered as usual but not kept, and its devices stay offline whatever presence is reported | Released after 3.0.0-beta.14 | A plugin the user turned off no longer has its widget types, layouts, folder views or screensavers offered, including after it reconnects, and its devices show offline. Nothing changes while it is on, or for a plugin that was never configured. When the user turns it back on, the plugin is asked to initialize again, as after a configuration change, and registers what it offers. |
| A `ui.list` reader starts its `reveal` count over when the list's content is replaced: it holds fewer children than at its previous paint, or the child at the furthest index sent is gone or has another id | Released after 3.0.0-beta.11 | A `reveal` can now carry an index at or below one the plugin already received, after its list shrank or its rows were replaced, including a row inserted or removed above the furthest index. A handler that only grows its window, as [List](https://docs.macro-deck.app/ui/components/list/#loading-more-items) shows, is unaffected; one that sets its window from the index unconditionally can shrink it and should keep the larger value. A reader that has not adopted this rule, such as an older Companion app, may not ask again after a replacement. |
| A colour with alpha, stored as `rgba(...)` or `#rrggbbaa`, is drawn translucent on the deck and in the widget editor | Released after 3.0.0-beta.15 | A widget appearance patch or stored widget data with such a colour, which used to be drawn opaque, now lets the tile face show through. Send `#rrggbb` to keep a colour opaque. Device surfaces still receive opaque `#rrggbb`. |
| The Slider and History Graph widgets have colour thresholds: while a widget's `thresholdsEnabled` is on, the band its value falls in picks its colour | Released after 3.0.0-beta.15 | A `WidgetAppearanceProperty.AccentColor` patch on such a widget is still stored and acknowledged, but has no visible effect until the user turns the thresholds off. |

## Patches

> Source: https://docs.macro-deck.app/ui/reference/patches/
>
> How a tree changes without a full resend, and the revision rule that keeps a patch attributable to the state it was computed from.

A patch is a bounded sequence of operations against one tree, applied atomically. Applying it advances
the tree's **revision** by exactly one - never more, never less, and never on a patch that carries no
operations. A provider that computed a patch against an earlier revision than the session currently holds
gets refused and resynced with a full tree rather than having the patch silently misapplied; see
[what a refused update looks like](https://docs.macro-deck.app/ui/views/sessions/#what-a-refused-update-looks-like) for the
complete set of ways a patch or a tree can be rejected.

The operation vocabulary itself - what an operation targets, what it carries, and which shapes are valid
against which node kinds - is defined in
[`ui-model/src/MacroDeck.Ui.Model/Patches/`](https://github.com/Macro-Deck-App/Macro-Deck/tree/main/ui-model/src/MacroDeck.Ui.Model/Patches)
rather than restated here; treat that source as the operation reference, and this page as the rule that
governs how any of them apply.

In practice you rarely construct a patch by hand: `MacroDeck.Ui`'s reactive runtime computes and emits
the minimal patch for you from a state change - see [Reactive updates](https://docs.macro-deck.app/ui/concepts/reactive-updates/).
Reach for the operations directly only when you are serving a tree straight from `MacroDeck.Ui.Model`,
without the DSL.

## Resources

> Source: https://docs.macro-deck.app/ui/reference/resources/
>
> The resource handle a tree references instead of carrying bytes, and the limit that bounds what it can promise.

A tree never carries bytes. Register your artwork and reference the handle:

```csharp
new UiImage { Key = "icon", Source = UiValue.Of(handle), Size = 0.2 }
```

The handle carries a `resourceId`, and optionally a `contentHash`, `mediaType` and `byteLength`. Macro
Deck serves the bytes and each client caches them by hash, so an icon shown by a hundred deck widgets is
transferred once per client rather than embedded a hundred times. A plugin gets a handle for its own bytes
from [`UiResources`](#registering-your-own-images), for an icon from its own bundled icon packs from
[`GetPluginIconAsync`](#icons-from-your-bundled-icon-packs), and for any installed icon from
[`GetIconAsync`](#icons-from-any-installed-icon-pack).

Macro Deck's own icons need no resource at all: name one with [`ui.icon`](https://docs.macro-deck.app/ui/components/icon/) and every
reader draws it from its own set.

`UiButton.Source` takes the same handle for its backdrop, framed by `Fit`, `Zoom`, `OffsetX`, `OffsetY`
and `Opacity`. Those are fractions and multipliers, not pixels or percentages: the scale is applied inside
the translation, so an offset covers the same distance at any zoom.

`Transition` says how a *change* of `Source` is drawn. `UiImageTransitions.Crossfade` holds the outgoing
artwork until the incoming one has decoded and then reveals it over 220 ms, which is normative rather than
a suggestion - two readers that chose their own timing would animate visibly differently. Leave it out and
the new artwork simply replaces the old one, which is also what a reader that does not implement the key
does.

`Opacity`, `Brightness` and `Saturation` adjust the artwork itself. Reach for `Opacity` to let what is
behind the artwork show through, and for the other two to change the artwork regardless of its ground -
"the same picture, darker" is `Brightness`, not a lower opacity, because a half-transparent cover ends up
looking like whatever sits behind it. Both are multipliers where absent means `1`, applied brightness
first and then saturation; the saturation result is normative down to its luma coefficients, since two
readers using different ones desaturate the same image to different greys.

### Registering your own images

```csharp
public async Task InitializeAsync(IIntegrationContext context)
{
    _photo = await context.UiResources.RegisterAsync("photo", await File.ReadAllBytesAsync(path), "image/jpeg");
}

new UiImage { Key = "photo", Source = UiValue.Of(_photo) }
```

`IIntegrationContext.UiResources` turns bytes into a handle. Put the handle it returns into the tree, never
one you build yourself: it carries the `contentHash` that makes clients fetch new bytes.

- **Names** are yours: a letter or digit, then up to 63 letters, digits, hyphens or underscores. All
  integrations in one plugin share them. Two plugins using the same name never collide.
- **Registering a name again replaces its bytes.** The `resourceId` stays, the `contentHash` changes, so a
  photo frame can show every picture under one name. Update the tree with the new handle and clients draw
  the new picture; a client still holding the old hash is sent the current bytes without caching them.
  Registering the same bytes under the same name again costs no upload.
- **Media types** are `image/png`, `image/jpeg`, `image/webp` and `image/gif`. SVG is not accepted from a
  plugin, the same rule as for icons a plugin supplies. PNG and JPEG are the safe choice for photos.
- **Size.** One resource is at most `maxUiResourceBytes` (2 MiB). That limit is deliberate and applies per
  resource: downscale camera photos before registering them. All of a plugin's resources together are at
  most `maxUiResourceBytesPerPlugin` (16 MiB) and `maxUiResourcesPerPlugin` (256). Over the quota,
  registration throws `UiResourceException` with `QuotaExceeded` and the name keeps what it had. Free room
  with `RemoveAsync`; removing a name that holds nothing is not an error.
- **Lifetime.** Macro Deck keeps resources in memory, never on disk, for as long as the plugin session
  lasts: through a reconnect that resumes it and through re-initialisation after a configuration change.
  They are released when the session ends and are gone after Macro Deck restarts, when your integration is
  initialised again on the new session. Register in `InitializeAsync`, or before you build the tree that
  shows the image.
- **Errors.** Argument problems (name, media type, empty or oversized content) are `ArgumentException`
  before anything is sent. `UiResourceException.ErrorCode` is `Unsupported` on a Macro Deck that predates
  resource registration, `QuotaExceeded`, `RateLimited`, or `Failed`, for example when the connection
  dropped. Registrations run one at a time, so starting many at once is safe.

A music player plugin can register its own player's cover in one call with
[`GetArtworkAsUiResourceAsync`](https://docs.macro-deck.app/features/music-players/#showing-the-cover-in-your-own-ui), and the cover of
any other player with
[`RegisterMusicPlayerArtworkAsync`](https://docs.macro-deck.app/features/music-players/#showing-another-players-cover).

In tests, `FakeIntegrationContext.UiResources` is a `FakeUiResourceRegistry` that applies the same rules and
exposes what was registered, and `MacroDeckTestHost` answers registrations over the wire.

### Icons from your bundled icon packs

A plugin that bundles icon packs in its artifact (`bundledIconPacks` in the
[manifest](https://docs.macro-deck.app/reference/manifest/)) shows one of their icons without uploading anything:

```csharp
UiResource logo = await context.UiResources.GetPluginIconAsync("logos", "spotify", cancellationToken);
var image = new UiImage { Key = "logo", Source = UiValue.Of(logo), Size = 0.2 };
```

The first argument is the pack's key in the manifest, the second the icon's name inside that pack.

- **No upload, no quota.** The handle points into Macro Deck's icon store. Nothing is sent from the
  plugin, nothing is held in memory for the session, and nothing counts against
  `maxUiResourceBytesPerPlugin` or `maxUiResourcesPerPlugin`.
- **Stable across restarts.** The handle stays valid after Macro Deck restarts, unlike a registered
  resource.
- **A replaced icon gets a new `contentHash`.** When an update or a development sync replaces the icon,
  the `resourceId` stays and the `contentHash` changes, so clients fetch the new bytes. Ask again when you
  build a tree rather than holding a handle for the plugin's whole lifetime.
- **Appearances are chosen by the client.** For an icon with
  [appearances](https://docs.macro-deck.app/guide/concepts/#icon-appearances), the handle's `resourceId` carries a marker and each
  client fetches the light, dark, static or animated image that fits it. The `contentHash` changes when any
  appearance changes. Treat `resourceId` as opaque: it changes when an icon gains or loses its appearances.
- **Your packs only.** The lookup by key and name is scoped to the calling plugin, so no plugin can name
  another's icons that way. To show an icon you know by id, use
  [`GetIconAsync`](#icons-from-any-installed-icon-pack).
- **Errors.** `UiResourceException.ErrorCode` is `PluginIconNotFound` when your packs hold no such key or
  name, `Unsupported` on a Macro Deck that predates bundled icon packs, and `Failed` when the icon cannot
  be served within `maxUiResourceBytes` or the call could not complete.

`UiIcon` stays limited to Macro Deck's own glyphs: a bundled icon is a coloured image and is drawn through
`UiImage` or a button's `Source`. In tests, `FakeUiResourceRegistry.AddPluginIcon(key, name, bytes,
mediaType)` makes an icon available to `GetPluginIconAsync`, and `MacroDeckTestHost` answers the lookup
over the wire as a plugin without bundled packs.

### Icons from any installed icon pack

Any icon installed in Macro Deck, from the user's own packs, imports, the Store or a plugin, can be shown
by its id, again without uploading anything:

```csharp
UiResource icon = await context.UiResources.GetIconAsync(iconId, cancellationToken);
var image = new UiImage { Key = "icon", Source = UiValue.Of(icon), Size = 0.2 };
```

The id is a `Guid`. Users copy it with **Copy icon id** on the icon packs page, which suits a plugin that
reads icon ids from text the user writes. When the user picks the icon in your configuration form instead,
the value holds the same id: a `UiIconInput` stores it as a string, and a `UiIconReferenceInput` as the
`Reference` of a `UiIconReference` of type `icon-pack`.

- **No upload, no quota, stable across restarts**, and **a replaced icon gets a new `contentHash`**, as for
  [bundled icons](#icons-from-your-bundled-icon-packs).
- **Errors.** `UiResourceException.ErrorCode` is `IconNotFound` when no installed pack holds an icon with
  that id, for example because the user deleted it, `Unsupported` on a Macro Deck that predates the lookup,
  and `Failed` when the icon cannot be served within `maxUiResourceBytes` or the call could not complete.

In tests, `FakeUiResourceRegistry.AddIcon(iconId, bytes, mediaType)` makes an icon available to
`GetIconAsync`, and `MacroDeckTestHost` answers the lookup over the wire as a Macro Deck without icons.

### Limits

`maxUiResourceBytes` bounds both a `UiResource`'s **declared** `byteLength` and the bytes the host's
resource store accepts for one resource, so a declaration can never promise more than the host will
serve. A `byteLength` of `null` is accepted. `maxUiResourceBytesPerPlugin` and `maxUiResourcesPerPlugin`
bound what one plugin may have registered at once. They are `maxUi*` limits, listed with every other
protocol limit in [Plugin WebSocket protocol](https://docs.macro-deck.app/reference/websocket/#limits-and-timeouts); read them from the
protocol descriptor or the session response rather than hard-coding them - see
[Serving a view](https://docs.macro-deck.app/ui/views/sessions/#limits) for the rest of the `maxUi*` family.
