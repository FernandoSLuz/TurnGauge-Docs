# Commands, events and snapshots

18 types in this area.

!!! abstract "On this page"
    [ActionCostState](#actioncoststate) &middot; [ActiveActionState](#activeactionstate) &middot; [ActiveCastState](#activecaststate) &middot; [BattleCommand](#battlecommand) &middot; [BattleEvent](#battleevent) &middot; [BattleIds](#battleids) &middot; [BattleSnapshot](#battlesnapshot) &middot; [CombatantState](#combatantstate) &middot; [CooldownState](#cooldownstate) &middot; [DecisionControlKind](#decisioncontrolkind) &middot; [DecisionEntry](#decisionentry) &middot; [PropertyEntry](#propertyentry) &middot; [PropertySet](#propertyset) &middot; [ResourceState](#resourcestate) &middot; [StartTeam](#startteam) &middot; [TaggedValue](#taggedvalue) &middot; [TaggedValueTag](#taggedvaluetag) &middot; [TeamState](#teamstate)

## ActionCostState

```csharp
public sealed class ActionCostState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

One line of an action's resource ledger: how much of one resource was paid, or refunded.
Zero-amount entries do not exist - a cost that was not charged is simply absent.

**Constructors**

`public ActionCostState(StableId resourceId, int amount)`

:   Creates a cost entry. Throws when `resourceId` is invalid or when `amount` is not positive.

    - `amount` &mdash; The strictly positive quantity paid or refunded on this ledger line.
    - `resourceId` &mdash; The required resource-pool identity charged by this line.

**Properties**

`public int Amount`

:   How much of the resource the line covers, always positive. On a refund line it is the amount handed back, which can be smaller than the amount originally paid when the pool has refilled in the meantime.

`public StableId ResourceId`

:   The pool this line charges against, matching a `ResourceState.ResourceId` owned by the acting combatant.

---

## ActiveActionState

```csharp
public sealed class ActiveActionState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

One action that has been accepted and has not finished resolving: its actor, skill, locked
targets, cost ledger, and cast window. A snapshot carries at most one of these per actor, so
this doubles as the answer to "what is that combatant doing right now".

**Constructors**

`public ActiveActionState(ulong rootActionSequence, ulong opportunitySequence, StableId actorId, StableId skillId, long acceptedTick, IEnumerable<StableId> lockedTargetIds, TimingResolutionKind timingResolutionKind, IEnumerable<ActionCostState> paidCosts, InterruptRefundPolicy interruptRefundPolicy, IEnumerable<ActionCostState> refundedCosts, bool queueCooldownStarted, ActiveCastState cast)`

:   Creates an active action, normalising the three collections into a canonical order: locked targets ascending, cost ledgers sorted by resource. Throws when the identity values are zero or invalid, when either enumerable is null, when locked targets are duplicated or exceed the per-command limit, when costs are duplicated or exceed the per-skill limit, or when a refund is not covered by the matching paid cost.

    - `rootActionSequence` &mdash; The sequence of the root action this belongs to; the value the snapshot orders its active actions by.
    - `opportunitySequence` &mdash; The decision opportunity this action was accepted against. Unique across a snapshot's active actions.
    - `acceptedTick` &mdash; The tick the action was accepted on, never later than the snapshot's own tick.
    - `lockedTargetIds` &mdash; Targets frozen at acceptance. Order is not preserved: the list is sorted ascending and must contain no duplicates or invalid IDs.
    - `paidCosts` &mdash; Resources already charged to the actor.
    - `refundedCosts` &mdash; Resources given back after an interrupt. Each entry must name a resource in `paidCosts` and may not exceed the amount paid.
    - `queueCooldownStarted` &mdash; Whether this action's cooldown was started at queue time rather than on completion, which decides whether completion starts it again.
    - `cast` &mdash; The cast window, or `null` for an action with no cast phase.
    - `actorId` &mdash; The required combatant identity that owns this in-flight action.
    - `interruptRefundPolicy` &mdash; Whether interruption refunds none or all of each paid resource cost.
    - `skillId` &mdash; The required compiled skill identity captured at acceptance.
    - `timingResolutionKind` &mdash; No timing interrupt, or interruption of the first locked target's cast; other values are rejected.

**Properties**

`public long AcceptedTick`

:   The tick the action was accepted on, which is not the tick it resolves on.

`public StableId ActorId`

:   The combatant performing the action. A snapshot holds at most one active action per actor, which is what makes `BattleSnapshot.FindActiveAction` unambiguous.

`public ActiveCastState Cast`

:   The cast window, or `null` when the skill has no cast phase or the cast has already resolved.

`public InterruptRefundPolicy InterruptRefundPolicy`

:   What becomes of `PaidCosts` if this cast is interrupted: `None` leaves them spent, `Full` returns them through `RefundedCosts`, each amount clamped to the room left in its pool. Fixed at acceptance from the skill's compiled timing, so a refund cannot be turned on partway through a cast.

`public FrozenList<StableId> LockedTargetIds`

:   Targets frozen at acceptance, sorted ascending rather than in the order they were requested. Empty for an action that targets nothing.

`public ulong OpportunitySequence`

:   The scheduler decision opportunity this action was accepted against, unique among a snapshot's active actions.

`public FrozenList<ActionCostState> PaidCosts`

:   Resources already charged to the actor for this action, sorted by resource ID.

`public bool QueueCooldownStarted`

:   Whether this action's cooldown already started when the action was queued, rather than waiting for completion.

`public FrozenList<ActionCostState> RefundedCosts`

:   Resources returned after an interrupt, sorted by resource ID and bounded by `PaidCosts`. Empty until something refunds.

`public ulong RootActionSequence`

:   The root action this belongs to. It orders `BattleSnapshot.ActiveActions`, and it is the value that ties emitted events, cooldowns, and reaction budgets back to the action that caused them.

`public StableId SkillId`

:   The skill being used. Its compiled timing is what supplied the cast window, the cost ledger, and the two policies recorded on this instance, all captured at acceptance rather than re-read as the action resolves.

`public TimingResolutionKind TimingResolutionKind`

:   Timing-layer work this action performs as it resolves, on top of its own effects. The only such work the built-in timing layer offers is interrupting the cast of the single locked target; `None` means the action resolves with no timing-layer side effect.

---

## ActiveCastState

```csharp
public sealed class ActiveCastState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

The cast window of an in-flight action. While the action is active the battle tick sits inside
`StartTick`..`EndTick`, and the action resolves on the tick that
reaches `EndTick`.

**Constructors**

`public ActiveCastState(long startTick, long endTick, bool interruptible)`

:   Creates a cast window. Throws when `startTick` is negative, when `endTick` is not strictly after it, or when the span exceeds the timing-tick limit.

    - `endTick` &mdash; The tick the cast completes on. The span `endTick - startTick` equals the skill's authored cast ticks.
    - `interruptible` &mdash; Whether another combatant's timing resolution may cancel this cast. Mirrors the skill's authored flag; the engine never flips it mid-cast.
    - `startTick` &mdash; The non-negative acceptance tick; `endTick` must follow it within the timing limit.

**Properties**

`public long EndTick`

:   The tick the cast completes on. The action's `ActiveActionState.Cast` stays non-null until the battle tick reaches this value; on that tick the cast completes and that property is cleared, while the action itself stays in `BattleSnapshot.ActiveActions` past this tick - through resolution and recovery - until its opportunity is finalised, so test `Cast` rather than list membership to ask whether a combatant is still casting. A cast interrupted before this tick never resolves its effects at all.

`public bool Interruptible`

:   Whether another combatant's timing resolution may cancel this cast. Copied from the skill's authored timing when the action was accepted and never changed while the cast runs, so a cast cannot be made vulnerable after the fact.

`public long StartTick`

:   The tick the cast began on, which is the tick the command was accepted.

---

## BattleCommand

**Start here**

```csharp
public sealed class BattleCommand
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleCommand.cs</small>

One immutable decision handed to a battle: which combatant acts, on which
tick, under which command type, and against what. Commands are the only way
outside input reaches the simulation, and both accepted and rejected ones
are recorded, so a replay is rebuilt from the start request, the seed, and
this history alone.

The constructor checks shape only. Legality is the engine's answer, and it
depends on state this object cannot see: a command is accepted only while
its actor owns the exposed decision, and only while
`CommandSequence` and `RequestedTick` still match
what the engine is waiting for. Build the command at the moment you submit
it rather than holding one across ticks.

**Constructors**

`public BattleCommand(ulong commandSequence, long requestedTick, StableId commandTypeId, StableId actorId, StableId? skillId, IEnumerable<StableId> requestedTargetIds, PropertySet properties)`

:   Captures one exact command sequence, requested tick, actor, optional skill, targets, and properties. Invalid IDs, negative ticks, or oversized targets throw before submission.

    - `commandSequence` &mdash; Position in the battle's command history, which must equal the engine's next expected number. It is supplied rather than assigned so that a command built against a stale view of the battle is rejected outright instead of being applied out of order.
    - `requestedTick` &mdash; Tick the caller believes the battle is on. The engine rejects the command when it has already moved past it, rather than acting on a decision made against a battle that no longer looks that way.
    - `commandTypeId` &mdash; Which kind of command this is, such as `BattleIds.ConcedeCommand` or `BattleIds.UseSkillCommand`. It must be a type the compiled content registers.
    - `actorId` &mdash; The combatant this command acts for.
    - `skillId` &mdash; Skill to use, or null for a command type that takes none. A concede carrying one is malformed, and a use-skill missing one is too.
    - `requestedTargetIds` &mdash; Targets the caller chose, kept in the order given; that order is part of the command's identity and survives hashing and replay unchanged. An empty sequence leaves the choice to the skill's target resolver, where its contract allows that.
    - `properties` &mdash; Extra tagged values travelling with the command. The engine accepts no command type beyond the two built-in ones, and both require this to be empty, so pass `PropertySet.Empty`; anything else is rejected as malformed rather than handed to a custom handler.

**Properties**

`public StableId ActorId`

:   The combatant acting. It has to be the one whose decision the engine is currently exposing, and it has to be alive, targetable, and on a team that has not conceded.

`public ulong CommandSequence`

:   Where this command sits in the battle's command history. A mismatch against the engine's next expected number is refused before any rule is consulted, which is what makes a duplicated or reordered submission harmless.

`public StableId CommandTypeId`

:   Which kind of command this is. Compare it against the fields on `BattleIds` rather than rebuilding an id from a string literal.

`public PropertySet Properties`

:   Tagged values carried with the command, hashed into its identity and replayed verbatim. Empty for every built-in command type: a concede or use-skill command with any property set is rejected as malformed.

`public FrozenList<StableId> RequestedTargetIds`

:   Targets the caller asked for, in the order given rather than sorted. That order is preserved because it feeds the command hash a replay verifies against; the engine sorts the targets it ends up locking separately.

`public long RequestedTick`

:   The tick this command was decided on. It must equal the tick the battle is actually on; the engine does not queue a command for a future tick or backdate one to a tick already past.

`public StableId? SkillId`

:   The skill being used, or null when the command type takes none. It is checked against what the actor's definition grants, its cooldown, and its costs, so a valid id here is still no guarantee of acceptance.

**Methods**

`public static BattleCommand Concede(ulong sequence, long tick, StableId actorId)`

:   Builds a forfeit for one combatant, with no skill, no targets, and no properties, which is the exact shape the engine requires of a concede.

    - `sequence` &mdash; The engine's next expected command sequence number.
    - `tick` &mdash; The tick the battle is currently on.
    - `actorId` &mdash; The combatant conceding. Its whole team is marked as having conceded and the battle ends, so this forfeits the match rather than skipping a turn.
    - **Returns** &mdash; A concede command ready to submit.

---

## BattleEvent

**Start here**

```csharp
public sealed class BattleEvent
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleEvent.cs</small>

One immutable gameplay event emitted by the battle engine: what happened, on
which tick, in what order, and under which root action. An event carries plain
values rather than live authoring or engine objects, so it is safe to keep,
queue, or serialize after the battle has ended, and inspecting one can never
advance or alter the simulation.

The strict total order over a battle's events is `Tick` then
`EventSequence`; ticks never decrease, and the sequence breaks ties
among events sharing a tick. Every emitted event also folds into the snapshot's
event-chain hash, so a dropped or reordered event is detectable.

**Constructors**

`public BattleEvent(long tick, ulong eventSequence, ulong rootActionSequence, StableId eventTypeId, PropertySet properties)`

:   Creates an immutable event record. The engine emits these; callers normally read events rather than construct them.

    - `tick` &mdash; Authoritative tick at emission. Must not be negative.
    - `eventSequence` &mdash; Battle-wide emission order, starting at 1. Must not be 0.
    - `rootActionSequence` &mdash; The action sequence this event belongs to, or 0 for a battle or scheduler event that sits outside any root action.
    - `eventTypeId` &mdash; The event type, one of the `BattleIds` event identifiers. Must be valid.
    - `properties` &mdash; The event's ordered tagged values, keyed by the `BattleIds` property identifiers. Required. A tagged identifier array may not exceed the per-array limit, the sole exception being `round.started` participant IDs, which may hold up to the total combatant count.

**Properties**

`public ulong EventSequence`

:   Battle-wide emission order, starting at 1 and incrementing exactly once per emitted event. It is the tie-breaker when several events share a tick.

`public StableId EventTypeId`

:   The event type, matched against the `BattleIds` event identifiers.

`public PropertySet Properties`

:   The event's payload, keyed by the `BattleIds` property identifiers. Which keys are present depends on `EventTypeId`, so read them by attempting a lookup rather than assuming.

`public ulong RootActionSequence`

:   The root action this event belongs to, letting a caller group an action with everything it caused, reactions included. 0 for a battle or scheduler event that sits outside any action.

`public long Tick`

:   The authoritative tick this event was emitted on.

---

## BattleIds

**Start here**

```csharp
public static class BattleIds
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleEvent.cs</small>

The stable identifiers the battle simulation emits and reads: command types,
event types, the reason and outcome identifiers those events reference, and the
`...Property` keys used to look values up in a
`BattleEvent.Properties` set.

Compare against these fields rather than rebuilding a `StableId` from
a literal string. The string is the serialized identity, so a mistyped literal
compiles cleanly and then silently matches nothing at runtime.

**Fields**

`public static readonly StableId ActionCancelled`

:   The event type reporting an action cancelled under its invalid-target or interruption policy.

`public static readonly StableId ActionCompleted`

:   The event type closing a root action after all immediate effects and reactions resolve.

`public static readonly StableId ActionConceded`

:   The action result identifier used when its command concedes a team.

`public static readonly StableId ActionInterrupted`

:   The event type reporting a cast or action stopped before its effects completed.

`public static readonly StableId ActionNoLegalCommand`

:   The action result identifier used when no command satisfies the current legal-action set.

`public static readonly StableId ActionPrevented`

:   The action result identifier used when battle state prevents command execution.

`public static readonly StableId ActionResolved`

:   The action result identifier used after the requested action resolves normally.

`public static readonly StableId ActionSkipped`

:   The event type recording that a ready combatant produced no executable action.

`public static readonly StableId ActionStarted`

:   The event type opening a root action and its event-chain grouping.

`public static readonly StableId ActorIdProperty`

:   The event property key whose value names the combatant performing an action.

`public static readonly StableId ActualDeltaProperty`

:   The event property key containing the signed resource change actually committed.

`public static readonly StableId AdjustmentKindProperty`

:   The scheduler-event property key classifying how its timing value was adjusted.

`public static readonly StableId AmountProperty`

:   The event property key containing a resolved fixed-point damage, healing, shield, or timing amount.

`public static readonly StableId ApplicationSequenceProperty`

:   The status-event property key identifying one application instance across refreshes and ticks.

`public static readonly StableId AttributionHashProperty`

:   The event property key containing the canonical hash of formula inputs and intermediates.

`public static readonly StableId BattleConcession`

:   The battle outcome reason identifying a terminal result caused by concession.

`public static readonly StableId BattleDefeat`

:   The result identifier describing the losing side of a resolved team outcome.

`public static readonly StableId BattleDraw`

:   The result identifier for a terminal battle with no unique winning team.

`public static readonly StableId BattleEnded`

:   The terminal event type carrying the battle's authoritative result and outcome identifiers.

`public static readonly StableId BattleStalled`

:   The result identifier used when deterministic progress limits end the battle without victory.

`public static readonly StableId BattleStarted`

:   The event type emitted once after the initial battle snapshot is accepted.

`public static readonly StableId BattleVictory`

:   The result identifier for a battle with one authoritative winning team.

`public static readonly StableId BlockedByShieldProperty`

:   Boolean property marking a resolved amount that a shield absorbed in whole or in part. Optional in the same way as `CriticalProperty`.

`public static readonly StableId CastCompleted`

:   The event type emitted when a scheduled cast reaches its completion tick.

`public static readonly StableId CastEndTickProperty`

:   The event property key containing the scheduled inclusive completion tick of a cast.

`public static readonly StableId CastStartTickProperty`

:   The event property key containing the authoritative tick on which casting began.

`public static readonly StableId CastStarted`

:   The event type recording a timed skill's caster, target, and scheduled completion tick.

`public static readonly StableId CombatantDied`

:   The event type marking a combatant as dead after authoritative health resolution.

`public static readonly StableId CombatantReady`

:   The scheduler event announcing that a combatant may submit its next command.

`public static readonly StableId CommandAccepted`

:   The event type confirming that a submitted command passed validation and entered resolution.

`public static readonly StableId CommandRejected`

:   The event type reporting that a submitted command changed no battle state.

`public static readonly StableId CommandSequenceProperty`

:   The event property key containing the battle-wide sequence of the submitted command.

`public static readonly StableId CommandTypeIdProperty`

:   The event property key containing the stable command-type identity.

`public static readonly StableId ConcedeCommand`

:   The command type that asks the authoritative engine to concede the actor's team.

`public static readonly StableId CriticalProperty`

:   Boolean property marking a resolved hit as critical. It is optional and non-authoritative: an emitter that never writes it leaves every hit reading as ordinary, which is how the vocabulary behaved before the key existed. Presentation reads it to pick the critical floating-number style per hit instead of per skill.

`public static readonly StableId DamageResolved`

:   The event type carrying the final deterministic damage amount and attribution.

`public static readonly StableId EffectEntryIdProperty`

:   The event property key identifying the compiled effect entry currently resolving.

`public static readonly StableId EffectMissed`

:   The event type identifying an effect primitive that failed its hit or chance check.

`public static readonly StableId HealingResolved`

:   The event type carrying the actual health restored after bounds are applied.

`public static readonly StableId InterruptDeathReason`

:   The interruption reason used when the caster dies before resolution.

`public static readonly StableId InterruptTimingReason`

:   The interruption reason used when another timing action invalidates an in-progress action.

`public static readonly StableId KillingBlowProperty`

:   Boolean property marking the resolved amount that took its target out of the battle. Optional in the same way as `CriticalProperty`; the authoritative death is still `combatant.died`, and this only lets a visual react on the blow itself rather than one event later.

`public static readonly StableId LosingTeamIdProperty`

:   The terminal-event property key naming the defeated team.

`public static readonly StableId OutcomeIdProperty`

:   The event property key containing the stable reason or outcome classification.

`public static readonly StableId ParticipantIdsProperty`

:   The round-event property key containing participants in deterministic scheduler order.

`public static readonly StableId PreviousTargetIdProperty`

:   The retargeting-event property key naming the target replaced by policy.

`public static readonly StableId PrimitiveIndexProperty`

:   The event property key containing the zero-based primitive position within an effect entry.

`public static readonly StableId ReactionEnqueued`

:   The event type recording a reaction accepted into the deterministic reaction queue.

`public static readonly StableId ReactionRuleIdProperty`

:   The reaction-event property key naming the compiled rule that matched.

`public static readonly StableId ReactionSequenceProperty`

:   The reaction-event property key containing its deterministic enqueue sequence.

`public static readonly StableId ReactionSuppressed`

:   The event type explaining why an otherwise matching reaction was not enqueued or executed.

`public static readonly StableId ReactionTriggered`

:   The event type emitted when an enqueued reaction begins executing its effects.

`public static readonly StableId ReasonIdProperty`

:   The event property key containing a machine-readable rejection, cancellation, or suppression reason.

`public static readonly StableId RequestedDeltaProperty`

:   The event property key containing the signed resource change requested before clamping.

`public static readonly StableId ResourceChanged`

:   The event type carrying requested and actual deltas for a combatant resource.

`public static readonly StableId ResultIdProperty`

:   The event property key containing an action or battle result identifier.

`public static readonly StableId RoundCompleted`

:   The event type emitted after every scheduled participant in the round has resolved.

`public static readonly StableId RoundIndexProperty`

:   The round-event property key containing the current one-based round number.

`public static readonly StableId RoundStarted`

:   The round boundary event carrying its one-based index and ordered participant identities.

`public static readonly StableId SchedulerAdjusted`

:   The event type carrying a scheduler-specific timing delta for one combatant.

`public static readonly StableId SchedulerIdProperty`

:   The event property key naming the scheduler implementation responsible for timing.

`public static readonly StableId ShieldApplied`

:   The event type recording creation of a shield contribution and its initial amount.

`public static readonly StableId ShieldChanged`

:   The event type reporting a shield amount changed without removing the contribution.

`public static readonly StableId ShieldRemoved`

:   The event type reporting that a shield contribution reached removal conditions.

`public static readonly StableId SkillIdProperty`

:   The event property key naming the skill being cast or resolved.

`public static readonly StableId SourceIdProperty`

:   The event property key naming the combatant or status that originated an effect.

`public static readonly StableId StackDeltaProperty`

:   The status-event property key containing the signed stack-count change.

`public static readonly StableId StatusApplied`

:   The event type recording a new status instance and its application sequence.

`public static readonly StableId StatusIdProperty`

:   The event property key naming the compiled status definition involved.

`public static readonly StableId StatusImmune`

:   The event type emitted when target immunity prevents a status application outright.

`public static readonly StableId StatusRefreshed`

:   The event type reporting that an existing status duration or metadata was refreshed.

`public static readonly StableId StatusRemoved`

:   The event type reporting removal of a specific applied status instance.

`public static readonly StableId StatusResisted`

:   The event type emitted when a status application loses its deterministic resistance check.

`public static readonly StableId StatusStackChanged`

:   The event type carrying the signed change to an existing status stack count.

`public static readonly StableId StatusTick`

:   The periodic event type emitted before a status executes its scheduled effects.

`public static readonly StableId TargetIdProperty`

:   The event property key naming the current resolved target.

`public static readonly StableId TargetRetargeted`

:   The event type carrying both requested and replacement target identities.

`public static readonly StableId TeamConceded`

:   The event type recording which team accepted defeat through a concede command.

`public static readonly StableId TeamIdProperty`

:   The event property key naming the team implicated by an event.

`public static readonly StableId UseSkillCommand`

:   The command type that requests an actor, skill, and legal target selection.

`public static readonly StableId WinningTeamIdProperty`

:   The terminal-event property key naming the victorious team.

---

## BattleSnapshot

**Start here**

```csharp
public sealed class BattleSnapshot
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

Immutable snapshot of an entire battle at one tick: teams, combatants, resources, cooldowns,
statuses, in-flight actions, the pending work queue, and the outcome so far. Reading it cannot
advance or alter the battle - every step the engine takes produces a new instance while the
old one stays valid and safe to hold, which is what makes forecasting, replay verification,
and comparing two moments possible. It has no public constructor: snapshots come from a
`BattleEngine` or from decoding a canonical byte stream through
`CanonicalBattleSerializer`.

**Properties**

`public FrozenList<ActiveActionState> ActiveActions`

:   Actions accepted but not yet finished, at most one per actor, ordered by root action sequence.

`public FrozenList<CombatantState> Combatants`

:   Every combatant on both teams, living and dead, ordered by ID rather than by turn order. Use `FindCombatant` instead of assuming a position.

`public ulong CompletedRootActionCount`

:   How many root actions have finished resolving since the battle began. This is the counter the configured root-action limit is tested against.

`public Sha256Digest ContentManifestHash`

:   Hash of the compiled content this battle was created from. A replay or checkpoint whose manifest hash does not match is rejected rather than replayed against the wrong content.

`public FrozenList<CooldownState> Cooldowns`

:   Only the cooldowns still blocking; an expired cooldown is removed rather than kept at zero. Sorted and unique per owner-and-skill pair.

`public FrozenList<DecisionEntry> DecisionEntries`

:   The scheduler's queue of combatants awaiting a decision. Empty under profile 1 and whenever there is no scheduler state.

`public int EngineVersion`

:   The engine contract version, taken from `Profile`. Surfaced here so code holding only a snapshot can version-gate without reaching through the profile.

`public Sha256Digest EventChainHash`

:   Rolling hash chaining every event emitted so far. Two runs that diverge by a single event produce different chain hashes from that point on, which is how replay divergence is caught.

`public FrozenList<ExecutionFrame> Frames`

:   The engine's pending work queue, drained front to back: index 0 is what the next step reduces. An empty queue means the battle is terminal, is waiting on a command, or is about to advance the scheduler - it does not by itself mean the battle is over.

`public ulong LastEventSequence`

:   The sequence of the most recently emitted event, or 0 before the first event.

`public ulong NextActionSequence`

:   The sequence the next root action will be given. Cooldowns and active actions in this snapshot always reference a value below it.

`public ulong NextApplicationSequence`

:   The sequence the next status application will be given. Statuses and shields identify themselves by the application sequence they were created under.

`public ulong NextCommandSequence`

:   The sequence the next accepted command will be given. Every `Next...` counter on a snapshot names the value about to be handed out, not the last one used, and all start at 1.

`public ulong NextEventSequence`

:   The sequence the next emitted event will be given. See `LastEventSequence` for the event already emitted.

`public ulong NextOpportunitySequence`

:   The sequence the next decision opportunity will be given. Advances by one per combatant the scheduler makes ready.

`public ulong NextReactionSequence`

:   The sequence the next triggered reaction will be given. Never zero.

`public StableId? PendingDecisionActorId`

:   The combatant the engine is waiting on for a command - the head of `DecisionEntries` outside profile 1 - or `null` when nothing is awaiting input. A non-null value is the cue to present a decision UI.

`public FrozenList<ReplayCheckpoint> PeriodicCheckpoints`

:   State and event-chain hashes taken every 32 recorded commands. A replay checks its own hashes against these as it runs, so a divergence is reported at the checkpoint where it first appears instead of only once the battle has finished.

`public SimulationContractProfile Profile`

:   The contract profile the battle runs under: the matched set of engine, replay, canonical, and registry versions that decides which features exist at all. It selects the canonical encoding this snapshot is hashed and serialised through, and several of the collections below stay empty under the lower profiles, so check it before assuming stats, statuses, or a scheduler are present.

`public FrozenList<ReactionRootBudgetState> ReactionRoots`

:   Per-root-action reaction budgets: nesting depth, how many reactions the root has enqueued, and which once-per-root rules it has spent. Empty under profiles 1 and 2.

`public FrozenList<RecordedCommand> RecordedCommands`

:   Every command the battle has folded in, in submission order, accepted and rejected alike; this list is what a replay is written from. Rejections are kept because a replay has to reproduce them to stay in step - each one still consumes a command sequence and emits an event. Commands turned away before reduction, such as one submitted away from a decision boundary, never reach the battle and leave no entry. The history is capped at 4096 entries, beyond which further submissions fail rather than silently dropping.

`public Sha256Digest RegistryBindingHash`

:   Hash of the mechanics bindings the battle resolved against. Meaningful only under profile 3; default (invalid) otherwise.

`public FrozenList<ResourceState> Resources`

:   Every resource pool in the battle, sorted and unique per owner-and-resource pair. Empty under profile 1.

`public BattleResultState Result`

:   The battle's outcome as of this snapshot. Never `null`: it reads as nonterminal until the battle ends, so `BattleResultState.IsTerminal` is the condition a loop driving the engine stops on.

`public DeterministicRng Rng`

:   The deterministic random stream at its current position. Two battles given the same content, start request, seed, and commands walk this stream identically, which is what makes a replay reproduce byte for byte.

`public SchedulerState Scheduler`

:   Alias for `SchedulerState`. Kept for call sites that read it as `snapshot.Scheduler`.

`public StableId SchedulerId`

:   Which scheduler drives turn order - one of the built-in IDs, or one registered with a `BattleSchedulerRegistry`. It also picks the codec that reads, writes, and hashes `SchedulerState`, so a battle on a custom scheduler must be hashed and replayed through the registry that scheduler was registered in.

`public SchedulerState SchedulerState`

:   State owned by the scheduler driving turn order. `null` under profile 1, which has no scheduler.

`public FrozenList<ShieldState> Shields`

:   Shields with absorption left. Empty under profiles 1 and 2.

`public Sha256Digest StateHash`

:   The canonical state hash, recomputed on every read: the getter re-encodes the whole snapshot and hashes it, so cache the value rather than reading it in a loop. It assumes the built-in scheduler registry; a battle running a custom registered scheduler must be hashed through `CanonicalBattleSerializer.HashBattleState(BattleSnapshot, BattleSchedulerRegistry)` instead.

`public FrozenList<CombatantStatState> Stats`

:   Current stat values per combatant. Empty under profiles 1 and 2, which have no stats.

`public FrozenList<StatusInstanceState> Statuses`

:   Live status instances across all combatants. Empty under profiles 1 and 2.

`public FrozenList<SystemStatusActionState> SystemStatusActions`

:   Engine-owned actions an applied status has scheduled for a future tick. Empty under profiles 1 and 2.

`public FrozenList<TeamState> Teams`

:   The battle's teams - exactly two.

`public long Tick`

:   The simulation tick this snapshot sits on. Ticks are the engine's only unit of time - it knows nothing of seconds or frames - so the host decides how many to advance per frame and can pause, slow, or fast-forward a battle without changing anything that happens in it.

**Methods**

`public ActiveActionState FindActiveAction(StableId actorId)`

:   Looks up what a combatant is currently doing. A snapshot holds at most one active action per actor, so this result is unambiguous.

    - `actorId` &mdash; The exact combatant identity whose in-flight action is requested.
    - **Returns** &mdash; The actor's in-flight action, or `null` when it has none.

`public CombatantState FindCombatant(StableId id)`

:   Looks up a combatant by ID, living or dead. A linear scan over `Combatants`; hoist the result if you need it repeatedly in one frame.

    - `id` &mdash; The exact combatant identity to match during the linear scan.
    - **Returns** &mdash; The combatant, or `null` when no combatant has that ID.

`public CooldownState FindCooldown(StableId ownerId, StableId skillId)`

:   Looks up a live cooldown for one combatant's skill.

    - `ownerId` &mdash; The combatant whose cooldown to look for.
    - `skillId` &mdash; The exact skill identity paired with `ownerId`.
    - **Returns** &mdash; The cooldown, or `null` when the skill is not on cooldown - a null result is the way to test readiness, since expired cooldowns are dropped rather than zeroed.

`public ResourceState FindResource(StableId ownerId, StableId resourceId)`

:   Looks up one combatant's pool for one resource.

    - `ownerId` &mdash; The combatant that owns the pool.
    - `resourceId` &mdash; The exact resource identity paired with `ownerId`.
    - **Returns** &mdash; The pool, or `null` when that combatant has no pool for that resource.

`public TeamState FindTeam(StableId id)`

:   Looks up a team by ID.

    - `id` &mdash; The exact team identity to match during the linear scan.
    - **Returns** &mdash; The team, or `null` when no team has that ID.

---

## CombatantState

```csharp
public sealed class CombatantState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

Immutable per-combatant state held by a `BattleSnapshot`: identity, team,
health bounds, target eligibility, and formation placement. Nothing on a combatant can
be edited in place; the engine replaces the instance when any of it changes.

**Constructors**

`public CombatantState(StableId id, StableId teamId, int maximumHealth, int health, bool targetable)`

:   Creates a combatant with no compiled definition, human control, no AI policy, and no formation placement - the shape used by profiles 1 and 2. Throws when either ID is invalid, when `maximumHealth` is not positive, or when `health` falls outside 0..`maximumHealth`.

    - `health` &mdash; Current health. Zero is legal and means the combatant is dead.
    - `targetable` &mdash; Whether target resolution may select this combatant at all. A living combatant that is not targetable is still skipped as a source and a target.
    - `id` &mdash; The required battle-unique combatant identity.
    - `maximumHealth` &mdash; The positive immutable health ceiling for this battle.
    - `teamId` &mdash; The required identity of the team this combatant belongs to.

**Properties**

`public StableId? AiPolicyId`

:   The automatic policy that decides for this combatant, or `null` when it has none. Always `null` under profiles 1 and 2.

`public DecisionControlKind ControlKind`

:   Whether this combatant's decision opportunities wait for a command submitted from outside or are filled by an AI policy. Always `DecisionControlKind.Human` under profiles 1 and 2, which have no AI layer.

`public StableId DefinitionId`

:   The compiled combatant definition this instance was built from. Default (invalid) under profiles 1 and 2, which have no compiled combatant definitions.

`public StableId FormationRowId`

:   The row of the occupied formation slot, copied from the compiled layout.

`public StableId FormationSideId`

:   The side of the occupied formation slot, copied from the compiled layout.

`public StableId FormationSlotId`

:   The compiled formation slot this combatant occupies. Default (invalid) under profiles 1 and 2, as are `FormationRowId` and `FormationSideId`.

`public int Health`

:   Health remaining, between zero and `MaximumHealth`. Damage is clamped to the health actually left rather than going negative, so how far an attack overkilled is not recoverable from here.

`public StableId Id`

:   Stable identity of this CombatantState within battle state. Display labels and object references are resolved outside the simulation.

`public bool IsLiving`

:   Whether the combatant is still standing, which is health above zero. A dead combatant stays in `BattleSnapshot.Combatants` rather than being removed, so filter on this rather than on membership of that list.

`public int MaximumHealth`

:   The ceiling on `Health`, always positive and fixed for the whole battle: healing clamps here, and nothing the engine does raises or lowers the bound itself.

`public bool Targetable`

:   Whether target resolution is allowed to select this combatant. Independent of health: eligibility checks require both `Targetable` and `IsLiving`.

`public StableId TeamId`

:   The team this combatant fights for, matching one of the two `TeamState.Id` values. Target resolution reads it to decide who counts as an ally and who as an enemy.

---

## CooldownState

```csharp
public sealed class CooldownState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

One skill still on cooldown for one combatant. Presence is the whole signal: the engine drops
the entry as soon as the cooldown expires, so any entry in a snapshot is still blocking. A
snapshot holds at most one entry per owner-and-skill pair.

**Constructors**

`public CooldownState(StableId ownerId, StableId skillId, CooldownClockKind clockKind, int remainingElapsedTicks, int remainingOwnerOpportunities, ulong startedActionSequence)`

:   Creates a live cooldown. Exactly one of the two remaining counters is used, chosen by `clockKind`; the unused one must be zero. Throws when either ID is invalid, when `startedActionSequence` is zero, when the clock kind is unrecognised, or when the counters do not match the clock kind.

    - `remainingElapsedTicks` &mdash; For an elapsed-tick clock, the ticks still to wait - remaining, not elapsed. Must be positive and within the timing-tick limit. Must be zero for an owner-opportunity clock.
    - `remainingOwnerOpportunities` &mdash; For an owner-opportunity clock, how many more of the owner's own actions must complete before the skill is free again. Must be positive and within the timing-tick limit. Must be zero for an elapsed-tick clock.
    - `startedActionSequence` &mdash; The root action that started this cooldown. The engine uses it to avoid counting that same action against an owner-opportunity clock.
    - `clockKind` &mdash; Whether elapsed ticks or completed owner opportunities decrement the live counter.
    - `ownerId` &mdash; The required combatant identity whose skill availability is blocked.
    - `skillId` &mdash; The required skill identity blocked until the selected counter expires.

**Properties**

`public CooldownClockKind ClockKind`

:   Which of the two remaining counters is live. `CooldownClockKind.ElapsedTicks` counts `RemainingElapsedTicks` down as the battle advances, so it thaws on its own; `CooldownClockKind.OwnerOpportunities` counts `RemainingOwnerOpportunities` down only as the owner finishes further actions, so it does not move while the owner does nothing. The counter belonging to the other kind stays zero.

`public StableId OwnerId`

:   The combatant this cooldown blocks. Cooldowns are per combatant, so an ally holding the same skill is unaffected by it.

`public int RemainingElapsedTicks`

:   Ticks still to wait, not ticks already spent. Zero unless `ClockKind` is `CooldownClockKind.ElapsedTicks`.

`public int RemainingOwnerOpportunities`

:   How many more of the owner's own actions must complete before the skill is free. Zero unless `ClockKind` is `CooldownClockKind.OwnerOpportunities`.

`public StableId SkillId`

:   The blocked skill. A command from the owner naming it is rejected with `command.skill.cooldown` for as long as this entry exists.

`public ulong StartedActionSequence`

:   The root action sequence that started this cooldown. Always below the snapshot's `BattleSnapshot.NextActionSequence`.

---

## DecisionControlKind

```csharp
public enum DecisionControlKind : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerDefinitions.cs</small>

Who fills a scheduled decision. `Human` holds the opportunity open for
an externally submitted command; `Automatic` has the combatant's AI
policy produce one, and a combatant declared automatic must resolve to a
known AI policy or the battle fails to start.

| Value | Meaning |
| --- | --- |
| `Human` | Chooses human semantics for decision control kind. |
| `Automatic` | Chooses automatic semantics for decision control kind. |

---

## DecisionEntry

```csharp
public sealed class DecisionEntry
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Scheduling/SchedulerSnapshot.cs</small>

One queued decision opportunity: an actor that became ready at a known
tick and is waiting for its command. The queue holding these is ordered
by `(readyTick, actorId, opportunitySequence)` and only its first
entry is served, so that ordering is what decides turn order.

**Constructors**

`public DecisionEntry(ulong opportunitySequence, long readyTick, StableId actorId, DecisionControlKind controlKind)`

:   Creates a decision entry. A zero opportunity sequence, a negative ready tick, an unset actor, or an undefined control kind throws.

    - `opportunitySequence` &mdash; The engine-assigned sequence for this readiness. Must be non-zero and unique inside the queue that receives the entry.
    - `readyTick` &mdash; The tick at which the actor became ready.
    - `controlKind` &mdash; Whether the command answering this opportunity comes from the player or from the actor's automatic decision policy.
    - `actorId` &mdash; Valid combatant identifier for which this unique queued opportunity awaits a command.

**Properties**

`public StableId ActorId`

:   The combatant this opportunity is being held open for. An actor can hold only one queued decision at a time, so this identifies the entry as precisely as its opportunity sequence does.

`public DecisionControlKind ControlKind`

:   The actor's control when the opportunity was created: a Human entry awaits a submitted command, an Automatic one is answered by the actor's decision policy.

`public ulong OpportunitySequence`

:   Monotonic scheduler opportunity number recorded for ordering and diagnostics. It is distinct from command, event, and action sequences.

`public long ReadyTick`

:   The tick the actor became ready, not a deadline.

---

## PropertyEntry

```csharp
public readonly struct PropertyEntry
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/TaggedValue.cs</small>

One key and one tagged value, the element type of a PropertySet. Both
halves are required: neither an invalid key nor a null value can be stored.

**Constructors**

`public PropertyEntry(StableId key, TaggedValue value)`

:   Pairs a key with a value, rejecting the default StableId as a key and a null value.

    - `key` &mdash; The non-default semantic identifier used to sort and retrieve the property.
    - `value` &mdash; The non-null tagged payload associated with `key`.

**Properties**

`public StableId Key`

:   The identifier this entry is filed under, never the default StableId. A set orders its entries by this key and holds no two entries with the same one, so it also fixes where the entry sits.

`public TaggedValue Value`

:   The payload stored against the key, never null. Read `TaggedValue.Tag` before reaching for an accessor unless the tag is already known, because the accessors throw on a mismatch.

---

## PropertySet

**Start here**

```csharp
public sealed class PropertySet : IReadOnlyList<PropertyEntry>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/TaggedValue.cs</small>

The immutable, sorted, bounded property bag every mechanics extension is
configured with: a formula, effect resolver, target resolver, AI policy, or
reaction rule reads its authored settings from one of these and from
nothing else. Keys are unique and held in ascending StableId ordinal order,
which is what makes TryGetValue a binary search and what makes the
canonical hash of a set reproducible - two sets with the same pairs hash
identically, so content and replays can be compared byte for byte.

!!! note "Remarks"
    Ordering is enforced at construction, not fixed up: entries supplied out of
    order, or with a duplicate key, are rejected rather than sorted. Sort your
    entries by key before constructing the set.

**Constructors**

`public PropertySet(IEnumerable<PropertyEntry> entries)`

:   Copies entries into an immutable set.

    - `entries` &mdash; Must already be in ascending StableId ordinal order with no repeated key; more than 256 entries is rejected. Copied immediately, so later changes to the source are not seen.

**Properties**

`public int Count`

:   How many key and value pairs the set holds; never more than 256, which is the limit construction enforces.

`public static PropertySet Empty`

:   The shared set with no entries. Pass it for a mechanics implementation that takes no configuration rather than constructing an empty set each time, since every caller can safely hold the same immutable instance.

**Methods**

`public IEnumerator<PropertyEntry> GetEnumerator()`

:   Walks the entries in ascending key order, which is the same order the canonical encoder writes them in.

    - **Returns** &mdash; An enumerator over entries in ascending property-key order.

`public TaggedValue Require(StableId key, TaggedValueTag expectedTag)`

:   Reads a property that must be present with a known tag, throwing an ArgumentException when it is missing or carries a different tag. This is the accessor to use inside a mechanics extension once compile-time validation has already established the property is mandatory.

    - `expectedTag` &mdash; The tag the value must carry; a mismatch throws rather than converting.
    - `key` &mdash; The identifier of the mandatory property.
    - **Returns** &mdash; The value, never null.

`public bool TryGetValue(StableId key, out TaggedValue value)`

:   Finds a property by key, using a binary search over the sorted entries and allocating nothing.

    - `value` &mdash; The value when the key is present, and null when it is not.
    - `key` &mdash; The property identifier to locate by ordinal binary search.
    - **Returns** &mdash; True when the key is present.

---

## ResourceState

```csharp
public sealed class ResourceState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

One combatant's pool for one resource, such as mana or stamina. A snapshot holds at most one
entry per owner-and-resource pair, so this is the whole of that pool's state.

**Constructors**

`public ResourceState(StableId ownerId, StableId resourceId, int maximum, int current)`

:   Creates a resource pool. Throws when either ID is invalid, when `maximum` is not positive, or when `current` falls outside 0..`maximum`.

    - `ownerId` &mdash; The combatant that owns the pool. Resources are never shared.
    - `current` &mdash; The available amount, inclusively bounded from zero through `maximum`.
    - `maximum` &mdash; The positive immutable capacity of this pool.
    - `resourceId` &mdash; The required compiled resource identity held by the pool.

**Properties**

`public int Current`

:   The amount available now, between zero and `Maximum`. A command whose costs exceed it is rejected with `command.cost.unpayable` rather than driving the pool negative, so this is the value a decision UI should grey a skill out against.

`public int Maximum`

:   The pool's ceiling, always positive and fixed for the battle. Gains and interrupt refunds clamp here instead of overfilling, which is why a refund can come back partial.

`public StableId OwnerId`

:   The combatant the pool belongs to. Pools are never shared, so owner and resource together identify one entry in `BattleSnapshot.Resources`.

`public StableId ResourceId`

:   Which compiled resource the pool holds - mana, stamina, or whatever the content declares. A skill cost naming the same ID is charged against this pool.

---

## StartTeam

```csharp
public sealed class StartTeam
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/CompiledBattleContent.cs</small>

One side as a battle begins: its id and the combatants it fields.

A battle takes exactly two, with distinct ids. Build them with the
constructor; `CreateB2` exists to rebuild a team from an older
contract version during restore and is not the way to author a new one.

**Constructors**

`public StartTeam(StableId teamId, IEnumerable<StartCombatant> combatants)`

:   Creates a profile-1 starting team containing at least one living targetable combatant.

    - `combatants` &mdash; One to the per-team limit of non-null profile-1 combatants with unique identifiers.
    - `teamId` &mdash; The non-default identity that must differ from the opposing team's identifier.

**Properties**

`public FrozenList<StartCombatant> Combatants`

:   Gets the team's starting combatants, sorted by combatant identifier.

`public StableId TeamId`

:   Stable ID for team ID; compare ordinal identity and resolve display text separately.

**Methods**

`public static StartTeam CreateB2(StableId teamId, IEnumerable<StartCombatant> combatants)`

:   Creates a profile-2 starting team containing at least one living combatant.

    - `combatants` &mdash; One to the per-team limit of non-null profile-2 combatants with unique identifiers.
    - `teamId` &mdash; The non-default identity that must differ from the opposing team's identifier.
    - **Returns** &mdash; An immutable profile-2 team whose combatants are sorted by identifier.

---

## TaggedValue

```csharp
public sealed class TaggedValue
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/TaggedValue.cs</small>

One immutable value carrying exactly one of the tagged payloads; it is the
value half of a PropertySet and so the unit every mechanics extension is
configured with. Accessors are tag-checked rather than reinterpreting, so
reading Int32Value on a Fixed64 value throws an InvalidOperationException
instead of handing back a plausible wrong number. Instances come only from
the From factory methods, which copy every array and byte payload on the
way in; collections are handed back as immutable FrozenList values and the
byte payload is copied on every read, so a value can never change under a
holder.

**Properties**

`public FrozenList<bool> BooleanArrayValue`

:   The wrapped bools, in the order they were supplied.

`public bool BooleanValue`

:   The wrapped bool. Nothing is coerced into one: a value carrying any other tag throws rather than reporting false.

`public byte[] BytesValue`

:   A fresh copy of the byte payload on every read, so mutating the array you get back does not affect the value. Copy once and reuse it if the blob is large.

`public FrozenList<Chance64> Chance64ArrayValue`

:   The wrapped probabilities, in the order they were supplied.

`public Chance64 Chance64Value`

:   The wrapped probability, rebuilt from the raw units stored when the value was created, so it survives the round trip exactly.

`public FrozenList<Fixed64> Fixed64ArrayValue`

:   The wrapped fixed-point numbers, in the order they were supplied.

`public Fixed64 Fixed64Value`

:   The wrapped fixed-point number, rebuilt from the raw units stored when the value was created, so it survives the round trip exactly.

`public FrozenList<int> Int32ArrayValue`

:   The wrapped ints, in the order they were supplied.

`public int Int32Value`

:   The wrapped int. A Fixed64 or Chance64 value is not reinterpreted as its raw units here; reading it through the wrong accessor throws instead of handing back a plausible wrong number.

`public FrozenList<long> Int64ArrayValue`

:   The wrapped longs, in the order they were supplied.

`public long Int64Value`

:   The wrapped long, for magnitudes that do not fit an int.

`public FrozenList<StableId> StableIdArrayValue`

:   The wrapped identifiers, in the order they were supplied and none of them the default StableId. The list is the immutable copy taken at construction, so nothing you do with it can change the value.

`public StableId StableIdValue`

:   The wrapped identifier, always a valid one because the factory refuses to store the default StableId.

`public FrozenList<string> StringArrayValue`

:   The wrapped strings, in the order they were supplied, each already normalized to Unicode NFC.

`public string StringValue`

:   The wrapped string, already normalized to Unicode NFC because the factory rejects one that is not.

`public TaggedValueTag Tag`

:   Which payload this value carries, and so the one accessor below that may be read from it. Test it first whenever the tag is not already fixed by the validation an extension went through at compile time.

`public uint UInt32Value`

:   The wrapped uint. The UInt32 tag stays decodable so earlier-schema commands and replays still load, but it sits outside schema 3's property union, so a schema 3 property carrying it is rejected when the content is compiled or canonically serialized.

`public FrozenList<ulong> UInt64ArrayValue`

:   The wrapped ulongs, in the order they were supplied.

`public ulong UInt64Value`

:   The wrapped ulong. A UInt32 value cannot be widened through this accessor: the tag has to match exactly.

**Methods**

`public static TaggedValue FromBoolean(bool value)`

:   Wraps a bool, readable afterwards only through BooleanValue.

    - `value` &mdash; The Boolean payload to store without conversion.
    - **Returns** &mdash; A value tagged `TaggedValueTag.Boolean`.

`public static TaggedValue FromBooleans(IEnumerable<bool> values)`

:   Copies bools into an immutable array value, readable afterwards only through BooleanArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected.
    - **Returns** &mdash; An immutable Boolean-array value preserving source order.

`public static TaggedValue FromBytes(byte[] value)`

:   Copies a byte blob into a value readable afterwards only through BytesValue. Like FromUInt32, the Bytes tag sits outside schema 3's property union and is rejected when schema 3 content is compiled or canonically serialized.

    - `value` &mdash; Copied immediately, so mutating the caller's array afterwards does not affect the value. Longer than 1 MiB is rejected.
    - **Returns** &mdash; A legacy-compatible bytes value containing a defensive copy of the payload.

`public static TaggedValue FromChance64(Chance64 value)`

:   Wraps a probability, storing its raw units unchanged and readable afterwards only through Chance64Value.

    - `value` &mdash; The probability payload whose raw units are preserved.
    - **Returns** &mdash; A value tagged `TaggedValueTag.Chance64`.

`public static TaggedValue FromChance64s(IEnumerable<Chance64> values)`

:   Copies probabilities into an immutable array value, readable afterwards only through Chance64ArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected.
    - **Returns** &mdash; An immutable probability-array value preserving source order.

`public static TaggedValue FromFixed64(Fixed64 value)`

:   Wraps a fixed-point number, storing its raw units unchanged and readable afterwards only through Fixed64Value.

    - `value` &mdash; The fixed-point payload whose raw units are preserved.
    - **Returns** &mdash; A value tagged `TaggedValueTag.Fixed64`.

`public static TaggedValue FromFixed64s(IEnumerable<Fixed64> values)`

:   Copies fixed-point numbers into an immutable array value, readable afterwards only through Fixed64ArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected.
    - **Returns** &mdash; An immutable fixed-point-array value preserving source order.

`public static TaggedValue FromInt32(int value)`

:   Wraps an int, readable afterwards only through Int32Value.

    - `value` &mdash; The signed 32-bit integer payload to store.
    - **Returns** &mdash; A value tagged `TaggedValueTag.Int32`.

`public static TaggedValue FromInt32s(IEnumerable<int> values)`

:   Copies ints into an immutable array value, readable afterwards only through Int32ArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected.
    - **Returns** &mdash; An immutable 32-bit integer-array value preserving source order.

`public static TaggedValue FromInt64(long value)`

:   Wraps a long, readable afterwards only through Int64Value.

    - `value` &mdash; The signed 64-bit integer payload to store.
    - **Returns** &mdash; A value tagged `TaggedValueTag.Int64`.

`public static TaggedValue FromInt64s(IEnumerable<long> values)`

:   Copies longs into an immutable array value, readable afterwards only through Int64ArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected.
    - **Returns** &mdash; An immutable 64-bit integer-array value preserving source order.

`public static TaggedValue FromStableId(StableId value)`

:   Wraps an identifier, readable afterwards only through StableIdValue.

    - `value` &mdash; Must be a valid StableId; the default identifier is rejected so a property can never carry a placeholder reference.
    - **Returns** &mdash; A value tagged `TaggedValueTag.StableId` that contains the supplied identifier.

`public static TaggedValue FromStableIds(IEnumerable<StableId> values)`

:   Copies identifiers into an immutable array value, readable afterwards only through StableIdArrayValue.

    - `values` &mdash; Copied immediately, so later changes to the source are not seen. More than 256 entries, or any default identifier among them, is rejected.
    - **Returns** &mdash; A value tagged `TaggedValueTag.StableIdArray` with an immutable copy of the identifiers.

`public static TaggedValue FromString(string value)`

:   Wraps a string, readable afterwards only through StringValue.

    - `value` &mdash; Must already be normalized to Unicode NFC; a string that is not gets rejected rather than normalized for you. It must also contain only valid Unicode scalar sequences and must not exceed 1 MiB once encoded as UTF-8.
    - **Returns** &mdash; A value tagged `TaggedValueTag.String` containing the validated text.

`public static TaggedValue FromStrings(IEnumerable<string> values)`

:   Copies strings into an immutable array value, readable afterwards only through StringArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected, and every entry must satisfy the same NFC, valid-Unicode, and 1 MiB UTF-8 rules FromString applies.
    - **Returns** &mdash; An immutable string-array value containing the validated NFC strings in source order.

`public static TaggedValue FromUInt32(uint value)`

:   Wraps a uint, readable afterwards only through UInt32Value. Prefer FromInt64 or FromUInt64 for new content: the UInt32 tag sits outside schema 3's property union and is rejected when schema 3 content is compiled or canonically serialized.

    - `value` &mdash; The unsigned 32-bit integer payload to store for legacy profiles.
    - **Returns** &mdash; A value tagged `TaggedValueTag.UInt32`.

`public static TaggedValue FromUInt64(ulong value)`

:   Wraps a ulong, readable afterwards only through UInt64Value.

    - `value` &mdash; The unsigned 64-bit integer payload to store.
    - **Returns** &mdash; A value tagged `TaggedValueTag.UInt64`.

`public static TaggedValue FromUInt64s(IEnumerable<ulong> values)`

:   Copies ulongs into an immutable array value, readable afterwards only through UInt64ArrayValue.

    - `values` &mdash; Copied immediately. More than 4,096 entries is rejected.
    - **Returns** &mdash; An immutable unsigned 64-bit integer-array value preserving source order.

---

## TaggedValueTag

```csharp
public enum TaggedValueTag : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/TaggedValue.cs</small>

Which payload a TaggedValue carries, and therefore the one accessor on it
that may be read. The tag byte is written verbatim into canonical output,
so these numbers are part of the serialized format and cannot be
renumbered.

| Value | Meaning |
| --- | --- |
| `Boolean` | Encodes a boolean payload in canonical property data. |
| `Int32` | Encodes a 32-bit integer payload in canonical property data. |
| `Int64` | Encodes a 64-bit integer payload in canonical property data. |
| `UInt32` | A uint. |
| `UInt64` | Encodes a u 64-bit integer payload in canonical property data. |
| `Fixed64` | A deterministic fixed-point number in raw units, where 10,000 equals 1.0. |
| `StableId` | Encodes a stable ID payload in canonical property data. |
| `StableIdArray` | A list of identifiers, none of which is ever the default StableId. |
| `Bytes` | An opaque byte blob. |
| `Chance64` | A deterministic probability in raw units, where 1,000,000 equals 100%. |
| `String` | Encodes a string payload in canonical property data. |
| `BooleanArray` | Encodes a boolean array payload in canonical property data. |
| `Int32Array` | Encodes a 32-bit integer array payload in canonical property data. |
| `Int64Array` | Encodes a 64-bit integer array payload in canonical property data. |
| `UInt64Array` | Encodes a u 64-bit integer array payload in canonical property data. |
| `Fixed64Array` | Encodes a fixed-point array payload in canonical property data. |
| `Chance64Array` | Encodes a fixed-point probability array payload in canonical property data. |
| `StringArray` | Encodes a string array payload in canonical property data. |

---

## TeamState

```csharp
public sealed class TeamState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

Immutable state of one team in a `BattleSnapshot`. A battle carries exactly
two of these.

**Constructors**

`public TeamState(StableId id, bool conceded)`

:   Creates a team state. Throws when `id` is invalid.

    - `conceded` &mdash; Whether the team has conceded. A conceded team is treated as having no surviving side when the engine tests for a terminal result, even while its combatants are still alive.
    - `id` &mdash; The required battle-unique team identity.

**Properties**

`public bool Conceded`

:   Whether the team has conceded. A conceded team cannot win and cannot retain an active opportunity.

`public StableId Id`

:   Stable identity of this TeamState within battle state. Display labels and object references are resolved outside the simulation.

---
