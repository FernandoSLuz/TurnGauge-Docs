# Running a battle

12 types in this area.

!!! abstract "On this page"
    [AdvanceTicksOutcome](#advanceticksoutcome) &middot; [AdvanceTicksResult](#advanceticksresult) &middot; [BattleEngine](#battleengine) &middot; [BattleResultState](#battleresultstate) &middot; [BattleStartRequest](#battlestartrequest) &middot; [CommandDisposition](#commanddisposition) &middot; [CommandResult](#commandresult) &middot; [SimulationLimits](#simulationlimits) &middot; [StepActionOutcome](#stepactionoutcome) &middot; [StepActionResult](#stepactionresult) &middot; [StepEventOutcome](#stepeventoutcome) &middot; [StepEventResult](#stepeventresult)

## AdvanceTicksOutcome

**Start here**

```csharp
public enum AdvanceTicksOutcome
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Why one `BattleEngine.AdvanceTicks(int)` call stopped.
`ReachedTarget` is the only value that means the requested target
tick was reached; the others each report a boundary the engine refused
to cross. Because the engine never advances past its target, every other
outcome leaves the battle at or below it.

| Value | Meaning |
| --- | --- |
| `ReachedTarget` | The requested target tick was reached with no event owed below it. |
| `AwaitingCommand` | A pending human decision stopped tick progress short of the target under the selected input-pause policy. |
| `Terminal` | The battle ended before the target tick was reached. |
| `NoScheduledWork` | A valid nonterminal configuration stalled with no future work before the target tick was reached. |
| `FatalInvariant` | A typed invariant or overflow failure, including a target tick that would overflow the battle clock. |

---

## AdvanceTicksResult

**Start here**

```csharp
public sealed class AdvanceTicksResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Immutable result of one `BattleEngine.AdvanceTicks(int)`
call: the outcome that stopped it, the absolute tick it was aiming for,
every event emitted on the way in strict tick and event-sequence order,
and the authoritative snapshot that follows. This is the result a
continuous game loop consumes: presentation converts elapsed real time
into an integer tick count, calls AdvanceTicks, and plays back the
returned events. No cast, status tick, cooldown, readiness, reaction, or
result event between the old and target ticks is ever skipped, and
consuming the returned events cannot alter the snapshot or the
event-chain digest.

**Properties**

`public FrozenList<AiDecisionTrace> AiDecisionTraces`

:   Non-authoritative AI decision evidence produced by this call alone, accumulated across every reduction it performed. It has been removed from the engine buffer, so `BattleEngine.DrainAiDecisionTraces` will not return it a second time.

`public Diagnostic? Diagnostic`

:   The typed failure. Set only for `AdvanceTicksOutcome.FatalInvariant`.

`public FrozenList<BattleEvent> Events`

:   Every event emitted during this call, already in strict tick and event-sequence order. Events produced before the call stopped or failed are still returned, so this can be non-empty for any outcome.

`public FrozenList<FormulaAttributionTrace> FormulaAttributionTraces`

:   Shorthand for `FormulaAttributions.Traces`.

`public FormulaAttributionTraceBatch FormulaAttributions`

:   Non-authoritative formula evidence produced by this call alone, likewise already handed over by the engine.

`public long OmittedFormulaAttributionTraceCount`

:   Shorthand for `FormulaAttributions.OmittedCount`: how many formula traces were produced but dropped to stay inside the documented result-memory bound.

`public AdvanceTicksOutcome Outcome`

:   Why the call stopped. Only `AdvanceTicksOutcome.ReachedTarget` means the requested target tick was reached; execution never runs past it, so every other value leaves the battle at or below `TargetTick`, which for a count that would overflow the battle clock is the unchanged current tick. A game loop that assumes the ticks it asked for were always spent will drift, so drive the next call from the returned snapshot's tick rather than from its own accumulator.

`public BattleSnapshot Snapshot`

:   The authoritative state the call stopped on. A reduction that failed is rolled back, so this is never a partially reduced state.

`public long TargetTick`

:   The absolute tick the call aimed to reach, not the number of ticks requested. When the requested count would overflow the battle clock no target exists, and this reports the unchanged current tick alongside `AdvanceTicksOutcome.FatalInvariant`.

---

## BattleEngine

**Start here**

```csharp
public sealed partial class BattleEngine
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.B2.cs</small>

Owns immutable battle state and advances it through deterministic command, scheduler, action, event, and mechanics reduction boundaries.

**Properties**

`public CompiledBattleContent Content`

:   The compiled content this battle runs against. Keep it beside the snapshot: restoring or replaying the battle needs content that hashes to the manifest digest recorded on the snapshot, and any other content is refused.

`public BattleMechanicsRegistry MechanicsRegistry`

:   The formula, effect, target, AI, and reaction implementations bound to this battle. Null for a B1 or B2 battle, because only the B3 profile resolves extensions through a mechanics registry.

`public SimulationContractProfile Profile`

:   The mechanics profile, taken from `Content`. It selects which reducer runs, and so determines which parts of a snapshot are populated at all: stats, statuses, shields, and reactions only exist under the B3 profile.

`public uint Seed`

:   The seed the battle's random sequence was expanded from. Record it alongside the content and the start request; those three plus the command order are what a reproduction needs.

`public BattleStartRequest StartRequest`

:   The start request the battle was created from. It stays reachable because restore and replay must be handed the same one, and because execution keeps reading per-combatant start data from it, such as granted skills and the initial gauge.

**Methods**

`public AdvanceTicksResult AdvanceTicks(int count)`

:   Advances the battle by up to `count` ticks and returns every event emitted along the way.

    - `count` &mdash; How many ticks to advance, relative to the current tick. Zero is allowed; negative values are not.
    - **Returns** &mdash; Why the call stopped, the absolute tick it aimed at, the events it emitted in tick and event-sequence order, and the resulting snapshot.

`public BattleEngine Clone()`

:   Returns a second engine positioned on the current snapshot and sharing the same content, start request, seed, scheduler, and registries.

    - **Returns** &mdash; An independently step-able engine at the same immutable snapshot, with shared static dependencies and empty diagnostic trace buffers.

`public static BattleEngine Create(CompiledBattleContent content, BattleStartRequest startRequest, uint seed)`

:   Starts a new battle on the built-in schedulers and the built-in mechanics and returns it standing on the opening snapshot. Nothing is reduced yet and no event exists: the opening work, including `battle.started`, is queued on that snapshot and is first reduced by a step or advance call. This is the overload to reach for unless the project ships a custom scheduler or a custom formula, effect, target, AI, or reaction implementation.

    - `content` &mdash; Compiled content whose profile must match that of `startRequest`; the profile also decides which reducer the returned engine runs.
    - `startRequest` &mdash; The roster, teams, and scheduler choice to open with.
    - `seed` &mdash; Seed for the battle's random sequence. The same seed and the same command order reproduce the run exactly.
    - **Returns** &mdash; An engine standing on the battle's first snapshot.

`public static BattleEngine Create(CompiledBattleContent content, BattleStartRequest startRequest, uint seed, BattleSchedulerRegistry registry)`

:   Starts a new battle on a caller-supplied scheduler registry, keeping the built-in mechanics. Use this when the project ships its own turn-order or gauge scheduler but no custom formulas or effects.

    - `content` &mdash; Compiled content whose profile must match that of `startRequest`.
    - `startRequest` &mdash; The roster, teams, and scheduler choice to open with.
    - `seed` &mdash; Seed for the battle's random sequence.
    - `registry` &mdash; Registry consulted for the scheduler named by the start request. It must also supply a state codec that accepts the state the scheduler creates, otherwise the battle is refused rather than started on a state that could not be saved.
    - **Returns** &mdash; An engine standing on the battle's first snapshot.

`public static BattleEngine Create(CompiledBattleContent content, BattleStartRequest startRequest, uint seed, BattleSchedulerRegistry schedulerRegistry, BattleMechanicsRegistry mechanicsRegistry)`

:   Starts a new battle on caller-supplied scheduler and mechanics registries. This is the overload a B3 battle with custom formulas, effects, targeting, AI, or reactions needs, because the compiled content is checked against the mechanics registry up front: every implementation the content names must be registered at the contract version it was compiled for, or the battle is refused here rather than failing partway through a fight.

    - `content` &mdash; Compiled content whose profile must match that of `startRequest`.
    - `startRequest` &mdash; The roster, teams, and scheduler choice to open with.
    - `seed` &mdash; Seed for the battle's random sequence.
    - `schedulerRegistry` &mdash; Registry consulted for the scheduler named by the start request.
    - `mechanicsRegistry` &mdash; Registry consulted for the mechanics implementations the content names. Its bindings are hashed into the snapshot, so a battle cannot later be restored against a differently bound registry.
    - **Returns** &mdash; An engine standing on the battle's first snapshot.

`public FrozenList<AiDecisionTrace> DrainAiDecisionTraces()`

:   Removes and returns whatever AI decision evidence is still buffered on the engine.

    - **Returns** &mdash; All currently buffered non-authoritative AI decision traces in recording order; the engine buffer is empty after the call.

`public FormulaAttributionTraceBatch DrainFormulaAttributionTraces()`

:   Removes and returns whatever formula attribution evidence is still buffered on the engine, on the same terms as `DrainAiDecisionTraces`. The returned batch also reports how many traces were dropped to stay inside the documented memory bound, so a caller can tell a quiet battle from a truncated one.

    - **Returns** &mdash; All buffered formula traces plus their omitted count; taking the batch clears both values from the engine buffer.

`public BattleSnapshot GetSnapshot()`

:   Returns the current authoritative state. The returned snapshot is immutable and is never edited in place, so it stays valid after the engine steps; call again to see the state that followed.

    - **Returns** &mdash; The immutable authoritative snapshot currently owned by this engine; later reductions replace rather than mutate it.

`public static BattleEngine Restore(CompiledBattleContent content, BattleStartRequest startRequest, uint seed, BattleSnapshot snapshot)`

:   Resumes a saved battle on the built-in schedulers and mechanics, continuing from `snapshot` exactly where it left off, including the position in the random sequence.

    - `content` &mdash; The same compiled content the battle was created against.
    - `startRequest` &mdash; The same start request the battle was created from.
    - `seed` &mdash; The seed the battle was created with.
    - `snapshot` &mdash; A snapshot previously taken from that battle.
    - **Returns** &mdash; An engine standing on `snapshot`.

`public static BattleEngine Restore(CompiledBattleContent content, BattleStartRequest startRequest, uint seed, BattleSnapshot snapshot, BattleSchedulerRegistry registry)`

:   Resumes a saved battle on a caller-supplied scheduler registry, keeping the built-in mechanics. Use this when the save was written by a battle running a custom scheduler, since the saved scheduler state can only be recognised by the codec that registry provides.

    - `content` &mdash; The same compiled content the battle was created against.
    - `startRequest` &mdash; The same start request the battle was created from.
    - `seed` &mdash; The seed the battle was created with.
    - `snapshot` &mdash; A snapshot previously taken from that battle.
    - `registry` &mdash; Registry that must resolve the scheduler named on the snapshot.
    - **Returns** &mdash; An engine standing on `snapshot`.

`public static BattleEngine Restore(CompiledBattleContent content, BattleStartRequest startRequest, uint seed, BattleSnapshot snapshot, BattleSchedulerRegistry schedulerRegistry, BattleMechanicsRegistry mechanicsRegistry)`

:   Resumes a saved battle on caller-supplied scheduler and mechanics registries. A B3 save needs this overload for two separate checks: `mechanicsRegistry` must resolve every mechanics binding `content` names, each at the contract version it was compiled for, and the binding digest recorded on the snapshot must equal the digest recomputed from that content. Content that has since moved a skill, status, or policy onto a different implementation id or contract version is therefore refused here instead of silently changing how the rest of the fight resolves. The digest covers those declared ids and versions only, so a different implementation object registered under the same id and version is not detected.

    - `content` &mdash; The same compiled content the battle was created against.
    - `startRequest` &mdash; The same start request the battle was created from.
    - `seed` &mdash; The seed the battle was created with.
    - `snapshot` &mdash; A snapshot previously taken from that battle.
    - `schedulerRegistry` &mdash; Registry that must resolve the scheduler named on the snapshot.
    - `mechanicsRegistry` &mdash; Registry that must reproduce the bindings the snapshot was written under.
    - **Returns** &mdash; An engine standing on `snapshot`.

`public FrozenList<BattleEvent> RunUntilBoundary()`

:   Steps events until the battle stops producing them and returns all of them in emission order.

    - **Returns** &mdash; Every event emitted before the battle stopped, in emission order.

`public StepActionResult StepAction()`

:   Drives execution to the end of one root action and returns every event emitted on the way, in order.

    - **Returns** &mdash; Why the call stopped, the events it emitted, and the snapshot at that boundary.

`public StepEventResult StepEvent()`

:   Reduces queued execution work until exactly one gameplay event is emitted, or until the battle stops at a boundary, stalls, or fails.

    - **Returns** &mdash; Why the call stopped, the event it emitted if any, and the resulting snapshot.

`public CommandResult Submit(BattleCommand command)`

:   Offers one command to the battle and runs command validation only.

    - `command` &mdash; The command to offer. Its sequence number and requested tick must match the current snapshot.
    - **Returns** &mdash; How the command was treated, the one command event it produced, and the snapshot that follows.

---

## BattleResultState

**Start here**

```csharp
public sealed class BattleResultState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Model/BattleSnapshot.cs</small>

The battle's outcome as of one snapshot: either nonterminal (`None`) or a
terminal verdict naming the result and, for team outcomes, the surviving and eliminated
teams. Victory and defeat are the same event seen from two sides - `WinningTeamId`
is always the surviving team, and the engine reports victory rather than defeat only when
that survivor is the start request's perspective team. Every combination is validated at
construction, so an instance can never claim a winner it has no result for, or a result
while the battle is still running.

**Constructors**

`public BattleResultState(bool terminal, StableId resultId, StableId winningTeamId, StableId losingTeamId)`

:   Creates a result from raw IDs, treating an invalid ID as absent. Prefer the named factories below. Throws when a nonterminal result is given any ID, when the result ID is not one of the five supported outcomes, when a team outcome is missing two distinct valid team IDs, or when a teamless outcome carries team IDs.

    - `terminal` &mdash; Whether the battle has ended. When `false`, all three IDs must be invalid.
    - `resultId` &mdash; One of `battle.victory`, `battle.defeat`, `battle.concession`, `battle.draw`, or `battle.stalled`. The first three require both team IDs; the last two must have neither.
    - `winningTeamId` &mdash; The surviving team, for the three team outcomes.
    - `losingTeamId` &mdash; The eliminated or conceding team, for the three team outcomes.

**Properties**

`public bool IsTerminal`

:   Whether the battle has ended. While it is `false` the other three properties are all `null`, so this is the flag to test before reading them, and the condition a loop driving the engine stops on.

`public StableId? LosingTeamId`

:   The eliminated or conceding team. `null` while nonterminal and for the teamless draw and stalled outcomes.

`public StableId? ResultId`

:   Which of the five outcomes ended the battle, or `null` while nonterminal.

`public StableId? WinningTeamId`

:   The surviving team, regardless of whether the result reads as victory or defeat. `null` while nonterminal and for the teamless draw and stalled outcomes.

**Fields**

`public static readonly BattleResultState None`

:   The nonterminal result: the battle is still running and carries no result, winner, or loser ID. This is the value a fresh snapshot starts with.

**Methods**

`public static BattleResultState Concession(StableId winningTeamId, StableId losingTeamId)`

:   A terminal `battle.concession`: the battle ended because one team conceded rather than because it was eliminated.

    - `winningTeamId` &mdash; The team that did not concede.
    - `losingTeamId` &mdash; The conceding team.
    - **Returns** &mdash; A terminal concession state naming the surviving and conceding teams.

`public static BattleResultState Defeat(StableId winningTeamId, StableId losingTeamId)`

:   A terminal `battle.defeat`: one team survived and it is not the perspective team.

    - `winningTeamId` &mdash; The surviving team - the perspective team's opponent.
    - `losingTeamId` &mdash; The eliminated perspective team.
    - **Returns** &mdash; A terminal defeat state carrying both distinct valid team identities.

`public static BattleResultState Draw()`

:   A terminal `battle.draw`: neither team has a living combatant left on an unconceded team, so there is no winner to name.

    - **Returns** &mdash; A terminal draw state with no winner or loser identity.

`public static BattleResultState Stalled()`

:   A terminal `battle.stalled`: both teams were still standing when the battle hit its configured root-action or tick limit, so the engine stopped without a winner.

    - **Returns** &mdash; A terminal stalled state with no winner or loser identity.

`public static BattleResultState Victory(StableId winningTeamId, StableId losingTeamId)`

:   A terminal `battle.victory`: one team survived and it is the start request's perspective team.

    - `winningTeamId` &mdash; The surviving perspective team.
    - `losingTeamId` &mdash; The opposing team, which must differ from the winner.
    - **Returns** &mdash; A terminal victory state carrying both distinct valid team identities.

---

## BattleStartRequest

**Start here**

```csharp
public sealed partial class BattleStartRequest
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Content/BattleStartV3.cs</small>

The immutable opening state of one battle: the scheduler that will run it, the two
opposing teams, and the health, resources, and statuses every combatant starts
with. Hand one to `BattleEngine` together with the compiled content it
was built against and a seed; starting a battle does not consume the request, so one
request can open any number of runs and the seed, not the request, is what varies
the rolls. Its profile-3 factories resolve every id against that compiled content
before they return, so a request they produce is one the engine will accept.

**Constructors**

`public BattleStartRequest(StableId schedulerId, IEnumerable<StartTeam> teams)`

:   Builds a profile-1 start from two opposing teams. Nothing is resolved against compiled content here, so `schedulerId` is taken on trust and the request carries no scheduler definition; use `CreateB2` or the profile-3 factories when the ids should be checked before the engine sees them.

    - `schedulerId` &mdash; The scheduler that will drive the battle. It has to be a valid id, but it is not looked up.
    - `teams` &mdash; Exactly two non-null teams with distinct ids, built with the `StartTeam` constructor rather than `StartTeam.CreateB2`. Combatant ids must not repeat across the pair. The sequence is read once and sorted by team id, so the order it arrives in cannot change the battle.

**Properties**

`public int CompiledSchemaVersion`

:   The compiled-content schema version implied by `Profile`, recorded and resolved as part of the same version tuple as `EngineVersion`.

`public int EngineVersion`

:   The engine contract version implied by `Profile`. A replay written from this start records it, and reading resolves it together with the other recorded versions back to a known profile, so it is not a number a caller sets independently.

`public StableId? PerspectiveTeamId`

:   The team the battle result is reported from: when one side is left standing, the result is a victory if that side is this team and a defeat otherwise. Always set on a profile-3 start and always `null` on profile 1 and 2 starts.

`public SimulationContractProfile Profile`

:   The contract profile this start was built for, decided by the factory that made it rather than set by the caller. The engine refuses to open a battle whose compiled content carries a different profile, so this is what stops a profile-1 start being run against profile-3 content.

`public StableId SchedulerId`

:   The scheduler that will drive the battle. On a profile-1 start it is only an id; on profile-2 and profile-3 starts it has already been resolved to a compiled scheduler definition, which is why those factories need the content.

`public FrozenList<StartTeam> Teams`

:   The two teams of a profile-1 or profile-2 start, ascending by team id. Empty on profile-3 starts, which carry their teams in `TeamsV3` instead.

`public FrozenList<StartTeamV3> TeamsV3`

:   The two teams of a profile-3 start, sorted by team id. Empty on profile 1 and 2 starts, which carry their teams in `Teams` instead.

**Methods**

`public static BattleStartRequest CreateB2(CompiledBattleContent content, StableId schedulerId, IEnumerable<StartTeam> teams)`

:   Builds a profile-2 start whose scheduler and combatants are resolved against compiled content before the request exists. Unlike the profile-1 constructor it reports a bad id at build time rather than leaving the engine to reject the pairing later, which is why it needs the content the battle will be run with.

    - `content` &mdash; Profile-2 compiled content. Every id in the start is looked up in it, and content compiled for another profile is refused.
    - `schedulerId` &mdash; The scheduler that will drive the battle. It has to name a scheduler definition present in `content`.
    - `teams` &mdash; Exactly two non-null teams with distinct ids, built through `StartTeam.CreateB2`. Combatant ids must not repeat across the pair, and the two teams together may hold at most `SimulationLimits.TotalCombatants` members.
    - **Returns** &mdash; A profile-2 start request whose teams and content references are ready for engine validation.

`public static BattleStartRequest CreateB3(CompiledBattleContent content, StableId schedulerId, IEnumerable<StartTeamV3> teams)`

:   Builds a profile-3 start, taking the perspective team to be whichever of the two team ids sorts first. Throws on the first broken start rule; call `TryCreateB3` to receive a diagnostic instead.

    - `content` &mdash; The compiled profile-3 content every id is resolved against.
    - `schedulerId` &mdash; The compiled scheduler definition that will drive the battle.
    - `teams` &mdash; Exactly two non-null teams with distinct ids.
    - **Returns** &mdash; A profile-3 start request whose default perspective is the first team in canonical order.

`public static BattleStartRequest CreateB3(CompiledBattleContent content, StableId schedulerId, IEnumerable<StartTeamV3> teams, StableId perspectiveTeamId)`

:   Builds a profile-3 start with the perspective team chosen explicitly. Throws on the first broken start rule; call `TryCreateB3` to receive a diagnostic instead.

    - `content` &mdash; The compiled profile-3 content every id is resolved against.
    - `schedulerId` &mdash; The compiled scheduler definition that will drive the battle.
    - `teams` &mdash; Exactly two non-null teams with distinct ids.
    - `perspectiveTeamId` &mdash; The team results are reported from; must be one of the two teams supplied.
    - **Returns** &mdash; A profile-3 start request reporting results from `perspectiveTeamId`.

`public static B3CreationResult<BattleStartRequest> TryCreateB3(CompiledBattleContent content, StableId schedulerId, IEnumerable<StartTeamV3> teams)`

:   Builds a profile-3 start exactly as the matching `CreateB3` overload does, inferring the perspective team, but reports a broken start rule as a failed result instead of throwing.

    - `content` &mdash; The compiled profile-3 content every id is resolved against.
    - `schedulerId` &mdash; The compiled scheduler definition that will drive the battle.
    - `teams` &mdash; Exactly two non-null teams with distinct ids.
    - **Returns** &mdash; A successful result holding the request, or a failed result carrying the single diagnostic for the first rule that was broken.

`public static B3CreationResult<BattleStartRequest> TryCreateB3(CompiledBattleContent content, StableId schedulerId, IEnumerable<StartTeamV3> teams, StableId perspectiveTeamId)`

:   Builds a profile-3 start with an explicit perspective team, reporting a broken start rule as a failed result instead of throwing.

    - `content` &mdash; The compiled profile-3 content every id is resolved against.
    - `schedulerId` &mdash; The compiled scheduler definition that will drive the battle.
    - `teams` &mdash; Exactly two non-null teams with distinct ids.
    - `perspectiveTeamId` &mdash; The team results are reported from; must be one of the two teams supplied.
    - **Returns** &mdash; A successful result holding the request, or a failed result carrying the single diagnostic for the first rule that was broken.

---

## CommandDisposition

```csharp
public enum CommandDisposition
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

How `BattleEngine.Submit(BattleCommand)` treated one
command. Only `Accepted` queues execution work for the following
step.

| Value | Meaning |
| --- | --- |
| `TransportRejected` | Refused by the transport gate before the command reached execution: the wrong command sequence, or no exposed decision or terminal boundary. |
| `Accepted` | Semantic validation accepted the command and emitted `command.accepted`. |
| `Rejected` | Semantic validation rejected the command and emitted `command.rejected`. |
| `FatalInvariant` | A typed invariant failure, or the bounded recorded-command history limit. |

---

## CommandResult

```csharp
public sealed class CommandResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Immutable result of one `BattleEngine.Submit(BattleCommand)`
call: how the command was treated, the single command event validation
produced, and the resulting snapshot. Submit runs command validation
only, so an accepted command's cast, effect, reaction, and completion
frames are still queued for the next step.

**Properties**

`public FrozenList<AiDecisionTrace> AiDecisionTraces`

:   Non-authoritative AI decision evidence produced by this call alone. It has been removed from the engine buffer, so `BattleEngine.DrainAiDecisionTraces` will not return it a second time.

`public BattleEvent CommandEvent`

:   The one `command.accepted` or `command.rejected` event validation emitted. Null for a transport rejection or a fatal invariant, because neither appends an event to the chain.

`public Sha256Digest? CommandEventHash`

:   The canonical digest of `CommandEvent`, or null when there is no command event. Replay compares this against the recorded digest to prove the same command produced the same event. The digest is recomputed on every read.

`public Diagnostic? Diagnostic`

:   The typed failure for a transport rejection or a fatal invariant. Null for an accepted command and for a semantic rejection, whose reason is `ReasonId` instead.

`public CommandDisposition Disposition`

:   How the submission was treated, and the first thing to branch on. Only `CommandDisposition.Accepted` queues execution work for the following step, and only it leaves `ReasonId` null. The two rejections differ in what they cost: a transport rejection leaves the expected command sequence and the snapshot untouched, so the same command can be resubmitted, whereas a semantic rejection consumes the sequence and is written into the recorded-command history.

`public FrozenList<FormulaAttributionTrace> FormulaAttributionTraces`

:   Shorthand for `FormulaAttributions.Traces`.

`public FormulaAttributionTraceBatch FormulaAttributions`

:   Non-authoritative formula evidence produced by this call alone, likewise already handed over by the engine.

`public long OmittedFormulaAttributionTraceCount`

:   Shorthand for `FormulaAttributions.OmittedCount`: how many formula traces were produced but dropped to stay inside the documented result-memory bound.

`public StableId? ReasonId`

:   Why the submission was not accepted: the rejection reason carried by the `command.rejected` event, or the diagnostic id for a transport rejection or a fatal invariant. Null when `Disposition` is `CommandDisposition.Accepted`.

`public BattleSnapshot Snapshot`

:   The authoritative state after submission. A transport rejection and a fatal invariant both leave this equal to the pre-submission snapshot.

---

## SimulationLimits

```csharp
public static class SimulationLimits
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Common/SimulationLimits.cs</small>

Every hard ceiling the simulation enforces, as compile-time constants.

They are here to be read, not only to be enforced: a caller sizing a buffer,
documenting a cap, or deciding whether a design fits should take the number
from here rather than restating it. Exceeding one is a typed diagnostic, not
an exception and not silent truncation, so a limit is always reported before
it costs anyone data.

The values are part of the contract. Changing one changes what content is
legal and what replays remain valid.

**Fields**

`public const int ActiveCasts`

:   Hard cap for active casts; validators reject larger inputs to bound memory and deterministic work.

`public const int AiCandidatesPerDecision`

:   Hard cap for AI candidates per decision; validators reject larger inputs to bound memory and deterministic work.

`public const int AiPolicyDefinitions`

:   Hard cap for AI policy definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int AtbGauge`

:   Hard cap for ATB gauge; validators reject larger inputs to bound memory and deterministic work.

`public const int AutomaticPolicies`

:   Hard cap for automatic policies; validators reject larger inputs to bound memory and deterministic work.

`public const int AutomaticPolicyEntries`

:   Hard cap for automatic policy entries; validators reject larger inputs to bound memory and deterministic work.

`public const int CombatantsPerTeam`

:   Hard cap for combatants per team; validators reject larger inputs to bound memory and deterministic work.

`public const int CompiledSkills`

:   Hard cap for compiled skills; validators reject larger inputs to bound memory and deterministic work.

`public const int CompiledSnapshotBytes`

:   Hard cap for compiled snapshot bytes; validators reject larger inputs to bound memory and deterministic work.

`public const int ConditionsPerAiRule`

:   Hard cap for conditions per AI rule; validators reject larger inputs to bound memory and deterministic work.

`public const int CooldownStates`

:   Hard cap for cooldown states; validators reject larger inputs to bound memory and deterministic work.

`public const int CostsPerSkill`

:   Hard cap for costs per skill; validators reject larger inputs to bound memory and deterministic work.

`public const int EffectEntriesPerSkill`

:   Hard cap for effect entries per skill; validators reject larger inputs to bound memory and deterministic work.

`public const int EffectiveSpeed`

:   Hard cap for effective speed; validators reject larger inputs to bound memory and deterministic work.

`public const int EffectiveSpeedScale`

:   Hard cap for effective speed scale; validators reject larger inputs to bound memory and deterministic work.

`public const int ExecutionFrames`

:   Hard cap for execution frames; validators reject larger inputs to bound memory and deterministic work.

`public const int ForecastActions`

:   Hard cap for forecast actions; validators reject larger inputs to bound memory and deterministic work.

`public const int ForecastEvents`

:   Hard cap for forecast events; validators reject larger inputs to bound memory and deterministic work.

`public const int ForecastTickDelta`

:   Hard cap for forecast tick delta; validators reject larger inputs to bound memory and deterministic work.

`public const int FormulaAttributionContributions`

:   Hard cap for formula attribution contributions; validators reject larger inputs to bound memory and deterministic work.

`public const int FormulaAttributionTracesPerResult`

:   Hard cap for formula attribution traces per result; validators reject larger inputs to bound memory and deterministic work.

`public const int FormulaRandomInputs`

:   Hard cap for formula random inputs; validators reject larger inputs to bound memory and deterministic work.

`public const int GrantedSkillsPerCombatant`

:   Hard cap for granted skills per combatant; validators reject larger inputs to bound memory and deterministic work.

`public const int IndependentStatusStacks`

:   Hard cap for independent status stacks; validators reject larger inputs to bound memory and deterministic work.

`public const long MaximumBattleTicks`

:   Hard cap for maximum battle ticks; validators reject larger inputs to bound memory and deterministic work.

`public const ulong MaximumCompletedRootActions`

:   Hard cap for maximum completed root actions; validators reject larger inputs to bound memory and deterministic work.

`public const int ModifiersPerStatus`

:   Hard cap for modifiers per status; validators reject larger inputs to bound memory and deterministic work.

`public const int PeriodicEffectsPerStatus`

:   Hard cap for periodic effects per status; validators reject larger inputs to bound memory and deterministic work.

`public const int PlannedPrimitivesPerEffect`

:   Hard cap for planned primitives per effect; validators reject larger inputs to bound memory and deterministic work.

`public const int PrimitiveExecutionsPerRootAction`

:   Hard cap for primitive executions per root action; validators reject larger inputs to bound memory and deterministic work.

`public const int PropertiesPerRecord`

:   Hard cap for properties per record; validators reject larger inputs to bound memory and deterministic work.

`public const int PropertyArrayValues`

:   Hard cap for property array values; validators reject larger inputs to bound memory and deterministic work.

`public const int PropertyStringUtf8Bytes`

:   Hard cap for property string utf8 bytes; validators reject larger inputs to bound memory and deterministic work.

`public const int ReactionDefinitions`

:   Hard cap for reaction definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int ReactionMaximumCount`

:   Hard cap for reaction maximum count; validators reject larger inputs to bound memory and deterministic work.

`public const int ReactionMaximumDepth`

:   Hard cap for reaction maximum depth; validators reject larger inputs to bound memory and deterministic work.

`public const int ReactionRulesPerOwner`

:   Hard cap for reaction rules per owner; validators reject larger inputs to bound memory and deterministic work.

`public const int ReadyDecisions`

:   Hard cap for ready decisions; validators reject larger inputs to bound memory and deterministic work.

`public const int RegisteredCommandTypes`

:   Hard cap for registered command types; validators reject larger inputs to bound memory and deterministic work.

`public const int ReplayBytes`

:   Hard cap for replay bytes; validators reject larger inputs to bound memory and deterministic work.

`public const int ReplayCheckpointInterval`

:   Hard cap for replay checkpoint interval; validators reject larger inputs to bound memory and deterministic work.

`public const int ReplayCheckpoints`

:   Hard cap for replay checkpoints; validators reject larger inputs to bound memory and deterministic work.

`public const int ReplayCommands`

:   Hard cap for replay commands; validators reject larger inputs to bound memory and deterministic work.

`public const int RequestedTargetsPerCommand`

:   Hard cap for requested targets per command; validators reject larger inputs to bound memory and deterministic work.

`public const int ResolvedTargetsPerOperation`

:   Hard cap for resolved targets per operation; validators reject larger inputs to bound memory and deterministic work.

`public const int ResourcesPerCombatant`

:   Hard cap for resources per combatant; validators reject larger inputs to bound memory and deterministic work.

`public const int SchedulerDefinitions`

:   Hard cap for scheduler definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int ShieldsPerCombatant`

:   Hard cap for shields per combatant; validators reject larger inputs to bound memory and deterministic work.

`public const int StableIdsPerTaggedArray`

:   Hard cap for stable IDs per tagged array; validators reject larger inputs to bound memory and deterministic work.

`public const int StartRequestBytes`

:   Hard cap for start request bytes; validators reject larger inputs to bound memory and deterministic work.

`public const int StatDefinitions`

:   Hard cap for stat definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int StaticReactionGraphEdges`

:   Hard cap for static reaction graph edges; validators reject larger inputs to bound memory and deterministic work.

`public const int StatusDefinitions`

:   Hard cap for status definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int StatusesPerBattle`

:   Hard cap for statuses per battle; validators reject larger inputs to bound memory and deterministic work.

`public const int StatusesPerCombatant`

:   Hard cap for statuses per combatant; validators reject larger inputs to bound memory and deterministic work.

`public const int TaggedBytes`

:   Hard cap for tagged bytes; validators reject larger inputs to bound memory and deterministic work.

`public const int TagsPerCombatantDefinition`

:   Hard cap for tags per combatant definition; validators reject larger inputs to bound memory and deterministic work.

`public const int Teams`

:   Hard cap for teams; validators reject larger inputs to bound memory and deterministic work.

`public const int TimingTicks`

:   Hard cap for timing ticks; validators reject larger inputs to bound memory and deterministic work.

`public const int TotalCombatants`

:   Hard cap for total combatants; validators reject larger inputs to bound memory and deterministic work.

`public const int ZeroEventReductionsPerCall`

:   Hard cap for zero event reductions per call; validators reject larger inputs to bound memory and deterministic work.

---

## StepActionOutcome

```csharp
public enum StepActionOutcome
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Why one `BattleEngine.StepAction` call stopped. Only
`ActionCompleted` means a root action reached its terminal
boundary.

| Value | Meaning |
| --- | --- |
| `ActionCompleted` | A root action reached its terminal event and every reaction owed before that boundary has drained. |
| `AwaitingCommand` | A human decision was reached before any action began. |
| `RejectedCommand` | A submitted command failed semantic validation. |
| `Terminal` | The battle ended before an action boundary was reached. |
| `NoScheduledWork` | Execution stalled with no future work before an action boundary was reached. |
| `FatalInvariant` | A typed invariant or overflow failure. |

---

## StepActionResult

```csharp
public sealed class StepActionResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Immutable result of one `BattleEngine.StepAction` call: every
event emitted while driving execution to the next action boundary, in
emission order, plus the snapshot at that boundary. Stepping one action
yields the same events, snapshot, and event chain as reaching the same
boundary through individual submit and step calls.

**Properties**

`public FrozenList<AiDecisionTrace> AiDecisionTraces`

:   Non-authoritative AI decision evidence produced by this call alone, accumulated across every reduction it performed. It has been removed from the engine buffer, so `BattleEngine.DrainAiDecisionTraces` will not return it a second time.

`public Diagnostic? Diagnostic`

:   The typed failure. Set only for `StepActionOutcome.FatalInvariant`.

`public FrozenList<BattleEvent> Events`

:   Every event emitted during this call, in emission order. Events produced before the call stopped or failed are still returned, so this can be non-empty for any outcome.

`public FrozenList<FormulaAttributionTrace> FormulaAttributionTraces`

:   Shorthand for `FormulaAttributions.Traces`.

`public FormulaAttributionTraceBatch FormulaAttributions`

:   Non-authoritative formula evidence produced by this call alone, likewise already handed over by the engine.

`public long OmittedFormulaAttributionTraceCount`

:   Shorthand for `FormulaAttributions.OmittedCount`: how many formula traces were produced but dropped to stay inside the documented result-memory bound.

`public StepActionOutcome Outcome`

:   Which boundary the call stopped on. Only `StepActionOutcome.ActionCompleted` means a root action finished, and it covers an action that was interrupted or skipped as well as one that ran to completion, so anything counting actions should count that value alone. The remaining values each report why no action boundary was reached; `Events` may still be non-empty under any of them.

`public BattleSnapshot Snapshot`

:   The authoritative state at the boundary the call stopped on. A reduction that failed is rolled back, so this is never a partially reduced state.

---

## StepEventOutcome

```csharp
public enum StepEventOutcome
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Why one `BattleEngine.StepEvent` call stopped. Exactly one
value is reported per call, and only `EventEmitted` means a new
gameplay event was appended to the authoritative event chain.

| Value | Meaning |
| --- | --- |
| `EventEmitted` | Exactly one new gameplay event was emitted and is carried on the result. |
| `AwaitingCommand` | Execution reached a human decision boundary and the selected input-pause policy permits no further authoritative progress until a command is submitted. |
| `Terminal` | The battle result is terminal and no execution frame remains. |
| `NoScheduledWork` | A valid nonterminal configuration has no future work under its stall policy. |
| `FatalInvariant` | A typed invariant or overflow failure. |

---

## StepEventResult

```csharp
public sealed class StepEventResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Engine/BattleEngine.cs</small>

Immutable result of one `BattleEngine.StepEvent` reduction:
why the call stopped, the single event it emitted, and the authoritative
snapshot that follows it. Holding or reading this result cannot advance
the battle, and the trace collections on it have already been handed
over by the engine, so a later drain will not return them again.

**Properties**

`public FrozenList<AiDecisionTrace> AiDecisionTraces`

:   Non-authoritative AI decision evidence produced by this call alone. It has been removed from the engine buffer, so `BattleEngine.DrainAiDecisionTraces` will not return it a second time.

`public Diagnostic? Diagnostic`

:   The typed failure. Set only for `StepEventOutcome.FatalInvariant`.

`public BattleEvent Event`

:   The single gameplay event this call emitted. Null unless `Outcome` is `StepEventOutcome.EventEmitted`.

`public FrozenList<FormulaAttributionTrace> FormulaAttributionTraces`

:   Shorthand for `FormulaAttributions.Traces`.

`public FormulaAttributionTraceBatch FormulaAttributions`

:   Non-authoritative formula evidence produced by this call alone, likewise already handed over by the engine.

`public long OmittedFormulaAttributionTraceCount`

:   Shorthand for `FormulaAttributions.OmittedCount`: how many formula traces were produced but dropped to stay inside the documented result-memory bound.

`public StepEventOutcome Outcome`

:   Why the call stopped. Read this before anything else on the result: only `StepEventOutcome.EventEmitted` means `Event` is populated and the authoritative event chain grew, and only `StepEventOutcome.FatalInvariant` means `Diagnostic` is set.

`public BattleSnapshot Snapshot`

:   The authoritative state after the reduction. On `StepEventOutcome.FatalInvariant` the failed reduction is rolled back, so this is the last valid snapshot instead.

---
