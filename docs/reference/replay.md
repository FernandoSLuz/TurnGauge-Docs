# Replay

10 types in this area.

!!! abstract "On this page"
    [IReplayMigration](#ireplaymigration) &middot; [ReplayDivergenceHashKind](#replaydivergencehashkind) &middot; [ReplayEnvelope](#replayenvelope) &middot; [ReplayExecutionResult](#replayexecutionresult) &middot; [ReplayExecutor](#replayexecutor) &middot; [ReplayMigrationChain](#replaymigrationchain) &middot; [ReplayMigrationResult](#replaymigrationresult) &middot; [ReplayReadResult](#replayreadresult) &middot; [ReplaySerializer](#replayserializer) &middot; [ReplayWriteException](#replaywriteexception)

## IReplayMigration

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IReplayMigration
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayMigration.cs</small>

One step of a replay upgrade: it takes the bytes of a replay written in
`FromFormatVersion` and returns the same replay written in
`ToFormatVersion`. Implement one for each older replay format
version you still need to load, then hand the set to a
`ReplayMigrationChain`, which is what runs the steps in order.

A step must advance exactly one version and must not skip: the chain
rejects anything else when it is constructed. It must also be
deterministic and must produce the canonical byte form for the target
version, because `ReplaySerializer` re-encodes what it reads
and refuses a replay that is valid JSON but not the canonical
representation of its declared format. Treat the argument as read-only and
return a new array; never return null, never report success without bytes,
and never report failure without a diagnostic, or the chain aborts the
whole run with `replay.migration.invalid-result`.

**Properties**

`public int FromFormatVersion`

:   The replay format version this step reads. Must be 1 or greater.

`public int ToFormatVersion`

:   The replay format version this step writes. Must be exactly `FromFormatVersion` plus one.

**Methods**

`public ReplayMigrationResult Migrate(byte[] immutableInput)`

:   Rewrites one replay from `FromFormatVersion` to `ToFormatVersion`.
    - `immutableInput` &mdash; The replay bytes as they exist at `FromFormatVersion`. The caller owns this array; read it, do not write to it.
    - **Returns** &mdash; A success carrying the rewritten bytes, or a failure carrying the diagnostic that explains the refusal. Never null.

---

## ReplayDivergenceHashKind

```csharp
public enum ReplayDivergenceHashKind : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayExecutor.cs</small>

Which pair of hashes disagreed when a replay diverged. It tells a caller
what the expected and actual hashes on a failed
`ReplayExecutionResult` are comparing, which is what narrows
a divergence down to a cause.

| Value | Meaning |
| --- | --- |
| `None` | The failure carries no hash pair: replay stopped for a structural reason rather than a mismatch. |
| `CommandEvent` | The event hash of a recorded command. |
| `State` | The canonical battle-state hash at a checkpoint. |
| `EventChain` | The running event-chain hash at a checkpoint. |
| `PreCommandState` | The state hash recorded immediately before a command was submitted. |

---

## ReplayEnvelope

```csharp
public sealed class ReplayEnvelope
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayEnvelope.cs</small>

A complete, portable recording of one battle: the contract profile it ran under,
the hashed compiled content and start request, the RNG seed, every recorded
command, and the checkpoints that pin the expected state and event-chain hashes.

Feeding one back through `ReplayExecutor` re-runs the battle and
verifies it against those checkpoints, reporting the exact point of divergence if
the outcome differs. An envelope is immutable and holds no engine reference, so it
can be serialized with `ReplaySerializer` and verified on another
machine. Obtain one from `Capture(BattleEngine)` or from
`ReplaySerializer.Read(byte[])`.

**Properties**

`public int? AiRegistryVersion`

:   Version of the AI contract that chose commands for automatic combatants, or null under a profile with no mechanics registry. Those decisions are recorded as commands, so a replay reproduces them without re-running the policy that made them.

`public int CanonicalVersion`

:   Version of the canonical encoding the embedded snapshot and start request are written in. `CompiledSnapshotHash` and `StartRequestHash` are taken over exactly those bytes, so a change here moves them even when the content itself is unchanged.

`public FrozenList<ReplayCheckpoint> Checkpoints`

:   Periodic checkpoints taken at a fixed recorded-command interval, used to catch divergence part-way through rather than only at the end. May be empty on a short battle; `FinalCheckpoint` is separate and always present.

`public int CommandVersion`

:   Version of the command contract, which governs how each entry of `Commands` is encoded and fed back to the engine on playback.

`public FrozenList<RecordedCommand> Commands`

:   Every command recorded during the battle in submission order, rejected ones included: a rejection still consumes a command sequence, so replaying only the accepted commands would not reproduce the battle.

`public int CompiledSchemaVersion`

:   Version of the compiled-content schema the embedded snapshot was written in. Reading compares the decoded content's own schema version against it and refuses a replay whose payload disagrees with its header.

`public byte[] CompiledSnapshot`

:   The canonically encoded compiled content. Each access returns a fresh copy, so mutating the array cannot corrupt the envelope - and reading it in a loop allocates each time.

`public Sha256Digest CompiledSnapshotHash`

:   Digest of the `CompiledSnapshot` bytes exactly as stored. Reading recomputes it and stops before decoding on a mismatch, which is what separates a corrupted file from one that is merely incompatible.

`public Sha256Digest ContentManifestHash`

:   Identity of the compiled content the battle ran against - a profile-tagged hash rather than a plain digest of the stored bytes. Capture requires the live snapshot to carry the same value and reading recomputes it from the decoded content, so a replay cannot be paired with content it was not recorded against.

`public CompiledBattleContent DecodedContent`

:   The compiled content already decoded from `CompiledSnapshot`, so running or inspecting a replay does not have to decode it again.

`public BattleStartRequest DecodedStartRequest`

:   The start request already decoded from `StartRequest`, the counterpart to `DecodedContent`.

`public int? EffectRegistryVersion`

:   Version of the effect contract that applied the recorded effect entries, or null under a profile with no mechanics registry.

`public int EngineVersion`

:   Version of the engine's stepping behaviour that produced the recording. This and every version below are checked as a set: reading resolves the whole tuple back to a known profile and rejects any combination it does not recognise, rather than loading a replay it would step differently.

`public int EventVersion`

:   Version of the battle-event contract. Events themselves are not stored: playback re-derives them and folds them into the event-chain hash that `FinalCheckpoint` is compared against.

`public int ExecutionVersion`

:   Version of the execution contract, which governs how an accepted command is turned into ordered frames and stepped.

`public ReplayCheckpoint FinalCheckpoint`

:   The expected end state: tick, last event sequence, state hash, and event-chain hash the replay must reach for verification to pass.

`public int FormatVersion`

:   Layout of the serialized replay document. It is written first and read first, and `ReplaySerializer` dispatches on it to pick which body to parse, so it is the one number that has to be understood before any of the rest of a file can be.

`public int? FormulaRegistryVersion`

:   Version of the formula contract that produced the recorded damage, hit, and critical results, or null under a profile with no mechanics registry.

`public int NumericVersion`

:   Version of the fixed-point arithmetic the battle computed with, covering `Fixed64` and `Chance64`.

`public SimulationContractProfile Profile`

:   The contract profile the recorded battle ran under. Every version number below is read from it, and capture requires the engine, its content, its start request, and its snapshot to all share this exact profile.

`public int? ReactionRegistryVersion`

:   Version of the reaction contract that decided when intrinsic reactions triggered, or null under a profile with no mechanics registry.

`public Sha256Digest RegistryBindingHash`

:   Identity of the mechanics implementations the content was bound to. Only meaningful for the B3 profile; the default digest for earlier profiles, which have no mechanics registry to bind.

`public int RngVersion`

:   Version of the deterministic random source. It fixes how `Seed` is expanded and how draws are taken, so the same seed under a different value would produce a different sequence.

`public int? SchedulerVersion`

:   Version of the scheduler contract, or null under a profile that has no scheduler. Where it is present, the scheduler is found in `BattleSchedulerRegistry` by ID and contract version together, so a scheduler that has since moved version will not be handed an old recording to reinterpret.

`public uint Seed`

:   The seed the battle's random source was built from. Playback re-creates the engine with it, so it is what makes the recorded commands roll the same way again; it is stored in the file as fixed-width hexadecimal so the text form cannot vary by culture.

`public byte[] StartRequest`

:   The canonically encoded start request. Each access returns a fresh copy, as with `CompiledSnapshot`.

`public Sha256Digest StartRequestHash`

:   Digest of the `StartRequest` bytes exactly as stored, checked on read in the same way as `CompiledSnapshotHash`.

`public int? TargetRegistryVersion`

:   Version of the targeting contract that resolved which combatants each skill hit, or null under a profile with no mechanics registry.

**Methods**

`public static ReplayEnvelope Capture(BattleEngine engine)`

:   Records the engine's battle as it stands right now, using the engine's own scheduler registry. Capture only reads the engine - it does not advance, reset, or otherwise disturb the battle, so it is safe to call mid-battle and again later. It fails closed rather than handing back a replay that cannot be trusted: it throws if the engine, content, start request, and snapshot profiles disagree, if the snapshot's content identity does not match the engine's content, or if the battle already exceeds the portable replay command, checkpoint, or byte limits.
    - `engine` &mdash; The engine to record. Must not be null.
    - **Returns** &mdash; An immutable recording that `ReplaySerializer.Write` is already known to accept.

`public static ReplayEnvelope Capture()`

:   Records the engine's battle using an explicitly supplied scheduler registry instead of the engine's own. Behaves exactly as `Capture(BattleEngine)` otherwise.
    - `engine` &mdash; The engine to record. Must not be null.
    - `schedulerRegistry` &mdash; The registry used to hash scheduler state into the final checkpoint under the B2 profile. Must not be null. Pass the same registry the battle was run with, or the recorded state hash will not match on playback.
    - **Returns** &mdash; An immutable recording that `ReplaySerializer.Write` is already known to accept.

---

## ReplayExecutionResult

```csharp
public sealed class ReplayExecutionResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayExecutor.cs</small>

The verdict of one replay run: whether the recording reproduced, the
state the run ended on, and, when it did not reproduce, the exact command
or checkpoint it stopped at and the hashes that disagreed there. A
divergence is reported here rather than thrown, so a caller can inspect
the failing state.

**Properties**

`public Sha256Digest? ActualHash`

:   The hash this run produced. Null when it could not be computed, which happens when the run never reached the boundary being checked.

`public FrozenList<AiDecisionTrace> AiDecisionTraces`

:   Consumer-owned decision evidence produced while replay execution revalidated automatic commands. It is intentionally outside the canonical battle state and replay hashes.

`public int CheckpointIndex`

:   How many of the recording's periodic checkpoints had already been verified when the run diverged. Minus one on success.

`public int CommandIndex`

:   Index into the recording's commands that the run was processing when it diverged, or the command count when it diverged after the last one. Minus one on success.

`public Diagnostic? Diagnostic`

:   Null on success. On failure, the replay-divergence diagnostic whose detail names what was being verified and, when hashes are involved, spells them out.

`public Sha256Digest? ExpectedHash`

:   The hash the recording holds. Null when the failure carries none.

`public FrozenList<FormulaAttributionTrace> FormulaAttributionTraces`

:   The traces held by `FormulaAttributions`, for callers that only want the list.

`public FormulaAttributionTraceBatch FormulaAttributions`

:   Consumer-owned formula evidence gathered while the run re-evaluated the recording, bounded so a long replay cannot grow it without limit. Like the decision traces, it sits outside the canonical battle state and the replay hashes.

`public ReplayDivergenceHashKind HashKind`

:   What `ExpectedHash` and `ActualHash` compare, and None when the failure carries no hash pair.

`public long OmittedFormulaAttributionTraceCount`

:   How many formula traces were dropped because the run produced more than the batch can hold. Non-zero means the traces are a partial record; it never means the replay itself diverged.

`public BattleSnapshot Snapshot`

:   State the run ended on: the reproduced final state on success, or the state at the point of divergence on failure.

`public bool Succeeded`

:   True when the recording reproduced exactly. False means the run diverged, and `CommandIndex`, `CheckpointIndex`, and `Diagnostic` then say where and how, with `Snapshot` holding the state at the point of divergence rather than the recorded final state.

---

## ReplayExecutor

```csharp
public static class ReplayExecutor
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayExecutor.cs</small>

Re-runs a recorded battle from its seed and its recorded commands and
reports whether it reproduced. Verification is exact: every recorded
command's event hash, every periodic checkpoint crossed along the way, and
the final checkpoint's state and event-chain hashes must all match, and
the run stops at the first thing that does not. The recording is only
read, never altered.

!!! note "Remarks"
    Recordings in the earliest format did not store exact submission
    boundaries, so that branch infers them; later formats are driven to the
    recorded tick, event sequence, and pre-command state hash before each
    command is submitted. A divergence comes back as a failed result rather
    than an exception.

**Methods**

`public static ReplayExecutionResult Execute(ReplayEnvelope replay)`

:   Executes a replay against fresh registries holding only the built-in schedulers and mechanics. Use an overload that takes registries when the recording references custom implementations, because a built-in registry cannot resolve them.
    - `replay` &mdash; The recording to reproduce.
    - **Returns** &mdash; Success with the reproduced final state, or the first divergence.

`public static ReplayExecutionResult Execute()`

:   Executes a replay with a caller-supplied scheduler registry, and built-in mechanics.
    - `replay` &mdash; The recording to reproduce.
    - `schedulerRegistry` &mdash; Registry the recording's scheduler is resolved and its state decoded through. It must contain the scheduler the recording was made with.
    - **Returns** &mdash; Success with the reproduced final state, or the first divergence.

`public static ReplayExecutionResult Execute()`

:   Executes a replay with both registries supplied. This is the overload to use for any game that registered its own formulas, effects, targeting, AI, reactions, or schedulers: reproducing a recording requires the same implementations under the same IDs and contract versions it was recorded against.
    - `replay` &mdash; The recording to reproduce.
    - `schedulerRegistry` &mdash; Registry the recording's scheduler is resolved and its state decoded through.
    - `mechanicsRegistry` &mdash; Registry the recording's mechanics implementations are resolved through. Still required for the earliest recording format, which has no mechanics to resolve.
    - **Returns** &mdash; Success with the reproduced final state, or the first divergence.

---

## ReplayMigrationChain

```csharp
public sealed class ReplayMigrationChain
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayMigration.cs</small>

A validated set of single-version `IReplayMigration` steps that
lifts replay bytes from the format version they were written in up to a
newer one, feeding each step's output into the next. Use it before
`ReplaySerializer`.Read, which accepts only the format versions
this build knows and otherwise fails with `replay.incompatible`.

The chain is checked once, when it is built, and is immutable afterwards:
registration throws for a step that skips a version or repeats a version
another step already starts from. A hole between two registered steps is
not caught there, and neither is a step that misbehaves; both are reported
as a failed `ReplayMigrationResult` when a run needs them.

**Constructors**

`public ReplayMigrationChain(IEnumerable<IReplayMigration> migrations)`

:   Copies and validates the steps the chain will run.
    - `migrations` &mdash; The steps, in any order; the chain sorts them by origin version itself. Every entry must be non-null, must start at version 1 or higher, and must advance exactly one version, and no two entries may start at the same version. Anything else throws `ArgumentException`. A version no entry covers is allowed here and surfaces only when a run reaches it.

**Methods**

`public ReplayMigrationResult Migrate(byte[] immutableInput, int fromVersion, int targetVersion)`

:   Runs one step per version from `fromVersion` up to `targetVersion`, passing each step's output to the next. Stops at the first failure and returns it unchanged.
    - `immutableInput` &mdash; The replay bytes as they exist at `fromVersion`. Copied before the first step, so this array is never written to.
    - `fromVersion` &mdash; The format version the bytes are currently in. Must be 1 or greater.
    - `targetVersion` &mdash; The format version to reach. Equal to `fromVersion` runs no step and succeeds with an unchanged copy; lower than it is refused, as migrations only move forward.
    - **Returns** &mdash; A success carrying the bytes at `targetVersion`; the failure a step reported; `replay.migration.missing` when the range is invalid or no step covers a version in it; or `replay.migration.invalid-result` when a step returned null, or claimed success without bytes, or claimed failure without a diagnostic.

---

## ReplayMigrationResult

```csharp
public sealed class ReplayMigrationResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayMigration.cs</small>

The outcome of one migration step, or of a whole
`ReplayMigrationChain` run: either the rewritten replay bytes
or the diagnostic explaining the refusal, never both. The buffer is copied
on the way in and on every read, so neither the array you passed in nor the
array you read out can be used to edit the result afterwards.

**Properties**

`public byte[] Bytes`

:   The migrated replay bytes, and null unless `Succeeded` is true. Every read hands back a fresh copy, so read it once and keep the reference rather than reading it inside a loop.

`public Diagnostic? Diagnostic`

:   Why the migration was refused. Carries a value only on failure.

`public bool Succeeded`

:   True when the rewrite produced bytes. Exactly one of `Bytes` and `Diagnostic` is ever populated, so this decides which of the two to read; a chain run reports the first step that refused, not a partially migrated replay.

**Methods**

`public static ReplayMigrationResult Failure(Diagnostic diagnostic)`

:   Reports a migration that could not be performed. Throws `ArgumentException` for a default-constructed diagnostic, because a failure a caller cannot identify is worse than none.
    - `diagnostic` &mdash; Valid machine-readable reason migration could not produce a complete target-version replay.
    - **Returns** &mdash; A failed result carrying no byte payload and preserving the supplied diagnostic.

`public static ReplayMigrationResult Success(byte[] bytes)`

:   Reports a migration that produced `bytes`, which are copied into the result. Throws `ArgumentNullException` when they are null; a success can never carry a null buffer.
    - `bytes` &mdash; The canonical byte payload to read.
    - **Returns** &mdash; A successful result that owns a defensive copy of the non-null canonical target-version bytes.

---

## ReplayReadResult

```csharp
public sealed class ReplayReadResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplayEnvelope.cs</small>

The outcome of parsing a replay. Exactly one side is populated: on success
`Replay` is set and `Diagnostic` is null, and on failure the
reverse. A malformed, non-canonical, or version-incompatible replay is reported
through this result rather than thrown, so loading a replay file that came from
outside your build does not need a try/catch.

**Properties**

`public Diagnostic? Diagnostic`

:   The reason parsing failed, or null when `Succeeded` is true.

`public ReplayEnvelope Replay`

:   The parsed replay, or null when `Succeeded` is false.

`public bool Succeeded`

:   Whether the replay parsed. Test it before touching `Replay`: a malformed, non-canonical, or version-incompatible file arrives here as false rather than as a thrown exception.

---

## ReplaySerializer

```csharp
public static class ReplaySerializer
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/ReplaySerializer.cs</small>

Writes and reads the portable replay document that carries a battle's compiled content, start
request, seed, and recorded command history as UTF-8 JSON.
The encoding is canonical rather than merely valid: for a given replay there is exactly one legal
byte sequence, and a read re-encodes whatever it parsed and rejects the input when the bytes
differ. A file that has been reformatted, reordered, or hand-edited is therefore refused instead of
quietly loaded, which is what lets two machines agree that they are replaying the same battle.

**Fields**

`public const int MaximumReplayBytes`

:   Largest accepted or emitted canonical replay document in UTF-8 bytes; readers reject larger input before parsing it.

**Methods**

`public static ReplayReadResult Read(byte[] utf8)`

:   Reads a replay against a registry of the built-in mechanics only. A replay whose compiled content binds a custom formula, effect, targeting rule, AI policy, or reaction cannot be resolved from the built-ins and will come back as a failure; pass the registry those implementations were registered in to the other overload instead.
    - `utf8` &mdash; The replay document, as canonical UTF-8 JSON bytes.
    - **Returns** &mdash; The decoded replay on success, or a failure carrying the diagnostic that rejected it.

`public static ReplayReadResult Read()`

:   Decodes a replay and verifies it end to end: the version tuple must resolve to a known contract profile, both embedded payloads must match their recorded hashes and their own canonical encodings, the content manifest and registry binding digests must agree with the compiled content, and the command and checkpoint history must be complete and in order. The document is then re-encoded and compared against the input bytes. A rejected replay is returned as an unsuccessful result rather than thrown, so a project loading a file it did not produce - a shared bug report, a leaderboard submission, an older build's save - can inspect the diagnostic and carry on without guarding the call.
    - `utf8` &mdash; The replay document, as canonical UTF-8 JSON bytes.
    - `mechanicsRegistry` &mdash; Registry the embedded compiled content's mechanics bindings are resolved through. It must contain every implementation the replay was recorded with, at the contract versions it recorded.
    - **Returns** &mdash; The decoded replay, together with the content and start request it embedded, on success; otherwise a failure carrying the diagnostic that rejected it.

`public static byte[] Write(ReplayEnvelope replay)`

:   Encodes a replay to its canonical bytes, emitting the field set that matches the replay's contract profile. The replay is checked before it is written, so an internally inconsistent one - a missing periodic checkpoint, a command without its submission boundary, a registry digest that does not match the embedded content - fails here rather than producing a file that only fails when someone tries to load it.
    - `replay` &mdash; The replay to encode.
    - **Returns** &mdash; Canonical UTF-8 JSON, never longer than `MaximumReplayBytes`.

---

## ReplayWriteException

```csharp
public sealed class ReplayWriteException : InvalidOperationException
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Replay/StrictJson.cs</small>

Thrown when a replay cannot be written out: its contract profile is unsupported or disagrees with
the content it embeds, a field that profile requires is absent, the recorded history breaks a
portability limit, or the encoded document is too large.
It derives from `InvalidOperationException` because the fault is in the replay handed
over rather than in the arguments of the call, and it carries a `Diagnostic` so callers
can branch on the reason instead of matching on the message text.

**Constructors**

`public ReplayWriteException(StableId diagnosticId, string message)`

:   Creates the exception and pairs its message with the diagnostic ID that classifies it.
    - `diagnosticId` &mdash; Identifies the class of failure. Must be a valid ID.
    - `message` &mdash; Explanation for a human reader. It is also kept as the diagnostic's detail, so the two never drift apart.

**Properties**

`public Diagnostic Diagnostic`

:   The machine-readable reason, pairing the ID this was constructed with against its message. Replay reading re-encodes what it parsed and reports any write failure through this same value, so a caller sees the identical reason whether it caught the exception or inspected a failed read result.

---

