# Macro Deck UI: components

Pages of docs.macro-deck.app merged into one file by `scripts/sync_docs.py`. Each page is an `## <Page title>` section with its source URL. Grep for a type or heading to jump to it.

Contents:

- Components: https://docs.macro-deck.app/ui/components/
- Button: https://docs.macro-deck.app/ui/components/button/
- Chart: https://docs.macro-deck.app/ui/components/chart/
- Dial: https://docs.macro-deck.app/ui/components/dial/
- First fit: https://docs.macro-deck.app/ui/components/first-fit/
- Gauge: https://docs.macro-deck.app/ui/components/gauge/
- Grid: https://docs.macro-deck.app/ui/components/grid/
- Icon: https://docs.macro-deck.app/ui/components/icon/
- Image: https://docs.macro-deck.app/ui/components/image/
- List: https://docs.macro-deck.app/ui/components/list/
- Modifier: https://docs.macro-deck.app/ui/components/modifier/
- Progress: https://docs.macro-deck.app/ui/components/progress/
- Range bar: https://docs.macro-deck.app/ui/components/range-bar/
- Responsive: https://docs.macro-deck.app/ui/components/responsive/
- Segmented: https://docs.macro-deck.app/ui/components/segmented/
- Shape: https://docs.macro-deck.app/ui/components/shape/
- Slider: https://docs.macro-deck.app/ui/components/slider/
- Stack and layer: https://docs.macro-deck.app/ui/components/stack-and-layer/
- Text field: https://docs.macro-deck.app/ui/components/text-field/
- Text: https://docs.macro-deck.app/ui/components/text/
- Time and clock: https://docs.macro-deck.app/ui/components/time/
- Toggle: https://docs.macro-deck.app/ui/components/toggle/
- Transform: https://docs.macro-deck.app/ui/components/transform/
- Video stream: https://docs.macro-deck.app/ui/components/video-stream/

## Components

> Source: https://docs.macro-deck.app/ui/components/
>
> Every node type the UI framework ships, and which page documents it.

A view is a tree of these node types. Each one has its own page below: purpose, properties - and what
leaving one out means - supported children, events and interactions, and how it sizes on the main and
cross axis.

### `ui.*`

