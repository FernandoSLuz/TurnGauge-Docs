# Stage and tokens

24 types in this area.

!!! abstract "On this page"
    [BattlePresenter](#battlepresenter) &middot; [BattleStage2D](#battlestage2d) &middot; [BattleStageBackdrop](#battlestagebackdrop) &middot; [BattleStageBloom](#battlestagebloom) &middot; [BattleStageFrame](#battlestageframe) &middot; [BattleStageInformationBank](#battlestageinformationbank) &middot; [BattleStageInformationBankSide](#battlestageinformationbankside) &middot; [BattleStageInformationBanks](#battlestageinformationbanks) &middot; [BattleStageInformationEntry](#battlestageinformationentry) &middot; [BattleStageInformationSide](#battlestageinformationside) &middot; [BeatDeriver](#beatderiver) &middot; [CombatantTokenView](#combatanttokenview) &middot; [PresentationBeat](#presentationbeat) &middot; [PresentationBeatContext](#presentationbeatcontext) &middot; [PresentationStagePreset](#presentationstagepreset) &middot; [PresenterBinding](#presenterbinding) &middot; [StageAnimationBinding](#stageanimationbinding) &middot; [StageAnimationSource](#stageanimationsource) &middot; [StageAudioBinding](#stageaudiobinding) &middot; [StageFrameMode](#stageframemode) &middot; [StagePresentationPlayback](#stagepresentationplayback) &middot; [StageVfxBinding](#stagevfxbinding) &middot; [TargetPreviewView](#targetpreviewview) &middot; [TargetingReticleView](#targetingreticleview)

## BattlePresenter

**Start here**

```csharp
public sealed class BattlePresenter : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattlePresenter.cs</small>

The pure presentation consumer. It owns a FIFO of presentation beats
derived deterministically from engine events and drives the visual
adapters, stage, and optional UI from supplied immutable values only. It
never calls `Submit`, `StepEvent`, `StepAction`,
`AdvanceTicks`, `RunUntilBoundary`, a forecast, or RNG, and it
holds no `BattleEngine`. Beat timing, speed, skipping, and pausing
affect visuals only, so presentation can never change a state hash, an
event chain, a replay, or a result.

**Properties**

`public int ActiveFloatingNumberCount`

:   Floating numbers currently on the stage, including ones still playing out their rise. Each returns to the pool as it finishes, and the oldest is retired early rather than exceeding `MaximumFloatingNumbers`.

`public Action CameraShakeCallback`

:   Optional camera-shake sink; visual only, never authoritative.

`public int CameraShakeRequestCount`

:   Camera shakes requested since `Bind`. Counted whether or not `CameraShakeCallback` is set.

`public int ForcedInstantBeatCount`

:   Beats that were finished instantly because the queue had already reached `MaximumQueuedBeats`. A non-zero count means visuals were compressed to keep up, never that the battle changed. Cleared by `Bind`.

`public bool IsIdle`

:   True when no beat is playing and none are queued, so the visuals have caught up with every event handed in so far.

`public IList<IPerformBeatModule> PerformModules`

:   The perform modules driving the moment a skill lands, run in list order as each phase begins. This is the seam the shipped effects are built on and the one a project extends: add a module, drop one, reorder them, or replace the set entirely. The presenter contains anything a module throws, so a project's own module cannot stop a battle from playing. The list starts empty and, unless the built-in perform feel is switched off in the inspector, the shipped set is installed on the first tick. Registering your own modules before then keeps them, and their order, exactly as you built them: only a kind that is missing is added.

`public StableId PlayerTeamId`

:   The team treated as the player's for ally/enemy tinting. Presentation only. Left unset, the first team in the compiled layout is used, which matches how the shipped encounters order their teams.

`public int QueuedBeatCount`

:   Beats waiting behind the one currently playing. It never passes `MaximumQueuedBeats`, because reaching that cap completes the oldest beat instantly to make room, so a count that sits near the cap means the visuals are trailing the engine rather than that events are being lost.

`public bool ReduceMotion`

:   Whether the session or its skin currently reduces presentation motion.

`public float Speed`

:   Presentation-only playback speed multiplier (visual). A negative value clamps to zero, which freezes the visuals rather than reversing them.

`public BattleStage2D Stage`

:   The stage this presenter created and owns, or null until `Bind` has run.

`public Rect StageWorldRect`

:   Where the stage lands in world space, in units, for the current viewport and scale. Tokens are placed in world space directly rather than under this transform, so a camera framed on this rectangle sees the whole formation wherever the presenter object itself sits. The setup wizard frames the scene camera from this value, so the framing is authored here rather than copied by hand into a scene.

`public float UnitsPerPixel`

:   World units per stage pixel, falling back to `DefaultUnitsPerPixel` when the serialized value is zero or negative, which is the coercion `BattleStage2D.Build` applies anyway.

`public FormationViewport Viewport`

:   The pixel rectangle the formation is projected into, read straight from the serialized stage fields. `SetViewport` writes those fields, so a `BattleStageFrame` that reframes the stage at runtime shows up in the inspector instead of hiding behind it.

**Fields**

`public const float DefaultUnitsPerPixel`

:   World units one stage pixel is worth when the serialized scale is left at zero or below. It repeats `BattleStage2D.Build`'s own fallback so a presenter nobody has touched frames exactly as before.

`public const int MaximumFloatingNumbers`

:   Section 10 cap: floating numbers concurrently visible.

`public const int MaximumQueuedBeats`

:   Section 10 cap: queued beats per presenter.

**Methods**

`public void AdoptSnapshot(BattleSnapshot snapshot)`

:   Adopts an authoritative snapshot for resync/skip and display.

    - `snapshot` &mdash; State to mirror onto the stage and HUD. It is read, never advanced or mutated; a null snapshot is accepted and updates nothing.

`public void Bind(PresenterBinding presenterBinding)`

:   Rebuilds the stage from an explicit binding and reconnects its optional interactive HUD. Clears queued visual beats and resets playback without changing the simulation.

    - `presenterBinding` &mdash; Required compiled content, layout, recipes, adapters, pool, labels and optional UI. Retained until the next binding; null throws.

`public void ConfigureStageFeel(PerformFeelPreset feel)`

:   Chooses the profile's fallback feel. An explicit inspector preset or host-installed module keeps precedence. Only automatically installed modules are replaced; their camera and body offsets reset first.

    - `feel` &mdash; Session-owned fallback feel; null returns to the presenter's default policy.

`public void EnqueueEvents(IReadOnlyList<BattleEvent> events)`

:   Derives and enqueues one beat per event (host step result).

    - `events` &mdash; Events from one engine step, in the order the engine produced them. A null list, and any null entry, is skipped. Once the queue reaches `MaximumQueuedBeats` the oldest beat is completed instantly to make room instead of being dropped, which increments `ForcedInstantBeatCount`.

`public int InstallBuiltInPerformModules(PerformFeelPreset feel, Camera camera, SkillTitleView titleView)`

:   Registers the shipped perform moment in one call: the skill title announcement, the focus pull, the body shake, and - when a camera is supplied - the camera shake and push-in, plus the bloom, vignette, and backdrop blur for whichever of those optional components the camera carries. This is the wiring the demo scene does by hand, offered as one line so a battle assembled from the shipped facade does not read flatter than the demo a buyer watched before purchasing. It adds only modules of a kind that is not registered yet, so calling it twice, or calling it after adding a module of your own, cannot double an effect. The first tick calls it for you with the serialized feel, camera, and no card, so calling it explicitly is only needed to pass a different preset, a different camera, or a card of your own. `PerformModules` stays open afterwards: drop one, reorder them, or add your own alongside.

    - `feel` &mdash; How hard the moment hits. Null uses the shipped defaults rather than zeroes, so the effects are visible without an asset being authored.
    - `camera` &mdash; The camera the shake and the push-in drive. Null registers the modules that need no camera and skips the rest.
    - `titleView` &mdash; The card the skill name is announced on. Null builds one over the bound interface, and skips the announcement when there is no interface to build it on.
    - **Returns** &mdash; How many modules were added.

`public void RebindEffects(PresentationRecipeSet recipes, IAnimationAdapter animation, IVfxAdapter vfx, IAudioAdapter audio, PresentationLog log = null)`

:   Replaces visual recipes and effect adapters without rebuilding the stage or HUD. Pending old effects are cancelled, not replayed. The snapshot, interactive subscriptions, selection and pool stay intact.

    - `recipes` &mdash; Replacement visual recipe set; must satisfy PresenterBinding's content contract.
    - `animation` &mdash; Adapter receiving animation keys from future phases.
    - `vfx` &mdash; Adapter receiving effect keys and participant anchors from future phases.
    - `audio` &mdash; Adapter receiving one-shot sound keys from future phases.
    - `log` &mdash; Replacement warning log, or null to retain the current binding's log.

`public void ResetPerformModules()`

:   Puts every module's effect back. Called on teardown and whenever playback is skipped, because a module that has dimmed the stage or moved the camera would otherwise leave it that way.

`public void SetCombatantArt(StableId combatantId, Sprite art)`

:   Gives one combatant its illustration, on the stage and on the rail at once. Existing source-facing metadata is preserved. Newly configured tokens default to right-facing source art; use the explicit overload when the imported illustration points elsewhere.

    - `combatantId` &mdash; The combatant to dress. Unknown ids are ignored.
    - `art` &mdash; The illustration, or null to strip it back to the lettered fallback. The same sprite becomes the bust crop on that combatant's turn-order chip, so a project assigns art once rather than twice.

`public void SetCombatantArt(StableId combatantId, Sprite art, FormationFacing sourceArtFacing)`

:   Gives a combatant art whose source orientation is supplied by the project. The direction is retained by the token and shared with the turn-order portrait, so stage art and the legacy rail never acquire independent mirror rules.

    - `combatantId` &mdash; The combatant to dress.
    - `art` &mdash; The source illustration, or null to clear it.
    - `sourceArtFacing` &mdash; Direction encoded by the unmirrored source sprite.

`public void SetCombatantArt(StableId combatantId, Sprite bodyArt, FormationFacing sourceArtFacing, Sprite portraitSprite, UiPortraitCrop portraitCrop)`

:   Assigns body art and an optional independent rail portrait crop.

    - `combatantId` &mdash; Combatant to dress.
    - `bodyArt` &mdash; Stage sprite, preserving the body's ground anchor.
    - `sourceArtFacing` &mdash; Direction encoded by the stage sprite.
    - `portraitSprite` &mdash; Optional independent rail sprite; body art is reused when null.
    - `portraitCrop` &mdash; Finite normalized crop, or default for exact legacy framing.

`public void SetReducedMotion(bool value)`

:   Applies a session preference to beats, stage and numbers without changing skin assets or battle state. A custom HUD applies its own matching policy. Existing perform modules reset when reduction is enabled. Effects already started outside those modules remain the host's responsibility.

    - `value` &mdash; Session preference, combined with the authored skin preference.

`public void SetViewport(FormationViewport value)`

:   Sets the stage viewport; rebuilds the stage when bound.

    - `value` &mdash; Pixel rectangle the formation is projected into. Written to the serialized stage fields even when the presenter is not bound yet, so the next `Bind` uses it and the inspector shows it.

`public void SkipAll()`

:   Finishes every queued beat immediately (visuals only).

`public void Teardown()`

:   Releases pooled instances and clears playback state.

`public void Tick(float presentationDeltaSeconds)`

:   Advances beats and adapters by presentation delta seconds.

    - `presentationDeltaSeconds` &mdash; Elapsed seconds, unscaled: `Speed` is applied on top, so a host passes its frame delta straight in. Zero or less does nothing, which is how a host implements pause.

`public void Tick(float presentationDeltaSeconds, bool reduceMotion)`

:   Advances visual beat playback using the current speed and motion preference. An unbound, paused or nonpositive-delta call leaves playback and the motion preference unchanged; simulation time is never advanced here.

    - `presentationDeltaSeconds` &mdash; Elapsed seconds, unscaled. Zero or less, or a zero `Speed`, preserves pause.
    - `reduceMotion` &mdash; Whether to compress beats, suppress new decorative effects and keep stage feedback static.

---

## BattleStage2D

```csharp
public sealed class BattleStage2D : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStage2D.cs</small>

A neutral 2D battle stage. It maps normalized formation space to stage
space with the documented aspect-fit rule by reusing
`FormationLayoutCompiler.Project`, spawns one
`CombatantTokenView` per compiled occupancy through the pool
adapter, and resolves slot/approach/anchor positions for beats. No
transform ever feeds back into anything authoritative.

**Properties**

`public int DepthRankCount`

:   How many distinct depth ranks the last `Build` found. One means a flat arrangement, which is a legitimate answer and the reason nothing scales or fades on a rank formation.

`public Func<object, bool> OwnsPointerSurface`

:   Optional identity filter for UI surfaces already covered by PointerBlocked. Other interfaces keep their normal raycast blocking.

`public Camera PickCamera`

:   The camera clicks are unprojected through. Left unset, the stage uses `Camera.main`, which is what the shipped setups have.

`public IReadOnlyDictionary<StableId, StageTokenPlacement> Placements`

:   Every token the last `Build` produced, keyed by combatant. Each entry carries the projected slot and approach points along with the slot's facing and sorting data, so a caller can read where a combatant stands without going through its transform.

`public Func<Vector2, bool> PointerBlocked`

:   Optional host screen-space HUD hit-test evaluated before stage picking. Binding a presenter preserves this callback.

`public int TokenCount`

:   How many tokens are currently spawned. It can be lower than the layout's occupancy count without that being an error: a team whose formation fails to project is skipped with a warning, while an occupancy whose slot is missing from the preset or whose pool returns nothing is skipped silently.

`public float TokenPickRadiusPixels`

:   How near a click has to land, in formation pixels, before it counts as hitting a combatant. It is measured against the token's slot point, so it is a radius around where the combatant stands rather than the bounds of whatever art is on top of it.

`public bool TokenPickingEnabled`

:   Whether the stage watches for clicks on its tokens at all. Turn it off for a project that reads its own input; with no listener attached the watch already costs nothing.

`public float TokenScale`

:   How far combatant art is scaled to fit the stage it was given. Art has a fixed world size, so a stage smaller than the box it was drawn for does not shrink it - the combatants simply run off the edges, which is what a 3v3 of painted characters did in portrait. Scaling by the tighter of the two axes keeps a whole formation on the stage at any shape without re-authoring a single slot, and leaves the authoring reference untouched at exactly 1.

`public IReadOnlyDictionary<StableId, CombatantTokenView> Tokens`

:   Every spawned token by combatant id, for a caller that has to walk the whole field rather than look one combatant up. Read only, and the instances belong to the pool: reposition or tint one and you must put it back, because the stage will not recompute it.

`public float UnitsPerPixel`

:   World units one projected formation pixel is worth on this stage. Exposed because anything drawn against a combatant -- a targeting cursor, a host's own marker -- has to be sized in the same currency the stage placed that combatant in, and guessing it produces a widget that looks right at one resolution only.

`public FormationViewport Viewport`

:   The viewport the current layout was projected against, as handed to `Build`. Nothing re-projects on its own, so a change of screen size means building again.

**Fields**

`public const int BackdropSortingOrder`

:   Sorting order the stage backdrop is drawn at, far below any token.

`public const float RankGroupingFraction`

:   How far apart two ground lines have to be, as a fraction of the projected stage height, before they count as different depth ranks. Some slack is required rather than optional: a formation's seats are authored in integer normalized space and then projected through an aspect fit, so two seats meant to share a ground line arrive a fraction of a pixel apart and would otherwise be staged as two ranks with an invisible size difference between them.

`public const float ReferenceStageHeight`

:   Height of that same authoring box.

`public const float ReferenceStageWidth`

:   The stage box combatant art is authored against, in projection pixels: a 1920-wide screen with the shipped bands taken off the top and bottom.

`public const string TokenPoolKey`

:   Pool key used for spawned combatant tokens when no per-combatant prototype has been registered. One prototype under this key serves every combatant.

**Events**

`public event Action<StableId> TokenClicked`

:   Raised when the player clicks a combatant on the stage. It is a report, not a command: the stage never decides what a click means, which is what lets the same click pick a target, open an inspector, or do nothing at all depending on who is listening.

**Methods**

`public void Build(CompiledEncounterFormationLayout layout, IPoolAdapter pool, FormationViewport viewport, PresentationLog log = null, float unitsPerPixel = 0.01f)`

:   Projects the layout at `viewport` and spawns the token set. Explicit; the stage never scans the scene.

    - `layout` &mdash; Compiled team formations and combatant-to-slot occupancies to project and spawn.
    - `log` &mdash; Optional log-once ledger for projection or missing-art warnings.
    - `pool` &mdash; Instance pool supplying shared or combatant-specific token objects.
    - `unitsPerPixel` &mdash; Positive conversion from projected formation pixels to Unity world units; invalid values use 0.01.
    - `viewport` &mdash; Integer projection rectangle applied independently to each team preset.

`public void Clear()`

:   Releases every token back to the pool and clears state.

`public bool IsPointerOccluded(Vector2 screenPoint)`

:   Tests semantic HUD occlusion and raycasts from other UI surfaces.

    - `screenPoint` &mdash; Pointer position in screen pixels supplied to host/native hit tests and the current EventSystem.
    - **Returns** &mdash; True when either semantic blocker accepts the point or an unowned UI raycast hit remains; false when no surface blocks stage picking.

`public void SetPresentation(CompiledBattleSkin battleSkin, DisplayStringTable labelTable, StableId allyTeamId)`

:   Supplies the skin and label table used to dress spawned tokens with nameplates, bars, and status pips. Call before `Build`. Optional: without it tokens still mirror state onto their properties, which is what the headless tests assert against.

    - `allyTeamId` &mdash; Team identity whose spawned token plates receive the ally tint.
    - `battleSkin` &mdash; Compiled skin used to build token plates; null leaves tokens headless.
    - `labelTable` &mdash; Combatant ID labels used on token plates; null selects an empty table.

`public void Tick(float presentationDeltaSeconds)`

:   Advances token plate animation by a visual delta.

    - `presentationDeltaSeconds` &mdash; Positive presentation-clock duration forwarded to every spawned token plate.

`public static string TokenPoolKeyFor(StableId combatantId)`

:   The pool key that gives one combatant its own body: `presentation.token.`. Register a prototype under this key and that combatant spawns from it; register nothing and it falls back to `TokenPoolKey`, so a project can give art to some combatants and not others. The stage only looks for the specific key when the pool can be asked whether it holds one, because `IPoolAdapter.Acquire` is allowed to fabricate an empty instance for an unknown key rather than returning null, and a fallback built on null would silently spawn blank tokens instead.

    - `combatantId` &mdash; The combatant whose prototype is wanted.
    - **Returns** &mdash; `presentation.token.` for exact prototype registration.

`public bool TryGetAnchorWorld(StableId combatantId, PresentationVfxAnchorKind kind, StableId? anchorId, out Vector3 world)`

:   Resolves a beat anchor to stage space for a combatant.

    - `anchorId` &mdash; Named VFX anchor when `kind` is Anchor; otherwise ignored.
    - `combatantId` &mdash; Spawned combatant whose compiled placement supplies the handle.
    - `kind` &mdash; Standing slot, approach point, or named anchor to resolve.
    - `world` &mdash; Receives the projected handle converted to stage-world units, or zero on failure.
    - **Returns** &mdash; True when the operation succeeds; otherwise false.

`public bool TryGetToken(StableId combatantId, out CombatantTokenView token)`

:   Returns the spawned token for a combatant, if present.

    - `combatantId` &mdash; Combatant identity used as the stage token dictionary key.
    - `token` &mdash; Receives the active pooled token view, or null when the combatant was not spawned.
    - **Returns** &mdash; True when the operation succeeds; otherwise false.

`public bool TryPickTokenAtScreen(Vector2 screenPoint, Camera camera, out StableId combatantId)`

:   Projects a pointer through `camera` and picks the nearest token on the stage plane. Input-system integrations can call this directly without depending on TurnGauge input packages.

    - `screenPoint` &mdash; Screen-space pointer position in pixels.
    - `camera` &mdash; Camera that produced the screen point.
    - `combatantId` &mdash; Picked combatant, or the default id.
    - **Returns** &mdash; True when the pointer reaches a token.

`public bool TryPickTokenAtWorld(Vector3 worldPoint, out StableId combatantId)`

:   Finds the combatant standing nearest a point on the stage.

    - `worldPoint` &mdash; The point to test, in world space, and only its x and y are read. Tokens are placed at world positions rather than under this transform, so this is measured against those positions directly.
    - `combatantId` &mdash; The combatant found, or the default id when none is near enough.
    - **Returns** &mdash; True when a combatant stands within `TokenPickRadiusPixels` of the point. Ties resolve to the lowest id so the same click always picks the same combatant.

`public bool TryProjectScreenToStage(Vector2 screenPoint, Camera camera, out Vector3 worldPoint)`

:   Projects one screen point onto the world-space stage plane at z = 0. A ray/plane intersection works for orthographic and perspective cameras, including cameras rotated away from the world z axis.

    - `screenPoint` &mdash; Screen-space pointer position in pixels.
    - `camera` &mdash; Camera that produced the screen point.
    - `worldPoint` &mdash; Intersection on the stage plane.
    - **Returns** &mdash; True when the camera ray reaches the stage plane.

`public void UpdateFromSnapshot(BattleSnapshot snapshot)`

:   Mirrors current snapshot state onto every token.

    - `snapshot` &mdash; Authoritative snapshot supplying health, shields, statuses, and death state for each spawned combatant.

---

## BattleStageBackdrop

```csharp
public sealed class BattleStageBackdrop : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageBackdrop.cs</small>

Optional background blur for the perform moment. **Off by default and never required.**

While a skill performs, everything behind the battle stage softens so the eye stays on
the participants. The shipped `FocusPerformModule` does the same job by
tinting non-participants, which costs nothing and works everywhere; this is the richer
alternative for a project that wants the background itself to go out of focus.

It renders the scene a second time, without TurnGauge's own content, into a
half-resolution RenderTexture, softens that through bilinear blits, and shows the
result on a quad behind the stage. This uses a secondary camera rather than
`OnRenderImage`; verify capture and blit behavior in your project's render pipeline.

**Only the background is blurred.** The capture hides the stage tokens and the battle
interface for the duration of its own render, so the participants are never in the
blurred image and never ghost behind their sharp selves.

The blur is live rather than a snapshot: it is re-rendered each frame while
`Strength` is above zero, so anything still moving behind the wash stays
readable. At zero it releases everything it allocated and costs nothing at all.

To enable: add it to the battle camera. Drive `Strength` yourself, or
register a `BackdropBlurPerformModule` to have it ride the perform beat.

**Properties**

`public bool IsActive`

:   True once the capture camera and its buffers exist.

`public float Strength`

:   How far out of focus the background is, 0 to 1. Zero tears the whole effect down. Writable so a perform module can pull focus on impact and ease it back. Values outside the range clamp rather than doing something surprising.

---

## BattleStageBloom

```csharp
public sealed class BattleStageBloom : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageBloom.cs</small>

Optional stage bloom and vignette. **Off by default and never required.**

The shipped look needs no post-processing: glow is drawn inside the
skinned-surface shader. That is why TurnGauge depends on no
post-processing package at all, and why a buyer's existing volumes,
renderer features, and profiles cannot conflict with it.

This component exists only for buyers who want a softer bloom across the
whole stage and are not already running their own post stack. It is a
self-contained image effect with no package dependency.

Built-in render pipeline only. Under URP or HDRP, `OnRenderImage` is
never called, so rather than silently doing nothing this component detects
the active pipeline, logs one explanatory warning, and disables itself.
Use that pipeline's own Bloom volume override instead.

To enable: add it to the battle camera and tick `Enabled`. Nothing in
the package adds it for you.

**Properties**

`public float Intensity`

:   Bloom strength added over the stage. Zero skips the bloom pass entirely and blits the frame through unchanged. Writable so a perform module can pulse it on impact and ease it back to the authored resting value. Negative values clamp to zero rather than inverting the effect.

`public bool IsSupportedPipeline`

:   True when this effect can run in the active pipeline.

`public float VignetteStrength`

:   Corner darkening strength, 0 to 1. Zero skips the vignette. Writable for the same reason `Intensity` is: a perform module can close the frame in on impact and ease it back to the authored resting value. Independent of the bloom -- a vignette with `Intensity` at zero draws the vignette and no bloom.

**Fields**

`public const string ShaderName`

:   Name of the optional bloom shader.

`public const string ShaderResourcePath`

:   Resources path of the optional bloom shader.

---

## BattleStageFrame

```csharp
public sealed class BattleStageFrame : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageFrame.cs</small>

Controls where the battle stage sits on screen and how large it is.

Without this, the stage was pinned to a hardcoded 1920x1080 viewport, so on
any other resolution the formation was cropped or floated in dead space,
and a buyer had no supported way to reserve screen area for their own
interface. Every value here is presentation-only: moving or resizing the
stage cannot change a state hash, an event chain, or a result.

Attach next to a `BattlePresenter`; it re-applies the viewport
whenever the screen, safe area, or any field changes.

**Properties**

`public FormationViewport AppliedViewport`

:   The viewport most recently pushed to the presenter.

**Methods**

`public void ApplyNow()`

:   Recomputes and applies the stage viewport. Cheap to call repeatedly: when the result matches the viewport already applied, the presenter is not touched at all. Screen and safe-area changes trigger this automatically, so an explicit call is only needed to force a re-frame.

`public FormationViewport Resolve(int screenWidth, int screenHeight, Rect safeAreaPixels)`

:   Computes the stage viewport for a screen. Public and parameterised so EditMode tests can verify every mode and margin without a device. Pure: it reads the serialized fields but applies nothing to the presenter.

    - `screenWidth` &mdash; Screen width in pixels. Outside Explicit mode, a non-positive value falls back to a 1x1 viewport rather than throwing.
    - `screenHeight` &mdash; Screen height in pixels, treated as `screenWidth` is.
    - `safeAreaPixels` &mdash; The device safe area in pixels. Ignored unless the safe-area option is on, and ignored when its width or height is not positive, so passing a default Rect is a valid way to ask for the full screen.
    - **Returns** &mdash; The stage rectangle in pixels with a bottom-left origin, never smaller than 1x1. In Explicit mode the screen arguments are ignored entirely.

`public void SetInterfaceLayout(IBattleStageLayout layout)`

:   Binds an optional native/custom view's stage reservation. Null restores legacy or host margins.

    - `layout` &mdash; View supplying normalized stage bounds, or null to restore the configured margin policy. The viewport is refreshed immediately.

`public void SetMode(StageFrameMode value)`

:   Sets the framing mode and re-frames immediately. Exists because a scene that builds its presenter at runtime, as the runtime demo does, has no inspector to set this in. `StageFrameMode.FullScreen` is what gives a wider screen more stage instead of wider empty gutters.

    - `value` &mdash; How the stage rectangle is derived from the screen.

---

## BattleStageInformationBank

```csharp
public sealed class BattleStageInformationBank
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageInformationBanks.cs</small>

A side rail. Entries are never discarded when the pilot capacity is exceeded.

**Properties**

`public bool CapacityExceeded`

:   Whether the retained entries exceed the visible three-row capacity.

`public IReadOnlyList<BattleStageInformationEntry> Entries`

:   All entries retained for the side, including overflow entries.

`public BattleStageInformationBankSide Side`

:   Rail side represented by this bank.

---

## BattleStageInformationBankSide

```csharp
public enum BattleStageInformationBankSide
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageInformationBanks.cs</small>

Which side of the information rail receives a team.

| Value | Meaning |
| --- | --- |
| `Left` | Left information rail. |
| `Right` | Right information rail. |

---

## BattleStageInformationBanks

```csharp
public sealed class BattleStageInformationBanks : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageInformationBanks.cs</small>

Optional, renderer-independent composition information for the two side
rails. It is inert until a presenter calls `Configure`.

**Properties**

`public IReadOnlyList<string> Diagnostics`

:   Layout diagnostics produced while rebuilding the banks.

`public bool IsConfigured`

:   Whether a stage has been configured for the banks.

`public BattleStageInformationBank Left`

:   Current left-side bank, or an empty bank after clearing.

`public BattleStageInformationBank Right`

:   Current right-side bank, or an empty bank after clearing.

**Fields**

`public const int BackingHorizontalExpansionPixels`

:   Horizontal backing expansion reserved around a cell.

`public const int BackingVerticalExpansionPixels`

:   Vertical backing expansion reserved around a cell.

`public const int CellPixels`

:   Authored side-cell size in pixels.

`public const int ContentHeightPixels`

:   Content height remaining inside a side-cell backing.

`public const int ContentWidthPixels`

:   Content width remaining inside a side-cell backing.

`public const int FirstTopPixels`

:   Top offset of the first rail row in full-HUD pixels.

`public const int MinimumHudWidthPixels`

:   Minimum full-HUD width that keeps both side rails readable.

`public const int RailLeftPixels`

:   Left rail inset from the full-HUD left edge in pixels.

`public const int RailRightPixels`

:   Right rail reference position in the default 1920-pixel HUD.

`public const int RailWidthPixels`

:   Authored width of each side rail in pixels.

`public const int RowStepPixels`

:   Vertical step between rail rows in full-HUD pixels.

`public const int RowsPerSide`

:   Maximum number of visible pilot rows per side.

**Methods**

`public void Clear()`

:   Clears the optional seam and all derived entries.

`public void Configure(BattleStage2D source, int fullHudWidthPixels, int fullHudHeightPixels, float pixelUnits, StableId playerTeam)`

:   Builds the pilot rail from a stage. The player identity is compared as data; no team display name or ordering convention is inferred.

    - `source` &mdash; Stage whose current placements populate the banks.
    - `fullHudWidthPixels` &mdash; Full-HUD width in pixels.
    - `fullHudHeightPixels` &mdash; Full-HUD height in pixels.
    - `pixelUnits` &mdash; World units represented by one authored pixel.
    - `playerTeam` &mdash; Team identity used by the default side mapping.

`public void Configure(BattleStage2D source, int fullHudWidthPixels, int fullHudHeightPixels, float pixelUnits, StableId playerTeam, IReadOnlyList<BattleStageInformationSide> sides)`

:   Builds the rail with explicit team-to-side identities.

    - `source` &mdash; Stage whose current placements populate the banks.
    - `fullHudWidthPixels` &mdash; Full-HUD width in pixels.
    - `fullHudHeightPixels` &mdash; Full-HUD height in pixels.
    - `pixelUnits` &mdash; World units represented by one authored pixel.
    - `playerTeam` &mdash; Team identity used when an explicit mapping is absent.
    - `sides` &mdash; Optional explicit team-to-side assignments.

`public static RectInt PilotCell(int fullHudHeightPixels, BattleStageInformationBankSide side, int row)`

:   Returns one pilot cell in full-HUD pixel coordinates.

    - `fullHudHeightPixels` &mdash; Full-HUD height in pixels.
    - `side` &mdash; Rail side for the cell.
    - `row` &mdash; Zero-based visible rail row.
    - **Returns** &mdash; The full-HUD rectangle assigned to the requested cell.

`public static RectInt PilotCell(int fullHudWidthPixels, int fullHudHeightPixels, BattleStageInformationBankSide side, int row)`

:   Returns one pilot cell in full-HUD pixel coordinates.

    - `fullHudWidthPixels` &mdash; Full-HUD width in pixels.
    - `fullHudHeightPixels` &mdash; Full-HUD height in pixels.
    - `side` &mdash; Rail side for the cell.
    - `row` &mdash; Zero-based visible rail row.
    - **Returns** &mdash; The full-HUD rectangle assigned to the requested cell.

`public void SetSelection(StableId actor, IReadOnlyList<StableId> targets)`

:   Marks the actor and selected targets for a legible plate highlight.

    - `actor` &mdash; Current actor identity.
    - `targets` &mdash; Current target identities, or null for no targets.

---

## BattleStageInformationEntry

```csharp
public readonly struct BattleStageInformationEntry
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageInformationBanks.cs</small>

One combatant retained by a side bank, including overflow entries.

**Constructors**

`public BattleStageInformationEntry(StableId combatantId, StableId teamId, ProjectedFormationPoint projected, BattleStageInformationBankSide side, RectInt cell, bool hasCell, Vector2 worldPosition, bool isActor, bool isTarget)`

:   Initializes the retained rail entry with projected formation, cell and selection data.

    - `combatantId` &mdash; Combatant identity represented by the entry.
    - `teamId` &mdash; Team identity associated with the combatant.
    - `projected` &mdash; Projected formation information for the combatant.
    - `side` &mdash; Rail side containing the entry.
    - `cell` &mdash; Full-HUD pixel cell assigned to the entry.
    - `hasCell` &mdash; Whether the entry fits within the visible rail capacity.
    - `worldPosition` &mdash; World-space position corresponding to the assigned cell.
    - `isActor` &mdash; Whether the entry is the current actor.
    - `isTarget` &mdash; Whether the entry is one of the current targets.

**Properties**

`public RectInt Cell`

:   Full-HUD pixel cell assigned to the entry.

`public StableId CombatantId`

:   Combatant identity represented by the entry.

`public bool HasCell`

:   Whether the entry fits within the visible rail capacity.

`public bool IsActor`

:   Whether the entry is the current actor.

`public bool IsTarget`

:   Whether the entry is one of the current targets.

`public ProjectedFormationPoint Projected`

:   Projected formation information for the combatant.

`public BattleStageInformationBankSide Side`

:   Rail side containing the entry.

`public StableId TeamId`

:   Team identity associated with the combatant.

`public Vector2 WorldPosition`

:   World-space position corresponding to the assigned cell.

---

## BattleStageInformationSide

```csharp
public readonly struct BattleStageInformationSide
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageInformationBanks.cs</small>

Maps a caller-owned team identity to a rail side without naming assumptions.

**Constructors**

`public BattleStageInformationSide(StableId teamId, BattleStageInformationBankSide side)`

:   Creates an explicit team-to-rail assignment.

    - `teamId` &mdash; Team identity assigned to the rail.
    - `side` &mdash; Rail side that receives the team.

**Properties**

`public BattleStageInformationBankSide Side`

:   Rail side assigned to the team.

`public StableId TeamId`

:   Team identity assigned to the rail.

---

## BeatDeriver

```csharp
public static class BeatDeriver
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BeatDeriver.cs</small>

Pure event-to-beat derivation. Every gameplay event maps to exactly one
beat: the resolved recipe when one matches, otherwise an instant
no-visual beat. The deriver reads only the event's property set and the
supplied recipe set/catalog, performs no simulation math, and holds no
engine reference.

**Methods**

`public static PresentationBeatContext BuildContext(BattleEvent battleEvent)`

:   Extracts the beat context from an event's property set.

    - `battleEvent` &mdash; The event to read; only its typed properties are inspected.
    - **Returns** &mdash; The extracted context, or the default context when the event is null. Source falls back to the actor id, and amount to the actual delta when present, otherwise the plain amount; both are absent when untyped. The critical, shielded, and killing-blow flags read false unless the event says otherwise.

`public static PresentationBeat Derive(BattleEvent battleEvent, PresentationRecipeSet recipes, CompiledAuthoringCatalog catalog)`

:   Derives the single beat for one event (never null).

    - `battleEvent` &mdash; The gameplay event to map; null yields a default context.
    - `recipes` &mdash; The candidate recipe set searched for a match.
    - `catalog` &mdash; Compiled content supplying the skill/status tag tables that tag selectors match against.
    - **Returns** &mdash; A beat pairing the event's context with the winning recipe, or with a null recipe (an instant no-visual beat) when no recipe matches.

---

## CombatantTokenView

```csharp
public sealed class CombatantTokenView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/CombatantTokenView.cs</small>

A neutral 2D token view for one combatant. It mirrors compiled slot data
(facing, sorting) and snapshot/event state (health, shield, status pips,
death) onto an optional `SpriteRenderer` and, when a skin is
supplied, onto a `SkinnedTokenPlate` that draws those values.

It reads values only; it never computes or mutates anything authoritative.

**Properties**

`public ProjectedFormationPoint ApproachProjected`

:   The projected point a step-in should travel toward, in reference pixels. It is recorded but never used here; the token stays at `SlotProjected` unless the host animates it.

`public StableId CombatantId`

:   The combatant this token stands for, as given to `Configure`. It is the default id until the token has been configured, which matters for tokens taken from a pool.

`public int DepthRank`

:   How far back this combatant stands, 0 at the front. Ranks come from the formation's own ground lines rather than from anything authored here, so a flat arrangement leaves every token at 0 and nothing scales or fades.

`public float EffectiveArtScale`

:   The size this token is actually drawn at: the stage fit multiplied by its rank's share of `SkinStagePresenceTokens.RankScale`.

`public FormationFacing Facing`

:   The facing recorded from the compiled slot. The sprite is mirrored when this differs from the direction set by `SetSourceArtFacing`, so one sprite serves both sides of the field.

`public int Health`

:   Health from the last mirrored snapshot state. A null combatant passed to `ApplyState` leaves the previous value standing.

`public float HealthFraction`

:   Normalized health in [0,1] for a bar; 0 when max is unset.

`public bool IsDead`

:   Whether the mirrored state has stopped counting the combatant as living. This is what desaturates and fades the sprite; the token is never hidden or destroyed on death.

`public bool IsTargetCandidate`

:   Whether this combatant is a legal pick for the skill being aimed. True is the resting state, so a token that is never told about targeting is never dimmed. Set false and the token also stops accepting picks, because a body the player can click but not target is worse than one they cannot click at all.

`public int MaximumHealth`

:   The health ceiling from the last mirrored snapshot state, used by `HealthFraction`.

`public SkinnedTokenPlate Plate`

:   The plate drawing this token's values, or null when unskinned.

`public int ShieldAmount`

:   The shield total the plate draws. A negative amount handed to `ApplyState` is stored as zero, so the bar can never invert.

`public ProjectedFormationPoint SlotProjected`

:   The projected rest position in reference pixels, which `Configure` converts to world units and moves the token to.

`public StableId SortingLayerKey`

:   The sorting layer the caller asked for. It is recorded only: `Configure` never assigns a layer to the renderer, so a host that cares about layers has to apply this itself.

`public int SortingOrder`

:   Draw order within the sorting layer. Unlike `SortingLayerKey`, this is written straight onto the sprite renderer.

`public FormationFacing SourceArtFacing`

:   The direction in which the current source sprite is authored before the token mirrors it for its formation slot.

`public int StatusPipCount`

:   How many status pips to draw, clamped at zero the same way `ShieldAmount` is.

**Fields**

`public const int ContactShadowSortingOrder`

:   Sorting order every contact shadow is drawn at, before the token's own order is added to break ties between them. Well below any body and well above `BattleStage2D.BackdropSortingOrder`. A shadow ordered relative to its own combatant would be correct for that combatant and wrong for the stage: the front rank's shadow would fall across the feet of the rank behind it, which is the one place a contact shadow must never be.

`public const float MinimumPlateScale`

:   How far the nameplate is allowed to shrink with the stage. The 24px combatant name is the smallest type on the plate, and 16px is the floor for anything a player reads mid-turn, so the plate may lose a third of its size and no more. Below this it stops following the stage, and two combatants standing close enough to collide is the composition's problem to solve rather than the plate's.

`public const float NonCandidateDim`

:   How far a combatant the current skill cannot reach is pushed back. This multiplier is applied after the stage's rank tint. At 0.72 a non-candidate is clearly de-emphasized while retaining enough of its authored colour to remain legible in a deep arrangement.

`public const float PlateGroundOverlapPixels`

:   Signed offset of the plate's top from a combatant's visual ground, in reference pixels. A negative value leaves space for the targeting ring beneath the feet instead of covering it with the identity card.

`public const float PlateOffsetPixels`

:   Plate offset above the token, in reference pixels.

**Methods**

`public void ApplySkin(CompiledBattleSkin battleSkin, float unitsPerPixel)`

:   Attaches the skinned plate that renders this token's values. Optional: a token with no skin still mirrors state onto its properties, which is what the headless tests assert against.

    - `battleSkin` &mdash; The compiled skin to draw with; null leaves the token unskinned and adds no plate.
    - `unitsPerPixel` &mdash; World units per reference pixel, used to size and offset the plate.

`public void ApplyState(CombatantState combatant, int shieldAmount, int statusPipCount)`

:   Mirrors snapshot/event state onto the token and its plate.

    - `combatant` &mdash; Snapshot state to mirror; null leaves health, maximum, and death as they were.
    - `shieldAmount` &mdash; Shield amount to display; negative values clamp to zero.
    - `statusPipCount` &mdash; How many status pips to show; negative values clamp to zero.

`public void Configure(StableId combatantId, FormationFacing facing, StableId sortingLayerKey, int sortingOrder, ProjectedFormationPoint slotProjected, ProjectedFormationPoint approachProjected, float unitsPerPixel)`

:   Places the token from its compiled slot projection.

    - `facing` &mdash; Compiled slot facing; the sprite is mirrored when this differs from its source art direction.
    - `sortingLayerKey` &mdash; Recorded for the caller to apply; only `sortingOrder` reaches the sprite renderer.
    - `slotProjected` &mdash; Projected rest position, in reference pixels, that the token is moved to.
    - `approachProjected` &mdash; Projected approach point, recorded for callers that animate a step-in; Configure does not move the token to it.
    - `unitsPerPixel` &mdash; World units per reference pixel, applied to the projected position.
    - `combatantId` &mdash; Stable combatant identity retained for later stage lookups.
    - `sortingOrder` &mdash; Renderer order within `sortingLayerKey`.

`public void Pulse()`

:   Starts a visual pulse that always returns to rest. Replaces the older behaviour of assigning a scale that was never restored.

`public void SetArt(Sprite art)`

:   Gives this combatant its painted body. This is the supported way to dress a token, and it does the two things that assigning `SpriteRenderer.sprite` directly does not: it retires the lettered fallback card, which would otherwise sit behind the art as a leftover box, and it moves the nameplate down to the new body's ground line.

    - `art` &mdash; The combatant's illustration, or null to return to the lettered fallback. A renderer is provisioned on the token root when needed.

`public void SetArtScale(float scale)`

:   Scales this combatant's art to fit the stage it is standing on. Only the body scales. The nameplate is built in reference pixels and keeps its own size, because a plate that shrank with the stage would take the name and the health readout below the size anybody can read - which is the fault this whole pass exists to fix.

    - `scale` &mdash; Multiplier for the art, normally `BattleStage2D.TokenScale`. Zero or less is ignored, so a caller that has not computed one yet leaves the token at its authored size.

`public void SetCastProgress(float fraction, bool visible)`

:   Shows cast progress on the plate, or hides the cast bar.

    - `fraction` &mdash; Cast progress in [0,1]; read only when `visible` is true.
    - `visible` &mdash; False hides the cast bar. Does nothing when the token is unskinned.

`public void SetGauge(float fraction, bool visible)`

:   Shows the scheduler gauge on the plate, or hides it.

    - `fraction` &mdash; Gauge fill in [0,1]; a full gauge is drawn with the ready accent.
    - `visible` &mdash; False hides the gauge. Does nothing when the token is unskinned.

`public void SetPlateIdentity(string label, Color teamTint)`

:   Updates set plate identity on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.

    - `label` &mdash; The resolved display string; ignored when the token is unskinned.
    - `teamTint` &mdash; Tint that distinguishes ally from enemy, replacing the skin default.

`public void SetSourceArtFacing(FormationFacing value)`

:   Sets the direction painted into the source sprite, independently of its compiled slot facing.

    - `value` &mdash; The source illustration's unmirrored direction. It persists when the stage reconfigures this token.

`public void SetStagePresence(SkinStagePresenceTokens presence, int rank)`

:   Stages this token for the depth rank it stands at. This is what makes a formation read as a scene instead of a diagram: a body further from the camera is smaller, darker, and lit less by the key light, and the three cues together are what the eye reads as distance. One of them alone reads as a smaller character, a shadowed character, or a differently-painted one.

    - `presence` &mdash; The skin's staging tokens. Sanitized on the way in, so an unclamped authored value cannot reach the transform.
    - `rank` &mdash; Depth rank, 0 at the front. Negative values are treated as the front, which is what a caller that could not resolve a rank should pass.

`public void SetTargetCandidate(bool eligible)`

:   Marks this token eligible, or not, for the pick in progress.

    - `eligible` &mdash; False dims the token to `NonCandidateDim`.

`public void SetVisualGroundAnchor(Transform anchor)`

:   Sets an authored point on this token that represents where its art meets the ground. The anchor may be the token itself or any descendant; a foreign transform is rejected so one combatant cannot ground itself from another object's moving hierarchy. Passing null restores renderer or fallback bounds grounding.

    - `anchor` &mdash; A transform in this token's hierarchy, or null to use visible bounds.

`public void StopPulse()`

:   Cancels the sample pulse without changing health, art, or selection.

`public void Tick(float deltaSeconds)`

:   Advances plate and pulse animation by a visual delta.

    - `deltaSeconds` &mdash; Wall-clock seconds since the last call. Non-positive values are ignored, and this is presentation time only: it never advances the battle.

`public bool TryGetVisualGroundWorld(out Vector3 groundWorld, out float widthWorld)`

:   Returns the actual visual ground line and width in world space. Renderer bounds keep this correct for a configured child renderer, pivots, flipX and transformed parents. When art is absent, the visible fallback card supplies the same contract.

    - `groundWorld` &mdash; Receives the visual ground centre in world coordinates.
    - `widthWorld` &mdash; Receives the visual width in world units.
    - **Returns** &mdash; True when a visible sprite or fallback body supplies a non-zero width.

---

## PresentationBeat

```csharp
public sealed class PresentationBeat
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationBeat.cs</small>

One immutable presentation beat: the event context plus the resolved
recipe. A null recipe is an instant, no-visual beat (an unmapped event).
Beat timing is derived from the recipe only for visuals and never feeds
back into any authoritative hash.

**Constructors**

`public PresentationBeat(PresentationBeatContext context, PresentationRecipeDefinition recipe)`

:   Pairs an event's beat context with the recipe resolved for it.

    - `context` &mdash; The data extracted from the source event.
    - `recipe` &mdash; The resolved recipe, or null to make this an instant no-visual beat.

**Properties**

`public PresentationBeatContext Context`

:   Everything the beat knows about the event it came from: participants, tick, and any amount. It is captured once when the beat is built, so a beat that plays several frames later still draws the situation as it stood at the event rather than as the battle stands now.

`public bool IsNoVisual`

:   True when the source event mapped to no recipe.

`public int PhaseCount`

:   The number of visual phases (0 for a no-visual beat, else 3).

`public PresentationRecipeDefinition Recipe`

:   The resolved recipe, or null for a no-visual beat.

`public float TotalDurationSeconds`

:   Total clamped duration across the three phases, in seconds.

---

## PresentationBeatContext

```csharp
public readonly struct PresentationBeatContext
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationBeat.cs</small>

The non-authoritative, immutable data a beat needs, extracted entirely
from one gameplay event's property set. It carries participants and an
optional amount for floating numbers; it performs no simulation math.

**Constructors**

`public PresentationBeatContext(StableId eventTypeId, long tick, ulong eventSequence, StableId? sourceId, StableId? targetId, StableId? skillId, StableId? statusId, StableId? reactionId, int? amount)`

:   Creates a beat context. Normally produced by `BeatDeriver.BuildContext` from an event's property set; construct one directly only to drive a beat without a live battle.

    - `eventTypeId` &mdash; The source event's type, one of the `BattleIds` event identifiers.
    - `tick` &mdash; The tick the source event was emitted on.
    - `eventSequence` &mdash; The source event's battle-wide sequence, which identifies this beat's origin uniquely.
    - `sourceId` &mdash; The acting combatant, or null when the event names none.
    - `targetId` &mdash; The affected combatant, or null when the event names none.
    - `skillId` &mdash; The skill involved, or null.
    - `statusId` &mdash; The status involved, or null.
    - `reactionId` &mdash; The reaction rule involved, or null.
    - `amount` &mdash; The event's numeric amount, for a floating number. Null when the event carries none, which is the common case for non-numeric events such as a cast starting.

`public PresentationBeatContext(StableId eventTypeId, long tick, ulong eventSequence, StableId? sourceId, StableId? targetId, StableId? skillId, StableId? statusId, StableId? reactionId, int? amount, bool isCritical, bool blockedByShield, bool isKillingBlow)`

:   Creates a beat context that also carries the outcome flags a hit can have. Same as the shorter form in every other respect; the flags default to false there, which is what an event that does not report them reads as.

    - `eventTypeId` &mdash; The source event's type, one of the `BattleIds` event identifiers.
    - `tick` &mdash; The tick the source event was emitted on.
    - `eventSequence` &mdash; The source event's battle-wide sequence, which identifies this beat's origin uniquely.
    - `sourceId` &mdash; The acting combatant, or null when the event names none.
    - `targetId` &mdash; The affected combatant, or null when the event names none.
    - `skillId` &mdash; The skill involved, or null.
    - `statusId` &mdash; The status involved, or null.
    - `reactionId` &mdash; The reaction rule involved, or null.
    - `amount` &mdash; The event's numeric amount, for a floating number. Null when the event carries none.
    - `isCritical` &mdash; Whether the event reported the hit as critical.
    - `blockedByShield` &mdash; Whether a shield absorbed some or all of the amount.
    - `isKillingBlow` &mdash; Whether the amount took its target out of the battle.

**Properties**

`public int? Amount`

:   The amount to show as a floating number, or null when the source event carries no numeric amount.

`public bool BlockedByShield`

:   Whether a shield absorbed some or all of the amount. Offered so a project can play a block rather than a hit; nothing in the shipped beats reads it yet.

`public ulong EventSequence`

:   The source event's battle-wide sequence. It identifies this beat's origin uniquely, so it is what to key on when suppressing a beat already played.

`public StableId EventTypeId`

:   Which kind of gameplay event the beat came from. Recipe resolution matches on it before anything else, so a recipe declaring another event type is never considered however specific its selector is.

`public bool IsCritical`

:   Whether the source event reported the hit as critical. False when the event says nothing about it, so a beat built from an emitter that does not report criticals reads exactly as it always did.

`public bool IsKillingBlow`

:   Whether this amount is what took the target out of the battle. The authoritative death is still its own event; this only lets a visual react on the blow instead of one event later.

`public StableId? ReactionId`

:   The reaction rule that produced the event, or null. Only a recipe selecting by reaction ID reads it, which is how a counter-attack can be given its own look without touching the ordinary attack recipe.

`public StableId? SkillId`

:   The skill involved, or null. A recipe that selects by skill ID or skill tag can only match while this is present; without it the candidates are the event-default recipes plus any status or reaction selector the event still satisfies.

`public StableId? SourceId`

:   The acting combatant, or null when the event names none. Animations play on this combatant's token, and a visual effect anchors here when the event carries no target.

`public StableId? StatusId`

:   The status involved, or null. It is what recipes selecting by status ID or status tag match against.

`public StableId? TargetId`

:   The affected combatant, or null when the event names none. Visual effects prefer this anchor over `SourceId`, so a hit lands on the receiver rather than on whoever swung.

`public long Tick`

:   The tick the source event was emitted on. It is battle time, not the moment the beat is drawn - a queue of beats can still be playing out several ticks behind the simulation.

---

## PresentationStagePreset

```csharp
public sealed class PresentationStagePreset : ScriptableObject
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationStagePreset.cs</small>

Closed, neutral presentation content for a battle stage. This asset is
visual-only and is never read by simulation or included in its hashes.

**Properties**

`public IReadOnlyList<StageAnimationBinding> AnimationBindings`

:   Authored neutral animation bindings in explicit order.

`public IReadOnlyList<StageAudioBinding> AudioBindings`

:   Authored one-shot sound bindings in explicit order.

`public PerformFeelPreset Feel`

:   Authored feel copied by each playback session.

`public PresentationRecipeSet Recipes`

:   Authored recipe set copied by each playback session.

`public IReadOnlyList<StageVfxBinding> VfxBindings`

:   Authored prefab/sprite effect bindings in explicit order.

**Methods**

`public IReadOnlyList<string> Validate()`

:   Returns authoring diagnostics without throwing. Duplicate keys are reported even though playback keeps the first binding deterministically.

    - **Returns** &mdash; Ordered diagnostics for missing content, duplicate keys and invalid effect values; empty when valid.

---

## PresenterBinding

**Start here**

```csharp
public sealed class PresenterBinding
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresenterBinding.cs</small>

The explicit dependency bundle a driver hands to a
`BattlePresenter`. It carries compiled content, the
non-authoritative formation layout, the recipe set, the four visual
adapters, the display-string table, and an optional uGUI root. The
binding contains no engine and no authoritative mutator.

**Constructors**

`public PresenterBinding(CompiledAuthoringCatalog catalog, CompiledEncounterFormationLayout layout, PresentationRecipeSet recipes, IAnimationAdapter animation, IVfxAdapter vfx, IAudioAdapter audio, IPoolAdapter pool, DisplayStringTable labels, BattleUiRoot ui = null, PresentationLog log = null, IBattleView surface = null)`

:   Bundles everything a presenter needs into one value. Every argument through `labels` is required and throws `ArgumentNullException` when null, so a binding that constructs is always complete: the presenter never has to null-check its own dependencies.

    - `layout` &mdash; The non-authoritative formation layout, used for placement only.
    - `recipes` &mdash; The recipe set beats are resolved against.
    - `labels` &mdash; The display-string table names are resolved through.
    - `ui` &mdash; Optional legacy uGUI root; null omits that root while an optional native surface can still provide a HUD.
    - `log` &mdash; Optional shared log-once ledger; a fresh one is created when null.
    - `animation` &mdash; Required adapter that plays animation keys named by presentation phases.
    - `audio` &mdash; Required adapter that plays phase sound keys without affecting simulation state.
    - `catalog` &mdash; Compiled content used to interpret event, skill, status, and combatant identities.
    - `pool` &mdash; Required owner of reusable token, floating-number, and effect instances.
    - `vfx` &mdash; Required adapter that spawns phase effect keys at resolved formation anchors.
    - `surface` &mdash; Optional native or custom view retained for presentation and target interaction. Its session and pointer contracts are bound by the presenter when supported.

**Properties**

`public IAnimationAdapter Animation`

:   Plays the animation keys named by a beat's phases.

`public IAudioAdapter Audio`

:   Plays the one-shot sound keys named by a beat's phases.

`public CompiledAuthoringCatalog Catalog`

:   The compiled catalog battle events are interpreted against, used to derive beats and the shape of a pending decision. It is read only, so the presenter can share the same catalog instance as the engine.

`public DisplayStringTable Labels`

:   Display text for the IDs shown to players. Compiled content carries no labels, so an ID this table does not hold falls back to its raw ID text instead of rendering blank.

`public CompiledEncounterFormationLayout Layout`

:   Where each combatant sits on the stage. It is non-authoritative, so swapping it moves the art and nothing else.

`public PresentationLog Log`

:   Shared log-once ledger for missing-key degradation.

`public IPoolAdapter Pool`

:   Lends out the instances behind token views, floating numbers, and pooled effects. The presenter and the stage return what they borrowed on teardown rather than destroying it, so the same pool survives repeated battles.

`public PresentationRecipeSet Recipes`

:   The ordered recipe list every battle event is matched against. Candidate recipes come only from this set and nothing else in the project is scanned, though tag selectors are matched against the catalog's compiled skill and status tables. An event that matches no recipe here still becomes a beat, just one with no visuals.

`public IBattleView Surface`

:   Renderer-independent HUD, supplied instead of the legacy uGUI root.

`public BattleUiRoot Ui`

:   Optional legacy uGUI root. Null omits only this root; the stage and an optional native surface can still be presented.

`public IVfxAdapter Vfx`

:   Plays the one-shot effect keys named by a beat's phases.

---

## StageAnimationBinding

```csharp
public sealed class StageAnimationBinding
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationStagePreset.cs</small>

Authored key to neutral source/target pulse binding.

**Fields**

`public string Key`

:   Ordinal animation key named by a presentation phase.

`public StageAnimationSource Source`

:   Participant whose neutral sample pulse plays.

---

## StageAnimationSource

```csharp
public enum StageAnimationSource
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationStagePreset.cs</small>

Where a neutral sample animation is anchored.

| Value | Meaning |
| --- | --- |
| `SourcePulse` | Pulses the source token named by the presentation cue. |
| `TargetPulse` | Pulses the target token named by the presentation cue. |

---

## StageAudioBinding

```csharp
public sealed class StageAudioBinding
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationStagePreset.cs</small>

Authored key to a one-shot audio clip.

**Fields**

`public AudioClip Clip`

:   One-shot clip; missing clips warn and play nothing.

`public string Key`

:   Ordinal sound key named by a presentation phase.

---

## StageFrameMode

```csharp
public enum StageFrameMode
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/BattleStageFrame.cs</small>

How the stage rectangle is derived from the screen.

| Value | Meaning |
| --- | --- |
| `FullScreen` | Use the whole screen, inset by the configured margins. |
| `FixedAspect` | Keep a fixed aspect ratio inside the margins, letterboxing as needed. |
| `Explicit` | Use an explicit pixel rectangle, ignoring screen size. |

---

## StagePresentationPlayback

```csharp
public sealed class StagePresentationPlayback : IPerformBeatModule, IDisposable
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/StagePresentationPlayback.cs</small>

Owns a preset's isolated presentation copies and transient stage effects.
All objects are parented below the supplied owner; no camera or scene scan
is used. Missing and malformed bindings degrade with one warning each.

**Constructors**

`public StagePresentationPlayback(PresentationStagePreset preset, BattlePresenter presenter, Transform owner, PresentationLog presentationLog = null)`

:   Copies recipes and feel without modifying their authored assets, then owns timed effects and one-shot audio below an explicit scene parent. Null preset or owner throws; absent effect bindings warn and play nothing.

    - `preset` &mdash; Authored visual content read once and copied for this session.
    - `presenter` &mdash; Optional existing stage for token pulses and relative sprite sorting.
    - `owner` &mdash; Required scene parent; Dispose destroys only descendants created by this playback.
    - `presentationLog` &mdash; Optional shared warning deduplicator; null creates a private one.

**Properties**

`public int ActiveVfxCount`

:   Live effects not yet expired or reset.

`public IAnimationAdapter Animation`

:   Neutral source/target pulse adapter.

`public IAudioAdapter Audio`

:   One-shot sound adapter under the explicit owner.

`public Transform EffectsRoot`

:   Root containing this session's effects, prototypes and audio.

`public PerformFeelPreset Feel`

:   Owned feel copy used by this playback session.

`public Transform Owner`

:   Explicit parent supplied by the host.

`public BattlePresenter Presenter`

:   Optional stage presenter used for token pulses and sprite sorting.

`public PresentationRecipeSet Recipes`

:   Owned recipe set containing owned definition copies.

`public IVfxAdapter Vfx`

:   Effect adapter with bounded, timed instances owned by this session.

**Methods**

`public void Dispose()`

:   Resets playback and destroys all owned copies and scene objects, once.

`public void OnPhaseBegin(PerformPhaseContext context)`

:   Intentionally does not redispatch phases already handled by the presenter.

    - `context` &mdash; Phase notification; adapters are dispatched separately by BattlePresenter.

`public void Reset()`

:   Releases effects, stops audio and restores owned neutral pulses.

`public void Tick(float presentationDeltaSeconds)`

:   Expires effects on positive finite presentation time.

    - `presentationDeltaSeconds` &mdash; Elapsed visual seconds; zero, negative and non-finite values are ignored.

---

## StageVfxBinding

```csharp
public sealed class StageVfxBinding
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/PresentationStagePreset.cs</small>

Authored key to a stage VFX prototype.

**Fields**

`public string Key`

:   Ordinal effect key named by a presentation phase.

`public float LifetimeSeconds`

:   Positive finite lifetime in the shared visual clock.

`public GameObject Prototype`

:   Optional prefab cloned with its authored renderer settings.

`public float Scale`

:   Positive finite multiplier of the effect's authored scale.

`public string SortingLayerName`

:   Sorting layer of the sprite alternative.

`public int SortingOrderOffset`

:   Sorting order relative to the target body, or source when no target exists.

`public Sprite Sprite`

:   Sprite alternative when no prefab is assigned.

`public Color Tint`

:   Tint for the sprite alternative; prefab colors are preserved.

---

## TargetPreviewView

```csharp
public sealed class TargetPreviewView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/TargetPreviewView.cs</small>

Draws what a skill is about to hit, on the stage, before the player
commits.

The invariant this exists to hold: the affected set is drawn on the stage
rather than described in a tooltip sentence. Nine of the twelve shipped
resolvers take no player pick at all, so for those a sentence was the only
thing the player ever got - and a sentence cannot say which three of six
bodies are in the blast.

Every treatment is procedural: rings, bands, scrims and ticks drawn from
the skin's own palette. Nothing ships for it, and every one is fed by
`TargetCandidateQuery.GetCandidates`, which already agrees with
the engine. Eight looks, one data source, no new simulation code.

**Properties**

`public bool BandVisible`

:   Whether a formation-row band is currently drawn.

`public TargetTreatment? Current`

:   The treatment currently on screen, or null when nothing is previewed.

`public bool ScrimVisible`

:   Whether a region fill is currently drawn.

`public int VisibleMarkCount`

:   How many marks the last `Show` drew.

**Fields**

`public const int PreviewSortingOrder`

:   Where the preview draws: above the contact shadows, below every body. A scrim over the combatants would be a filter on the picture rather than a mark on the ground, and the player would be judging the pick through it.

`public const float RingPixels`

:   Diameter of a candidate ring, in reference pixels.

`public const float RowBandPixels`

:   Height of a formation-row band, in reference pixels.

`public const float ScrimOpacity`

:   Opacity of a team or stage scrim.

**Methods**

`public void Build(CompiledBattleSkin battleSkin, float unitsPerPixel)`

:   Prepares the preview to draw with a skin. Call before `Show`.

    - `battleSkin` &mdash; The compiled skin whose palette the marks are drawn from.
    - `unitsPerPixel` &mdash; World units per reference pixel, matching the stage.

`public void Hide(BattleStage2D stage)`

:   Clears the preview and gives every token its colour back.

    - `stage` &mdash; The stage to un-dim; null skips that half.

`public void Show(BattleStage2D stage, TargetTreatment treatment, IReadOnlyList<StableId> affected, IReadOnlyList<StableId> candidates, StableId playerTeamId)`

:   Draws `treatment` for the set the resolver returned. The treatment is degraded for the party in front of it first, so a region shape with one candidate collapses to the single-pick look rather than drawing a team scrim around one body.

    - `stage` &mdash; The stage whose placements supply every position.
    - `treatment` &mdash; The classified treatment, before degradation.
    - `affected` &mdash; Combatants the skill would reach.
    - `candidates` &mdash; Legal picks. Anything on the stage and not in here is dimmed.
    - `playerTeamId` &mdash; The player's team, which decides which half of the stage is theirs.

---

## TargetingReticleView

```csharp
public sealed class TargetingReticleView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Stage/TargetingReticleView.cs</small>

The cursor that lives on one candidate: a marker hanging over whoever is
currently pointed at, with that candidate's position in the list beside it.

This is the treatment `TargetingPreset.Reticle` asks for, and it
is the one the genre trained players to expect -- a marker above a head that
steps sideways when you press a direction and commits when you press
confirm. Until now the package expressed every pick the same way whatever the
preset said: a row of name buttons under the stage, which is fine with a
mouse and close to unusable on a pad.

It is drawn from the skin's own shapes, so it ships no texture, needs no font
glyph, and inherits whatever look the project chose. It is presentation only:
it never resolves a target, it only says which one is being pointed at.

**Properties**

`public bool IsShown`

:   True while the marker is on screen.

`public StableId? Pointed`

:   The combatant the marker is over, or null while it is hidden.

**Fields**

`public const float BobHertz`

:   Bobs per second. Slow enough to read as breathing, not as an alarm.

`public const float BobPixels`

:   Half-height of the marker's bob, in reference pixels.

`public const float HoverPixels`

:   How far above the combatant's art the marker floats, in reference pixels.

`public const float MarkerPixels`

:   Marker width and height in reference pixels.

`public const int ReticleSortingOrder`

:   Sorting order the marker draws at, above every combatant plate.

**Methods**

`public void ApplySkin(CompiledBattleSkin battleSkin)`

:   Re-applies the skin's colours without rebuilding the marker.

    - `battleSkin` &mdash; The skin to adopt.

`public void Build(CompiledBattleSkin battleSkin, float pixelScale)`

:   Builds the marker. Explicit so EditMode tests can construct one.

    - `battleSkin` &mdash; Skin the marker is dressed from; null falls back to the package default.
    - `pixelScale` &mdash; World units one reference pixel is worth.

`public void Hide()`

:   Takes the marker off screen.

`public void Show(BattleStage2D stage, StableId combatantId, int index, int count)`

:   Puts the marker over one candidate.

    - `stage` &mdash; Stage that knows where the combatant is standing.
    - `combatantId` &mdash; The candidate to point at.
    - `index` &mdash; Zero-based position in the candidate list.
    - `count` &mdash; How many candidates there are.

`public void Tick(float presentationDeltaSeconds)`

:   Advances the marker's bob around the anchor it was shown at. The offset is applied to a remembered anchor rather than to the current position, because adding a delta to the live transform every frame is how a bob turns into a drift.

    - `presentationDeltaSeconds` &mdash; Visual seconds elapsed.

---
