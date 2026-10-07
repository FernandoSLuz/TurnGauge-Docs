# The perform moment

13 types in this area.

!!! abstract "On this page"
    [BackdropBlurPerformModule](#backdropblurperformmodule) &middot; [BloomPulsePerformModule](#bloompulseperformmodule) &middot; [BodyShakePerformModule](#bodyshakeperformmodule) &middot; [CameraShakePerformModule](#camerashakeperformmodule) &middot; [CameraZoomPerformModule](#camerazoomperformmodule) &middot; [FocusPerformModule](#focusperformmodule) &middot; [IPerformBeatModule](#iperformbeatmodule) &middot; [PerformBeatPhase](#performbeatphase) &middot; [PerformFeelPreset](#performfeelpreset) &middot; [PerformModuleBase](#performmodulebase) &middot; [PerformPhaseContext](#performphasecontext) &middot; [SkillAnnouncementPerformModule](#skillannouncementperformmodule) &middot; [VignettePulsePerformModule](#vignettepulseperformmodule)

## BackdropBlurPerformModule

```csharp
public sealed class BackdropBlurPerformModule : IPerformBeatModule
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Pulls focus for the whole perform: the background goes out of focus as the skill winds
up and comes back as it closes.

This is the richer alternative to `FocusPerformModule`, which separates the
participants by tinting everyone else. The two compose -- run both and non-participants
dim while the world behind them softens -- or drop the tint and keep only this.

Unlike the bloom and vignette modules, it does not follow the shipped
`PerformModuleBase` decay curve, because a blur is not a hit accent: it
belongs across the whole moment rather than as a spike on impact. It ramps in on the
opening phase, holds, and eases out on the closing one, which is the same shape
`FocusPerformModule` uses.

`BattleStageBackdrop` uses a secondary camera rather than an image effect.
Verify capture behavior in your project's render pipeline before enabling this module.

**Constructors**

`public BackdropBlurPerformModule(BattleStageBackdrop stageBackdrop, PerformFeelPreset performFeel = null)`

:   Creates the module for a backdrop component; null makes it inert.
    - `performFeel` &mdash; Backdrop blur amount, transition, and hold tuning; null uses package defaults.
    - `stageBackdrop` &mdash; Stage backdrop receiving the non-authoritative blur strength; null disables the module.

**Properties**

`public float CurrentStrength`

:   The strength currently written to the backdrop, 0 at rest.

**Methods**

`public void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

`public void Reset()`

:   &mdash;

`public void Tick(float presentationDeltaSeconds)`

:   &mdash;

---

## BloomPulsePerformModule

```csharp
public sealed class BloomPulsePerformModule : PerformModuleBase
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Adds a burst of bloom on impact, over whatever the optional bloom component
is resting at.

Built-in render pipeline only, because that is all
`BattleStageBloom` supports. Under URP or HDRP the bloom
component disables itself and this module goes quiet with it rather than
pretending to work - use that pipeline's own volume overrides instead.

**Constructors**

`public BloomPulsePerformModule(BattleStageBloom stageBloom, PerformFeelPreset feel = null)`

:   Creates the module for a bloom component; null makes it inert.
    - `feel` &mdash; Bloom pulse amount and duration tuning; null uses package defaults.
    - `stageBloom` &mdash; Pipeline-neutral stage bloom component to pulse and restore; null disables the module.

**Methods**

`public override void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

---

## BodyShakePerformModule

```csharp
public sealed class BodyShakePerformModule : PerformModuleBase
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Jolts the combatant that was struck, so a hit reads on the body as well as
in the numbers.

Transform only, so it is pipeline independent. The token is put back exactly
where the stage placed it, which matters because the stage owns that position
and will not recompute it.

**Constructors**

`public BodyShakePerformModule(PerformFeelPreset feel = null)`

:   Impact phases shake the struck combatant token and restore its exact local position when playback settles.
    - `feel` &mdash; Body-shake duration and strength tuning; null uses package defaults.

**Methods**

`public override void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

---

## CameraShakePerformModule

```csharp
public sealed class CameraShakePerformModule : PerformModuleBase
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Shakes the battle camera when a phase asks for it.

Works in every render pipeline, because it moves a transform rather than
touching post-processing. The camera is returned to exactly where it started,
so this composes with a project that moves the camera for its own reasons
only if that project does not move it during a shake.

**Constructors**

`public CameraShakePerformModule(Transform cameraTransform, PerformFeelPreset feel = null)`

:   Creates the module for a camera transform; null makes it inert.
    - `cameraTransform` &mdash; Camera transform displaced locally during authored shake phases; null disables the module.
    - `feel` &mdash; Camera-shake duration and strength tuning; null uses package defaults.

**Methods**

`public override void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

`public override void Reset()`

:   &mdash;

---

## CameraZoomPerformModule

```csharp
public sealed class CameraZoomPerformModule : PerformModuleBase
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Pushes the camera in through the impact and releases it afterwards.

Orthographic only, which is what the shipped stage uses. A perspective
camera is left alone rather than moved in a way the project did not ask for.

**Constructors**

`public CameraZoomPerformModule(Camera camera, PerformFeelPreset feel = null)`

:   Creates the module for a camera; null, or a perspective camera, makes it inert.
    - `camera` &mdash; Orthographic battle camera whose size is pulsed; null or perspective cameras disable the module.
    - `feel` &mdash; Zoom amount and duration tuning; null uses package defaults.

**Methods**

`public override void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

`public override void Reset()`

:   &mdash;

---

## FocusPerformModule

```csharp
public sealed class FocusPerformModule : IPerformBeatModule
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/AnnouncementPerformModules.cs</small>

Dims everyone not taking part, so the eye goes to the combatants the action
concerns.

This is the cheap, dependable version of a focus pull: it tints sprite
renderers rather than blurring the frame, so it costs nothing, works in every
render pipeline, and cannot conflict with a project's own post-processing. A
project that wants a true background blur can replace this module with one of
its own and keep everything else.

Every tint is restored on reset, including when a player skips the animation
mid-perform, because a combatant left dimmed reads as a bug for the rest of
the battle.

**Constructors**

`public FocusPerformModule(PerformFeelPreset performFeel = null)`

:   The focus module uses the supplied feel tuning, or package defaults, to dim uninvolved combatants during opening and impact.
    - `performFeel` &mdash; Tuning; null uses the shipped defaults.

**Properties**

`public int DimmedCount`

:   How many combatants are currently dimmed.

**Methods**

`public void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

`public void Reset()`

:   &mdash;

`public void Tick(float presentationDeltaSeconds)`

:   &mdash;

---

## IPerformBeatModule

```csharp
public interface IPerformBeatModule
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/IPerformBeatModule.cs</small>

One step of the perform moment: the announcement, the focus pull, the shake,
the return, or anything a project invents.

This is the seam that makes the perform moment yours. The package ships a
module per effect and runs them in list order; add, remove, reorder, or
replace them and the feel changes without a line of package code being
touched. It is the same bargain as the presentation adapters: implement a
small interface, register it, and the presenter drives it.

A module is presentation only. It runs after the simulation has already
decided the outcome, it may be skipped entirely when a player fast-forwards,
and it must therefore never be the place where anything authoritative
happens.

**Methods**

`public void OnPhaseBegin(PerformPhaseContext context)`

:   Called once as each phase begins, in registration order. Throwing here is contained by the presenter and reported, and the remaining modules still run, so one broken module cannot take the battle down with it.
    - `context` &mdash; Beat, phase, presenter, and resolved world positions available to the module.

`public void Reset()`

:   Called when playback is torn down or fast-forwarded past. Put the world back: a module that has moved a camera or tinted a sprite must undo it here, or the effect leaks into the next battle.

`public void Tick(float presentationDeltaSeconds)`

:   Called every presentation tick while the battle is playing, already scaled by the presenter's speed. Use it to advance a shake, a zoom, or a fade; a module with nothing to advance can leave it empty.
    - `presentationDeltaSeconds` &mdash; Elapsed presentation time, never negative.

---

## PerformBeatPhase

```csharp
public enum PerformBeatPhase
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/PerformFeelPreset.cs</small>

The parts of one impact, in the order a player reads them.

They are phases of a single beat rather than separate effects, which is the
whole point: an impact that lands, is counted, and is booked in that order
reads as one event, while the same five things on five independent timers
read as five things that happened to coincide.

| Value | Meaning |
| --- | --- |
| `Flash` | The hit itself: camera shake, bloom, vignette. |
| `Body` | The struck body's jolt and settle, riding the flash. |
| `NumberArc` | The number leaving the body, just after the hit registers. |
| `BarDrain` | The bar travelling to its new value, trailing the number. |
| `Banner` | The banner naming what happened, over the consequence. |
| `ChipReorder` | The turn order re-sorting, last, once the damage has read. |

---

## PerformFeelPreset

```csharp
public sealed class PerformFeelPreset : ScriptableObject
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/PerformFeelPreset.cs</small>

One asset holding how the perform moment feels: how long the skill title
holds, how far the camera pushes in, how hard the impact hits, how the world
behind the action recedes.

It is deliberately separate from the recipes. A recipe says what
happens on an event - which animation key, which effect, which sound. This
says how much, once, for the whole game. Tuning the feel is then a
handful of sliders on a single asset rather than an edit across every
recipe, and a project can ship several and swap them per chapter.

Nothing here can reach the simulation. Every value is presentation only, so
no amount of tuning can change a battle's outcome or its event-chain digest.

**Properties**

`public float BackdropBlur`

:   How far the background goes out of focus while a skill performs; zero disables the backdrop blur.

`public float BackdropBlurSeconds`

:   Seconds to pull focus in, and the same to let it back out.

`public float BloomPulse`

:   Extra bloom intensity added at impact.

`public float BloomPulseSeconds`

:   Seconds for the bloom pulse to decay, with the rest of the flash.

`public float BodyShakeSeconds`

:   Seconds for a struck body to settle, riding the flash.

`public float BodyShakeStrength`

:   Body jolt amplitude in world units; zero disables the body shake.

`public float CameraShakeSeconds`

:   Seconds for a camera shake to decay to nothing. Choreographed: the camera, the bloom, and the vignette are one flash and decay together, because three decays of 0.28, 0.30 and 0.34 seconds is not three ideas - it is one idea arriving three times.

`public float CameraShakeStrength`

:   Camera shake amplitude in world units.

`public bool ChoreographToBeat`

:   Whether the impact effects are placed inside `ImpactBeatSeconds`. Off restores the pre-choreography behaviour, where each effect ran its own independent duration.

`public float FocusDim`

:   How far non-participants dim during a perform; zero disables the focus pull.

`public float FocusFadeSeconds`

:   Seconds to reach full dim and to release it.

`public float ImpactBeatSeconds`

:   How long one whole impact lasts. Every phase is placed inside it, so this is the single number that retimes the choreography.

`public float TitleFadeSeconds`

:   Fade in and out time for the skill title, never more than half the hold.

`public float TitleHoldSeconds`

:   How long the skill title holds; zero hides it.

`public float VignettePulse`

:   Extra corner darkening added at impact. Added to the bloom component's resting vignette and clamped there, so a stage already at full vignette pulses no further rather than overshooting.

`public float VignettePulseSeconds`

:   Seconds for the vignette pulse to decay, with the rest of the flash.

`public float ZoomAmount`

:   Fraction the camera pushes in at impact; zero disables the zoom.

**Methods**

`public float BeatOnsetSeconds(PerformBeatPhase phase)`

:   How far into the beat `phase` starts.
    - `phase` &mdash; The phase to place. An unknown value starts at the downbeat.
    - **Returns** &mdash; Seconds from the start of the beat, or zero when choreography is off.

`public float BeatSpanSeconds(PerformBeatPhase phase)`

:   How long `phase` runs for.
    - `phase` &mdash; The phase to measure. An unknown value takes the whole beat.
    - **Returns** &mdash; Seconds, or the whole beat when the phase is unknown. Choreography off returns the beat unchanged, because a caller asking for a span still needs a duration to animate over.

`public static PerformFeelPreset CreateDefault()`

:   The shipped defaults, as a throwaway instance. Used when a project wires no asset, so the modules still have sensible numbers rather than zeroes that would silently disable every effect.
    - **Returns** &mdash; A transient preset carrying the package's serialized field defaults.

---

## PerformModuleBase

```csharp
public abstract class PerformModuleBase : IPerformBeatModule
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Shared plumbing for the shipped modules: a feel preset that is never null,
and a decaying timer, which is the shape almost every piece of juice takes.

Deriving from this is optional. A project's own module only has to implement
`IPerformBeatModule`; this exists to keep the shipped ones short
enough to read as examples.

**Methods**

`public abstract void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

`public virtual void Reset()`

:   &mdash;

`public virtual void Tick(float presentationDeltaSeconds)`

:   &mdash;

---

## PerformPhaseContext

```csharp
public readonly struct PerformPhaseContext
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/IPerformBeatModule.cs</small>

Everything a perform module is told about the phase it is reacting to.

Passed by value and never retained by the presenter, so a module may keep a
copy. Nothing here is authoritative: a module reads the simulation's decision
and stages it, and can never change what happened.

**Constructors**

`public PerformPhaseContext()`

:   Creates a phase context. The presenter builds these; a test may build one directly.
    - `beat` &mdash; Simulation event context being staged by the current presentation beat.
    - `phaseIndex` &mdash; Zero-based in, impact, or out phase index.
    - `presenter` &mdash; Presenter whose stage resolves combatant tokens and anchors.
    - `sourceWorld` &mdash; World position of the acting combatant, or zero when unresolved.
    - `spec` &mdash; Authored timing, adapter keys, and shake settings for this phase.
    - `targetWorld` &mdash; World position of the target, falling back to the source position.

**Properties**

`public PresentationBeatContext Beat`

:   What the simulation reported: the event type, the actors, the skill, and the amount where one applies. `SkillId` is what an announcement module puts on screen.

`public bool IsImpact`

:   True for the impact phase, which is where most juice belongs.

`public int PhaseIndex`

:   Which of the three phases this is: 0 in, 1 impact, 2 out.

`public BattlePresenter Presenter`

:   The presenter driving playback. Its `Stage` resolves tokens and anchors.

`public Vector3 SourceWorld`

:   Stage position of the acting combatant, or zero when it has no token.

`public PresentationBeatSpec Spec`

:   The authored phase being played, including its duration, keys, and the camera-shake request. A module may read these to stay in step with the authored timing rather than inventing its own.

`public Vector3 TargetWorld`

:   Stage position of the target, falling back to the source when the event has none.

---

## SkillAnnouncementPerformModule

```csharp
public sealed class SkillAnnouncementPerformModule : IPerformBeatModule
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/AnnouncementPerformModules.cs</small>

Puts the performed skill's name on screen as the action opens.

This is the announcement half of the perform moment. It fires on the opening
phase rather than on impact, so the card is up before the blow lands and the
player reads what is coming instead of what already happened.

The name comes from the display-string table, so it is whatever the project
localized it to; an unmapped skill falls back to its id rather than showing
nothing, which makes a missing string visible instead of silent.

**Constructors**

`public SkillAnnouncementPerformModule()`

:   The skill-title card is bound to opening phases, with raw skill IDs used when no display label exists.
    - `titleView` &mdash; Card to drive; null makes the module inert.
    - `displayStrings` &mdash; Table skill ids are resolved through; null falls back to raw ids.
    - `performFeel` &mdash; Tuning; null uses the shipped defaults.

**Methods**

`public void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

`public void Reset()`

:   &mdash;

`public void Tick(float presentationDeltaSeconds)`

:   &mdash;

---

## VignettePulsePerformModule

```csharp
public sealed class VignettePulsePerformModule : PerformModuleBase
```

`TurnGauge.Presentation` &middot; <small>TurnGauge/Runtime/Presentation/Perform/BuiltInPerformModules.cs</small>

Closes the frame in on impact by pulsing the optional stage vignette, then
eases it back to the strength the component is resting at.

The counterpart to `BloomPulsePerformModule`, and useful without
it: a vignette pulse reads as the stage tightening around the hit rather than
brightening, which suits a darker skin where more bloom would only wash the
frame out. The two compose -- run both for a hit that flares and closes in.

Nothing here requires the bloom to be on. `BattleStageBloom` draws
the vignette independently of its bloom intensity, so a project can set that
to zero and use this component purely as a vignette.

Built-in render pipeline only, for the same reason as the bloom pulse: under
URP or HDRP the component disables itself and this module goes quiet with it
instead of pretending to work. Use that pipeline's own Vignette volume
override there.

**Constructors**

`public VignettePulsePerformModule(BattleStageBloom stageBloom, PerformFeelPreset feel = null)`

:   Creates the module for a bloom component; null makes it inert.
    - `feel` &mdash; Vignette pulse amount and duration tuning; null uses package defaults.
    - `stageBloom` &mdash; Stage bloom component whose vignette strength is pulsed and restored.

**Methods**

`public override void OnPhaseBegin(PerformPhaseContext context)`

:   &mdash;

---

