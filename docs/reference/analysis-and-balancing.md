# Analysis and balancing

13 types in this area.

!!! abstract "On this page"
    [AnalysisDiagnosticIds](#analysisdiagnosticids) &middot; [AnalysisLimits](#analysislimits) &middot; [BatchExport](#batchexport) &middot; [BatchOutcomeKind](#batchoutcomekind) &middot; [BatchSeedPlan](#batchseedplan) &middot; [BattleBatchAggregate](#battlebatchaggregate) &middot; [BattleBatchLimits](#battlebatchlimits) &middot; [BattleBatchRequest](#battlebatchrequest) &middot; [BattleBatchResult](#battlebatchresult) &middot; [BattleBatchRunner](#battlebatchrunner) &middot; [BattleOutcomeRecord](#battleoutcomerecord) &middot; [SingleBattleReproduction](#singlebattlereproduction) &middot; [TeamWinCount](#teamwincount)

## AnalysisDiagnosticIds

```csharp
public static class AnalysisDiagnosticIds
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/AnalysisDiagnostics.cs</small>

Permanent diagnostic identifiers for analysis batch contract 1. These
IDs never change once shipped; new failure modes receive new IDs.

**Fields**

`public static readonly StableId ReproductionDivergence`

:   A failing-seed rerun did not reproduce the batch record.

`public static readonly StableId RequestInvalid`

:   A batch request member is null, empty, out of range, or inconsistent.

`public static readonly StableId StartRequiresAutomatic`

:   The start request contains a human-controlled combatant.

---

## AnalysisLimits

```csharp
public static class AnalysisLimits
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

Structural limits for analysis batch contract 1. Caps are checked with
checked arithmetic before any dependent allocation.

**Fields**

`public const int BatchWorkers`

:   The largest worker count `BattleBatchRunner.RunParallel` accepts.

`public const int CancellationPollRootActionInterval`

:   The ceiling on `BattleBatchLimits.CancellationPollRootActionInterval`.

`public const int DefaultCancellationPollRootActionInterval`

:   The cancellation poll interval a default-constructed `BattleBatchLimits` uses.

`public const int DefaultRootActionsPerBattle`

:   The root-action limit a default-constructed `BattleBatchLimits` uses.

`public const long DefaultTicksPerBattle`

:   The tick limit a default-constructed `BattleBatchLimits` uses.

`public const int RootActionsPerBattle`

:   The ceiling on `BattleBatchLimits.MaximumRootActionsPerBattle`.

`public const int SeedsPerBatch`

:   The most seeds one `BatchSeedPlan` may carry.

`public const long TicksPerBattle`

:   The ceiling on `BattleBatchLimits.MaximumTicksPerBattle`.

---

## BatchExport

```csharp
public static class BatchExport
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchExport.cs</small>

Deterministic CSV and JSON text generation for batch results. Export is
text only; no file dialog, path choice, or I/O lives in this assembly.
Both encoders use invariant culture, `\n` line endings, and ASCII
output, so equal results export byte-identically across cultures,
platforms, and worker counts.

**Methods**

`public static string WriteCsv(BattleBatchResult result)`

:   Encodes one batch result as CSV: a fixed header line, then one line per record in the order `BattleBatchResult.Records` holds them, which is ascending by seed. A result carrying an aggregate then gets one `# aggregate name=value` comment line per aggregate field, so the reduction travels with the records in the same file.

    - `result` &mdash; The result to encode. A failed or cancelled result exports the records it does have and no aggregate block, because it has none.
    - **Returns** &mdash; The CSV text. Every line, the last one included, ends with a single `\n`. Per-record engine diagnostics are not exported, which is what lets two runs of the same request compare byte for byte.

`public static string WriteJson(BattleBatchResult result)`

:   Encodes one batch result as a single JSON object: the format version, the succeeded and cancelled flags, the records in the same seed order the CSV uses, and the aggregate. The aggregate member is always present and is JSON null when the result has none.

    - `result` &mdash; The result to encode.
    - **Returns** &mdash; The JSON text, ASCII only: any character outside printable ASCII is escaped as a `\uXXXX` sequence rather than emitted directly. It carries the same fields as the CSV and likewise omits per-record engine diagnostics.

---

## BatchOutcomeKind

```csharp
public enum BatchOutcomeKind
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

The recorded stop reason of one batch battle.

| Value | Meaning |
| --- | --- |
| `Terminal` | The engine reached a terminal battle result. |
| `RootActionLimit` | The completed root-action count reached `BattleBatchLimits.MaximumRootActionsPerBattle`. |
| `TickLimit` | The tick reached `BattleBatchLimits.MaximumTicksPerBattle`. |
| `CommandLimit` | The engine's bounded recorded-command history reached its cap, so the battle stopped before the next command could trip an invariant. |
| `NoScheduledWork` | The engine ran out of scheduled work without reaching a terminal result. |
| `FatalInvariant` | The engine could not complete a step. |

---

## BatchSeedPlan

```csharp
public sealed class BatchSeedPlan
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

An immutable deduplicated ascending seed list. Construction failures
(negative counts, ranges that would wrap past UInt32.MaxValue, and the
65,536-seed cap) are retained on the plan and surfaced as the typed
`analysis.request.invalid` failure through the batch request gate
instead of throwing.

**Properties**

`public FrozenList<uint> Seeds`

:   The planned seeds, ascending and free of duplicates, one battle per entry. It is empty when planning failed, and the batch request gate rejects an empty plan rather than running a batch of no battles.

**Methods**

`public static BatchSeedPlan FromRange(uint firstSeed, int count)`

:   Plans the ascending run of consecutive seeds that starts at `firstSeed`.

    - `firstSeed` &mdash; The lowest seed in the run.
    - `count` &mdash; How many consecutive seeds to plan. Must be at least 1 and at most `AnalysisLimits.SeedsPerBatch`.
    - **Returns** &mdash; The planned seeds, or an empty plan carrying the retained failure detail when the count is out of range or the run would pass `uint.MaxValue`. This method never throws.

`public static BatchSeedPlan FromSeeds(IEnumerable<uint> seeds)`

:   Plans arbitrary seeds, dropping duplicates and sorting the rest ascending, so the plan never depends on enumeration order.

    - `seeds` &mdash; The seeds to plan; repeated values collapse to one.
    - **Returns** &mdash; The deduplicated ascending plan, or an empty plan carrying the retained failure detail when more than `AnalysisLimits.SeedsPerBatch` distinct seeds arrive. An empty sequence yields an empty plan, which the batch request gate then rejects.

---

## BattleBatchAggregate

```csharp
public sealed class BattleBatchAggregate
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

The deterministic single-threaded ordered reduction over the sorted
records of one completed batch.

**Properties**

`public int BattleCount`

:   How many records were reduced, which for a completed batch is every planned seed.

`public int CommandLimitCount`

:   Records that stopped on `BatchOutcomeKind.CommandLimit`, where the engine's bounded recorded-command history filled up before the battle resolved.

`public int ConcessionCount`

:   Records whose terminal result was the engine's concession result.

`public int DrawCount`

:   Records whose terminal result was the engine's draw result.

`public int FatalInvariantCount`

:   Records that stopped on `BatchOutcomeKind.FatalInvariant`. These are the only records carrying `BattleOutcomeRecord.Diagnostic`, and any count above zero is worth reading through before the rest of this reduction is trusted.

`public long MaximumFinalTick`

:   The final tick of the longest battle in the batch. With `MinimumFinalTick` and `TotalFinalTicks` divided by `BattleCount`, it gives the spread and the mean battle length without keeping the records.

`public long MinimumFinalTick`

:   The final tick of the shortest battle in the batch.

`public int NoScheduledWorkCount`

:   Records that stopped on `BatchOutcomeKind.NoScheduledWork`, where the engine had nothing left to schedule and yet no side had won. It points at content that can reach a standstill rather than at a limit being too tight.

`public Sha256Digest RecordSetHash`

:   The batch's portable identity: the SHA-256 over the exported record lines in seed order. Diagnostics are excluded, so the same request hashes identically regardless of worker count.

`public int RootActionLimitCount`

:   Records that stopped on `BatchOutcomeKind.RootActionLimit`. Any count above zero means part of the batch was cut short, so `TeamWins` understates what a longer run would have decided.

`public int StalledCount`

:   Records whose terminal result was the engine's stalled result.

`public FrozenList<TeamWinCount> TeamWins`

:   Wins per team in ascending team-ID order. Teams that won no battle have no entry.

`public int TickLimitCount`

:   Records that stopped on `BatchOutcomeKind.TickLimit`, which reads the same way as `RootActionLimitCount`: unfinished battles, not results.

`public long TotalDamageDealt`

:   Applied health damage summed across every record. Like the per-record total it counts health actually lost, so it tracks how much the batch's damage reached its targets rather than how much it rolled.

`public long TotalFinalTicks`

:   The sum of every record's final tick. This is a total across battles, not the length of any one battle.

`public long TotalHealingDone`

:   Applied healing summed across every record.

`public ulong TotalRootActions`

:   Completed root actions summed across every record. Divided by `BattleCount` it gives the average battle length in actions, which tunes a root-action limit better than tick counts do.

---

## BattleBatchLimits

```csharp
public sealed class BattleBatchLimits
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

Per-battle stopping bounds. Out-of-range values are retained and
surfaced as the typed request-gate failure instead of throwing.

**Constructors**

`public BattleBatchLimits()`

:   Creates the bounds from `AnalysisLimits.DefaultRootActionsPerBattle`, `AnalysisLimits.DefaultTicksPerBattle`, and `AnalysisLimits.DefaultCancellationPollRootActionInterval`, which are well inside every accepted range.

`public BattleBatchLimits(int maximumRootActionsPerBattle, long maximumTicksPerBattle, int cancellationPollRootActionInterval)`

:   Creates per-battle bounds. Values are stored exactly as given; the range check happens in the batch request gate.

    - `maximumRootActionsPerBattle` &mdash; The completed root-action count at which a battle stops and records `BatchOutcomeKind.RootActionLimit`.
    - `maximumTicksPerBattle` &mdash; The tick at which a battle stops and records `BatchOutcomeKind.TickLimit`.
    - `cancellationPollRootActionInterval` &mdash; How many completed root actions may pass between cancellation-token polls inside one battle. Smaller values react to cancellation sooner.

**Properties**

`public int CancellationPollRootActionInterval`

:   Completed root actions between cancellation-token polls inside one battle.

`public int MaximumRootActionsPerBattle`

:   The completed root-action count at which a battle stops and records `BatchOutcomeKind.RootActionLimit`. A battle that has already reached a terminal result is never reinterpreted as a limit stop, so this bounds only battles that would otherwise run on.

`public long MaximumTicksPerBattle`

:   The tick at which a battle stops and records `BatchOutcomeKind.TickLimit`. The bound is tested once per completed root action rather than every tick, so the recorded final tick can sit past this value instead of exactly on it.

---

## BattleBatchRequest

```csharp
public sealed class BattleBatchRequest
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

The complete immutable input of one Monte Carlo batch. Null members are
accepted here and rejected by the request gate with the permanent
`analysis.request.invalid` diagnostic before any battle or thread
starts.

**Constructors**

`public BattleBatchRequest(CompiledBattleContent content, BattleStartRequest startRequest, BattleSchedulerRegistry schedulerRegistry, BattleMechanicsRegistry mechanicsRegistry, BatchSeedPlan seedPlan, BattleBatchLimits limits, CancellationToken cancellationToken)`

:   Captures the batch input as given. Nothing is validated here, so constructing a request never throws and never starts work.

    - `content` &mdash; The compiled content every battle in the batch runs against.
    - `startRequest` &mdash; The start request shared by every battle. Its profile must match `content` and no combatant may be human controlled, or the request gate rejects the batch.
    - `schedulerRegistry` &mdash; The registry battles resolve their scheduler through.
    - `mechanicsRegistry` &mdash; The registry battles resolve their mechanics through.
    - `seedPlan` &mdash; The seeds to run: one battle per planned seed.
    - `limits` &mdash; The per-battle stopping bounds.
    - `cancellationToken` &mdash; Polled between battles and, within a battle, at `BattleBatchLimits.CancellationPollRootActionInterval`.

**Properties**

`public CancellationToken CancellationToken`

:   Polled between battles and, inside a battle, at `BattleBatchLimits.CancellationPollRootActionInterval`. Signalling it keeps the records of the battles that already finished and drops the aggregate, since a partial batch cannot be reduced into one.

`public CompiledBattleContent Content`

:   The compiled content every battle in the batch runs against. Its profile has to match the one on `StartRequest` or the request gate rejects the batch.

`public BattleBatchLimits Limits`

:   The stopping bounds applied to every battle in the batch.

`public BattleMechanicsRegistry MechanicsRegistry`

:   The registry each battle resolves its formulas, effects, targeting, AI, and reactions through.

`public BattleSchedulerRegistry SchedulerRegistry`

:   The registry each battle resolves its scheduler through.

`public BatchSeedPlan SeedPlan`

:   The seeds to run, one battle each.

`public BattleStartRequest StartRequest`

:   The starting position shared by every battle, so the seed is the only thing that differs between them. No combatant may be human controlled, because the batch runner drives battles automatically and never offers a decision.

---

## BattleBatchResult

```csharp
public sealed class BattleBatchResult
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

The complete immutable result of one batch execution. Request-level
failures carry a diagnostic and nothing else; cancelled batches keep
every fully completed record and no aggregate.

**Properties**

`public BattleBatchAggregate Aggregate`

:   The reduction over `Records`, or null when the batch failed or was cancelled.

`public Diagnostic? Diagnostic`

:   The request-gate failure, or null when the batch ran.

`public FrozenList<BattleOutcomeRecord> Records`

:   The fully completed records in ascending seed order, whichever entry point produced them.

`public bool Succeeded`

:   False only when the request gate rejected the batch. A cancelled batch still succeeded.

`public bool WasCancelled`

:   True when cancellation stopped the batch before every planned seed ran.

---

## BattleBatchRunner

```csharp
public sealed class BattleBatchRunner
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BattleBatchRunner.cs</small>

The deterministic scripted AI-versus-AI Monte Carlo runner. Instances
hold no state; `Run` and `RunParallel` are pure
functions of the request, and for the same request both produce
byte-identical records, aggregate, record-set hash, CSV, and JSON
regardless of worker count, scheduling, or processor count.

**Methods**

`public BattleBatchResult Run(BattleBatchRequest request)`

:   Runs every planned seed synchronously on the caller thread.

    - `request` &mdash; The batch to run. Null, a null member, and every other invalid input are reported through the returned result rather than thrown.
    - **Returns** &mdash; A completed result carrying the records and their aggregate; a failed result carrying only the request-gate diagnostic when the request is rejected; or, if the token is signalled partway, a succeeded but cancelled result holding the seeds that finished and no aggregate.

`public BattleBatchResult RunParallel(BattleBatchRequest request, int workerCount)`

:   Runs the planned seeds on worker threads owned by this call. Workers execute whole battles only, share no mutable state, and deliver completed immutable records that are merged and sorted by seed before the single-threaded ordered aggregation.

    - `request` &mdash; The batch to run, gated exactly as `Run` gates it.
    - `workerCount` &mdash; Threads to start. It must be between 1 and `AnalysisLimits.BatchWorkers` or the request gate rejects the batch, and it is lowered to the planned seed count when it exceeds it. It changes only how long the batch takes, never its result.
    - **Returns** &mdash; The same three shapes `Run` returns, for the same reasons.

`public SingleBattleReproduction RunSingleForReproduction(BattleBatchRequest request, uint seed)`

:   Reruns one seed through the identical per-battle algorithm the batch loop uses and additionally captures the strict replay envelope bytes from the same engine. Invalid requests throw the request-gate diagnostic as an `ArgumentException`; cancellation throws `OperationCanceledException`.

    - `request` &mdash; The batch whose content, start, registries, and limits this rerun uses. Its seed plan still has to pass the gate, but is not consulted.
    - `seed` &mdash; The seed to rerun. It need not be one of the planned seeds, so a single interesting seed can be reproduced from the batch's request.
    - **Returns** &mdash; The record the batch loop would have produced for this seed, together with the replay bytes captured from the very engine that produced it.

---

## BattleOutcomeRecord

```csharp
public sealed class BattleOutcomeRecord : IEquatable<BattleOutcomeRecord>
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

The immutable outcome of one batch battle. Records reference no engine,
snapshot, event list, or trace. The optional `Diagnostic`
exists only on `BatchOutcomeKind.FatalInvariant` records and
is excluded from CSV, JSON, and `RecordSetHash`.

**Constructors**

`public BattleOutcomeRecord(uint seed, BatchOutcomeKind kind, StableId? resultId, StableId? winningTeamId, StableId? losingTeamId, long finalTick, ulong completedRootActions, int eventCount, long totalDamageDealt, long totalHealingDone, int survivingCombatants, Sha256Digest finalStateHash, Sha256Digest finalEventChainHash, Diagnostic? diagnostic)`

:   Creates a record and enforces its pairing invariants: a result ID exists exactly on `BatchOutcomeKind.Terminal` records, team result IDs require that result ID, counters are nonnegative, both hashes are valid, and only fatal-invariant records carry a diagnostic.

    - `seed` &mdash; The batch seed this battle ran with.
    - `kind` &mdash; Why the battle stopped.
    - `resultId` &mdash; The engine's terminal result ID, or null when the battle stopped for any other reason.
    - `winningTeamId` &mdash; The winning team, or null when the result decided none.
    - `losingTeamId` &mdash; The losing team, or null when the result decided none.
    - `finalTick` &mdash; The tick the battle stopped on.
    - `completedRootActions` &mdash; Root actions the battle finished before stopping.
    - `eventCount` &mdash; How many events the battle emitted. The events themselves are not retained.
    - `totalDamageDealt` &mdash; Applied health damage as a nonnegative total.
    - `totalHealingDone` &mdash; Applied healing as a nonnegative total.
    - `survivingCombatants` &mdash; Combatants still above zero health when the battle stopped.
    - `finalStateHash` &mdash; The state hash of the stopping snapshot.
    - `finalEventChainHash` &mdash; The event-chain hash of the stopping snapshot.
    - `diagnostic` &mdash; The engine diagnostic, allowed only when `kind` is `BatchOutcomeKind.FatalInvariant`.

**Properties**

`public ulong CompletedRootActions`

:   Root actions that finished resolving before the battle stopped. Reactions and anything else nested under a root action do not add to it, and it is the counter `BattleBatchLimits.MaximumRootActionsPerBattle` is tested against.

`public Diagnostic? Diagnostic`

:   The engine diagnostic explaining the stop; null on every kind other than `BatchOutcomeKind.FatalInvariant`. It is left out of CSV, JSON, and the record-set hash, so diagnostic text can never change a batch's exported identity.

`public int EventCount`

:   How many events the battle emitted in total. The events themselves are not retained anywhere on the record, so this is all that survives of them.

`public Sha256Digest FinalEventChainHash`

:   The rolling event-chain hash at the stopping snapshot. It covers the path the battle took rather than where it ended, so two runs that emitted any differing event differ here even when their final states match.

`public Sha256Digest FinalStateHash`

:   The canonical state hash of the snapshot the battle stopped on. Two runs that agree here agree on the entire final state, which is what makes a batch comparable across machines and worker counts.

`public long FinalTick`

:   The tick of the snapshot the battle stopped on, which is how long the battle lasted in simulation time.

`public BatchOutcomeKind Kind`

:   Why the battle stopped. Only `BatchOutcomeKind.Terminal` records reached a battle result; every other kind stopped on a configured bound or a fault, so their totals describe an unfinished battle.

`public StableId? LosingTeamId`

:   The losing team, or null when the result named none, as a draw or a stalled battle does.

`public StableId? ResultId`

:   The engine's terminal result ID; null unless `Kind` is `BatchOutcomeKind.Terminal`.

`public uint Seed`

:   The batch seed this battle ran with. It is the record's identity: records are sorted by it, and rerunning the same request with the same seed reproduces this battle exactly.

`public int SurvivingCombatants`

:   Combatants above zero health when the battle stopped, counted across every team rather than per team.

`public long TotalDamageDealt`

:   The battle's applied health damage as a nonnegative total, summed from the resolved-damage events as the health actually lost rather than the amount the formula produced.

`public long TotalHealingDone`

:   The battle's applied healing as a nonnegative total, summed from the resolved-healing events as the health actually restored.

`public StableId? WinningTeamId`

:   The winning team, or null when the result named none, as a draw or a stalled battle does.

**Methods**

`public bool Equals(BattleOutcomeRecord other)`

:   Value comparison across the whole record.

    - `other` &mdash; The record to compare with; null is never equal.
    - **Returns** &mdash; True when every recorded member matches, the diagnostic included.

`public override bool Equals(object obj)`

:   Value comparison with any object; only another record can be equal.

    - `obj` &mdash; The object to compare with.
    - **Returns** &mdash; True when `obj` is a record with matching members.

`public override int GetHashCode()`

:   Hashes the seed, kind, final tick, and both final hashes only. It stays consistent with `Equals(BattleOutcomeRecord)` without visiting every member.

    - **Returns** &mdash; A deterministic hash code for this value.

---

## SingleBattleReproduction

```csharp
public sealed class SingleBattleReproduction
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

A single-seed rerun derived by the exact batch per-battle algorithm plus
the strict replay bytes captured from the same engine.

**Properties**

`public BattleOutcomeRecord Record`

:   The outcome the batch loop would have recorded for this seed. It comes from the same per-battle algorithm the batch uses, so it can be compared field for field with the batch's own record for that seed.

`public byte[] ReplayBytes`

:   The captured replay envelope. Every read returns a fresh copy, so the stored bytes cannot be mutated and repeated reads allocate.

---

## TeamWinCount

```csharp
public sealed class TeamWinCount
```

`TurnGauge.Analysis` &middot; <small>Runtime/Analysis/BatchContracts.cs</small>

One winning team and how many batch records it won.

**Properties**

`public StableId TeamId`

:   The team the counted battles named as winner.

`public int Wins`

:   How many records in the batch named this team the winner. It is always at least one, because a team that won nothing gets no entry at all rather than a zero.

---
