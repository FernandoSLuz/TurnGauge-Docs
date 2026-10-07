# Presentation adapters and recipes

17 types in this area.

!!! abstract "On this page"
    [BuiltInAnimationAdapter](#builtinanimationadapter) &middot; [BuiltInAudioAdapter](#builtinaudioadapter) &middot; [BuiltInPoolAdapter](#builtinpooladapter) &middot; [BuiltInVfxAdapter](#builtinvfxadapter) &middot; [FloatingNumberStyle](#floatingnumberstyle) &middot; [IAnimationAdapter](#ianimationadapter) &middot; [IAudioAdapter](#iaudioadapter) &middot; [IPoolAdapter](#ipooladapter) &middot; [IPoolPrototypeQuery](#ipoolprototypequery) &middot; [IVfxAdapter](#ivfxadapter) &middot; [PresentationBeatSpec](#presentationbeatspec) &middot; [PresentationCue](#presentationcue) &middot; [PresentationLog](#presentationlog) &middot; [PresentationRecipeDefinition](#presentationrecipedefinition) &middot; [PresentationRecipeSet](#presentationrecipeset) &middot; [PresentationSelectorKind](#presentationselectorkind) &middot; [PresentationVfxAnchorKind](#presentationvfxanchorkind)

## BuiltInAnimationAdapter

```csharp
public sealed class BuiltInAnimationAdapter : IAnimationAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/BuiltInPresentationAdapters.cs</small>

Neutral built-in animation adapter. Customers bind a stable-id key to a
handler (their own flip-book, Animator trigger, etc.). Out of the box no
keys are bound, so every key degrades to a single logged warning and a
no-op, never a gameplay effect. Fully replaceable per B6-08.

**Constructors**

`public BuiltInAnimationAdapter(PresentationLog log = null)`

:   Creates an adapter with nothing bound, so every key degrades until `Register` supplies a handler.
    - `log` &mdash; Shared warning ledger; null gives this adapter its own, which routes to the Unity console.

**Methods**

`public void Play(string animationKey, PresentationCue cue)`

:   Invokes the handler bound to `animationKey`. A null or empty key is ignored outright; an unbound key warns once through the log and then stays silent, so a render frame never throws.
    - `animationKey` &mdash; Ordinal key registered to an Animator trigger.
    - `cue` &mdash; Resolved participant and stage placement supplied to custom bindings.

`public void Register(string animationKey, Action<PresentationCue> handler)`

:   Binds a key to a neutral flip-book/animator handler.
    - `animationKey` &mdash; Authored key a beat names; null or empty throws, and re-registering a bound key replaces its handler.
    - `handler` &mdash; Invoked with the beat's cue each time the key plays; null throws.

---

## BuiltInAudioAdapter

```csharp
public sealed class BuiltInAudioAdapter : IAudioAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/BuiltInPresentationAdapters.cs</small>

Neutral built-in audio adapter. Registered keys map to a clip played
through an optional shared `AudioSource`; unknown keys
degrade to a single warning and a no-op.

**Constructors**

`public BuiltInAudioAdapter(AudioSource source = null, PresentationLog log = null)`

:   The audio adapter routes registered phase keys through one optional non-positional AudioSource.
    - `source` &mdash; Voice every one-shot plays through; with no source the adapter stays silent even for bound keys.
    - `log` &mdash; Shared warning ledger; null gives this adapter its own, which routes to the Unity console.

**Methods**

`public void Play(string audioKey)`

:   Plays the clip bound to `audioKey` as a one-shot on the shared source, so playback is non-positional. A null or empty key is ignored; an unbound key warns once and then stays silent.
    - `audioKey` &mdash; Ordinal sound binding named by the presentation phase.

`public void Register(string audioKey, AudioClip clip)`

:   Binds a key to a one-shot clip.
    - `audioKey` &mdash; Authored key; null or empty throws, and re-registering a bound key replaces its clip.
    - `clip` &mdash; Clip to play. A null clip is accepted: the key counts as bound and plays nothing, without a warning.

---

## BuiltInPoolAdapter

```csharp
public sealed class BuiltInPoolAdapter : IPoolAdapter, IPoolPrototypeQuery
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/BuiltInPresentationAdapters.cs</small>

Simple keyed GameObject pool. Instances are reused across acquire/release
cycles so open/close loops leak nothing. Each key is capped at
`MaximumPerKey` live instances; an over-cap acquire degrades
to a single warning and a null result rather than allocating forever.

**Constructors**

`public BuiltInPoolAdapter(Transform root = null, PresentationLog log = null)`

:   The built-in pool retains keyed prototypes, idle clones, live ownership, and per-key structural caps.
    - `root` &mdash; Parent given to freshly created instances and to anything released back; null leaves them at the scene root.
    - `log` &mdash; Shared warning ledger; null gives this pool its own, which routes to the Unity console.

**Fields**

`public const int MaximumPerKey`

:   Section 10 structural cap: pool size per key.

**Methods**

`public GameObject Acquire(string key)`

:   Hands out a live instance for `key`, reusing an idle one when there is one. A key with no registered prototype still succeeds: it yields a bare `GameObject` named after the key, which the caller has to give visuals of its own.
    - `key` &mdash; Pool channel to acquire from, reusing idle instances before cloning its prototype.
    - **Returns** &mdash; An active instance, or null when the key is null or empty or already holds `MaximumPerKey` live instances - hitting the cap warns once for that key.

`public int ActiveCount(string key)`

:   Instances handed out for a key and not yet released; zero for a null key or one that has never been acquired.
    - `key` &mdash; Pool channel whose unreleased checkout count is requested.
    - **Returns** &mdash; Live instance count for the key, or zero for null or unknown keys.

`public bool HasPrototype(string key)`

:   True when `RegisterPrototype` has bound a prototype to `key` and that prototype is still alive. A destroyed prototype reports false rather than true, so a scene teardown that took the source object with it degrades to the shared fallback instead of cloning a dead reference.
    - `key` &mdash; Prototype identity to inspect without creating or acquiring an instance.
    - **Returns** &mdash; when the exact key maps to a non-destroyed prototype.

`public int IdleCount(string key)`

:   Idle (recycled) instances retained for a key.
    - `key` &mdash; Pool channel whose recycled-instance count is requested.
    - **Returns** &mdash; Inactive retained instance count for the key, or zero for null or unknown keys.

`public void RegisterPrototype(string key, GameObject prototype)`

:   Binds a key to a prototype cloned on acquire.
    - `key` &mdash; Pool key; null or empty throws. Re-registering replaces the prototype without disturbing instances already handed out or idle.
    - `prototype` &mdash; Object cloned when no idle instance is available; null throws.

`public void Release(GameObject instance)`

:   Takes back an instance from `Acquire`: deactivates it, reparents it under the pool root, and keeps it for reuse rather than destroying it. A null instance, one this pool did not hand out, and a second release of the same instance are all ignored, so a duplicate release during teardown is harmless.
    - `instance` &mdash; Owned live checkout to deactivate, reparent, and return to its keyed idle stack.

---

## BuiltInVfxAdapter

```csharp
public sealed class BuiltInVfxAdapter : IVfxAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/BuiltInPresentationAdapters.cs</small>

Neutral built-in VFX adapter. Registered keys spawn a pooled instance of
a prototype at the cue position through the shared pool; unknown keys
degrade to a single warning and a no-op.

**Constructors**

`public BuiltInVfxAdapter(IPoolAdapter pool = null, PresentationLog log = null)`

:   The effect adapter borrows keyed instances from the optional pool and shares a log-once warning ledger.
    - `pool` &mdash; Source of the spawned instances; with no pool a registered key resolves quietly to nothing, since only unregistered keys warn.
    - `log` &mdash; Shared warning ledger; null gives this adapter its own, which routes to the Unity console.

**Methods**

`public void Play(string vfxKey, PresentationCue cue)`

:   Spawns a pooled instance for `vfxKey` at the cue. An unregistered key warns once and no-ops; a registered key with no pool, or one the pool has capped, does nothing at all. This adapter never releases what it acquired, so whoever owns the pool decides when the instance goes back.
    - `cue` &mdash; Placement for the effect; its parent, when set, adopts the instance without moving it.
    - `vfxKey` &mdash; Ordinal effect binding and pool key named by the presentation phase.

`public void RegisterKey(string vfxKey)`

:   Registers a VFX key as bound to art.
    - `vfxKey` &mdash; Authored key that should stop warning; null or empty throws. Registering the key does not supply the art - the pool prototype under the same key does.

---

## FloatingNumberStyle

```csharp
public enum FloatingNumberStyle
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Recipes/PresentationRecipeDefinition.cs</small>

Floating-number presentation style; purely cosmetic.

!!! note "Remarks"
    The presenter acquires every number from the pool adapter under the key
    `"presentation.floating."` plus the member name, so a host registers
    one prototype per style it wants to look different.

| Value | Meaning |
| --- | --- |
| `None` | No number spawns, even when the event carries an amount. |
| `Damage` | Health loss is shown with the skin's damage color and unsigned magnitude. |
| `Heal` | Restored health is shown with the skin's healing color and a positive prefix. |
| `Shield` | Shield gain or loss is shown with the skin's shield color. |
| `Resource` | Resource changes are shown with the skin's resource color. |
| `Status` | Status application or removal uses the skin's status-event color. |
| `Critical` | Critical impact uses enlarged text and the skin's critical color. |

---

## IAnimationAdapter

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IAnimationAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

Plays a keyed animation for a beat phase. Implementations bind the
stable-id key to their own art; a missing key must degrade silently.
The presenter calls this while replaying beats with no exception guard, so
an implementation must not throw and must not read or write battle state:
swapping the adapter has to leave the state hash, event chain, and result
byte-identical.

**Methods**

`public void Play(string animationKey, PresentationCue cue)`

:   Starts the animation bound to `animationKey`. Fires once per beat phase that names a key, which can be several times in a single frame when the visual clock is scaled up or beats are skipped.
    - `animationKey` &mdash; Authored key, never null or empty from the presenter; an unbound key must no-op rather than throw.
    - `cue` &mdash; Placement for this beat, passed by value. Its position is the beat source's stage slot, or (0,0,0) when that combatant has no resolved placement.

---

## IAudioAdapter

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IAudioAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

Plays a keyed one-shot sound. Timing is presentation-only. Implementations
must degrade an unknown key to a no-op instead of throwing, and must not
touch battle state: audio can never change a battle outcome.

**Methods**

`public void Play(string audioKey)`

:   Plays the sound bound to `audioKey`. No cue is supplied, so playback is non-positional. A skip or a sped-up clock can deliver many calls in one frame, so an implementation that cares about voice count must cap itself.
    - `audioKey` &mdash; Authored key, never null or empty from the presenter; an unbound key must no-op rather than throw.

---

## IPoolAdapter

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IPoolAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

Keyed instance pool for token views, floating numbers, and pooled VFX.
`Acquire` returns null when a key exceeds its structural
cap so the caller degrades visibly rather than allocating without bound.
The presenter and the stage release everything they acquired on teardown,
so an implementation must survive repeated acquire/release cycles without
leaking instances and without destroying them.

**Methods**

`public GameObject Acquire(string key)`

:   Hands out a live instance for `key`, reusing a previously released one when there is one. An implementation must return null once the key is at its cap rather than allocate without bound; every caller in the package reads null as "skip this visual" and carries on.
    - `key` &mdash; Pool channel or prototype identity to check out.
    - **Returns** &mdash; An active instance the caller may reposition, reparent, and add components to, or null when the key is capped.

`public int ActiveCount(string key)`

:   Instances acquired for `key` and not yet released. A key that has never been acquired reports zero rather than throwing.
    - `key` &mdash; Pool channel whose unreleased instance count is requested.
    - **Returns** &mdash; The number of live checkouts for the key, or zero when the key is unknown.

`public void Release(GameObject instance)`

:   Takes back an instance from `Acquire`. An implementation must deactivate and retain it for reuse rather than destroy it, and must ignore a null instance or one it does not own, so a duplicate release during teardown is harmless.
    - `instance` &mdash; Previously acquired object to deactivate and retain for reuse.

---

## IPoolPrototypeQuery

```csharp
public interface IPoolPrototypeQuery
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

An optional capability a pool may add: answering whether it holds a
prototype for a key, without acquiring one.

It exists because `IPoolAdapter.Acquire` is allowed to
fabricate an empty instance for an unregistered key, so "acquire and check
for null" cannot distinguish a registered prototype from a blank
stand-in. The stage uses this to decide whether a combatant has art of its
own before it commits to a key.

Implementing it is optional. A pool that does not is treated as holding
nothing specific, which is exactly the behaviour every project had before
per-combatant art existed.

**Methods**

`public bool HasPrototype(string key)`

:   True when a prototype has been registered for `key`. Must not acquire, allocate, or mutate anything.
    - `key` &mdash; Prototype identity to inspect without checking out an instance.
    - **Returns** &mdash; only when a live registered prototype exists for the exact key.

---

## IVfxAdapter

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IVfxAdapter
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

Plays a keyed one-shot visual effect at the cue position. Implementations
bind the key to their own art and must treat an unknown key as a no-op,
never an exception, since the presenter calls this unguarded. Effects are
cosmetic only and must never feed back into anything authoritative.

**Methods**

`public void Play(string vfxKey, PresentationCue cue)`

:   Spawns the effect bound to `vfxKey`. Fires once per beat phase that names a key, and may fire several times in one frame when beats are skipped or the visual clock is scaled up.
    - `vfxKey` &mdash; Authored key, never null or empty from the presenter; an unbound key must no-op rather than throw.
    - `cue` &mdash; Anchor the phase asked for, resolved against the beat's target or its source when there is no target; the position is (0,0,0) when neither resolves.

---

## PresentationBeatSpec

```csharp
public sealed class PresentationBeatSpec
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Recipes/PresentationRecipeDefinition.cs</small>

One of the three fixed beats (In / Impact / Out) of a recipe. Timing is
a raw Fixed64 seconds value bounded to the section 10 cap; every field is
non-authoritative and never enters any battle hash.

**Constructors**

`public PresentationBeatSpec()`

:   Creates an instant, silent beat: zero duration, no animation, VFX or audio key, no floating number and no camera shake. This is what an unauthored beat of a recipe reads as.

`public PresentationBeatSpec()`

:   Creates a beat from authored values. Nothing is validated or clamped here: the duration is stored exactly as given and only clamped when read, and null keys are stored as empty strings.
    - `durationRawSeconds` &mdash; Beat length in raw Fixed64 seconds. May exceed the 0..30 s cap, in which case `ExceedsDurationCap` reports it.
    - `animationKey` &mdash; Key handed to the animation adapter; empty plays no animation.
    - `vfxKey` &mdash; Key handed to the VFX adapter; empty plays no VFX.
    - `vfxAnchorKind` &mdash; Which slot point the VFX plays at.
    - `vfxAnchorId` &mdash; Formation anchor id, consulted only when `vfxAnchorKind` is `PresentationVfxAnchorKind.Anchor`.
    - `audioKey` &mdash; Key handed to the audio adapter; empty plays no sound.
    - `floatingNumberStyle` &mdash; The number style for this beat, or `FloatingNumberStyle.None` for no number.
    - `cameraShake` &mdash; True to request a camera shake; the host's optional shake sink decides what that looks like.

`public PresentationBeatSpec()`

:   Creates a beat that also names the style to use when the hit was a critical. Identical to the shorter form otherwise, which leaves the critical style at `FloatingNumberStyle.Critical`.
    - `durationRawSeconds` &mdash; Beat length in raw Fixed64 seconds.
    - `animationKey` &mdash; Key handed to the animation adapter; empty plays no animation.
    - `vfxKey` &mdash; Key handed to the VFX adapter; empty plays no VFX.
    - `vfxAnchorKind` &mdash; Which slot point the VFX plays at.
    - `vfxAnchorId` &mdash; Formation anchor id, consulted only when `vfxAnchorKind` is `PresentationVfxAnchorKind.Anchor`.
    - `audioKey` &mdash; Key handed to the audio adapter; empty plays no sound.
    - `floatingNumberStyle` &mdash; The number style for an ordinary hit, or `FloatingNumberStyle.None` for no number at all.
    - `criticalNumberStyle` &mdash; The number style for a critical hit. `FloatingNumberStyle.None` draws criticals in the ordinary style rather than suppressing them.
    - `cameraShake` &mdash; True to request a camera shake.

**Properties**

`public string AnimationKey`

:   Animation adapter key; empty means the presenter plays none.

`public string AudioKey`

:   Audio adapter key; empty means the presenter plays none.

`public bool CameraShake`

:   True when the beat requests a camera shake. It is only a request: the presenter forwards it to the host's optional shake sink.

`public long ClampedDurationRaw`

:   Raw duration clamped to the 0..30 s structural cap.

`public FloatingNumberStyle CriticalNumberStyle`

:   The style a critical hit's number is drawn in instead. It applies only when the event itself reported a critical, so a beat can keep one look for ordinary hits and another for big ones without the recipe having to declare a whole skill critical.

`public long DurationRawSeconds`

:   Raw Fixed64 seconds as authored (may be out of range).

`public float DurationSeconds`

:   Clamped duration expressed in presentation seconds.

`public bool ExceedsDurationCap`

:   True when the authored duration exceeds the structural cap.

`public FloatingNumberStyle FloatingNumberStyle`

:   The number style to spawn; a number appears only when the source event also carries an amount.

`public string VfxAnchorId`

:   Formation anchor id, read only when `VfxAnchorKind` is `PresentationVfxAnchorKind.Anchor`.

`public PresentationVfxAnchorKind VfxAnchorKind`

:   Which point of the occupant's formation slot this beat's VFX plays at. Only `PresentationVfxAnchorKind.Anchor` reads `VfxAnchorId`; the other kinds resolve from the slot alone, so a beat authored against a slot works on any preset.

`public string VfxKey`

:   VFX adapter key; empty means the presenter plays none.

**Fields**

`public const long MaximumDurationRaw`

:   Section 10 cap: presentation beat duration is 0..30 s.

**Methods**

`public FloatingNumberStyle ResolveFloatingNumberStyle(PresentationBeatContext context)`

:   Picks the number style for one beat's context.
    - `context` &mdash; The beat being played; only its critical flag is read.
    - **Returns** &mdash; `CriticalNumberStyle` for a critical hit and `FloatingNumberStyle` otherwise. A beat that draws no number at all keeps drawing none, because a critical is a reason to draw the number differently and never a reason to introduce one.

---

## PresentationCue

```csharp
public readonly struct PresentationCue
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

Immutable spatial context handed to a visual adapter. It carries the
world placement resolved by the stage plus the participant identifiers
for the beat, never any authoritative value or engine reference.

**Constructors**

`public PresentationCue()`

:   Creates a cue from an already-resolved placement. The cue carries placement and identity only, never an authoritative battle value.
    - `parent` &mdash; Optional parent for spawned instances; null leaves them unparented.
    - `sourceId` &mdash; Beat source, or the default id when the beat has no source.
    - `targetId` &mdash; Beat target, or the default id when the beat has no target.
    - `facing` &mdash; Compiled formation direction the spawned visual should face.
    - `worldPosition` &mdash; Resolved stage position where the adapter should play the cue.

**Properties**

`public FormationFacing Facing`

:   Facing derived from the compiled formation slot.

`public Transform Parent`

:   Optional parent for spawned instances; may be null.

`public StableId SourceId`

:   Beat source identifier; may be the default (invalid) id.

`public StableId TargetId`

:   Beat target identifier; may be the default (invalid) id.

`public Vector3 WorldPosition`

:   Stage-space position the adapter should present at.

---

## PresentationLog

```csharp
public sealed class PresentationLog
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Adapters/PresentationAdapters.cs</small>

Non-authoritative, log-once warning ledger shared by the presenter and
its adapters. A missing adapter key degrades to a single warning per
key so a render frame never spams the console or throws.

**Constructors**

`public PresentationLog(Action<string> sink = null)`

:   Creates a ledger that forwards each first-time warning to `sink`.
    - `sink` &mdash; Receiver for warning text; null routes to the Unity console through Debug.LogWarning.

**Properties**

`public int WarningCount`

:   Distinct keys that have produced a warning so far.

**Methods**

`public bool HasWarnedFor(string key)`

:   Reports whether a warning has already been recorded for `key`, without recording one.
    - `key` &mdash; Exact adapter or recipe key whose warning-ledger membership is queried.
    - **Returns** &mdash; True once `WarnOnce` has fired for that exact key; always false for a null key, which `WarnOnce` dedupes under the empty string instead.

`public void WarnOnce(string key, string message)`

:   Emits at most one warning per `key`. Subsequent calls with the same key are silently ignored (documented degrade).
    - `key` &mdash; Ordinal deduplication key; null shares the empty-string ledger entry.
    - `message` &mdash; Warning text sent only for the key's first occurrence; null falls back to the key.

---

## PresentationRecipeDefinition

```csharp
public sealed class PresentationRecipeDefinition : StableIdDefinition
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Recipes/PresentationRecipeDefinition.cs</small>

A stable-id presentation recipe (In / Impact / Out beats) authored as a
B4-style ScriptableObject. Recipes are excluded from B3 compilation and
from every authoritative hash; editing one can never change a simulation
output. Selectors bind an event type plus an optional mechanic id or tag.

**Properties**

`public string EventTypeIdRaw`

:   Raw serialized event type id the recipe reacts to.

`public PresentationBeatSpec ImpactBeat`

:   The impact beat; never null, unauthored it reads as instant.

`public PresentationBeatSpec InBeat`

:   The wind-up beat; never null, unauthored it reads as instant.

`public PresentationBeatSpec OutBeat`

:   The recovery beat; never null, unauthored it reads as instant.

`public PresentationSelectorKind SelectorKind`

:   What this recipe narrows its event type down to: an exact mechanic id, a tag, or nothing further. It also fixes the recipe's `SelectorSpecificity`, so it is what settles which recipe wins when several match the same event.

`public int SelectorSpecificity`

:   Deterministic specificity rank: exact id (3) beats tag (2) beats event default (1). Higher wins; ties break by recipe stable id.

`public string SelectorValueRaw`

:   Raw serialized exact-id or tag value; empty for defaults.

**Methods**

`public PresentationBeatSpec GetBeat(int phaseIndex)`

:   Fetches the beat for a fixed phase index (0=In,1=Impact,2=Out).
    - `phaseIndex` &mdash; The phase to read; only 0, 1 and 2 are valid.
    - **Returns** &mdash; The recipe's own beat instance, not a copy, so it stays valid only as long as the recipe asset does.

`public bool TryGetEventTypeId(out StableId id)`

:   Parses the event type id; false when it is unset or invalid. A recipe whose event id does not parse can never win resolution.
    - `id` &mdash; The parsed id, or the default id on failure.
    - **Returns** &mdash; True when the raw event type id parsed.

`public bool TryGetSelectorValue(out StableId id)`

:   Parses the selector value; false for defaults or bad ids.
    - `id` &mdash; The parsed id or tag, or the default id on failure.
    - **Returns** &mdash; True when the raw selector value parsed. False is normal for an `PresentationSelectorKind.EventDefault` recipe, which matches without reading the value at all.

---

## PresentationRecipeSet

```csharp
public sealed class PresentationRecipeSet : StableIdDefinition
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Recipes/PresentationRecipeSet.cs</small>

An explicit, ordered list of presentation recipes. Resolution reads only
this list and never scans the project, so a set is a closed, reviewable
unit of skinnable content. The set is non-authoritative and never enters
any battle hash.

**Properties**

`public bool ExceedsRecipeCap`

:   True when the set exceeds its structural cap.

`public IReadOnlyList<PresentationRecipeDefinition> Recipes`

:   The explicit recipe list in authored order.

**Fields**

`public const int MaximumRecipes`

:   Section 10 structural cap: recipes per set.

**Methods**

`public static PresentationRecipeSet CreateTransient()`

:   Creates a non-persistent recipe set for runtime composition. The caller owns and must destroy the returned ScriptableObject.
    - `authoredRecipes` &mdash; Recipe assets copied into serialized order; null produces an empty set.
    - `stableIdRaw` &mdash; Unvalidated identity text assigned to the transient set.
    - **Returns** &mdash; A caller-owned, unsaved ScriptableObject containing the supplied recipe references.

---

## PresentationSelectorKind

```csharp
public enum PresentationSelectorKind
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Recipes/PresentationRecipeDefinition.cs</small>

How a recipe selector narrows an event to a specific mechanic. The
deterministic specificity ordering is exact id > tag > event
default, matching `PresentationRecipeResolver`.

| Value | Meaning |
| --- | --- |
| `EventDefault` | Matches every event of the recipe's event type, whatever mechanic it names. |
| `SkillId` | Matches presentation recipes by skill ID before the event-default fallback. |
| `SkillTag` | Matches presentation recipes by skill tag before the event-default fallback. |
| `StatusId` | Matches presentation recipes by status ID before the event-default fallback. |
| `StatusTag` | Matches presentation recipes by status tag before the event-default fallback. |
| `ReactionId` | Matches presentation recipes by reaction ID before the event-default fallback. |

---

## PresentationVfxAnchorKind

```csharp
public enum PresentationVfxAnchorKind
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Recipes/PresentationRecipeDefinition.cs</small>

Where a beat's VFX anchors, resolved through the compiled slot.

| Value | Meaning |
| --- | --- |
| `Slot` | The combatant's slot position; also the fallback anchor. |
| `Approach` | The approach point authored on the combatant's slot. |
| `Anchor` | A named VFX anchor of the slot, chosen by the beat's anchor id. |

---

