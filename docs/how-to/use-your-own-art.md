# Use your own character art, animation and effects

Replace the placeholder token with your own prefab, drive an `Animator` from beat keys, keep an idle
loop alive between beats, and anchor an effect to a point you authored on a slot. You need a bound
presenter ([guide 3](../tutorials/show-the-battle.md)) and a recipe set that names keys
([Turn events into visuals](presentation-recipes.md)). The package supplies keys and placement; the
art, and every line below, is host code.

The snippets on this page draw on three namespaces. Paste all three at the top of any file you copy
code into, or the types will not resolve:

```csharp
using TurnGauge.Presentation;   // adapters, PresenterBinding, BattleStage2D, beat specs
using TurnGauge.Simulation;     // StableId
using TurnGauge.Authoring;      // FormationFacing
```

## Replace the token prototype

Tokens come from the pool adapter under one key,
[`BattleStage2D.TokenPoolKey`](../reference/stage-and-tokens.md#battlestage2d) (`"presentation.token"`),
and must be registered before `Bind`, because the stage spawns its tokens inside that call.

Order matters twice over. `PresenterBinding` takes the pool as a constructor argument, so build the
pool first, register into it, and only then construct the binding - passing a different
`IPoolAdapter` to the binding than the one you registered the prototype on is the easiest way to get
placeholder tokens back with no error to explain them.

```csharp
var log = new PresentationLog();
var pool = new BuiltInPoolAdapter(presenterHost.transform, log);
pool.RegisterPrototype(BattleStage2D.TokenPoolKey, myCharacterPrefab);

// The binding must carry that same pool instance.
var binding = new PresenterBinding(
    catalog, layout, recipes,
    animation, vfx, audio, pool,
    labels);               // ui and log are optional trailing arguments
presenter.Bind(binding);   // the stage clones the prototype once per occupied slot
```

Each clone is parented under the stage, given the
[`CombatantTokenView`](../reference/stage-and-tokens.md#combatanttokenview) on its **root** (the
stage looks only there, and adds one when the root carries none), then moved to the projected slot
position with `localScale` reset to `Vector3.one` - so bake scale into a child rather than the
prefab root, and keep the view on the root or the stage will configure a second copy beside it.

<figure aria-label="Engineering map of token pooling and formation anchors">
<style>
  .tg-art-flow { display:grid; gap:0.7em; max-width:70rem; margin:1rem 0; color:#f2f5f7; font:16px/1.35 system-ui,sans-serif; }
  .tg-art-flow .tg-flow-step { display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1fr); align-items:stretch; gap:0.7em; }
  .tg-art-flow .tg-flow-node { min-width:0; padding:0.65em 0.8em; border:2px solid #72b7d6; border-radius:0.65rem; background:#18212b; text-align:center; overflow-wrap:anywhere; }
  .tg-art-flow .tg-flow-node strong, .tg-art-flow .tg-flow-node span { display:block; }
  .tg-art-flow .tg-flow-node span { margin-top:0.3rem; color:#c7d6de; font-family:ui-monospace,SFMono-Regular,monospace; font-size:1em; }
  .tg-art-flow .tg-flow-arrow { display:flex; align-items:center; justify-content:center; color:#e4ad62; font-size:1.5em; font-weight:700; }
  .tg-art-flow .tg-flow-branch { padding:0.8em; border:2px solid #8db7c8; border-radius:0.65rem; background:#202b36; text-align:center; }
  .tg-art-flow .tg-flow-branch > strong { display:block; margin-bottom:0.7rem; }
  .tg-art-flow .tg-flow-choices { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:0.7em; }
  .tg-art-flow .tg-flow-choice { min-width:0; padding:0.65em; border:2px solid #8db7c8; border-radius:0.55rem; background:#18212b; overflow-wrap:anywhere; }
  .tg-art-flow .tg-flow-choice span { display:block; margin-top:0.25rem; color:#c7d6de; font-family:ui-monospace,SFMono-Regular,monospace; font-size:1em; }
  .tg-art-flow .tg-flow-merge { margin-top:0.65rem; color:#e4ad62; font-size:1.5em; font-weight:700; }
  .tg-art-flow .tg-flow-inline::before { content:"\2192"; }
  @media (max-width:700px) {
    .tg-art-flow .tg-flow-inline::before { content:"\2193"; }
    .tg-art-flow .tg-flow-step { grid-template-columns:minmax(0,1fr); }
    .tg-art-flow .tg-flow-arrow { min-height:1.5rem; }
    .tg-art-flow .tg-flow-choices { grid-template-columns:minmax(0,1fr); }
  }
</style>
<div class="tg-art-flow" role="group" aria-label="PresenterBinding passes the same pool to BattleStage2D, which selects a specific or shared pool key before cloning CombatantTokenView and resolving the compiled formation anchor">
  <div class="tg-flow-step">
    <div class="tg-flow-node"><strong>PresenterBinding</strong><span>same IPoolAdapter passed to Bind</span></div>
    <div class="tg-flow-arrow tg-flow-inline" aria-hidden="true"></div>
    <div class="tg-flow-node"><strong>BattleStage2D</strong><span>one occupied slot</span></div>
  </div>
  <div class="tg-flow-arrow" aria-hidden="true">&#8595;</div>
  <div class="tg-flow-branch">
    <strong>Select the pool key for that occupied slot</strong>
    <div class="tg-flow-choices">
      <div class="tg-flow-choice"><strong>specific key</strong><span>TokenPoolKeyFor(id), when HasPrototype is true</span></div>
      <div class="tg-flow-choice"><strong>shared fallback</strong><span>TokenPoolKey, presentation.token, otherwise</span></div>
    </div>
    <div class="tg-flow-merge" aria-hidden="true">&#8595; both paths converge</div>
  </div>
  <div class="tg-flow-arrow" aria-hidden="true">&#8595;</div>
  <div class="tg-flow-node"><strong>clone root</strong><span>CombatantTokenView, then project the occupied slot</span></div>
  <div class="tg-flow-arrow" aria-hidden="true">&#8595;</div>
  <div class="tg-flow-node"><strong>formation compiled anchor</strong><span>TryGetAnchorWorld(..., VfxAnchorId)</span></div>
</div>
<figcaption>Engineering map of the verified extension seams. This is an authored diagram, not a runtime capture or art approval.</figcaption>
</figure>

The stage asks an `IPoolPrototypeQuery` before it acquires a specific key. That check is what
preserves the shared fallback when a combatant has no dedicated prototype. Once the root is
spawned, named formation anchors are resolved from the compiled placement by
`TryGetAnchorWorld(combatantId, PresentationVfxAnchorKind.Anchor, anchorId, out world)`;
the VFX adapter receives the resulting stage-space position.

### A SpriteRenderer is optional

`CombatantTokenView` takes a serialized `SpriteRenderer`, falls back to `GetComponent` in `Awake`,
and works without either, so a rigged 2D prefab, an `Animator`-driven model and a full 3D character
are all valid prototypes. What that renderer would have done is then yours, from a component that
reads the view in `LateUpdate` - never `OnEnable`, which runs before the stage configures a token.

| Without a `SpriteRenderer` | Read instead |
| --- | --- |
| No horizontal flip on a slot | Compare `token.SourceArtFacing` with `token.Facing`; mirror only when they differ |
| No `sortingOrder` written | `token.SortingOrder`; `token.SortingLayerKey` is recorded, never applied |
| No desaturate-and-fade on death | `token.IsDead` |

### Keep source and displayed facing explicit

`Facing` describes the direction the token should face in its compiled formation slot.
`SourceArtFacing` describes the direction already painted into the sprite before TurnGauge mirrors
it. The token mirrors the sprite only when those values differ. This keeps a sprite authored facing
left facing left in a left-facing slot, while a left-authored sprite placed in a right-facing slot
is mirrored once. The rule applies to the stage body and the matching turn-order portrait; it does
not mirror HUD labels, world effects or other presentation elements.

The two-argument `SetCombatantArt` overload remains compatible with older projects and preserves the
token's existing source-facing metadata. A newly configured token defaults to a Right-facing source;
use the overload with `sourceArtFacing` whenever the imported illustration points elsewhere:

```csharp
// This sprite was painted facing left, and the formation slot currently faces right.
presenter.SetCombatantArt(combatantId, leftFacingSprite, FormationFacing.Left);
// The stage body and its rail portrait are mirrored once for the right-facing slot.
```

For a UI-only binding with no stage token, the three-argument
`SetCombatantPortrait(combatantId, portrait, sourceFacing)` overload records the source direction
and derives the displayed direction from the current team row. When the rail needs an explicit
destination, use the four-argument overload instead:

```csharp
ui.SetCombatantPortrait(
    combatantId,
    leftFacingPortrait,
    FormationFacing.Left,   // source art direction
    FormationFacing.Right); // desired displayed direction
```

Passing the same direction for source and desired (`Left` to `Left`, for example) deliberately keeps
the portrait unmirrored. Keep portrait framing and crop decisions separate from the token's visual
ground or formation anchors: changing the crop must not move the feet, HUD, or effect attachment.

### Author the visual ground point

Character illustrations often include transparent breathing room below the feet. The renderer
bounds still include that canvas, so the default ground line can leave a contact shadow or a
nameplate visibly low. When the feet are not the bottom of the imported rectangle, add a child
transform at the intended contact point and assign it as the token's visual ground anchor:

```csharp
var feet = token.transform.Find("Visual Ground");
token.SetVisualGroundAnchor(feet);

if (token.TryGetVisualGroundWorld(out var ground, out var artWidth))
{
    // ground is the authored feet position; artWidth is still the renderer's visible width.
}
```

`SetVisualGroundAnchor` accepts the token transform or a descendant of it. A transform from
another hierarchy is rejected. Passing `null` removes the override and restores grounding from
the visible sprite or fallback bounds. The plate and contact shadow are repositioned when the
anchor changes. The lookup is deliberately authored: TurnGauge does not scan texture alpha,
crop transparent pixels, or guess where feet are.

Keep this point separate from a formation or VFX anchor. A formation anchor belongs to a slot and
places an effect in stage space; the visual ground anchor belongs to one token and controls where
that token's plate and contact shadow meet the ground. Samples use a measured child anchor while
keeping the complete source canvas, so the art is never cropped to make placement work.

For 2D authoring, keep the local origin on the intended ground line and choose the sprite pivot
that suits the drawing. The Sira sample convention is pivot `(0.5, 0.08333)`, with the artwork
supported from that local origin; a separate `Visual Ground` child remains the precise option when
the feet do not coincide with the imported bounds. This convention does not replace formation or
VFX anchors.

### Give one combatant its own prefab

`BattleStage2D.TokenPoolKey` is the shared fallback. To give a combatant a body of its own, register
under [`BattleStage2D.TokenPoolKeyFor(combatantId)`](../reference/stage-and-tokens.md#battlestage2d)
instead, which is that key plus the combatant id:

```csharp
pool.RegisterPrototype(BattleStage2D.TokenPoolKey, genericPrefab);          // everyone else
pool.RegisterPrototype(BattleStage2D.TokenPoolKeyFor(knightId), knightPrefab);
```

The stage prefers the specific key when the pool holds a prototype for it and falls back to the
shared one otherwise, so you can give art to some combatants and not others. Tokens are released
back to the key they came from, so a rebuild does not hand a combatant someone else's body.

!!! note "Why the stage asks before it acquires"
    `IPoolAdapter.Acquire` is allowed to fabricate an empty instance for an unregistered key rather
    than return null, so "try the specific key and check for null" would spawn blank tokens instead
    of falling back. The stage asks first, through the optional
    [`IPoolPrototypeQuery`](../reference/presentation-adapters-and-recipes.md#ipoolprototypequery).
    A custom `IPoolAdapter` that does not implement it keeps the old single-key behaviour exactly.

For a sprite swap rather than a whole prefab, you do not need any of this: resolve the token after
binding and set the renderer, which is what the shipped demo does.

## Drive an Animator from the animation adapter

[`BuiltInAnimationAdapter.Register(animationKey, handler)`](../reference/presentation-adapters-and-recipes.md#builtinanimationadapter)
binds one key to one `Action<PresentationCue>`. The
[cue](../reference/presentation-adapters-and-recipes.md#presentationcue) carries `WorldPosition`,
`Facing`, `Parent`, `SourceId` and `TargetId` - never a token - so look the token up on the stage.
An animation cue always resolves against the beat's **source**, never its target.

```csharp
var animation = new BuiltInAnimationAdapter(log);
animation.Register("anim.attack", cue =>       // one Register call per authored key
{
    if (!presenter.Stage.TryGetToken(cue.SourceId, out var token)) return;
    var animator = token.GetComponentInChildren<Animator>();
    if (animator == null) return;
    animator.speed = presenter.Speed;          // Animators run on Unity's clock, not the visual one
    animator.SetTrigger("Attack");
});
```

Keys match ordinally and case-sensitively, and an unbound key warns once through the shared
`PresentationLog` then stays silent. A beat whose source has no token on the stage still calls your
handler, with the cue at `(0,0,0)` but `SourceId` intact; an event that names no source at all
arrives at `(0,0,0)` with a *default* `SourceId`, which no token can match. Both make the early
returns required rather than defensive.

## Keep a looping idle alive across beats

A beat is three phases - In, Impact, Out. Each fires its cues **once, as it starts**, then waits out
its duration on the visual clock; after Out the beat is dropped. Nothing fires when a phase or a
beat *ends* and no callback reports one finishing, so a loop your handler starts runs until you stop
it. Poll `presenter.IsIdle`, true when no beat is playing and none are queued, after `Tick`:

```csharp
presenter.Tick(Time.deltaTime);
foreach (var combatantId in myCombatantIds)
    if (presenter.Stage.TryGetToken(combatantId, out var token))
        token.GetComponentInChildren<Animator>()?.SetBool("Busy", !presenter.IsIdle);
```

`SkipAll()` fires every remaining phase of every queued beat at once and a raised `presenter.Speed`
can consume several beats in one `Tick`, so restart a loop idempotently - a bool or
`CrossFadeInFixedTime`, not counted `SetTrigger` calls.

## Use a VideoPlayer as an idle loop

The package has no video support of any kind: no video adapter, no `RenderTexture` management, no
synchronisation between video time and the visual clock. What follows is an ordinary animation
handler you write against `UnityEngine.Video`, and it is the whole integration.

```csharp
animation.Register("anim.idle", cue =>
{
    if (!presenter.Stage.TryGetToken(cue.SourceId, out var token)) return;
    var video = token.GetComponentInChildren<VideoPlayer>();
    if (video == null) return;
    video.isLooping = true;
    video.playbackSpeed = Mathf.Max(0.01f, presenter.Speed);
    if (!video.isPlaying) video.Play();
});
```

Prepare the clip before the battle or the first frames are blank, and expect to re-issue `Play`: a
pooled token is deactivated on release, which stops playback. One decoding `VideoPlayer` per
combatant is expensive, so a single video on a shared `RenderTexture` is usually the cheaper design.

## Anchor an effect to a formation anchor point

A slot carries up to 16 named **VFX anchors**, authored in the
[Formation Editor](place-formations.md). A beat reaches one through two fields on
[`PresentationBeatSpec`](../reference/presentation-adapters-and-recipes.md#presentationbeatspec):
`VfxAnchorKind` = [`PresentationVfxAnchorKind.Anchor`](../reference/presentation-adapters-and-recipes.md#presentationvfxanchorkind),
and `VfxAnchorId` = the anchor's id, which `Slot` and `Approach` ignore.

```csharp
var impact = new PresentationBeatSpec(     // the values the recipe Inspector writes into a beat
    durationRawSeconds: 2_500L,            // raw Fixed64: 10,000 is one second, capped at 30 s
    animationKey: "anim.hit", vfxKey: "vfx.slash",
    vfxAnchorKind: PresentationVfxAnchorKind.Anchor, vfxAnchorId: "anchor.chest",
    audioKey: "sfx.hit", floatingNumberStyle: FloatingNumberStyle.Damage, cameraShake: true);

var vfx = new BuiltInVfxAdapter(pool, log);
pool.RegisterPrototype("vfx.slash", slashPrefab);   // the art
vfx.RegisterKey("vfx.slash");                       // stops the key warning
```

The anchor resolves on the beat's **target**, or its source when the event has no target. Only an
empty or malformed `VfxAnchorId` falls back to the slot position; an id that parses but names no
anchor on that slot resolves to the world origin `(0,0,0)` - a silent success, not a failure, so an
effect that lands in the corner of the screen means a typo in the id rather than a missing anchor.
[`BuiltInVfxAdapter`](../reference/presentation-adapters-and-recipes.md#builtinvfxadapter) sets
position and parents the instance under the stage: no rotation is applied and nothing follows a
moving token, so read `cue.Facing` in an adapter of your own if you need either.

!!! warning "The built-in VFX adapter never releases what it spawns"
    Each pool key is capped at `BuiltInPoolAdapter.MaximumPerKey` (256) live instances. Past that,
    `Acquire` warns once, returns null, and the key stops appearing. Put a component on the effect
    prefab that calls `IPoolAdapter.Release(gameObject)` when the effect ends.

## Audio uses the same pattern

[`BuiltInAudioAdapter`](../reference/presentation-adapters-and-recipes.md#builtinaudioadapter)
registers and plays like the others, with clips in place of handlers.

```csharp
var audio = new BuiltInAudioAdapter(audioSource, log);
audio.Register("sfx.hit", hitClip);
```

`Play` is a `PlayOneShot` on that one shared source, so playback is non-positional: `IAudioAdapter`
receives a key and no cue. A key registered with a null clip counts as bound and is silent without
warning, an adapter with no source is silent for every key, and a skip can deliver many calls in one
frame - implement `IAudioAdapter` yourself for voice limiting or positional audio.

## Next

- **[Turn events into visuals](presentation-recipes.md)** - the keys, anchors and beats this page binds art to.
- **[Place combatants with the Formation Editor](place-formations.md)** - authoring the slot, approach and anchor points.
- **[Presentation adapters and recipes](../reference/presentation-adapters-and-recipes.md)** - every adapter type in full.
