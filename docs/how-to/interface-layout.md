# Fit the battle to your screen

Every interface region is placed by the skin, and the stage rectangle by one component. Between
them you can move any part of the interface, reserve screen area for your own UI, and keep the
formation inside the space you left it.

## Region placement

The **Layout** and **Regions** groups on a `BattleSkinPreset` position the whole interface. There
is no prefab to open: each region host is built from its tokens at runtime, so moving a region is
an asset edit.

### The fields every region carries

| Field | What it does |
| --- | --- |
| **Visible** | Whether the region exists at all. See [Hide what you replace](#hide-what-you-replace) |
| **Anchor** | Which corner or edge the region attaches to - nine values, from `TopLeft` to `BottomRight` ([`SkinAnchor`](../reference/skinning-and-appearance.md#skinanchor)) |
| **Offset** | Distance from that anchor in reference pixels. Positive values move the region inward, so the same offset reads the same way on every anchor |
| **Size** | Width and height in reference pixels. Zero on an axis leaves that axis to the region's own content, which is how the roster and tooltip grow to fit their rows |
| **Scale** | Extra scale for this region alone, 0 to 2. A value of 0 resolves to 1, so scaling is not a way to hide a region |

Out-of-range numbers are clamped when the skin compiles rather than rejected, so a half-edited
layout still renders. Full list in
[`SkinRegionTokens`](../reference/skinning-and-appearance.md#skinregiontokens).

### Where the shipped skins put each region

All four shipped skins share these values, and a new preset starts from them.

| Region | Anchor | Offset | Size |
| --- | --- | --- | --- |
| Status (roster) | `TopLeft` | 24, 24 | 340 wide, sized to content |
| Timeline | `TopCenter` | 0, 20 | 720 x 76 |
| Skill tray | `BottomCenter` | 0, 28 | 880 x 116 |
| Feedback log | `BottomLeft` | 24, 160 | 420 x 168 |
| Result banner | `MiddleCenter` | 0, 0 | 520 x 150 |
| Transport | `TopRight` | 24, 24 | 360 x 118 |
| Tooltip | `BottomRight` | 24, 160 | 360 wide, sized to content |

Those numbers are in the skin's **Reference Resolution** - 1920 x 1080 by default, never smaller
than 320 x 240 - which drives the interface canvas scaler along with **Match Width Or Height**,
where 0 matches width, 1 matches height and the default is 0.5.

!!! warning "The Skin Browser preview is not a layout preview"
    The browser draws a fixed mock interface: a roster panel, bars, pips, one timeline chip and
    one tray button. It is enough to judge colours and bar shapes, and it ignores your region
    anchors entirely, so check placement in play mode.

## Safe area

Leave **Use Safe Area** on and the interface builds one rect inset to the device safe area and
parents every region inside it, so every region is safe-area correct without you positioning
anything twice and nothing lands under a notch or a home indicator.
[`SafeAreaFitter`](../reference/interface-and-widgets.md#safeareafitter) re-applies only when the
screen or the reported safe area changes, so it costs nothing on desktop. The stage is inset
separately, by its own **Respect Safe Area** field below.

## Hide what you replace

Set **Visible** to false on any region you are drawing yourself. A hidden region is never created,
so it costs nothing, and the interface calls that would have fed it become no-ops rather than
errors - you can keep forwarding snapshots and decisions while you replace one panel at a time.

For a shipping build, hide the transport region or tick **Hide Transport Controls** on
`BattleUiRoot`. That tick forces the region invisible whichever skin is assigned, which makes it
the safer switch. The scenario, seed and playback controls are development tools.

!!! note "TransportMount follows the transport region"
    `BattleUiRoot.TransportMount` is the rect your own controls can be parented to, and it exists
    only while the transport region is visible. A skin swap destroys and rebuilds it - see
    [Restyle the interface](../tutorials/skinning-your-battle.md#what-a-swap-rebuilds).

## Frame the stage

Without a frame component the presenter uses a fixed 1920 x 1080 viewport at the screen origin, so
on any other resolution the formation is cropped or floats in dead space. Add **TurnGauge >
Battle Stage Frame** to the presenter's own object to derive the rectangle from the real screen.

| Field | What it does |
| --- | --- |
| **Mode** | `FixedAspect` (the default) keeps **Design Aspect**, 16:9 out of the box, and centres the stage inside the margins, so combatant spacing is identical on every device. `FullScreen` uses everything inside the margins. `Explicit` uses **Explicit Rect** in pixels and ignores screen size |
| **Margin Left / Right / Top / Bottom** | Fractions of the available area reserved on each side, each capped at 0.45. The defaults reserve nothing at the sides, 12% at the top for the timeline and 18% at the bottom for the skill tray |
| **Respect Safe Area** | On by default. Starts from the safe area rather than the full screen, then applies the margins inside it |
| **Stage Scale** | 0.25 to 2, applied about the rectangle's centre. Below 1 pulls the formation tighter without shrinking your token art, because only positions come from the viewport |

The component re-frames whenever the screen size or safe area changes, and while you edit a field
in the inspector in play mode. Stage and interface are placed independently, so these margins are
the only thing keeping the stage out from under the interface: a top margin of 0 leaves the
timeline over the back rank.

```csharp
var frame = presenter.GetComponent<BattleStageFrame>();
FormationViewport applied = frame.AppliedViewport;   // the rectangle now in use
frame.ApplyNow();                                    // re-frame after a change

// Or place the stage yourself, with no frame component at all.
presenter.SetViewport(new FormationViewport(left: 0, bottom: 120, width: 1600, height: 760));
```

Every value here is presentation-only: moving or resizing the stage cannot change a state hash, an
event chain or a result. Field list in
[`BattleStageFrame`](../reference/stage-and-tokens.md#battlestageframe).

## Assign your own token art

TurnGauge draws nameplates, bars and pips over a combatant. Six drawn characters ship under
`Samples/Characters/`, licensed for use in your own projects, so the demo reads as a battle from the
first run and you can keep them if they suit you. Register a prototype carrying a `SpriteRenderer` under
`BattleStage2D.TokenPoolKey` before you bind, and every spawned token is a clone of it. The token view
records the slot facing and mirrors the sprite only when that direction differs from the source-art
direction, writes the slot's sorting order to the renderer, and treats the prototype's colour as the tint a downed
combatant desaturates away from. For per-combatant art, resolve the token after binding:

```csharp
if (presenter.Stage.TryGetToken(combatantId, out var token))
    token.GetComponent<SpriteRenderer>().sprite = mySprite;
```

!!! warning "Re-apply per-token art after a re-frame"
    Any viewport change rebuilds the stage: every token returns to the pool and is acquired again.
    Nothing re-assigns a sprite you set on an individual token, so re-apply your art after a
    re-frame, or bake it into the prototype.

## Optional bloom

The shipped look needs no post-processing - glow is drawn inside the interface shader, which is why
the package depends on no post-processing package and cannot conflict with your volumes.
**TurnGauge > Battle Stage Bloom (Optional)** exists only for projects that want a softer bloom
and vignette over the whole stage and are not already running a post stack. Nothing adds it for
you; put it on the battle camera yourself.

**Intensity** at 0 disables the bloom pass, **Threshold** raises the brightness a pixel needs
before it blooms, and **Downsample** and **Iterations** trade fill rate for softness. If the
shader cannot be loaded the frame is copied through untouched rather than going black.

!!! warning "Built-in render pipeline only"
    Under URP or HDRP this component logs one explanatory warning and disables itself rather than
    silently doing nothing. Use that pipeline's own Bloom and Vignette volume overrides instead;
    read `IsSupportedPipeline` to check from code.

## Next

- **[What each interface region draws](interface-regions.md)** - what you are placing, and what each
  region refuses to do.
- **[Place combatants with the Formation Editor](place-formations.md)** - the slot layout projected
  into the stage rectangle you just framed.
- **[Palette and surfaces](skin-surfaces.md)** - the colours and shapes regions are drawn from.
