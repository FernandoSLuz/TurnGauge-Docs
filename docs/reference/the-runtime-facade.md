# The runtime facade

19 types in this area.

!!! abstract "On this page"
    [AudioBinding](#audiobinding) &middot; [BattleRuntimeCheckpoint](#battleruntimecheckpoint) &middot; [BattleRuntimeController](#battleruntimecontroller) &middot; [BattleRuntimeEndReason](#battleruntimeendreason) &middot; [BattleRuntimeEndedEvent](#battleruntimeendedevent) &middot; [BattleRuntimeEventsEvent](#battleruntimeeventsevent) &middot; [BattleRuntimeFailedEvent](#battleruntimefailedevent) &middot; [BattleRuntimeFailure](#battleruntimefailure) &middot; [BattleRuntimeHumanControlRequirement](#battleruntimehumancontrolrequirement) &middot; [BattleRuntimeOperationResult](#battleruntimeoperationresult) &middot; [BattleRuntimePacing](#battleruntimepacing) &middot; [BattleRuntimeSeedPolicy](#battleruntimeseedpolicy) &middot; [BattleRuntimeSnapshotCause](#battleruntimesnapshotcause) &middot; [BattleRuntimeSnapshotEvent](#battleruntimesnapshotevent) &middot; [BattleRuntimeStartedEvent](#battleruntimestartedevent) &middot; [BattleRuntimeState](#battleruntimestate) &middot; [BattleRuntimeUnityEvent](#battleruntimeunityevent) &middot; [BattleRuntimeValueResult](#battleruntimevalueresult) &middot; [VfxBinding](#vfxbinding)

## AudioBinding

```csharp
public sealed class AudioBinding
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeController.cs</small>

Maps one presentation audio key to a Unity audio clip.

---

## BattleRuntimeCheckpoint

```csharp
public sealed class BattleRuntimeCheckpoint
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Persistable battle restore point. The battle state is canonical bytes and
the three hashes pin it to one compiled encounter.

**Constructors**

`public BattleRuntimeCheckpoint()`

:   Creates a restore point, usually from external persisted fields. All identity fields are validated and the state payload is defensively copied.
    - `encounterId` &mdash; Exact encounter the state belongs to.
    - `seed` &mdash; Seed originally used to create the battle.
    - `contentManifestHash` &mdash; Compiled content manifest hash.
    - `compiledSnapshotHash` &mdash; Compiled catalog snapshot hash.
    - `startRequestHash` &mdash; Selected encounter start-request hash.
    - `stateBytes` &mdash; Non-empty canonical battle-state bytes.

**Properties**

`public Sha256Digest CompiledSnapshotHash`

:   The compiled catalog snapshot hash.

`public Sha256Digest ContentManifestHash`

:   The compiled catalog's content manifest hash.

`public StableId EncounterId`

:   The explicit encounter this checkpoint restores.

`public uint Seed`

:   The battle seed.

`public Sha256Digest StartRequestHash`

:   The selected encounter's start-request hash.

**Methods**

`public byte[] GetStateBytes()`

:   Returns a defensive copy of the canonical state bytes.
    - **Returns** &mdash; The validated result of the operation.

---

## BattleRuntimeController

**Start here**

```csharp
public sealed class BattleRuntimeController : MonoBehaviour
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeController.cs</small>

Designer-first scene facade over BattleEngine. It compiles one explicit
catalog, starts one explicit encounter, owns the fixed-tick loop, binds
presentation, translates UI choices, and exposes checkpoint/replay
operations. It never rewrites authored combatant controls, discovers
content, or substitutes another encounter when configuration is invalid.

**Properties**

`public CompiledAuthoringCatalog ActiveCatalog`

:   The immutable compiled catalog used by the active engine.

`public StableId ActiveEncounterId`

:   The explicit encounter ID bound to the active engine.

`public uint ActiveSeed`

:   The seed bound to the active engine.

`public IAnimationAdapter AnimationAdapter`

:   The animation player, or null to use the shipped one. Set this to drive an Animator or a sprite library from the authored animation keys.

`public IAudioAdapter AudioAdapter`

:   The sound player, or null to use the shipped one. Set this to route battle audio through FMOD, Wwise, or your own mixer instead of the serialized clips.

`public bool AutoAdvance`

:   Whether Update converts elapsed time into fixed integer ticks.

`public BattleContentCatalog Catalog`

:   Serialized catalog used by the no-argument start.

`public DecisionOptions CurrentDecisionOptions`

:   The legal presentation choices for the current human decision, or `DecisionOptions.None` while no battle is active or the engine is not waiting for a human. Reading this property never advances or mutates the authoritative engine.

`public BattleSnapshot CurrentSnapshot`

:   The latest authoritative snapshot, or null before a battle starts.

`public string EncounterId`

:   Serialized encounter ID used by the no-argument start.

`public bool HasBattle`

:   Whether this controller currently owns an authoritative engine.

`public bool IsPaused`

:   True while `Pause` has frozen the battle and its visuals. `State` keeps reporting what the battle itself is doing, because a paused battle is still mid-fight rather than finished.

`public BattleRuntimePacing Pacing`

:   When the tick pump is allowed to run. Changing it mid-battle is safe: pacing decides when ticks are requested, never what they produce.

`public IPoolAdapter PoolAdapter`

:   The pool the presentation spawns instances through, or null to use the shipped one. Assign an implementation of your own before the battle starts to load art from Addressables or an existing pool; the built-in pool is used for any adapter left null.

`public float SpeedMultiplier`

:   The playback multiplier in force, one of `SpeedSteps`. It scales both the battle clock and the visuals, so nothing drifts apart at 4x.

`public BattleRuntimeState State`

:   The facade's current lifecycle state.

`public float TicksPerSecond`

:   How many simulation ticks one real second is worth before `SpeedMultiplier` is applied. Values below one are raised to one, because a battle that cannot reach a whole tick never moves.

`public IVfxAdapter VfxAdapter`

:   The effect player, or null to use the shipped one. A host adapter replaces the VFX bindings on this component rather than adding to them.

**Fields**

`public const float DefaultTicksPerSecond`

:   The default conversion rate from elapsed seconds to integer ticks.

`public static readonly FrozenList<float> SpeedSteps`

:   The playback multipliers `CycleSpeed` steps through, in order. Speed scales the visual clock and the tick pump together, so a fight watched at 4x still reaches the same result through the same ticks as one watched at 1x.

**Events**

`public event Action<BattleRuntimeEndedEvent> BattleEnded`

:   Raised when the battle reaches a clean end or Stop is called.

`public event Action<BattleRuntimeStartedEvent> BattleStarted`

:   Raised after a new or restored battle is fully bound.

`public event Action<BattleRuntimeEventsEvent> EventsProduced`

:   Raised once per non-empty event batch.

`public event Action<BattleRuntimeFailedEvent> RuntimeFailed`

:   Raised when a configuration or engine failure is contained.

`public event Action<BattleRuntimeSnapshotEvent> SnapshotChanged`

:   Raised after every authoritative snapshot change.

**Methods**

`public BattleRuntimeOperationResult AdvanceOneAction()`

:   Advances the battle to the end of exactly one action instead of a budget of ticks, which is what a turn-based or animation-driven host wants: call it once per attack and let the visuals finish before calling it again. It stops at a human decision without inventing a command.
    - **Returns** &mdash; The resulting lifecycle state and authoritative snapshot.

`public BattleRuntimeOperationResult AdvanceTicks(int count)`

:   Advances an exact positive integer number of simulation ticks and stops at engine boundaries. Non-positive counts fail without mutation.
    - `count` &mdash; Positive number of simulation ticks.
    - **Returns** &mdash; The resulting lifecycle state and authoritative snapshot.

`public BattleRuntimeValueResult<BattleRuntimeCheckpoint> CaptureCheckpoint()`

:   Captures canonical state plus the hashes required for exact restore. The returned checkpoint owns a defensive copy of its byte payload.
    - **Returns** &mdash; A checkpoint value, or BattleNotRunning/CheckpointInvalid.

`public BattleRuntimeValueResult<byte[]> CaptureReplay()`

:   Captures canonical replay JSON for the active battle using the same scheduler registry that compiled and runs it.
    - **Returns** &mdash; Replay bytes, or BattleNotRunning/ReplayCaptureFailed.

`public void CycleSpeed()`

:   Moves to the next entry of `SpeedSteps`, wrapping back to the slowest after the fastest.

`public void Pause()`

:   Freezes the battle and everything drawing it. Repeating the call does nothing, and no tick is lost: the clock simply stops accumulating.

`public BattleRuntimeOperationResult Restore(BattleRuntimeCheckpoint checkpoint)`

:   Restores an exact canonical checkpoint against the current catalog. All catalog and encounter hashes must match before state is decoded; a rejected restore leaves an existing battle unchanged.
    - `checkpoint` &mdash; Checkpoint value and canonical state bytes.
    - **Returns** &mdash; The restored state or a typed fail-closed diagnostic.

`public void Resume()`

:   Restarts a paused battle from exactly where it stopped.

`public void SkipVisuals()`

:   Finishes every queued animation now. It only compresses visuals, so a player who skips sees the same battle arrive at the same result.

`public BattleRuntimeOperationResult StartBattle()`

:   Starts the serialized encounter with the configured seed policy. Compilation and configuration failures are returned and published; the method does not throw an integration exception or select fallback content.
    - **Returns** &mdash; The resulting lifecycle state, snapshot, and typed failure.

`public BattleRuntimeOperationResult StartBattle(string requestedEncounterId, uint seed)`

:   Starts an explicit authored encounter and seed. Invalid, missing, or unknown IDs fail closed and leave an already active battle unchanged.
    - `requestedEncounterId` &mdash; Exact authored stable-ID text.
    - `seed` &mdash; Unsigned deterministic battle seed.
    - **Returns** &mdash; The resulting lifecycle state, snapshot, and typed failure.

`public BattleRuntimeOperationResult StartBattle(StableId requestedEncounterId, uint seed)`

:   Starts an explicit authored encounter and seed. Unknown content or a failed compile is reported without replacing an active battle.
    - `requestedEncounterId` &mdash; Exact valid authored encounter ID.
    - `seed` &mdash; Unsigned deterministic battle seed.
    - **Returns** &mdash; The resulting lifecycle state, snapshot, and typed failure.

`public BattleRuntimeOperationResult Stop()`

:   Stops and tears down the active battle while returning its last snapshot. Calling Stop without an active battle fails without events.
    - **Returns** &mdash; The stopped state and final snapshot, or BattleNotRunning.

`public BattleRuntimeOperationResult Submit(BattleUiCommandChoice choice)`

:   Submits a UI choice after deterministic command translation. A stale actor, unavailable skill, or unsatisfied target contract is rejected without inventing a different command.
    - `choice` &mdash; Intent emitted by a battle UI.
    - **Returns** &mdash; The authoritative command result and resulting snapshot.

`public BattleRuntimeOperationResult Submit(BattleCommand command)`

:   Submits an advanced, already-built battle command. Gameplay rejection is returned as `BattleRuntimeFailure.CommandRejected`; fatal invariants move the controller to the failed state.
    - `command` &mdash; Exact command for authoritative validation.
    - **Returns** &mdash; The command disposition, resulting state, and snapshot.

---

## BattleRuntimeEndReason

```csharp
public enum BattleRuntimeEndReason
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Why a normally driven battle stopped advancing.

| Value | Meaning |
| --- | --- |
| `TerminalResult` | The authored win or loss condition became terminal. |
| `NoScheduledWork` | The engine has no remaining scheduled work. |
| `StoppedByHost` | The host called Stop. |

---

## BattleRuntimeEndedEvent

```csharp
public sealed class BattleRuntimeEndedEvent
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Payload raised when driving reaches a clean end.

**Properties**

`public BattleRuntimeEndReason Reason`

:   The clean end reason.

`public BattleSnapshot Snapshot`

:   The last authoritative snapshot.

---

## BattleRuntimeEventsEvent

```csharp
public sealed class BattleRuntimeEventsEvent
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Payload raised for a non-empty event batch.

**Properties**

`public FrozenList<BattleEvent> Events`

:   The non-empty immutable event batch.

---

## BattleRuntimeFailedEvent

```csharp
public sealed class BattleRuntimeFailedEvent
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Payload raised for fail-closed runtime failures.

**Properties**

`public BattleRuntimeFailure Failure`

:   The typed failure category.

`public string Message`

:   Actionable diagnostic detail.

---

## BattleRuntimeFailure

```csharp
public enum BattleRuntimeFailure
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Typed reasons a facade operation can fail without throwing.

| Value | Meaning |
| --- | --- |
| `None` | No failure occurred. |
| `CatalogMissing` | No authoring catalog was assigned. |
| `EncounterIdMissing` | No encounter ID was supplied. |
| `EncounterIdInvalid` | The supplied encounter ID is not valid stable-ID text. |
| `EncounterNotFound` | The explicit encounter is absent from the compiled catalog. |
| `CatalogCompileFailed` | The authoring catalog failed compilation. |
| `RegistryProviderFailed` | The configured registry provider threw while building registries. |
| `HumanControlRequirementNotMet` | The encounter does not satisfy the configured human-control policy. |
| `BattleNotRunning` | The requested operation requires an active battle. |
| `CommandTranslationFailed` | A presentation choice could not be translated into a command. |
| `CommandRejected` | The authoritative engine rejected the submitted command. |
| `CheckpointInvalid` | The supplied or captured checkpoint is malformed. |
| `CheckpointIncompatible` | The checkpoint hashes do not match the compiled content. |
| `RestoreRejected` | The engine rejected the checkpoint state. |
| `ReplayCaptureFailed` | Replay capture could not complete. |
| `FatalInvariant` | The simulation reported a deterministic fatal invariant. |
| `InvalidTickCount` | The requested tick count is not positive. |
| `UnexpectedException` | An unexpected integration exception was contained. |

---

## BattleRuntimeHumanControlRequirement

```csharp
public enum BattleRuntimeHumanControlRequirement
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Optional fail-closed check over the control kinds authored into an
encounter. The controller never rewrites the compiled start request.

| Value | Meaning |
| --- | --- |
| `UseAuthoredControls` | Accept the encounter's authored Human/Automatic assignments. |
| `RequireAtLeastOneHuman` | Require at least one living human-controlled combatant. |
| `RequirePerspectiveTeamHuman` | Require a living human-controlled member on the perspective team. |

---

## BattleRuntimeOperationResult

```csharp
public class BattleRuntimeOperationResult
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Common typed result returned by controller operations.

**Properties**

`public CommandResult CommandResult`

:   The underlying command result for Submit operations.

`public BattleRuntimeFailure Failure`

:   Typed failure, or None on success.

`public string Message`

:   Actionable detail suitable for a log or error panel.

`public BattleSnapshot Snapshot`

:   Authoritative snapshot after the operation, when one exists.

`public BattleRuntimeState State`

:   Controller state after the operation.

`public bool Succeeded`

:   True only when the requested operation completed.

---

## BattleRuntimePacing

```csharp
public enum BattleRuntimePacing
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

How the controller decides when the battle clock may advance. It changes
pacing only: the same encounter and seed still reach the same result
through the same ticks either way.

| Value | Meaning |
| --- | --- |
| `Continuous` | Convert elapsed time into ticks every frame. |
| `WaitForPresentation` | Hold the next tick until the presenter has finished playing every beat it has been handed. |

---

## BattleRuntimeSeedPolicy

```csharp
public enum BattleRuntimeSeedPolicy
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

How the no-argument StartBattle operation chooses its seed.

| Value | Meaning |
| --- | --- |
| `Fixed` | Use the serialized fixed seed for every start. |
| `Incrementing` | Add the number of successful starts on this controller to the fixed seed. |

---

## BattleRuntimeSnapshotCause

```csharp
public enum BattleRuntimeSnapshotCause
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Why a snapshot was published through SnapshotChanged.

| Value | Meaning |
| --- | --- |
| `Started` | A new engine published its initial snapshot. |
| `Restored` | A restored engine published its restored snapshot. |
| `CommandSubmitted` | Command submission produced the snapshot. |
| `TicksAdvanced` | Integer tick advancement produced the snapshot. |
| `ActionAdvanced` | One action boundary produced the snapshot. |

---

## BattleRuntimeSnapshotEvent

```csharp
public sealed class BattleRuntimeSnapshotEvent
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Payload raised whenever the authoritative snapshot changes.

**Properties**

`public BattleRuntimeSnapshotCause Cause`

:   The operation that published the snapshot.

`public BattleSnapshot Snapshot`

:   The authoritative snapshot.

---

## BattleRuntimeStartedEvent

```csharp
public sealed class BattleRuntimeStartedEvent
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Payload raised when a battle starts or is restored.

**Properties**

`public StableId EncounterId`

:   The encounter that was bound.

`public bool Restored`

:   True for Restore; false for a new start.

`public uint Seed`

:   The seed that was bound.

`public BattleSnapshot Snapshot`

:   The initial authoritative snapshot.

---

## BattleRuntimeState

```csharp
public enum BattleRuntimeState
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

The runtime facade's externally visible lifecycle.

| Value | Meaning |
| --- | --- |
| `Idle` | No battle has been started. |
| `Running` | The engine can advance without a human command. |
| `AwaitingInput` | The engine is paused at a human decision boundary. |
| `Completed` | The battle reached a clean terminal or no-work outcome. |
| `Stopped` | The host explicitly stopped the battle. |
| `Failed` | A contained failure prevents further automatic driving. |

---

## BattleRuntimeUnityEvent

```csharp
public sealed class BattleRuntimeUnityEvent : UnityEvent
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

Parameterless inspector event paired with the typed C# events.

---

## BattleRuntimeValueResult

```csharp
public sealed class BattleRuntimeValueResult
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeContracts.cs</small>

An operation result that also returns an immutable value.

**Properties**

`public T Value`

:   The captured value on success; default on failure.

---

## VfxBinding

```csharp
public sealed class VfxBinding
```

`TurnGauge.Runtime` &middot; <small>TurnGauge/Runtime/Integration/BattleRuntimeController.cs</small>

Maps one presentation VFX key to an optional pooled prototype.

---
