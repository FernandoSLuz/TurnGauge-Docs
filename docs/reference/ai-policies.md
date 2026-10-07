# AI policies

6 types in this area.

!!! abstract "On this page"
    [AiCandidateDescription](#aicandidatedescription) &middot; [AiCandidatePlan](#aicandidateplan) &middot; [AiCandidateTrace](#aicandidatetrace) &middot; [AiConditionTrace](#aiconditiontrace) &middot; [AiContext](#aicontext) &middot; [AiDecisionTrace](#aidecisiontrace)

## AiCandidateDescription

```csharp
public sealed class AiCandidateDescription
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/AI/AiContracts.cs</small>

One action a policy puts forward for consideration: the authored rule it comes from, the
skill to use, and the targets to request. Proposing a candidate does not commit it: the
engine still checks the rule's conditions and the full legality of the resulting command,
and may reject it.

**Constructors**

`public AiCandidateDescription(StableId ruleId, StableId skillId, int priority, uint weight, IEnumerable<StableId> requestedTargets)`

:   Describes one candidate action.
    - `ruleId` &mdash; Authored rule this candidate comes from. Must be a rule of the policy being executed.
    - `skillId` &mdash; Skill to use. Must match the skill the named rule declares.
    - `priority` &mdash; Ordering key for priority-based selection; higher is preferred.
    - `weight` &mdash; Relative share for weighted random selection; ignored by policies that do not draw randomly.
    - `requestedTargets` &mdash; Targets to request. Stored in ascending identifier order, so authored order is not preserved; identifiers must be valid and duplicates are rejected.

**Properties**

`public int Priority`

:   Ordering key for priority-based selection, highest first. The engine itself selects the first legal candidate in plan order, so this value matters only insofar as the policy ordered the plan by it.

`public FrozenList<StableId> RequestedTargets`

:   Requested targets in ascending identifier order, valid and free of duplicates.

`public StableId RuleId`

:   Authored rule this candidate was built from. The engine matches it back against the policy it is executing and rejects any candidate naming a rule that policy does not own, which is what stops a policy proposing actions it was never given.

`public StableId SkillId`

:   Skill this candidate would use. It has to be the skill the named rule declares; a candidate whose skill disagrees with its rule is rejected rather than run.

`public uint Weight`

:   Relative share used by weighted random selection, taken against the summed weight of the candidates that survived validation. Policies that do not draw randomly ignore it, and a zero weight can never be drawn.

---

## AiCandidatePlan

```csharp
public sealed class AiCandidatePlan
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/AI/AiContracts.cs</small>

The candidates a policy returns for one decision opportunity, in preference order. Order is
significant: for policies that do not draw randomly the engine takes the first candidate that
survives validation, so a policy expresses its ranking by how it orders this list.

**Constructors**

`public AiCandidatePlan(IEnumerable<AiCandidateDescription> candidates)`

:   Freezes a candidate list, preserving the order given.
    - `candidates` &mdash; Candidates in preference order. Must contain no nulls and must not exceed the per-decision candidate limit. An empty plan is legal and means the actor has nothing to propose.

**Properties**

`public FrozenList<AiCandidateDescription> Candidates`

:   The proposed candidates, frozen in the order the policy supplied them. That order is the policy's ranking, so it is preserved exactly rather than re-sorted. An empty list is legal and means the actor put nothing forward.

---

## AiCandidateTrace

```csharp
public sealed class AiCandidateTrace
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/AI/AiContracts.cs</small>

Per-candidate record of why one proposed action was or was not eligible, including the
conditions that were evaluated for it and the diagnostic that rejected it.

**Constructors**

`public AiCandidateTrace(StableId ruleId, StableId skillId, IEnumerable<AiConditionTrace> conditions, Diagnostic? rejection, int priority, uint weight)`

:   Records the evaluation of one candidate.
    - `ruleId` &mdash; Rule the candidate came from.
    - `skillId` &mdash; Skill the candidate proposed.
    - `conditions` &mdash; Conditions evaluated for the rule, in evaluation order. Condition evaluation stops at the first failure, so this ends at the failing condition rather than covering every authored condition.
    - `rejection` &mdash; Reason the candidate was discarded, or null if it was accepted as legal.
    - `priority` &mdash; Priority as proposed by the policy.
    - `weight` &mdash; Weight as proposed by the policy.

**Properties**

`public FrozenList<AiConditionTrace> Conditions`

:   Conditions evaluated for this candidate, in evaluation order. Evaluation short-circuits on the first failure, so the last entry of a condition-rejected candidate is the one that failed.

`public int Priority`

:   Priority exactly as the policy proposed it, recorded whether or not the selection actually used it. It is the authored ranking, not the position the candidate ended up in.

`public Diagnostic? Rejection`

:   Why the candidate was discarded, or null if it was accepted as legal and became eligible for selection.

`public StableId RuleId`

:   Rule the traced candidate came from. Rule identifiers are unique within a policy, so this is how a trace entry is tied back to the authored rule that produced it.

`public StableId SkillId`

:   Skill the candidate proposed, exactly as proposed. A candidate whose skill disagrees with the rule it names - or that names a rule the policy does not own - is still traced, with this value and a `Rejection`, so it need not be the skill any rule declares.

`public uint Weight`

:   Weight exactly as the policy proposed it, before validation. A rejected candidate still records its weight here, but its share never reaches `AiDecisionTrace.SelectionBound`, which sums only the candidates that survived.

---

## AiConditionTrace

```csharp
public readonly struct AiConditionTrace
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/AI/AiContracts.cs</small>

Record of one authored condition being evaluated for a rule during an AI decision.

**Constructors**

`public AiConditionTrace(StableId ruleId, int conditionIndex, bool passed)`

:   Records the outcome of a single condition evaluation.
    - `ruleId` &mdash; Rule the condition belongs to.
    - `conditionIndex` &mdash; Position of the condition within that rule's condition list.
    - `passed` &mdash; Whether the condition held.

**Properties**

`public int ConditionIndex`

:   Position of the condition within that rule's authored condition list, counted from zero. It is what lines a trace entry up against the rule as it was authored.

`public bool Passed`

:   Whether the condition held. Evaluation stops at the first failure, so a false value here is the last condition recorded for the candidate.

`public StableId RuleId`

:   Rule whose condition list this evaluation was taken from.

---

## AiContext

```csharp
public sealed class AiContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/AI/AiContracts.cs</small>

Read-only input handed to an `IAiPolicy` when the engine asks it to propose
candidates for a single decision opportunity. The policy sees a projection of the battle
rather than the authoritative snapshot, so nothing reachable from this context can advance
or mutate the simulation.

**Constructors**

`public AiContext(CompiledBattleContent content, BattleSnapshot snapshot, StableId actorId, CompiledAiPolicyDefinition policy)`

:   Binds compiled content, immutable snapshot, acting combatant, and compiled policy for one AI decision. Policies may read it but cannot mutate the engine.
    - `content` &mdash; Compiled content the decision is resolved against.
    - `snapshot` &mdash; Battle state at the decision tick. It is wrapped in a `BattleStateView`; the snapshot itself is not retained or exposed.
    - `actorId` &mdash; Combatant whose decision opportunity is being resolved. Must be a valid identifier.
    - `policy` &mdash; Compiled policy being executed.

**Properties**

`public StableId ActorId`

:   Combatant whose decision opportunity is being resolved.

`public CompiledBattleContent Content`

:   Compiled catalog the decision is resolved against. The skills, statuses, and resources a policy inspects or proposes are looked up from here rather than from the battle state, so a policy reads authored intent and current state separately.

`public CompiledAiPolicyDefinition Policy`

:   Policy being executed. Its authored rules bound what may be proposed: the engine rejects any candidate that does not name a rule of this policy, or whose skill disagrees with the skill that rule declares.

`public BattleStateView Snapshot`

:   Projection of the battle at the decision tick. This is a view, not the authoritative snapshot, and it carries no random source.

---

## AiDecisionTrace

```csharp
public sealed class AiDecisionTrace
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/AI/AiContracts.cs</small>

Complete audit record of one automatic decision: every candidate considered and why it was
kept or dropped, every random draw consumed to choose among them and to resolve targets, and
the command that resulted. Because the draws are recorded alongside the outcome, a decision
can be re-derived and compared exactly, which is what makes replay divergence diagnosable.
Traces are surfaced on step, forecast, and replay results.

**Constructors**

`public AiDecisionTrace(long tick, ulong opportunitySequence, StableId actorId, StableId policyId, MechanicsImplementationReference implementation, IEnumerable<AiCandidateTrace> candidates, ulong? selectionBound, ulong? selectionSample, IEnumerable<StableId> targetCandidates, IEnumerable<uint> targetSamples, BattleCommand selectedCommand, bool noLegalCommand)`

:   Records one automatic decision. Either a command was selected or the decision yielded no legal command; exactly one of those two outcomes must be supplied, and a no-legal-command decision must carry no selection or target draws.
    - `tick` &mdash; Tick on which the decision was made.
    - `opportunitySequence` &mdash; Identifies the decision opportunity being resolved. Must be non-zero.
    - `actorId` &mdash; Combatant that decided.
    - `policyId` &mdash; Policy that produced the decision.
    - `implementation` &mdash; Implementation and contract version that served the policy.
    - `candidates` &mdash; One trace per candidate the policy proposed, in the order they were considered.
    - `selectionBound` &mdash; Total weight the selection draw was taken against, or null when no weighted draw occurred. Must be paired with `selectionSample`.
    - `selectionSample` &mdash; Value drawn to pick among the weighted candidates. Must be below `selectionBound`.
    - `targetCandidates` &mdash; Targets that were available to the selected command, in ascending identifier order.
    - `targetSamples` &mdash; One draw per randomly drawn target, in draw order; empty when the command's targets were requested explicitly or resolved without randomness. Each entry indexes the candidates still remaining at that point, so entry i must be below the candidate count minus i, and there cannot be more samples than candidates.
    - `selectedCommand` &mdash; Command the decision produced, or null when no legal command was available.
    - `noLegalCommand` &mdash; True when no candidate survived validation. Must be the inverse of whether `selectedCommand` was supplied.

**Properties**

`public StableId ActorId`

:   The combatant whose decision opportunity this trace answered.

`public FrozenList<AiCandidateTrace> Candidates`

:   One entry per candidate the policy proposed, in the order they were considered. Entries whose `AiCandidateTrace.Rejection` is null are the ones selection chose from.

`public MechanicsImplementationReference Implementation`

:   Implementation and contract version that served the policy.

`public bool NoLegalCommand`

:   True when no candidate survived validation, in which case the trace carries no selection or target draws.

`public ulong OpportunitySequence`

:   Monotonic scheduler opportunity number recorded for ordering and diagnostics. It is distinct from command, event, and action sequences.

`public StableId PolicyId`

:   The policy the engine ran for this decision - the acting combatant's authored default, or the override its start entry named in place of it.

`public BattleCommand SelectedCommand`

:   Command the decision produced, or null when no legal command was available. Null exactly when `NoLegalCommand` is true.

`public ulong? SelectionBound`

:   Summed weight of the eligible candidates that the selection draw was taken against, or null when the decision needed no weighted draw.

`public ulong? SelectionSample`

:   Value drawn below `SelectionBound` to pick the winning candidate; null exactly when `SelectionBound` is null.

`public FrozenList<StableId> TargetCandidates`

:   Targets that were available to the selected command, in ascending identifier order.

`public FrozenList<uint> TargetSamples`

:   One draw per randomly drawn target, in draw order, and empty when the command's targets were requested explicitly or resolved without randomness. Each entry indexes the candidates still remaining when it was drawn rather than `TargetCandidates` directly, so reconstructing the picks means removing each one as you walk the list.

`public long Tick`

:   Tick the decision was taken on. Several decisions can land on the same tick, so match a trace by `OpportunitySequence` rather than by tick.

---
