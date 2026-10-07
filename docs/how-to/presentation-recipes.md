# Turn events into visuals

Every event the engine emits becomes exactly one presentation beat. A **Presentation Recipe**
decides what that beat looks and sounds like, and the four adapters you write turn its keys into
your own art.

## What a recipe maps

A recipe names one event type, narrows it with a selector, and carries three beats.

| Field | What it does |
| --- | --- |
| **Event Type Id** | The event this recipe reacts to, such as `damage.resolved` |
| **Selector Kind** | `Event Default`, `Skill Id`, `Skill Tag`, `Status Id`, `Status Tag` or `Reaction Id` |
| **Selector Value** | The exact ID or tag to match; left empty for `Event Default` |
| **In Beat**, **Impact Beat**, **Out Beat** | The three sets of cues, described below |

Recipes are collected in a **Presentation Recipe Set**: an explicit list of up to 1024 that
resolution reads and never scans past. None of it is compiled and none of it enters a hash, so
editing a recipe changes what a battle looks like and never what it does - see
[Determinism](../explanation/determinism.md).

### One recipe wins per event

Beats do not layer. For each event the resolver keeps the single most specific recipe whose event
type *and* selector both match: an exact `Skill Id`, `Status Id` or `Reaction Id` beats a
`Skill Tag` or `Status Tag`, which beats an `Event Default`. Ties go to the lower recipe stable ID,
compared ordinally, so the result never depends on list order or on Unity's load order.

A selector matches only when the event carries the property it names. Tags come from the compiled
skill or status definition, so one tag selector covers every mechanic you tagged.

| Selector kinds | Needs the property | Carried by, among others |
| --- | --- | --- |
| `Skill Id`, `Skill Tag` | `skill-id` | `cast.started`, `cast.completed`, `action.interrupted`, `target.retargeted` |
| `Status Id`, `Status Tag` | `status-id` | `status.applied`, `status.refreshed`, `status.removed`, `status.tick` |
| `Reaction Id` | `reaction-rule-id` | `reaction.enqueued`, `reaction.triggered`, `reaction.suppressed` |

!!! warning "A resolution event carries no skill ID"
    `damage.resolved` and `healing.resolved` name their source and target, not the skill that caused
    them, so a `Skill Id` selector aimed at either never matches. Aim skill-specific recipes at
    `cast.started` or `cast.completed` instead.

## The three beats

A mapped event plays **In**, then **Impact**, then **Out**, in that order. Each beat has its own
duration and its own cues, and a beat with no cues is a pause. **Duration Raw Seconds** is a raw
fixed-point value - **10,000 is one second** - clamped to the range 0 to 30 seconds, so a
mistyped duration shortens or lengthens a beat and never stalls the queue.

A beat fires its cues once, as it starts, then waits out its duration; a duration of `0` still
fires them and moves straight on. An event with no matching recipe becomes an instant beat that
fires nothing - which is what you see before authoring any recipes. Playback runs on the
presenter's visual clock, so `presenter.Speed` and `SkipAll()` change the pacing and never a
simulation value: see [Draw the battle on screen](../tutorials/show-the-battle.md).

## Keys, anchors and floating numbers

Beyond its duration, each beat carries five cue channels, and an empty key fires nothing.

| Field | Fires | Positioned at |
| --- | --- | --- |
| **Animation Key** | `IAnimationAdapter.Play` | the beat source's slot point |
| **Vfx Key** | `IVfxAdapter.Play` | the anchor below, on the target, or on the source when the event has no target |
| **Audio Key** | `IAudioAdapter.Play` | nowhere; audio receives a key only |
| **Floating Number Style** | a rise-and-fade number | the target's slot point, or the source's |
| **Camera Shake** | `presenter.CameraShakeCallback` | nowhere |

### Anchors

