# Compiling and validating content

13 types in this area.

!!! abstract "On this page"
    [AuthoringCompileOptions](#authoringcompileoptions) &middot; [AuthoringCompileRequest](#authoringcompilerequest) &middot; [AuthoringCompileResult](#authoringcompileresult) &middot; [AuthoringDiagnostic](#authoringdiagnostic) &middot; [AuthoringDiagnosticSeverity](#authoringdiagnosticseverity) &middot; [AuthoringLimits](#authoringlimits) &middot; [AuthoringValidationReport](#authoringvalidationreport) &middot; [BattleContentCompiler](#battlecontentcompiler) &middot; [BattleRegistryProvider](#battleregistryprovider) &middot; [BattleRegistrySet](#battleregistryset) &middot; [CompiledAuthoringCatalog](#compiledauthoringcatalog) &middot; [CompiledEncounterSnapshot](#compiledencountersnapshot) &middot; [FrozenSortedIndex](#frozensortedindex)

## AuthoringCompileOptions

```csharp
public sealed class AuthoringCompileOptions
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/AuthoringCompileOptions.cs</small>

The two knobs a compile takes: how it can be stopped, and whether warnings
are reported alongside errors. Neither changes the compiled output, so two
compiles of the same catalog under different options still produce the same
content and the same hashes.

**Constructors**

`public AuthoringCompileOptions(CancellationToken cancellationToken = default(CancellationToken), bool includeWarnings = true)`

:   Creates a set of compile options. Both arguments are optional and default to an uncancellable compile that reports warnings.
    - `cancellationToken` &mdash; Polled between compile stages. Useful for an editor import or a batch job over a large catalog, where a compile can take long enough to be worth abandoning.
    - `includeWarnings` &mdash; Whether warnings survive into the reported diagnostics. Errors are kept either way.

**Properties**

`public CancellationToken CancellationToken`

:   The token the compiler polls between stages. Cancelling comes back as an ordinary failed result whose `AuthoringCompileResult.WasCancelled` flag is set, not as a thrown `System.OperationCanceledException`, so a cancelled import is handled on the same path as a catalog that failed to compile.

`public static AuthoringCompileOptions Default`

:   The shared options every compile entry point falls back to when it is handed none: no cancellation, warnings reported. It is immutable and safe to reuse across threads.

`public bool IncludeWarnings`

:   Whether warnings reach the reported diagnostics. Clearing it hides them from the result and nothing more: it does not change what is compiled, and it cannot turn a failing compile into a passing one, because only errors decide that.

---

## AuthoringCompileRequest

:material-star: **Start here**

```csharp
public sealed class AuthoringCompileRequest
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/AuthoringCompileContracts.cs</small>

Everything `BattleContentCompiler` needs for one compile: the
catalog root to read, the scheduler and mechanics registries that authored
references are resolved against, and the compile options. The registries are
passed in rather than discovered, so a catalog naming a custom formula or
scheduler only compiles when you supply the registry it was registered in.
Nothing is validated on construction: a missing catalog or registry becomes a
diagnostic on the result instead of an exception here.

**Constructors**

`public AuthoringCompileRequest(BattleContentCatalog catalog, BattleSchedulerRegistry schedulerRegistry, BattleMechanicsRegistry mechanicsRegistry, AuthoringCompileOptions options = null)`

:   Pins one catalog to explicit scheduler/mechanics registries and compile options. The compiler does not scan assemblies or replace either registry.
    - `catalog` &mdash; The authoring catalog root to compile.
    - `schedulerRegistry` &mdash; Registry each encounter's scheduler reference is resolved against.
    - `mechanicsRegistry` &mdash; Registry every formula, effect, target, AI policy, and reaction reference is resolved against.
    - `options` &mdash; Compile options; null selects `AuthoringCompileOptions.Default`, so `Options` is never null.

**Properties**

`public BattleContentCatalog Catalog`

:   The single root the compile reads. Nothing outside the graph hanging off it is consulted, so an asset that is not reachable from here does not take part however the project is laid out. Null here becomes a compile diagnostic rather than an exception.

`public BattleMechanicsRegistry MechanicsRegistry`

:   Registry every formula, effect, target, AI policy, and reaction reference is resolved against, and the same null rule applies as for `SchedulerRegistry`.

`public AuthoringCompileOptions Options`

:   Cancellation and warning settings for this compile. Never null, because the constructor substitutes `AuthoringCompileOptions.Default`.

`public BattleSchedulerRegistry SchedulerRegistry`

:   Registry the scheduler each encounter names is resolved against. A null registry fails the compile with a diagnostic; it does not quietly fall back to the built-in schedulers.

**Methods**

`public static AuthoringCompileRequest WithBuiltIns(BattleContentCatalog catalog, AuthoringCompileOptions options = null)`

:   Builds a request against freshly created registries holding only the package's built-in schedulers and mechanics. Use the constructor instead once you have registered anything of your own: a catalog that references a custom formula, effect, target, AI policy, reaction, or scheduler will not compile against the built-ins alone.
    - `catalog` &mdash; The authoring catalog root to compile.
    - `options` &mdash; Compile options; null selects `AuthoringCompileOptions.Default`.
    - **Returns** &mdash; A request carrying new built-in registry instances, not shared ones.

---

## AuthoringCompileResult

:material-star: **Start here**

```csharp
public sealed class AuthoringCompileResult
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/AuthoringCompileContracts.cs</small>

The outcome of one compile: either a published `CatalogSnapshot`
or the diagnostics that stopped it, never both and never neither. The
compiler is fail-closed, so a single error discards the whole snapshot rather
than handing back partially compiled content. Cancellation and unexpected
compiler faults arrive here as failed results too, not as exceptions.

**Properties**

`public CompiledAuthoringCatalog CatalogSnapshot`

:   The published catalog, non-null exactly when `Succeeded` is true and null on every failure.

`public FrozenList<AuthoringDiagnostic> Diagnostics`

:   Every diagnostic the compile produced, deduplicated and in a stable order that does not depend on catalog traversal order. Never null, and not necessarily empty on success: warnings are reported unless `AuthoringCompileOptions.IncludeWarnings` was cleared, while errors are always kept.

`public bool Succeeded`

:   Whether the compile produced usable content. It is true exactly when `CatalogSnapshot` is non-null, and a single error clears it; warnings on their own never do. Check it before reading the snapshot, and read `Diagnostics` either way.

`public bool WasCancelled`

:   True when the compile stopped because the options' cancellation token was signalled. A cancelled result is always a failed result.

---

## AuthoringDiagnostic

```csharp
public sealed class AuthoringDiagnostic : IEquatable<AuthoringDiagnostic>
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Validation/AuthoringDiagnostics.cs</small>

One problem found in authored content: which problem it is
(`DiagnosticId`), how serious it is (`Severity`), and where in
the authored data it sits (`Source`). Validation and compilation report
these rather than throwing, so a broken catalog yields a full list to fix instead of
one exception.

Instances are immutable and compared by value, and `HumanDetail` is
deliberately left out of that comparison: two reports of the same problem collapse
into one however differently their text reads.

**Constructors**

`public AuthoringDiagnostic(StableId diagnosticId, AuthoringDiagnosticSeverity severity, PortableSourceCoordinate source, string ownerStableIdRaw = null, StableId? relatedId = null, Diagnostic? nestedB3Diagnostic = null, string humanDetail = null)`

:   Creates a diagnostic, rejecting anything a report could not present coherently: an invalid diagnostic ID, a severity other than Error or Warning, an invalid source coordinate, an invalid related ID or nested diagnostic, or an owner ID that disagrees with the source coordinate's owner key.
    - `diagnosticId` &mdash; The stable code naming this problem, such as `authoring.id.duplicate`. Take it from the package's authoring diagnostic IDs rather than composing text.
    - `severity` &mdash; Error or Warning; any other value throws.
    - `source` &mdash; Where the problem is. The coordinate names serialized fields, not C# members, so it keeps pointing at the same authored site across refactors.
    - `ownerStableIdRaw` &mdash; The owning definition's authored ID exactly as written, or empty when the problem has no owner. When it is valid ID text it must equal the source coordinate's owner key; when it is present but malformed, the coordinate must carry that owner's hashed key form instead, which is how a diagnostic can still point at content whose own ID is unusable.
    - `relatedId` &mdash; A second ID the problem is about: the reference that was missing, the duplicate, the scheduler an encounter failed to match. Must be valid when supplied.
    - `nestedB3Diagnostic` &mdash; The simulation-layer diagnostic this one was translated from, when the failure arose while building simulation content. Its ID must be valid.
    - `humanDetail` &mdash; Extra human-readable detail, such as an explanatory sentence or the compile stage that failed. Empty when omitted, and excluded from equality and ordering, so no caller should key behaviour off it.

**Properties**

`public StableId DiagnosticId`

:   The stable code naming this problem; the field to branch on.

`public string HumanDetail`

:   Human-readable detail, empty when none was supplied. Excluded from equality, ordering, and de-duplication, so its wording can change without changing a report.

`public Diagnostic? NestedB3Diagnostic`

:   The simulation-layer diagnostic this one was translated from, when the failure came from building simulation content. Absent for problems found purely in authoring.

`public string OwnerStableIdRaw`

:   The owning definition's authored ID as written, or empty when the problem has no owner. It is not guaranteed to be valid ID text - that can be the problem itself.

`public StableId? RelatedId`

:   A second ID the problem is about, such as the missing reference or the duplicate. Absent when the problem concerns only its own site.

`public AuthoringDiagnosticSeverity Severity`

:   Whether this stops a compile or merely reports on it. A single error is decisive and no catalogue is published; warnings never block one. Errors also sort ahead of warnings in a frozen list, so the entries worth fixing first are the ones at the top.

`public PortableSourceCoordinate Source`

:   Where the problem is, expressed in serialized-field terms rather than C# member names.

**Methods**

`public bool Equals(AuthoringDiagnostic other)`

:   Value equality over every field except `HumanDetail`, which is what lets two differently-worded reports of one problem collapse into a single entry.
    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value equality against any object; false for other types and for null.
    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override int GetHashCode()`

:   A hash over the same fields `Equals(AuthoringDiagnostic)` compares, `HumanDetail` excluded.
    - **Returns** &mdash; A deterministic hash code for this value.

---

## AuthoringDiagnosticSeverity

```csharp
public enum AuthoringDiagnosticSeverity : byte
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Validation/AuthoringDiagnostics.cs</small>

How serious an `AuthoringDiagnostic` is. A single error is decisive:
compilation stops at the stage that produced it and returns no compiled catalog.
Warnings never block a compile, and are reported alongside errors unless the caller
clears `AuthoringCompileOptions.IncludeWarnings`.

Errors also sort ahead of warnings in a frozen diagnostic list, and these two are the
only values a diagnostic will accept.

| Value | Meaning |
| --- | --- |
| `Error` | Marks a diagnostic as error so tooling can decide whether compilation may continue. |
| `Warning` | Marks a diagnostic as warning so tooling can decide whether compilation may continue. |

---

## AuthoringLimits

```csharp
public static class AuthoringLimits
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Validation/AuthoringLimits.cs</small>

The structural ceilings authoring compilation enforces: how many definitions one
catalog may reference, how many teams, encounters, and formation presets it may
hold, the ranges normalized coordinates, aspect components, and sorting orders
have to fall inside, and how many diagnostics a single compile may report.

They are compile-time constants rather than settings because crossing one is
reported as a diagnostic and stops the catalog compiling; nothing is trimmed,
wrapped, or clamped to fit. The diagnostic pair works together:
`OrdinaryDiagnostics` ordinary entries are kept, and the one extra
slot up to `TotalDiagnostics` is reserved for the terminal
limit-exceeded diagnostic that says the report was truncated. The ceilings that
belong to the simulation instead of to authoring - skills, statuses, tags per
combatant - live on `TurnGauge.Simulation.SimulationLimits`.

**Fields**

`public const int AggregateNestedRecords`

:   Hard cap for aggregate nested records; validators reject larger inputs to bound memory and deterministic work.

`public const int AspectComponentMaximum`

:   Hard cap for aspect component maximum; validators reject larger inputs to bound memory and deterministic work.

`public const int CatalogDefinitionReferences`

:   Hard cap for catalog definition references; validators reject larger inputs to bound memory and deterministic work.

`public const int EncounterDefinitions`

:   Hard cap for encounter definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int ExpandedMembersPerEncounter`

:   Hard cap for expanded members per encounter; validators reject larger inputs to bound memory and deterministic work.

`public const int FormationAssignmentsPerEncounter`

:   Hard cap for formation assignments per encounter; validators reject larger inputs to bound memory and deterministic work.

`public const int FormationPresets`

:   Hard cap for formation presets; validators reject larger inputs to bound memory and deterministic work.

`public const int FormationSlotsPerPreset`

:   Hard cap for formation slots per preset; validators reject larger inputs to bound memory and deterministic work.

`public const int NormalizedCoordinateMaximum`

:   Hard cap for normalized coordinate maximum; validators reject larger inputs to bound memory and deterministic work.

`public const int OrdinaryDiagnostics`

:   Hard cap for ordinary diagnostics; validators reject larger inputs to bound memory and deterministic work.

`public const int SortingOrderMaximum`

:   Hard cap for sorting order maximum; validators reject larger inputs to bound memory and deterministic work.

`public const int SortingOrderMinimum`

:   Hard cap for sorting order minimum; validators reject larger inputs to bound memory and deterministic work.

`public const int TeamDefinitions`

:   Hard cap for team definitions; validators reject larger inputs to bound memory and deterministic work.

`public const int TeamMembersPerTeam`

:   Hard cap for team members per team; validators reject larger inputs to bound memory and deterministic work.

`public const int TotalDiagnostics`

:   Hard cap for total diagnostics; validators reject larger inputs to bound memory and deterministic work.

`public const int VfxAnchorsPerSlot`

:   Hard cap for VFX anchors per slot; validators reject larger inputs to bound memory and deterministic work.

---

## AuthoringValidationReport

```csharp
public sealed class AuthoringValidationReport
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/AuthoringCompileContracts.cs</small>

The diagnostics half of a compile, returned by
`BattleContentCompiler.Validate`. Validation runs the same full
pipeline and then discards the snapshot, so it costs what a compile costs and
reports exactly the diagnostics a compile would.

**Properties**

`public FrozenList<AuthoringDiagnostic> Diagnostics`

:   Ordered and filtered exactly as `AuthoringCompileResult.Diagnostics`. Never null.

`public bool IsValid`

:   True when the same catalog would have compiled. Errors clear it; warnings on their own do not.

`public bool WasCancelled`

:   True when validation stopped on cancellation. A cancelled report is never valid.

---

## BattleContentCompiler

:material-star: **Start here**

```csharp
public sealed partial class BattleContentCompiler
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/BattleContentCompiler.B4ContentMapping.cs</small>

The B4 mapping path converts captured authoring snapshots into the established B3 compiled-content model.

**Methods**

`public AuthoringCompileResult Compile(AuthoringCompileRequest request)`

:   Compiles one authoring catalogue into a published immutable snapshot, or reports the diagnostics that stopped it. The compiler is fail-closed and synchronous: a single error discards the whole snapshot rather than handing back partly compiled content, and cancellation or an unexpected compiler fault arrives as a failed result instead of an exception. The catalogue's Unity objects are read once and never retained, so the result can be kept for the lifetime of the game while the authoring assets are free to change or unload.
    - `request` &mdash; The catalogue to compile, the scheduler and mechanics registries to resolve it against, and the options to compile under. A null `AuthoringCompileRequest.Options` means `AuthoringCompileOptions.Default`.
    - **Returns** &mdash; A successful result carrying the published catalogue, or a failed one carrying only diagnostics. Never null.

`public AuthoringValidationReport Validate(AuthoringCompileRequest request)`

:   Runs the same pipeline as `Compile` and then discards the snapshot, keeping only the diagnostics. It costs what a compile costs and reports exactly what a compile would report, so it answers "would this catalogue build?" without the caller holding on to content it does not want yet.
    - `request` &mdash; The same request `Compile` takes.
    - **Returns** &mdash; A report whose `AuthoringValidationReport.IsValid` is true exactly when the equivalent compile would have succeeded. Never null.

---

## BattleRegistryProvider

```csharp
public abstract class BattleRegistryProvider : ScriptableObject
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/BattleRegistryProvider.cs</small>

Project-owned extension point for custom schedulers and mechanics. The
runtime controller and Battle Workbench both consume this same asset, so
an authored catalog is compiled and executed against the same explicit
registrations. TurnGauge never scans assemblies for implementations.

**Methods**

`public BattleRegistrySet CreateRegistries()`

:   Creates fresh built-in registries, then lets the provider add its project-specific registrations. A fresh pair is returned on every call so mutable registry state is never shared between sessions.
    - **Returns** &mdash; A fresh complete pair after project configuration.

---

## BattleRegistrySet

```csharp
public sealed class BattleRegistrySet
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/BattleRegistryProvider.cs</small>

One matched scheduler/mechanics registry pair. Keeping the pair together
prevents a catalog from being compiled with one set and started with
another by accident.

**Constructors**

`public BattleRegistrySet(BattleSchedulerRegistry schedulerRegistry, BattleMechanicsRegistry mechanicsRegistry)`

:   Creates a complete non-null registry pair.
    - `schedulerRegistry` &mdash; Scheduler implementations.
    - `mechanicsRegistry` &mdash; Formula, effect, target, AI, and reaction implementations.

**Properties**

`public BattleMechanicsRegistry MechanicsRegistry`

:   The mechanics implementations available to compilation and execution.

`public BattleSchedulerRegistry SchedulerRegistry`

:   The scheduler implementations available to compilation and execution.

**Methods**

`public static BattleRegistrySet WithBuiltIns()`

:   Creates a fresh pair containing only TurnGauge built-ins.
    - **Returns** &mdash; A new registry pair that is safe to extend independently.

---

## CompiledAuthoringCatalog

:material-star: **Start here**

```csharp
public sealed class CompiledAuthoringCatalog
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/AuthoringCompileContracts.cs</small>

The published output of a successful compile: the compiled battle content,
the registries it was resolved against, the encounters that can be started,
and the hashes identifying all of it. It is immutable and holds no reference
to the authoring assets it came from, so a game can compile once at load time
and never read a `BattleContentCatalog` again. Everything
`BattleEngine.Create` needs comes from here, which is also what lets the
same catalog drive a live battle, a headless batch, and an editor preview.

**Constructors**

`public CompiledAuthoringCatalog(CompiledBattleContent battleContent, BattleSchedulerRegistry schedulerRegistry, BattleMechanicsRegistry mechanicsRegistry, Sha256Digest compiledSnapshotHash, Sha256Digest contentManifestHash, IEnumerable<KeyValuePair<StableId, CompiledFormationPreset>> formationPresets, IEnumerable<KeyValuePair<StableId, CompiledEncounterSnapshot>> encounters)`

:   Publishes a compiled catalog, defensively copying both indexes into key-sorted immutable form.
    - `battleContent` &mdash; The compiled content the engine simulates.
    - `schedulerRegistry` &mdash; The scheduler registry this compile resolved against, carried through so a battle can be created from the catalog alone.
    - `mechanicsRegistry` &mdash; The mechanics registry this compile resolved against, carried through for the same reason.
    - `compiledSnapshotHash` &mdash; Digest of the canonical encoding of `battleContent`; must be a valid digest.
    - `contentManifestHash` &mdash; Content-identity digest for the same content; must be a valid digest.
    - `formationPresets` &mdash; Compiled formation presets keyed by preset id. Duplicate keys are rejected.
    - `encounters` &mdash; Compiled encounters keyed by encounter id. Duplicate keys are rejected.

**Properties**

`public CompiledBattleContent BattleContent`

:   The immutable content a battle is simulated against: rules, stats, resources, combatants, skills, statuses, reactions, and AI policies. It is what `CompiledSnapshotHash` digests, and it holds data only, never a delegate or a reference back to an authoring asset.

`public Sha256Digest CompiledSnapshotHash`

:   SHA-256 of the canonical encoding of `BattleContent`. Two catalogs sharing this digest compiled to byte-identical content.

`public Sha256Digest ContentManifestHash`

:   Content identity stamped into every battle started from this catalog. A checkpoint or replay whose manifest hash differs is rejected rather than resumed against the wrong content. It covers the canonical contract versions as well as the content, so upgrading the package can change it even when the authored data did not.

`public FrozenSortedIndex<StableId, CompiledEncounterSnapshot> Encounters`

:   Compiled encounters keyed and sorted by their authored encounter id. Each value carries the `CompiledEncounterSnapshot.StartRequest` a battle is created from, so this index is the usual entry point into a compiled catalog.

`public FrozenSortedIndex<StableId, CompiledFormationPreset> FormationPresets`

:   Compiled seating presets keyed and sorted by preset id. Their coordinates, facing, and draw order never reach `BattleContent` or any hash, so repositioning a seat changes where a combatant is drawn and nothing the simulation computes. The slot, row, and side ids are the exception: those travel into each combatant's start state, where row- and side-based targeting matches on them.

`public BattleMechanicsRegistry MechanicsRegistry`

:   The mechanics registry this compile resolved against, carried for the same reason as `SchedulerRegistry`: every formula, effect, target, AI policy, and reaction the content names is known to resolve in it.

`public BattleSchedulerRegistry SchedulerRegistry`

:   The scheduler registry this compile resolved against, carried so a battle can be created from the catalog alone. Starting one against a different registry risks the scheduler the content names no longer resolving.

---

## CompiledEncounterSnapshot

```csharp
public sealed class CompiledEncounterSnapshot
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/AuthoringCompileContracts.cs</small>

One authored encounter compiled into the exact inputs a battle starts from:
the start request, the formation layout the stage is built from, and the
digest identifying that start. It carries no seed, so one snapshot can start
any number of differently seeded battles.

**Constructors**

`public CompiledEncounterSnapshot(StableId encounterId, BattleStartRequest startRequest, CompiledEncounterFormationLayout formationLayout, Sha256Digest startRequestHash)`

:   Publishes one compiled encounter.
    - `encounterId` &mdash; Id of the authored encounter; must be a valid id.
    - `startRequest` &mdash; The compiled start a battle is created from.
    - `formationLayout` &mdash; Compiled seating for both teams.
    - `startRequestHash` &mdash; Digest of the canonical encoding of `startRequest`; must be a valid digest.

**Properties**

`public StableId EncounterId`

:   Id of the authored encounter this came from, and the key it is filed under in `CompiledAuthoringCatalog.Encounters`.

`public CompiledEncounterFormationLayout FormationLayout`

:   Which combatant sits in which slot for this encounter, indexed both by combatant and by slot. The stage places tokens from it; the engine reads nothing here beyond the slot, row, and side ids already carried in `StartRequest`.

`public BattleStartRequest StartRequest`

:   The compiled start a battle is created from: the teams, their combatants, and each combatant's opening resources, statuses, and seat. It carries no seed, which is what lets one encounter drive any number of differently seeded battles from the same bytes.

`public Sha256Digest StartRequestHash`

:   SHA-256 of the canonical encoding of `StartRequest`. The compiler proves the encoding round-trips to the same bytes and digest before publishing, and a replay records this same digest for its start.

---

## FrozenSortedIndex

```csharp
public sealed class FrozenSortedIndex
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Compilation/FrozenSortedIndex.cs</small>

A defensively copied, key-sorted immutable index.

**Constructors**

`public FrozenSortedIndex(IEnumerable<KeyValuePair<TKey, TValue>> source)`

:   Copies the supplied entries, sorts them by key, and refuses duplicate keys. Sorting once here is what lets every later lookup be a binary search, and the copy means the caller can keep mutating the collection it passed in without disturbing the index.
    - `source` &mdash; Entries to index, in any order. Enumerated exactly once.

**Properties**

`public int Count`

:   How many entries the index holds. Fixed for its lifetime, since the contents are settled at construction.

`public static FrozenSortedIndex<TKey, TValue> Empty`

:   A shared index with no entries. Hand this back instead of null so callers can enumerate or query an absent index without guarding it.

**Methods**

`public IEnumerator<KeyValuePair<TKey, TValue>> GetEnumerator()`

:   Walks the entries in ascending key order, which is not necessarily the order they were supplied in. Iteration is therefore stable across runs however the source collection was assembled.
    - **Returns** &mdash; An enumerator that visits the frozen key-value pairs in ascending key order.

`public bool TryGetValue(TKey key, out TValue value)`

:   Finds the entry with the given key by binary search, so lookup cost grows with the logarithm of `Count` rather than linearly.
    - `key` &mdash; Key to match, compared with its own comparer.
    - `value` &mdash; The matching value, or the value type's default when nothing matched.
    - **Returns** &mdash; True when an entry matched the key.

---
