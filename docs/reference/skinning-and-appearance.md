# Skinning and appearance

21 types in this area.

!!! abstract "On this page"
    [BattleSkinDefaults](#battleskindefaults) &middot; [BattleSkinPreset](#battleskinpreset) &middot; [CompiledBattleSkin](#compiledbattleskin) &middot; [SkinAnchor](#skinanchor) &middot; [SkinBarTokens](#skinbartokens) &middot; [SkinEasing](#skineasing) &middot; [SkinFillMode](#skinfillmode) &middot; [SkinFloatingNumberTokens](#skinfloatingnumbertokens) &middot; [SkinLayoutProfile](#skinlayoutprofile) &middot; [SkinMaterialPool](#skinmaterialpool) &middot; [SkinMotionTokens](#skinmotiontokens) &middot; [SkinPaletteTokens](#skinpalettetokens) &middot; [SkinRegionStretch](#skinregionstretch) &middot; [SkinRegionTokens](#skinregiontokens) &middot; [SkinShape](#skinshape) &middot; [SkinStagePresenceTokens](#skinstagepresencetokens) &middot; [SkinStatusPipTokens](#skinstatuspiptokens) &middot; [SkinSurfaceGraphic](#skinsurfacegraphic) &middot; [SkinSurfaceTokens](#skinsurfacetokens) &middot; [SkinTargetingTokens](#skintargetingtokens) &middot; [SkinTypographyTokens](#skintypographytokens)

## BattleSkinDefaults

```csharp
public static class BattleSkinDefaults
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinDefaults.cs</small>

The shipped skins, defined in code rather than as serialized assets.

Two reasons. First, the interface always has a complete, valid look even
when a scene assigns no skin asset, so the package never renders as
unstyled boxes. Second, no texture, font, or material is redistributed,
which keeps the provenance audit clean; every look is drawn procedurally
from these numbers.

The Skin Browser materializes any of these into an editable
`BattleSkinPreset` asset via "Duplicate and Edit".

**Fields**

`public const float CommandDeckHeight`

:   Height of the full-bleed command deck, in reference pixels.

`public float CornerRadius`

:   Corner radius every surface in the look starts from, in reference pixels. Bars clamp it to half their own height, so a generous value rounds a thin bar into a capsule instead of distorting it.

`public const string DefaultSkinId`

:   Identity of the skin loaded when a scene assigns none.

`public SkinFillMode FillMode`

:   Fill treatment for the look's surfaces. The stage backdrop ignores it and always uses a radial gradient, since it is the one surface that has to sit behind everything else.

`public const float GaugeBandHeight`

:   Height of the full-bleed turn-order band, in reference pixels.

`public float GlowIntensity`

:   Base glow intensity, scaled by the same fraction as `GlowRadius`. Values above 1 read as bloom without a post-processing stack.

`public float GlowRadius`

:   Base outer glow radius. Each recipe scales it - raised panels, pips, and bar fills take a fraction of it - so a single zero here turns the glow off across the whole look.

`public float GradientSpread`

:   How far the second gradient stop is darkened away from the fill colour. Zero leaves the two stops identical, which makes even a gradient fill read as flat.

`public const float LogStripHeight`

:   Height of the log strip that caps the command deck, in reference pixels.

`public SkinShape PipShape`

:   Silhouette of the status pips, the one shape that changes from look to look. It also decides whether a pip is given a corner radius at all, since only a rounded rectangle reads one.

`public const string PreviousDefaultSkinId`

:   Identity of the look that was the default before Ironlight. It is still shipped and still selectable; only the default moved, so a project that recorded this id keeps the look it chose.

`public const float SafeMargin`

:   Safe margin held clear at the screen edge, in reference pixels.

`public float ShadowRadius`

:   Base drop-shadow softness. A surface that ends up with a radius of zero is also given a fully transparent shadow colour, so it draws no shadow rather than a hard edge.

`public float StrokeWidth`

:   Border thickness the look's surfaces are stroked with. The stage backdrop is the exception and drops it to zero, since it draws no border behind the rest of the interface.

`public SkinShape SurfaceShape`

:   Silhouette every panel, button, and bar in the look is cut from. The four original skins are rounded rectangles; Ironlight is chamfered, which is most of what makes it read as machined metal rather than as soft plastic.

**Methods**

`public static IReadOnlyList<CompiledBattleSkin> All()`

:   Every shipped skin, in browser order.
    - **Returns** &mdash; A fresh five-item list ordered Ironlight, Slate Nocturne, Parchment Atlas, Neon Circuit, then Minimal Mono.

`public static CompiledSkinLayout BandLayout(SkinLayoutProfile profile)`

:   The three-band region placement for one aspect profile.
    - `profile` &mdash; Which composition to build. Wide and Ultrawide share their numbers on purpose - band heights are fixed, so a wider screen spends every extra pixel on the stage instead of inflating the interface.
    - **Returns** &mdash; A complete layout whose regions all dock into a band edge or the safe margin.

`public static CompiledBattleSkin Default()`

:   The skin used when a scene assigns none.
    - **Returns** &mdash; A freshly compiled Ironlight skin used as the package fallback.

`public static SkinFloatingNumberTokens DefaultFloatingNumbers()`

:   Floating-number sizing and timing shared by every shipped skin. The rise, easing, and scatter are unchanged; only the sizes moved. A number spawned over the stage competes with a 300-pixel character, so 26 disappeared against it. Criticals land at 80 with the skin's warning colour and a halo, which is the one moment the interface is allowed to shout.
    - **Returns** &mdash; Shared floating-number size, critical scale, rise, lifetime, easing, and scatter tokens.

`public static CompiledSkinLayout DefaultLayout()`

:   The region placement shared by every shipped skin.
    - **Returns** &mdash; The wide-profile three-band region placement used by every built-in skin.

`public static SkinMotionTokens DefaultMotion()`

:   Transition timings shared by every shipped skin.
    - **Returns** &mdash; Shared bar, panel, pip, timeline, and pulse transition timings at full motion scale.

`public static SkinStagePresenceTokens DefaultStagePresence()`

:   Depth falloff, contact shadow, and key light shared by every shipped skin.
    - **Returns** &mdash; Staging enabled, with a rank falloff and a shadow width in the middle of the windows the visual direction specifies, so a skin that edits neither still satisfies the composition audit.

`public static SkinTypographyTokens DefaultTypography()`

:   Type sizing shared by every shipped skin. The floor is 16, not 13. Thirteen reference pixels on a 27-inch monitor at arm's length is about a quarter of a degree of arc, which is fine for an inspector field and far too small for something a player has to read while deciding a turn. Everything above the floor is a step in the same four-size scale - caption, body, name, heading - so at most four sizes are ever on screen at once.
    - **Returns** &mdash; Shared caption, body, tracked-label, name, heading, title, spacing, and dark-outline typography tokens.

`public static CompiledBattleSkin Ironlight()`

:   Dark iron lit by one warm lamp. The shipped default.
    - **Returns** &mdash; A complete freshly compiled Ironlight skin with the band layout, chamfered surfaces, and team-coloured health.

`public static SkinSurfaceTokens IronlightBackdrop()`

:   Default-look stage backdrop drawn behind the combatants.
    - **Returns** &mdash; Borderless radial Ironlight backdrop tokens for the combat stage.

`public static SkinSurfaceTokens IronlightButton()`

:   Default-look card surface: the resting skill card and rail chip.
    - **Returns** &mdash; Ironlight resting button surface tokens.

`public static SkinSurfaceTokens IronlightButtonDisabled()`

:   Default-look card surface for a skill the actor cannot currently use.
    - **Returns** &mdash; Ironlight disabled-button tokens with muted contrast.

`public static SkinSurfaceTokens IronlightButtonSelected()`

:   Default-look card surface for the selected or hovered entry.
    - **Returns** &mdash; Ironlight selected-button tokens using the brass accent treatment.

`public static SkinBarTokens IronlightCastBar()`

:   Default-look cast bar. It carries no delta ghost, since progress only rises.
    - **Returns** &mdash; Ironlight cast-progress tokens without a delayed ghost.

`public static SkinBarTokens IronlightGauge()`

:   Default-look scheduler gauge for the combatant plate; no delta ghost either.
    - **Returns** &mdash; Ironlight scheduler-gauge tokens without a delayed ghost.

`public static SkinBarTokens IronlightHealthBar()`

:   Default-look health bar. Its fill is the ally team colour, not green.
    - **Returns** &mdash; Ironlight health-bar track, fill, ghost, border, and timing tokens.

`public static SkinPaletteTokens IronlightPalette()`

:   Dark iron lit by one warm lamp. The default look. The single rule that separates it from the others is that health is team-coloured rather than green: allies read bone-steel, enemies read rust, and green is freed up to mean healing and nothing else. On a 6v6 board that is the difference between twelve identical bars and a picture of who is winning.
    - **Returns** &mdash; Dark-iron palette tokens with a brass accent, steel alternate, and team-coloured health roles.

`public static SkinSurfaceTokens IronlightPanel()`

:   Default-look base panel: feedback log, tooltip, and band backings.
    - **Returns** &mdash; Ironlight base-panel surface tokens derived from its palette and look profile.

`public static SkinSurfaceTokens IronlightPanelRaised()`

:   Default-look raised surface: the acting chip and hovered rows.
    - **Returns** &mdash; Ironlight raised-panel tokens with stronger separation than the base panel.

`public static SkinStatusPipTokens IronlightPips()`

:   Default-look status pip strip drawn above each combatant.
    - **Returns** &mdash; Ironlight status-pip shape, color, size, spacing, and pop-motion tokens.

`public static SkinBarTokens IronlightResourceBar()`

:   Default-look resource bar for the actor's spendable pools.
    - **Returns** &mdash; Ironlight resource-bar tokens for spendable pools.

`public static SkinBarTokens IronlightShieldBar()`

:   Default-look shield bar, drawn as a second thinner rail under health.
    - **Returns** &mdash; Thin Ironlight shield-bar tokens.

`public static SkinSurfaceTokens IronlightTooltip()`

:   Default-look tooltip and result banner backing.
    - **Returns** &mdash; Ironlight elevated tooltip and result-banner surface tokens.

`public static CompiledBattleSkin MinimalMono()`

:   Light, flat, glowless; the neutral base to customize from.
    - **Returns** &mdash; A complete freshly compiled light skin with flat surfaces, no glow, and reduced pulse scale.

`public static SkinPaletteTokens MinimalMonoPalette()`

:   Light, flat, glowless. The neutral base to customize from.
    - **Returns** &mdash; Light neutral palette tokens intended as a glowless customization base.

`public static CompiledBattleSkin NeonCircuit()`

:   Deep indigo with saturated neon rims and heavy halos.
    - **Returns** &mdash; A complete freshly compiled neon skin with strong in-shader halos.

`public static SkinPaletteTokens NeonCircuitPalette()`

:   Deep indigo with saturated neon rims. The loudest look.
    - **Returns** &mdash; Deep-indigo palette tokens with saturated cyan, magenta, and violet accents.

`public static CompiledBattleSkin ParchmentAtlas()`

:   Warm paper and ink, no glow.
    - **Returns** &mdash; A complete freshly compiled parchment skin with outline-free sepia typography.

`public static SkinPaletteTokens ParchmentAtlasPalette()`

:   Warm paper and ink. Suits adventure and campaign framing.
    - **Returns** &mdash; Warm parchment palette tokens with sepia ink and muted red and green states.

`public static CompiledBattleSkin Resolve(BattleSkinPreset preset)`

:   Resolves the skin a component should draw with: the assigned asset when present, otherwise the shipped default. Never returns null, so callers need no null branch.
    - `preset` &mdash; Assigned authored preset to compile, or null to select Slate Nocturne.
    - **Returns** &mdash; The preset's compiled tokens when assigned; otherwise a non-null default skin.

`public static CompiledBattleSkin SlateNocturne()`

:   Dark slate with cyan and amber accents.
    - **Returns** &mdash; A complete freshly compiled dark-slate skin with default typography, motion, and layout.

`public static SkinSurfaceTokens SlateNocturneBackdrop()`

:   Default-look stage backdrop drawn behind the combatants.
    - **Returns** &mdash; Borderless radial Slate Nocturne backdrop tokens for the combat stage.

`public static SkinSurfaceTokens SlateNocturneButton()`

:   Default-look button surface: skill tray, timeline, and transport buttons.
    - **Returns** &mdash; Slate Nocturne resting button surface tokens.

`public static SkinSurfaceTokens SlateNocturneButtonDisabled()`

:   Default-look button surface for a skill the actor cannot currently use.
    - **Returns** &mdash; Slate Nocturne disabled-button tokens with muted contrast.

`public static SkinSurfaceTokens SlateNocturneButtonSelected()`

:   Default-look button surface for the selected or hovered entry.
    - **Returns** &mdash; Slate Nocturne selected-button tokens using the active accent treatment.

`public static SkinBarTokens SlateNocturneCastBar()`

:   Default-look cast bar. It carries no delta ghost, since progress only rises.
    - **Returns** &mdash; Slate Nocturne cast-progress tokens without a delayed ghost.

`public static SkinBarTokens SlateNocturneGauge()`

:   Default-look scheduler gauge for the combatant plate; no delta ghost either.
    - **Returns** &mdash; Slate Nocturne scheduler-gauge tokens without a delayed ghost.

`public static SkinBarTokens SlateNocturneHealthBar()`

:   Default-look health bar for nameplates and roster rows.
    - **Returns** &mdash; Slate Nocturne health-bar track, fill, ghost, border, and timing tokens.

`public static SkinPaletteTokens SlateNocturnePalette()`

:   Dark slate with cyan and amber accents. The previous default look.
    - **Returns** &mdash; Dark slate palette tokens with cyan informational and amber selection accents.

`public static SkinSurfaceTokens SlateNocturnePanel()`

:   Previous-default base panel: status roster, feedback log, timeline backing.
    - **Returns** &mdash; Slate Nocturne base-panel surface tokens derived from its palette and look profile.

`public static SkinSurfaceTokens SlateNocturnePanelRaised()`

:   Default-look raised surface: roster rows and the next timeline entry.
    - **Returns** &mdash; Slate Nocturne raised-panel tokens with stronger separation than the base panel.

`public static SkinStatusPipTokens SlateNocturnePips()`

:   Default-look status pip strip drawn above each combatant.
    - **Returns** &mdash; Slate Nocturne status-pip shape, color, size, spacing, and pop-motion tokens.

`public static SkinBarTokens SlateNocturneResourceBar()`

:   Default-look resource bar for the actor's spendable pools.
    - **Returns** &mdash; Slate Nocturne resource-bar tokens for spendable pools.

`public static SkinBarTokens SlateNocturneShieldBar()`

:   Default-look shield bar, drawn thinner than the health bar.
    - **Returns** &mdash; Thin Slate Nocturne shield-bar tokens.

`public static SkinSurfaceTokens SlateNocturneTooltip()`

:   Default-look tooltip and result banner backing.
    - **Returns** &mdash; Slate Nocturne elevated tooltip and result-banner surface tokens.

`public static SkinSurfaceTokens StageGround(SkinPaletteTokens palette)`

:   The lit ground a formation stands on: a soft, wide pool of light warmed towards the skin's accent, fading to nothing at its rim. Nothing like it existed. Without a ground plane every combatant hung in mid-air, which is most of why the shipped screenshots read as an unfinished scene rather than a battle. It is derived from the palette rather than stored on the skin asset, so every existing preset -- including one a buyer authored before this shipped -- gets a floor with no migration and no new serialized field.
    - `palette` &mdash; The palette the ground is tinted from.
    - **Returns** &mdash; Surface tokens for one team's ground pool.

`public static bool TryFind(string stableId, out CompiledBattleSkin skin)`

:   Finds a shipped skin by its stable id.
    - `stableId` &mdash; Id to match exactly; a skin asset's own id is never found here, since only the shipped looks are searched.
    - `skin` &mdash; The matching skin, or null when nothing matches.
    - **Returns** &mdash; True when a shipped skin carries that id.

---

## BattleSkinPreset

:material-star: **Start here**

```csharp
public sealed class BattleSkinPreset : ScriptableObject
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinPreset.cs</small>

Every value the battle interface draws itself with, in one asset.
Duplicate a shipped skin, edit it in the inspector, and the whole HUD
restyles with no prefab surgery and no code changes.

A skin is presentation-only. It never enters a snapshot, a replay, a
state hash, or a compiled catalog, so swapping skins can never change a
battle outcome.

**Properties**

`public string Description`

:   Description shown in the Skin Browser.

`public string DisplayName`

:   Name shown in the Skin Browser.

`public string StableIdText`

:   Persistent skin identity.

**Methods**

`public CompiledBattleSkin Compile()`

:   Resolves this asset into the immutable value set the HUD consumes. Out-of-range authored values are clamped rather than rejected, so a half-edited skin still renders instead of throwing at runtime.
    - **Returns** &mdash; A complete skin, never null. Every token group is copied by value, so editing this asset afterwards does not alter an already-compiled skin.

`public void CopyFrom(CompiledBattleSkin source, string newStableId, string newDisplayName)`

:   Overwrites every field from `source`. Used by "Duplicate and Edit" in the Skin Browser and by the editor tests; it is the only supported way to author a skin from code.
    - `source` &mdash; Values to write in. Required; a null source throws.
    - `newStableId` &mdash; Replacement identity, or null or empty to keep the source's id.
    - `newDisplayName` &mdash; Replacement Skin Browser name, or null or empty to keep the source's name.

---

## CompiledBattleSkin

```csharp
public sealed class CompiledBattleSkin
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinPreset.cs</small>

The immutable skin the HUD reads. Built either from a
`BattleSkinPreset` asset or from `BattleSkinDefaults`
so the interface always has a complete, valid look even when no asset is
assigned.

**Constructors**

`public CompiledBattleSkin()`

:   Assembles a skin from finished token groups. Values are stored exactly as given; clamping is `BattleSkinPreset.Compile`'s job, not this constructor's. A null surface, bar, or layout group throws, because the interface has nothing to fall back to for those.
    - `bars` &mdash; Complete styling for health, shield, resource, cast, and scheduler bars.
    - `description` &mdash; Player-facing prose describing the skin, or for no description.
    - `displayName` &mdash; Player-facing skin name, or for an empty name.
    - `floatingNumbers` &mdash; Size, travel, and easing tokens for combat floating numbers.
    - `layout` &mdash; Canvas scaling and placement for every HUD region; must not be .
    - `motion` &mdash; Durations, easing, and reduced-motion policy shared by HUD animations.
    - `palette` &mdash; Semantic colors consumed by surfaces, bars, text, and feedback.
    - `stableIdText` &mdash; Persistence-safe skin identifier, or for an empty identifier.
    - `statusPips` &mdash; Size, spacing, and count presentation for combatant status pips.
    - `stagePresence` &mdash; Grounding, silhouette and selection-presence tokens for world-space combatant art.
    - `surfaces` &mdash; Complete styling for panels, buttons, tooltips, and the stage backdrop; must not be .
    - `typography` &mdash; Font reference, sizes, and text style shared across the HUD.
    - `targeting` &mdash; Reticle and affected-area preview tokens used to show a pending target request.

**Properties**

`public CompiledSkinBars Bars`

:   Styling for the health, shield, resource, cast and scheduler bars. Never null.

`public string Description`

:   The short prose describing the look, shown under the name in the Skin Browser. Empty, never null, when the source supplied none.

`public string DisplayName`

:   The name to list this skin under in a picker. Empty, never null, when the source supplied none.

`public SkinFloatingNumberTokens FloatingNumbers`

:   Size, rise distance and easing for the damage, healing and shield numbers. Their colours come from `FloatingNumberColor` instead, so that damage and healing stay tied to the palette.

`public CompiledSkinLayout Layout`

:   Reference resolution, canvas match, safe-area handling and the position of every HUD region. Never null.

`public SkinMotionTokens Motion`

:   Transition timings for the whole interface. Widgets scale their durations through `SkinMotionTokens.Scale`, which is how a single reduce-motion flag snaps every animation at once instead of each widget deciding for itself.

`public SkinPaletteTokens Palette`

:   The semantic colour roles every widget draws from. Because widgets ask for a role rather than a literal colour, recolouring the whole interface is a change here and nowhere else.

`public string StableIdText`

:   The skin's persistent identity, carried over from the asset it was compiled from. Renaming the asset does not change it, so this is what to record when saving a player's chosen look. Empty, never null, when the source supplied none.

`public SkinStagePresenceTokens StagePresence`

:   Depth falloff between ranks, the contact shadow under every combatant, and the key light they are tinted by. This is what separates a stage from a set of correctly-placed coordinates; turn `SkinStagePresenceTokens.Enabled` off for a flat stage.

`public SkinStatusPipTokens StatusPips`

:   Size, spacing and stack-count settings for the status pip strip drawn above each combatant.

`public CompiledSkinSurfaces Surfaces`

:   Fills, strokes, glows and shadows for the panels, buttons, tooltip and stage backdrop. Never null.

`public SkinTargetingTokens Targeting`

:   How a target pick is expressed, and whether that choice adapts to the device. Never changes what is legal; see `TargetPreview`.

`public SkinTypographyTokens Typography`

:   Type sizes and treatment. Read the font through `ResolveFont` rather than from here, since an unset font falls back to Unity's built-in one.

**Methods**

`public Color FloatingNumberColor(FloatingNumberStyle style)`

:   The colour a floating number of `style` uses.
    - `style` &mdash; Semantic event category whose palette role should be selected.
    - **Returns** &mdash; The palette color assigned to the requested category, or primary text for an unknown enum value.

`public TMP_FontAsset ResolveFont()`

:   The font the skin draws text with. It always returns one, even in a project that has never imported TextMeshPro's resources, so the battle interface can never come up wordless or unbuilt.
    - **Returns** &mdash; The configured font, TextMeshPro's default, the essential-resources font, or one built from Unity's own built-in typeface.

---

## SkinAnchor

```csharp
public enum SkinAnchor
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Where a HUD region attaches inside the safe area.

| Value | Meaning |
| --- | --- |
| `TopLeft` | Top-left safe-area point with a matching pivot. |
| `TopCenter` | Horizontal center of the safe area's top edge. |
| `TopRight` | Top-right safe-area point with a matching pivot. |
| `MiddleLeft` | Vertical center of the safe area's left edge. |
| `MiddleCenter` | Center point of the safe area. |
| `MiddleRight` | Vertical center of the safe area's right edge. |
| `BottomLeft` | Bottom-left safe-area point with a matching pivot. |
| `BottomCenter` | Horizontal center of the safe area's bottom edge. |
| `BottomRight` | Bottom-right safe-area point with a matching pivot. |

---

## SkinBarTokens

```csharp
public struct SkinBarTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

A value bar: health, shield, resource, cast, or gauge.

**Fields**

`public float CornerRadius`

:   The bar's intended corner radius in reference pixels. What is actually drawn is the radius on `Track` and `Fill`, since those are the surfaces that reach the shader; the shipped bars set all three to the same value, so change them together when reshaping a bar.

`public float DeltaCatchUpSeconds`

:   Seconds the ghost holds at the previous value before catching up. The ghost only appears when the value falls, and this duration passes through `SkinMotionTokens.Scale`, so zero here, a zero `SkinMotionTokens.MotionScale`, or `SkinMotionTokens.ReduceMotion` each suppress it.

`public Color DeltaColor`

:   Colour of the trailing ghost that marks the value just lost.

`public SkinSurfaceTokens Fill`

:   The surface masked to the current value. The trailing ghost is built from it too, recoloured to `DeltaColor` and stripped of its glow. Only the fill colour is cut by the value; a stroke on this surface still traces the whole bar, so use `Track` for the outline and leave the fill's stroke transparent unless that is the look you want.

`public float Height`

:   Bar height in reference pixels. It is also the layout height the bar requests, so the rows around it move when this changes.

`public Color SegmentColor`

:   Colour the tick marks are blended toward. Its alpha controls how strongly they cut in, and a fully transparent colour draws none at all whatever `SegmentCount` says. The ticks go onto both `Track` and `Fill`, so they stay aligned as the value moves.

`public int SegmentCount`

:   Tick marks drawn across the bar. Zero draws one continuous bar.

`public SkinSurfaceTokens Track`

:   The surface drawn across the bar's full width, showing what the value is measured against. It sits behind both the ghost and the fill, so its own glow is largely hidden and its stroke is what gives the bar its outline.

**Methods**

`public SkinBarTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy, with `Track` and `Fill` sanitized in turn; this instance is unchanged.

---

## SkinEasing

```csharp
public enum SkinEasing
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

The easing curve applied to a skinned transition.

| Value | Meaning |
| --- | --- |
| `Linear` | Constant rate; no easing. |
| `EaseIn` | Accelerates from rest. |
| `EaseOut` | Decelerates into rest. |
| `EaseInOut` | Accelerates then decelerates. |
| `BackOut` | Overshoots slightly then settles. |

---

## SkinFillMode

```csharp
public enum SkinFillMode
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

How a skinned surface fills its rectangle.

| Value | Meaning |
| --- | --- |
| `Flat` | A single flat colour. |
| `LinearGradient` | A two-stop linear gradient along `SkinSurfaceTokens.GradientAngleDegrees`. |
| `RadialGradient` | A two-stop radial gradient from the surface centre. |

---

## SkinFloatingNumberTokens

```csharp
public struct SkinFloatingNumberTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Rise-and-fade numbers for damage, healing, and shields.

**Fields**

`public float CriticalScale`

:   Multiplies `FontSize` for `FloatingNumberStyle.Critical` only; every other style draws at the base size.

`public int FontSize`

:   Size every number is drawn at before `CriticalScale` is applied. Numbers are drawn on their own world-space canvas over the stage, not in the HUD, so this is independent of `SkinTypographyTokens` and needs to be much larger than body text to read at the same distance.

`public float HorizontalScatter`

:   Horizontal spread in reference pixels so stacked hits stay readable. The offset is derived from the spawn position rather than a random draw, so it never touches RNG the simulation could observe. Zero stacks the numbers.

`public float LifetimeSeconds`

:   Seconds a number stays visible. `SkinMotionTokens.ReduceMotion` caps it at a quarter second rather than removing the number, so a hit is never silent.

`public float RiseDistance`

:   How far a number travels upward from where it was spawned, in reference pixels, over the whole of `LifetimeSeconds`. The number fades out over the second half of that time regardless, so a long rise reads as slower rather than as lingering longer.

`public SkinEasing RiseEasing`

:   Shapes the rise over the number's lifetime. It moves the position only; the fade always runs on the same schedule, so easing changes where the number is when it starts disappearing. `SkinEasing.BackOut` carries the number past `RiseDistance` before settling back, which is worth knowing if the rise is tuned to clear a nameplate exactly.

**Methods**

`public SkinFloatingNumberTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy; this instance is unchanged. `RiseEasing` is left as authored.

---

## SkinLayoutProfile

```csharp
public enum SkinLayoutProfile
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Which band composition a layout is authored for. The three shipped
profiles keep the same band heights and move only what has to move, so a
project does not re-author a HUD per device.

| Value | Meaning |
| --- | --- |
| `Wide` | 16:9 and wider-but-not-ultrawide. |
| `Ultrawide` | 21:9 and wider. |
| `Portrait` | Taller than it is wide. |

---

## SkinMaterialPool

```csharp
public sealed class SkinMaterialPool : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/SkinMaterialPool.cs</small>

Reference-counted material pool for skinned surfaces, owned by a component
rather than by static state.

The Presentation assembly forbids static fields that can retain a
`UnityEngine.Object`, because such a cache survives a domain
reload and a scene unload and then hands out destroyed materials. Anchoring
the pool to the canvas root gives every material a real owner: when the
interface goes away, so do its materials.

The shader is loaded from Resources rather than found by name so it
survives build shader stripping without the buyer editing Always Included
Shaders. If it cannot load, callers fall back to the default UI material,
which draws a plain quad instead of a magenta error surface.

**Properties**

`public int CachedMaterialCount`

:   Live cached material count; useful in tests and profiling.

`public bool IsShaderAvailable`

:   True when the skinned-surface shader is available.

**Fields**

`public const string ShaderName`

:   Shader name, used as a secondary lookup.

`public const string ShaderResourcePath`

:   Resources path of the skinned-surface shader.

**Methods**

`public Material Acquire(SkinMaterialRequest request)`

:   Returns a material for `request`, sharing an existing one when the parameters match exactly.
    - `request` &mdash; The immutable request to validate and execute.
    - **Returns** &mdash; A shared reference-counted material for the request, or null when the shader is unavailable.

`public void Clear()`

:   Destroys every pooled material. Safe to call repeatedly.

`public static SkinMaterialPool EnsureFor(Component owner)`

:   Finds the pool owning `owner`, creating one on the nearest canvas root when absent. Returns null only when the owner is not in a scene.
    - `owner` &mdash; Scene component whose nearest parent pool or Canvas host should own materials.
    - **Returns** &mdash; The existing parent pool, a new pool on the Canvas or owner object, or null for a null owner.

`public void Release(Material material)`

:   Drops one reference to a pooled material.
    - `material` &mdash; Material previously acquired from this pool; foreign or null materials are ignored.

---

## SkinMotionTokens

```csharp
public struct SkinMotionTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Transition timings. Every duration scales by `MotionScale`.

**Fields**

`public SkinEasing BarEasing`

:   Shapes that travel. It applies to the fill only; the ghost behind it always catches up at a constant rate, which is what keeps the gap between the two readable.

`public float BarTransitionSeconds`

:   How long a bar takes to travel to a new value, before scaling. Once `Scale` reduces it to zero the bar snaps instead, and the trailing ghost is skipped with it, so a reduced-motion player sees the new value but not the amount just lost.

`public float MotionScale`

:   Multiplies every duration handed out by `Scale`. Zero snaps every change instantly.

`public float PanelFadeSeconds`

:   How long a panel takes to fade in, before scaling. The result banner uses it; at zero the banner appears at full opacity on the frame it is shown rather than never appearing.

`public float PipPopSeconds`

:   How long a status pip takes to pop in, before scaling. Offered for hosts that animate their own pip strip; the shipped combatant plate adds and removes pips outright and does not read it.

`public float PulseScale`

:   Scale a combatant token reaches at the peak of a pulse. The pulse rises and falls within `PulseSeconds`, so this is a peak rather than a resting size and a token is never left enlarged. Values close to 1 still register: the shipped Minimal Mono skin pulses at 1.04.

`public float PulseSeconds`

:   How long a whole pulse takes, out and back, before scaling. Once `Scale` reduces it to zero the token is returned to its rest scale immediately, so a pulse requested under reduced motion cannot leave a token stuck at `PulseScale`.

`public bool ReduceMotion`

:   Skip decorative motion. `Scale` then returns zero for every duration, so values snap instead of animating, while floating numbers stay briefly visible so nothing is missed. Drive this from a player accessibility setting.

`public float TimelineShiftSeconds`

:   How long the timeline takes to settle after the running order changes, before scaling. Offered for hosts that animate their own timeline; the shipped strip repaints in place and does not read it.

**Methods**

`public static float Ease(SkinEasing easing, float t)`

:   Maps a normalized 0..1 progress value through the selected easing curve. Input and output are clamped for presentation use only.
    - `t` &mdash; Progress from 0 to 1; anything outside that range is clamped first.
    - `easing` &mdash; Linear, smooth-step, cubic-out, or back-out curve applied to normalized time.
    - **Returns** &mdash; Eased progress. Every curve stays within 0..1 except `SkinEasing.BackOut`, which rises above 1 near the end and is what gives it its overshoot, so a caller that lerps with this result must tolerate values past the target.

`public SkinMotionTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy; this instance is unchanged. `ReduceMotion` and `BarEasing` are left as authored.

`public float Scale(float seconds)`

:   The effective duration for `seconds` under this skin.
    - `seconds` &mdash; The unscaled duration the animation would like.
    - **Returns** &mdash; `seconds` multiplied by `MotionScale`, never negative, and zero whenever `ReduceMotion` is set. Treat a zero result as an instruction to snap rather than animate.

---

## SkinPaletteTokens

```csharp
public struct SkinPaletteTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

The semantic colour roles a skin assigns once and reuses everywhere.

**Fields**

`public Color Accent`

:   The colour the interface uses to point at something: the selected skill button and its glow, the next timeline entry, status pips, and the scheduler gauge while it fills. It appears more often than any other accent, so it is the single value that most changes a skin's character.

`public Color AccentAlt`

:   Secondary accent. The cast bar, the resource bar, and resource floating numbers use it.

`public Color AllyTeam`

:   Tints the name plate of a combatant on the player's team. The stage decides which team that is by matching each team against the player team id it was given, so with no player team set every combatant is tinted `EnemyTeam` instead.

`public Color Background`

:   The colour behind everything else. The shipped skins build the stage backdrop as a radial gradient from it to a darker shade of itself, and reuse it for the empty part of a bar track and for segment ticks, so it sets how deep the HUD reads overall rather than only the scene edges.

`public Color Border`

:   The stroke colour panels and bars fall back to when nothing more specific applies. A selected or focused widget swaps it for `Accent`, which is what makes selection read at a glance.

`public Color EnemyTeam`

:   Tints the name plate of every combatant not on the player's team. Only the plate label takes the tint; bars keep the colours the skin gave them, so health still reads the same on both sides of the field.

`public Color Negative`

:   Reads as bad news: damage numbers and the defeat banner.

`public Color Positive`

:   Reads as good news: healing numbers, the health bar, and the victory banner.

`public Color Shield`

:   Shield and barrier amounts: the shield bar, shield numbers, and a roster row that is holding shield.

`public Color Surface`

:   The resting colour of a HUD panel. Its alpha is carried through to the panel surface, so a translucent value lets the stage read through the interface; the tooltip surface forces the same colour opaque so text over a busy stage stays legible.

`public Color SurfaceRaised`

:   The colour that lifts something out of a panel: a roster row, a skill button, the next timeline entry, and the +N overflow status pip all use it, so it needs enough contrast against `Surface` to be read as a state change rather than as decoration.

`public Color TextMuted`

:   The recessive text colour: a dead combatant's name, the target caption under a skill button, the tooltip's target row, and the order number of timeline entries that are not next. It still has to be read, so keep it clearly distinguishable from `TextSecondary`.

`public Color TextPrimary`

:   The colour of anything the player is meant to read first: combatant names, headline text, bar readouts, and floating numbers that carry no semantic colour of their own.

`public Color TextSecondary`

:   The colour of text that supports a primary label rather than competing with it: log lines, the tooltip's chance and timing rows, and roster detail. The tooltip's cost row is drawn in `AccentAlt` instead, so a price still reads as its own thing.

`public Color Warning`

:   Reads as caution: critical-hit numbers and the concession banner.

---

## SkinRegionStretch

```csharp
public enum SkinRegionStretch
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

How a HUD region behaves on each axis: pinned at its authored size, or
stretched to the full width or height of the safe area.

Stretching is what makes a band. A pinned region floats at an anchor with
a pixel offset, which is individually reasonable and collectively
arbitrary; a stretched region shares an edge with the screen and with
every other region docked into the same band, so the composition holds at
any aspect ratio without re-authoring an offset.

| Value | Meaning |
| --- | --- |
| `None` | Pinned at the authored size on both axes. |
| `Horizontal` | Full-bleed across the safe-area width. |
| `Vertical` | Full-bleed down the safe-area height, with the authored width kept and the vertical offset read as a top and bottom inset. |
| `Both` | Full-bleed on both axes, inset by `SkinRegionTokens.Offset`. |

---

## SkinRegionTokens

```csharp
public struct SkinRegionTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Where one HUD region sits. Every region is independently placeable so a
customer can move the whole interface without editing a prefab.

**Fields**

`public SkinAnchor Anchor`

:   The point of the safe area the region hangs from. It becomes the region's anchor and its pivot at once, so the region grows away from that corner and stays put on screens of any aspect. `Offset` is then measured inward from it.

`public Vector2 Offset`

:   Distance from the anchor in reference pixels, always measured inward, so the same numbers keep their meaning when the region is re-anchored to another corner. See `InwardOffset` for the signed form a RectTransform wants.

`public float Scale`

:   Extra scale for this region alone. Zero or negative is read as 1, so an unset value never scales a region out of sight.

`public Vector2 Size`

:   Region size in reference pixels. Zero on an axis leaves that axis alone, so the region sizes to its content.

`public SkinRegionStretch Stretch`

:   Whether the region is pinned at its authored size or stretched to the full width or height of the safe area. A stretched axis reads `Offset` as an inset from both edges of that axis and ignores `Size` on it. That is what turns a region into a band: it shares an edge with the screen, so panels docked into it line up with each other at every aspect ratio instead of drifting apart.

`public bool Visible`

:   Whether the interface builds this region. A hidden region is never created rather than created and disabled, so switching it off costs nothing at runtime and its view is simply skipped when the interface repaints. This is how a host drops a block of the HUD it does not want without editing a prefab.

**Methods**

`public static Vector2 AnchorPoint(SkinAnchor anchor)`

:   The normalized anchor point for `anchor`.
    - `anchor` &mdash; Named safe-area location to convert into normalized coordinates.
    - **Returns** &mdash; The matching point with (0,0) at the bottom left and (1,1) at the top right, ready to use as a RectTransform anchor and pivot. A value outside the enum falls back to the bottom right.

`public static SkinRegionTokens At(SkinAnchor anchor, Vector2 offset, Vector2 size)`

:   A visible region anchored at `anchor`.
    - `offset` &mdash; Inward distance from the anchor in reference pixels.
    - `size` &mdash; Size in reference pixels; zero on an axis sizes to content.
    - `anchor` &mdash; Safe-area edge or corner that fixes both region anchors and pivot.
    - **Returns** &mdash; A visible region at scale 1.

`public static SkinRegionTokens Band()`

:   A visible full-bleed horizontal band of `height` reference pixels, hung from the top or bottom of the safe area.
    - `anchor` &mdash; Edge the band hangs from. Only the vertical half is read, so any of the three top anchors gives a top band and any of the three bottom anchors gives a bottom band.
    - `height` &mdash; Band height in reference pixels.
    - `sideInset` &mdash; Left and right inset in reference pixels. Zero is true full bleed, which is what the shipped gauge rail uses.
    - `edgeOffset` &mdash; Distance inward from that edge in reference pixels. Zero sits the band flush against the edge; a positive value stacks it above a band that is already there, which is how the log strip caps the command deck.
    - **Returns** &mdash; A visible, horizontally stretched region at scale 1.

`public Vector2 InwardOffset()`

:   Converts `Offset` into a signed anchored position so positive values always move a region inward from its anchor.
    - **Returns** &mdash; `Offset` with its sign flipped on each axis whose anchor sits at the far edge. A centred axis keeps the raw value, where positive still means right and up.

`public SkinRegionTokens Sanitized()`

:   Copies the region with nonnegative dimensions and a scale capped at two. A nonpositive scale becomes one; other fields are retained.
    - **Returns** &mdash; A presentation copy with those clamps applied. This method does not validate finite values or modify the source region.

`public SkinRegionTokens ScaledBand(float scale)`

:   Clamps every token into its supported range.
    - `scale` &mdash; Factor from `CompiledSkinLayout.BandScale`. One, or anything outside a sane range, returns this region untouched.
    - **Returns** &mdash; A clamped copy; this instance is unchanged. A zero or negative `Scale` becomes 1, and a negative `Size` axis becomes zero.

---

## SkinShape

```csharp
public enum SkinShape
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

The silhouette a skinned surface draws.

| Value | Meaning |
| --- | --- |
| `RoundedRect` | A rounded rectangle honouring the corner radius. |
| `Circle` | A circle inscribed in the shorter rectangle axis. |
| `Capsule` | A capsule: fully rounded on the shorter axis. |
| `Hexagon` | A hexagon inscribed in the rectangle. |
| `Diamond` | A diamond inscribed in the rectangle. |
| `Chamfer` | A rectangle with its corners cut off at 45 degrees rather than rounded. |

---

## SkinStagePresenceTokens

```csharp
public struct SkinStagePresenceTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

How the stage stages its combatants: the falloff between depth ranks, the
contact shadow every body stands on, and the one warm key light.

Draw order alone does not make a scene. A formation whose seats are at
correct coordinates and correct sorting still reads as a diagram, because
nothing tells the eye which body is near and which is far - every
silhouette is the same size, the same brightness, and touches nothing.
These tokens are what turn that arrangement into a photograph of a fight.

Rank is depth, and it is read from the formation rather than authored:
seats sharing a ground line share a rank, and rank rises going away from
the camera. A flat arrangement therefore has one rank and no falloff at
all, which is the right answer for it.

**Fields**

`public Color ContactShadowColor`

:   Colour of the contact shadow. It is a colour rather than plain black because a shadow on a lit stage carries the bounce of whatever it sits on, and pure black on a coloured backdrop reads as a hole.

`public float ContactShadowFlatness`

:   The shadow's height as a fraction of its width. Low values read as a high camera looking down a shallow stage, which is the shipped framing; at 1 the shadow is a circle and the stage reads top-down.

`public float ContactShadowOpacity`

:   How opaque the contact shadow is against the backdrop.

`public float ContactShadowWidth`

:   Width of a combatant's contact shadow as a fraction of that combatant's own sprite width, so one value serves bodies of every size. Zero removes the shadow. Without one a painted character floats: there is no evidence it is standing on the same ground as anybody else, and no amount of correct positioning supplies that evidence.

`public bool Enabled`

:   Whether the stage stages at all. Off leaves every combatant at one size, one brightness, and no shadow - the pre-staging look - without the host having to neutralize four separate tokens to get there.

`public Color KeyLightColor`

:   The single key light every combatant is lit by, tinting bodies toward it most strongly at the front rank and falling off with depth. One light, deliberately. Two lights need a direction each and turn a skin into a lighting rig; one warm key against a cool backdrop is the whole of what this presentation needs to stop looking flat.

`public float KeyLightStrength`

:   How far the front rank is tinted toward `KeyLightColor`. Zero leaves art exactly as painted, which is what a project with its own lighting wants.

`public float RankDarkening`

:   How much luminance each rank loses against the one in front of it, compounding the same way `RankScale` does. Scale alone is ambiguous - a smaller silhouette can be a smaller character. Darkening is what makes it distance, because atmosphere takes light out of everything behind the front line.

`public float RankScale`

:   How much smaller each rank is than the one in front of it. Applied per rank, so the second rank back is this squared. Below about 0.8 the back rank stops reading as further away and starts reading as smaller creatures; at 1 there is no depth cue left. The shipped value sits in the middle of that window.

**Methods**

`public SkinStagePresenceTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy; this instance is unchanged. `Enabled` and both colours are left as authored.

`public float ScaleForRank(int rank)`

:   The size multiplier for a combatant standing at `rank`.
    - `rank` &mdash; Depth rank, 0 at the front. Negative values are treated as the front.
    - **Returns** &mdash; `RankScale` raised to `rank`, or exactly 1 when staging is off, so a caller can multiply unconditionally.

`public Color TintForRank(Color tint, int rank)`

:   Lights and depth-fades one combatant's tint for its rank.
    - `tint` &mdash; The combatant's own tint, normally white for unmodified art.
    - `rank` &mdash; Depth rank, 0 at the front. Negative values are treated as the front.
    - **Returns** &mdash; The tint pulled toward `KeyLightColor` and then darkened for depth. Alpha is carried through untouched, so this composes with a death fade rather than fighting it. Staging off returns `tint` unchanged.

---

## SkinStatusPipTokens

```csharp
public struct SkinStatusPipTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

The status pip strip drawn above a combatant.

**Fields**

`public int MaximumVisible`

:   Pips drawn before the strip overflows. Past this many statuses the last visible pip becomes a +N pip counting the ones not shown, so the strip never grows wider than this.

`public bool ShowStackCounts`

:   Allows a count to be drawn inside a pip. On the shipped combatant plate only the overflow pip carries one, reading +N for every status the strip has no pip of its own for. The overflow pip takes the place of the last visible one, so N runs one higher than the count past `MaximumVisible`. Turning this off leaves that pip blank, so the strip still shows that something is hidden but not how much.

`public float Size`

:   Edge length of one pip in reference pixels. It also fixes the height of the strip and the size of the stack-count digits, which are derived from it, so a small pip stays legible rather than carrying unreadable text.

`public float Spacing`

:   Gap between neighbouring pips in reference pixels. It widens the strip without widening the pips, so together with `Size` and `MaximumVisible` it decides how much room the strip takes above a combatant.

`public SkinSurfaceTokens Surface`

:   Pip surface. Its shape, stroke, and glow are drawn as authored, but the fill is replaced when the pip is drawn: `SkinPaletteTokens.Accent` for a status pip, `SkinPaletteTokens.SurfaceRaised` for the overflow pip.

**Methods**

`public SkinStatusPipTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy, with `Surface` sanitized in turn; this instance is unchanged.

---

## SkinSurfaceGraphic

```csharp
public sealed class SkinSurfaceGraphic : MaskableGraphic
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/SkinSurfaceGraphic.cs</small>

Draws one `SkinSurfaceTokens` as a uGUI graphic through the
TurnGauge skinned-surface shader. Every panel, button, bar, gauge, and
status pip in the HUD is one of these, so restyling the interface means
changing token values rather than swapping prefabs or textures.

The mesh is padded beyond the layout rect so glow and shadow can bleed
outside the shape without being clipped. Padding is excluded from layout,
so a glowing widget still occupies exactly its `RectTransform`.

**Properties**

`public float FillAmount`

:   Filled fraction in [0,1]. Bars and gauges animate this; other surfaces leave it at 1.

`public bool FillVertical`

:   True when `FillAmount` runs bottom-to-top.

`public float Padding`

:   Padding in reference pixels added around the rect so glow and shadow are not clipped by the quad.

`public SkinSurfaceTokens Surface`

:   The surface tokens this graphic draws.

**Methods**

`public void Apply(SkinSurfaceTokens value)`

:   Updates apply on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `value` &mdash; Shape, fill, stroke, glow, and shadow tokens to sanitize and draw.

`public void ApplySegments(int count, Color color)`

:   Applies segment ticks, used by segmented bars.
    - `color` &mdash; Shader color used for separators between filled segments.
    - `count` &mdash; Requested segment count, clamped to zero through 32.

`public void SetFillColors(Color primary, Color secondary)`

:   Replaces only the fill colours, keeping shape and glow.
    - `primary` &mdash; Replacement first gradient stop.
    - `secondary` &mdash; Replacement second gradient stop.

`public void SetGlow(Color color, float radius, float intensity)`

:   Replaces only the glow, keeping shape and fill.
    - `color` &mdash; Replacement outer-glow color.
    - `intensity` &mdash; Replacement glow multiplier sanitized to the supported shader range.
    - `radius` &mdash; Replacement glow radius in reference pixels.

---

## SkinSurfaceTokens

```csharp
public struct SkinSurfaceTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Fill, stroke, and glow for one skinned surface. Every skinned widget
resolves to one of these, so a customer restyles the whole HUD by editing
a handful of surfaces rather than hunting individual prefabs.

**Fields**

`public float CornerRadius`

:   Corner treatment in reference pixels: the fillet radius under `SkinShape.RoundedRect` and the cut length under `SkinShape.Chamfer`. Every other shape ignores it. The shader clamps it to half the shorter axis, so an over-large value settles into a capsule or a diamond instead of distorting the shape.

`public Color FillColor`

:   The near gradient stop, and the entire fill under `SkinFillMode.Flat`. A linear gradient starts from it at the leading edge and a radial gradient starts from it at the centre, so this is the colour a surface reads as whichever fill mode is chosen.

`public Color FillColorSecondary`

:   The far gradient stop. `SkinFillMode.Flat` ignores it and draws `FillColor` alone.

`public SkinFillMode FillMode`

:   Flat, linear-gradient, or radial-gradient sampling used by the surface shader.

`public Color GlowColor`

:   Halo colour. Its alpha is one of the three switches on the glow, so a fully transparent colour suppresses the halo however generous `GlowRadius` and `GlowIntensity` are. The halo falls off outside the silhouette only, so it never washes out the fill.

`public float GlowIntensity`

:   Multiplies the glow mask. A glow needs a non-zero `GlowRadius`, a non-zero intensity, and a `GlowColor` carrying alpha before anything is drawn at all; values above 1 widen the solid core of the halo, which reads as bloom without a post-processing stack.

`public float GlowRadius`

:   How far the halo reaches beyond the silhouette, in reference pixels. The mesh is padded by this distance so the halo is not clipped by the quad, and the padding is excluded from layout, so a widget that glows still occupies exactly its RectTransform and does not push its neighbours around.

`public float GradientAngleDegrees`

:   Direction of a `SkinFillMode.LinearGradient` fill, in degrees anticlockwise from screen right: 0 runs `FillColor` to `FillColorSecondary` left to right, 90 runs bottom to top. The flat and radial modes ignore it.

`public Color ShadowColor`

:   Drop-shadow colour. Its alpha both gates and scales the shadow: a fully transparent colour draws nothing whatever `ShadowRadius` and `ShadowOffset` say, and it is also what stops a shadowless surface from paying for shadow padding.

`public Vector2 ShadowOffset`

:   Displacement of the shadow from the surface in reference pixels, with positive x to the right and positive y upward. The offset is added to `ShadowRadius` when the mesh is padded, so a far-thrown shadow is drawn in full rather than cut off at the quad edge.

`public float ShadowRadius`

:   Drop-shadow softness in reference pixels. Zero, or a fully transparent `ShadowColor`, draws no shadow.

`public SkinShape Shape`

:   The silhouette every part of the surface is measured against: fill, stroke, glow, and shadow all follow it. The shape is cut from a signed distance field inside the shader rather than built from geometry, so switching shapes costs no extra vertices and needs no sprite or mask.

`public Color StrokeColor`

:   Border colour. It is drawn over the fill as a band hugging the inside of the silhouette, and it is not masked by a partial fill, so a bar built on a stroked surface keeps a complete outline however low its value runs.

`public float StrokeWidth`

:   Border thickness in reference pixels, drawn inside the silhouette so it never enlarges the surface. Zero, or a fully transparent `StrokeColor`, draws no border.

**Methods**

`public static SkinSurfaceTokens Flat(Color fill, float cornerRadius = 0f)`

:   A flat, strokeless, glowless surface in `fill`.
    - `cornerRadius` &mdash; Corner radius in reference pixels; zero gives square corners.
    - `fill` &mdash; Single color assigned to both surface gradient stops.
    - **Returns** &mdash; A rounded-rect surface with no stroke, glow, or shadow, ready to be built on.

`public SkinSurfaceTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy; this instance is unchanged. `GradientAngleDegrees` wraps into 0..360 rather than clamping, and the colours are left exactly as authored.

`public SkinSurfaceTokens WithFill(Color fill)`

:   Returns this surface with its fill replaced by `fill`.
    - `fill` &mdash; Replacement color written to both gradient stops on the returned copy.
    - **Returns** &mdash; A copy with both gradient stops set to `fill`, so a gradient surface reads as flat until a second stop is set again.

`public SkinSurfaceTokens WithGlow(Color color, float radius, float intensity)`

:   Returns this surface with its glow replaced.
    - `radius` &mdash; Glow radius in reference pixels, measured outward from the silhouette.
    - `intensity` &mdash; Glow strength; above 1 the halo reads as bloom.
    - `color` &mdash; Replacement outer-glow color on the returned token copy.
    - **Returns** &mdash; A copy carrying the new glow. The values are stored as given, so call `Sanitized` if they came from outside the supported ranges.

---

## SkinTargetingTokens

```csharp
public struct SkinTargetingTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

How a target pick is expressed. Two fields, because the interesting
decision is not which of the four presets to use - it is whether to let the
package pick for you.

None of this changes what is legal. Legality stays with the resolver, so a
project can swap presets, or hand the choice to its players as an
accessibility setting, without touching content or invalidating a replay.

**Fields**

`public bool AdaptToDevice`

:   Move to the preset the device and party size call for. A preset that adapts is worth more on a store page than four a buyer has to configure. Off honours `Preset` verbatim, which is what a project with one target platform wants.

`public TargetingPreset Preset`

:   The preset a pick is expressed with. With `AdaptToDevice` on this is the starting point rather than the last word.

**Methods**

`public static SkinTargetingTokens Default()`

:   The shipped default: reticle, adapting to the device.
    - **Returns** &mdash; Reticle with adaptation enabled.

---

## SkinTypographyTokens

```csharp
public struct SkinTypographyTokens
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Skin/BattleSkinTokens.cs</small>

Type sizing and treatment. Fonts stay optional so no font is redistributed.

**Fields**

`public int BodySize`

:   Size of the interface's ordinary text: roster names, skill names, and the tooltip's damage preview.

`public int CaptionSize`

:   Size of small supporting text, and the busiest of the three sizes: it covers combatant plates, bar readouts, log lines, timeline entries, and tooltip cost and timing rows. Several regions derive their row heights from it, so raising it grows those rows rather than overflowing them.

`public TMP_FontAsset Font`

:   Optional font. Left empty, the skin falls back to Unity's built-in runtime font, so a skin never depends on a font asset the package would have to redistribute.

`public int HeadingSize`

:   Size of titles. The result banner scales it up further for its headline, so a large value here grows the end-of-battle text faster than it grows a tooltip title.

`public int LabelSize`

:   Size of a tracked, uppercase label: ACTING, TARGET, NOW, CAST, and the card footers. These are read as shapes rather than as words, so they sit between caption and heading and are always drawn with letter spacing. Zero means "derive": the size settles midway between `BodySize` and `HeadingSize`, so a skin authored before this token existed still gets a sensible value rather than the minimum.

`public float LineSpacing`

:   Multiplies the gap between lines of a wrapped label. Most HUD text is a single line, so this mainly affects the feedback log and tooltip body.

`public int NameSize`

:   Size of a combatant's name on the stage nameplate. It is the largest type a player reads mid-turn without stopping, so it is deliberately a step above `BodySize` rather than sharing it. Zero derives it from `HeadingSize`.

`public Color OutlineColor`

:   Colour of that outline. It is read only while `UseOutline` is set, and it should oppose the text colour rather than match the panel behind it: the shipped dark skins outline in black, the neon skin in its own near-black backdrop colour.

`public int TitleSize`

:   Size of the skill announcement banner that crosses the stage on perform. It is display type: it exists to be seen from across a room for half a second, not to be read carefully. Zero derives it from `HeadingSize`.

`public bool UseOutline`

:   Adds a one-pixel contrast outline to every label the skin builds, which is what keeps text readable where it sits directly over the stage. The outline is attached when a label is created, so a skin swapped at runtime applies it on the rebuild rather than to labels already on screen. The two light shipped skins leave it off; their text is already dark against pale panels.

**Methods**

`public SkinTypographyTokens Sanitized()`

:   Clamps every token into its supported range.
    - **Returns** &mdash; A clamped copy; this instance is unchanged. `Font`, `UseOutline`, and `OutlineColor` are left as authored.

---