**Vfx Anchor Kind** picks which point of the resolved combatant's formation slot the effect spawns
at: `Slot` where the combatant stands, `Approach` for the slot's second point, or `Anchor` for the
named VFX anchor whose ID you put in **Vfx Anchor Id**. Those points are authored per slot in the
[Formation Editor](place-formations.md). An `Anchor` naming an ID no slot defines falls back to the
slot point rather than failing, as does any cue whose combatant the stage cannot place.

### Floating numbers

Size, rise, lifetime and easing come from the skin; the style picks the text and palette role.

| Style | Shown as | Colour role |
| --- | --- | --- |
| `Damage` | `120` | Negative |
| `Critical` | `120!`, at a larger size | Warning |
| `Heal` | `+40` | Positive |
| `Shield` | `+25` | Shield |
| `Resource` | `+3` | Accent Alt |
| `Status` | the amount, or `&#9679;` when it is zero | Accent |

!!! warning "A number needs an amount"
    One is spawned only when the event carries an `actual-delta` or `amount` integer. Resolution
    events do; the status events carry a stack delta instead, so a style set on those shows nothing.

## Adapters receive the keys

The keys are yours to define. You implement three cue interfaces, plus `IPoolAdapter`
(`Acquire`, `Release`, `ActiveCount`) for the instances they spawn:

```csharp
public interface IAnimationAdapter { void Play(string animationKey, PresentationCue cue); }
public interface IVfxAdapter       { void Play(string vfxKey, PresentationCue cue); }
public interface IAudioAdapter     { void Play(string audioKey); }
```

A `PresentationCue` carries `WorldPosition`, `Facing`, an optional `Parent` and the beat's
`SourceId` and `TargetId` - no engine reference and no authoritative value, so an adapter cannot
reach into the simulation. The package ships neutral implementations you bind art to:

```csharp
var pool = new BuiltInPoolAdapter(host.transform, log);
var vfx = new BuiltInVfxAdapter(pool, log);
pool.RegisterPrototype("particle-spark", sparkPrefab);
vfx.RegisterKey("particle-spark");
new BuiltInAnimationAdapter(log).Register("anim.hit", cue => { /* your flip-book */ });
new BuiltInAudioAdapter(audioSource, log).Register("sfx-hit", hitClip);
```

Keys are matched exactly and case-sensitively. An unbound key produces one warning through the
shared `PresentationLog` and then nothing, every later beat using it staying silent, so a missing
key costs you a visual and never a frame or an exception.

!!! note "Floating-number prototypes"
    Numbers are acquired from the pool under `presentation.floating.` plus the style name, such as
    `presentation.floating.Damage`. Register a prototype for that key to supply your own art;
    without one the presenter attaches a skinned label to a bare object. Each pool key is capped
    at 256 live instances.

## The starter recipe set

`Assets/TurnGauge/Samples/StarterContent/Recipes/StarterRecipeSet.asset` holds 16 recipes, all
`Event Default`, one each for `action.started`, `action.completed`, `cast.started`,
`cast.completed`, `damage.resolved`, `healing.resolved`, `resource.changed`, `shield.applied`,
`shield.changed`, `shield.removed`, `status.applied`, `status.removed`, `status.tick`,
`reaction.triggered`, `combatant.died` and `battle.ended`. It is what the demo scene runs: beat
durations of 0.1 to 0.25 seconds, `anim.` animation keys, `particle-` VFX keys, `sfx-` audio
keys, camera shake on the damage impact only.

!!! tip "Start by duplicating one"
    Recipes have no **Assets > Create** entry. Duplicate a starter recipe, press
    **Regenerate Stable ID** on the copy so the tie-break stays unambiguous, then add it to your
    own set. Point the presenter at your set and the starter set stops being read.

## Next

- **[Draw the battle on screen](../tutorials/show-the-battle.md)** - bind the set and the adapters.
- **[Place combatants with the Formation Editor](place-formations.md)** - author the points cues resolve to.
- **[Palette and surfaces](skin-surfaces.md)** - the palette roles numbers are coloured from.