| Type | Purpose | Page |
|---|---|---|
| `ui.stack` | Lays children out in one direction | [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/) |
| `ui.text` | One run of text | [Text](https://docs.macro-deck.app/ui/components/text/) |
| `ui.image` | Draws a resource | [Image](https://docs.macro-deck.app/ui/components/image/) |
| `ui.range-bar` | A gradient-filled span with an optional point marker | [Range bar](https://docs.macro-deck.app/ui/components/range-bar/) |
| `ui.slider` | A level the user drags | [Slider](https://docs.macro-deck.app/ui/components/slider/) |
| `ui.button` | A container the user presses | [Button](https://docs.macro-deck.app/ui/components/button/) |
| `ui.layer` | Stacks children through the depth of the box instead of along an axis | [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/) |
| `ui.chart` | A series drawn as a filled line | [Chart](https://docs.macro-deck.app/ui/components/chart/) |
| `ui.text-field` | A line the user types | [Text field](https://docs.macro-deck.app/ui/components/text-field/) |
| `ui.list` | A container that scrolls and asks for more | [List](https://docs.macro-deck.app/ui/components/list/) |
| `ui.transform` | Rotates, scales and shifts its children together about a pivot | [Transform](https://docs.macro-deck.app/ui/components/transform/) |
| `ui.shape` | A filled and stroked rectangle, rounded rectangle, circle, capsule or path | [Shape](https://docs.macro-deck.app/ui/components/shape/) |
| `ui.icon` | One glyph of Macro Deck's built-in icon set, drawn by name | [Icon](https://docs.macro-deck.app/ui/components/icon/) |
| `ui.grid` | Lays children out in equal columns and rows, with spans | [Grid](https://docs.macro-deck.app/ui/components/grid/) |
| `ui.gauge` | A read-only level drawn along an arc or ring | [Gauge](https://docs.macro-deck.app/ui/components/gauge/) |
| `ui.toggle` | An on/off switch the user flips | [Toggle](https://docs.macro-deck.app/ui/components/toggle/) |
| `ui.segmented` | A row of segments the user chooses one of | [Segmented](https://docs.macro-deck.app/ui/components/segmented/) |
| `ui.dial` | A rotary level the user turns | [Dial](https://docs.macro-deck.app/ui/components/dial/) |
| `ui.modifier` | Pads, fades, clips, masks or frames its one child | [Modifier](https://docs.macro-deck.app/ui/components/modifier/) |
| `ui.responsive` | Draws one of several layouts, chosen by the box it is given | [Responsive](https://docs.macro-deck.app/ui/components/responsive/) |
| `ui.first-fit` | Draws the first of several layouts whose text fits the box it is given | [First fit](https://docs.macro-deck.app/ui/components/first-fit/) |

Any node can also carry a `modifiers` object - background, border, radius, accessibility text and
`disabled` - and the gesture events. See [Modifier](https://docs.macro-deck.app/ui/components/modifier/).

### `macrodeck.*`

A component belongs here when a reader cannot draw it from the tree alone, because it must resolve a
Macro Deck-defined reference - a time or a media position
([ADR 0065](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0065-the-component-profile-authoring-contracts.md))
- against its own clock, or ask Macro Deck for a video stream session itself. Everything else is `ui.*`,
however Macro Deck-flavoured its styling.

| Type | Purpose | Page |
|---|---|---|
| `macrodeck.dynamic-text` | A run of text derived from a time reference the reader resolves itself | [Time and clock](https://docs.macro-deck.app/ui/components/time/) |
| `macrodeck.clock-dial` | An analogue clock face drawn from the same kind of reference | [Time and clock](https://docs.macro-deck.app/ui/components/time/) |
| `macrodeck.progress-bar` | A track whose filled span follows a position that keeps moving | [Progress](https://docs.macro-deck.app/ui/components/progress/) |
| `macrodeck.progress-text` | A run of text derived from that same moving position | [Progress](https://docs.macro-deck.app/ui/components/progress/) |
| `macrodeck.video-stream` | A live video stream from a provider, played from a session the reader opens | [Video stream](https://docs.macro-deck.app/ui/components/video-stream/) |

## Button

> Source: https://docs.macro-deck.app/ui/components/button/
>
> A pressable tile that lays out its children like a stack and adds artwork, a ring and a press.

A tile the user presses. It lays out its children exactly as `ui.stack` does, and adds artwork behind
them, a ring around the edge, and the press itself.

`ui.button`

### Example

```csharp
new UiButton
{
    Key = "mute",
    Justify = UiComponentJustify.Center,
    Background = UiValue.From(() => state.Value.Face),
    Source = UiValue.From(() => state.Value.Icon),
    Fit = UiComponentImageFits.Cover,
    Events = [UiEventHandler.On(UiComponentEvents.Press, () => ToggleMute())],
    Children = [new UiTextRun { Key = "label", Text = UiText.Of("Mute"), Size = 0.14 }],
}
```

*[Image: A red button tile with a crossed-out microphone icon and the label Mute centred beneath it]*

A tile with an icon covering its face and a centred label; a completed press calls `ToggleMute`.

### Handling a press

```csharp
Events =
[
    UiEventHandler.On(UiComponentEvents.Press, () => Run()),
    UiEventHandler.On(UiComponentEvents.LongPress, () => OpenOptions()),
],
```

Declare only the names you handle. Declaring just `Press` is how you say the button has no long-press
behaviour. A button with no events is still drawn, but accepts nothing. To show it as unavailable as well,
wrap it in a [modifier](https://docs.macro-deck.app/ui/components/modifier/#disabled) with `Disabled`.
Use `PressStart` and `PressEnd` to drive something for as long as the finger is down.

Declare `DoublePress` next to `Press` for a separate action on a double tap. The trade-off: once
`DoublePress` is declared, every single tap's `Press` arrives 400 ms late, because the reader waits to see
whether a second tap follows. A double tap sends `DoublePress` only, never `Press`. A reader that predates
`double-press` sends `Press` for each tap, so a button stays usable there.

### Artwork and ring

```csharp
Source = UiValue.From(() => state.Value.Artwork),
Fit = UiComponentImageFits.Cover,
Zoom = 1.2,
Brightness = UiValue.From(() => state.Value.Paused ? 0.6 : 1.0),
BorderStyle = UiComponentBorderStyles.Breathing,
BorderColor = "#ff3b30",
```

*[Image: A button whose face is a zoomed album cover filling the whole tile, with a thin red ring along its edge]*

The artwork fills the whole box behind the children, so swapping the face is a property patch rather than
a rebuilt subtree. `hue-shift` and `rgb` rings cycle their own colours and ignore `BorderColor`.

`Tint = "#4f8cff"` draws the artwork as a silhouette in that colour: every pixel keeps its own
transparency, so a white icon on a transparent background becomes a blue icon, while an image without
transparency becomes a solid rectangle. A reader that does not know `tint` draws the artwork in its own
colours, and so does one whose engine cannot mask. Tint is unrelated to the press feedback.

### Filling the tile

```csharp
new UiButton { Key = "backdrop", Fill = true, Corner = UiComponentButtonCorners.Tile, /* ... */ }
```

A button that is the whole tree already takes the tile's corner. A nested full-bleed button asks for it
with `Corner = Tile`; otherwise it rounds itself by a share of its own height and cuts an arc across the
tile.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Direction` (`direction`) | `vertical`, `horizontal` | `vertical` | The layout axis for children. |
| `Justify` (`justify`) | `UiComponentJustify` | `start` | How free space is distributed on the main axis. |
| `Align` (`align`) | `UiComponentAlignments` | `stretch` | How children align on the cross axis. |
| `Gap` (`gap`) | length | No gap | The gap between children. |
| `Padding` (`padding`) | length | No padding | Inner padding on every edge. |
| `Background` (`background`) | `#rrggbb` or `transparent` | The reader's own accent colour | The button's face - unlike a stack, a button always has one. `transparent` asks for no face at all, and on the widget's root also removes the tile face behind it. |
| `Source` (`source`) | resource | None | Artwork drawn across the whole box behind the children. |
| `Transition` (`transition`) | `crossfade` | The new artwork replaces the old | How a change of `Source` is drawn. |
| `Fit` (`fit`) | `contain`, `cover` | `contain` | How the artwork fills the box. |
| `Zoom` (`zoom`) | `0.1..4` | `1` | Scales the artwork about its own centre. |
| `OffsetX` (`offsetX`) | `-1..1` | `0` | Shifts the artwork across by a fraction of the element's width, after `Zoom`. |
| `OffsetY` (`offsetY`) | `-1..1` | `0` | Shifts the artwork down by a fraction of the element's height, after `Zoom`. |
| `Opacity` (`opacity`) | `0..1` | Fully opaque | How opaque the artwork is drawn. |
| `Brightness` (`brightness`) | `0..2` | `1` | Multiplies the artwork's luminance. |
| `Saturation` (`saturation`) | `0..2` | `1` | Multiplies the artwork's saturation. |
| `Tint` (`tint`) | `#rrggbb` | The artwork's own colours | Draws the artwork in this colour, keeping each pixel's transparency. |
| `BorderStyle` (`borderStyle`) | `static`, `heartbeat`, `breathing`, `blink`, `comet`, `ants`, `hue-shift`, `rgb` | No ring - no value spells "off" | How the ring is drawn. |
| `BorderColor` (`borderColor`) | `#rrggbb` | The style's own colour | The ring's tint, ignored by `hue-shift` and `rgb`. |
| `Corner` (`corner`) | `tile` | `0.12` of the button's own height | How round the button's own corners are. |

Enum values live in `UiComponentImageFits`, `UiComponentImageTransitions`, `UiComponentBorderStyles` and
`UiComponentButtonCorners`. For `background`'s default see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Events

| Event | Fires when | Payload |
|---|---|---|
| `press` (`UiComponentEvents.Press`) | The user completed a press without holding it | None |
| `long-press` (`UiComponentEvents.LongPress`) | The press was still held after 600 ms | None |
| `press-start` (`UiComponentEvents.PressStart`) | The press began | None |
| `press-end` (`UiComponentEvents.PressEnd`) | The press ended, however it ended | None |
| `double-press` (`UiComponentEvents.DoublePress`) | A second tap completed shortly after the first; the taps send no `press` | None |

### Children

Any elements, any number, laid out as `ui.stack` lays out its children along `direction`.

### Layout

Identical to `ui.stack`: `direction`, `justify`, `align`, `gap` and `padding` divide the button's content
box among its children. On its parent's main axis a button follows the ordinary rule - `MainSize` or
`Fill` if declared, otherwise its content extent. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- **Interaction only where declared.** A button with no events is drawn but accepts nothing.
- **`press` is primary.** A reader that implements one press name implements `press`. It never infers
  `press` from a `press-start`/`press-end` pair, never sends `press` in an interaction where `long-press`
  already fired, and never sends a name the node did not declare.
- **`press-end` always follows `press-start`**, including when the pointer left the element or the gesture
  was cancelled.
- **Double tap:** only with `double-press` declared, a completed tap holds its `press` for 400 ms. A second
  press starting within that window and within 24 px of the first tap, and released before the long-press
  threshold, sends `double-press` after its `press-end`, and neither tap sends `press`. If the second press
  becomes a long press or is cancelled, the held `press` is sent at that moment, after the second press's
  `press-start`. A second press starting farther away sends the held `press` first and counts as a new first
  tap. Without `double-press` declared, `press` is never delayed. This is a pointer reader's rule: a press
  from a hardware deck reaches your tree as `press` for every tap, never as `double-press`. The same rule applies to any
  other node that declares a press name. The slider's own `double-press` rule is different; see
  [Slider](https://docs.macro-deck.app/ui/components/slider/).
- **Press feedback is local and immediate:** tint the whole element white at `0.2` alpha, fade in over
  `20 ms`, out over `140 ms`, visible at least `60 ms`. Never wait for the producer before painting.
- **Paint order:** `background`, artwork, children, press feedback, ring.
- **Transparent face:** a `background` of `transparent` paints nothing instead of the accent colour. On a
  button that is the widget's root, draw the tile without its face fill and shadow too. Any other value
  that is not `#rrggbb` still falls back to the accent colour, and a modifier's `background` stays
  `#rrggbb` only.
- **Ring:** a fixed `2` device-independent units along the inner edge, following the corner radius - the
  one length not relative to the basis. Looping styles are phase-locked to Macro Deck's shared clock and
  keep animating regardless of the viewer's reduced-motion preference.
- **Corner:** absent means `0.12` of the button's own height, except a button that is the whole widget tree,
  which takes the tile's corner. An older reader ignores `corner` and paints its own corner.
- The button conformance fixtures in `ui-model/fixtures/component-profile/` pin the exact event ordering.

### See also

- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)
- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)

## Chart

> Source: https://docs.macro-deck.app/ui/components/chart/
>
> Draws a normalised series as a line with the area beneath it filled.

A line across the element with the area beneath it filled, drawn from a series you have already
normalised to `0..1`.

`ui.chart`

### Example

```csharp
var samples = new UiState<IReadOnlyList<double>>([]);

new UiChart
{
    Key = "chart",
    Points = UiValue.From(() => samples.Value),
    PlotTop = 0.66,
    Thickness = UiSize.Capped(2d / UiLength.Cell, 2),
}
```

*[Image: A wide tile with a thin blue line chart and a faint fill across its bottom third]*

A hairline history across the bottom third of the tile, in the reader's accent colour - the chart the
built-in History Graph widget draws.

### Appending points

```csharp
var fraction = Math.Clamp((celsius - 20) / 60, 0, 1);
samples.Set([.. samples.Peek().TakeLast(59), fraction]);
```

Keep a rolling window and map each raw value onto your own scale before it reaches the tree. The chart
carries no axis, unit or range; the producer owns the scale and decides whether it is fixed or follows
the data.

| Series | Drawn as |
|---|---|
| `[]` or absent | Nothing - no line, no fill |
| `[0.5]` | A flat line across the whole width at half height |
| `[0, 0.5, 1]` | Rising from the bottom-leading corner to the top-trailing corner of the band |
| `[1.4, -0.2]` | Clamped to `[1, 0]` |

### A band at the foot of the tile

```csharp
PlotTop = 0.66,
```

`PlotTop` moves the top of the plot band down, leaving the space above for labels. `0` in the series
is the element's bottom edge and `1` is the band's top.

### A colour of its own

```csharp
Color = config.AccentColor is { } accent ? UiValue.Of(accent) : UiValue.None<string>(),
```

*[Image: The same series drawn in green with a taller plot band]*

`Color` is a literal `#rrggbb` because it encodes data rather than theme. Leave it absent to follow the
reader's accent colour. See [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Properties

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Points` (`points`) | Numbers in `0..1`, oldest first | Nothing is drawn | The series as fractions of the plot band. |
| `Color` (`color`) | `#rrggbb` | The reader's accent colour | The line and fill colour. |
| `PlotTop` (`plotTop`) | `0..1` | `0` - the band is the whole element | Where the band starts, as a fraction of the element's height. |
| `Thickness` (`thickness`) | A length | Left to the reader | The line's width. |

### Events

None. A chart is never interactive.

### Children

None - `ui.chart` is a leaf.

### Layout

A chart follows the ordinary leaf rule on its parent stack's main axis: `mainSize` or `fill` if
declared, otherwise its content extent. A live numeric readout beside a chart should reserve its width
with `ui.text`'s `digits`, or the chart shifts whenever the value gains or loses a digit - see
[Text](https://docs.macro-deck.app/ui/components/text/). Full model: [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

The geometry is normative; the fixtures in `ui-model/fixtures/component-profile/` pin it, including a
dense series and every clamp branch.

- The plot band spans the element's full width and runs from `plotTop` of its height to its bottom edge.
  `0` is the bottom of the band, `1` the top.
- Values outside `0..1` are clamped, never rejected.
- Points sit at equal horizontal spacing, the first on the leading edge and the last on the trailing edge,
  joined by straight segments with round joins and caps.
- A single point is a flat line across the whole width at its height, not a dot.
- The line is drawn in `color` at `0.9` opacity, `thickness` wide.
- The area between the line and the element's bottom edge is filled in `color` at `0.16` opacity, with no
  stroke.
- An absent or empty series draws nothing at all - in particular not a flat line along the foot of the
  band, which would read as a real zero.
- An absent `color` means the reader's own accent colour.

### See also

- [Range bar](https://docs.macro-deck.app/ui/components/range-bar/)
- [Text](https://docs.macro-deck.app/ui/components/text/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)
- [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/)

## Dial

> Source: https://docs.macro-deck.app/ui/components/dial/
>
> A rotary level the user turns, the interactive counterpart of the gauge.

A rotary level: a [gauge](https://docs.macro-deck.app/ui/components/gauge/)'s arc with a thumb the user turns. Like a
[slider](https://docs.macro-deck.app/ui/components/slider/) it holds a fraction of the sweep in `0..1`, not a value in your own units.

`ui.dial`

### Example

```csharp
new UiDial
{
    Key = "volume",
    Level = UiValue.From(() => state.Value.Volume / 100.0),
    Step = 0.05,
    Thickness = 0.08,
    Events =
    [
        UiEventHandler.On(UiComponentEvents.Adjust, data => Preview(data)),
        UiEventHandler.On(UiComponentEvents.Change, data => Apply(data)),
    ],
    Fallback = new UiSlider
    {
        Key = "volumeFallback",
        Level = UiValue.From(() => state.Value.Volume / 100.0),
        Step = 0.05,
        Events =
        [
            UiEventHandler.On(UiComponentEvents.Adjust, data => Preview(data)),
            UiEventHandler.On(UiComponentEvents.Change, data => Apply(data)),
        ],
    },
}
```

*[Image: A three-quarter arc open at the bottom, filled in blue to 60 percent, with a white thumb at the end of the fill]*

`adjust` and `change` carry the level as a bare number and behave exactly as on a slider - see
[Reading the level](https://docs.macro-deck.app/ui/components/slider/#reading-the-level) and
[Adjust or change](https://docs.macro-deck.app/ui/components/slider/#adjust-or-change).

### Turning past the ends

The level follows the pointer's angle about the centre of the box, and never jumps across the ends of the
sweep. Once it reaches `0` or `1` it stays there while the pointer carries on past the end - through the gap
at the bottom, or on around a full ring - and follows again as soon as the pointer turns back inside the
sweep. A drag that overshoots the maximum never lands on the minimum.

A press that begins in the gap takes the nearer end. Near the centre the angle means nothing, so a pointer
within `0.2` of the radius from the centre keeps the current level.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Level` (`level`) | `0..1` | `0` | The filled fraction of the sweep. |
| `Step` (`step`) | fraction of the sweep | Continuous | The granularity the level snaps to, as on a slider. |
| `StartAngle` (`startAngle`) | `double`, degrees | `-135` | Where the arc begins, clockwise from twelve o'clock. |
| `EndAngle` (`endAngle`) | `double`, degrees | `135` | Where the arc ends. |
| `LevelColor` (`levelColor`) | `#rrggbb` | The reader's own accent colour | The filled arc's colour. |
| `Thickness` (`thickness`) | length | Left to the reader | The arc's width; the thumb scales with it. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | - | - | Shared with every leaf - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |

### Events

| Event | Fires when | Payload |
|---|---|---|
| `adjust` (`UiComponentEvents.Adjust`) | An intermediate level while the user is still turning | The level, a bare number |
| `change` (`UiComponentEvents.Change`) | The interaction ended, sent once | The level, a bare number |

### Children

None. `ui.dial` is a leaf.

### Layout

The element's whole box is the interactive surface. A dial has no content extent: on its parent's main axis
it takes `MainSize` or `Fill`, and without either it is `0` long. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- **Geometry:** the arc and fill exactly as [`ui.gauge`](https://docs.macro-deck.app/ui/components/gauge/#reader-behaviour) draws them,
  plus a thumb disc of radius `1.25 * thickness` on the arc at the level, in the primary text colour, ringed
  by `0.28 * thickness` in the widget's own background colour.
- **Interaction only where declared.** A dial with no events is drawn and cannot be touched.
- **Pointer mapping:** the pointer's angle about the box centre, projected onto the sweep and tracked
  continuously during a drag. The level is clamped to the sweep: at `0` or `1` it stays while the pointer
  goes further and moves again only once the pointer comes back inside. A press that begins outside the
  sweep takes the nearer end. Within `0.2 * radius` of the centre the level does not change.
- **A zero sweep** offers no interaction.
- **Snapping, painting locally first, rate and order** are those of [`ui.slider`](https://docs.macro-deck.app/ui/components/slider/#reader-behaviour):
  `adjust` at most ten times a second, never after the `change` that ended the interaction.
- **Keyboard and hardware:** activating a tile from the keyboard does nothing to a dial. A deck's rotary
  encoders (layout regions of kind `LayoutRegionKinds.Encoder`) are not routed to widgets yet, so a physical
  knob does not turn a dial.
- A reader that does not know `ui.dial` draws the node's `fallback`: a `ui.slider` with the same events, or
  a `ui.range-bar` at the same level when the dial declares none:

```json
{
  "type": "ui.dial",
  "properties": { "level": 0.6, "step": 0.05, "events": ["adjust", "change"] },
  "fallback": {
    "type": "ui.slider",
    "properties": { "level": 0.6, "step": 0.05, "events": ["adjust", "change"] }
  }
}
```

### See also

- [Gauge](https://docs.macro-deck.app/ui/components/gauge/)
- [Slider](https://docs.macro-deck.app/ui/components/slider/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)

## First fit

> Source: https://docs.macro-deck.app/ui/components/first-fit/
>
> Offer several layouts for the same content and let the reader draw the first one whose text fits, measured in the viewer's own font.

`UiFirstFit` holds several layouts for one place in the tree, in order of preference. The reader draws the
first one whose texts fit the box without being cut off or overflowing, and the last one when none does. It
measures with the font it paints in, so you do not have to guess the viewer's font, size or language.

`ui.first-fit` (component version 1)

### Example

A list row with a name and a caption. When both fit on one line they sit side by side; when they do not, the
caption moves under the name instead of both being cut off.

```csharp
new UiFirstFit
{
    Key = "namegroup",
    Children =
    [
        new UiStack
        {
            Key = "inline",
            Direction = UiComponentDirections.Horizontal,
            Children = [name, caption],
        },
        new UiStack { Key = "stacked", Children = [name, caption] },
    ],
}
```

### What fits means

A layout fits when, in the box the node is given:

- no text in it is cut off. A single-line text counts as cut off when its natural width is wider than the
  room it has, after any `MinSize` shrinking; a wrapping or line-limited text when it needs more lines than it
  is allowed;
- the layout itself does not overflow the box. A text may reach slightly past its parent, as it always may so
  descenders are not clipped; overflow beyond that makes a layout not fit, and a rounding difference of half a
  pixel in the box does not. A single-line text has no such allowance: it is cut off as soon as it needs an
  ellipsis.

A text that shrinks to its `MinSize` to fit counts as fitting. Images, shapes and other non-text content are
not measured.

The reader decides again whenever the box, a text, the font or the language changes.

### The box it chooses by

The node's box comes from its own sizing, never from the layout it draws. As the root of a widget it gets the
whole tile. Inside a stack give it `Fill` or `MainSize` like any other child, or put it in a stack whose
cross axis is definite. A node that has to size itself takes the size of its last layout, so a node without a
definite box is judged against the room the last layout needs.

`MainSize`, `Fill`, `ColumnSpan` and `RowSpan` go on the `UiFirstFit`. A layout that sets them is rejected
when the view is built, and so is a layout that is a `UiWhen`, a `UiRepeat` or a fragment.

### What every layout costs

Every layout is built, kept current, sent to the reader and painted, whichever one is on screen. They all
count toward the tree limits: 2000 nodes, 192 KiB per tree and 64 KiB per patch. A clock, an image or an
input inside a layout exists once per layout, and the copy an older reader draws (below) is one more.

Keep the layouts small and build them from a helper method. Keep any control identical across layouts, so a
press means the same thing whichever layout is drawn.

### Older readers and readers that cannot measure

A reader that does not know `ui.first-fit` draws the node's `Fallback`. When you set none, the last layout is
sent a second time as the fallback, under ids below `<id>._fallback`. A reader that cannot measure draws the
last layout as well, so make the last layout the one that is always acceptable, even if it is not the one you
prefer. The same consequences as for [Responsive](https://docs.macro-deck.app/ui/components/responsive/#older-readers) apply: the copy is
patched along with the original, the key `_fallback` is reserved, the copy's ids are longer, and a
[configuration input](https://docs.macro-deck.app/ui/views/configuration/) cannot sit inside the last layout unless you set an explicit
`Fallback`.

### Presses and hardware keys

A pointer press on a drawn control always reaches that control. For the tile's own press, a keyboard
activation or a hardware key on a device, the reader and the host look for a control in every layout, because
only the renderer knows which one fits. A `UiResponsive` nested in a layout counts its default layout there.
When the root of the widget is a `UiFirstFit`, the tile does not treat it as a stack or button: it gets no
transparent tile background and no tile press ring, as with a `UiLayer` root.

### Testing

`UiTestHost` cannot measure, so it lists every layout. `ByType`, `SingleByType` and `ByText` see all of them,
not only the one a reader would draw, and never the copy an older reader draws.

### Reference

| Property (`UiFirstFit`) | Wire | Meaning |
|---|---|---|
| `Children` | `children` | The layouts in order of preference; the last is the fallback |
| `MainSize`, `Fill`, `ColumnSpan`, `RowSpan` | as on any node | The node's slot in its parent |
| `Fallback` | `fallback` | Your own fallback; when absent, a copy of the last layout |

Reader rules:

- Paint every child across the whole box. Show the first one whose texts are not cut off and which does not
  overflow the box, else the last. Hide the others from sight, pointers and assistive technology.
- Measure after the texts have settled, and choose again when the box or a text changes.
- Size an unsized node like its last child.

### See also

- [Responsive](https://docs.macro-deck.app/ui/components/responsive/) - layouts chosen by the size of the box
- [Text](https://docs.macro-deck.app/ui/components/text/)
- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [ADR 0102](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0102-first-fit-layouts-are-chosen-by-measured-text.md)

## Gauge

> Source: https://docs.macro-deck.app/ui/components/gauge/
>
> A read-only level drawn along an arc, or around a full ring.

A read-only level drawn along an arc - a speedometer, a CPU load, a battery ring. It holds a fraction of the
sweep in `0..1`, not a value in your own units.

`ui.gauge`

### Example

```csharp
new UiGauge
{
    Key = "cpu",
    Level = UiValue.From(() => cpu.Value / 100.0),
    Thickness = 0.08,
    LevelColor = "#2b6cee",
    Fallback = new UiRangeBar { Key = "cpuBar", Start = 0, End = UiValue.From(() => cpu.Value / 100.0), StartColor = "#2b6cee", EndColor = "#2b6cee" },
}
```

*[Image: A three-quarter arc open at the bottom, filled in blue to 70 percent over a grey track]*

The default sweep runs from `-135` to `135` degrees: three quarters of a turn, open at the bottom.

### Rings

```csharp
new UiGauge { Key = "battery", Level = 0.4, StartAngle = 0, EndAngle = 360, Thickness = 0.1, LevelColor = "#34c759" }
```

*[Image: A full ring in grey, filled in green clockwise from twelve o'clock to 40 percent]*

Angles are degrees clockwise from twelve o'clock. The sweep is `EndAngle - StartAngle`, so an end before the
start runs counterclockwise; its size is clamped to one full turn.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Level` (`level`) | `0..1` | `0` | The filled fraction of the sweep. |
| `StartAngle` (`startAngle`) | `double`, degrees | `-135` | Where the arc begins, clockwise from twelve o'clock. |
| `EndAngle` (`endAngle`) | `double`, degrees | `135` | Where the arc ends. |
| `LevelColor` (`levelColor`) | `#rrggbb` | The reader's own accent colour | The filled arc's colour. |
| `Thickness` (`thickness`) | length | Left to the reader | The arc's width. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | - | - | Shared with every leaf - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |

`LevelColor` is a literal colour, not a theme role - see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Events

None. `ui.gauge` is never interactive - use [`ui.dial`](https://docs.macro-deck.app/ui/components/dial/) for the same picture the user
can turn.

### Children

None. `ui.gauge` is a leaf. Put a `ui.text` over it in a [layer](https://docs.macro-deck.app/ui/components/stack-and-layer/) to show
the reading in the middle.

### Layout

A gauge has no content extent: on its parent's main axis it takes `MainSize` or `Fill`, and without either
it is `0` long. The arc is drawn in the largest centred square the box allows. See
[Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

The geometry is normative; see the [`UiGauge`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/ui-model/src/MacroDeck.Ui/Components/UiElements.cs)
remarks.

- The sweep is `endAngle - startAngle`, signed, with its magnitude clamped to `360`.
- The arc is centred in the box, `thickness` wide, with a centreline radius of
  `(min(width, height) - thickness) / 2` and fully rounded caps.
- The track covers the whole sweep in the reader's tertiary surface colour. The filled arc runs from the
  start over `level` of the sweep in `levelColor` or the accent colour; `level` is clamped to `0..1`, and `0`
  paints no filled arc.
- A reader that does not know `ui.gauge` draws the node's `fallback`, typically a `ui.range-bar` at the
  same level:

```json
{
  "type": "ui.gauge",
  "properties": { "level": 0.7, "thickness": { "basis": 0.08 }, "levelColor": "#2b6cee" },
  "fallback": {
    "type": "ui.range-bar",
    "properties": { "start": 0, "end": 0.7, "startColor": "#2b6cee", "endColor": "#2b6cee" }
  }
}
```

### See also

- [Dial](https://docs.macro-deck.app/ui/components/dial/)
- [Range bar](https://docs.macro-deck.app/ui/components/range-bar/)
- [Transform](https://docs.macro-deck.app/ui/components/transform/) - a needle over your own artwork

## Grid

> Source: https://docs.macro-deck.app/ui/components/grid/
>
> A container laying its children out in equal columns and rows, with column and row spans.

Lays its children out in equal columns and rows - a keypad, a set of stats, a dashboard with one wide
cell - without nesting stacks.

`ui.grid`

### Example

```csharp
new UiGrid
{
    Key = "stats",
    Columns = 2,
    Gap = 0.04,
    Padding = 0.06,
    Children =
    [
        new UiStack { Key = "cpu", Background = "#1c2430", ColumnSpan = 2, Children = [cpuChart] },
        new UiTextRun { Key = "ram", Text = UiText.From(() => $"{ram.Value:0} %") },
        new UiTextRun { Key = "gpu", Text = UiText.From(() => $"{gpu.Value:0} %") },
    ],
    Fallback = new UiStack { Key = "statsFallback", Children = [cpuRow, ramAndGpuRow] },
}
```

*[Image: A two-by-two tile with one wide cell across the top row and two cells side by side beneath it]*

A wide chart across the top and two readings beneath it.

### Placement

Children are placed in declaration order. Each takes the first position, scanning row by row from the top
left, where its whole `ColumnSpan` by `RowSpan` block is free:

```
Columns = 3; children A (ColumnSpan 2), B (RowSpan 2), C, D

  +-----+-----+-----+
  |  A        |  B  |
  +-----+-----+     +
  |  C  |  D  |     |
  +-----+-----+-----+
```

A later small child can fill a hole an earlier large one left, so the order on screen can differ from the
order of the children.

### Spans and rows

`ColumnSpan` and `RowSpan` sit on every element and mean something only under a grid; any other parent
ignores them. A span below `1` counts as `1`, and a column span wider than the grid is clamped to `Columns`.

Leave `Rows` absent and the grid has as many rows as placement needs. Set it and a child that does not fit
in those rows is not drawn.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Columns` (`columns`) | `int` | `1` | The column count; below `1` means `1`. |
| `Rows` (`rows`) | `int` | As many as needed | The row count; children that do not fit are not drawn. |
| `Gap` (`gap`) | length | No gap | The gap between columns and between rows. |
| `Padding` (`padding`) | length | No padding | Inner padding on every edge. |
| `MainSize` (`mainSize`), `Fill` (`fill`), `Answer` (`answer`) | - | - | Shared with every container - see [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/). |

On a grid's children:

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `ColumnSpan` (`columnSpan`) | `int` | `1` | How many columns the child covers; clamped to `Columns`. |
| `RowSpan` (`rowSpan`) | `int` | `1` | How many rows the child covers. |

### Events

None of its own.

### Children

Any element, any number.

### Layout

The content box minus padding is divided into equal column and row tracks separated by `gap`, and each child
is drawn across its block. A child's `mainSize` and `fill` mean nothing here, because the grid decides the
block. Lengths inside a child keep resolving against the widget basis, not the cell, so text is the same
size in a grid as anywhere else. On its own parent's main axis a grid has no content extent: give it
`MainSize` or `Fill`. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- Treat an absent or below-`1` `columns`, `columnSpan` or `rowSpan` as `1`; clamp `columnSpan` to
  `columns`.
- Place children with the dense row-major rule above; with `rows` present, skip a child whose block does
  not fit and keep placing the ones after it.
- Draw each child across its block, ignoring its `mainSize` and `fill`; keep the widget basis unchanged.
- Hold `columns`, `rows`, `columnSpan` and `rowSpan` to at most 64.
- Where the parent leaves the grid's height open - inside a vertical [list](https://docs.macro-deck.app/ui/components/list/) - make
  every row as tall as a column is wide, and the grid as tall as its rows need.
- A reader that does not know `ui.grid` draws the node's `fallback`, typically nested `ui.stack` rows:

```json
{
  "type": "ui.grid",
  "properties": { "columns": 2, "gap": { "basis": 0.04 } },
  "children": [
    { "type": "ui.text", "properties": { "text": "A" } },
    { "type": "ui.text", "properties": { "text": "B" } }
  ],
  "fallback": {
    "type": "ui.stack",
    "properties": { "direction": "horizontal", "gap": { "basis": 0.04 } },
    "children": [
      { "type": "ui.text", "properties": { "text": "A", "fill": true } },
      { "type": "ui.text", "properties": { "text": "B", "fill": true } }
    ]
  }
}
```

### See also

- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## Icon

> Source: https://docs.macro-deck.app/ui/components/icon/
>
> One glyph of Macro Deck's built-in icon set, drawn by name in one colour, with no resource to upload.

One glyph from Macro Deck's own icon set, named rather than uploaded. It is drawn as a single-colour mask,
so it takes a theme role or a literal colour like text does.

`ui.icon`

### Example

```csharp
new UiIcon
{
    Key = "state",
    Icon = UiValue.From(() => state.Value.Playing ? UiIcons.Pause : UiIcons.Play),
    Size = 0.4,
    Role = UiComponentTextRoles.Primary,
    Fallback = new UiTextRun { Key = "stateLabel", Text = UiText.From(() => state.Value.Playing ? "Pause" : "Play") },
}
```

*[Image: A white play glyph centred in a tile]*

A play/pause glyph: switching it is a `set-properties` patch carrying `icon` alone.

### Colour

```csharp
Color = "#34c759",
```

`Role` picks a theme role and follows the viewer's theme; `Color` is a literal colour that overrides it. See
[Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Names and versions

A reader draws a glyph only for a name it carries. Names are published in groups: group 1 is
`UiIcons.Version1` below, and every later name arrives in a new group that raises `ui.icon`'s maximum
component version. A name is never removed or renamed, and it keeps its meaning: the drawing of a name may be
restyled, for example when Macro Deck's icons moved to the Lucide set, but it always denotes the same concept.

Use the `UiIcons` constants rather than string literals. For a name above group 1, ask for its version and
carry a fallback, so an older reader draws the fallback instead of an empty box:

```csharp
RequiredComponentVersion = UiIcons.VersionOf(name),
Fallback = new UiTextRun { Key = "label", Text = "Wi-Fi" },
```

`UiIcons.VersionOf` returns `1` for every name listed here and `null` for a name no version draws. A
`RequiredComponentVersion` of `1` or `null` asks for nothing beyond knowing the type.

### Published names

Component version 1 draws these 76 names:

`action-button-type`, `alert-triangle`, `align-bottom`, `align-center`, `align-left`, `align-middle`,
`align-right`, `align-top`, `arrow-down`, `arrow-left`, `arrow-right`, `arrow-up`, `bell`, `braces-x`,
`bug`, `chart`, `check`, `chevron-right`, `clipboard`, `clock-type`, `code`, `copy`, `crosshair`,
`device-desktop`, `device-floppy`, `device-phone`, `device-tablet`, `disc`, `discord`, `dots-vertical`,
`download`, `external-link`, `file-text`, `folder`, `folder-plus`, `globe`, `grid`, `heart`,
`history-graph-type`, `image`, `info`, `layers`, `list-play`, `lock`, `log-out`, `message-square`, `minus`,
`moon`, `music-note`, `music-player-type`, `pause`, `pencil`, `pin`, `pin-off`, `play`, `plus`, `power`,
`puzzle`, `refresh`, `scissors`, `search`, `settings`, `sidebar`, `sliders`, `star`, `store`, `sun`,
`trash`, `undo`, `unlock`, `upload`, `user`, `weather-type`, `wifi`, `x`, `zap`.

The C# constant is the name in PascalCase - `UiIcons.AlertTriangle` is `alert-triangle`. The list is
[`UiIcons`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/ui-model/src/MacroDeck.Ui/Components/UiComponentValues.cs);
[ADR 0084](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0084-built-in-icon-names-are-a-versioned-public-vocabulary.md)
records why it is frozen.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Icon` (`icon`) | a `UiIcons` name | Draws nothing | The glyph. |
| `Size` (`size`) | length | The box's smaller side | The edge of the square the glyph is drawn in. |
| `Role` (`role`) | `UiComponentTextRoles` | `primary` | The theme colour; ignored when `Color` is present. |
| `Color` (`color`) | `#rrggbb` | Uses `Role` | A literal colour overriding `Role`. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | - | - | Shared with every leaf - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |

### Events

None. Put the icon inside a [button](https://docs.macro-deck.app/ui/components/button/) to press it.

### Children

None. `ui.icon` is a leaf.

### Layout

On its parent's main axis an icon is `Size` long unless `MainSize` or `Fill` says otherwise. The glyph is
centred in its box. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- Draw the glyph as a single-colour mask in a `size` square centred in the box, in `color`, else `role`, else
  the primary text colour.
- Draw nothing for a name outside the groups the reader carries - never a placeholder square.
- Advertise as the maximum component version the number of name groups carried.
- A reader that does not know `ui.icon` draws the node's `fallback`, typically a `ui.text` saying what the
  icon meant:

```json
{
  "type": "ui.icon",
  "properties": { "icon": "play", "size": { "basis": 0.4 } },
  "fallback": { "type": "ui.text", "properties": { "text": "Play" } }
}
```

### See also

- [Image](https://docs.macro-deck.app/ui/components/image/) - your own artwork
- [Resources](https://docs.macro-deck.app/ui/reference/resources/)
- [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/)
- [Compatibility](https://docs.macro-deck.app/ui/reference/compatibility/)

## Image

> Source: https://docs.macro-deck.app/ui/components/image/
>
> Draws a resource handle, fitted into a square box and never cropped.

Draws a registered resource, fitted into a square box. A tree never carries image bytes, only a handle
that each client fetches and caches by hash.

`ui.image`

### Example

```csharp
new UiImage
{
    Key = "icon",
    Source = UiValue.From(() => state.Value.ConditionIcon),
    Size = 0.16,
    Transition = UiComponentImageTransitions.Crossfade,
}
```

*[Image: A weather tile with a small yellow sun icon above the temperature 23° and the caption Sunny]*

A weather-condition icon that fades to the new one when the condition changes, adapted from the built-in
Weather widget. `ConditionIcon` is a `UiResource` handle.

A plugin registers its own images with `IIntegrationContext.UiResources`; see
[Registering your own images](https://docs.macro-deck.app/ui/reference/resources/#registering-your-own-images).

### Changing artwork smoothly

```csharp
Transition = UiComponentImageTransitions.Crossfade,
```

Without `Transition`, a new `Source` simply replaces the old image.

### Dimming artwork

```csharp
Brightness = 0.6,
Saturation = 0.55,
```

*[Image: The same album cover twice: at full colour on the left, darker and less saturated on the right]*

A paused cover, as the built-in Music player draws it. `Brightness` changes the artwork itself and looks the
same on any background - use it, not a lower `Opacity`, for "the same picture, darker". `Opacity` lets what
is behind show through. `Saturation = 0` draws in greys.

### Recolouring an icon

```csharp
Tint = "#4f8cff",
```

Draws the image as a silhouette in that colour: every pixel keeps its own transparency, so a white icon on a
transparent background becomes a blue icon, while an image without transparency becomes a solid rectangle.
The built-in Slider uses it for its Icon Color setting.

### A source that may be missing

```csharp
Source = UiValue.Optional(() => state.Value.Icon is { } icon
    ? UiValue.Of(icon)
    : UiValue.None<UiResource>()),
```

An absent or unresolvable source draws nothing. Wrap the image in a `UiWhen` instead if it
should not take up space either.

### Properties

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Source` (`source`) | `UiResource` handle | Nothing is drawn | The resource to draw. |
| `Size` (`size`) | `UiSize` length | Left to the reader | The edge of the square box the image is fitted into, preserving aspect ratio and never cropped. |
| `Transition` (`transition`) | `UiComponentImageTransitions`: `crossfade` | The new image replaces the old at once | How a change of `Source` is drawn. |
| `Opacity` (`opacity`) | `0..1` | Fully opaque | How opaque the image is drawn. |
| `Brightness` (`brightness`) | `0..2` | `1` | A multiplier of the image's own luminance. |
| `Saturation` (`saturation`) | `0..2` | `1` | A multiplier of the image's own saturation; `0` is greyscale. |
| `Tint` (`tint`) | `#rrggbb` | The image's own colours | Draws the image in this colour, keeping each pixel's transparency. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/) | `Size` | The image's extent along the parent stack's main axis. |

### Events

None. `ui.image` is never interactive. For a tappable image, use a [Button](https://docs.macro-deck.app/ui/components/button/) with
`Source` set; it adds `Fit`, `Zoom`, `OffsetX` and `OffsetY` framing on top of `Opacity`, `Brightness` and
`Saturation`.

### Children

None. `ui.image` is a leaf.

### Layout

An image is `size` on both axes, fitted into a square box. Along its parent stack's main axis it takes
`mainSize` or `fill` if declared, otherwise `size` is what a reader measures it at without a font. See
[Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- A `source` that cannot be resolved draws nothing; it never fails the tree.
- Fit the image into the square box preserving aspect ratio; never crop.
- `crossfade` is normative: hold the outgoing artwork until the incoming one has decoded, then reveal it over
  220 ms on an ease-out curve, from fully transparent at scale 1.02 about its centre to fully opaque at
  scale 1.
- Artwork that fails to decode replaces the outgoing artwork at once, with no fade.
- `brightness` is normative: multiply each channel by the value, before `saturation` and before
  compositing at `opacity`, and clamp each channel rather than wrapping it.
- `saturation` is normative: `out = luma + saturation * (channel - luma)`, with
  `luma = 0.213 R + 0.715 G + 0.072 B`, applied after `brightness`.
- `tint` is normative: every pixel takes the colour and keeps its own alpha, then `opacity` applies. A reader
  that does not implement the key, or whose engine cannot mask, draws the image in its own colours.

### See also

- [Resources](https://docs.macro-deck.app/ui/reference/resources/)
- [Button](https://docs.macro-deck.app/ui/components/button/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## List

> Source: https://docs.macro-deck.app/ui/components/list/
>
> A scrolling container for dialogs that asks for more children as the user reaches its end.

A container that scrolls, and tells you when the user reaches the end of what it holds. It is for the
**dialog** surface: a deck tile is a fixed box, and a list in one would hide content behind a gesture the
deck itself uses.

`ui.list`

### Example

```csharp
new UiList
{
    Key = "results",
    Fill = true,
    Gap = UiSize.FromBasis(0.015),
    Events = [UiEventHandler.On(UiComponentEvents.Reveal, OnRevealed)],
    Children =
    [
        new UiRepeat<CatalogItem>
        {
            Key = "rows",
            Items = UiValue.From<IReadOnlyList<CatalogItem>>(() => items.Value.Take(window.Value).ToList()),
            KeySelector = item => item.Id,
            Template = (item, _) => Row(item),
        },
    ],
}
```

*[Image: A scrolling list of track rows, each with a cover, a title and an artist line; the last row is cut off at the bottom edge]*

A windowed result list, adapted from the built-in music picker: it starts with a few rows and grows as the
user scrolls.

### Loading more items

```csharp
void OnRevealed(UiEventData data)
{
    if (!data.TryGetDouble(out var index)) return;

    var wanted = (int)index + 25;
    if (wanted > window.Value) window.Value = wanted;
}
```

`reveal` carries the index of the furthest child the user has brought into view. Append children, or do
not; there are no page sizes and no "has more" flag. When you run out, append nothing - the reader asks
again only once the user goes further than before.

Replacing the rows, as a new search does, starts that over: once the list holds fewer children than before,
or a different child sits where the furthest one reported was, the reader reports again from what is in view,
even an index at or below one it sent earlier. Grow your window only when the new index asks for more, as
above, so a lower index never takes rows away. If you shrink your window but the list still shows the same
children, the reader cannot tell, and asks again only beyond the furthest index it already reported.

### Keeping rows stable

```csharp
KeySelector = item => item.Id,
```

Key rows by the item's own id, never its position. Rows are patched in place as the list grows or a filter
narrows it, and a positional key would re-key everything below the change.

### Showing an empty or loading state

```csharp
new UiWhen
{
    Key = "emptyWhen",
    Condition = () => items.Value.Count == 0,
    Content = () => new UiTextRun { Key = "empty", Text = "Nothing found", Role = UiComponentTextRoles.Secondary },
},
```

"Loading" and "empty" are your own state, so express them as ordinary children of the list rather than
properties.

### Scrolling horizontally

```csharp
new UiList
{
    Key = "covers",
    Direction = UiComponentDirections.Horizontal,
    RequiredComponentVersion = 2,
    Fallback = new UiStack { Key = "coversFallback", Children = [firstCover] },
    Children = covers,
}
```

`Horizontal` needs component version 2. A version 1 reader ignores `direction` and scrolls vertically,
so ask for version 2 and carry a `ui.stack` fallback.

### Following the end

```csharp
new UiList
{
    Key = "chat",
    Fill = true,
    Anchor = UiComponentListAnchors.End,
    RequiredComponentVersion = 3,
    Fallback = new UiList
    {
        Key = "chatNewestFirst",
        Fill = true,
        Children = [new UiRepeat<ChatMessage> { Key = "rows", Items = newestFirst, KeySelector = m => m.Id, Template = Row }],
    },
    Children = [new UiRepeat<ChatMessage> { Key = "rows", Items = oldestFirst, KeySelector = m => m.Id, Template = Row }],
}
```

A chat or a log appends at the bottom. With `Anchor = End` the reader keeps the view at the end while the
user is there, so each new row scrolls into view. Once the user scrolls up to read, new rows and rows removed
above the view, such as the oldest messages dropping off a capped history, leave the view where it is, and
the reader offers a way back to the newest row. You send nothing and receive nothing for any of this: where
the view is belongs to the reader.

Only a vertical list follows its end. `End` needs component version 3; an older reader ignores `anchor` and
leaves the newest row below the fold, so ask for version 3 and carry a fallback that shows the newest row
first, such as the same rows in reverse order.

### Properties

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Direction` (`direction`) | `UiComponentDirections.Vertical`, `.Horizontal` (`vertical`, `horizontal`) | `vertical` | The scroll axis; `horizontal` needs component version 2. |
| `Anchor` (`anchor`) | `UiComponentListAnchors.Start`, `.End` (`start`, `end`) | `start` | Which end the view holds on to; `end` follows new rows at the end of a vertical list and needs component version 3. |
| `Gap` (`gap`) | length | No gap | The gap between children. |
| `Padding` (`padding`) | length | No padding | Inner padding on every edge. |
| `Background` (`background`) | `#rrggbb` | Paints nothing behind its children | The list's own fill, a literal colour like every container fill - see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/). |
| `MainSize` (`mainSize`), `Fill` (`fill`), `Answer` (`answer`) | - | - | Shared with every container - see [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/). |

### Events

Declared only where `Events` names it - see [Events](https://docs.macro-deck.app/ui/concepts/events/).

| Event | When | Payload |
|---|---|---|
| `UiComponentEvents.Reveal` (`reveal`) | The user has reached the end of what the list currently holds | The index of the furthest child brought into view, as a bare number |

### Children

Any element, any number, one after another along the scroll axis.

### Layout

The main axis - `y` for a vertical list, `x` for a horizontal one - is unbounded: children take their
natural extent along it, and their `mainSize`/`fill` are ignored on that axis. Across it, each child takes
the list's inner extent. On its own parent's main axis a list follows the ordinary container rule:
`mainSize` or `fill` if declared, otherwise its content extent. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- Send `reveal` only if the node declares it.
- Send at most two `reveal` events a second, and only for an index beyond the furthest one already sent
  for the same list's current content.
- Start that over when the list holds fewer children than at its previous paint, or when the child at the
  furthest index sent is gone or has a different id: the content was replaced.
- When the throttle holds back an index the user has reached, send it as soon as the throttle allows: a user
  already at the end of the list may never scroll again.
- The payload is a child index, not a page; never assume a page size.
- A version 1 reader ignores `direction` and scrolls vertically - negotiation catches unknown types, not
  unknown values, so producers pair `horizontal` with version 2 and a fallback.
- Ignore children's `mainSize` and `fill` on the scroll axis.
- `anchor` absent, `start` or a value you do not know: leave the view where the user put it, as always.
  `end` on a vertical list:
  - While the view is at the end of the list, keep it there: after a paint that adds or removes children,
    and while children grow after one, scroll to the end.
  - Once the user has scrolled away from the end, never move the view for a content change. When children
    above the view are removed, keep the first visible child that is still there at the same offset from
    the top edge.
  - Deciding whether the view is at the end is up to the user's own scrolling: a paint, a resized box or
    children that grew are not the user leaving the end.
  - When a child the list did not hold before arrives last while the user is away, offer a way back to the
    end, such as a control that scrolls there. Removing the last child is not new content. The control must
    not count as a press on any node, and it goes away once the view is back at the end. A reader that
    cannot keep it in view, such as an engine without sticky positioning, may leave it out.
  - A horizontal list ignores `anchor`.
  - None of this is reported to the producer.
- Advertise `ui.list` version 3 only once you follow the end; a version 2 reader ignores `anchor`, so
  producers pair `end` with version 3 and a fallback.

### See also

- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [Text field](https://docs.macro-deck.app/ui/components/text-field/) - the other dialog-only element
- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## Modifier

> Source: https://docs.macro-deck.app/ui/components/modifier/
>
> Background, border, radius, accessibility, disabled and gestures on any node, and padding, opacity, clip, mask and frame through a wrapper.

One DSL element, `UiModifier`, decorates the single element it wraps. What reaches the wire depends on
which members you set, because the two halves degrade differently on an older reader:

- **The `modifiers` property** carries the members that change no geometry. It sits on the wrapped node
  itself, and a reader that does not know it ignores it and draws the node plainer.
- **The `ui.modifier` type** carries padding, opacity, clip, mask and frame. Ignoring any of them would
  draw something wrong or move its siblings, so they are a negotiated type: an older reader draws your
  explicit `Fallback`, and there is no default one. Without a fallback, an older reader draws none of the
  wrapped content (Macro Deck's own renderer shows a faint placeholder box in its place) - see
  [The UI model](https://docs.macro-deck.app/ui/concepts/ui-model/#a-node).

`ui.modifier` (component version 1)

### Example

```csharp
new UiModifier
{
    Key = "card",
    Background = UiGradient.Linear(135,
        new UiGradientStop { Offset = 0, Color = "#2b6cee" },
        new UiGradientStop { Offset = 1, Color = "#7a3cf0" }),
    Radius = 0.12,
    Padding = 0.08,
    Child = new UiImage { Key = "icon", Source = icon },
    Fallback = new UiImage { Key = "iconPlain", Source = icon },
}
```

*[Image: A white music note inset from the edges of a rounded tile filled with a blue-to-violet diagonal gradient]*

`Padding` makes this a `ui.modifier` node, so the gradient and radius sit on the wrapper and cover the
padding. An older reader draws the plain icon.

### Decorating a node

```csharp
new UiModifier
{
    Key = "roomCard",
    Background = "#1c1c1e",
    Radius = 0.1,
    BorderWidth = UiSize.Capped(2d / UiLength.Cell, 2),
    BorderColor = "#ff9500",
    BorderLine = UiComponentBorderLines.Dashed,
    AccessibilityLabel = UiText.Of(strings.RoomLabel),
    Child = new UiStack { Key = "room", Children = [/* ... */] },
}
```

```json
{ "id": "room", "type": "ui.stack", "properties": { "modifiers": { "background": "#1c1c1e", "radius": { "basis": 0.1 }, "borderWidth": { "basis": 0.0167, "maxOfCell": 0.0167 }, "borderColor": "#ff9500", "borderLine": "dashed", "accessibilityLabel": {"$localized":…} } }, "children": [] }
```

*[Image: A white music note inside a dark rounded square traced by a dashed orange border, on a black tile]*
*[Image: The same music note inside a solid orange border]*
*[Image: The same music note inside a dotted orange border]*
*[Image: A button whose gradient artwork fills the tile inside its padding, framed by a white border drawn above the artwork]*
*[Image: A music note on a tile filled with a flat blue background]*
*[Image: A heart on a tile filled with a pink-to-orange linear gradient]*
*[Image: A power symbol on a tile filled with a green radial gradient that darkens towards the edges]*
*[Image: A music note on a blue square whose corners are rounded by the radius modifier]*

With only these members set, the modifier adds no node: the members land on the child's `modifiers`
object and the id stays the child's. The child must then build to exactly one component node - a `UiWhen`,
`UiRepeat` or fragment child is rejected when the view is built. Nested modifiers of this kind merge onto
the same node; setting the same member twice on one node is rejected. Because it produces no node of its
own, such a modifier cannot set `MainSize`, `Fill`, `ColumnSpan`, `RowSpan`, `Answer`, `Fallback` or
`RequiredComponentVersion` - set those on the child, or add a wrapper member to make it a `ui.modifier`
node.

### Events on a modifier

```csharp
new UiModifier
{
    Key = "pagerGestures",
    Events = [UiEventHandler.On(UiComponentEvents.Swipe, e => { if (e.TryGetString(out var dir)) Page(dir); })],
    Child = pager,
}
```

A modifier's handlers join the declared events of the node its members land on. When the modifier and the
child both handle a name, both run: the child first, then the modifiers from the inside out.

### Gestures

| Event | Fires | Payload |
|---|---|---|
| `drag` (`UiComponentEvents.Drag`) | While the pointer moves, once it has travelled `0.04` of the basis. At most every `100 ms`. | `{"x":n,"y":n}`, the translation since the gesture began, in basis fractions, `x` right-positive, `y` down-positive |
| `drag-end` (`UiComponentEvents.DragEnd`) | Once on release, only after a `drag` began. Not sent if the node leaves the tree or becomes disabled mid-drag. | As `drag`, the final translation |
| `swipe` (`UiComponentEvents.Swipe`) | On release, when the dominant axis travelled at least `0.2` of the basis within `500 ms`. | `"left"`, `"right"`, `"up"` or `"down"` |
| `pinch` (`UiComponentEvents.Pinch`) | While two pointers move. At most every `100 ms`. | A bare number, the scale since the pinch began |
| `pinch-end` (`UiComponentEvents.PinchEnd`) | Once, when the pinch ends. Not sent if the node leaves the tree or becomes disabled mid-pinch. | As `pinch`, the final scale |

The constants live on `UiComponentModifiers` (`GestureSlop`, `SwipeMinDistance`, `SwipeMaxDurationMs`,
`GestureThrottleMs`). A gesture can be declared on any node, with or without a modifier.

- **Inner controls win.** A pointer that starts inside a descendant that takes a value (a slider, dial,
  toggle, segmented control or text field), declares a gesture of its own, or is a `ui.list` belongs to
  that descendant.
- **An inner press wins until slop.** Once the pointer travels past `0.04` of the basis, the outer gesture
  takes over and the press ends with `press-end` and no `press`.
- **Touch action.** A node declaring a gesture turns off the browser's own panning and zooming for its box.
  A `ui.list` inside it keeps scrolling.
- **On a deck tile, a gesture claims the pointer but not a key.** A tree declaring a gesture takes every
  pointer press on its tile, so the tile's own long-press cannot fire in the middle of a drag. Keyboard and
  physical-control activation cannot drag, so a tree that declares only gestures still runs the tile's own
  flow from a key.
- `pinch` on iOS, and every gesture at the Safari 9 floor, is unverified.

### Pointer streams and taps

`drag`, `swipe` and `pinch` report a recognised gesture. For a surface that needs every finger - a touchpad,
a drawing pad, a joystick - declare the pointer family instead:

```csharp
new UiModifier
{
    Key = "touchpad",
    Events =
    [
        UiEventHandler.On(UiComponentEvents.PointerDown, e =>
        {
            if (e.TryGetPointerDown(out var down)) fingers[down.Sample.Id] = down.Sample;
        }),
        UiEventHandler.On(UiComponentEvents.PointerMove, e =>
        {
            if (!e.TryGetPointerSamples(out var samples)) return;
            foreach (var sample in samples)
            {
                if (fingers.Count == 1 && fingers.TryGetValue(sample.Id, out var last))
                    mouse.MoveBy(sample.X - last.X, sample.Y - last.Y);
                fingers[sample.Id] = sample;
            }
        }),
        UiEventHandler.On(UiComponentEvents.PointerUp, e =>
        {
            if (e.TryGetPointerUp(out var up)) fingers.Remove(up.Sample.Id);
        }),
        UiEventHandler.On(UiComponentEvents.Tap, e =>
        {
            if (e.TryGetTap(out var pointers)) mouse.Click(pointers == 2 ? MouseButton.Right : MouseButton.Left);
        }),
    ],
    Child = new UiStack(),
}
```

`fingers` is a `Dictionary<int, UiPointerSample>` the view keeps, and `mouse` stands for the plugin's own
input code.

| Event | Fires | Payload |
|---|---|---|
| `pointer-down` (`UiComponentEvents.PointerDown`) | A finger, pen or primary mouse button went down on the node. | `{"id":n,"x":n,"y":n,"t":n,"width":n,"height":n}` |
| `pointer-move` (`UiComponentEvents.PointerMove`) | Pointers moved. At most every `16 ms`, carrying every position since the previous one, except that waiting samples are sent at once before any other event of the family. | `{"samples":[{"id":n,"x":n,"y":n,"t":n}, ...]}`, oldest first, at most `256` |
| `pointer-up` (`UiComponentEvents.PointerUp`) | A pointer lifted, or the platform cancelled it. | `{"id":n,"x":n,"y":n,"t":n}`, plus `"cancelled":true` for a cancelled one |
| `tap` (`UiComponentEvents.Tap`) | After the last `pointer-up` of a touch that took at most `400 ms` from the first finger down to the last finger up, in which no pointer travelled more than `0.04` of the basis and none was cancelled. | `{"pointers":n}`, the most fingers down at once |

- **Ids.** `id` is an opaque integer that stays the same from a pointer's `pointer-down` to its `pointer-up`.
  Every reader starts its ids at a random point, so two decks on one shared widget reporting the same id is
  very unlikely, though not impossible.
- **Positions** are relative to the node's top-left corner in basis fractions, `x` right-positive, `y`
  down-positive; `width` and `height` on `pointer-down` give the node's size in the same unit. Inside a
  rotated `ui.transform` they are in screen axes, as `drag` is.
- **Time.** `t` is whole milliseconds since the first finger of the current touch went down, so samples of
  different fingers line up.
- **Order.** Waiting samples are always sent before any other event of the family, and `tap` after the last
  `pointer-up`.
- **A newer move may replace an older one.** While a `pointer-move` for the same node from the same client
  is still waiting to be delivered, Macro Deck and the plugin runtime may drop it in favour of the newer one,
  and a move the plugin could not take because it was busy or slow is dropped instead of ending the session.
  A finger that appeared only in a dropped batch keeps its older position until it moves again or lifts.
  Read time from `t`, never from the number of events.
- **Handle `pointer-move` synchronously and do not rebuild the tree for each one.** An asynchronous handler
  is started for every event and not awaited, so slow ones pile up and may finish out of order. UI updates
  are limited to 30 a second (a burst of 90); a tree that changes on every move soon ends its session.
- **`pointer-up` is not guaranteed after a connection ends.** One follows each `pointer-down` while the node
  still declares it, is enabled and is in the tree. Nothing arrives after the client disconnects or leaves the
  view, or when a stalled connection drops events: release whatever a finger holds when the session ends, and
  do not keep a mouse button held for a finger that has sent nothing for a while.
- **The node owns its fingers.** A pointer that starts on a node declaring any of the four belongs to it: an
  ancestor's `drag`, `pinch` or press does not take it, the browser does not pan under it, and a `ui.list`
  cannot be scrolled from a touch that starts there. Nested nodes: the innermost one owns the finger, so one
  touch taps once.
- **Buttons on a pad.** A finger that starts on a button inside the node is still streamed to the node, the
  button still presses, and that touch sends no `tap`. A touch on a node that declares a press name itself
  sends no `tap` either. Once a streamed finger travels past the slop, a press it started ends without
  `press`, as with `drag`.
- **Keys and hardware.** A tree declaring only the pointer family still runs the tile's own flow from a key
  or a hardware deck; nothing is streamed from them. The interactive screensaver does not pass the pointer
  to these nodes.
- The constants are `UiComponentModifiers.PointerMoveIntervalMs`, `PointerMoveMaxSamples` and
  `TapMaxDurationMs`. Below the Safari 9 floor the pointer family is unverified.

### Disabled

```csharp
new UiModifier { Key = "controlsState", Disabled = UiValue.From(() => !connected.Value), Child = controls }
```

`Disabled` is shorthand for the producer, not a second source of truth: [events stay the
contract](https://docs.macro-deck.app/ui/concepts/events/#interaction-only-where-declared).

- **The DSL strips events.** While `Disabled` is true, no node in the wrapped subtree, and none in its
  fallback, declares an event, and `UiView.Dispatch` answers `Ignored` for any of them.
- **On the wire it is presentation.** `disabled: true` dims the node to `0.4` opacity once - a disabled
  region inside another is not dimmed twice - and marks the subtree `aria-disabled`.
- **Readers refuse events inside a disabled region**, even when a hand-written tree still declares them, and
  a slider, dial, toggle, segmented control or text field inside one cannot be operated.
- **A disabled region absorbs every press on the tile.** If any node in a deck tile's tree is disabled,
  pressing anywhere on the tile runs none of the tile's own flows. `Disabled` therefore means "a control
  that is unavailable"; to fade something that is only decorative, use `Opacity` instead. On a hardware
  deck the host asks a plugin tile's tree once per press. A tree that does not answer within a second, or
  a plugin already at its limit of open views, absorbs that press as well.

*[Image: A mute button tile, dimmed: the red face, the crossed-out microphone and the Mute label all shown at reduced opacity]*

An older reader ignores `disabled` and draws the region undimmed. Because the DSL stripped its events, it
offers none of them either, but it does not absorb the tile's press: on a deck tile, the tile's own flows
still run there, as they do from a hardware key today.

Known gaps:

- The web client's keyboard and hardware activation honours the absorption but not the tree's own
  activation.

### Properties

#### `modifiers` (on any node)

| DSL member (wire member) | Values | Absent | An older reader |
|---|---|---|---|
| `Background` (`background`) | `#rrggbb`, a linear or a radial gradient | No change | Draws the node's own background |
| `Radius` (`radius`) | length | The node's own corner | Draws the node's own corner |
| `BorderWidth` (`borderWidth`) | length | No border | Draws no border |
| `BorderColor` (`borderColor`) | `#rrggbb` | The reader's choice - set it whenever the colour matters | Draws no border |
| `BorderLine` (`borderLine`) | `solid`, `dashed`, `dotted` | `solid` | Draws no border |
| `AccessibilityLabel` (`accessibilityLabel`) | localized text | No label | Omits the label |
| `AccessibilityHint` (`accessibilityHint`) | localized text | No hint | Omits the hint |
| `Disabled` (`disabled`) | `true` | Not disabled | Draws the node undimmed |

A gradient travels as `{"linear":{"angle":deg,"stops":[{"offset":0..1,"color":"#rrggbb"}]}}`, angle in the
CSS convention (`0` towards the top, clockwise), or `{"radial":{"centerX":0..1,"centerY":0..1,"stops":[...]}}`,
with at least two stops; a reader draws no gradient from fewer, or from any stop it cannot read.
Colours are literal, like every data colour - see [Theming](https://docs.macro-deck.app/ui/concepts/theming/#literal-colours). On a
stack, button or list, `background` and `radius` replace the component's own background and corner.

#### `ui.modifier`

| DSL member (wire property) | Values | Absent |
|---|---|---|
| `Padding` (`padding`) | length | No padding |
| `Opacity` (`opacity`) | `0..1` | Fully opaque |
| `Clip` (`clip`) | `bounds`, `circle`, `capsule` | Nothing is clipped |
| `Mask` (`mask`) | a linear or radial gradient of `{"offset","opacity"}` stops | No mask |
| `Frame` (`frame`) | `width`, `height`, `minWidth`, `maxWidth`, `minHeight`, `maxHeight` lengths, `aspectRatio` greater than `0` | The box the parent hands it |
| `MainSize` (`mainSize`), `Fill` (`fill`), `Answer` (`answer`) | - | Shared with every container - see [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/#shared-with-every-container). |

The wrapper node may also carry `modifiers` and `events`. Enum values live in `UiComponentClips` and
`UiComponentBorderLines`.

*[Image: A gradient disc clipped to a circle in the middle of a black tile]*
*[Image: A gradient tile whose lower part fades out through a linear mask]*
*[Image: A gradient card held to a 16:9 aspect ratio inside a tile two cells wide]*
*[Image: Artwork shown at reduced opacity over the tile background]*
*[Image: A gradient square clipped to its bounds with rounded corners]*
*[Image: A wide gradient card clipped to a capsule with fully rounded ends]*
*[Image: A gradient card at a fixed width and height in the middle of a tile]*
*[Image: A filling gradient card held between a minimum and maximum width inside a tile two cells wide]*

**Why padding is here.** Padding could have been a plain property, but padding on an arbitrary node
changes that component's own geometry, so a reader ignoring it would lay the siblings out wrongly rather
than just more plainly.

### Children

Exactly one element.

### Layout

The wrapper lays its child out in its own box minus `padding` on every edge. `frame` fixes or clamps the
wrapper's box and, with `aspectRatio`, its shape; a frame smaller than the space it is given is centred in
it. On its parent's main axis the wrapper is its child's content extent plus twice the padding, or the
frame's fixed length, clamped by the frame's minimum and maximum.

Wrapping moves `MainSize` and `Fill` to the wrapper: set them on the `UiModifier`, since a wrapped child
that sets them is rejected when the view is built. A filling wrapper's maximum clamps only its own size;
the surplus is not handed to its siblings. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/#frames-and-wrapping).

### Reader behaviour

- **`radius` does not clip.** It rounds the background and border only; to clip content, use `clip` on a
  wrapper. `clip: bounds` rounds by the wrapper's own `modifiers.radius`.
- **`radius` is ignored on the tree root**, because the tile's corner belongs to the surface
  ([ADR 0065](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0065-the-component-profile-authoring-contracts.md#the-corner-radius-is-part-of-the-surface)).
- **The border is drawn inside the edge.** It takes no space, so the node's content and its
  children's boxes are unchanged. On a stack, button, layer, transform, grid, toggle, segmented control or
  `ui.modifier` it is a layer above the content, including a button's artwork; on every other node it is an
  outline, which an older engine may draw with square corners.
- **Opacity** covers the whole wrapper; a disabled wrapper at `opacity: 0.5` shows at `0.2`.
- **A fallback is its own node.** A reader drawing a node's fallback draws the fallback's own `modifiers`,
  not the replaced node's; give the fallback the ones it needs.
- **Accessibility.** `accessibilityLabel` becomes the node's accessible name and `accessibilityHint` its
  description, the latter with weaker support at the Safari 9 floor. A labelled node that claims a press
  gets the button role, other labelled nodes without a native role the group role; a text field keeps its
  own.
- A reader that does not know `ui.modifier` draws the node's `fallback`, negotiated in turn. Without one
  it draws none of the wrapped content (Macro Deck's own renderer shows a faint placeholder box in its
  place), per [The UI model](https://docs.macro-deck.app/ui/concepts/ui-model/#a-node). Give a wrapper a fallback built from the same content under
  its own keys:

```json
{
  "id": "card",
  "type": "ui.modifier",
  "properties": { "padding": { "basis": 0.08 }, "modifiers": { "radius": { "basis": 0.12 } } },
  "children": [{ "id": "icon", "type": "ui.image", "properties": { "source": { "resourceId": "icon" } }, "children": [] }],
  "fallback": { "id": "iconPlain", "type": "ui.image", "properties": { "source": { "resourceId": "icon" } }, "children": [] }
}
```

The shared fixture
[`conformance-modifier-tree.json`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/ui-model/fixtures/component-profile/conformance-modifier-tree.json)
covers every member, property and event on this page.

### See also

- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)
- [Theming](https://docs.macro-deck.app/ui/concepts/theming/)
- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [Compatibility](https://docs.macro-deck.app/ui/reference/compatibility/)

## Progress

> Source: https://docs.macro-deck.app/ui/components/progress/
>
> Draws a moving playback position as a bar or a time readout, advanced by the reader's own clock.

A playback timeline and its elapsed, remaining or total time. Both carry a progress reference - where the
medium was at one instant and how fast it is moving - so a playing track needs no patch until it changes.

`macrodeck.progress-bar`, `macrodeck.progress-text`

### Example

```csharp
var position = UiValue.Of(UiProgressReference.Advancing(42_000, DateTimeOffset.UtcNow, durationMs: 215_000));

new UiStack
{
    Key = "timeline",
    Children =
    [
        new UiProgressBar { Key = "progress", Value = position, Thickness = 0.02, MainSize = 0.02 },
        new UiStack
        {
            Key = "times",
            Direction = UiComponentDirections.Horizontal,
            Justify = UiComponentJustify.SpaceBetween,
            Children =
            [
                new UiProgressText { Key = "elapsed", Value = position, Format = UiProgressFormats.Elapsed, Role = UiComponentTextRoles.Muted },
                new UiProgressText { Key = "duration", Value = position, Format = UiProgressFormats.Duration, Role = UiComponentTextRoles.Muted, Align = UiComponentAlignments.End },
            ],
        },
    ],
}
```

*[Image: A thin blue progress bar a fifth of the way along, with 0:42 under its start and 3:35 under its end]*

A track 42 seconds into 3:35, with `0:42` and `3:35` beneath it, both advancing on the reader's clock -
the built-in Music Player widget's timeline.

### Paused vs playing

```csharp
UiProgressReference.Advancing(positionMs, now, durationMs)   // rate absent - normal speed
UiProgressReference.Halted(positionMs, now, durationMs)      // "rate": 0
```

Paused is a value, not something a reader infers. Send a new reference when playback starts, stops,
seeks or changes track; while it plays on schedule, keep the previous one - the built-in player re-anchors
only when the reported position drifts from the predicted one.

### Elapsed and remaining

| Format (`UiProgressFormats`) | 42 s of 215 s | 3,725 s of 7,200 s | No duration |
|---|---|---|---|
| `elapsed` (`Elapsed`) | `0:42` | `1:02:05` | The position |
| `remaining` (`Remaining`) | `2:53` | `57:55` | Empty |
| `duration` (`Duration`) | `3:35` | `2:00:00` | Empty |

Hours appear only when the value shown reaches one, and every segment below the leading one is padded to
two digits. A caption bound to `remaining` or `duration` disappears for a live stream rather than counting
down from nothing.

### A live stream

```csharp
UiProgressReference.Advancing(positionMs, now)   // no durationMs
```

With no duration the bar draws an empty track and only `elapsed` has anything to show.

### Fallbacks

```csharp
Fallback = new UiRangeBar { Key = "progressFallback", Start = 0, End = 42_000d / 215_000 },
```

Give both a fallback holding the value at the anchor - a `UiRangeBar` for the bar, a `UiTextRun` for the
text - so an older reader shows the right picture at the wrong second rather than nothing.

### Properties

#### `macrodeck.progress-bar`

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Value` (`value`) | A progress reference | An empty track | The position to draw. |
| `StartColor` (`startColor`) | `#rrggbb` | The reader's accent colour | The colour at the start of the filled span. |
| `EndColor` (`endColor`) | `#rrggbb` | The reader's accent colour | The colour at the head of the filled span. |
| `Thickness` (`thickness`) | A length | Left to the reader | The track's cross-axis thickness. |

#### `macrodeck.progress-text`

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Value` (`value`) | A progress reference | Nothing is drawn | The position to draw. |
| `Format` (`format`) | `elapsed`, `remaining`, `duration` | - | Which derivation to draw; an unknown value draws nothing. |
| `Size` (`size`) | A length | Left to the reader | The font size. |
| `MinSize` (`minSize`) | A length | Never shrinks; ellipsizes instead | The floor `size` may shrink to so the run fits. |
| `Weight` (`weight`) | A font weight | `regular` | The font weight. |
| `Role` (`role`) | A text role | `primary` | The semantic colour. |
| `Align` (`align`) | A `UiComponentAlignments` value | `start` | Alignment within the run's own box. |

### Events

None. Both are read-only - to let the user drag the position, use a [Slider](https://docs.macro-deck.app/ui/components/slider/).

### Children

None - both are leaves.

### Layout

`macrodeck.progress-bar` lays out like `ui.range-bar`: the track spans the element's full main-axis
extent and is `thickness` tall on the cross axis. `macrodeck.progress-text` sizes like `ui.text`: its box
is its font size, with a line height of one. Both follow the ordinary leaf rule on their parent stack's
main axis - `mainSize` or `fill` if declared, otherwise content extent. Full model:
[Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

These are `macrodeck.*` types because a reader cannot draw them from the tree alone - it must resolve
`$progress` against its own clock. The governing contract is
[ADR 0065](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0065-the-component-profile-authoring-contracts.md).

- `{"$progress":{"positionMs":42000,"durationMs":215000,"anchor":"2026-08-25T12:00:00.000Z"}}` resolves to
  `clamp(positionMs + (t - anchor) * rate, 0, durationMs)`, where `t` is now on the reader's
  host-synchronised clock. With no `durationMs` the upper clamp is dropped.
- `rate` absent means `1`; `0` means halted.
- A negative `positionMs` is clamped to zero, not rejected.
- `positionMs`, `durationMs` and `rate` must be numbers and `anchor` an ISO-8601 instant; a `$progress`
  member with any other member, or a missing `positionMs` or `anchor`, is rejected.
- A reader re-evaluates at least once a second. Sub-second interpolation is allowed but not required.
- The bar's geometry is `ui.range-bar`'s exactly, with the span starting at the track's start and no
  marker. Its end is `position(t) / durationMs` clamped to `0..1`, and `0` with no `durationMs`.
- Every format is a duration, not a clock time: no zone, no day period, no hour cycle.
- `remaining` and `duration` are empty with no `durationMs`.
- Digits are drawn with equal advance width, so the run does not shift as it counts.
- A reader draws nothing for a `format` it does not know.

### See also

- [Range bar](https://docs.macro-deck.app/ui/components/range-bar/) - the shared bar geometry
- [Time and clock](https://docs.macro-deck.app/ui/components/time/) - the same idea for the current time
- [Slider](https://docs.macro-deck.app/ui/components/slider/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## Range bar

> Source: https://docs.macro-deck.app/ui/components/range-bar/
>
> A read-only horizontal track with one gradient-filled span and an optional point marker.

A read-only track carrying one gradient-filled span, with an optional marker for a point inside it -
a forecast's low-to-high span, a level meter, a position on a fixed scale.

`ui.range-bar`

### Example

```csharp
new UiRangeBar
{
    Key = "bar",
    Fill = true,
    Thickness = UiSize.FromBasis(0.03, 0.35),
    Start = 0.2,
    End = 0.6,
    StartColor = "#2b6cee",
    EndColor = "#ee2b2b",
    Marker = UiValue.From(() => state.Value.TodayFraction),
}
```

*[Image: A thin span fading from blue to red between 20 and 60 percent of the track, with a white marker dot on it]*

A forecast row: a blue-to-red span from 20 % to 60 % of the track, with today's temperature marked on it.

### Point marker

```csharp
Marker = isToday ? UiValue.From(() => state.Value.TodayFraction) : UiValue.None<double>(),
```

*[Image: A three-day forecast with a low, a blue-to-red range bar and a high per row; only the Today row carries a marker]*

Leave `Marker` absent and no marker is drawn. The marker is painted in the reader's text colour, not the
gradient, so it stays visible wherever it lands.

### Colours

`StartColor` and `EndColor` are literal colours, not theme roles: they encode data, so a value must look the
same in every theme - see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/). Use the same colour twice for a solid
span.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Start` (`start`) | `0..1` | - | Where the filled span begins, as a fraction of the track. |
| `End` (`end`) | `0..1` | - | Where the filled span ends, as a fraction of the track. |
| `StartColor` (`startColor`) | `#rrggbb` | - | The colour at `start`. |
| `EndColor` (`endColor`) | `#rrggbb` | - | The colour at `end`. |
| `Marker` (`marker`) | `0..1` | No marker is drawn | Where the point marker sits, as a fraction of the track. |
| `Thickness` (`thickness`) | length | Left to the reader | The track's thickness on the cross axis. |

### Events

None. `ui.range-bar` is never interactive - use [`ui.slider`](https://docs.macro-deck.app/ui/components/slider/) for the same shape
the user can drag.

### Children

None. `ui.range-bar` is a leaf.

### Layout

The track spans the element's full main-axis extent and is `thickness` tall on the cross axis. The element
follows the ordinary leaf rule on its parent's main axis - `MainSize` or `Fill` if declared, otherwise its
content extent. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

The geometry is normative; the fixtures in `ui-model/fixtures/component-profile/` resolve it at two sizes.

- The track is centred on the cross axis with fully rounded ends; the unfilled track uses the reader's
  tertiary surface colour.
- The filled span runs from `start` to `end` with a linear gradient from `startColor` to `endColor` along
  the main axis, and keeps fully rounded ends even when it stops short of the track's ends.
- The marker is a filled disc of radius `0.75 * thickness` in the reader's primary text colour, ringed by a
  stroke of width `0.28 * thickness` in the widget's own background colour.
- The marker's centre is inset from both ends by `radius + strokeWidth / 2`; when the track is narrower
  than twice that inset, the marker is centred instead.

### See also

- [Slider](https://docs.macro-deck.app/ui/components/slider/)
- [Progress](https://docs.macro-deck.app/ui/components/progress/)
- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)

## Responsive

> Source: https://docs.macro-deck.app/ui/components/responsive/
>
> Different layouts for different box sizes - a widget at 1x1, 2x1 or 1x2, a folder view on a phone or a tablet - chosen by the reader without a round-trip.

`UiResponsive` holds several layouts for one place in the tree. The reader draws the first one whose
condition holds for the box the node is given, and chooses again whenever that box changes. Your view never
learns the size and never rebuilds when it changes.

`ui.responsive` (component version 1)

### Example

```csharp
new UiResponsive
{
    Key = "weather",
    Default = new UiStack
    {
        Key = "compact",
        Justify = UiComponentJustify.Center,
        Children = [new UiTextRun { Key = "temp", Text = "21°", Size = 0.3 }],
    },
    Variants =
    [
        new UiResponsiveVariant
        {
            MinWidth = 1.5,
            Content = new UiStack
            {
                Key = "wide",
                Direction = UiComponentDirections.Horizontal,
                Children = [icon, details],
            },
        },
        new UiResponsiveVariant
        {
            MaxAspect = 0.67,
            Content = new UiStack { Key = "tall", Children = [icon, temperature, forecast] },
        },
    ],
}
```

*[Image: The weather widget on one cell: only the temperature, large and centred]*
*[Image: The same widget two cells wide: the icon beside the temperature and the condition]*
*[Image: The same widget two cells tall: the icon above the temperature and a short forecast]*

One tree, three layouts: the default on one cell, the wide one on 2x1 and the tall one on 1x2. Resizing the
widget on the deck switches between them immediately.

### Conditions

| Member | Holds when |
|---|---|
| `MinWidth` | the box is at least this many cells wide |
| `MaxWidth` | the box is less than this many cells wide |
| `MinHeight` | the box is at least this many cells tall |
| `MaxHeight` | the box is less than this many cells tall |
| `MinAspect` | width over height is at least this |
| `MaxAspect` | width over height is less than this |

- A variant holds when every member you set holds. A variant with none set always holds, so put it last.
- Variants are tried in order and the first that holds wins. `Default` is drawn when none does.
- A minimum includes its value and a maximum excludes it, so `MaxWidth = 2` and `MinWidth = 2` split the
  range with nothing drawn twice. Both are compared with a tolerance of `0.0001`
  (`UiResponsiveSelection.Tolerance`), so a tile that is exactly two cells wide counts as two cells even when
  the reader's scaled pixels round.
- A member that needs a side the reader does not know never holds. `MinAspect` needs both sides.

#### What a cell is

On a deck tile, one cell is one grid cell: a 2x1 tile is two cells wide plus the spacing between them, so
it is slightly more than `2`. Spans are exact, so `MinWidth = 2` means "two columns or more" whatever the
folder's spacing.

Anywhere else - a [folder view](https://docs.macro-deck.app/ui/views/folder-views/), a [modal](https://docs.macro-deck.app/ui/views/modal/), a
[screensaver](https://docs.macro-deck.app/ui/views/screensavers/) - a cell is 120 of the reader's own layout units, which are CSS pixels
in Macro Deck's clients. `MinWidth = 6` there means "at least 720 px wide". A measured CSS width can land a
fraction of a pixel either side of a round number, so leave some room around a threshold rather than
putting it exactly on a width you expect.

Aspect conditions mean the same everywhere and are usually the better choice for "landscape" and
"portrait".

### The box it chooses by

The node chooses by its own box, not by the tile's or the window's. As the root of a widget it gets the whole
tile. Inside a stack it gets the slot the stack gives it, so give it `Fill` or `MainSize` like any other
child. The chosen layout is always drawn across the whole box.

`MainSize`, `Fill`, `ColumnSpan` and `RowSpan` go on the `UiResponsive`. A layout that sets them is rejected
when the view is built, and so is a layout that is a `UiWhen`, a `UiRepeat` or a fragment. Put those inside
a layout instead.

### What every layout costs

Every layout is built, kept current and sent to the reader, whichever one is on screen. They all count
toward the tree limits: 2000 nodes, 192 KiB per tree and 64 KiB per patch. Each `UiResponsive` also adds a
level toward the 32-level nesting limit.

Keep the layouts small, and share what they have in common through a helper method rather than a large
subtree repeated in every variant.

Per-client state that lives in the reader, such as a text field's unsent text or a list's scroll position,
is lost when the reader switches to another layout. State in your view is not.

### Older readers

A reader that does not know `ui.responsive` draws the node's `Fallback`. When you set none, `Default` is sent
a second time as the fallback, under ids below `<id>._fallback`, so an older reader draws your default layout.
That copy has consequences:

- It is patched along with the default, so a change inside `Default` is sent twice.
- A `UiResponsive` nested inside another's `Default` is copied again for each level.
- The key `_fallback` is reserved: a layout keyed `_fallback` is rejected.
- The copy's ids are longer. One that would pass the 128-character id limit is rejected with a message that
  names the node.
- A [configuration input](https://docs.macro-deck.app/ui/views/configuration/) cannot sit inside `Default`, because its id would appear
  twice.

In each of these cases, set an explicit `Fallback` and no copy is made.

An older reader also walks every layout when it decides whether the tile's own press belongs to a control in
the tree. Put the controls a tile must never lose in `Default`.

### Presses and hardware keys

A pointer press on a drawn control always reaches that control.

For the tile's own press, a keyboard activation or a hardware key on a device, the reader looks for a control
in the layout it draws. That is exact for a `UiResponsive` at the root of the widget, or reached from the root
only through a `UiLayer`, a `UiTransform` or a `UiModifier` without padding or frame. For one nested deeper, the tile counts
its default layout. A drag or swipe on a control inside a nested layout can therefore also start the tile's
own press.

When the layout at the root is itself a button, it is treated as the whole tile, exactly as a bare button
root would be.

### Testing

`UiTestHost.SetBox(widthCells, heightCells)` picks the layout `ByType`, `SingleByType` and `ByText` see. See
[Custom views](https://docs.macro-deck.app/ui/views/custom/#testing-it).

```csharp
var host = UiTestHost.Render(weather, widgetSurface);
host.SetBox(2.1, 1);
Assert.That(host.ByText("Sunny"), Is.Not.Empty);
```

`UiResponsiveSelection.SelectChild` is the rule itself, over the wire form, for a reader of your own.

### Reference

| Property (`UiResponsive`) | Wire | Meaning |
|---|---|---|
| `Default` | `children[0]` | Drawn when no variant holds, and by an older reader |
| `Variants` | `children[1..]` and `variants` | The conditional layouts in order; `variants[i]` is the condition for `children[i + 1]` |
| `MainSize`, `Fill`, `ColumnSpan`, `RowSpan` | as on any node | The node's slot in its parent |
| `Fallback` | `fallback` | Your own fallback; when absent, a copy of `Default` |

Reader rules:

- Draw the first `children[i + 1]` whose `variants[i]` holds for the node's own box, else `children[0]`.
  Draw only that child, across the whole box.
- Widths and heights are in cells of 120 reference units. A side that is zero, negative or unknown is unknown.
- A condition that is not an object never holds. A member that is not a number is ignored.
- Choose again whenever the box changes.
- A tree root that is a `ui.responsive` hands its root status to the child it draws.

### See also

- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/) - lengths that scale within one layout
- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [Deck widget views](https://docs.macro-deck.app/ui/views/widget/)
- [ADR 0094](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0094-responsive-layouts-are-chosen-by-the-reader.md)

## Segmented

> Source: https://docs.macro-deck.app/ui/components/segmented/
>
> A row of segments the user chooses one of, reporting the chosen index.

A row of equal segments with one selected - a mode switch, a scene picker. Each child is one segment's
content; the control, not the children, receives the press.

`ui.segmented`

### Example

```csharp
new UiSegmented
{
    Key = "mode",
    Selected = UiValue.From(() => (int)state.Value.Mode),
    Events = [UiEventHandler.On(UiComponentEvents.Change, data => SetMode(data))],
    Children =
    [
        new UiIcon { Key = "sun", Icon = UiIcons.Sun, Size = 0.14 },
        new UiIcon { Key = "moon", Icon = UiIcons.Moon, Size = 0.14 },
        new UiTextRun { Key = "auto", Text = "Auto", Size = 0.1 },
    ],
    Fallback = new UiStack { Key = "modeFallback", Direction = UiComponentDirections.Horizontal, Children = modeButtons },
}
```

*[Image: A wide capsule split into three segments - a sun, a moon and the word Auto - with a blue face behind the sun]*

### Reading the index

```csharp
UiEventOutcome SetMode(UiEventData data)
{
    if (!data.TryGetDouble(out var index))
    {
        return UiEventOutcome.Rejected("The event payload is not a number.");
    }

    state.Set(state.Value with { Mode = (Mode)(int)index });
    return UiEventOutcome.Accepted;
}
```

`change` carries the zero-based index of the segment the user chose, as a JSON number. Set `Selected` from
it.

### Holding the selection

A completed press on a segment other than the drawn selection moves the face there at once and sends
`change`. The reader holds that selection until your `Selected` changes or one second passes, as a
[toggle](https://docs.macro-deck.app/ui/components/toggle/) holds its state. A press on the segment already selected sends nothing.

### Children are content

The children are drawn, never pressed. A button or slider inside a segment is painted but offers none of its
events, and the deck never treats one as the tile's control.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Selected` (`selected`) | `int`, zero-based | No face drawn | The selected segment. Out of range also draws no face. |
| `LevelColor` (`levelColor`) | `#rrggbb` | The reader's own accent colour | The selected face's colour. |
| `MainSize` (`mainSize`), `Fill` (`fill`), `Answer` (`answer`) | - | - | Shared with every container - see [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/). |

### Events

| Event | Fires when | Payload |
|---|---|---|
| `change` (`UiComponentEvents.Change`) | A press completed on a segment other than the selected one | The segment's zero-based index, a JSON number |

### Children

Any element, any number; one segment per child. Their own events are never offered.

### Layout

The width is divided into one equal segment per child, in a row, and each child is laid out over its
segment's box. The element's whole box is the press surface. On its parent's main axis a segmented control
has no content extent: give it `MainSize` or `Fill`. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- **Geometry:** a capsule track over the whole box in the tertiary surface colour; the selected segment's
  face is a capsule inset by `0.08` of the box height, in `levelColor` or the accent colour.
- **Interaction only where declared.** Without `change` the control is drawn and cannot be touched.
- **The pointer picks the segment** from its position; children never receive it, and their declared events
  are never sent.
- **Press feedback:** with `change` declared, the reader paints its press tint on touch. The deck tile's own
  pressed state follows the control only when it is the root of the tree, as for a button.
- **A completed press** on a segment other than the drawn selection selects it, sends `change` once with its
  index, and holds it until `selected` changes or 1000 ms pass. A cancelled press sends nothing.
- **Keyboard and hardware:** in the Macro Deck desktop app, activating a tile whose first interactive node
  is a segmented control selects the next segment, wrapping to the first after the last; with nothing
  selected it selects the first. The web client does not activate tree nodes from the keyboard.
- **Activation acts on the producer's value:** it steps from the `selected` the tree last carried, not a
  selection the reader is still holding after a tap, and the face moves when the producer answers.
- A reader that does not know `ui.segmented` draws the node's `fallback`, typically a `ui.stack` of
  `ui.button`:

```json
{
  "type": "ui.segmented",
  "properties": { "selected": 0, "events": ["change"] },
  "children": [
    { "type": "ui.text", "properties": { "text": "Day" } },
    { "type": "ui.text", "properties": { "text": "Night" } }
  ],
  "fallback": {
    "type": "ui.stack",
    "properties": { "direction": "horizontal" },
    "children": [
      { "type": "ui.button", "properties": { "events": ["press"], "fill": true }, "children": [{ "type": "ui.text", "properties": { "text": "Day" } }] },
      { "type": "ui.button", "properties": { "events": ["press"], "fill": true }, "children": [{ "type": "ui.text", "properties": { "text": "Night" } }] }
    ]
  }
}
```

### See also

- [Toggle](https://docs.macro-deck.app/ui/components/toggle/)
- [Button](https://docs.macro-deck.app/ui/components/button/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)

## Shape

> Source: https://docs.macro-deck.app/ui/components/shape/
>
> A filled and stroked rectangle, rounded rectangle, circle, capsule or path, drawn from the tree alone.

A filled and stroked outline - a status dot, a badge behind a number, a divider, a simple glyph of your own -
drawn without registering any artwork.

`ui.shape`

### Example

```csharp
new UiShape
{
    Key = "status",
    Shape = UiComponentShapes.Circle,
    Color = UiValue.From(() => state.Value.Online ? "#34c759" : "#ff3b30"),
    StrokeColor = "#ffffff",
    StrokeWidth = 0.02,
    MainSize = 0.3,
}
```

*[Image: A green filled circle with a thin white outline, centred in a tile]*

A status dot: switching its colour is a `set-properties` patch carrying `color` alone.

### Rounded rectangles and capsules

```csharp
new UiShape { Key = "badge", Shape = UiComponentShapes.RoundedRectangle, CornerRadius = 0.06, Color = "#2b6cee" }
new UiShape { Key = "pill", Shape = UiComponentShapes.Capsule, Color = "#2b6cee" }
```

`CornerRadius` is clamped to half the box's smaller side, so a very large radius on a rounded rectangle
gives a capsule. A capsule always takes that half side and ignores `CornerRadius`.

### Paths

```csharp
new UiShape
{
    Key = "play",
    Shape = UiComponentShapes.Path,
    Path = "M0.3 0.2 L0.8 0.5 L0.3 0.8 Z",
    Color = "#ffffff",
}
```

*[Image: A white triangle pointing right drawn from a path, next to an outlined heart-like path]*

The coordinates are in a unit box: `0..1` spans the element's own width and height, so the path stretches
with the box while the stroke keeps its width. Only the absolute commands `M L H V C Q A Z` are accepted,
with SVG 1.1's number syntax and implicit repetition. A path with anything else, including relative
(lower-case) commands, draws nothing.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Shape` (`shape`) | `UiComponentShapes.Rectangle`, `.RoundedRectangle`, `.Circle`, `.Capsule`, `.Path` (`rectangle`, `rounded-rectangle`, `circle`, `capsule`, `path`) | `rectangle` | The outline. |
| `CornerRadius` (`cornerRadius`) | length | Square corners | The corner radius of a `rounded-rectangle`. |
| `Color` (`color`) | `#rrggbb` | No fill | The fill. |
| `StrokeColor` (`strokeColor`) | `#rrggbb` | No stroke | The outline colour. |
| `StrokeWidth` (`strokeWidth`) | length | No stroke | The outline width. |
| `Path` (`path`) | restricted SVG path data | Draws nothing for `path` | The outline of a `path` shape, in the unit box. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | - | - | Shared with every leaf - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |

The colours are literal colours, not theme roles - see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Events

None. `ui.shape` is never interactive; put it inside a [button](https://docs.macro-deck.app/ui/components/button/) to press it.

### Children

None. `ui.shape` is a leaf.

### Layout

A shape has no content extent: on its parent's main axis it takes `MainSize` or `Fill`, and without either
it is `0` long. On the cross axis it follows the parent's alignment. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

The geometry is normative; see the [`UiShape`](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/ui-model/src/MacroDeck.Ui/Components/UiElements.cs)
remarks.

- `rectangle` fills the box; `rounded-rectangle` fills it with corners of `cornerRadius` clamped to half the
  smaller side; `circle` is inscribed in the smaller side and centred; `capsule` fills the box with corners of
  half the smaller side.
- An absent `color` paints no fill; an absent `strokeColor` or `strokeWidth` paints no stroke. The stroke is
  centred on the outline and never scaled with a path's box.
- A `path` is validated before it is drawn. Anything outside the absolute commands `M L H V C Q A Z`, SVG
  numbers, whitespace and commas, or data not starting with `M`, draws nothing.
- Reject a command whose arguments are not a whole multiple of its arity (two for `M L`, one for `H V`, six
  for `C`, four for `Q`, seven for `A`, none for `Z`); such path data draws nothing.
- A `shape` value the reader does not know draws nothing. A new value raises this type's component version,
  so a producer using one sets `RequiredComponentVersion` and a fallback.
- A reader that does not know `ui.shape` draws the node's `fallback`. Leave it out when the shape is
  decoration; where it carries meaning, a `ui.stack` with the same `background` is the closest match:

```json
{
  "type": "ui.shape",
  "properties": { "shape": "rounded-rectangle", "cornerRadius": { "basis": 0.06 }, "color": "#2b6cee" },
  "fallback": { "type": "ui.stack", "properties": { "background": "#2b6cee" } }
}
```

### See also

- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/) - `background`
- [Icon](https://docs.macro-deck.app/ui/components/icon/)
- [Image](https://docs.macro-deck.app/ui/components/image/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## Slider

> Source: https://docs.macro-deck.app/ui/components/slider/
>
> A draggable level on a rounded track, the interactive counterpart of the range bar.

A draggable level: a rounded track carrying a filled span. It holds a fraction of the track in `0..1`,
not a value in your own units.

`ui.slider`

### Example

```csharp
new UiSlider
{
    Key = "volume",
    Fill = true,
    Level = UiValue.From(() => state.Value.Volume / 100.0),
    Step = 0.05,
    Thickness = UiSize.FromBasis(0.12, 0.55),
    Events =
    [
        UiEventHandler.On(UiComponentEvents.Adjust, data => Preview(data)),
        UiEventHandler.On(UiComponentEvents.Change, data => Apply(data)),
    ],
}
```

*[Image: A wide tile with a horizontal slider filled in blue to 65 percent and a white thumb at the level]*

A horizontal volume track snapping to 5 % steps: `adjust` moves the display while dragging, `change`
commits the level the user landed on.

### Reading the level

```csharp
UiEventOutcome Apply(UiEventData data)
{
    if (!data.TryGetDouble(out var level))
    {
        return UiEventOutcome.Rejected("The event payload is not a number.");
    }

    state.Set(state.Value with { Volume = level * 100 });
    return UiEventOutcome.Accepted;
}
```

Both events carry the level as a bare number. Convert it to your own units yourself; a number beside the
slider is an ordinary `ui.text` you update.

### Adjust or change

Act on `change` alone for anything costly, such as a seek, and let `adjust` just move the level. Acting on
every `adjust` would drag the target through every waypoint; ignoring both would leave a control that does
not move.

### Vertical slider

```csharp
Direction = UiComponentDirections.Vertical,
```

*[Image: A tall tile with a vertical slider filled in blue from the bottom to 40 percent, the thumb at the top of the fill]*

`Direction` is the axis the level travels along, not the element's axis in its parent. Vertical runs
bottom to top - up is more.

### Relative drag

```csharp
Interaction = UiComponentSliderInteractions.Relative,
```

By default a press jumps the level to the pointer. With `Interaction` set to `relative`, a press leaves the
level where it is, and the level then moves by how far the pointer travels: a travel of the whole box
length spans the whole `0..1` range, in either direction, clamped at both ends. Use it where users nudge a
value, such as a volume, and a jump to the touch point would throw it far off. A tap moves nothing and
sends neither `adjust` nor `change`.

A reader that predates `interaction` ignores it and keeps the absolute behaviour, so the slider still
works, only without the grab.

### Colour and fallback

```csharp
LevelColor = "#2b6cee",
Fallback = new UiRangeBar { Key = "trackFallback", Start = 0, End = level, StartColor = "#2b6cee", EndColor = "#2b6cee" },
```

A reader without `ui.slider` draws the fallback, here the same level as a read-only range bar.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `Level` (`level`) | `0..1` | `0` | The filled fraction of the track. |
| `Step` (`step`) | fraction of the track | Continuous | The granularity the level snaps to. |
| `LevelColor` (`levelColor`) | `#rrggbb` | The reader's own accent colour | The filled span's colour. |
| `Direction` (`direction`) | `horizontal`, `vertical` | `horizontal` - unlike `ui.stack` | The axis the level travels along. |
| `Interaction` (`interaction`) | `relative` | Absolute: the level jumps to the pointer | How a pointer maps to the level - see [Relative drag](#relative-drag). An unknown value reads as absent. |
| `Thickness` (`thickness`) | length | Left to the reader | The drawn track's thickness on the cross axis. |

`LevelColor` is a literal colour, not a theme role - see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Events

| Event | Fires when | Payload |
|---|---|---|
| `adjust` (`UiComponentEvents.Adjust`) | An intermediate level while the user is still working the control | The level, a bare number |
| `change` (`UiComponentEvents.Change`) | The interaction ended, sent once - not for a relative tap, see [Reader behaviour](#reader-behaviour) | The level, a bare number |
| `double-press` (`UiComponentEvents.DoublePress`) | A second tap completed shortly after the first, neither one a drag | None |

Declare `double-press` for an action on a double tap, such as resetting to a home level. Each tap is still an
ordinary interaction and sends its own `change` first, so the handler sees the level the second tap set and
replaces it. A reader that predates `double-press` never sends it, and the taps stay plain level changes. On a
relative slider a tap moves nothing, so `double-press` arrives on its own. Unlike on a [button](https://docs.macro-deck.app/ui/components/button/#reader-behaviour),
nothing is held back while waiting for a second tap.

### Children

None. `ui.slider` is a leaf.

### Layout

The element's whole box is the interactive surface; the drawn track is smaller. `Thickness` sizes only the
drawn track, not the element. On its parent's main axis the slider follows the ordinary rule - `MainSize`
or `Fill` if declared, otherwise its content extent. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- **Interaction only where declared.** A node with no events carries no `events` property and is drawn as
  a level the user cannot touch; there is no disabled property.
- **The whole box takes input.** A pointer anywhere in it sets the level to its position projected onto
  `direction`, clamped to `0..1`; the cross-axis position is ignored. A pointer that leaves the box
  mid-drag keeps control until release.
- **Snapping:** with `step` present, the level becomes `round(level / step) * step`, clamped to `0..1`,
  before it is painted or sent. A tie rounds up.
- **Paint locally first:** the reader paints the level it computed straight away and reconciles with the
  producer afterwards.
- **Rate and order:** `adjust` at most ten times a second, never after the `change` that ended the
  interaction. Only declared names are sent.
- **Double tap:** with `double-press` declared, a tap released within 400 ms of the previous one and starting
  within 24 px of it, neither moving more than a few pixels, sends `double-press` right after its `change`.
  A drag or a cancelled gesture in between starts over.
- **Relative drag** (`interaction: relative`), overriding the input, rate-and-order and double-tap rules
  above where they differ: a press paints and sends nothing. Within the few pixels of tap slop the level does
  not move; past it, the level is the one at the press plus the pointer's travel along `direction` since the
  press, divided by the box's measured length on that axis (up is more when vertical), clamped to `0..1` after
  every move so reversing at an end moves back at once. `step` snaps as usual, and the level counts as moved
  only once that snapped level differs from the snapped level at the press. An interaction whose level never
  moved sends neither `adjust` nor `change`; one that moved sends `change` even if it ended where it began.
- **Geometry is normative:** the track and thumb are implemented exactly; the fixtures in
  `ui-model/fixtures/component-profile/` resolve both at two sizes.

### See also

- [Range bar](https://docs.macro-deck.app/ui/components/range-bar/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)

## Stack and layer

> Source: https://docs.macro-deck.app/ui/components/stack-and-layer/
>
> A stack lays children beside each other along one axis; a layer draws them on top of each other.

A stack lays its children out along one axis. A layer draws every child across the whole box, the first one
furthest back.

`ui.stack` / `ui.layer`

### Example

```csharp
new UiStack
{
    Key = "row",
    Direction = UiComponentDirections.Horizontal,
    Align = UiComponentAlignments.Center,
    Gap = UiSize.FromBasis(0.025),
    Padding = UiSize.FromBasis(0.02),
    Children =
    [
        new UiImage { Key = "art", Source = cover, Size = UiSize.FromBasis(0.09) },
        new UiStack
        {
            Key = "labels",
            Fill = true,
            Justify = UiComponentJustify.Center,
            Gap = UiSize.FromBasis(0.004),
            Children =
            [
                new UiTextRun { Key = "title", Text = item.Title, Size = UiSize.FromBasis(0.038), Weight = UiComponentTextWeights.Medium },
                new UiTextRun { Key = "subtitle", Text = item.Subtitle, Size = UiSize.FromBasis(0.032), Role = UiComponentTextRoles.Secondary },
            ],
        },
    ],
}
```

*[Image: A row with a square cover on the left and a white title above a grey subtitle filling the rest]*

A track row from the built-in music picker: cover art on the left, two lines of text filling the rest.

### A row with one filling child

```csharp
new UiStack
{
    Key = "header",
    Direction = UiComponentDirections.Horizontal,
    Children =
    [
        new UiTextRun { Key = "name", Text = "Office", Size = 0.12, Fill = true },
        new UiTextRun { Key = "temp", Text = "21°", Size = 0.12, MainSize = 0.3, Align = UiComponentAlignments.End },
    ],
}
```

```
+--------------------------+--------+
| Office                   |    21° |
+--------------------------+--------+
```

*[Image: A wide tile with Office at the leading edge and 21° at the trailing edge]*

`Fill` takes whatever the siblings leave. A text next to a filling sibling needs its own `MainSize`, because
a reader cannot measure text without a font - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Spreading children apart

```csharp
new UiStack
{
    Key = "current",
    Direction = UiComponentDirections.Horizontal,
    Justify = UiComponentJustify.SpaceBetween,
    Align = UiComponentAlignments.Center,
    Children = [icon, temperature],
}
```

```
+-----------------------------------+
| [icon]                        21° |
+-----------------------------------+
```

*[Image: A wide tile with a sun icon at the leading edge and a bold 21° at the trailing edge]*

`SpaceBetween` puts all free space between children and none at the edges.

### Lining up a value and its unit

```csharp
new UiStack
{
    Key = "reading",
    Direction = UiComponentDirections.Horizontal,
    Align = UiComponentAlignments.Baseline,
    Children =
    [
        new UiTextRun { Key = "value", Text = "73", Size = 0.3 },
        new UiTextRun { Key = "unit", Text = "km/h", Size = 0.1 },
    ],
}
```

*[Image: A large 73 with a small km/h beside it, both sitting on the same baseline]*

`Baseline` puts the runs' text on one line instead of aligning their boxes. Only children that draw text
take part; anything else in the row aligns to the trailing edge.

### Spacing without margins

```csharp
new UiStack
{
    Key = "card",
    Padding = UiSize.FromBasis(0.06),
    Gap = UiSize.FromBasis(0.03),
    Children = [title, new UiStack { Key = "inset", Padding = 0.04, Children = [body] }],
}
```

No element has a margin property. Space around one child comes from wrapping it in its own stack with
`Padding`.

### Keeping the newest children at the end

```csharp
new UiStack
{
    Key = "feed",
    Fill = true,
    Overflow = UiComponentOverflows.ClipStart,
    Padding = UiSize.FromBasis(0.2 * textSize),
    RequiredComponentVersion = 2,
    Fallback = new UiStack { Key = "feedFallback", Fill = true, Children = [newestMessage] },
    Children = messages,
}
```

A stack shrinks its children when they need more room than it has. With `ClipStart` it keeps every child
at its natural size instead, puts the content against its end edge and cuts off what does not fit at the
start: a vertical feed shows its last children at the bottom and loses the first ones at the top. `fill`
on a child is ignored, and `ClipStart` overrides `Justify`. The stack still reports the sum of its children
as its own size, so give it its box from its parent with `Fill` or `MainSize`. A padding of 0.2 of the text
size keeps the descenders of the last line inside the clip.

`ClipStart` needs component version 2. A version 1 reader ignores `overflow` and shrinks every child into
the box, so ask for version 2 and carry a fallback that reads well shrunk, such as the newest few messages.

### Drawing one element behind another

```csharp
new UiLayer
{
    Key = "historyGraph",
    Children =
    [
        new UiChart { Key = "chart", Points = points, PlotTop = 0.66 },
        new UiStack { Key = "labels", Padding = safeArea, Children = [title, subtitle] },
        value,
    ],
    Fallback = value,
}
```

```
+----------------------+
| CPU             <- labels
|        42 %     <- value
|  /\_/\__/\      <- chart (furthest back)
+----------------------+
```

*[Image: A history graph tile: a filled line chart along the bottom, CPU and Package labels at the top left, and 42 % drawn over the middle]*

The built-in history graph: a chart edge to edge, labels inset over it. Each layer child that needs
padding, gap, justify or align wraps itself in a `ui.stack`, which also lets two layers inset differently.
`Fallback` gives an older reader the value alone.

### Properties

#### `ui.stack`

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Direction` (`direction`) | `UiComponentDirections.Vertical`, `.Horizontal` (`vertical`, `horizontal`) | `vertical` | The layout axis. |
| `Justify` (`justify`) | `UiComponentJustify.Start`, `.Center`, `.End`, `.SpaceBetween` (`start`, `center`, `end`, `space-between`) | `start` | How free space is distributed along the main axis. |
| `Align` (`align`) | `UiComponentAlignments.Start`, `.Center`, `.End`, `.Stretch`, `.Baseline` (`start`, `center`, `end`, `stretch`, `baseline`) | `stretch` | How children are aligned on the cross axis. |
| `Gap` (`gap`) | length | No gap | The gap between children. |
| `Padding` (`padding`) | length | No padding | Inner padding on every edge. |
| `Background` (`background`) | `#rrggbb` or `transparent` | Paints nothing behind its children | The stack's own fill, a literal colour rather than a theme role - see [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/). `transparent` paints nothing; on the widget's root it also removes the tile face behind the widget. |
| `Overflow` (`overflow`) | `UiComponentOverflows.Shrink`, `.ClipStart` (`shrink`, `clip-start`) | `shrink` | What happens to children that do not fit the main axis; `clip-start` needs component version 2. |

#### `ui.layer`

No properties of its own: no padding, gap, justify, align or background.

#### Shared with every container

| Property | Values | Default | Meaning |
|---|---|---|---|
| `MainSize` (`mainSize`) | length | Measured from content | The extent on the parent's main axis - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |
| `Fill` (`fill`) | `bool` | Does not fill | Takes the parent's leftover main-axis space - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |
| `Answer` (`answer`) | string | No answer | On a dialog surface, the value a press inside it settles the dialog with - see [Events](https://docs.macro-deck.app/ui/concepts/events/). |

### Events

None of their own. Either can still complete a dialog through `Answer` when a descendant's press claims
it: the affordance belongs to the declared event, not the node type, so a list row can be a stack (no
accent background) and still settle the dialog.

### Children

Both: any element, any number, in any combination.

### Layout

A stack divides its own main-axis extent among its children: each child's `mainSize` or `fill` competes
for that budget, and a child declaring neither is measured from what a renderer can work out without a font.
A text needs its own `mainSize` whenever a filling sibling sits next to it.

When the children ask for more than the stack has, they shrink to share the shortfall. With
`overflow: "clip-start"` they keep their natural size instead: `fill` is ignored, a `mainSize` still holds,
the content sits against the end edge whatever `justify` says, and what does not fit is clipped at the
start edge.

A layer gives every child the whole content box, in declaration order, first one furthest back.
`mainSize` and `fill` mean nothing on a layer's children, because there is no axis to divide.

See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/) for the full model.

### Reader behaviour

- A stack with no `direction` lays out vertically, no `justify` means `start`, no `align` means `stretch`.
- `baseline` applies to children that draw text; other children in the row align to the trailing edge.
- A stack with no `background` paints nothing behind its children; a layer never paints a background.
- A `background` of `transparent` paints nothing either. When the widget's root stack (after resolving a
  `ui.responsive` root to its drawn variant) carries it, draw the tile without its face fill and shadow, so
  the folder background shows through; keep the border ring. Reject any other value that is not `#rrggbb`.
  A modifier's `background` stays `#rrggbb` only.
- On a layer, ignore `mainSize` and `fill` on children; every child gets the whole box.
- `overflow` absent, `shrink` or a value you do not know: shrink the children as always. `clip-start`:
  give each child its natural main size (its `mainSize` if declared, `fill` ignored), align the content to
  the end edge regardless of `justify`, and clip at the stack's own box so the first children are the ones
  cut off. Advertise `ui.stack` version 2 only once you do this.
- `overflow` belongs to `ui.stack`; a `ui.button` does not take it.
- A reader that does not know `ui.layer` draws the node's `fallback` - it is a type, not a third
  `direction`, so negotiation catches it.

### See also

- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/)
- [Transform](https://docs.macro-deck.app/ui/components/transform/) - a layer that also rotates, scales and shifts
- [List](https://docs.macro-deck.app/ui/components/list/) - a scrolling container for dialogs

## Text field

> Source: https://docs.macro-deck.app/ui/components/text-field/
>
> A single line of text the user types, for dialogs.

One line of text the user types - the framework's only text entry. It is meant for
[dialogs](https://docs.macro-deck.app/ui/views/modal/): a deck tile has nowhere to type.

`ui.text-field`

### Example

```csharp
var query = new UiState<string>(string.Empty);

new UiTextField
{
    Key = "search",
    Text = UiValue.From(() => query.Value),
    Placeholder = Strings.SearchPlaceholder(),
    Size = 0.045,
    Events =
    [
        UiEventHandler.On(UiComponentEvents.Adjust, e =>
        {
            if (e.TryGetString(out var text))
            {
                query.Value = text;
            }
        }),
    ],
}
```

*[Image: An empty text field showing the grey placeholder "Search songs, albums, artists"]*

A search box that filters as the user types, adapted from the built-in Music player picker.

### Acting only on the final value

```csharp
Events = [UiEventHandler.On(UiComponentEvents.Change, RunSearch)],
```

Every keystroke arrives as `adjust`; the value the user settled on - they left the field or pressed
Enter - arrives as `change`. Filter on `adjust` when the query is cheap; act only on `change` when each
one costs a network call. The field shows everything typed in between either way.

### Read-only display

```csharp
new UiTextField { Key = "apiKey", Text = UiValue.From(() => state.Value.ApiKey) }
```

A field that declares no events is drawn with the producer's text and accepts no typing.

### Properties

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Text` (`text`) | `UiValue<string>`, literal only | Shows nothing | The value the field holds - what the user typed or the producer put there to edit. |
| `Placeholder` (`placeholder`) | `UiText`: literal or localized | Shows nothing while empty | What the field shows while it is empty. |
| `Size` (`size`) | `UiSize` length | Left to the reader | The font size. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/) | Content extent | The field's extent along the parent stack's main axis. |

`Text` is never localized; `Placeholder` is, like any prompt.

### Events

| Event | When | Payload |
|---|---|---|
| `adjust` (`UiComponentEvents.Adjust`) | Every keystroke, while the user is still typing | The field's current text |
| `change` (`UiComponentEvents.Change`) | The user left the field or pressed Enter | The field's current text |

Typing is offered only when events are declared. The pair is the same one [Slider](https://docs.macro-deck.app/ui/components/slider/)
uses. See [Events](https://docs.macro-deck.app/ui/concepts/events/).

### Children

None. `ui.text-field` is a leaf.

### Layout

A leaf: `mainSize` or `fill` if declared, otherwise its content extent. `size` is the font size, not a
main-axis extent. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- Draw one line that scrolls horizontally; never wrap.
- Accept typing only when the field declares events; otherwise display `text` read-only.
- Send `adjust` no more than ten times a second - each accepted event is one state write on the producer.
- The producer is authoritative for `text`, except while the field has focus: keep showing what the user
  typed and do not apply an echoed value, so the caret never moves under them.

### See also

- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [Slider](https://docs.macro-deck.app/ui/components/slider/)
- [List](https://docs.macro-deck.app/ui/components/list/) for the results under a search field
- [Modal views](https://docs.macro-deck.app/ui/views/modal/)

## Text

> Source: https://docs.macro-deck.app/ui/components/text/
>
> A single run of text, sized as a fraction of the view basis.

A single run of text, laid out with a line height of exactly one, so its box is exactly its font size.

`ui.text`

### Example

```csharp
new UiStack
{
    Key = "reading",
    Direction = UiComponentDirections.Horizontal,
    Align = UiComponentAlignments.Baseline,
    Gap = 0.02,
    Children =
    [
        new UiTextRun
        {
            Key = "value",
            Text = UiText.From(() => state.Value.Value),
            Size = 0.24,
            Weight = UiComponentTextWeights.Bold,
            Digits = 3,
        },
        new UiTextRun
        {
            Key = "unit",
            Text = "°C",
            Size = 0.1,
            Weight = UiComponentTextWeights.SemiBold,
            Role = UiComponentTextRoles.Secondary,
        },
    ],
}
```

*[Image: A tile showing a large bold reading of 23.4 with a smaller grey °C unit beside it on the same baseline]*

A large live reading with its unit beside it, adapted from the built-in History graph widget.

### Live numeric readouts

```csharp
Text = UiText.From(() => state.Value.Value),
Digits = 2.5,
```

`Digits` reserves room for that many digit widths, so a value that gains or loses a digit does not push
its neighbours sideways. It is a count, not a length, and may be fractional: a decimal separator is
narrower than a digit.

### Shrinking to fit

```csharp
new UiTextRun { Key = "providerName", Text = label, Size = 0.044, MinSize = 0.034 }
```

The run shrinks from `Size` towards `MinSize` until it fits its box. Without `MinSize` it never shrinks
and ellipsizes instead.

### Wrapping

```csharp
new UiTextRun { Key = "label", Text = label, Wrap = UiValue.Of(true), MaxLines = 3 }
```

A run stays on one line unless `Wrap` is true. `MaxLines` caps how many lines it may use before it
ellipsizes.

### Mixing text and images

```csharp
new UiTextRun
{
    Key = "message",
    Text = "ada: hi Kappa",
    Size = 0.08,
    Wrap = UiValue.Of(true),
    MaxLines = 4,
    Spans = UiValue.Of<IReadOnlyList<UiTextSpan>>(
    [
        UiTextSpan.FromText("ada", color: "#9146ff", weight: UiComponentTextWeights.Bold),
        UiTextSpan.FromText(": hi "),
        UiTextSpan.FromImage(emote, alt: "Kappa"),
    ]),
}
```

`Spans` draws styled text and inline images as one paragraph, in place of `Text`. A text span may set its
own `#rrggbb` colour and weight; anything it leaves out comes from the run. An image span is a square one
line high, so the line height stays exactly one and the run is as tall as it is without images. While an
image cannot be shown, its `alt` text is drawn in its place; an image without `alt` is decorative and
draws nothing.

Keep `Text` the plain equivalent of the spans - the same words, with each image as the text it stands for.
A reader that does not know `spans` draws `Text` instead. A span's text is drawn exactly as given: it is
never resolved as a localization reference and never read as markup.

### Colour

```csharp
Role = UiComponentTextRoles.Muted,        // follows the reader's theme
Color = "#ff8800",                        // a colour the user chose; wins over Role
```

Use `Role` for theme colours and `Color` only for a colour that is data. See
[Colours and text](https://docs.macro-deck.app/ui/concepts/theming/).

### Localized text

```csharp
Text = "Now playing",                     // literal
Text = Strings.NowPlaying(),              // your plugin's generated catalog
```

A localization reference resolves in each reader's own active language.

### Properties

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Text` (`text`) | `UiText`: literal, computed or localized | Nothing is drawn | The content. |
| `Size` (`size`) | `UiSize` length | Left to the reader | The font size, which is also the run's line height. |
| `MinSize` (`minSize`) | `UiSize` length | Never shrinks; ellipsizes | The floor `Size` may shrink to so the run fits. |
| `Weight` (`weight`) | `UiComponentTextWeights`: `regular`, `medium`, `semibold`, `bold` | `regular` | The font weight. |
| `Role` (`role`) | `UiComponentTextRoles`: `primary`, `secondary`, `muted` | `primary` | The semantic colour, ignored when `Color` is set. |
| `Color` (`color`) | `#rrggbb` | `Role` decides | A literal colour that overrides `Role`. |
| `Align` (`align`) | `UiComponentAlignments`: `start`, `center`, `end`, `stretch`, `baseline` | `start` | Alignment within the run's own box. |
| `MaxLines` (`maxLines`) | `int` | One; no limit when `Wrap` is true | How many lines the run may occupy before it ellipsizes. |
| `Wrap` (`wrap`) | `bool` | One line, ellipsized | Whether the run may break across lines at all. |
| `FontFace` (`fontFace`) | Font catalogue identifier | The reader's default face | The typeface, from Macro Deck's font catalogue. |
| `Digits` (`digits`) | `double`, digit widths | Exactly as wide as the content | How many digit widths the run reserves. |
| `Spans` (`spans`) | List of `UiTextSpan`: `text` with optional `color` and `weight`, or `image` (`UiResource`) with optional `alt` | Draws `Text` | Inline runs of styled text and images drawn in place of `Text`. |
| `Shadow` (`shadow`) | `bool` | The reader decides | `false` turns off the legibility shadow a reader draws behind text, such as Macro Deck's shadow behind text on a button. |
| `StrokeColor` (`strokeColor`) | `#rrggbb` | No outline | The colour of an outline around the glyphs. |
| `StrokeWidth` (`strokeWidth`) | `UiSize` length | No outline | How far the outline reaches outside each glyph. Drawn only with `StrokeColor` and a width above zero. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/) | Sized by the reader | The run's extent along the parent stack's main axis. |

`Size` is the font, `MainSize` is the extent along the parent's main axis; setting one does not imply the
other.

A label that sits on artwork can drop the shadow and carry an outline instead:

```csharp
new UiTextRun
{
    Text = "Play",
    Shadow = false,
    StrokeColor = "#000000",
    StrokeWidth = UiSize.FromBasis(0.01),
}
```

### Events

None. `ui.text` is never interactive: a value it shows is patched by its producer, never entered by the
reader.

### Children

None. `ui.text` is a leaf.

### Layout

The cross-axis extent is always the line height - exactly the resolved `size` - whatever the parent
offers. Along the main axis a text takes `mainSize` or `fill` if declared, otherwise the reader's own
measurement.

Measured without a font, a text with neither `mainSize` nor `fill` takes **nothing** along the main axis.
So when a sibling fills a row, give every text in that row its own `mainSize`, or the filling sibling
takes their width too and pushes them out of the box. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- Lay the run out with a line height of one; stack gaps are the only vertical spacing.
- Absent `wrap` means one line, ellipsized. A reader that does not know the key does the same, so the run
  stays inside its box.
- Reject any `color` that is not `#rrggbb`, and any `role` outside the listed values, rather than passing
  it through to the styling layer.
- `fontFace`: hold the run back until the face is usable, then reveal it - never draw a fallback face and
  swap. If the face never arrives, or the identifier cannot be resolved, reveal the run in the default face.
- `digits`: draw every digit on the same advance width, and centre the content in the reservation when it
  is narrower.
- `spans`: draw the spans in one inline flow instead of `text`, bounded by `wrap` and `maxLines` like
  `text`. Draw each image square and one line high, aligned to the top of its line, so the line height
  stays one; draw its `alt` text while the image is unavailable, or nothing when `alt` is absent. Ignore a
  span `color` that is not `#rrggbb` and a span that carries neither `text` nor `image`. A reader that does
  not implement `spans` draws `text`.
- `shadow`: when `false`, draw no legibility shadow behind the run. Absent or `true` keeps the reader's
  default. A reader that does not know the key keeps its default.
- `strokeColor` and `strokeWidth`: draw an outline of that colour around every glyph, reaching `strokeWidth`
  outside the glyph edge and never eating into the glyph. The outline does not change the run's box or its
  fit; give it room to paint instead of clipping it. Draw nothing when either key is missing or invalid, or
  the width is zero. A reader that does not know the keys draws no outline. Macro Deck's renderer draws at
  most a tenth of the cell basis, keeps the legibility shadow of a run on a button around its outline unless
  `shadow` is `false`, and shows an outlined run without outline or shadow where the browser cannot apply
  SVG filters to HTML.

### See also

- [Colours and text](https://docs.macro-deck.app/ui/concepts/theming/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)
- [Time](https://docs.macro-deck.app/ui/components/time/) for clocks and timers that tick on the reader
- [Text field](https://docs.macro-deck.app/ui/components/text-field/) for text the user types

## Time and clock

> Source: https://docs.macro-deck.app/ui/components/time/
>
> Draws the current time, digitally or as an analogue face, advanced by the reader's own clock.

A digital time run and an analogue clock face. Both carry a time reference meaning "now, as the reader
sees it", so the tree is built once and every reader keeps it ticking on its own clock.

`macrodeck.dynamic-text`, `macrodeck.clock-dial`

### Example

```csharp
var reference = UiValue.Of(UiTimeReference.InZone("America/New_York"));

new UiDynamicText
{
    Key = "time",
    Value = reference,
    Format = UiTimeFormats.Time,
    Seconds = true,
    Size = 0.24,
    MinSize = 0.13,
    Weight = UiComponentTextWeights.Bold,
    Align = UiComponentAlignments.Center,
}
```

*[Image: A wide tile showing 10:05 in large bold digits followed by smaller grey seconds :30]*

New York's time in the viewer's own language and hour cycle, with smaller muted seconds - the built-in
Clock widget's face. It costs no patch and keeps running while the connection is down.

### Time zones

```csharp
UiTimeReference.Now()                          // {"$time":{}}
UiTimeReference.InZone("Europe/Berlin")        // {"$time":{"zone":"Europe/Berlin"}}
```

A zone is an IANA id. Absent (or a null or empty id passed to `InZone`) means the reader's own zone.

### Captions for the zone

```csharp
new UiDynamicText { Key = "caption", Value = reference, Format = UiTimeFormats.ZoneName }
```

*[Image: The time 10:05:30 with the caption New York beneath it]*

| Format | `America/New_York` | No zone |
|---|---|---|
| `zone-name` | `New York` | Empty |
| `zone-offset` | `UTC-05:00` in winter, `UTC-04:00` in summer | Empty |

A caption bound to either disappears when the reference has no zone, rather than echoing the reader's
own zone back.

### A 12/24-hour clock

```csharp
new UiDynamicText
{
    Key = "time",
    Value = reference,
    Format = UiTimeFormats.Time24Hour,
    RequiredComponentVersion = 2,
    Fallback = new UiDynamicText { Key = "timeLocalized", Value = reference, Format = UiTimeFormats.Time },
}
```

Pin a face only when the display must look the same on every device, and always through a named format,
never a pattern of your own. Every format except `time`, `date` and `zone-name` needs
`RequiredComponentVersion = 2` and a `time`/`date` fallback: negotiation catches unknown types, not unknown
values, so an older reader would otherwise draw an empty run.

| Format (`UiTimeFormats`) | 14:05 on 31 Dec 2025 |
|---|---|
| `time` (`Time`) | The reader's language and the user's app-wide 12h/24h/system preference |
| `time-12h` (`Time12Hour`) | `2:05 PM` - hour `1`-`12`, the reader's day period |
| `time-12h-padded` (`Time12HourPadded`) | `02:05 PM` - hour `01`-`12` |
| `time-24h` (`Time24Hour`) | `14:05` - hour `00`-`23` |
| `time-24h-unpadded` (`Time24HourUnpadded`) | `14:05`, but `9:05` rather than `09:05` - hour `0`-`23` |

### Dates

| Format (`UiTimeFormats`) | 31 Dec 2025 |
|---|---|
| `date` (`Date`) | Abbreviated weekday, day and month, ordered by the reader's language |
| `date-day-first` (`DateDayFirst`) | `31/12/25` |
| `date-month-first` (`DateMonthFirst`) | `12/31/25` |
| `date-iso` (`DateIso`) | `2025-12-31` |
| `date-long` (`DateLong`) | Full weekday and month names with the day, ordered by the reader's language |

### An analogue face

```csharp
new UiClockDial
{
    Key = "dial",
    Value = reference,
    Seconds = true,
    Fill = true,
    Fallback = new UiDynamicText { Key = "dialFallback", Value = reference, Format = UiTimeFormats.Time },
}
```

*[Image: An analogue clock face with twelve tick marks, white hour and minute hands at five past ten, and a blue second hand]*

A dial degrades to a dynamic text, which in turn degrades to `ui.text`, so a reader that draws no dial
still shows the right time. `Color` tints the ticks and the hour and minute hands; the face, second
hand and hub keep the theme.

### Properties

#### `macrodeck.dynamic-text`

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Value` (`value`) | A time reference | Nothing is drawn | The instant to show. |
| `Format` (`format`) | A `UiTimeFormats` value | - | Which derivation to draw; an unknown value draws nothing. |
| `Seconds` (`seconds`) | `true`, `false` | `false` | Whether a `time*` run includes seconds. |
| `Size` (`size`) | A length | Left to the reader | The font size. |
| `MinSize` (`minSize`) | A length | Never shrinks; ellipsizes instead | The floor `size` may shrink to so the run fits. |
| `Weight` (`weight`) | A font weight | `regular` | The font weight. |
| `Role` (`role`) | A text role | `primary` | The semantic colour. |
| `Color` (`color`) | `#rrggbb` | The `role` colour | A literal run colour that overrides `role`. |
| `Align` (`align`) | A `UiComponentAlignments` value | `start` | Alignment within the run's own box. |

#### `macrodeck.clock-dial`

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Value` (`value`) | A time reference | Nothing is drawn | The instant the hands show. |
| `Seconds` (`seconds`) | `true`, `false` | `false` | Whether the second hand is drawn. |
| `Color` (`color`) | `#rrggbb` | Every mark keeps the theme | Tints both tick weights and the hour and minute hands. |

### Events

None. Both are read-only.

### Children

None - both are leaves.

### Layout

`macrodeck.dynamic-text` sizes exactly like `ui.text`: its box is its font size, with a line height of
one. `macrodeck.clock-dial` draws in `d`, the largest square that fits its box, centred rather than
stretched. Both follow the ordinary leaf rule on their parent stack's main axis. Full model:
[Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

These are `macrodeck.*` types because a reader cannot draw them from the tree alone - it must resolve
`$time` against its own clock. The governing contract is
[ADR 0065](https://github.com/Macro-Deck-App/Macro-Deck/blob/main/engineering/decisions/0065-the-component-profile-authoring-contracts.md).

- `{"$time":{"zone":"..."}}` means the current instant on the reader's host-synchronised clock, read in
  that zone. Absent zone means the reader's own zone; an unrecognised zone falls back to the reader's own
  zone rather than failing the tree.
- A `$time` member must be an object and defines only `zone`, a string; anything else is rejected.
  `dynamic-text`'s `value` accepts only a time reference - never a progress reference.
- Separator, digit system, writing direction and day-period position come from the reader's language.
  `time`'s hour cycle follows the user's app-wide preference as supplied by the host, falling back to the
  reader's language; the pinned `time-*` formats ignore it.
- Every `time*` format draws seconds, with the separator before them, at `0.55` of the run's `size` in
  the `muted` role - even when `color` is set.
- Digits are drawn with equal advance width, so the run does not shift as it counts.
- `zone-name` is the last segment of the IANA id with underscores replaced by spaces; `zone-offset` is
  `UTC±hh:mm` at that instant. Both are empty with no zone.
- A reader draws nothing for a `format` it does not know. Only `time`, `date` and `zone-name` are
  guaranteed at component version 1.
- A reader that predates dial `color` draws a themed dial; `color` carries no version requirement.
- A dial re-evaluates at least once a second and computes hand angles from the whole second. No
  sub-second sweep - it is not derivable from the reference.
- Dial lengths are fractions of `d`. The fixtures in `ui-model/fixtures/component-profile/` resolve the
  face, tick and hand geometry and state the three hand angles for one named instant.

### See also

- [Progress](https://docs.macro-deck.app/ui/components/progress/) - the same idea for a playback position
- [Text](https://docs.macro-deck.app/ui/components/text/)
- [Components](https://docs.macro-deck.app/ui/components/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## Toggle

> Source: https://docs.macro-deck.app/ui/components/toggle/
>
> An on/off switch the user flips, reporting the new state as a boolean.

An on/off switch: a capsule track with a knob at one end. The user flips it; you receive the new state.

`ui.toggle`

### Example

```csharp
new UiToggle
{
    Key = "mute",
    On = UiValue.From(() => state.Value.Muted),
    LevelColor = "#34c759",
    Events = [UiEventHandler.On(UiComponentEvents.Change, data => SetMuted(data))],
    Fallback = new UiButton
    {
        Key = "muteFallback",
        Events = [UiEventHandler.On(UiComponentEvents.Press, () => ToggleMuted())],
        Children = [new UiTextRun { Key = "label", Text = UiText.From(() => state.Value.Muted ? "On" : "Off") }],
    },
}
```

*[Image: A green switch with its white knob at the right end, centred in a tile]*

### Reading the state

```csharp
UiEventOutcome SetMuted(UiEventData data)
{
    if (!data.TryGetBoolean(out var muted))
    {
        return UiEventOutcome.Rejected("The event payload is not a boolean.");
    }

    state.Set(state.Value with { Muted = muted });
    return UiEventOutcome.Accepted;
}
```

`change` carries the state the user switched to, as a JSON boolean - not a request to invert whatever you
hold. Set `On` from it, and the switch stays where the user put it.

### Holding the flip

A completed press flips the drawn switch at once and sends `change`. The reader holds that state until your
`On` changes or one second passes, the same reconciliation a [slider](https://docs.macro-deck.app/ui/components/slider/) uses. If you
reject the change or never update `On`, the switch returns to your value after that second.

### Properties

| Property | Values | Default (absent) | Meaning |
|---|---|---|---|
| `On` (`on`) | `bool` | Off | Whether the switch is on. |
| `LevelColor` (`levelColor`) | `#rrggbb` | The reader's own accent colour | The track's colour when on. |
| `Size` (`size`) | length | As high as the box allows | The track's height; the track is `1.75` times as wide. |
| `MainSize` (`mainSize`), `Fill` (`fill`) | - | - | Shared with every leaf - see [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/). |

### Events

| Event | Fires when | Payload |
|---|---|---|
| `change` (`UiComponentEvents.Change`) | A press completed on the switch | The new state, a JSON boolean |

### Children

None. `ui.toggle` is a leaf.

### Layout

The element's whole box is the press surface; the drawn track is centred in it. On its parent's main axis
a toggle is `Size` long in a vertical parent and `1.75 * Size` in a horizontal one, unless `MainSize` or
`Fill` says otherwise. See [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- **Geometry:** a capsule track `size` high (absent: `min(height, width / 1.75)`) and `1.75` times as wide,
  centred. A knob of diameter `0.8 * size`, inset `0.1 * size`, in the primary text colour, at the trailing
  end when on and the leading end when off. The track is `levelColor` or the accent colour when on, the
  tertiary surface colour when off.
- **Interaction only where declared.** Without `change` the switch is drawn and cannot be touched.
- **Press feedback:** with `change` declared, the reader paints its press tint on touch. The deck tile's own
  pressed state follows the switch only when the toggle is the root of the tree, as for a button.
- **A completed press** flips the drawn state, sends `change` once with the new state, and holds it until
  `on` changes or 1000 ms pass. A cancelled press sends nothing.
- **Keyboard and hardware:** in the Macro Deck desktop app, activating a tile whose first interactive node
  is a toggle flips it, exactly as a press does. The web client does not activate tree nodes from the
  keyboard.
- **Activation acts on the producer's value:** it negates the `on` the tree last carried, not a state the
  reader is still holding after a tap, and the drawn switch moves when the producer answers.
- A reader that does not know `ui.toggle` draws the node's `fallback`, typically a `ui.button` whose label
  says the state:

```json
{
  "type": "ui.toggle",
  "properties": { "on": true, "events": ["change"] },
  "fallback": {
    "type": "ui.button",
    "properties": { "events": ["press"] },
    "children": [{ "type": "ui.text", "properties": { "text": "On" } }]
  }
}
```

### See also

- [Segmented](https://docs.macro-deck.app/ui/components/segmented/)
- [Button](https://docs.macro-deck.app/ui/components/button/)
- [Events](https://docs.macro-deck.app/ui/concepts/events/)
- [State and bindings](https://docs.macro-deck.app/ui/concepts/state-and-bindings/)

## Transform

> Source: https://docs.macro-deck.app/ui/components/transform/
>
> Rotates, scales and shifts its children together about a pivot, so a needle turns by patching one number.

Draws its children like a [layer](https://docs.macro-deck.app/ui/components/stack-and-layer/) - every child across the whole box,
first one furthest back - then scales, rotates and shifts them together as one picture.

`ui.transform`

### Example

```csharp
new UiTransform
{
    Key = "needle",
    Rotation = UiValue.From(() => speed.Value * 1.8 - 90),
    OriginX = 0.5,
    OriginY = 0.9,
    Children = [new UiImage { Key = "needleArt", Source = needle }],
    Fallback = new UiTextRun { Key = "reading", Text = UiText.From(() => $"{speed.Value:0} km/h") },
}
```

*[Image: A half-circle gauge filled in blue to 70 percent, with a white needle turned about a pivot near the bottom edge]*

A gauge needle pivoting near its bottom edge. Each update is a `set-properties` patch carrying `rotation`
alone; the reader redraws locally, with no new image per update.

### Rotating an icon

```csharp
new UiTransform { Key = "arrow", Rotation = 90, Children = [arrowIcon] }
```

*[Image: An upward arrow icon rotated 90 degrees so it points right]*

`Rotation` is degrees, clockwise, about the pivot. The pivot defaults to the centre.

### Moving the pivot

```csharp
new UiTransform { Key = "hand", Rotation = 30, OriginX = 0.5, OriginY = 1.0, Children = [hand] }
```

```
     /        pivot at (0.5, 1.0):
    /         the hand turns about
   o          the middle of the bottom edge
```

`OriginX` and `OriginY` are fractions of the element's own width and height. A value outside `0..1`
puts the pivot outside the box.

### Scaling and nudging

```csharp
new UiTransform { Key = "art", Zoom = 1.2, OffsetX = 0.1, OffsetY = -0.05, Children = [artwork] }
```

Applied in a fixed order: `Zoom`, then `Rotation`, both about the pivot, then the offsets in the parent's
unrotated axes. These are the same keys a [button](https://docs.macro-deck.app/ui/components/button/) frames its artwork with; on a
button the artwork scales about its own centre within the ranges listed there, here it scales about the
pivot and any finite value is allowed.

### Nesting

```csharp
new UiTransform { Key = "dial", Rotation = dialAngle, Children = [face, new UiTransform { Key = "needle", Rotation = needleAngle, Children = [needle] }] }
```

Nested transforms compose.

### Properties

| Property | Values | Default | Meaning |
|---|---|---|---|
| `Rotation` (`rotation`) | `double`, degrees | `0` | The clockwise turn about the pivot. |
| `OriginX` (`originX`) | `double`, fraction of own width | `0.5` | Where the pivot sits across the box; outside `0..1` is outside the box. |
| `OriginY` (`originY`) | `double`, fraction of own height | `0.5` | Where the pivot sits down the box. |
| `Zoom` (`zoom`) | `double`, multiplier | `1` | Scales the content about the pivot; a value not greater than `0` means `1`. |
| `OffsetX` (`offsetX`) | `double`, fraction of own width | `0` | Shifts the content across, after zoom and rotation. |
| `OffsetY` (`offsetY`) | `double`, fraction of own height | `0` | Shifts the content down, after zoom and rotation. |
| `MainSize` (`mainSize`), `Fill` (`fill`), `Answer` (`answer`) | - | - | Shared with every container - see [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/). |

### Events

None of its own.

### Children

Any element, any number. Transforms nest and compose.

### Layout

The transform is visual only. The node's own box, its size on the parent's main axis and its siblings are
laid out as if it were absent, and text inside it is fitted to its untransformed box. See
[Sizing](https://docs.macro-deck.app/ui/concepts/sizing/).

### Reader behaviour

- Apply `zoom`, then `rotation`, both about the pivot, then `offsetX`/`offsetY` in the parent's unrotated
  axes.
- Treat a `zoom` not greater than `0` as `1`; accept any finite value otherwise.
- Lay out and fit text as if the transform were absent.
- Clip nothing; an ancestor that clips, such as a tile or a button, still does.
- Presses hit the drawn shape. A `ui.slider` under a non-zero `rotation` has no defined pointer mapping.
- A reader that does not know `ui.transform` draws the node's `fallback`, so a gauge should carry one that
  still shows its reading:

```json
{
  "type": "ui.transform",
  "properties": { "rotation": 42, "originX": 0.5, "originY": 0.9 },
  "children": [{ "type": "ui.image", "properties": { "source": { "resourceId": "needle" } } }],
  "fallback": { "type": "ui.text", "properties": { "text": "42 km/h" } }
}
```

### See also

- [Stack and layer](https://docs.macro-deck.app/ui/components/stack-and-layer/)
- [Button](https://docs.macro-deck.app/ui/components/button/) - `zoom` and offsets on artwork
- [Slider](https://docs.macro-deck.app/ui/components/slider/)
- [Sizing](https://docs.macro-deck.app/ui/concepts/sizing/)

## Video stream

> Source: https://docs.macro-deck.app/ui/components/video-stream/
>
> Shows a live video stream from a video stream provider, played from a session the reader opens, suspends and closes itself.

A live video stream that a [video stream provider](https://docs.macro-deck.app/features/video-streams/) offers: an OBS scene, a camera,
a capture device. The tree names the stream and nothing else. The client showing it asks Macro Deck for a
session, plays it over a transport it supports, and releases it again, so you never write a
player, a reconnect loop or a placeholder yourself.

`macrodeck.video-stream`

### Example

```csharp
new UiVideoStream
{
    Key = "program",
    Stream = UiValue.Of(new UiVideoStreamReference { Provider = "com.example.obs::studio", Id = "Program" }),
    Fit = UiComponentImageFits.Cover,
    Fill = true,
    Fallback = new UiTextRun { Key = "programFallback", Text = "Update Macro Deck to see the stream" },
}
```

*[Image: A wide tile with the same landscape video twice: letterboxed on the left, filling and cropped on the right]*

The same stream with `contain` on the left and `cover` on the right.

`macrodeck.video-stream` works wherever Macro Deck UI does: in a built-in widget, in your own
[widget type](https://docs.macro-deck.app/ui/views/widget-types/), in a [folder view](https://docs.macro-deck.app/ui/views/folder-views/), in a
[modal](https://docs.macro-deck.app/ui/views/modal/) or on a [screensaver](https://docs.macro-deck.app/ui/views/screensavers/), and the same whether your plugin
runs in or out of process.

### Properties

| Property | Meaning |
|---|---|
| `Stream` | The stream to show, as a `UiVideoStreamReference`. Absent shows a placeholder. |
| `Fit` | `contain` (default) shows the whole picture, letterboxed; `cover` fills the box and crops. |
| `Size` | The extent along the parent stack's main axis. |

`Provider` is the provider's qualified id, `plugin.id::provider-id`, the one
`VideoStreamProviderRegistration.QualifiedId` returns. `Id` is the stream's id within that provider.
On the wire:

```json
{"type":"macrodeck.video-stream","properties":{"stream":{"provider":"com.example.obs::studio","id":"Program"},"fit":"cover"}}
```

A reader treats a `stream` it cannot read, such as a missing member, as absent.

### Sizing

`Size` is how much of the parent stack's main axis the view takes, not the edge of a square: the other axis
is whatever the stack gives it. Absent, the view takes no space on the main axis, so give it `Size` or
`Fill`. The picture always keeps the stream's own aspect ratio inside that box. Before the first frame arrives,
the reader reserves the width and height the provider declared for the stream, so the layout does not jump.

### What the reader takes care of

- **The session.** It opens one while the view is on screen, suspends it while the view is scrolled out of
  sight or covered by the screensaver or the lock screen, and closes it when the view goes away or the
  page is hidden.
- **States.** While the stream is connecting or reconnecting, gone, or offered in no transport this device
  plays, the reader draws its own placeholder and a short message, in the reader's language. A message the
  provider sends with its session update is shown instead of the generic one.
- **Recovery.** A session that ended because the provider restarted, the connection to Macro Deck dropped or
  the source went away is opened again on its own, with a growing delay. A stream that does not exist is
  tried again when the provider's streams change.
- **Transports.** The client offers `hls`, only where the device plays it natively, and `mjpeg`, which every
  device plays, and uses the first one the provider serves. A transport that fails to play on this device,
  for example because the browser blocks autoplay, is dropped for the next attempt while another is left.
  The media comes from Macro Deck itself, never from the provider. See
  [What Macro Deck's clients play](https://docs.macro-deck.app/features/video-streams/#what-macro-decks-clients-play).
- **Sound.** The stream always plays muted.

The reader names the view after the stream for assistive technology.

### Older readers

A reader that predates `macrodeck.video-stream` draws the node's `Fallback`, as for any type it does not
know, so set one. The type needs no `RequiredComponentVersion`.
