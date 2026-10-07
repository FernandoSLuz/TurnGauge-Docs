# Other

69 types in this area.

!!! abstract "On this page"
    [AudioArtBinding](#audioartbinding) &middot; [AudioBinding](#audiobinding) &middot; [BattleCancelRelay](#battlecancelrelay) &middot; [BattleFeedbackLayout](#battlefeedbacklayout) &middot; [BattleLayoutIdentity](#battlelayoutidentity) &middot; [BattlePresentationLabel](#battlepresentationlabel) &middot; [BattlePresentationProfile](#battlepresentationprofile) &middot; [BattleProfileCatalog](#battleprofilecatalog) &middot; [BattleRulesPreset](#battlerulespreset) &middot; [BattleRuntimeCheckpoint](#battleruntimecheckpoint) &middot; [BattleRuntimeController](#battleruntimecontroller) &middot; [BattleRuntimeEndReason](#battleruntimeendreason) &middot; [BattleRuntimeEndedEvent](#battleruntimeendedevent) &middot; [BattleRuntimeEventsEvent](#battleruntimeeventsevent) &middot; [BattleRuntimeFailedEvent](#battleruntimefailedevent) &middot; [BattleRuntimeFailure](#battleruntimefailure) &middot; [BattleRuntimeHumanControlRequirement](#battleruntimehumancontrolrequirement) &middot; [BattleRuntimeOperationResult](#battleruntimeoperationresult) &middot; [BattleRuntimePacing](#battleruntimepacing) &middot; [BattleRuntimeSeedPolicy](#battleruntimeseedpolicy) &middot; [BattleRuntimeSnapshotCause](#battleruntimesnapshotcause) &middot; [BattleRuntimeSnapshotEvent](#battleruntimesnapshotevent) &middot; [BattleRuntimeStartedEvent](#battleruntimestartedevent) &middot; [BattleRuntimeState](#battleruntimestate) &middot; [BattleRuntimeUnityEvent](#battleruntimeunityevent) &middot; [BattleRuntimeValueResult](#battleruntimevalueresult) &middot; [BattleStageBounds](#battlestagebounds) &middot; [BattleTheme](#battletheme) &middot; [BattleUiCommandTranslationResult](#battleuicommandtranslationresult) &middot; [BattleUiCommandTranslator](#battleuicommandtranslator) &middot; [BattleUiTechnology](#battleuitechnology) &middot; [BattleViewAction](#battleviewaction) &middot; [BattleViewBehaviour](#battleviewbehaviour) &middot; [BattleViewCombatant](#battleviewcombatant) &middot; [BattleViewCommand](#battleviewcommand) &middot; [BattleViewIntent](#battleviewintent) &middot; [BattleViewIntentKind](#battleviewintentkind) &middot; [BattleViewProjection](#battleviewprojection) &middot; [BattleViewRoster](#battleviewroster) &middot; [BattleViewSession](#battleviewsession) &middot; [BattleViewState](#battleviewstate) &middot; [CustomMechanicsRegistryProvider](#custommechanicsregistryprovider) &middot; [CustomShieldEffectResolver](#customshieldeffectresolver) &middot; [DemoIdleSheet](#demoidlesheet) &middot; [DisplayStringTableAsset](#displaystringtableasset) &middot; [Entry](#entry) &middot; [ForecastRequest](#forecastrequest) &middot; [ForecastResult](#forecastresult) &middot; [ForecastStopReason](#forecaststopreason) &middot; [GeneratedUiText](#generateduitext) &middot; [IBattleFeedbackLayout](#ibattlefeedbacklayout) &middot; [IBattlePointerBlocker](#ibattlepointerblocker) &middot; [IBattleStageInformationLayout](#ibattlestageinformationlayout) &middot; [IBattleStageLayout](#ibattlestagelayout) &middot; [IBattleView](#ibattleview) &middot; [IInteractiveBattleView](#iinteractivebattleview) &middot; [LowestHealthAllyTargetResolver](#lowesthealthallytargetresolver) &middot; [ParticleArtBinding](#particleartbinding) &middot; [SessionEndState](#sessionendstate) &middot; [TargetCandidateQuery](#targetcandidatequery) &middot; [TargetPreview](#targetpreview) &middot; [TargetTreatment](#targettreatment) &middot; [TargetingPreset](#targetingpreset) &middot; [TokenArtBinding](#tokenartbinding) &middot; [ToolkitBattleView](#toolkitbattleview) &middot; [TurnGaugeDemoBootstrap](#turngaugedemobootstrap) &middot; [UguiBattleView](#uguibattleview) &middot; [UiPortraitCrop](#uiportraitcrop) &middot; [VfxBinding](#vfxbinding)

## AudioArtBinding

```csharp
public sealed class AudioArtBinding
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/TurnGaugeDemoBootstrap.cs</small>

Nested in `TurnGauge.Presentation.Demo.TurnGaugeDemoBootstrap`.

Binds a recipe audio key (an sfx-* clip name) to art.

**Fields**

`public string AudioKey`

:   Recipe audio key whose clip is being bound.

`public AudioClip Clip`

:   Audio clip played for the bound recipe key.

---

## AudioBinding

```csharp
public sealed class AudioBinding
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeController.cs</small>

Nested in `TurnGauge.Runtime.BattleRuntimeController`.

Maps one presentation audio key to a Unity audio clip.

**Fields**

`public AudioClip Clip`

:   The clip played for the key, or null for an intentional no-op.

`public string Key`

:   The presentation recipe's audio key.

---

## BattleCancelRelay

```csharp
public sealed class BattleCancelRelay : MonoBehaviour, ICancelHandler
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUGUI/BattleCancelRelay.cs</small>

Routes the active input module's cancel event without depending on a particular input package.

**Fields**

`public BattleViewBehaviour Owner`

:   View that receives the cancel intent, or null when the relay is inactive.

**Methods**

`public void OnCancel(BaseEventData eventData)`

:   Routes a cancel navigation event to the owning battle view when gamepad input is enabled.

    - `eventData` &mdash; Event data consumed when the owner handles the cancel intent.

---

## BattleFeedbackLayout

```csharp
public static class BattleFeedbackLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Computes a deterministic clear rectangle for presentation feedback.

The routine is renderer- and engine-independent. It clips positive
obstacle intersections to the supplied stage, considers every pair of
resulting x edges, and finds the largest y gap in that vertical slab.
The expected obstacle count is small (normally twelve or fewer), so the
bounded temporary arrays are rebuilt once per call. Callers should cache
the result across frames when geometry is stable; this helper deliberately
does not retain mutable static scratch state.

**Methods**

`public static bool TryFindClearBounds(BattleStageBounds stage, IReadOnlyList<BattleStageBounds> obstacles, out BattleStageBounds bounds)`

:   Finds the largest axis-aligned rectangle inside `stage` that does not positively intersect any obstacle. Obstacles outside the stage are ignored; obstacles crossing its edge are clipped. A touching edge has zero intersection and therefore does not reduce the available area. Ties prefer the rectangle whose centre is closest to the original stage centre, then lexicographic (left, bottom, width, height) order, making results independent of obstacle input ordering.

    - `stage` &mdash; Valid normalized stage bounds.
    - `obstacles` &mdash; Information bands or other occupied bounds.
    - `bounds` &mdash; Receives the largest clear rectangle.
    - **Returns** &mdash; False when the stage is invalid or fully covered.

---

## BattleLayoutIdentity

```csharp
public enum BattleLayoutIdentity
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattlePresentationProfile.cs</small>

Visual family used for starter palettes and default stage reservations.

| Value | Meaning |
| --- | --- |
| `Fantasy` | Fantasy presentation framing and palette family. |
| `ScienceFiction` | Science-fiction presentation framing and palette family. |

---

## BattlePresentationLabel

```csharp
public sealed class BattlePresentationLabel
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattlePresentationProfile.cs</small>

One display text override owned by a presentation profile.

**Fields**

`public string Id`

:   Stable display identifier looked up by the presentation layer.

`public string Text`

:   Text shown for the identifier.

---

## BattlePresentationProfile

```csharp
public sealed class BattlePresentationProfile : ScriptableObject
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattlePresentationProfile.cs</small>

Authored references only. Runtime and preview never write to this asset.

**Fields**

`public int ActionsPerPage`

:   Maximum number of action choices shown on one page.

`public BattleContentCatalog Catalog`

:   Authoring catalog supplying the encounter and content references.

`public string EncounterId`

:   Stable encounter identifier selected for presentation.

`public BattlePresentationLabel[] Labels`

:   Optional display text overrides; these never affect battle hashes.

`public UnityEngine.Object LayoutAsset`

:   Optional UI Toolkit visual tree asset.

`public BattleRegistryProvider RegistryProvider`

:   Optional registry provider used when the runtime has no explicit provider.

`public BattleRulesPreset RulesPreset`

:   Scheduler preset used to build the runtime catalog.

`public uint Seed`

:   Initial deterministic seed supplied to the battle session.

`public UnityEngine.Object StagePresentation`

:   Optional stage preset validated and consumed by the runtime presentation layer.

`public int TargetsPerPage`

:   Maximum number of target choices shown on one page.

`public BattleUiTechnology Technology`

:   UI technology a host should instantiate for this profile.

`public BattleTheme Theme`

:   Theme values copied into the active view.

`public float TicksPerSecond`

:   Simulation ticks represented by one real second.

`public bool UseGamepad`

:   Enables directional keyboard and controller navigation.

`public bool UseSideInformationBanks`

:   Groups stage information beside the bodies instead of attaching each plate to its feet. The initial bank layout supports three combatants per side.

`public BattleViewBehaviour ViewPrefab`

:   View prefab that owns the profile's UI layout.

---

## BattleProfileCatalog

```csharp
public sealed class BattleProfileCatalog : IDisposable
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattleProfileCatalog.cs</small>

Owns the partial runtime catalog required by a presentation profile.
The catalog clone, selected scheduler, and encounters rewired to that
scheduler are runtime-owned; other definitions referenced by the graph
remain shared with the source and must be treated as read-only.

**Constructors**

`public BattleProfileCatalog(BattleContentCatalog source, string encounterId, BattleRulesPreset preset)`

:   Creates a partial runtime catalog for one presentation profile. The nodes this class replaces are isolated; referenced definitions that are not replaced remain shared with the source and are read-only for consumers of the returned catalog.

    - `source` &mdash; Authored catalog to copy.
    - `encounterId` &mdash; Stable encounter identifier to select.
    - `preset` &mdash; Scheduler behavior to apply.

**Properties**

`public BattleContentCatalog Catalog`

:   Runtime-owned catalog containing copied scheduler and encounter nodes. Definitions not replaced while selecting the profile remain shared references to the source catalog and are not safe to edit through this property.

**Methods**

`public void Dispose()`

:   Destroys all runtime-owned catalog copies and releases the catalog.

---

## BattleRulesPreset

```csharp
public enum BattleRulesPreset
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattlePresentationProfile.cs</small>

Choice of Action Order rounds or paused ATB when deriving a profile's runtime catalog.

| Value | Meaning |
| --- | --- |
| `Rounds` | Round-based scheduler with action order. |
| `AtbPause` | Active-time scheduler that pauses while input is requested. |

---

## BattleRuntimeCheckpoint

```csharp
public sealed class BattleRuntimeCheckpoint
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

Persistable battle restore point. The battle state is canonical bytes and
the three hashes pin it to one compiled encounter.

**Constructors**

`public BattleRuntimeCheckpoint(StableId encounterId, uint seed, Sha256Digest contentManifestHash, Sha256Digest compiledSnapshotHash, Sha256Digest startRequestHash, byte[] stateBytes)`

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

    - **Returns** &mdash; A new byte array containing the checkpoint's canonical battle state.

---

## BattleRuntimeController

```csharp
public sealed partial class BattleRuntimeController
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeController.Presentation.cs</small>

Coordinates authored presentation profiles, runtime views and optional stage presentation.

**Properties**

`public CompiledAuthoringCatalog ActiveCatalog`

:   The immutable compiled catalog used by the active engine.

`public StableId ActiveEncounterId`

:   The explicit encounter ID bound to the active engine.

`public uint ActiveSeed`

:   The seed bound to the active engine.

`public StagePresentationPlayback ActiveStagePresentation`

:   The isolated stage effects owned by this battle, or null when no preset is configured.

`public BattleViewBehaviour ActiveView`

:   The instantiated presentation view for the active battle, or null before it starts.

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

`public bool LogFailuresToConsole`

:   Whether a failed operation is written to the Console. On by default, because a designer who cannot read a `BattleRuntimeOperationResult` has no other channel. Turn it off in a project that surfaces failures its own way through `OnRuntimeFailed`, or in a test that provokes a failure on purpose.

`public BattleRuntimePacing Pacing`

:   When the tick pump is allowed to run. Changing it mid-battle is safe: pacing decides when ticks are requested, never what they produce.

`public IPoolAdapter PoolAdapter`

:   The pool the presentation spawns instances through, or null to use the shipped one. Assign an implementation of your own before the battle starts to load art from Addressables or an existing pool; the built-in pool is used for any adapter left null.

`public BattlePresentationProfile PresentationProfile`

:   The authored presentation profile currently selected by this controller.

`public BattleRegistryProvider RegistryProvider`

:   Explicit custom mechanics registry. Assign before starting a battle; a profile provider is used only when this is null.

`public float SpeedMultiplier`

:   The playback multiplier in force, one of `SpeedSteps`. It scales both the battle clock and the visuals, so nothing drifts apart at 4x.

`public BattlePresenter StagePresenter`

:   Optional stage presenter used to render combatants and target previews. It may be assigned only while no battle is active.

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

`public void ConfigureBattle(BattleContentCatalog content, string encounter, uint seed)`

:   Configures an explicit catalog without mutating it or starting a battle.

    - `content` &mdash; Authored catalog prepared at StartBattle; it is not modified by this controller.
    - `encounter` &mdash; Stable encounter ID in the supplied catalog.
    - `seed` &mdash; Fixed deterministic seed used by subsequent starts.

`public void ConfigurePresentation(BattlePresentationProfile profile)`

:   Chooses a native or custom view before starting. The authored profile is read-only.

    - `profile` &mdash; Authored view and presentation configuration, or null to use the legacy host.

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

`public void UpdateStagePresentation(UnityEngine.Object stagePresentation)`

:   Updates visual recipes, bindings and feel during a battle. Cancels old pending effects and restores their offsets without restarting simulation, replacing its view, or writing to the authored profile.

    - `stagePresentation` &mdash; Optional PresentationStagePreset asset; null clears profile effects. Other object types warn and clear them.

---

## BattleRuntimeEndReason

```csharp
public enum BattleRuntimeEndReason
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

Payload raised for a non-empty event batch.

**Properties**

`public FrozenList<BattleEvent> Events`

:   The non-empty immutable event batch.

---

## BattleRuntimeFailedEvent

```csharp
public sealed class BattleRuntimeFailedEvent
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

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

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

Parameterless inspector event paired with the typed C# events.

---

## BattleRuntimeValueResult

```csharp
public sealed class BattleRuntimeValueResult
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeContracts.cs</small>

An operation result that also returns an immutable value.

**Properties**

`public T Value`

:   The captured value on success; default on failure.

---

## BattleStageBounds

```csharp
public readonly struct BattleStageBounds
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

A presentation-only rectangle in normalized screen space, with a bottom-left origin.

**Constructors**

`public BattleStageBounds(float left, float bottom, float width, float height)`

:   Creates normalized bottom-left stage bounds.

    - `left` &mdash; Normalized left edge.
    - `bottom` &mdash; Normalized bottom edge.
    - `width` &mdash; Normalized width.
    - `height` &mdash; Normalized height.

**Properties**

`public float Bottom`

:   Normalized bottom coordinate.

`public float Height`

:   Normalized height.

`public bool IsValid`

:   True when the rectangle is positive and contained in normalized space.

`public float Left`

:   Normalized left coordinate.

`public float Width`

:   Normalized width.

---

## BattleTheme

```csharp
public sealed class BattleTheme
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattlePresentationProfile.cs</small>

Serializable visual values copied by views before they render.

**Fields**

`public Color Accent`

:   Primary action and selection accent color.

`public Color Background`

:   Background color used by the view.

`public Font Font`

:   Optional legacy Unity font for controls that require one.

`public UnityEngine.Object FontAsset`

:   Optional native font asset consumed by the selected UI technology.

`public float FontSize`

:   Default font size used by native controls created by a view.

`public Color Foreground`

:   Primary readable text and foreground color.

`public BattleLayoutIdentity Identity`

:   Layout family whose colors and framing this theme describes.

`public Color Negative`

:   Color used for negative outcomes such as damage.

`public Color Panel`

:   Panel fill color used by the view.

`public Color Positive`

:   Color used for positive outcomes such as healing.

`public bool ReduceMotion`

:   Requests reduced motion in the presentation layer.

`public Material SurfaceMaterial`

:   Optional material used by the view's panel surfaces.

`public Sprite SurfaceSprite`

:   Optional surface sprite used by the view's panels.

**Methods**

`public BattleTheme Clone()`

:   Returns a shallow copy so a view can adjust values without editing the asset.

    - **Returns** &mdash; A new theme object sharing the referenced Unity assets.

`public static BattleTheme Create(BattleLayoutIdentity identity)`

:   Builds a new theme with the layout family's background, panel, accent, and foreground defaults.

    - `identity` &mdash; Layout family to seed.
    - **Returns** &mdash; A new theme with that family's default colors.

---

## BattleUiCommandTranslationResult

```csharp
public sealed class BattleUiCommandTranslationResult
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/BattleUiCommandTranslator.cs</small>

Typed result of translating a presentation choice into a command.

**Properties**

`public BattleCommand Command`

:   The translated command on success; null on failure.

`public string Message`

:   Actionable failure detail, or an empty string on success.

`public bool Succeeded`

:   True when a complete command was produced.

---

## BattleUiCommandTranslator

```csharp
public static class BattleUiCommandTranslator
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/BattleUiCommandTranslator.cs</small>

Turns a UI choice into the exact command shape the engine expects. When
the caller supplies no explicit targets for a resolver that requires
them, this asks that skill's registered `ITargetResolver` who is
eligible and takes the lowest stable IDs from the answer, so a project
whose resolver narrows further than its declared contract gets an
auto-pick its own resolver accepts. Explicit target lists are preserved
verbatim, checked against the same resolver, and remain subject to
authoritative engine validation.

**Methods**

`public static BattleUiCommandTranslationResult Translate(BattleUiCommandChoice choice, BattleSnapshot snapshot, CompiledAuthoringCatalog catalog)`

:   Translates a presentation choice against the current authoritative snapshot and compiled command shapes. It returns a failed result for null context, a stale actor, an unavailable skill, or an unsatisfied target contract; normal validation failures do not throw.

    - `choice` &mdash; Player intent to translate.
    - `snapshot` &mdash; Current authoritative state.
    - `catalog` &mdash; Compiled content used by the battle.
    - **Returns** &mdash; A complete command on success or actionable failure detail.

---

## BattleUiTechnology

```csharp
public enum BattleUiTechnology
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattlePresentationProfile.cs</small>

Native UI backend required by a profile's view prefab.

| Value | Meaning |
| --- | --- |
| `UGUI` | Uses Unity's Canvas-based UI. |
| `UIToolkit` | Uses Unity UI Toolkit. |

---

## BattleViewAction

```csharp
public sealed class BattleViewAction
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

A legal action and the candidate IDs supplied by its actual resolver.

**Constructors**

`public BattleViewAction(StableId id, string label, string description, int minimumTargets, int maximumTargets, bool automaticTargets, FrozenList<StableId> candidates = null)`

:   Creates an action projection; candidates are caller supplied view data and are not validated here.

    - `id` &mdash; Stable action identity.
    - `label` &mdash; Display label.
    - `description` &mdash; Display description.
    - `minimumTargets` &mdash; Minimum manually selected targets.
    - `maximumTargets` &mdash; Maximum manually selected targets.
    - `automaticTargets` &mdash; Whether target selection is automatic.
    - `candidates` &mdash; Projected candidate IDs.

**Properties**

`public bool AutomaticTargets`

:   Whether targets are selected automatically.

`public FrozenList<StableId> Candidates`

:   Authoritative candidate IDs from the resolver.

`public string Description`

:   Display description.

`public StableId Id`

:   Stable action identifier.

`public string Label`

:   Display label.

`public int MaximumTargets`

:   Maximum manual target count.

`public int MinimumTargets`

:   Minimum manual target count.

---

## BattleViewBehaviour

```csharp
public abstract class BattleViewBehaviour : MonoBehaviour, IInteractiveBattleView, IBattlePointerBlocker, IBattleStageLayout, IBattleStageInformationLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUnity/BattleViewBehaviour.cs</small>

Unity lifecycle shell. Native adapters share selection and command semantics.

**Properties**

`public BattlePresentationProfile Profile`

:   Profile last applied through `Configure`.

`public BattleViewSession Session`

:   Session holding selection, navigation, and command state.

`public abstract BattleUiTechnology Technology`

:   UI technology implemented by this concrete view.

`public BattleTheme Theme`

:   Runtime copy of the active theme.

`public bool UseSideInformationBanks`

:   Optional side information layout requested by the applied profile.

**Events**

`public event Action<BattleViewCommand> CommandChosen`

:   Raised when the user confirms a battle command.

**Methods**

`public virtual void ApplyTheme(BattleTheme theme)`

:   Copies a theme and refreshes the rendered view.

    - `theme` &mdash; Theme to copy, or null for defaults.

`public virtual bool BlocksStagePointer(float screenX, float screenY)`

:   Checks whether this view consumes a stage pointer at the supplied screen coordinate.

    - `screenX` &mdash; Screen-space horizontal coordinate.
    - `screenY` &mdash; Screen-space vertical coordinate.
    - **Returns** &mdash; Always false in the base view; a concrete view overrides this when its UI blocks the stage.

`public abstract void BuildDefaultLayout(BattleLayoutIdentity identity)`

:   Builds the view's default layout for a layout family.

    - `identity` &mdash; Layout family to author.

`public virtual void Configure(BattlePresentationProfile profile)`

:   Retains the supplied profile reference and applies a cloned theme. Null profile or theme inputs use defaults; authored theme values and simulation state are not changed.

    - `profile` &mdash; Profile to apply, or null to use default theme values.

`public void ConfigureStageBounds(BattleStageBounds? bounds)`

:   Configures a view's stage reservation without changing combat state. Null retains host framing.

    - `bounds` &mdash; Normalized bottom-left rectangle to reserve, or null to release the reservation.

`public void HandleIntent(BattleViewIntent intent)`

:   Dispatches a user intent through the view session.

    - `intent` &mdash; Input intent to process.

`public virtual bool OwnsPointerSurface(object surface)`

:   Checks whether this view handles the supplied external pointer surface.

    - `surface` &mdash; Host surface object to inspect.
    - **Returns** &mdash; Always false in the base view; a concrete technology adapter overrides this when it owns the surface.

`public virtual void RefreshBindingsIfNeeded()`

:   Editor hosts call this while the simulation is idle to observe native live reload.

`public void Render(BattleViewState state)`

:   Renders a state snapshot without changing simulation state.

    - `state` &mdash; Latest presentation snapshot.

`public bool TryGetStageBounds(out BattleStageBounds bounds)`

:   Returns the authored stage reservation when enabled.

    - `bounds` &mdash; Receives the normalized bottom-left stage rectangle.
    - **Returns** &mdash; True when this view reserves a valid stage rectangle.

`public abstract string[] ValidateBindings()`

:   Reports missing or invalid bindings needed by this view.

    - **Returns** &mdash; Human-readable validation messages; an empty array means valid.

---

## BattleViewCombatant

```csharp
public sealed class BattleViewCombatant
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Immutable, renderer-independent information shown for one combatant.

**Constructors**

`public BattleViewCombatant(StableId id, string name, string team, int health, int maximumHealth, int shield = 0, string resources = "", string statuses = "", StableId teamId = default, int statusCount = 0)`

:   Creates a read-only combatant projection; null display strings become empty.

    - `id` &mdash; Stable combatant identity.
    - `name` &mdash; Display name.
    - `team` &mdash; Display team label.
    - `health` &mdash; Current health units.
    - `maximumHealth` &mdash; Maximum health units.
    - `shield` &mdash; Current shield units.
    - `resources` &mdash; Preformatted resource text.
    - `statuses` &mdash; Preformatted status text.
    - `teamId` &mdash; Stable team identity, or invalid for legacy label-only data.
    - `statusCount` &mdash; Number of statuses represented by the projection.

**Properties**

`public int Health`

:   Current health.

`public StableId Id`

:   Stable combatant identifier.

`public int MaximumHealth`

:   Maximum health.

`public string Name`

:   Display name.

`public string Resources`

:   Preformatted resource summary.

`public int Shield`

:   Current shield.

`public int StatusCount`

:   Number of statuses represented by this projection.

`public string Statuses`

:   Preformatted status summary.

`public string Team`

:   Display team label.

`public StableId TeamId`

:   Stable team identity; invalid means legacy display data.

---

## BattleViewCommand

```csharp
public readonly struct BattleViewCommand
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Immutable command choice forwarded for authoritative validation.

**Constructors**

`public BattleViewCommand(StableId actorId, StableId? skillId, bool isConcede, FrozenList<StableId> targets = null)`

:   Packages actor, skill, concession, and requested targets for host validation; it performs no command legality checks.

    - `actorId` &mdash; Actor whose decision is represented.
    - `skillId` &mdash; Selected skill, or null for concession.
    - `isConcede` &mdash; Whether this is a concession request.
    - `targets` &mdash; Requested target IDs.

**Properties**

`public StableId ActorId`

:   Actor for whom the choice was made.

`public bool IsConcede`

:   Whether this requests concession.

`public StableId? SkillId`

:   Selected skill, or null for concession.

`public FrozenList<StableId> Targets`

:   Requested target IDs.

---

## BattleViewIntent

```csharp
public readonly struct BattleViewIntent
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

A UI gesture; the host still validates the resulting command.

**Constructors**

`public BattleViewIntent(BattleViewIntentKind kind, StableId id = default)`

:   Creates an intent with an optional action or target ID.

    - `kind` &mdash; Interaction requested by the view.
    - `id` &mdash; Action or target identity, when applicable.

**Properties**

`public StableId Id`

:   Action or target identifier.

`public BattleViewIntentKind Kind`

:   Requested interaction kind.

---

## BattleViewIntentKind

```csharp
public enum BattleViewIntentKind
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Interaction intents understood by a battle view session.

| Value | Meaning |
| --- | --- |
| `SelectAction` | Requests that the session select an available skill and clear its current targets. |
| `SelectTarget` | Toggles an eligible target. |
| `Confirm` | Publishes the current selection. |
| `Cancel` | Clears the current selection. |
| `Concede` | Publishes a concession request. |

---

## BattleViewProjection

```csharp
public static class BattleViewProjection
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/BattleViewProjection.cs</small>

The single snapshot-to-UI projection for every native or customer renderer.

**Methods**

`public static BattleViewState Create(BattleSnapshot snapshot, CompiledAuthoringCatalog catalog, DisplayStringTable labels = null, IEnumerable<string> feedback = null, StableId? rosterTeamId = null)`

:   Projects a battle snapshot and compiled content into read-only HUD rows, available actions, target candidates, timeline labels and a terminal result. Does not submit commands or advance the simulation.

    - `snapshot` &mdash; Authoritative snapshot to present. Null returns the empty view state.
    - `catalog` &mdash; Compiled content used for decision shapes, costs and target candidates. Null returns the empty view state.
    - `labels` &mdash; Optional display-name table; missing names fall back to stable identities.
    - `feedback` &mdash; Optional feedback lines copied into the resulting presentation state.
    - `rosterTeamId` &mdash; Optional viewing-team identity. When omitted, uses the first human-controlled combatant's team, or the first snapshot team for an automatic-only battle; never the current decision actor.
    - **Returns** &mdash; A presentation state with a decision key derived from command sequence and actor identity, or the empty state when required input is absent.

---

## BattleViewRoster

```csharp
public static class BattleViewRoster
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewRoster.cs</small>

Pure grouping helpers for immutable presentation rosters.

**Methods**

`public static FrozenList<FrozenList<BattleViewCombatant>> BuildPages(FrozenList<BattleViewCombatant> combatants, int capacity)`

:   Builds pages containing one team each; teams follow first occurrence and members keep input order.

    - `combatants` &mdash; Source projections; a null source or null entries produces no members.
    - `capacity` &mdash; Positive maximum members per page.
    - **Returns** &mdash; Frozen pages of combatant projections.

`public static int FindActorPage(FrozenList<FrozenList<BattleViewCombatant>> pages, StableId? actorId)`

:   Finds the page containing an actor by exact stable ID, or returns the first page.

    - `pages` &mdash; Roster pages produced by `BuildPages`.
    - `actorId` &mdash; Current decision actor, when one is available.
    - **Returns** &mdash; The zero-based page containing the actor, or zero when no exact match exists.

`public static FrozenList<BattleViewCombatant> ForTeam(BattleViewState state, StableId teamId)`

:   Returns every member with the exact team ID, including defeated members.

    - `state` &mdash; State supplying the roster; null produces an empty result.
    - `teamId` &mdash; Valid stable team identity.
    - **Returns** &mdash; Matching members in source order.

---

## BattleViewSession

```csharp
public sealed class BattleViewSession
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewSession.cs</small>

Shared interaction state survives visual tree reconstruction. Never owns an engine.

**Constructors**

`public BattleViewSession()`

:   Creates an empty selection session; it owns presentation state only.

**Properties**

`public bool CanConfirm`

:   Whether the current selection satisfies local UI constraints.

`public string Error`

:   Latest host rejection or local selection error.

`public bool IsSubmissionPending`

:   Remains pending until the host rejects or publishes a different decision.

`public BattleViewAction SelectedAction`

:   Currently selected available action, or null.

`public IReadOnlyList<StableId> SelectedTargets`

:   Currently selected eligible targets.

`public BattleViewState State`

:   Current immutable host-provided view state.

**Events**

`public event Action Changed`

:   Raised after state or selection changes.

`public event Action<BattleViewCommand> CommandChosen`

:   Raised when a validated UI selection is published to the host.

**Methods**

`public void Dispatch(BattleViewIntent intent)`

:   Processes an intent locally and forwards only a choice; the host remains authoritative.

    - `intent` &mdash; Interaction to apply to the current selection.

`public void Reject(string error)`

:   Clears the pending submission and records a host rejection.

    - `error` &mdash; Host-provided rejection text; null becomes empty.

`public void UpdateState(BattleViewState state)`

:   Replaces host state and prunes selections no longer available.

    - `state` &mdash; New host snapshot; null selects `BattleViewState.Empty`.

---

## BattleViewState

```csharp
public sealed class BattleViewState
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

A complete read-only view; contains no scene objects or authority to change combat.

**Constructors**

`public BattleViewState(string decisionKey, string heading, StableId? actorId, bool canConcede, FrozenList<BattleViewCombatant> combatants = null, FrozenList<BattleViewAction> actions = null, FrozenList<string> timeline = null, FrozenList<string> feedback = null, string resultText = "", StableId? rosterTeamId = null)`

:   Creates an immutable renderer-independent decision snapshot.

    - `decisionKey` &mdash; Host decision identity.
    - `heading` &mdash; Display heading.
    - `actorId` &mdash; Deciding actor, when any.
    - `canConcede` &mdash; Whether concession is offered.
    - `combatants` &mdash; Combatant projections.
    - `actions` &mdash; Available action projections.
    - `timeline` &mdash; Timeline text entries.
    - `feedback` &mdash; Feedback text entries.
    - `resultText` &mdash; Terminal result text.
    - `rosterTeamId` &mdash; Optional valid team identity for roster scoping.

**Properties**

`public FrozenList<BattleViewAction> Actions`

:   Actions currently available to the actor.

`public StableId? ActorId`

:   Actor currently expected to decide, when any.

`public bool CanConcede`

:   Whether concession is currently offered.

`public FrozenList<BattleViewCombatant> Combatants`

:   Read-only combatant projections.

`public string DecisionKey`

:   Host decision identity used to retain or reset selection.

`public FrozenList<string> Feedback`

:   Presentation feedback entries.

`public string Heading`

:   Display heading.

`public string ResultText`

:   Terminal result text, when the battle has ended.

`public StableId? RosterTeamId`

:   Optional valid stable team identity for a scoped roster.

`public FrozenList<string> Timeline`

:   Presentation timeline entries.

**Fields**

`public static readonly BattleViewState Empty`

:   Empty state used before the first host update.

---

## CustomMechanicsRegistryProvider

```csharp
public sealed class CustomMechanicsRegistryProvider : BattleRegistryProvider
```

`TurnGauge.Samples.CustomMechanics` &middot; <small>Samples/CustomMechanics/CustomMechanicsRegistryProvider.cs</small>

Adds the sample shield effect and lowest-health ally target resolver to
the built-in registry set used by authored battles and replay.

---

## CustomShieldEffectResolver

```csharp
public sealed class CustomShieldEffectResolver : IEffectResolver
```

`TurnGauge.Samples.CustomMechanics` &middot; <small>Samples/CustomMechanics/CustomShieldEffectResolver.cs</small>

Creates a shield equal to a configured fraction of missing health.

**Properties**

`public int ContractVersion`

:   Gets the contract version implemented by this resolver.

`public int EffectContractVersion`

:   Gets the effect registry contract version implemented by this resolver.

`public StableId ImplementationId`

:   Gets the stable implementation id used for compatibility checks.

`public StableId ResolverId`

:   Gets the resolver's stable registry id.

**Fields**

`public static readonly StableId Id`

:   Stable registry id for this effect resolver.

`public static readonly StableId PriorityKey`

:   Property key for the shield priority.

`public static readonly StableId RatioKey`

:   Property key for the missing-health fraction to convert into shield.

`public static readonly StableId ShieldKey`

:   Property key for the shield identity to apply.

**Methods**

`public static long CalculateShieldRaw(int missingHealth, Fixed64 ratio)`

:   Calculates the fixed-point shield amount from missing health and a ratio.

    - `missingHealth` &mdash; Positive amount of health missing from the target.
    - `ratio` &mdash; Fixed-point fraction applied to the missing health.
    - **Returns** &mdash; The raw fixed-point shield amount, or zero for non-positive inputs.

`public EffectPlan Plan(EffectPlanningContext context, PropertySet properties)`

:   Plans a shield primitive equal to the target's missing health times the configured ratio.

    - `context` &mdash; Planning context containing the target snapshot and content.
    - `properties` &mdash; Validated effect properties controlling shield id, ratio, and priority.
    - **Returns** &mdash; An effect plan, empty when no shield is needed or validation fails.

`public ValidationReport Validate(EffectValidationContext context, PropertySet properties)`

:   Validates the three required property values and their ranges.

    - `context` &mdash; Content context used to validate the effect.
    - `properties` &mdash; Effect properties, requiring ratio, shield id, and priority.
    - **Returns** &mdash; A valid report or a diagnostic identifying the first contract violation.

---

## DemoIdleSheet

```csharp
public static class DemoIdleSheet
```

`TurnGauge.Presentation` &middot; <small>Samples/RuntimeDemo/DemoIdleSheet.cs</small>

Reads the sample character art, which ships as a grid of idle frames rather than
as a single still so combatants breathe instead of standing frozen.

Everything that dresses a combatant goes through here, because the bound sprite
covers the whole grid: handing it to a token unsliced would put thirty tiny
characters on one formation slot. Art that is not the authored grid - the token
gems, or a buyer's own drawing - is passed through untouched.

Cells are the full authored canvas, so every frame keeps the (0.5, 0) ground-line
pivot and the importer's pixels-per-unit and a combatant neither drifts nor
resizes as it plays.

It holds nothing. An earlier version memoized the sliced frames in a static
dictionary keyed by texture, which is two faults at once: the presentation
assembly forbids static state that can retain a UnityEngine.Object, and the
entries outlived the textures they were keyed on, so every domain reload left
a table of destroyed keys pointing at sprites nothing would ever free. Callers
keep the frames they asked for; the shipped demo already did.

It also lives outside the demo-driver namespace deliberately. That namespace
is exempt from the purity rules because the driver owns a battle engine by
specification, and a sprite utility has no business inheriting an exemption
written for something else - particularly one the layout audit and the
documentation capture both call.

**Fields**

`public const int Columns`

:   Columns in the authored grid.

`public const float FramesPerSecond`

:   Frames per second the grid is authored to play at.

`public const int Rows`

:   Rows in the authored grid.

`public const string TextureNamePrefix`

:   Only art named like the shipped characters is treated as a grid.

**Methods**

`public static bool ConfigureSampleGround(CombatantTokenView token)`

:   Authors a stable foot anchor for the six shipped idle grids without cropping their art. Their full cells include transparent padding below the feet; renderer bounds alone would place shadows and targeting there. Custom art is left untouched and can author its own ground anchor.

    - `token` &mdash; Sample token whose root renderer wears a sliced idle frame.
    - **Returns** &mdash; True when a known sample frame supplied a configured foot anchor.

`public static Sprite RestingFrame(Sprite source)`

:   The frame a combatant rests on: frame zero of the grid, or the sprite itself when it is a plain still. This is what everything that only needs one image - the turn-order rail, a documentation screenshot, a layout measurement - should be given, so a measurement never reads the whole sheet as one combatant.

`public static Sprite[] Slice(Sprite source)`

:   The frames of `source`'s grid, or null when the art is a plain still and should be used exactly as authored.

---

## DisplayStringTableAsset

```csharp
public sealed class DisplayStringTableAsset : DisplayStringTableProvider
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/DisplayStringTableAsset.cs</small>

The shipped serialized string-table asset the demo driver supplies to the
presenter (specification section 3: display text comes from an explicit
table, never from compiled snapshots, which exclude labels from every
hash). Entries map a stable id to a human display name; the asset is
authored by the Internal presentation-content generator and consumed by
`TurnGaugeDemoBootstrap` through `Build`. It is
non-authoritative data and never enters any battle hash.

**Properties**

`public IReadOnlyList<Entry> Entries`

:   The authored entries in serialized order.

**Methods**

`public override DisplayStringTable Build()`

:   Builds the runtime `DisplayStringTable`. Invalid ids and null entries and invalid ids are skipped defensively. A null label is stored as an empty string; lookups for missing ids fall back to the raw id text inside the table itself.

---

## Entry

```csharp
public sealed class Entry
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/DisplayStringTableAsset.cs</small>

Nested in `TurnGauge.Presentation.Demo.DisplayStringTableAsset`.

One stable-id-to-display-name pair.

**Fields**

`public string Id`

:   Stable id parsed into the table when this entry is valid.

`public string Label`

:   Display text stored for the parsed id; a null value becomes an empty string.

---

## ForecastRequest

```csharp
public sealed class ForecastRequest
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Forecast/BattleForecast.cs</small>

The three caps that bound one `BattleForecast.Run` call: how
far ahead it may look, and how much work and evidence it may collect
before stopping. The constructor accepts any values; out-of-range caps
are reported by `BattleForecast.Run` as
`ForecastStopReason.FatalInvariant` rather than thrown.

**Constructors**

`public ForecastRequest(int maximumTickDelta, int maximumActions, int maximumEvents)`

:   Creates a forecast bound. All three caps are checked at `BattleForecast.Run` time, not here.

    - `maximumTickDelta` &mdash; Ticks to look ahead of the source engine's current tick, not an absolute tick. Valid range is 0 to `SimulationLimits.ForecastTickDelta`.
    - `maximumActions` &mdash; The most action-terminal events the forecast may pass through. Valid range is 1 to `SimulationLimits.ForecastActions`.
    - `maximumEvents` &mdash; The most events the forecast may collect. Valid range is 1 to `SimulationLimits.ForecastEvents`.

**Properties**

`public int MaximumActions`

:   The cap on `ForecastResult.CompletedActions`: how many action-terminal events the forecast may pass through before it stops with `ForecastStopReason.ActionLimit`.

`public int MaximumEvents`

:   The cap on `ForecastResult.Events` before the forecast stops with `ForecastStopReason.EventLimit`.

`public int MaximumTickDelta`

:   Ticks ahead of the source engine's current tick, not an absolute tick. The forecast derives its absolute horizon by adding this to the source tick.

---

## ForecastResult

```csharp
public sealed class ForecastResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Forecast/BattleForecast.cs</small>

Immutable outcome of one `BattleForecast.Run` call: where the
lookahead stopped, the state and events of the throwaway clone it ran,
and the non-authoritative evidence it produced. Only
`BattleForecast` creates it, and holding it has no effect on
the engine it was forecast from.

**Properties**

`public FrozenList<AiDecisionTrace> AiDecisionTraces`

:   Non-authoritative AI decision evidence from the automatic decisions the clone took. It is outside canonical battle state and hashes.

`public int CompletedActions`

:   How many action-terminal events (action completed, interrupted, or skipped) appear in `Events`, which is the count compared against `ForecastRequest.MaximumActions`.

`public Diagnostic? Diagnostic`

:   The typed reason a cap or invariant ended the run. Set only for `ForecastStopReason.ActionLimit`, `ForecastStopReason.EventLimit`, and `ForecastStopReason.FatalInvariant`; null otherwise.

`public FrozenList<BattleEvent> Events`

:   The events the clone emitted, in emission order. They belong to the forecast alone and are not part of the source engine's event chain.

`public FrozenList<FormulaAttributionTrace> FormulaAttributionTraces`

:   Shorthand for `FormulaAttributions.Traces`.

`public FormulaAttributionTraceBatch FormulaAttributions`

:   Non-authoritative formula evidence produced by the clone, likewise outside canonical battle state and hashes.

`public long OmittedFormulaAttributionTraceCount`

:   Shorthand for `FormulaAttributions.OmittedCount`: how many formula traces were produced but dropped to stay inside the documented result-memory bound.

`public long RequestedHorizonTick`

:   The absolute tick the forecast was asked to reach: the source tick plus `ForecastRequest.MaximumTickDelta`. It records the request, not the outcome; only `ForecastStopReason.HorizonReached` means it was reached. When the request itself was rejected this is the source tick.

`public BattleSnapshot Snapshot`

:   State of the throwaway clone where the lookahead stopped. The source engine's own snapshot, hashes, RNG, and history are unchanged, so this is a prediction and never the authoritative battle state.

`public ForecastStopReason StopReason`

:   Why the lookahead stopped, and the first thing to branch on. Only `ForecastStopReason.HorizonReached` means the whole requested window was covered, and only `ForecastStopReason.Terminal` means the battle itself ended inside it; every other value leaves the rest of the window unknown rather than empty.

---

## ForecastStopReason

```csharp
public enum ForecastStopReason : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Forecast/BattleForecast.cs</small>

Why one `BattleForecast.Run` call stopped. Caps are
evaluated only at complete emitted boundaries, so a forecast never stops
part-way through an event.

| Value | Meaning |
| --- | --- |
| `HorizonReached` | The forecast reached `ForecastResult.RequestedHorizonTick` with no earlier stop. |
| `UnknownHumanDecision` | The next decision belongs to a human-controlled actor, so the forecast stopped instead of inventing a command. |
| `Terminal` | A terminal battle result was reached, or the source was already terminal. |
| `NoScheduledWork` | The forecast ran out of scheduled work before the horizon without reaching a terminal result. |
| `ActionLimit` | `ForecastRequest.MaximumActions` was reached. |
| `EventLimit` | `ForecastRequest.MaximumEvents` was reached. |
| `FatalInvariant` | The request was null or out of range, the horizon would overflow, or a step failed. |

---

## GeneratedUiText

```csharp
public sealed class GeneratedUiText : MonoBehaviour
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUGUI/GeneratedUiText.cs</small>

Marks adapter-owned text that participates in presentation themes.

!!! note "Remarks"
    Remove this marker to keep a label's authored font and size.

---

## IBattleFeedbackLayout

```csharp
public interface IBattleFeedbackLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Optional presentation-only reservation for feedback that must stay clear
of the stage and its other information bands.

**Methods**

`public bool TryGetFeedbackBounds(out BattleStageBounds bounds)`

:   Returns the normalized rectangle reserved for feedback.

    - `bounds` &mdash; Receives the reserved rectangle when available.
    - **Returns** &mdash; True when a valid reservation is available.

---

## IBattlePointerBlocker

```csharp
public interface IBattlePointerBlocker
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Optional screen-space hit-test owned by a view.

**Methods**

`public bool BlocksStagePointer(float screenX, float screenY)`

:   Returns whether the view blocks a stage pointer at the coordinates.

    - `screenX` &mdash; Screen-space horizontal coordinate.
    - `screenY` &mdash; Screen-space vertical coordinate.
    - **Returns** &mdash; True when the view owns an opaque hit area at those coordinates.

`public bool OwnsPointerSurface(object surface)`

:   Returns whether the supplied surface belongs to this view.

    - `surface` &mdash; Renderer-specific input-surface identity.
    - **Returns** &mdash; True when the surface belongs to this view.

---

## IBattleStageInformationLayout

```csharp
public interface IBattleStageInformationLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Optional presentation-only choice to group combatant information beside the action stage.

**Properties**

`public bool UseSideInformationBanks`

:   True when the view requests side information banks. This does not change formation or simulation coordinates.

---

## IBattleStageLayout

```csharp
public interface IBattleStageLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Optional authored stage reservation. Custom views may retain the host's framing.

**Methods**

`public bool TryGetStageBounds(out BattleStageBounds bounds)`

:   Provides a presentation-only normalized stage reservation that the host may use for camera framing without changing combat.

    - `bounds` &mdash; Receives the reservation when available.
    - **Returns** &mdash; True when authored bounds are available.

---

## IBattleView

```csharp
public interface IBattleView
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Renderer-neutral contract for rendering state and forwarding intents.

**Events**

`public event Action<BattleViewCommand> CommandChosen`

:   Raised when the view publishes a command choice.

**Methods**

`public void HandleIntent(BattleViewIntent intent)`

:   Handles a user intent.

    - `intent` &mdash; Interaction to process.

`public void Render(BattleViewState state)`

:   Replaces the rendered state.

    - `state` &mdash; Immutable state to render.

---

## IInteractiveBattleView

```csharp
public interface IInteractiveBattleView : IBattleView
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationCore/BattleViewState.cs</small>

Optional interaction surface used by a world-space presentation bridge.
It is deliberately separate from `IBattleView` so existing
adapters and custom views do not acquire a new implementation burden.

**Properties**

`public BattleViewSession Session`

:   Shared selection and submission session.

---

## LowestHealthAllyTargetResolver

```csharp
public sealed class LowestHealthAllyTargetResolver : ITargetResolver
```

`TurnGauge.Samples.CustomMechanics` &middot; <small>Samples/CustomMechanics/LowestHealthAllyTargetResolver.cs</small>

Chooses the living targetable ally with the lowest health ratio.

**Properties**

`public int ContractVersion`

:   Gets the contract version implemented by this resolver.

`public StableId ImplementationId`

:   Gets the stable implementation id used for compatibility checks.

`public TargetRequestContract RequestContract`

:   Gets the request contract requiring one living, targetable ally and no manual picks.

`public StableId ResolverId`

:   Gets the resolver's stable registry id.

`public int TargetContractVersion`

:   Gets the target registry contract version implemented by this resolver.

**Fields**

`public static readonly StableId Id`

:   Stable registry id for this target resolver.

**Methods**

`public FrozenList<StableId> GetCandidates(TargetContext context, PropertySet properties)`

:   Returns the lowest-health living, targetable ally of the acting combatant.

    - `context` &mdash; Snapshot and actor context used to identify allies.
    - `properties` &mdash; Resolver properties, which must be empty.
    - **Returns** &mdash; One candidate id, or an empty list when the actor or allies are unavailable.

`public static StableId SelectLowestHealthRatio(BattleStateView snapshot, FrozenList<StableId> candidates)`

:   Selects the lowest-health-ratio valid candidate from a snapshot.

    - `snapshot` &mdash; Battle snapshot used to resolve candidate ids.
    - `candidates` &mdash; Candidate ids to compare.
    - **Returns** &mdash; The selected id, or the default id when no candidate remains valid.

`public static StableId SelectLowestHealthRatio(IEnumerable<CombatantState> candidates)`

:   Selects the lowest-health-ratio valid combatant from an enumerable.

    - `candidates` &mdash; Combatants to compare.
    - **Returns** &mdash; The selected id, or the default id when no candidate is valid.

`public ValidationReport Validate(TargetValidationContext context, PropertySet properties)`

:   Validates that this resolver receives no custom properties.

    - `context` &mdash; Targeting context used to validate the request.
    - `properties` &mdash; Resolver properties, which must be empty.
    - **Returns** &mdash; A valid report for an empty property set, otherwise an unknown-property diagnostic.

`public TargetRequestResult ValidateRequested(TargetContext context, PropertySet properties, FrozenList<StableId> requested)`

:   Rejects manual picks and accepts the resolver's computed lowest-health ally.

    - `context` &mdash; Snapshot and actor context used to recompute the candidate.
    - `properties` &mdash; Resolver properties, which must be empty.
    - `requested` &mdash; Manual ids supplied by the caller; any non-empty request is rejected.
    - **Returns** &mdash; A rejection for manual requests, otherwise an acceptance containing the computed id.

---

## ParticleArtBinding

```csharp
public sealed class ParticleArtBinding
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/TurnGaugeDemoBootstrap.cs</small>

Nested in `TurnGauge.Presentation.Demo.TurnGaugeDemoBootstrap`.

Binds a recipe VFX key (a particle-* sprite name) to art.

**Fields**

`public Sprite ParticleSprite`

:   Sprite used by the particle effect.

`public string VfxKey`

:   Recipe VFX key whose particle sprite is being bound.

---

## SessionEndState

```csharp
public enum SessionEndState
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/TurnGaugeDemoBootstrap.cs</small>

Nested in `TurnGauge.Presentation.Demo.TurnGaugeDemoBootstrap`.

Typed end-of-session states surfaced by the driver.

| Value | Meaning |
| --- | --- |
| `None` | No battle, or the battle is still running. |
| `TerminalResult` | The engine reported a terminal result (victory, defeat, draw, concession, or the stalled result). |
| `NoScheduledWork` | The engine reported no scheduled work remains. |
| `FatalInvariant` | The engine reported a fatal invariant; the driver stops pumping instead of entering an exception loop. |

---

## TargetCandidateQuery

```csharp
public static class TargetCandidateQuery
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/TargetCandidateQuery.cs</small>

Asks a skill's registered target resolver who it may legally hit right
now, and whether one particular pick would be accepted.

It is the single place the interface and the command translator both go
for that answer, which is what keeps the two from disagreeing: a project
that registers a resolver narrower than its declared contract - front row
only, lowest health only, line of fire - narrows the picker and the
auto-pick together, because both ask the same object the engine will ask.

Everything here is a read. The snapshot is projected into the read-only
view the resolver contract already takes, no command is submitted, and no
RNG is drawn, so consulting it can never change a battle.

**Methods**

`public static FrozenList<StableId> GetCandidates(BattleSnapshot snapshot, CompiledAuthoringCatalog catalog, StableId actorId, StableId skillId)`

:   Lists every combatant the skill's resolver currently considers a legal pick for `actorId`.

    - `snapshot` &mdash; Current authoritative state; read, never advanced.
    - `catalog` &mdash; Compiled content and the registry the resolver is looked up in.
    - `actorId` &mdash; The combatant that would use the skill.
    - `skillId` &mdash; The skill whose resolver is consulted.
    - **Returns** &mdash; Candidate ids, ascending and without duplicates. Empty for a missing argument, an unknown skill, an unregistered resolver, or a resolver that threw; an empty result therefore means "offer no picks" rather than "every combatant is legal".

`public static bool ValidateRequest(BattleSnapshot snapshot, CompiledAuthoringCatalog catalog, StableId actorId, StableId skillId, IReadOnlyList<StableId> requested, out string message)`

:   Puts a proposed pick through the same resolver check the engine runs before it accepts a command.

    - `snapshot` &mdash; Current authoritative state; read, never advanced.
    - `catalog` &mdash; Compiled content and the registry the resolver is looked up in.
    - `actorId` &mdash; The combatant that would use the skill.
    - `skillId` &mdash; The skill whose resolver is consulted.
    - `requested` &mdash; Exactly the ids the command would carry, in pick order. An empty list asks for automatic selection.
    - `message` &mdash; Why the pick would be refused, or an empty string when it would be accepted. It is developer-facing detail, not player-facing text.
    - **Returns** &mdash; True when the resolver accepts the request. A resolver this method cannot reach at all also returns true: the engine remains the authority, and refusing a command the UI merely failed to preview would be worse than letting the engine answer.

---

## TargetPreview

```csharp
public static class TargetPreview
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/TargetPreview.cs</small>

Turns a resolver into the way its affected set should be shown, and a
device into the way a pick should be expressed.

Pure classification over ids the simulation already owns. It adds no
simulation code and reaches no engine: every treatment here is fed by
`TargetCandidateQuery.GetCandidates`, which already exists and
already agrees with the engine. Eight looks, one data source.

**Fields**

`public const int CollapseToSinglePickAt`

:   Below this many candidates a region treatment says nothing. A team scrim drawn around one combatant communicates no more than a reticle would and reads as a bug, which is why a duel collapses to the single-pick look however the resolver is written.

`public const int PerHeadMarkCeiling`

:   Past this many resolved targets, per-head marks stop scaling and the region plus a count does the work instead. Six ticks over six heads is noise; a scrim and the number six is a sentence.

`public const int SlotGridCandidateCeiling`

:   Past this many candidates a side, picking on the stage stops being reliable and the slot grid takes over.

**Methods**

`public static TargetingPreset Adapt(TargetingPreset authored, bool adapt, int candidatesPerSide, bool portrait, bool touch)`

:   The preset a pick should actually be expressed with, given the device and the stage in front of the player. A preset that adapts is worth more than four a buyer has to configure, so the shipped default starts at `TargetingPreset.Reticle` and moves when the situation makes it the wrong tool. A project that wants its authored choice honoured verbatim turns adaptation off.

    - `authored` &mdash; The preset the skin asks for.
    - `adapt` &mdash; False returns `authored` untouched.
    - `candidatesPerSide` &mdash; The largest candidate count on either side.
    - `portrait` &mdash; Whether the stage is taller than it is wide.
    - `touch` &mdash; Whether the device is touch-first.
    - **Returns** &mdash; The preset to drive the pick with.

`public static TargetTreatment ClassifyTreatment(StableId resolverId, TargetLifeState allowedLifeState)`

:   The treatment `resolverId` should be previewed in.

    - `allowedLifeState` &mdash; The life state the resolver accepts. Dead outranks the shape: revive is the one skill that wants a corpse legible, and showing it as an ordinary ally pick is what makes players think it is broken.
    - `resolverId` &mdash; The shipped resolver key, such as `target.one-enemy.v1`.
    - **Returns** &mdash; The matching treatment, or `TargetTreatment.SinglePick` for a resolver this version does not know. A custom resolver therefore gets the reticle rather than nothing, which is wrong in a way a player can see and recover from rather than wrong in a way that looks like a missing feature.

`public static TargetTreatment Degrade(TargetTreatment treatment, int candidateCount)`

:   Degrades a treatment for the party size and stage shape in front of it. Three thresholds decide everything: one candidate, more than `PerHeadMarkCeiling`, and a portrait stage. No per-encounter targeting art, and nothing to re-author when a project changes its party size.

    - `treatment` &mdash; The treatment the resolver classified to.
    - `candidateCount` &mdash; How many combatants the query returned.
    - **Returns** &mdash; The treatment to draw. A region shape with one candidate collapses to the single-pick look; everything else is returned as classified.

`public static bool TakesAPlayerPick(TargetTreatment treatment)`

:   Whether this treatment asks the player to choose, rather than showing them what the resolver has already decided.

    - `treatment` &mdash; The treatment to classify.
    - **Returns** &mdash; True for the three shapes that take a pick. The other five resolve themselves, which is exactly why they still have to be previewed: nothing else will tell the player what is about to be hit.

`public static bool UsesPerHeadMarks(int resolvedCount, bool portrait)`

:   Whether each resolved target gets its own mark, or the region carries a count instead.

    - `resolvedCount` &mdash; How many combatants the shape resolves to.
    - `portrait` &mdash; Whether the stage is taller than it is wide.
    - **Returns** &mdash; False past `PerHeadMarkCeiling`, and false in portrait, where rows run horizontally and a band reads where per-head ticks do not.

---

## TargetTreatment

```csharp
public enum TargetTreatment
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/TargetPreview.cs</small>

The visual language one target shape is previewed in.

There are eight because there are eight kinds of answer a resolver can
give, not because eight looked like a good number. Twelve resolvers ship
and only three of them take a player pick, so a preview built around the
reticle - the interface for exactly one shape - showed the player nothing
at all for the other nine.

| Value | Meaning |
| --- | --- |
| `SinglePick` | One combatant, chosen by the player. |
| `WholeTeam` | A whole side. |
| `Everyone` | Both sides at once. |
| `RandomPool` | N drawn from a pool. |
| `FormationRow` | One formation row, marked at its ground line across the stage. |
| `FormationSide` | One side of the field, filled to a hard vertical edge. |
| `Self` | The actor alone. |
| `DeadTarget` | A corpse, which keeps its greyscale but regains a rim and hit-testing. |

---

## TargetingPreset

```csharp
public enum TargetingPreset
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/Runtime/TargetPreview.cs</small>

How a pick is expressed. It never changes what is legal: legality stays
with the resolver, so a project can swap presets - or offer the choice to
its players as an accessibility setting - without touching content or
invalidating a replay.

| Value | Meaning |
| --- | --- |
| `Reticle` | A cursor living on one candidate. |
| `Direct` | Drag from the card onto a body, or tap card then body. |
| `SlotGrid` | A formation-shaped mini map beside the deck. |
| `AutoConfirm` | No pick step: the resolver decides and one button commits. |

---

## TokenArtBinding

```csharp
public sealed class TokenArtBinding
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/TurnGaugeDemoBootstrap.cs</small>

Nested in `TurnGauge.Presentation.Demo.TurnGaugeDemoBootstrap`.

Binds a starter combatant definition id to its generated
token sprite (the token-* art keys from the art manifest).

**Fields**

`public string CombatantDefinitionId`

:   Stable combatant definition id whose token art is being bound.

`public Sprite TokenSprite`

:   Sprite drawn for the combatant's token.

---

## ToolkitBattleView

```csharp
public sealed class ToolkitBattleView : BattleViewBehaviour, IBattleFeedbackLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUIToolkit/ToolkitBattleView.cs</small>

A replaceable UXML surface. All decision state lives outside the visual tree.

**Properties**

`public VisualTreeAsset LayoutAsset`

:   UXML asset used by the UIDocument; assigning it rebinds the live tree.

`public override BattleUiTechnology Technology`

:   Reports the UI Toolkit backend implemented by this replaceable UXML surface.

`public VisualElement ViewRoot`

:   Currently bound battle root, or null until the document is available.

**Methods**

`public override void ApplyTheme(BattleTheme theme)`

:   Applies the shared theme to the bound UI Toolkit surface.

    - `theme` &mdash; Theme values to apply.

`public override bool BlocksStagePointer(float screenX, float screenY)`

:   Tests whether a screen point belongs to an interactive battle surface.

    - `screenX` &mdash; Screen-space horizontal coordinate.
    - `screenY` &mdash; Screen-space vertical coordinate.
    - **Returns** &mdash; True when the picked element is an interactive battle control.

`public override void BuildDefaultLayout(BattleLayoutIdentity identity)`

:   Replaces the current UXML tree with an immediately generated default layout. Existing document elements are cleared; when the UIDocument has no root, the method only clears the asset assignment and returns.

    - `identity` &mdash; Layout identity requested by the presentation profile.

`public override void Configure(BattlePresentationProfile profile)`

:   Loads the profile's VisualTreeAsset and forwards the profile settings to the base view.

    - `profile` &mdash; Profile whose layout and theme should be used.

`public override bool OwnsPointerSurface(object surface)`

:   Reports whether the last pointer hit belonged to this view's panel.

    - `surface` &mdash; Panel object previously used for the pointer hit.
    - **Returns** &mdash; True only when the last hit was owned by this view and the supplied panel matches.

`public void Rebind()`

:   Explicit refresh hook for editor previews and custom live-reload hosts.

`public override void RefreshBindingsIfNeeded()`

:   Rebinds when UIDocument or required controls changed.

`public void SetVisualHost(VisualElement host, Action<BattleViewIntent> dispatchIntent = null)`

:   Hosts this view in a dedicated public visual container, or returns to its UIDocument when null. The host owns panel attachment and dimensions; this view owns its children and bindings.

    - `host` &mdash; Dedicated container for the authored layout.
    - `dispatchIntent` &mdash; Optional host routing for visual input, such as preview decision guards.

`public bool TryGetFeedbackBounds(out BattleStageBounds bounds)`

:   Finds a clear feedback rectangle using the currently attached visual tree, including the complete timeline header.

    - `bounds` &mdash; Receives the largest normalized area inside the authored stage reservation that avoids visible HUD panels.
    - **Returns** &mdash; True when layout is ready and a clear area exists. False means feedback must wait or stay hidden.

`public override string[] ValidateBindings()`

:   Validates required UXML names and button types without changing battle state.

    - **Returns** &mdash; Diagnostic messages; an empty array means the required bindings are valid.

---

## TurnGaugeDemoBootstrap

```csharp
public sealed class TurnGaugeDemoBootstrap : MonoBehaviour
```

`TurnGauge.Presentation.Demo` &middot; <small>Samples/RuntimeDemo/TurnGaugeDemoBootstrap.cs</small>

The runtime demo driver (specification section 9). It compiles the
starter catalog with built-in registries explicitly at load, offers the
scenario picker over the AUTHORED encounter variants (scheduler and
formation choices are inputs to scenario identity, so picking one of the
eight already-compiled encounters IS the scheduler/formation choice; no
preset is ever swapped on a live start), exposes a user-visible seed
field, owns the `BattleEngine`, and runs the continuous
driver loop from ExecutionSteppingV1 section 7: accumulated presentation
time is converted into an integer requested tick count and handed to
`AdvanceTicks`, whose returned events feed the presenter and whose
snapshots are adopted verbatim.

The DRIVER is the single audited engine owner in the Presentation
assembly (specification section 3 rule 1: "The demo's driver object owns
the engine; the presenter only receives values"); the presenter-purity
audit carves out exactly this demo namespace and nothing else. Pause,
speed, and skip affect presentation only: they scale or halt the
presentation-time accumulator and the visual beat clock, never a
simulation value, so the same (scenario, scheduler, formation, seed)
tuple always reproduces the same hashes. Human-decision scenarios must
author the PauseOnInput scheduler policy so presentation speed cannot
shift submission ticks; the shipped starter scenarios are all-Automatic.
`FatalInvariant`, `NoScheduledWork`, and the stalled terminal
result surface as typed end-of-session states without an exception loop.

**Properties**

`public int AtbCompileErrorCount`

:   Error diagnostic count from the ATB load-time compile.

`public bool AtbCompileSucceeded`

:   True when the assigned ATB showcase catalog compiled.

`public int CompileErrorCount`

:   Error diagnostic count from the primary load-time compile.

`public bool CompileSucceeded`

:   True when the primary catalog compiled with zero errors.

`public IReadOnlyList<StableId> EncounterIds`

:   The authored encounter variants offered by the picker.

`public SessionEndState EndState`

:   The typed end-of-session state of the current battle.

`public bool IsBattleRunning`

:   True when a battle exists and has not reached an end state.

`public bool Paused`

:   Presentation-only pause; halts presentation-time accumulation (and therefore tick pumping) without touching state.

`public StableId? SelectedEncounterId`

:   The picker's currently selected encounter variant.

`public float SpeedMultiplier`

:   The active presentation speed step.

`public StableId? TerminalResultId`

:   The terminal result id when `EndState` is `SessionEndState.TerminalResult` (battle.stalled marks a stall surfaced as a clean terminal result).

**Fields**

`public const float BaseTicksPerSecond`

:   Simulation ticks represented by one presentation second at 1x speed.

`public static readonly float[] SpeedSteps`

:   The specification section 9 presentation speed steps.

**Methods**

`public void CompileCatalog()`

:   Explicitly compiles both starter catalogs with built-in registries (specification section 9: compile at load through the same public entry point the Workbench and tests use). The picker then spans the primary catalog's Action Order variants plus the dedicated ATB catalog's variant; each variant remembers its owning compiled catalog because the engine binds scheduler-adjustment support per catalog at creation (specification section 6).

`public void CycleSpeed()`

:   Cycles the presentation speed through 0.5x/1x/2x/4x.

`public void SelectNextEncounter()`

:   Moves the scenario picker forward through the authored variants.

`public void SelectPreviousEncounter()`

:   Moves the scenario picker backward through the authored variants.

`public void SkipAll()`

:   Finishes every queued presentation beat now (visuals only).

`public bool StartBattle(StableId encounterId, uint seedValue)`

:   Creates the engine for one authored encounter variant from the variant's OWNING compiled catalog (primary or ATB) and binds a fresh presenter to its compiled formation layout.

`public bool StartSelectedBattle()`

:   Starts (or restarts) the picker-selected encounter variant with the current seed value. The variant is an authored, already-compiled start; nothing is re-authored or swapped at runtime.

---

## UguiBattleView

```csharp
public sealed class UguiBattleView : BattleViewBehaviour, IBattleFeedbackLayout
```

`TurnGauge.UI` &middot; <small>Runtime/PresentationUGUI/UguiBattleView.cs</small>

Prefab-authored uGUI surface. Named slots may appear anywhere in the authored tree.

**Properties**

`public RectTransform CustomRoot`

:   Optional authored subtree containing the required named slots.

`public override BattleUiTechnology Technology`

:   Reports the uGUI backend implemented by this prefab-authored surface.

**Methods**

`public override bool BlocksStagePointer(float screenX, float screenY)`

:   Tests whether a screen point falls within a visible raycastable battle slot.

    - `screenX` &mdash; Screen-space horizontal coordinate.
    - `screenY` &mdash; Screen-space vertical coordinate.
    - **Returns** &mdash; True when a visible slot contains the supplied screen point.

`public override void BuildDefaultLayout(BattleLayoutIdentity identity)`

:   Generates the built-in responsive uGUI layout under the selected root.

    - `identity` &mdash; Layout identity used to choose the default arrangement.

`public void Rebind()`

:   Forces slot discovery again after an authored hierarchy change.

`public bool TryGetFeedbackBounds(out BattleStageBounds bounds)`

:   Finds a clear feedback rectangle from the current HUD geometry, without moving the formation or camera.

    - `bounds` &mdash; Receives the largest normalized area inside the authored stage reservation that avoids visible HUD panels.
    - **Returns** &mdash; True when layout is ready and a clear area exists. False means feedback must wait or stay hidden.

`public override string[] ValidateBindings()`

:   Checks required named slots and reports missing, duplicate or incompatible controls.

    - **Returns** &mdash; Diagnostic messages; an empty array means the authored hierarchy is valid.

---

## UiPortraitCrop

```csharp
public readonly struct UiPortraitCrop : IEquatable<UiPortraitCrop>
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UiPortraitCrop.cs</small>

Normalized source-space window used only by a portrait presentation.

**Constructors**

`public UiPortraitCrop(float centerX, float centerY, float width, float height)`

:   Creates a finite normalized source-space crop.

    - `centerX` &mdash; Crop center in normalized source coordinates.
    - `centerY` &mdash; Crop center in normalized source coordinates.
    - `width` &mdash; Crop width between .01 and 1.
    - `height` &mdash; Crop height between .01 and 1.

**Properties**

`public Vector2 Center`

:   Normalized bottom-left source coordinate at the crop center.

`public float Height`

:   Normalized crop height.

`public bool IsConfigured`

:   True when this value contains a configured, finite crop.

`public Vector2 Size`

:   Normalized source-space crop size.

`public float Width`

:   Normalized crop width.

**Fields**

`public static readonly UiPortraitCrop Default`

:   Unconfigured sentinel that selects the unchanged legacy crop.

**Methods**

`public bool Equals(UiPortraitCrop other)`

:   Compares crop components exactly, including the unconfigured sentinel.

    - `other` &mdash; Crop value to compare with this value.
    - **Returns** &mdash; True when both crop values have equal components.

`public override bool Equals(object obj)`

:   Compares this crop with another object.

    - `obj` &mdash; Object to compare with this crop.
    - **Returns** &mdash; True when `obj` is an equal `UiPortraitCrop` value.

`public override int GetHashCode()`

:   Returns a hash derived from the crop components.

    - **Returns** &mdash; A hash code for this crop value.

`public static bool IsValid(float centerX, float centerY, float width, float height)`

:   Checks finite values, normalized bounds and containment.

    - `centerX` &mdash; Crop center in normalized source coordinates.
    - `centerY` &mdash; Crop center in normalized source coordinates.
    - `width` &mdash; Crop width between .01 and 1.
    - `height` &mdash; Crop height between .01 and 1.
    - **Returns** &mdash; True when all values are finite and the crop is contained in normalized space.

`public static bool operator !=(UiPortraitCrop left, UiPortraitCrop right)`

:   Compares two crop values for component inequality.

    - `left` &mdash; First crop value.
    - `right` &mdash; Second crop value.
    - **Returns** &mdash; True when any crop component differs.

`public static bool operator ==(UiPortraitCrop left, UiPortraitCrop right)`

:   Compares two crop values for component equality.

    - `left` &mdash; First crop value.
    - `right` &mdash; Second crop value.
    - **Returns** &mdash; True when both crop values have equal components.

---

## VfxBinding

```csharp
public sealed class VfxBinding
```

`TurnGauge.Runtime` &middot; <small>Runtime/Integration/BattleRuntimeController.cs</small>

Nested in `TurnGauge.Runtime.BattleRuntimeController`.

Maps one presentation VFX key to an optional pooled prototype.

**Fields**

`public string Key`

:   The presentation recipe's VFX key.

`public GameObject Prototype`

:   The pooled GameObject prototype, or null for a diagnostic no-op.

---
