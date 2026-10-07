# Scheduling and tempo

44 types in this area.

!!! abstract "On this page"
    [ActionCostPaymentPolicy](#actioncostpaymentpolicy) &middot; [ActionOrderScheduler](#actionorderscheduler) &middot; [ActionOrderSchedulerStateCodec](#actionorderschedulerstatecodec) &middot; [ActionOrderState](#actionorderstate) &middot; [AtbScheduler](#atbscheduler) &middot; [AtbSchedulerStateCodec](#atbschedulerstatecodec) &middot; [AtbState](#atbstate) &middot; [BattleForecast](#battleforecast) &middot; [BattleSchedulerRegistry](#battleschedulerregistry) &middot; [CompiledActionCost](#compiledactioncost) &middot; [CompiledSkillTiming](#compiledskilltiming) &middot; [CooldownClockKind](#cooldownclockkind) &middot; [CooldownStartPolicy](#cooldownstartpolicy) &middot; [GaugeEntry](#gaugeentry) &middot; [IBattleScheduler](#ibattlescheduler) &middot; [ISchedulerAdjustmentAdapter](#ischeduleradjustmentadapter) &middot; [ISchedulerAdjustmentAdapterProvider](#ischeduleradjustmentadapterprovider) &middot; [ISchedulerStateCodec](#ischedulerstatecodec) &middot; [ISchedulerStateCodecProvider](#ischedulerstatecodecprovider) &middot; [InputPausePolicy](#inputpausepolicy) &middot; [InterruptRefundPolicy](#interruptrefundpolicy) &middot; [ReadyTickEntry](#readytickentry) &middot; [RoundState](#roundstate) &middot; [SchedulerAdjustmentContext](#scheduleradjustmentcontext) &middot; [SchedulerAdjustmentResult](#scheduleradjustmentresult) &middot; [SchedulerAdvanceContext](#scheduleradvancecontext) &middot; [SchedulerAdvanceResult](#scheduleradvanceresult) &middot; [SchedulerAdvanceStopReason](#scheduleradvancestopreason) &middot; [SchedulerCombatantTimingView](#schedulercombatanttimingview) &middot; [SchedulerCreateContext](#schedulercreatecontext) &middot; [SchedulerCreateResult](#schedulercreateresult) &middot; [SchedulerDiagnosticIds](#schedulerdiagnosticids) &middot; [SchedulerDueTimer](#schedulerduetimer) &middot; [SchedulerDueTimerKind](#schedulerduetimerkind) &middot; [SchedulerOpportunityContext](#scheduleropportunitycontext) &middot; [SchedulerOpportunityOutcome](#scheduleropportunityoutcome) &middot; [SchedulerOpportunityResult](#scheduleropportunityresult) &middot; [SchedulerState](#schedulerstate) &middot; [SchedulerStateDecodeResult](#schedulerstatedecoderesult) &middot; [SchedulerStateTag](#schedulerstatetag) &middot; [SchedulerTransitionResult](#schedulertransitionresult) &middot; [SchedulerWork](#schedulerwork) &middot; [SchedulerWorkTag](#schedulerworktag) &middot; [TimingResolutionKind](#timingresolutionkind)

## ActionCostPaymentPolicy

```csharp
public enum ActionCostPaymentPolicy : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

When an action's resource costs are debited. `Acceptance` is the only
supported policy: costs are spent as the command is accepted, before any
cast window, and come back only under
`InterruptRefundPolicy.Full`.

| Value | Meaning |
| --- | --- |
| `Acceptance` | Chooses acceptance semantics for action cost payment policy. |

---

## ActionOrderScheduler

```csharp
public sealed class ActionOrderScheduler : IBattleScheduler, ISchedulerStateCodecProvider
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/ActionOrderScheduler.cs</small>

The built-in round-based scheduler: every eligible combatant is offered
one opportunity per round, in ready-tick order, and the round closes once
all of them have resolved.
A round snapshots the combatants that were eligible when it opened, so one
that becomes eligible partway through waits for the next round instead of
being slotted into the current one, and one that stops being eligible
counts as resolved rather than stalling the round. Speed decides position
inside the round rather than how many turns an actor gets: a finished actor
is given a next ready tick of the current tick plus its recovery scaled by
effective speed, so a fast combatant comes back sooner but still acts once
per round.

**Properties**

`public int SchedulerContractVersion`

:   The scheduler contract version this implementation targets. Resolution matches on ID and version together, so a state saved under another version is refused rather than reinterpreted.

`public StableId SchedulerId`

:   The identity compiled definitions and saved states name to resolve this scheduler, `scheduler.action-order.v1`.

`public ISchedulerStateCodec StateCodec`

:   The canonical codec for this scheduler's state. Because it is exposed here, registering the scheduler does not require naming the codec separately.

**Methods**

`public SchedulerAdvanceResult Advance(SchedulerAdvanceContext context, SchedulerState state)`

:   Moves the schedule to its next boundary, which is the earliest of the leading ready tick, the earliest engine due timer, and the caller's tick ceiling. Stopping on the scheduler's own readiness queues one decision and reports a ready opportunity; stopping on either of the other two only advances timers. The state is normalised first: ready ticks and queued decisions belonging to actors that are no longer eligible are dropped, and participants that lost eligibility are counted as resolved. A round whose participants have all resolved is closed and the next one opened before any readiness is examined, so a round boundary and a new decision never come out of the same call, and at most one decision is queued per call.

    - `context` &mdash; Current tick, timing views, the next opportunity sequence to allocate, the engine's due timers, and the optional tick ceiling.
    - `state` &mdash; The state to advance from. Its `SchedulerState.LastAdvancedTick` must equal the context's current tick.
    - **Returns** &mdash; The next state with its ordered work and stop reason, or a failure carrying `SchedulerDiagnosticIds.StateInvalid` when context and state disagree, `SchedulerDiagnosticIds.RoundOverflow` when the round index cannot be incremented, or `SchedulerDiagnosticIds.OpportunityOverflow` when no further opportunity sequence can be allocated.

`public SchedulerCreateResult Create(SchedulerCreateContext context)`

:   Builds the opening state: every eligible combatant becomes a participant of the first round, and each eligible idle one is given a ready tick of zero, so the battle opens with all of them able to act and ties broken by actor ID.

    - `context` &mdash; The compiled definition, the creation tick, and one timing view per combatant. Only tick zero is accepted.
    - **Returns** &mdash; The initial state, or a failure carrying `SchedulerDiagnosticIds.DefinitionInvalid` when the definition is not an Action Order one at the expected contract version and state tag, `SchedulerDiagnosticIds.NoEligibleCombatants` when nobody can act, or `SchedulerDiagnosticIds.StateInvalid` or `SchedulerDiagnosticIds.SpeedInvalid` when the timing views are not a valid roster.

`public SchedulerTransitionResult OnOpportunityAccepted(SchedulerOpportunityContext context, SchedulerState state)`

:   Drops the head decision as the engine consumes it, leaving everything else untouched. No recovery is charged and no round bookkeeping happens here, because the actor has not finished acting yet.

    - `context` &mdash; The opportunity sequence and actor being consumed, which must identify the current head of the decision queue.
    - `state` &mdash; The state still holding that decision.
    - **Returns** &mdash; The state without that decision plus a single no-work record, or a failure carrying `SchedulerDiagnosticIds.StateInvalid` when the sequence and actor do not match the queue head.

`public SchedulerTransitionResult OnOpportunityFinished(SchedulerOpportunityResult result, SchedulerState state)`

:   Charges the actor's recovery and marks it resolved for the round in progress. The next ready tick is the finish tick plus the recovery scaled by effective speed, and when that resolution completes the round, the round is closed and the next one opened within the same call. Recovery is charged for every outcome, interrupted and skipped included, so an actor cannot act again for free by having its action cut short.

    - `result` &mdash; The finished opportunity, its outcome, and the recovery the actor owes.
    - `state` &mdash; The state after the decision was consumed, which must no longer hold a decision for that actor.
    - **Returns** &mdash; The state with the actor's next readiness recorded, plus the round work if the round closed, or a failure carrying `SchedulerDiagnosticIds.TickOverflow` when the scaled recovery cannot be represented, `SchedulerDiagnosticIds.RoundOverflow` when the round index cannot be incremented, or `SchedulerDiagnosticIds.StateInvalid` otherwise.

---

## ActionOrderSchedulerStateCodec

```csharp
public sealed class ActionOrderSchedulerStateCodec : ISchedulerStateCodec
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/BattleSchedulerRegistry.cs</small>

The canonical state codec for the built-in Action Order scheduler, covering the
decision queue, each actor's next ready tick, and the round bookkeeping.
`BattleSchedulerRegistry.CreateWithBuiltIns` already registers it;
use `Instance` when registering an Action Order scheduler by hand,
since the codec is stateless and has no public constructor.

**Properties**

`public int SchedulerContractVersion`

:   The scheduler contract version this build ships. Payloads written under an earlier version are rejected rather than reinterpreted, so a save from an older build fails loudly instead of decoding into a state that means something else.

`public StableId SchedulerId`

:   Always the built-in Action Order scheduler's ID, which is what confines this codec to that scheduler: the registry refuses to pair it with any other, and a payload naming a different scheduler fails to decode.

`public SchedulerStateTag StateTag`

:   Marks the payload as carrying the Action Order state shape - the decision queue, each actor's next ready tick, and the round bookkeeping.

**Fields**

`public static readonly ActionOrderSchedulerStateCodec Instance`

:   Stateless singleton for canonical Action Order scheduler-state payloads.

**Methods**

`public bool CanHandle(SchedulerState state)`

:   Accepts only a state that names the Action Order scheduler at this contract version, carries the Action Order tag, and populates the Action Order payload with no ATB payload.

    - `state` &mdash; Candidate state to test against the built-in Action Order ID, current version, tag, and exclusive payload shape.
    - **Returns** &mdash; True only for a complete current-version Action Order state with no ATB payload; null and foreign states return false.

`public SchedulerStateDecodeResult DecodePayload(byte[] payload)`

:   Reads bytes written by `EncodePayload` back into a state, checking the scheduler ID, contract version, state tag, entry ordering, and that nothing trails the payload.

    - `payload` &mdash; Candidate canonical Action Order bytes; null, malformed, foreign, oversized, or trailing data produces a failed decode result.
    - **Returns** &mdash; The decoded state, or a failure when the payload is null, empty, oversized, written by another codec, or malformed. It never throws for bad bytes.

`public byte[] EncodePayload(SchedulerState state)`

:   Writes the state to its canonical payload bytes.

    - `state` &mdash; Current-version Action Order state accepted by `CanHandle`.
    - **Returns** &mdash; A newly allocated canonical payload containing scheduler identity, decision queue, ready ticks, and round state.

---

## ActionOrderState

```csharp
public sealed class ActionOrderState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

The Action Order payload of a `SchedulerState`: per-actor ready
ticks plus the round they are being spent in. Present only when the state's
tag is `SchedulerStateTag.ActionOrder`.

**Constructors**

`public ActionOrderState(IEnumerable<ReadyTickEntry> readyTicks, ulong roundIndex, RoundState round)`

:   Creates an Action Order payload. The ready ticks are sorted here into `(readyTick, actorId)` order, at most one per actor and no more than the combatant limit; a null round throws.

    - `roundIndex` &mdash; The 1-based index of the round in progress. Must be positive; it increments once per completed round and is never allowed to wrap.
    - `readyTicks` &mdash; At most one non-null readiness record per actor; entries are copied and sorted by tick then actor ID.
    - `round` &mdash; Required participant and resolution snapshot for the current round.

**Properties**

`public FrozenList<ReadyTickEntry> ReadyTicks`

:   Ready ticks in service order, one entry per actor at most. An actor queued for a decision has no entry here: the owning `SchedulerState` rejects an actor that is both ready and queued.

`public RoundState Round`

:   The round `ReadyTicks` is being spent in. Never null: an Action Order battle is always inside a round, including before anyone has acted, so callers do not have to handle a between-rounds state.

`public ulong RoundIndex`

:   The 1-based index of the round in progress.

**Methods**

`public ReadyTickEntry FindReadyTick(StableId actorId)`

:   Finds the ready-tick entry for `actorId`.

    - `actorId` &mdash; Combatant identifier whose Action Order readiness record is requested.
    - **Returns** &mdash; The entry, or `null` when the actor has none, which is the case while it is queued for a decision or has been removed from the battle.

---

## AtbScheduler

```csharp
public sealed class AtbScheduler : IBattleScheduler, ISchedulerStateCodecProvider
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/AtbScheduler.cs</small>

The built-in gauge-based scheduler: each combatant accrues its raw
effective speed in gauge units per tick, and becomes ready when the gauge
reaches the definition's threshold. There are no rounds, so a fast
combatant genuinely acts more often than a slow one.
The crossing is spent rather than reset: the threshold is subtracted and
the remainder carried, so accumulated overshoot is not thrown away. A gauge
fills only while its actor is eligible, not busy, and not already holding a
queued decision, and after acting it stays frozen until the recovery lock
tick passes. Because several gauges can cross on the same tick, one advance
may queue several decisions at once, which is why the definition's
input-pause policy decides whether time keeps running while a player
decision is outstanding.

**Properties**

`public int SchedulerContractVersion`

:   The scheduler contract version this implementation targets. Resolution matches on ID and version together, so a state saved under another version is refused rather than reinterpreted.

`public StableId SchedulerId`

:   The identity compiled definitions and saved states name to resolve this scheduler, `scheduler.atb.v1`.

`public ISchedulerStateCodec StateCodec`

:   The canonical codec for this scheduler's state. Because it is exposed here, registering the scheduler does not require naming the codec separately.

**Methods**

`public SchedulerAdvanceResult Advance(SchedulerAdvanceContext context, SchedulerState state)`

:   Moves the schedule to its next boundary, which is the earliest of the first gauge crossing, the earliest engine due timer, and the caller's tick ceiling. Stopping on a crossing converts every gauge that reached the threshold into a queued decision in the same call; stopping on either of the other two only fills gauges and advances timers. What happens while a decision is already queued depends on the input-pause policy held in state: an automatic decision, or a human one under `InputPausePolicy.PauseOnInput`, stops the clock entirely; under `InputPausePolicy.WaitForInput` gauges keep filling but are capped one unit below the threshold, so time passes without a second opportunity opening; under `InputPausePolicy.Active` the battle carries on and another combatant may become ready meanwhile.

    - `context` &mdash; Current tick, timing views, the next opportunity sequence to allocate, the engine's due timers, and the optional tick ceiling.
    - `state` &mdash; The state to advance from. Its `SchedulerState.LastAdvancedTick` must equal the context's current tick.
    - **Returns** &mdash; The next state with its ordered work and stop reason, or a failure carrying `SchedulerDiagnosticIds.TickOverflow` when a crossing tick or a gauge total cannot be represented, `SchedulerDiagnosticIds.ReadyQueueLimit` when the crossings would queue more decisions than there are combatants, `SchedulerDiagnosticIds.OpportunityOverflow` when the opportunity sequences cannot be allocated, `SchedulerDiagnosticIds.AtbGaugeInvalid` when a gauge would be left outside its valid range, or `SchedulerDiagnosticIds.StateInvalid` when context and state disagree.

`public SchedulerCreateResult Create(SchedulerCreateContext context)`

:   Builds the opening state, giving every combatant a gauge seeded from its timing view's initial units and no recovery lock. Ineligible combatants still receive a gauge, so the roster stays the same size for the rest of the battle; they simply do not fill. Starting units are what stagger the first wave of turns, and they are required to sit below the threshold, so nobody can be ready before the battle has run a tick.

    - `context` &mdash; The compiled definition, the creation tick, and one timing view per combatant. Only tick zero is accepted.
    - **Returns** &mdash; The initial state, or a failure carrying `SchedulerDiagnosticIds.DefinitionInvalid` when the definition is not an ATB one at the expected contract version and state tag, `SchedulerDiagnosticIds.AtbThresholdInvalid` when the gauge threshold is not positive and within the gauge limit, `SchedulerDiagnosticIds.SpeedInvalid` when an actor would gain more than a full gauge in one tick, `SchedulerDiagnosticIds.AtbGaugeInvalid` when a starting gauge is negative or not below the threshold, or `SchedulerDiagnosticIds.NoEligibleCombatants` when nobody can act.

`public SchedulerTransitionResult OnOpportunityAccepted(SchedulerOpportunityContext context, SchedulerState state)`

:   Drops the head decision as the engine consumes it, leaving every gauge as it was. No recovery lock is applied here, because the actor has not finished acting yet; its gauge simply stays out of the fill while it is busy.

    - `context` &mdash; The opportunity sequence and actor being consumed, which must identify the current head of the decision queue.
    - `state` &mdash; The state still holding that decision.
    - **Returns** &mdash; The state without that decision plus a single no-work record, or a failure carrying `SchedulerDiagnosticIds.StateInvalid` when the sequence and actor do not match the queue head.

`public SchedulerTransitionResult OnOpportunityFinished(SchedulerOpportunityResult result, SchedulerState state)`

:   Freezes the actor's gauge until the finish tick plus its recovery, leaving the accumulated units untouched. The recovery is taken as an absolute number of ticks and is not scaled by speed, so under ATB speed governs how fast the gauge refills afterwards and not how long the pause itself lasts. Recovery is charged for every outcome, interrupted and skipped included, so an actor cannot act again for free by having its action cut short.

    - `result` &mdash; The finished opportunity, its outcome, and the recovery the actor owes.
    - `state` &mdash; The state after the decision was consumed, which must no longer hold a decision for that actor and must already hold a gauge for it.
    - **Returns** &mdash; The state with the actor's recovery lock recorded plus a single no-work record, or a failure carrying `SchedulerDiagnosticIds.TickOverflow` when the lock tick cannot be represented, or `SchedulerDiagnosticIds.StateInvalid` otherwise.

---

## AtbSchedulerStateCodec

```csharp
public sealed class AtbSchedulerStateCodec : ISchedulerStateCodec
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/BattleSchedulerRegistry.cs</small>

The canonical state codec for the built-in ATB scheduler, covering the decision
queue, the gauge threshold and input-pause policy, and each actor's gauge units
and recovery lock. `BattleSchedulerRegistry.CreateWithBuiltIns`
already registers it; use `Instance` when registering an ATB
scheduler by hand, since the codec is stateless and has no public constructor.

**Properties**

`public int SchedulerContractVersion`

:   The scheduler contract version this build ships. Payloads written under an earlier version are rejected rather than reinterpreted, so a save from an older build fails loudly instead of decoding into a state that means something else.

`public StableId SchedulerId`

:   Always the built-in ATB scheduler's ID, which is what confines this codec to that scheduler: the registry refuses to pair it with any other, and a payload naming a different scheduler fails to decode.

`public SchedulerStateTag StateTag`

:   Marks the payload as carrying the ATB state shape - the decision queue, the gauge threshold and input-pause policy, and each actor's gauge units and recovery lock.

**Fields**

`public static readonly AtbSchedulerStateCodec Instance`

:   Stateless singleton for canonical ATB scheduler-state payloads.

**Methods**

`public bool CanHandle(SchedulerState state)`

:   Accepts only a state that names the ATB scheduler at this contract version, carries the ATB tag, and populates the ATB payload with no Action Order payload.

    - `state` &mdash; Candidate state to test against the built-in ATB ID, current version, tag, and exclusive payload shape.
    - **Returns** &mdash; True only for a complete current-version ATB state with no Action Order payload; null and foreign states return false.

`public SchedulerStateDecodeResult DecodePayload(byte[] payload)`

:   Reads bytes written by `EncodePayload` back into a state, checking the scheduler ID, contract version, state tag, gauge ordering, and that nothing trails the payload.

    - `payload` &mdash; Candidate canonical ATB bytes; null, malformed, foreign, oversized, or trailing data produces a failed decode result.
    - **Returns** &mdash; The decoded state, or a failure when the payload is null, empty, oversized, written by another codec, or malformed. It never throws for bad bytes.

`public byte[] EncodePayload(SchedulerState state)`

:   Writes the state to its canonical payload bytes.

    - `state` &mdash; Current-version ATB state accepted by `CanHandle`.
    - **Returns** &mdash; A newly allocated canonical payload containing scheduler identity, decision queue, threshold, pause policy, and actor gauges.

---

## AtbState

```csharp
public sealed class AtbState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

The ATB payload of a `SchedulerState`: the gauge threshold, the
input-pause policy in force, and every actor's gauge. Present only when the
state's tag is `SchedulerStateTag.Atb`.

**Constructors**

`public AtbState(int gaugeThresholdUnits, InputPausePolicy inputPausePolicy, IEnumerable<GaugeEntry> gaugeEntries)`

:   Creates an ATB payload. Gauge entries are sorted here by actor, at most one per actor and no more than the combatant limit, and every one of them must be strictly below `gaugeThresholdUnits`.

    - `gaugeThresholdUnits` &mdash; The units an actor must accumulate to become ready. Copied from the compiled scheduler definition; must be positive and within the ATB gauge limit.
    - `inputPausePolicy` &mdash; How the battle clock behaves while a player decision is pending. Held in state as well as in content so that a corrupted mismatch between the two is rejected.
    - `gaugeEntries` &mdash; At most one gauge per combatant; entries are copied, actor-sorted, and required to remain below the threshold.

**Properties**

`public FrozenList<GaugeEntry> GaugeEntries`

:   Every actor's gauge, sorted by actor and always below the threshold: a gauge that crossed it has already become a decision entry.

`public int GaugeThresholdUnits`

:   The units an actor must accumulate to become ready.

`public InputPausePolicy InputPausePolicy`

:   How the clock behaves while a human decision is pending. It is copied from the compiled scheduler definition and kept here too, so restoring a snapshot whose policy disagrees with the content it is restored against is rejected instead of quietly changing the battle's pacing.

**Methods**

`public GaugeEntry FindGauge(StableId actorId)`

:   Finds the gauge for `actorId`.

    - `actorId` &mdash; Combatant identifier whose ATB gauge and recovery lock are requested.
    - **Returns** &mdash; The entry, or `null` when the actor has no gauge.

---

## BattleForecast

```csharp
public static class BattleForecast
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Forecast/BattleForecast.cs</small>

Read-only lookahead over a live battle. It clones the source engine at
its exact current state and advances only the clone, so calling it cannot
advance the battle, consume its RNG, or change its hashes or history.
Automatic actors are driven by the same compiled decision policies as
live execution; the first human-controlled decision stops the run rather
than being guessed.

**Methods**

`public static ForecastResult Run(BattleEngine source, ForecastRequest request)`

:   Predicts how the battle continues from `source`'s current state, within the caps in `request`. The clone is executed only through the engine's normal step paths, so the prediction is exactly what live execution would produce for the same automatic decisions.

    - `source` &mdash; The engine to forecast from. It is read and cloned, never advanced or mutated.
    - `request` &mdash; The lookahead caps. A null or out-of-range request is reported in the result as `ForecastStopReason.FatalInvariant` instead of throwing.
    - **Returns** &mdash; The stop reason with the clone's resulting snapshot, its emitted events, the action count, and a diagnostic when a cap or invariant ended the run.

---

## BattleSchedulerRegistry

**Start here**

```csharp
public sealed class BattleSchedulerRegistry
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/BattleSchedulerRegistry.cs</small>

The immutable set of turn-order schedulers a battle may use, keyed by scheduler
ID and contract version, each stored with its canonical state codec and its
optional scheduler-adjustment adapter. There is no reflection discovery: a
scheduler the engine, compiler, or serializer asks for must have been registered
here, or the lookup fails with
`SchedulerDiagnosticIds.RegistryMissing`. Every
`Register` call returns a new registry and leaves this one untouched, so a
shared base registry can be extended per game without being copied defensively.

**Methods**

`public static BattleSchedulerRegistry CreateWithBuiltIns()`

:   Creates a registry holding the two built-in schedulers, Action Order and ATB, each with its canonical state codec and its scheduler-adjustment adapter. This is what the engine, the serializer, the replay executor, and the content compiler fall back to when no registry is supplied.

    - **Returns** &mdash; A fresh immutable registry containing Action Order and ATB schedulers, their canonical codecs, and their retiming adapters.

`public BattleSchedulerRegistry Register(IBattleScheduler scheduler)`

:   Registers a scheduler that carries its own codec, taking the codec from `ISchedulerStateCodecProvider` and, when the scheduler also implements `ISchedulerAdjustmentAdapterProvider`, its adjustment adapter as well.

    - `scheduler` &mdash; The scheduler to register. It must implement `ISchedulerStateCodecProvider` and expose a non-null codec.
    - **Returns** &mdash; A new registry holding the existing registrations plus this one; this instance is unchanged.

`public BattleSchedulerRegistry Register(IBattleScheduler scheduler, ISchedulerStateCodec stateCodec)`

:   Registers a scheduler with an explicit state codec and no adjustment adapter. A battle whose content uses the scheduler-adjustment effect then refuses to start on this scheduler, so pass an adapter if any skill, status, or reaction retimes an actor.

    - `scheduler` &mdash; Deterministic implementation with a valid ID and positive contract version not already registered as a pair.
    - `stateCodec` &mdash; Non-null canonical codec whose scheduler ID and contract version match `scheduler` and whose state tag is supported.
    - **Returns** &mdash; A new registry holding the existing registrations plus this one; this instance is unchanged.

`public BattleSchedulerRegistry Register(IBattleScheduler scheduler, ISchedulerStateCodec stateCodec, ISchedulerAdjustmentAdapter adjustmentAdapter)`

:   Registers a scheduler with an explicit state codec and adjustment adapter.

    - `stateCodec` &mdash; The canonical codec for this scheduler's state. Its scheduler ID and contract version must equal the scheduler's, and its state tag must be Action Order or ATB.
    - `adjustmentAdapter` &mdash; How effects retime an actor under this scheduler, or null when the scheduler supports no adjustments. When given, its scheduler ID and contract version must match the scheduler's.
    - `scheduler` &mdash; Deterministic implementation whose valid ID and positive contract version form the unique registration key.
    - **Returns** &mdash; A new registry holding the existing registrations plus this one; this instance is unchanged.

`public BattleSchedulerResolveResult Resolve(StableId schedulerId, int schedulerContractVersion)`

:   Looks up the scheduler registered under an exact ID and contract version, together with its state codec and its adjustment adapter.

    - `schedulerContractVersion` &mdash; The version the caller requires. The same ID registered at a different version does not match, which is what stops an older saved state from being reinterpreted by a newer scheduler.
    - `schedulerId` &mdash; Stable scheduler registry key to match ordinally; an unknown or invalid ID produces a typed missing result rather than an exception.
    - **Returns** &mdash; A successful result carrying the scheduler, its codec, and its adjustment adapter, which is null when none was registered; otherwise a failed result whose diagnostic is `SchedulerDiagnosticIds.VersionUnsupported` when the ID is registered at another version, or `SchedulerDiagnosticIds.RegistryMissing` when the ID is not registered at all. An unknown scheduler is reported, never thrown.

---

## CompiledActionCost

```csharp
public sealed class CompiledActionCost
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

One resource cost of an action: which resource is spent, and how much. The
amount is always positive, and it is debited when the command is accepted
rather than when the action resolves.

**Constructors**

`public CompiledActionCost(StableId resourceId, int amount)`

:   Pairs one valid resource identifier with the strictly positive amount debited at command acceptance.

    - `amount` &mdash; Units to spend; must be greater than zero.
    - `resourceId` &mdash; Resource pool to debit; an empty or otherwise invalid stable identifier is rejected.

**Properties**

`public int Amount`

:   Units spent, always greater than zero. A cost the actor cannot afford in full stops the command being accepted rather than being partly paid.

`public ActionCostPaymentPolicy PaymentPolicy`

:   When the cost is debited. Only `ActionCostPaymentPolicy.Acceptance` is supported, so the resource is gone before the cast window even opens and an interrupted cast gets it back only under `InterruptRefundPolicy.Full`.

`public StableId ResourceId`

:   The resource this cost is drawn from. A skill carries at most one cost per resource, so two entries never both debit the same pool.

---

## CompiledSkillTiming

```csharp
public sealed class CompiledSkillTiming
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

The compiled timing, cooldown, cost, and target-count contract for one
skill. The engine reads it when it accepts a command and again when the
action resolves, so every field is checked here rather than at use: an
instance that exists has already passed the simulation's structural limits.

**Constructors**

`public CompiledSkillTiming(StableId skillId, int castTicks, int recoveryTicks, bool interruptible, InterruptRefundPolicy interruptRefundPolicy, CooldownStartPolicy cooldownStartPolicy, CooldownClockKind cooldownClockKind, int cooldownAmount, int minimumRequestedTargets, int maximumRequestedTargets, TimingResolutionKind timingResolutionKind, IEnumerable<CompiledActionCost> costs)`

:   Creates a skill timing record, rejecting any field that falls outside the simulation's structural limits.

    - `castTicks` &mdash; Ticks between acceptance and resolution; zero resolves the action in the step that accepts it.
    - `recoveryTicks` &mdash; Ticks the actor stays locked out after the action finishes; must be greater than zero.
    - `interruptible` &mdash; Whether the cast window may be interrupted. It has no effect when `castTicks` is zero, because no cast window exists.
    - `cooldownAmount` &mdash; Cooldown length in the unit chosen by `cooldownClockKind`; zero means the skill has no cooldown.
    - `minimumRequestedTargets` &mdash; Fewest target IDs a command for this skill may carry.
    - `maximumRequestedTargets` &mdash; Most target IDs a command for this skill may carry; may not be below `minimumRequestedTargets`.
    - `costs` &mdash; Resource costs. They are copied and sorted by resource ID, and a repeated resource ID is rejected.
    - `cooldownClockKind` &mdash; Clock domain in which `cooldownAmount` is measured; undefined values are rejected.
    - `cooldownStartPolicy` &mdash; Event - acceptance or resolution - that starts the skill's cooldown.
    - `interruptRefundPolicy` &mdash; Whether an interrupted cast restores costs already paid at acceptance.
    - `skillId` &mdash; Valid stable identifier of the skill whose timing contract is being compiled.
    - `timingResolutionKind` &mdash; Extra timing-layer operation performed at resolution, such as interrupting the first locked cast.

**Properties**

`public int CastTicks`

:   Ticks between acceptance and resolution; zero resolves in the accepting step.

`public int CooldownAmount`

:   Cooldown length in the unit named by `CooldownClockKind`; zero means none.

`public CooldownClockKind CooldownClockKind`

:   The unit `CooldownAmount` is counted in: elapsed simulation ticks, or the owner's own finished opportunities after the one that started the cooldown. The second makes the cooldown track how often the actor acts rather than how much time passes, and only the chosen clock ever runs.

`public CooldownStartPolicy CooldownStartPolicy`

:   Whether the cooldown starts as the command is accepted or only once the action resolves. Under `CooldownStartPolicy.Resolve` a cast interrupted before it resolves leaves the skill immediately reusable.

`public FrozenList<CompiledActionCost> Costs`

:   Resource costs, sorted by resource ID, with at most one entry per resource.

`public InterruptRefundPolicy InterruptRefundPolicy`

:   What becomes of the costs already paid when this skill's cast is interrupted. A refund is clamped to the room left below each resource's maximum, so it can come back partial.

`public bool Interruptible`

:   Whether the cast window may be interrupted; irrelevant when `CastTicks` is zero.

`public int MaximumRequestedTargets`

:   Most target IDs a command for this skill may carry.

`public int MinimumRequestedTargets`

:   Fewest target IDs a command for this skill may carry.

`public int RecoveryTicks`

:   Ticks the actor stays locked out after the action finishes; always at least one.

`public StableId SkillId`

:   The skill these timings apply to. Timings are keyed by skill and not by actor, so every combatant that uses the skill starts from the same declared cast, recovery, and cooldown numbers. Recovery is the one that does not stay identical in play: the Action Order scheduler divides `RecoveryTicks` by the acting combatant's effective speed when it sets that actor's next ready tick, so a faster actor comes back sooner from the same skill.

`public TimingResolutionKind TimingResolutionKind`

:   Timing-layer work the skill performs as it resolves, on top of its own effects. `TimingResolutionKind.InterruptFirstLockedCast` only makes sense for an instant single-target skill, so pairing it with cast ticks or any other target count is rejected here rather than surfacing as a contradiction mid-battle.

---

## CooldownClockKind

```csharp
public enum CooldownClockKind : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

The clock a cooldown counts down on. `ElapsedTicks` counts simulation
ticks; `OwnerOpportunities` counts the owner's later finished
opportunities, excluding the one that started the cooldown. A cooldown runs
on one clock only, and the other remaining counter on
`CooldownState` stays zero.

| Value | Meaning |
| --- | --- |
| `ElapsedTicks` | Chooses elapsed ticks semantics for cooldown clock kind. |
| `OwnerOpportunities` | Chooses owner opportunities semantics for cooldown clock kind. |

---

## CooldownStartPolicy

```csharp
public enum CooldownStartPolicy : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

When a skill's cooldown clock starts. `Queue` starts it as the command
is accepted, before any cast window; `Resolve` starts it only once the
action resolves, so a cast interrupted before that point starts none.

| Value | Meaning |
| --- | --- |
| `Queue` | Chooses queue semantics for cooldown start policy. |
| `Resolve` | Chooses resolve semantics for cooldown start policy. |

---

## GaugeEntry

```csharp
public sealed class GaugeEntry
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

One ATB actor's gauge: how far it has filled toward the scheduler's
threshold, plus the tick until which filling stays suppressed after the
actor acted. Persisted gauges are always below the threshold, because a
crossing is converted into a decision entry and only the remainder kept.

**Constructors**

`public GaugeEntry(StableId actorId, int gaugeUnits, long recoveryLockUntilTick)`

:   Creates a gauge entry. An unset actor, a negative gauge, or a negative recovery lock throws. The threshold is not known here, so it is `AtbState` that rejects a gauge at or above it.

    - `actorId` &mdash; Valid combatant identifier whose deterministic ATB progress this entry records.
    - `gaugeUnits` &mdash; Non-negative accumulated progress; the owning `AtbState` additionally requires it below the readiness threshold.
    - `recoveryLockUntilTick` &mdash; Non-negative absolute tick through which this actor's gauge remains frozen after acting.

**Properties**

`public StableId ActorId`

:   The combatant whose gauge this is. Entries are ordered by this ID rather than by gauge, so the same set of gauges always serialises to the same bytes however it was assembled.

`public int GaugeUnits`

:   Accumulated gauge units. Filling adds the actor's raw effective speed per tick, and an actor that is queued, busy, or ineligible does not fill at all.

`public long RecoveryLockUntilTick`

:   The tick until which this gauge stays frozen after the actor acted; `0` means unlocked. No units accrue at or before it.

---

## IBattleScheduler

**Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IBattleScheduler
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

The pure turn-order contract. An implementation decides only when an actor
may act; the engine keeps ownership of time, events, commands, and battle
state. Implement it to add a turn-order family beyond the built-in Action
Order and ATB schedulers.

!!! note "Remarks"
    Every method must be a deterministic function of its arguments alone:
    identical inputs must produce identical results on every machine, every run,
    and every culture. An implementation must not emit events, mutate a snapshot,
    submit commands, draw RNG, read the clock or any other ambient state, or
    retain a collection it was handed. `SchedulerState` is immutable,
    so return a new state instead of editing the one supplied. Each call either
    succeeds with a complete new state or fails with a diagnostic and changes
    nothing; there is no partial transition. Register the implementation
    explicitly with `BattleSchedulerRegistry` together with a
    canonical state codec - there is no reflection discovery, and an unregistered
    scheduler fails with
    `SchedulerDiagnosticIds.RegistryMissing`.

**Properties**

`public int SchedulerContractVersion`

:   Version of this scheduler contract the implementation targets; it must be positive. Resolution matches on ID and version together, so raising the version deliberately stops older saved states from loading rather than reinterpreting them.

`public StableId SchedulerId`

:   Stable identity a compiled definition and a saved state refer to. It is half of the registry key, so the same ID may be registered only once per contract version.

**Methods**

`public SchedulerAdvanceResult Advance(SchedulerAdvanceContext context, SchedulerState state)`

:   Moves the schedule forward from the state's last advanced tick to its next boundary. Advance to the earliest of the scheduler's own next readiness, the earliest due timer, and the caller's tick ceiling, and never past it; ticks in between may be jumped as long as the result equals what per-tick execution would produce. Return work in the exact order the engine must apply it, and report a no-work record with the stop reason when nothing happens.

    - `context` &mdash; Current tick, timing views, the next opportunity sequence to allocate, the due timers, and the optional tick ceiling.
    - `state` &mdash; The current state, whose `SchedulerState.LastAdvancedTick` equals the context's current tick.
    - **Returns** &mdash; The next state with its ordered work and stop reason, or a failure.

`public SchedulerCreateResult Create(SchedulerCreateContext context)`

:   Builds the initial scheduler state at battle start, deciding who is immediately ready and what each actor's starting timing is.

    - `context` &mdash; The compiled definition, the creation tick, and one timing view per combatant.
    - **Returns** &mdash; The initial state, or a failure whose diagnostic prevents the battle from starting.

`public SchedulerTransitionResult OnOpportunityAccepted(SchedulerOpportunityContext context, SchedulerState state)`

:   Called once as the engine consumes the head of the decision queue, before the actor's command resolves. Remove that decision from the returned state; the actor is not finished acting yet, so do not charge recovery here.

    - `context` &mdash; The opportunity sequence and actor being consumed, which must identify the current queue head.
    - `state` &mdash; The state still holding that decision.
    - **Returns** &mdash; The state without that decision, or a failure, which the engine treats as fatal.

`public SchedulerTransitionResult OnOpportunityFinished(SchedulerOpportunityResult result, SchedulerState state)`

:   Called once after an opportunity completes, is interrupted, or is skipped. This is where recovery is charged and the actor's next readiness is set, and where a round-based scheduler marks the actor resolved and may open the next round.

    - `result` &mdash; The finished opportunity, its outcome, and the recovery the actor owes.
    - `state` &mdash; The state after the decision was consumed, which must no longer hold a decision for that actor.
    - **Returns** &mdash; The state with the actor's next readiness recorded plus any work the finish created, or a failure, which the engine treats as fatal.

---

## ISchedulerAdjustmentAdapter

**Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface ISchedulerAdjustmentAdapter
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerAdjustment.cs</small>

Lets an effect retime one actor inside a scheduler's state - hasten it, delay it,
or push its ATB gauge - without the effect knowing how that scheduler measures
time. It is the only route by which the `AdjustScheduler` effect primitive
can reach turn order, so a scheduler family that wants hasten-and-delay skills
needs one.

!!! note "Remarks"
    Register the adapter alongside its scheduler through
    `BattleSchedulerRegistry`. `SchedulerId` and
    `SchedulerContractVersion` must equal that scheduler's or
    registration throws, and a scheduler registered without an adapter simply cannot
    be adjusted: the effect fails rather than quietly doing nothing.
    `Apply` must be a deterministic function of its two arguments alone -
    no RNG, no clock, no ambient state - and must neither mutate nor retain them;
    `SchedulerState` is immutable, so return a new state.
    It must also change nothing the request does not name. The engine independently
    recomputes the expected state, actual delta, and work, compares them against what
    the adapter returned, and on any difference ends the step with
    `StepEventOutcome.FatalInvariant` and
    `SchedulerDiagnosticIds.StateInvalid`, rolling back to the last valid
    snapshot. In practice that means reproducing the built-in rules exactly: clamp a
    ready tick so it never lands before the current tick, clamp a gauge to zero and to
    its readiness threshold, and when a gauge reaches that threshold reset it and
    queue exactly one opportunity using
    `SchedulerAdjustmentContext.NextOpportunitySequence`. An adapter that
    invents its own arithmetic will be rejected at runtime, not silently honoured.

**Properties**

`public int SchedulerContractVersion`

:   The scheduler contract version this adapter targets; it must match the registered scheduler's version.

`public StableId SchedulerId`

:   The scheduler this adapter retimes. It must match the scheduler it is registered with, or `BattleSchedulerRegistry` rejects the registration.

**Methods**

`public SchedulerAdjustmentResult Apply(SchedulerAdjustmentContext context, SchedulerState state)`

:   Applies one adjustment, returning a new state rather than editing the one supplied. Verify the request first - that the kind is supported, that the state is this scheduler's and stands at the context's current tick, and that the actor is present, eligible, and not busy - and refuse it with a diagnostic instead of throwing.

    - `context` &mdash; The actor, the kind of adjustment, the requested delta, the timing views, and the next opportunity sequence available.
    - `state` &mdash; The current scheduler state, whose `SchedulerState.LastAdvancedTick` equals the context's current tick.
    - **Returns** &mdash; The retimed state with the delta actually applied and any readiness it opened, or a failure carrying the unchanged state.

`public bool Supports(SchedulerAdjustmentKind kind)`

:   Reports whether this adapter can apply that kind of adjustment. The engine calls it before `Apply`, and a false answer fails the effect outright instead of turning it into a no-op, so answer for the quantities the scheduler actually keeps - the built-in Action Order adapter accepts only `SchedulerAdjustmentKind.ReadyTickDelta` and the ATB adapter only `SchedulerAdjustmentKind.GaugeDelta`. It must be a pure function of `kind` and must not throw.

    - `kind` &mdash; Requested scheduler quantity, including unknown enum values that implementations must answer without throwing.
    - **Returns** &mdash; True only when this adapter can deterministically apply that adjustment category to its scheduler state.

---

## ISchedulerAdjustmentAdapterProvider

**Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface ISchedulerAdjustmentAdapterProvider
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerAdjustment.cs</small>

Implemented by a scheduler that carries its own adjustment adapter, so
`BattleSchedulerRegistry.Register(IBattleScheduler)` picks it up
without the caller naming it separately.

!!! note "Remarks"
    The adapter must match the scheduler's ID and contract version, or registration
    throws. Returning null is allowed and means the scheduler cannot be retimed by an
    effect; every other part of the scheduler still works.

**Properties**

`public ISchedulerAdjustmentAdapter AdjustmentAdapter`

:   Adapter automatically registered alongside the scheduler, or null when that scheduler deliberately exposes no retiming effect.

---

## ISchedulerStateCodec

**Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface ISchedulerStateCodec
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/BattleSchedulerRegistry.cs</small>

The canonical byte form of one scheduler's state. Every canonical battle-state
write and read routes `SchedulerState` through the codec registered
alongside its scheduler, so this is what makes a scheduler's state saveable,
replayable, and hashable.

!!! note "Remarks"
    `SchedulerId` and `SchedulerContractVersion` must equal
    those of the scheduler the codec is registered with, and
    `StateTag` must be one of the two built-in state shapes;
    `BattleSchedulerRegistry` rejects the registration otherwise.
    Encoding must be deterministic and lossless: the serializer encodes the state,
    decodes the payload again, requires the decoded state to be identical to the
    original in canonical form, and then keeps the decoded state - so a codec that
    drops, reorders, or rounds a field does not merely lose detail, it changes the
    battle-state hash or fails the write outright. The same state must produce the
    same bytes on every machine, run, and culture. `SchedulerState` is
    immutable, so neither method may mutate or retain what it is handed, and
    neither may read the clock or any other ambient state.

**Properties**

`public int SchedulerContractVersion`

:   The contract version this payload layout belongs to; it must match the registered scheduler's version. Raising it therefore stops older payloads from decoding rather than letting them be reinterpreted.

`public StableId SchedulerId`

:   The scheduler this codec speaks for. It must match the registered scheduler's ID, and a payload naming a different ID must fail to decode.

`public SchedulerStateTag StateTag`

:   Which of the two state shapes this codec encodes. The registry accepts only `SchedulerStateTag.ActionOrder` or `SchedulerStateTag.Atb`, so a custom scheduler must reuse one of them rather than invent a third.

**Methods**

`public bool CanHandle(SchedulerState state)`

:   Reports whether this codec owns the given state. The engine and the serializer call it before encoding and again on the decoded result, so it must accept exactly the states this codec can round-trip, and return false rather than throw for a null or foreign state.

    - `state` &mdash; Candidate scheduler state, which may be null or belong to a different implementation.
    - **Returns** &mdash; True only when scheduler ID, contract version, state tag, and payload shape are all encodable by this codec.

`public SchedulerStateDecodeResult DecodePayload(byte[] payload)`

:   Rebuilds a state from bytes produced by `EncodePayload`.

    - `payload` &mdash; The bytes to read. A null, empty, truncated, oversized, foreign, or otherwise malformed payload must be reported as a failed result rather than thrown; the canonical reader turns a failed decode into a read diagnostic, whereas an escaping exception reaches the caller.
    - **Returns** &mdash; The decoded state, or a failure carrying `SchedulerDiagnosticIds.StateInvalid`.

`public byte[] EncodePayload(SchedulerState state)`

:   Encodes a state this codec accepts into its canonical payload bytes.

    - `state` &mdash; Non-null scheduler state previously accepted by `CanHandle`; foreign state is rejected rather than coerced.
    - **Returns** &mdash; A self-contained payload that also carries the scheduler ID, contract version, and state tag, so `DecodePayload` can verify them.

---

## ISchedulerStateCodecProvider

**Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface ISchedulerStateCodecProvider
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/BattleSchedulerRegistry.cs</small>

Implemented by a scheduler that carries its own canonical state codec, so it can
be handed to `BattleSchedulerRegistry.Register(IBattleScheduler)`
without the caller naming the codec separately.

!!! note "Remarks"
    `StateCodec` must never be null and must be the canonical codec for
    this scheduler - same scheduler ID and contract version - or registration throws.

**Properties**

`public ISchedulerStateCodec StateCodec`

:   Non-null canonical codec automatically paired with the implementing scheduler during registration.

---

## InputPausePolicy

```csharp
public enum InputPausePolicy : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

What the ATB scheduler does with time while a human decision is pending.
`Active` keeps gauges filling, so a second combatant can become ready
too; `WaitForInput` keeps gauges filling but caps them one unit below
the readiness threshold, so no second opportunity opens; `PauseOnInput`
stops the scheduler advancing at all. This is an ATB-only setting, and an
Action Order definition must leave it unset.

| Value | Meaning |
| --- | --- |
| `Active` | Chooses active semantics for input pause policy. |
| `WaitForInput` | Chooses wait for input semantics for input pause policy. |
| `PauseOnInput` | Chooses pause on input semantics for input pause policy. |

---

## InterruptRefundPolicy

```csharp
public enum InterruptRefundPolicy : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

What happens to the costs already paid for an action whose cast is
interrupted. `None` keeps them spent; `Full` restores them, each
clamped to the room left below its resource maximum, so a refund can be
partial when the resource has meanwhile refilled.

| Value | Meaning |
| --- | --- |
| `None` | Chooses none semantics for interrupt refund policy. |
| `Full` | Chooses full semantics for interrupt refund policy. |

---

## ReadyTickEntry

```csharp
public sealed class ReadyTickEntry
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

The earliest tick at which one Action Order actor may next be offered an
opportunity. Eligible idle combatants start at tick 0; a finished actor
receives a fresh entry whose delay is scaled by its effective speed.

**Constructors**

`public ReadyTickEntry(StableId actorId, long readyTick)`

:   Creates a ready-tick entry. An unset actor or a negative ready tick throws.

    - `actorId` &mdash; Valid combatant identifier whose next Action Order opportunity is being scheduled.
    - `readyTick` &mdash; Non-negative absolute battle tick at or after which the actor may become ready.

**Properties**

`public StableId ActorId`

:   The combatant this ready tick belongs to. An actor already queued for a decision carries no entry here at all, rather than one with a far-off tick.

`public long ReadyTick`

:   The earliest tick this actor may act on. A tick already in the past is treated as the current tick, so a stale entry cannot rewind the clock.

---

## RoundState

```csharp
public sealed class RoundState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

One Action Order round: the participants snapshotted when the round began
and the subset that has already resolved. The round is complete once the
two sets are the same size, which is what makes the scheduler close it and
start the next one.

**Constructors**

`public RoundState(long startedTick, IEnumerable<StableId> participantIds, IEnumerable<StableId> resolvedParticipantIds)`

:   Creates a round. Both identifier sets are sorted here, so caller order does not matter, but they must hold valid unique IDs, the resolved set must be a subset of the participants, and the participant count may not exceed the combatant limit.

    - `startedTick` &mdash; The tick the round began on. The owning `SchedulerState` additionally rejects a round that begins after its own tick.
    - `resolvedParticipantIds` &mdash; Participants that already acted this round, or that stopped being eligible during it.
    - `participantIds` &mdash; Valid unique actors eligible when the round opened; the set is sorted and frozen independently of caller order.

**Properties**

`public FrozenList<StableId> ParticipantIds`

:   The actors that were eligible when the round began. A combatant that becomes eligible later is not offered an opportunity until the next round snapshots it.

`public FrozenList<StableId> ResolvedParticipantIds`

:   The participants that can no longer act this round, whether because they finished acting or because they stopped being eligible.

`public long StartedTick`

:   The tick this round began on. The owning `SchedulerState` rejects a round that starts after its own tick, so this is never in the future relative to the state holding it.

**Methods**

`public bool ContainsParticipant(StableId actorId)`

:   Whether `actorId` is in this round's participant snapshot. Non-participants are not offered opportunities this round.

    - `actorId` &mdash; Combatant identifier to search in the immutable round-start participant set.
    - **Returns** &mdash; True when the actor belonged to the participant snapshot captured at round start; otherwise false.

`public bool IsResolved(StableId actorId)`

:   Whether `actorId` has already resolved this round. A resolved participant is passed over even when its ready tick is the smallest, until the next round begins.

    - `actorId` &mdash; Participant identifier to search in the immutable resolved subset.
    - **Returns** &mdash; True when the participant has acted or become ineligible during this round; otherwise false.

---

## SchedulerAdjustmentContext

```csharp
public sealed class SchedulerAdjustmentContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerAdjustment.cs</small>

Immutable input to `ISchedulerAdjustmentAdapter.Apply`: which actor
is being retimed, whether its ready tick or its ATB gauge moves, and by how
much. It carries no authoritative battle state, so an adjustment can reach turn
order and nothing else.

**Constructors**

`public SchedulerAdjustmentContext(long currentTick, StableId actorId, SchedulerAdjustmentKind kind, long delta, IEnumerable<SchedulerCombatantTimingView> combatants, ulong nextOpportunitySequence)`

:   Describes one requested adjustment and freezes the timing views into an actor-ID-ordered snapshot, so later changes to the caller's collection cannot reach the adapter.

    - `currentTick` &mdash; The tick the adjustment is requested on. It must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it, or the built-in adapters refuse the adjustment with `SchedulerDiagnosticIds.StateInvalid`.
    - `actorId` &mdash; The actor being retimed. For the `AdjustScheduler` effect primitive that is the effect's target, not the caster. Required.
    - `delta` &mdash; The requested signed change: ticks for `SchedulerAdjustmentKind.ReadyTickDelta`, gauge units for `SchedulerAdjustmentKind.GaugeDelta`. Negative hastens the actor, and the value is clamped rather than rejected when it would run past a bound.
    - `combatants` &mdash; Every combatant in the battle, eligible or not. Required, and entries must be non-null.
    - `nextOpportunitySequence` &mdash; The first opportunity sequence the adapter may assign should the adjustment itself make the actor ready. It may not be zero.
    - `kind` &mdash; Scheduler quantity to retime: absolute Action Order readiness or accumulated ATB gauge.

**Properties**

`public StableId ActorId`

:   The actor being retimed. The built-in adapters require it to appear in `Combatants`, to be eligible, and not to be busy, so an actor mid-action or out of the fight cannot be retimed.

`public FrozenList<SchedulerCombatantTimingView> Combatants`

:   Every combatant in the battle, including ineligible ones, sorted by actor ID.

`public long CurrentTick`

:   The tick the adjustment is requested on, which must equal `SchedulerState.LastAdvancedTick` of the state being adjusted.

`public long Delta`

:   The requested signed change - ticks for a ready-tick adjustment, gauge units for a gauge adjustment. Clamping may shrink it, so read `SchedulerAdjustmentResult.ActualDelta` rather than assuming it was applied in full.

`public SchedulerAdjustmentKind Kind`

:   Which quantity `Delta` moves: a ready tick or an ATB gauge. Each built-in adapter accepts exactly one of the two, so this decides whether a hasten-or-delay effect can reach the scheduler in play at all - an unsupported kind fails the effect rather than passing quietly.

`public ulong NextOpportunitySequence`

:   The first opportunity sequence this adjustment may assign, needed only when the adjustment makes the actor ready. Allocate consecutively from it, one per ready opportunity returned, because the engine advances its own counter by exactly that many.

---

## SchedulerAdjustmentResult

```csharp
public sealed class SchedulerAdjustmentResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerAdjustment.cs</small>

Outcome of `ISchedulerAdjustmentAdapter.Apply`: the scheduler state
after the adjustment, how much of the requested delta survived clamping, and any
readiness the adjustment itself opened. A failure carries the unchanged input
state rather than null, so a refused adjustment leaves turn order exactly as it
was.

**Properties**

`public long ActualDelta`

:   How much of `SchedulerAdjustmentContext.Delta` the new state actually reflects, after the built-in floors: a ready tick never moves earlier than the current tick, and a gauge is clamped to zero below and to its readiness threshold above. Zero on failure.

`public Diagnostic? Diagnostic`

:   The failure detail, or null when the adjustment succeeded.

`public SchedulerState State`

:   The state after the adjustment, or the unchanged input state when the adjustment was refused. It is never null.

`public bool Succeeded`

:   True when the adapter applied the adjustment. On false the adjustment touched nothing: `State` is the input state, `Work` is empty, `ActualDelta` is zero, and `Diagnostic` holds the reason.

`public FrozenList<SchedulerWork> Work`

:   Work the adjustment created, in the order the engine must apply it, and always empty on failure. The built-in adapters produce a single `SchedulerWorkTag.ReadyOpportunity` record when a gauge adjustment reaches the readiness threshold, and nothing otherwise.

**Methods**

`public static SchedulerAdjustmentResult Failure(SchedulerState unchangedState, Diagnostic diagnostic)`

:   Reports that the adjustment was refused. The engine raises the diagnostic and rolls the step back, so the battle keeps its last valid snapshot.

    - `unchangedState` &mdash; The state the adapter was handed, returned untouched. Required.
    - `diagnostic` &mdash; Why the adjustment was refused. Prefer an ID from `SchedulerDiagnosticIds` so tooling classifies the failure.
    - **Returns** &mdash; A failed result that preserves `unchangedState`, emits no work, applies zero delta, and carries the diagnostic.

`public static SchedulerAdjustmentResult Success(SchedulerState state, long actualDelta, IEnumerable<SchedulerWork> work = null)`

:   Reports an applied adjustment and freezes the work into an immutable list, so a later change to the caller's collection cannot reach the engine.

    - `state` &mdash; The state after the adjustment. Required.
    - `actualDelta` &mdash; How much of the requested delta the new state reflects, after clamping. The engine reports it on the scheduler-adjusted event, so it is what a UI can show as the retiming that landed.
    - `work` &mdash; Work the adjustment created, in application order - a ready opportunity when the adjustment made the actor ready. Null means none.
    - **Returns** &mdash; A successful result owning the supplied state, frozen work records, actual clamped delta, and no diagnostic.

---

## SchedulerAdvanceContext

```csharp
public sealed class SchedulerAdvanceContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Immutable input to `IBattleScheduler.Advance`: the current
tick, one timing view per combatant, the next opportunity sequence the
scheduler may allocate, the engine's due timers, and the caller's optional
tick ceiling. A scheduler may jump over empty ticks, but never past the
earliest due timer or the ceiling.

**Constructors**

`public SchedulerAdvanceContext(long currentTick, IEnumerable<SchedulerCombatantTimingView> combatants, ulong nextOpportunitySequence, IEnumerable<SchedulerDueTimer> dueTimers = null, long? tickCeiling = null)`

:   Freezes the supplied timing views and due timers into ordered snapshots the scheduler cannot observe changing afterwards.

    - `currentTick` &mdash; The tick the scheduler is advancing from. It must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it.
    - `nextOpportunitySequence` &mdash; The first opportunity sequence this transition may assign. Allocate consecutively from it, one per ready opportunity produced, because the engine advances its own counter by exactly that many.
    - `dueTimers` &mdash; Engine-owned timers, none of which may be due before `currentTick`. Null means no timer is pending; entries must be non-null and unique.
    - `tickCeiling` &mdash; The highest tick the caller's advance request permits, or null when the caller set no ceiling.
    - `combatants` &mdash; Complete timing view of the battle roster; entries are copied and sorted by actor ID for deterministic traversal.

**Properties**

`public FrozenList<SchedulerCombatantTimingView> Combatants`

:   Every combatant in the battle, including ineligible ones, sorted by actor ID.

`public long CurrentTick`

:   The tick the schedule is advancing from. It must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it; a mismatch is rejected rather than reconciled.

`public FrozenList<SchedulerDueTimer> DueTimers`

:   Engine-owned timers the scheduler must stop at, ordered by due tick and then by the tie precedence of `SchedulerDueTimerKind`. Empty when nothing is pending.

`public SchedulerDueTimer EarliestDueTimer`

:   The first entry of `DueTimers`, or null when nothing is pending. Because that list is ordered by due tick and then by kind, this is the engine-owned boundary an advance has to stop at.

`public long? ExternalDueTick`

:   Due tick of `EarliestDueTimer`, or null when no timer is pending. A scheduler must not advance the clock beyond it.

`public ulong NextOpportunitySequence`

:   The first opportunity sequence this transition may assign. Sequences are allocated consecutively from here, one per ready opportunity returned.

`public long? TickCeiling`

:   The highest tick the caller's advance request permits, or null when the caller set no ceiling. Stopping here reports `SchedulerAdvanceStopReason.ReachedTickCeiling` and emits no event.

---

## SchedulerAdvanceResult

```csharp
public sealed class SchedulerAdvanceResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Outcome of `IBattleScheduler.Advance`: the next scheduler state,
the ordered work for the engine to translate, and why the transition stopped.
A failure carries only the diagnostic - no state and no work - so a rejected
advance can never leave the battle partly advanced.

**Properties**

`public Diagnostic? Diagnostic`

:   The failure detail, or null when the advance succeeded.

`public SchedulerState State`

:   The state after the advance, or null when it failed.

`public SchedulerAdvanceStopReason StopReason`

:   Why the advance stopped. It is meaningful only when `Succeeded` is true.

`public bool Succeeded`

:   Whether the advance was accepted. When false the engine keeps its last valid snapshot and neither `State` nor `Work` is populated, so a rejected advance leaves the clock exactly where it was.

`public FrozenList<SchedulerWork> Work`

:   The work the engine should translate, in the order it must be applied; null when the advance failed.

**Methods**

`public static SchedulerAdvanceResult Failure(Diagnostic diagnostic)`

:   Reports that the advance was rejected. The engine raises the diagnostic and keeps its last valid snapshot, so the input state is never partly advanced.

    - `diagnostic` &mdash; Machine-readable reason the requested scheduler advance was rejected without producing state or work.
    - **Returns** &mdash; A failed advance result carrying only the supplied diagnostic, so callers cannot consume partial state.

`public static SchedulerAdvanceResult Success(SchedulerState state, IEnumerable<SchedulerWork> work, SchedulerAdvanceStopReason stopReason)`

:   Reports a completed advance and freezes the work into an immutable list, so a later change to the caller's collection cannot reach the engine.

    - `state` &mdash; The state after the advance. Required.
    - `work` &mdash; The work records in application order. Required, entries must be non-null, and the count may not exceed `SimulationLimits.ExecutionFrames`.
    - `stopReason` &mdash; Why the advance stopped; must be a defined value.
    - **Returns** &mdash; A successful advance result with the required next state, an immutable ordered work list, and its validated stop reason.

---

## SchedulerAdvanceStopReason

```csharp
public enum SchedulerAdvanceStopReason : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Why `IBattleScheduler.Advance` stopped. The engine turns this
into caller control flow, so the value decides whether stepping continues,
returns to the caller, or reports a stalled battle.

| Value | Meaning |
| --- | --- |
| `WorkProduced` | The scheduler reached its own next boundary and produced work. |
| `ReachedTickCeiling` | Stopped at the caller's tick ceiling, before the scheduler's own next boundary. |
| `ExternalBoundary` | Stopped at an engine-owned due timer rather than at readiness. |
| `AwaitingCommand` | A queued decision must be resolved before the scheduler can go further. |
| `NoScheduledWork` | Nothing is scheduled: no readiness, no due timer, and no ceiling to advance to. |

---

## SchedulerCombatantTimingView

```csharp
public sealed class SchedulerCombatantTimingView
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Immutable per-actor timing input the engine builds for one scheduler
transition. It exposes only what turn order may depend on, so a scheduler
can neither read nor change authoritative battle state through it.

**Constructors**

`public SchedulerCombatantTimingView(StableId actorId, int effectiveSpeedRaw, DecisionControlKind controlKind, bool isEligible, bool isBusy, int initialAtbGaugeUnits = 0)`

:   Captures one actor's timing inputs. The constructor stores the values as given; the scheduler validates them when the transition runs.

    - `effectiveSpeedRaw` &mdash; Fixed-point speed where `SimulationLimits.EffectiveSpeedScale` (10,000) is normal speed.
    - `isEligible` &mdash; Whether the actor may receive a new opportunity at all.
    - `isBusy` &mdash; Whether the actor already holds an active action or cast.
    - `initialAtbGaugeUnits` &mdash; Gauge units the actor starts an ATB battle with. Action Order ignores the value.
    - `actorId` &mdash; Stable identifier of the combatant whose eligibility, speed, and busy state this view exposes.
    - `controlKind` &mdash; Whether a ready opportunity for this actor requires human input or automatic policy evaluation.

**Properties**

`public StableId ActorId`

:   The combatant this view describes, and the key every frozen timing collection is sorted by. It must be valid and appear only once per transition, or the call fails with `SchedulerDiagnosticIds.StateInvalid`.

`public DecisionControlKind ControlKind`

:   Who fills a decision handed to this actor. The value is copied onto the queued `DecisionEntry`, and the ATB scheduler reads it back alongside the definition's `InputPausePolicy` to decide whether the clock keeps running while that decision is outstanding.

`public int EffectiveSpeedRaw`

:   Fixed-point speed, where `SimulationLimits.EffectiveSpeedScale` (10,000) is normal speed. Action Order divides a recovery cost by it to get the next ready tick; ATB adds it to the gauge on every filling tick. It must be positive and at most `SimulationLimits.EffectiveSpeed`, and under ATB no greater than the gauge threshold, or the transition fails with `SchedulerDiagnosticIds.SpeedInvalid`.

`public int InitialAtbGaugeUnits`

:   Starting gauge units, read only when an ATB scheduler creates its state and required to be below the gauge threshold. Action Order ignores the value.

`public bool IsBusy`

:   Whether the actor already holds an active action or cast. A busy actor receives no new opportunity, and its ATB gauge does not fill.

`public bool IsEligible`

:   Whether the actor may receive a new opportunity: living, on a non-conceded team, and not otherwise prevented from acting. An ineligible actor never becomes ready, and Action Order counts it as resolved for the current round.

---

## SchedulerCreateContext

```csharp
public sealed class SchedulerCreateContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Immutable input to `IBattleScheduler.Create`: the compiled
definition to honour, the tick the state is created at, and one timing
view per combatant. The built-in schedulers accept only tick zero, so
creation happens at battle start and never mid-battle.

**Constructors**

`public SchedulerCreateContext(CompiledSchedulerDefinition definition, long currentTick, IEnumerable<SchedulerCombatantTimingView> combatants)`

:   Freezes the supplied timing views into an actor-ID-ordered snapshot, so later changes to the caller's collection cannot reach the scheduler.

    - `currentTick` &mdash; Tick the scheduler state is created at; the built-in schedulers accept only zero.
    - `combatants` &mdash; Every combatant in the battle, eligible or not. Required, and entries must be non-null.
    - `definition` &mdash; Compiled scheduler settings used to create the initial state; the selected scheduler validates that its tag and contract version match.

**Properties**

`public FrozenList<SchedulerCombatantTimingView> Combatants`

:   Every combatant in the battle, including ineligible ones, sorted by actor ID.

`public long CurrentTick`

:   Tick the state is created at. The built-in schedulers accept only zero, so the schedule is always laid out before the clock has moved.

`public CompiledSchedulerDefinition Definition`

:   The compiled settings the new state must honour: the recovery an actor owes when its opportunity produces no action and, for ATB, the gauge threshold and input-pause policy.

---

## SchedulerCreateResult

```csharp
public sealed class SchedulerCreateResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Outcome of `IBattleScheduler.Create`. Success carries the initial
`SchedulerState` and no diagnostic; failure carries the diagnostic
and no state, and the engine refuses to start the battle.

**Properties**

`public Diagnostic? Diagnostic`

:   The failure detail, or null when creation succeeded.

`public SchedulerState State`

:   The initial scheduler state, or null when creation failed.

`public bool Succeeded`

:   Whether a state was produced. When false the battle does not start, so check it before reading `State`.

**Methods**

`public static SchedulerCreateResult Failure(Diagnostic diagnostic)`

:   Reports that no state could be created. Prefer an ID from `SchedulerDiagnosticIds` so tooling classifies the failure.

    - `diagnostic` &mdash; Machine-readable reason scheduler state creation could not satisfy its contract.
    - **Returns** &mdash; A failed creation result containing no scheduler state and preserving the supplied diagnostic.

`public static SchedulerCreateResult Success(SchedulerState state)`

:   Reports a created scheduler state.

    - `state` &mdash; The initial state. Required.
    - **Returns** &mdash; A successful creation result containing the required initial state and no diagnostic.

---

## SchedulerDiagnosticIds

```csharp
public static class SchedulerDiagnosticIds
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

The stable diagnostic IDs the registry and the built-in schedulers report.
The string values are part of the published contract, so tests and tooling can
match on them; a custom scheduler should reuse these rather than invent
parallel IDs for the same failures.

**Fields**

`public static readonly StableId AtbGaugeInvalid`

:   Failure code when an actor's ATB gauge is negative, reaches an impossible value, or is not below the threshold at initialization.

`public static readonly StableId AtbThresholdInvalid`

:   Failure code for a non-positive ATB readiness threshold or one above the simulation gauge limit.

`public static readonly StableId DefinitionInvalid`

:   Failure code for scheduler definitions whose state tag, contract version, ranges, or ATB-only fields violate the selected implementation.

`public static readonly StableId NoEligibleCombatants`

:   Failure code when scheduler creation or transition finds no combatant that can ever receive an opportunity.

`public static readonly StableId OpportunityOverflow`

:   Failure code when allocating one or more opportunity sequences would wrap the unsigned sequence counter.

`public static readonly StableId ReadyQueueLimit`

:   Failure code when scheduler output would exceed the bounded ready-decision queue.

`public static readonly StableId RegistryMissing`

:   No scheduler is registered under the requested ID, whatever its version.

`public static readonly StableId RoundOverflow`

:   Failure code when opening the next Action Order round would wrap its unsigned round index.

`public static readonly StableId SpeedInvalid`

:   Failure code for a combatant speed outside deterministic bounds or incompatible with the configured ATB threshold.

`public static readonly StableId StateInvalid`

:   Failure code for malformed scheduler state, mismatched current ticks, duplicate actors, or inconsistent decision queues.

`public static readonly StableId TickOverflow`

:   Failure code when advancing, scaling recovery, or computing a due tick would exceed the signed tick range.

`public static readonly StableId VersionUnsupported`

:   The requested scheduler ID is registered, but not at the requested contract version.

---

## SchedulerDueTimer

```csharp
public sealed class SchedulerDueTimer
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

One engine-owned boundary the scheduler must stop at. The identity fields
exist so the engine can pair the boundary back to its own record; a
scheduler normally needs only `DueTick` and `Kind`.

**Constructors**

`public SchedulerDueTimer(SchedulerDueTimerKind kind, long dueTick, StableId ownerId, StableId timerId, ulong applicationSequence = 0UL)`

:   Describes one due timer, rejecting a kind and identity combination the engine could not pair back to a record.

    - `dueTick` &mdash; Tick the timer comes due on; may not be negative.
    - `ownerId` &mdash; Combatant that owns the timer. Required.
    - `timerId` &mdash; Skill ID for a cast or cooldown timer, status definition ID for a status boundary. Required.
    - `applicationSequence` &mdash; Which application of a status the boundary belongs to. It must be non-zero for `SchedulerDueTimerKind.ElapsedStatusBoundary` and zero for every other kind.
    - `kind` &mdash; Engine boundary category, which also establishes tie precedence for timers sharing a due tick.

**Properties**

`public ulong ApplicationSequence`

:   Which application of a status this boundary belongs to; zero for cast and cooldown timers.

`public long DueTick`

:   Tick the timer comes due on, never negative. It is the primary ordering key of `SchedulerAdvanceContext.DueTimers`.

`public SchedulerDueTimerKind Kind`

:   Which engine-owned boundary this is. It also settles the order when several timers come due on the same tick.

`public StableId OwnerId`

:   The combatant whose cast, cooldown, or status the timer belongs to. It is part of how the engine pairs the boundary back to its own record, rather than something a scheduler is expected to act on.

`public StableId TimerId`

:   Skill ID for a cast or cooldown timer, status definition ID for a status boundary.

---

## SchedulerDueTimerKind

```csharp
public enum SchedulerDueTimerKind : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

The engine-owned timer categories a scheduler must not advance past. When
several fall on the same tick they are ordered cast completion first, then
elapsed status boundary, then elapsed cooldown expiry.

| Value | Meaning |
| --- | --- |
| `CastCompletion` | An active cast reaches its end tick. |
| `ElapsedCooldownExpiry` | An elapsed-tick cooldown reaches its due tick. |
| `ElapsedStatusBoundary` | A status application reaches its next elapsed-tick boundary, whichever of its periodic tick or its expiry comes first. |

---

## SchedulerOpportunityContext

```csharp
public sealed class SchedulerOpportunityContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Immutable input to `IBattleScheduler.OnOpportunityAccepted`,
naming the queued decision the engine is about to consume. The sequence and
actor must identify the head of the decision queue; anything else is a
state-invalid failure.

**Constructors**

`public SchedulerOpportunityContext(long currentTick, ulong opportunitySequence, StableId actorId, IEnumerable<SchedulerCombatantTimingView> combatants)`

:   Names the decision being consumed and freezes the timing views into an actor-ID-ordered snapshot.

    - `currentTick` &mdash; The current tick, which must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it.
    - `opportunitySequence` &mdash; Sequence of the decision being consumed. It must match the queue head and may not be zero.
    - `actorId` &mdash; Stable identifier on the decision-queue head being accepted.
    - `combatants` &mdash; Current complete roster timing view, defensively copied and sorted by actor ID.

**Properties**

`public StableId ActorId`

:   The actor whose decision is being consumed. It must be the actor on the queue head named by `OpportunitySequence`, so the two together identify one decision rather than merely describing it.

`public FrozenList<SchedulerCombatantTimingView> Combatants`

:   Every combatant in the battle, including ineligible ones, sorted by actor ID.

`public long CurrentTick`

:   The tick the decision is consumed on. It must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it.

`public ulong OpportunitySequence`

:   Sequence of the decision being consumed, which must match the head of the decision queue.

---

## SchedulerOpportunityOutcome

```csharp
public enum SchedulerOpportunityOutcome : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

How an opportunity ended, as reported to
`IBattleScheduler.OnOpportunityFinished`. Recovery is charged
for all three outcomes, so no outcome lets an actor act again for free.

| Value | Meaning |
| --- | --- |
| `Completed` | The action resolved normally. |
| `Interrupted` | The action was interrupted before it resolved. |
| `Skipped` | The opportunity produced no action, because no command was legal or the actor was prevented from acting. |

---

## SchedulerOpportunityResult

```csharp
public sealed class SchedulerOpportunityResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Immutable report that one opportunity has finished, and the input to
`IBattleScheduler.OnOpportunityFinished`. This is where an
actor's next readiness is charged, so a scheduler that ignores it will hand
the same actor consecutive turns.

**Constructors**

`public SchedulerOpportunityResult(long currentTick, ulong opportunitySequence, StableId actorId, int recoveryTicks, SchedulerOpportunityOutcome outcome, IEnumerable<SchedulerCombatantTimingView> combatants)`

:   Reports a finished opportunity and freezes the timing views into an actor-ID-ordered snapshot.

    - `currentTick` &mdash; The tick the opportunity finished on, which must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it.
    - `opportunitySequence` &mdash; Sequence of the opportunity that finished; may not be zero.
    - `recoveryTicks` &mdash; Recovery the actor owes before it may act again. It must be positive and at most `SimulationLimits.TimingTicks`.
    - `actorId` &mdash; Stable identifier of the combatant whose opportunity finished and whose next readiness must be scheduled.
    - `combatants` &mdash; Current complete roster timing view used to validate the actor and, for Action Order, scale recovery by speed.
    - `outcome` &mdash; Completion, interruption, or skip classification recorded for the finished opportunity.

**Properties**

`public StableId ActorId`

:   The actor that finished acting, and whose next readiness this transition sets. Its timing view has to be present in `Combatants`, or the transition fails as state-invalid. Action Order additionally reads that view's effective speed to scale the recovery; ATB does not.

`public FrozenList<SchedulerCombatantTimingView> Combatants`

:   Every combatant in the battle, including ineligible ones, sorted by actor ID. Action Order reads the finishing actor's effective speed from here, so its recovery is scaled by the speed the actor holds now rather than the speed it had when the opportunity opened; ATB charges recovery as an absolute tick count and does not scale it.

`public long CurrentTick`

:   The tick the opportunity finished on, and the tick the actor's recovery is measured from. It must equal `SchedulerState.LastAdvancedTick` of the state passed alongside it.

`public ulong OpportunitySequence`

:   Sequence of the opportunity that finished, the same one `IBattleScheduler.OnOpportunityAccepted` was given when the decision was consumed. Never zero.

`public SchedulerOpportunityOutcome Outcome`

:   How the opportunity ended. It records what happened rather than whether the actor pays, since recovery is charged for all three outcomes.

`public int RecoveryTicks`

:   Recovery the actor owes before it may act again, always positive. Action Order turns it into the next ready tick with `currentTick + ceil(recoveryTicks * 10000 / effectiveSpeedRaw)`; ATB adds it to the current tick as an absolute recovery lock during which the gauge does not fill.

---

## SchedulerState

```csharp
public sealed class SchedulerState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

The authoritative scheduler half of a battle snapshot: the ordered decision
queue plus exactly one family payload chosen by `StateTag`.
Immutable, so reading it cannot advance the battle; every scheduler
transition returns a new instance instead of editing this one.

**Properties**

`public ActionOrderState ActionOrder`

:   The Action Order payload, or null under any other tag.

`public AtbState Atb`

:   The ATB payload, or null under any other tag.

`public FrozenList<DecisionEntry> DecisionEntries`

:   Actors waiting for a command, ordered by `(readyTick, actorId, opportunitySequence)`. An actor appears at most once, opportunity sequences are unique, and the count is capped by the ready-decision limit.

`public DecisionEntry HeadDecision`

:   The decision the engine serves next, or null when nothing is queued.

`public long LastAdvancedTick`

:   The tick this state has been advanced to. After a completed reduction it equals the snapshot tick, and a scheduler rejects any context whose current tick disagrees with it.

`public int SchedulerContractVersion`

:   The scheduler contract version this state was written under. It has to match the running scheduler, so raising it makes older saves fail to restore rather than be reinterpreted under new rules.

`public StableId SchedulerId`

:   The scheduler this state belongs to. Restoring a snapshot whose scheduler ID is not the one the compiled content names is refused, so a save cannot be replayed under a different turn order.

`public SchedulerStateTag StateTag`

:   Which payload this state carries. It selects exactly one of `ActionOrder` and `Atb`; the other is null.

**Methods**

`public SchedulerState ClearDecisions()`

:   Drops every queued decision, keeping the tick and the payload. The engine uses this when a battle ends with decisions still pending.

    - **Returns** &mdash; A state with an empty queue, or this same instance when the queue was already empty.

`public static SchedulerState CreateActionOrder(StableId schedulerId, int schedulerContractVersion, long lastAdvancedTick, IEnumerable<DecisionEntry> decisionEntries, ActionOrderState actionOrder)`

:   Builds an Action Order state. The tag and payload must agree, so `actionOrder` is required; its round may not have begun after `lastAdvancedTick`, and no actor may be both ready and queued.

    - `decisionEntries` &mdash; The queue to sort into service order. Actors and opportunity sequences must be unique, and the count may not exceed the ready-decision limit.
    - `actionOrder` &mdash; Required Action Order payload whose current round cannot start after the state tick.
    - `lastAdvancedTick` &mdash; Non-negative battle tick through which this scheduler state has already been reduced.
    - `schedulerContractVersion` &mdash; Positive compatibility version required when resolving the scheduler that owns the state.
    - `schedulerId` &mdash; Valid registry identifier of the scheduler implementation that produced the state.
    - **Returns** &mdash; A new immutable state tagged as Action Order with its decisions sorted into service order; inconsistent payloads throw.

`public static SchedulerState CreateAtb(StableId schedulerId, int schedulerContractVersion, long lastAdvancedTick, IEnumerable<DecisionEntry> decisionEntries, AtbState atb)`

:   Builds an ATB state. The tag and payload must agree, so `atb` is required.

    - `decisionEntries` &mdash; The queue to sort into service order. Actors and opportunity sequences must be unique, and the count may not exceed the ready-decision limit.
    - `atb` &mdash; Required gauge payload carrying the readiness threshold, pause policy, and actor entries.
    - `lastAdvancedTick` &mdash; Non-negative battle tick through which this scheduler state has already been reduced.
    - `schedulerContractVersion` &mdash; Positive compatibility version required when resolving the scheduler that owns the state.
    - `schedulerId` &mdash; Valid registry identifier of the ATB scheduler implementation that produced the state.
    - **Returns** &mdash; A new immutable state tagged as ATB with its decisions sorted into service order; null or inconsistent payloads throw.

`public SchedulerState RemoveHeadDecision(ulong opportunitySequence, StableId actorId)`

:   Removes the head decision, which must be the one identified by both `opportunitySequence` and `actorId`. Decisions behind the head are never removed out of order.

    - `actorId` &mdash; Combatant identifier that must match the actor on the current queue head.
    - `opportunitySequence` &mdash; Non-zero opportunity identity that must match the current queue head.
    - **Returns** &mdash; The state without that decision, or `null` when the queue is empty or its head is a different decision. The built-in schedulers turn that null into an invalid-state diagnostic rather than throwing.

`public bool TryFindDecision(StableId actorId, out DecisionEntry decision)`

:   Finds the queued decision belonging to `actorId`.

    - `actorId` &mdash; Combatant identifier to locate in the unique-actor decision queue.
    - `decision` &mdash; Receives the actor's queued entry on success, or null when no entry belongs to that actor.
    - **Returns** &mdash; True when the actor is queued, in which case `decision` receives its single entry.

---

## SchedulerStateDecodeResult

```csharp
public sealed class SchedulerStateDecodeResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerStateCodec.cs</small>

The outcome of rebuilding a `SchedulerState` from payload
bytes: either the state, or the diagnostic saying it could not be read.

Decoding reports a failure rather than throwing, because payload bytes are
untrusted input: a truncated, oversized, foreign, or tampered save turns
into a rejected load the caller can handle, not an exception out of the
middle of a restore.

**Properties**

`public Diagnostic? Diagnostic`

:   Why the payload was refused, or null on success. Every failure reports the same invalid-state ID rather than describing where reading broke down, so it says a save cannot be trusted, not how it was malformed.

`public SchedulerState State`

:   The decoded state, or null on failure. A state returned here has already been accepted by the codec that decoded it, so it is safe to hand back to that scheduler.

`public bool Succeeded`

:   Whether the payload was read. It is the only flag worth branching on: `State` and `Diagnostic` are populated according to it, one or the other but never both.

**Methods**

`public static SchedulerStateDecodeResult Failure()`

:   Reports that a payload could not be read. Custom codecs should return this for anything they do not recognise instead of throwing, so an unreadable save is refused rather than crashing the load.

    - **Returns** &mdash; A failed result with no state, carrying the invalid-state diagnostic.

`public static SchedulerStateDecodeResult Success(SchedulerState state)`

:   Reports a decoded state.

    - `state` &mdash; The state that was read; required.
    - **Returns** &mdash; A successful result carrying no diagnostic.

---

## SchedulerStateTag

```csharp
public enum SchedulerStateTag : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

Discriminates which payload a `SchedulerState` carries. Exactly
one of the Action Order or ATB payloads is populated, and it must match the
tag; a mismatched pair is rejected at construction.

| Value | Meaning |
| --- | --- |
| `ActionOrder` | Encodes the action order branch of scheduler state tag. |
| `Atb` | Encodes the ATB branch of scheduler state tag. |

---

## SchedulerTransitionResult

```csharp
public sealed class SchedulerTransitionResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

Outcome of an opportunity transition, either
`IBattleScheduler.OnOpportunityAccepted` or
`IBattleScheduler.OnOpportunityFinished`. It carries the next
state and any work the transition created. Unlike an advance, a failure here
is fatal: the engine raises the diagnostic rather than retrying, because the
opportunity has already been committed.

**Properties**

`public Diagnostic? Diagnostic`

:   The failure detail, or null when the transition succeeded.

`public SchedulerState State`

:   The state after the transition, or null when it failed.

`public bool Succeeded`

:   Whether the transition was accepted. A false value is fatal rather than recoverable: the opportunity has already been committed, so the engine raises the diagnostic instead of retrying or backing out.

`public FrozenList<SchedulerWork> Work`

:   The work the engine should translate, in the order it must be applied; null when the transition failed.

**Methods**

`public static SchedulerTransitionResult Failure(Diagnostic diagnostic)`

:   Reports that the transition was rejected. The engine treats this as fatal and raises the diagnostic.

    - `diagnostic` &mdash; Machine-readable reason an accepted or finished opportunity could not transition the scheduler state.
    - **Returns** &mdash; A failed transition containing neither state nor work; the engine treats this committed-opportunity failure as fatal.

`public static SchedulerTransitionResult Success(SchedulerState state, IEnumerable<SchedulerWork> work)`

:   Reports a completed transition and freezes the work into an immutable list. When nothing changed, the built-in schedulers return a single no-work record rather than an empty list.

    - `state` &mdash; The state after the transition. Required.
    - `work` &mdash; The work records in application order. Required, entries must be non-null, and the count may not exceed `SimulationLimits.ExecutionFrames`.
    - **Returns** &mdash; A successful opportunity transition with the required next state and a frozen application-ordered work sequence.

---

## SchedulerWork

```csharp
public sealed class SchedulerWork
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

One ordered unit of scheduler output: a closed union whose payload the engine
copies into execution frames. Only the members belonging to
`Tag` carry meaning, and instances exist only through the static
factories, so an ill-formed record cannot be built.

**Properties**

`public DecisionEntry Decision`

:   The queued decision that became ready, set only for `SchedulerWorkTag.ReadyOpportunity`; null otherwise.

`public long FromTick`

:   Tick the clock moves from, set only for `SchedulerWorkTag.AdvanceTimers`.

`public SchedulerAdvanceStopReason NoWorkReason`

:   Why nothing happened, meaningful only for `SchedulerWorkTag.NoWork`.

`public RoundState Round`

:   Participant snapshot of the round that started or completed; null for every other tag.

`public ulong RoundIndex`

:   Index of the round that started or completed, set only for the two round tags.

`public SchedulerWorkTag Tag`

:   Which kind of record this is, and therefore which of the payload members below carry meaning. The others hold their default - zero or null - so reading one that does not belong to the tag is silently uninformative rather than an error.

`public long ToTick`

:   Tick the clock moves to, set only for `SchedulerWorkTag.AdvanceTimers` and always later than `FromTick`.

**Methods**

`public static SchedulerWork AdvanceTimers(long fromTick, long toTick)`

:   Reports that the battle clock moves forward with no scheduler boundary in between. The engine applies the whole delta at once, which is how a scheduler jumps over empty ticks without changing the outcome.

    - `fromTick` &mdash; Tick the clock leaves; may not be negative.
    - `toTick` &mdash; Tick the clock reaches, which must be strictly later than `fromTick`.
    - **Returns** &mdash; A timer-advance work record carrying the strictly increasing half-open tick movement; invalid bounds throw.

`public static SchedulerWork CompleteRound(ulong roundIndex, RoundState round)`

:   Reports that the round with this index finished. The engine emits the round-completed frame before any work that can expose new readiness.

    - `round` &mdash; Participants of the round that completed. Required.
    - `roundIndex` &mdash; Non-zero deterministic sequence of the round whose participant snapshot has completed.
    - **Returns** &mdash; A work record tagged `SchedulerWorkTag.CompleteRound` and retaining the required round snapshot.

`public static SchedulerWork NoWork(SchedulerAdvanceStopReason reason)`

:   Reports that the transition produced nothing, and why. Returning this rather than an empty work list is what lets the engine distinguish a paused battle from a stalled one.

    - `reason` &mdash; Why no work happened. `SchedulerAdvanceStopReason.WorkProduced` is rejected, since it contradicts the record.
    - **Returns** &mdash; A no-work record carrying the specified non-work stop reason; `SchedulerAdvanceStopReason.WorkProduced` is rejected.

`public static SchedulerWork ReadyOpportunity(DecisionEntry decision)`

:   Reports that an actor is ready to act and that its decision has been queued. The engine consumes one opportunity sequence per record of this kind, so return exactly one for each sequence allocated.

    - `decision` &mdash; The queued decision, carrying its opportunity sequence, ready tick, actor, and control kind. Required.
    - **Returns** &mdash; A work record tagged `SchedulerWorkTag.ReadyOpportunity` and owning the supplied non-null decision reference.

`public static SchedulerWork StartRound(ulong roundIndex, RoundState round)`

:   Reports that a round began. The engine translates it into a round-started frame using the participant snapshot.

    - `round` &mdash; Participants of the round that started. Required.
    - `roundIndex` &mdash; Non-zero deterministic sequence of the round whose participant snapshot is opening.
    - **Returns** &mdash; A work record tagged `SchedulerWorkTag.StartRound` and retaining the required round snapshot.

---

## SchedulerWorkTag

```csharp
public enum SchedulerWorkTag : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/IBattleScheduler.cs</small>

The closed set of work a scheduler can return, and the tag that says which
payload of `SchedulerWork` is populated. The engine translates
each record into execution frames; a scheduler never emits events itself.

| Value | Meaning |
| --- | --- |
| `StartRound` | A round began, carrying its index and participant snapshot. |
| `CompleteRound` | The round identified by the index finished. |
| `ReadyOpportunity` | An actor became ready, carrying the queued decision. |
| `AdvanceTimers` | The clock moves from one tick to a later one with no scheduler boundary in between. |
| `NoWork` | Nothing happened; the no-work reason says why. |

---

## TimingResolutionKind

```csharp
public enum TimingResolutionKind : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

Timing-layer work a skill performs as it resolves, on top of its own
effects. `InterruptFirstLockedCast` interrupts the interruptible cast
of its single locked target; a skill that declares it must have zero cast
ticks and require exactly one target, which
`CompiledSkillTiming` enforces at construction.

| Value | Meaning |
| --- | --- |
| `None` | Chooses none semantics for timing resolution kind. |
| `InterruptFirstLockedCast` | Chooses interrupt first locked cast semantics for timing resolution kind. |

---
