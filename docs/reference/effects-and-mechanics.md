# Effects and mechanics

41 types in this area.

!!! abstract "On this page"
    [AiValidationContext](#aivalidationcontext) &middot; [BattleFormulaService](#battleformulaservice) &middot; [BattleMechanicsRegistry](#battlemechanicsregistry) &middot; [BattleStateView](#battlestateview) &middot; [EffectPlan](#effectplan) &middot; [EffectPlanningContext](#effectplanningcontext) &middot; [EffectPrimitive](#effectprimitive) &middot; [EffectPrimitiveTag](#effectprimitivetag) &middot; [EffectValidationContext](#effectvalidationcontext) &middot; [FormulaAttribution](#formulaattribution) &middot; [FormulaAttributionTrace](#formulaattributiontrace) &middot; [FormulaAttributionTraceBatch](#formulaattributiontracebatch) &middot; [FormulaContext](#formulacontext) &middot; [FormulaContribution](#formulacontribution) &middot; [FormulaContributionKind](#formulacontributionkind) &middot; [FormulaEvaluationRequest](#formulaevaluationrequest) &middot; [FormulaModifierInput](#formulamodifierinput) &middot; [FormulaPreview](#formulapreview) &middot; [FormulaPreviewContext](#formulapreviewcontext) &middot; [FormulaRandomBoundKind](#formularandomboundkind) &middot; [FormulaRandomInputDescriptor](#formularandominputdescriptor) &middot; [FormulaRandomSample](#formularandomsample) &middot; [FormulaResult](#formularesult) &middot; [FormulaValidationContext](#formulavalidationcontext) &middot; [IAiPolicy](#iaipolicy) &middot; [IEffectResolver](#ieffectresolver) &middot; [IFormula](#iformula) &middot; [IMechanicsImplementation](#imechanicsimplementation) &middot; [IMechanicsRandomSource](#imechanicsrandomsource) &middot; [IReactionRule](#ireactionrule) &middot; [ITargetResolver](#itargetresolver) &middot; [MechanicsCategoryTag](#mechanicscategorytag) &middot; [MechanicsDiagnosticIds](#mechanicsdiagnosticids) &middot; [MechanicsIds](#mechanicsids) &middot; [MechanicsRegistryBinding](#mechanicsregistrybinding) &middot; [MechanicsResolveResult](#mechanicsresolveresult) &middot; [ReactionValidationContext](#reactionvalidationcontext) &middot; [SchedulerAdjustmentKind](#scheduleradjustmentkind) &middot; [StatusApplicationPreview](#statusapplicationpreview) &middot; [TargetValidationContext](#targetvalidationcontext) &middot; [ValidationReport](#validationreport)

## AiValidationContext

```csharp
public sealed class AiValidationContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Read-only catalog passed to IAiPolicy.Validate while compiled content is
being built. A policy checks its authored PropertySet against this
catalog; any error in the returned report aborts compilation.

**Constructors**

`public AiValidationContext(CompiledBattleContent content)`

:   Binds the context to the catalog being compiled.
    - `content` &mdash; Non-null compiled catalog used to validate skill, status, and other IDs named by AI policy properties.

**Properties**

`public CompiledBattleContent Content`

:   The catalog an authored property value must resolve against, such as a skill or status a policy's tuning refers to. The policy definition and its rules are not supplied here; they arrive with the decision, on `AiContext`.

---

## BattleFormulaService

```csharp
public static class BattleFormulaService
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Formulas/BattleFormulaService.cs</small>

Pure formula input and evaluation boundary shared by runtime, forecast,
replay, Workbench, tooltips, and range previews.

**Methods**

`public static FormulaContext BuildContext()`

:   Freezes every input the requested primitive's formula is allowed to read: source stat, potency, target defense, hit and critical chances, variance and clamp bounds, and the status modifiers that apply, in canonical order. Building a context reads state but never draws, so the same context can be evaluated or previewed.
    - `content` &mdash; Compiled catalog the request's IDs and the battle rules are read from. It must be a profile 3 catalog.
    - `snapshot` &mdash; State the combatants, stats, and statuses are read from. It must be a profile 3 snapshot, and it is not modified.
    - `request` &mdash; Coordinates of the primitive to build inputs for.
    - **Returns** &mdash; The frozen inputs for exactly that primitive. Unless the effect authored its own source stat, healing scales off the rules' spirit stat and damage off the power stat; healing also gets no variance band and no critical chance unless the effect asked for one.

`public static FormulaResult Evaluate()`

:   Runs the request's formula and returns the authoritative result. This is the only call here that consumes RNG, and it is the same call the reducer makes, so given the same context and the same draw cursor it produces the same number every time.
    - `registry` &mdash; Registry the primitive's formula ID and contract version are resolved through.
    - `context` &mdash; Frozen inputs, normally from `BuildContext`. Its source, target, effect entry, and primitive index must match the request or the call throws.
    - `random` &mdash; Draw cursor the formula consumes, in the order `DescribeRandomInputs` declared.
    - `request` &mdash; The immutable request to validate and execute.
    - **Returns** &mdash; Hit, critical, final magnitude, and the attribution the engine hashes into its event. Never null.

`public static FormulaPreview Preview()`

:   Reports the range the same inputs could produce, without drawing and without changing anything. This is the surface tooltips and range previews should call: it can be asked at any time, as often as wanted, and cannot advance the battle or disturb its RNG.
    - `content` &mdash; Compiled catalog the request's IDs are read from. It must be a profile 3 catalog.
    - `snapshot` &mdash; State the preview is computed against. It is not modified.
    - `registry` &mdash; Registry the primitive's formula ID and contract version are resolved through.
    - `request` &mdash; Coordinates of the primitive to forecast.
    - **Returns** &mdash; Minimum and maximum for a use that lands, plus the chances shown to a player. Never null.

`public static StatusApplicationPreview PreviewStatusApplication()`

:   Resolves the odds of one status landing on one target: the authored base chance reduced by the target's matching resistances, or refused outright when the target is immune. No RNG is consumed. The live reducer decides status application with this same call, so a tooltip built from it shows the chance the engine will actually roll against.
    - `content` &mdash; Compiled catalog the status and the target's definition are read from.
    - `snapshot` &mdash; State the target is looked up in. It is not modified.
    - `targetId` &mdash; Combatant the status would be applied to.
    - `statusId` &mdash; Status definition whose odds are asked.
    - `baseChance` &mdash; Chance authored on the applying effect, before resistance.
    - **Returns** &mdash; The base chance, the resolved resistance, the resulting final chance, and whether the target is immune.

---

## BattleMechanicsRegistry

:material-star: **Start here**

```csharp
public sealed class BattleMechanicsRegistry
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/BattleMechanicsRegistry.cs</small>

The immutable table that binds every formula, effect resolver, target
resolver, AI policy, and reaction rule to an ID and a contract version.
Compiled content and replays store only those IDs and versions, so the
registry is the one thing a running battle, a content compile, and a
canonical round-trip must all agree on. Content that names an
implementation the registry does not hold is rejected with a registry
diagnostic rather than quietly running against a substitute.

!!! note "Remarks"
    Registration is persistent rather than in place: every Register overload
    returns a new registry and leaves the receiver untouched, so build the
    registry once during start-up and hand the final instance to the engine.
    Registering a null implementation, one whose category alias disagrees with
    its ImplementationId or ContractVersion, or a category, ID, and version
    that is already present throws an InvalidOperationException carrying a
    registry diagnostic - a duplicate is never silently replaced. A finished
    registry never changes, so it can be shared between concurrently running
    engines.

**Properties**

`public FrozenList<MechanicsRegistryBinding> Bindings`

:   Every registered key, ordered by category, then implementation ID, then contract version. Each read builds a fresh list, so cache the result rather than reading it inside a loop.

`public static BattleMechanicsRegistry Empty`

:   The registry with no entries, and the starting point for a chain of Register calls when you want none of the built-in implementations.

**Methods**

`public static BattleMechanicsRegistry CreateWithBuiltIns()`

:   Builds a registry holding every implementation TurnGauge ships: the standard damage, healing, and scalar formulas, the built-in effect and target resolvers, the priority, conditional, and weighted AI policies, and the effect-tag reaction rule. This is the usual starting point - keep registering onto the result to add your own.
    - **Returns** &mdash; A new registry containing only the built-in entries.

`public BattleMechanicsRegistry Register(IFormula implementation)`

:   Files a formula under its FormulaId and FormulaContractVersion.
    - `implementation` &mdash; Its FormulaId and FormulaContractVersion must equal its ImplementationId and ContractVersion, or registration throws.
    - **Returns** &mdash; A new registry containing the entry; this instance is unchanged.

`public BattleMechanicsRegistry Register(IEffectResolver implementation)`

:   Files an effect resolver under its ResolverId and EffectContractVersion.
    - `implementation` &mdash; Its ResolverId and EffectContractVersion must equal its ImplementationId and ContractVersion, or registration throws.
    - **Returns** &mdash; A new registry containing the entry; this instance is unchanged.

`public BattleMechanicsRegistry Register(ITargetResolver implementation)`

:   Files a target resolver under its ResolverId and TargetContractVersion.
    - `implementation` &mdash; Its ResolverId and TargetContractVersion must equal its ImplementationId and ContractVersion, or registration throws.
    - **Returns** &mdash; A new registry containing the entry; this instance is unchanged.

`public BattleMechanicsRegistry Register(IAiPolicy implementation)`

:   Files an AI policy under its PolicyId and AiContractVersion.
    - `implementation` &mdash; Its PolicyId and AiContractVersion must equal its ImplementationId and ContractVersion, or registration throws.
    - **Returns** &mdash; A new registry containing the entry; this instance is unchanged.

`public BattleMechanicsRegistry Register(IReactionRule implementation)`

:   Files a reaction rule under its ImplementationId. IReactionRule has no separate ID alias, so only the version aliases are cross-checked.
    - `implementation` &mdash; Its ReactionContractVersion must equal its ContractVersion, or registration throws.
    - **Returns** &mdash; A new registry containing the entry; this instance is unchanged.

`public MechanicsResolveResult<IAiPolicy> ResolveAi(StableId id, int version)`

:   Looks up a registered AI policy. A failed lookup is reported in the result rather than thrown.
    - `version` &mdash; Contract version, matched exactly; there is no latest-version fallback, and a version below one is rejected outright.
    - `id` &mdash; Exact AI policy implementation key recorded by the compiled automatic-decision policy.
    - **Returns** &mdash; The policy, or a failed result carrying the diagnostic. Never null.

`public MechanicsResolveResult<IEffectResolver> ResolveEffect(StableId id, int version)`

:   Looks up a registered effect resolver. A failed lookup is reported in the result rather than thrown.
    - `version` &mdash; Contract version, matched exactly; there is no latest-version fallback, and a version below one is rejected outright.
    - `id` &mdash; Exact effect-resolver key recorded on the compiled effect entry.
    - **Returns** &mdash; The resolver, or a failed result carrying the diagnostic. Never null.

`public MechanicsResolveResult<IFormula> ResolveFormula(StableId id, int version)`

:   Looks up a registered formula. A failed lookup is reported in the result rather than thrown.
    - `version` &mdash; Contract version, matched exactly; there is no latest-version fallback, and a version below one is rejected outright.
    - `id` &mdash; Exact formula implementation key; invalid, missing, wrong-category, and wrong-version cases return distinct diagnostics.
    - **Returns** &mdash; The formula, or a failed result whose diagnostic distinguishes an unknown ID, an ID registered under another category, and an ID registered only at other versions. Never null.

`public MechanicsResolveResult<IReactionRule> ResolveReaction(StableId id, int version)`

:   Looks up a registered reaction rule. A failed lookup is reported in the result rather than thrown.
    - `version` &mdash; Contract version, matched exactly; there is no latest-version fallback, and a version below one is rejected outright.
    - `id` &mdash; Exact reaction-rule implementation key recorded by the compiled reaction definition.
    - **Returns** &mdash; The rule, or a failed result carrying the diagnostic. Never null.

`public MechanicsResolveResult<ITargetResolver> ResolveTarget(StableId id, int version)`

:   Looks up a registered target resolver. A failed lookup is reported in the result rather than thrown.
    - `version` &mdash; Contract version, matched exactly; there is no latest-version fallback, and a version below one is rejected outright.
    - `id` &mdash; Exact target-resolver key recorded on the compiled skill target contract.
    - **Returns** &mdash; The resolver, or a failed result carrying the diagnostic. Never null.

---

## BattleStateView

```csharp
public sealed class BattleStateView
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/BattleStateView.cs</small>

Immutable, RNG-free projection supplied to non-formula mechanics extensions.
The authoritative snapshot deliberately is not reachable from this type.

**Properties**

`public FrozenList<ActiveActionState> ActiveActions`

:   Actions accepted but not yet finished resolving, at most one per actor, ordered by root action sequence. This is what tells an extension who is mid-action.

`public FrozenList<CombatantState> Combatants`

:   Every combatant on both teams, living and dead, ordered by identifier rather than by turn order. Use `FindCombatant` rather than assuming a position.

`public FrozenList<CooldownState> Cooldowns`

:   Only the cooldowns still blocking: an expired cooldown is dropped rather than kept at zero, so the presence of an entry is the whole readiness test.

`public SimulationContractProfile Profile`

:   Contract profile of the battle this projection was taken from. It decides which of the collections below can hold anything at all: stats, statuses, and shields stay empty under the earlier profiles, and resources are empty under profile 1.

`public FrozenList<ResourceState> Resources`

:   Every resource pool in the battle, at most one entry per owner-and-resource pair. Empty under profile 1. Use `FindResource` to reach a single pool.

`public BattleResultState Result`

:   The battle's outcome as of this tick. It is never `null`: a battle still running carries the nonterminal result rather than nothing.

`public StableId SchedulerId`

:   Stable ID of the scheduler that owns the encoded state. Restore requires a registry binding with the same ID and contract version.

`public SchedulerState SchedulerState`

:   The scheduler's own state, including the ordered queue of combatants awaiting a decision. `null` under profile 1, which runs without a scheduler.

`public FrozenList<ShieldState> Shields`

:   Shields with absorption left; a spent shield is removed rather than held at zero. Empty under profiles 1 and 2.

`public FrozenList<CombatantStatState> Stats`

:   Base stat values per combatant, before any status modifier is folded in - reading an entry here is not the same as reading a combatant's effective stat. Empty under profiles 1 and 2, which have no stats.

`public FrozenList<StatusInstanceState> Statuses`

:   Live status instances across every combatant, not grouped by owner. Empty under profiles 1 and 2.

`public FrozenList<TeamState> Teams`

:   The battle's teams - exactly two.

`public long Tick`

:   The tick the projected snapshot sat on. Every value on this view describes that one moment; it does not advance as the battle continues.

**Methods**

`public CombatantState FindCombatant(StableId id)`

:   Looks up a combatant by identifier, living or dead. This is a linear scan over `Combatants`, so hoist the result rather than repeating the call inside a loop.
    - `id` &mdash; Identifier of the combatant to find.
    - **Returns** &mdash; The combatant, or `null` when none carries that identifier.

`public ResourceState FindResource(StableId ownerId, StableId resourceId)`

:   Looks up one combatant's pool for one resource. Pools are never shared between combatants, so the pair matches at most one entry.
    - `ownerId` &mdash; The combatant that owns the pool.
    - `resourceId` &mdash; The resource the pool holds.
    - **Returns** &mdash; The pool, or `null` when that combatant has no pool for that resource.

`public TeamState FindTeam(StableId id)`

:   Looks up a team by identifier.
    - `id` &mdash; Identifier of the team to find.
    - **Returns** &mdash; The team, or `null` when neither team carries that identifier.

---

## EffectPlan

```csharp
public sealed class EffectPlan
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Effects/EffectPlan.cs</small>

What one effect entry expands into: the primitives to execute, in order,
plus any diagnostics that make the expansion unusable. The engine runs the
primitives in the order they appear here, so a resolver expresses sequence
by position. A plan that carries even one diagnostic executes nothing: the
step fails with the first diagnostic and the snapshot the engine started
from is restored.

**Constructors**

`public EffectPlan(IEnumerable<EffectPrimitive> primitives, IEnumerable<Diagnostic> diagnostics)`

:   Builds a plan from a resolver's primitives and diagnostics. Both arguments are required; pass an empty diagnostic list for a plan the engine should execute.
    - `primitives` &mdash; Primitives in execution order, none of them null, at most the per-effect planning limit.
    - `diagnostics` &mdash; Reasons the plan cannot be executed, or empty.

**Properties**

`public FrozenList<Diagnostic> Diagnostics`

:   Reasons this plan cannot run. The engine fails the step with the first entry.

`public bool IsValid`

:   True only while no diagnostic is present. The engine checks this before it executes anything, so an invalid plan changes no state.

`public FrozenList<EffectPrimitive> Primitives`

:   The primitives in the order the engine executes them.

---

## EffectPlanningContext

```csharp
public sealed class EffectPlanningContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Effects/EffectPlan.cs</small>

Frozen inputs for one call to IEffectResolver.Plan: the compiled catalog,
a read-only view of the battle state, and the source, target, and effect
entry being planned. Nothing reachable from here can advance or mutate the
battle, and no RNG is offered - planning must stay a pure function of
these inputs.

**Constructors**

`public EffectPlanningContext(CompiledBattleContent content, BattleSnapshot snapshot, StableId sourceId, StableId targetId, StableId effectEntryId)`

:   Binds the context to one source, target, and effect entry. Every argument is required and all three IDs must be valid.
    - `content` &mdash; Compiled catalog the resolver may read while planning.
    - `snapshot` &mdash; Authoritative state to project into the read-only view the resolver sees; the snapshot itself is not exposed.
    - `sourceId` &mdash; Combatant performing the action.
    - `targetId` &mdash; The one combatant this planning call covers; the engine plans separately for each resolved target.
    - `effectEntryId` &mdash; The compiled effect entry being planned.

**Properties**

`public CompiledBattleContent Content`

:   The compiled catalog the resolver may read while planning, and the same instance the battle is running, so anything looked up here is what the engine will go on to execute.

`public StableId EffectEntryId`

:   Identity of the compiled effect entry being planned. It is reported on the events and formula traces this effect produces, which is how a consumer ties them back to the authored entry.

`public BattleStateView Snapshot`

:   Read-only projection of the state as it stands at planning time. The authoritative snapshot is deliberately not reachable from it.

`public StableId SourceId`

:   The combatant performing the action. A damage or healing formula the plan produces reads this combatant's stats as the source side.

`public StableId TargetId`

:   The one combatant this planning call covers. The engine plans separately for each locked target, so a multi-target action calls the resolver once per target with only this member changing between calls.

---

## EffectPrimitive

```csharp
public sealed class EffectPrimitive
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Effects/EffectPlan.cs</small>

One immutable unit of work an effect resolver asks the engine to perform.
Build one with the static factory for the operation you want: the
factories are the only way to make a primitive, and each rejects a
payload the engine could not execute, so an accepted primitive is always
structurally sound. A primitive states what should happen; the engine
still decides how much of it lands.

**Properties**

`public bool BypassDefense`

:   When set, the formula reads the target's defense stat as zero.

`public bool BypassIncomingModifiers`

:   When set, incoming-stage modifiers from statuses on the target are left out of the formula's contributions.

`public bool BypassShield`

:   When set, damage lands straight on health and the target's shields absorb nothing.

`public Chance64 Chance`

:   Base application chance for a status primitive, before the target's resistances and immunities narrow it. Zero for every other tag.

`public Fixed64 FixedAmount`

:   Shield strength for a shield primitive; the engine clamps it to at least one point. Zero for every other tag.

`public MechanicsImplementationReference Formula`

:   Exact formula the engine evaluates for a damage or healing primitive. Other tags leave it unset.

`public PropertySet FormulaProperties`

:   Authored configuration that formula reads - source stat, potency, hit chance, critical allowance for the built-in formulas. Never null; empty when the resolver passed nothing.

`public StableId Id`

:   What the operation acts on: the resource to change, the shield to create, the status definition to apply or remove, or the reason recorded for a cast interrupt. Those tags require a valid ID; the others leave it unset.

`public StableId? LinkedStatusDefinitionId`

:   Status definition a shield primitive binds itself to, so the two are applied, reapplied, and removed together. Only a shield primitive may set it, and the engine skips that shield unless a status instance applied to the target by the same action matches.

`public StatusPolarity Polarity`

:   The polarity a status must have for a dispel primitive to remove it. Unused by every other tag.

`public int Priority`

:   Absorption order for a shield primitive - the target's lowest-priority shield absorbs first - or, for a scheduler adjustment, the requested SchedulerAdjustmentKind. Zero for every other tag.

`public long SignedAmount`

:   The integer payload: the resource delta for a resource change, the most statuses a dispel may remove, or the delta handed to the scheduler. Zero for every other tag.

`public EffectPrimitiveTag Tag`

:   The operation to perform. It decides which of the members below carry meaning; the rest hold their defaults.

`public FrozenList<StableId> Tags`

:   Tag filter for a dispel primitive, sorted and deduplicated: a status qualifies when it shares at least one of these tags. Empty means no tag filter. Never null.

**Methods**

`public static EffectPrimitive AdjustScheduler(SchedulerAdjustmentKind kind, long delta)`

:   Creates a scheduler-adjustment primitive. The battle's scheduler must expose an adjustment adapter that supports this kind, or the step fails; the adapter clamps the delta and reports what it applied.
    - `kind` &mdash; Which timing value to move; it must be a defined kind.
    - `delta` &mdash; Signed amount to move it by, in ticks or gauge units according to the kind.
    - **Returns** &mdash; A validated scheduler-adjustment primitive retaining the requested kind and signed ticks-or-gauge delta.

`public static EffectPrimitive ApplyShield()`

:   Updates apply shield on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `shieldId` &mdash; Identity of the shield to create; it must be valid.
    - `amount` &mdash; Strength of the shield; the engine clamps it to at least one point.
    - `priority` &mdash; Absorption order among the target's shields; the lowest absorbs first.
    - `linkedStatusDefinitionId` &mdash; Status definition to bind the shield to, so status and shield are applied, reapplied, and removed together, or null for a free-standing shield. The shield is skipped when the same action has not applied that status to the target.
    - **Returns** &mdash; A validated shield primitive carrying strength, absorption priority, and optional status linkage; invalid IDs throw.

`public static EffectPrimitive ApplyStatus(StableId statusDefinitionId, Chance64 baseChance)`

:   Creates a status-application primitive. The engine narrows the chance by the target's resistances, skips the roll entirely when the target is immune, and draws RNG only when the narrowed chance is neither impossible nor guaranteed.
    - `statusDefinitionId` &mdash; Status definition to apply; it must be valid and present in the compiled catalog.
    - `baseChance` &mdash; Chance before the target's resistances and immunities are taken into account.
    - **Returns** &mdash; A validated status-application primitive carrying the definition ID and pre-resistance probability.

`public static EffectPrimitive ChangeResource(StableId resourceId, long delta)`

:   Creates a resource-change primitive. The engine clamps the delta to the resource's range, so the change that actually lands can be smaller than the one asked for.
    - `resourceId` &mdash; Resource on the target to change; it must be valid and the target must own it.
    - `delta` &mdash; Signed amount to add, in resource points.
    - **Returns** &mdash; A validated resource-change primitive carrying the resource ID and unclamped signed point delta.

`public static EffectPrimitive Damage()`

:   Creates a damage primitive: the engine evaluates the formula and applies its result to the target, through the target's shields unless they are bypassed.
    - `formula` &mdash; Formula ID and contract version; both are required and must resolve at execution time.
    - `formulaProperties` &mdash; Authored configuration for that formula; null is treated as empty.
    - `bypassShield` &mdash; Applies the result straight to health, leaving the target's shields untouched.
    - `bypassDefense` &mdash; Makes the formula read the target's defense stat as zero.
    - `bypassIncomingModifiers` &mdash; Leaves incoming-stage modifiers from statuses on the target out of the formula.
    - **Returns** &mdash; A validated damage primitive carrying the exact formula reference, normalized property set, and three bypass flags.

`public static EffectPrimitive Dispel(StatusPolarity polarity, IEnumerable<StableId> tags, int maximumCount)`

:   Creates a dispel primitive that removes dispellable statuses from the target, oldest application first. Only statuses whose definition is marked dispellable are candidates, so a dispel can legitimately remove nothing.
    - `polarity` &mdash; Polarity a status must match to qualify: Neutral, Buff, or Debuff.
    - `tags` &mdash; Tag filter - a status qualifies when it shares at least one of these tags; null or empty means no tag filter. The list is sorted and deduplicated.
    - `maximumCount` &mdash; Most statuses this primitive may remove; it must be at least one and no more than the per-combatant status limit.
    - **Returns** &mdash; A validated dispel primitive with a canonical tag filter and bounded positive removal count.

`public static EffectPrimitive Heal(MechanicsImplementationReference formula, PropertySet formulaProperties)`

:   Creates a healing primitive. The engine clamps the formula's result to the target's missing health, and a dead target is healed for nothing.
    - `formula` &mdash; Formula ID and contract version; both are required and must resolve at execution time.
    - `formulaProperties` &mdash; Authored configuration for that formula; null is treated as empty.
    - **Returns** &mdash; A validated healing primitive carrying the exact formula reference and a non-null property set.

`public static EffectPrimitive InterruptCast(StableId reasonId)`

:   Creates a primitive that cancels the target's in-progress cast. A target with no cast in progress - including one whose cast completed at this same tick boundary - is a deterministic no-op; a cast that is not interruptible fails the step.
    - `reasonId` &mdash; Reason recorded on the interrupt; it must be valid.
    - **Returns** &mdash; A validated cast-interruption primitive carrying the stable reason ID reported by the engine.

`public static EffectPrimitive RemoveStatus(StableId statusDefinitionId)`

:   Creates a primitive that removes one instance of the named status from the target, dispellable or not, and does nothing when the target does not carry it.
    - `statusDefinitionId` &mdash; Status definition to remove; it must be valid.
    - **Returns** &mdash; A validated single-status removal primitive that ignores authored dispellable restrictions at execution time.

---

## EffectPrimitiveTag

```csharp
public enum EffectPrimitiveTag : byte
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Effects/EffectPlan.cs</small>

The operation one planned primitive performs. The tag also decides which
of a primitive's payload members carry meaning; the others stay at their
defaults.

| Value | Meaning |
| --- | --- |
| `CalculateAndDamage` | Evaluates the referenced formula and applies the result as damage, through the target's shields unless the primitive bypasses them. |
| `CalculateAndHeal` | Evaluates the referenced formula and applies the result as healing, clamped to the target's missing health. |
| `ChangeResource` | Shifts one named resource on the target by the signed amount, clamped to the resource's zero-to-maximum range. |
| `ApplyShield` | Adds a shield that absorbs damage before health. |
| `ApplyStatus` | Rolls the primitive's chance, after the target's resistances and immunities have narrowed it, and applies the named status definition when it lands. |
| `RemoveStatus` | Removes one instance of the named status definition from the target, whether or not that status is dispellable. |
| `Dispel` | Removes dispellable statuses that match the primitive's polarity and tag filter, oldest application first, up to the primitive's maximum count. |
| `AdjustScheduler` | Hands a timing delta to the scheduler's adjustment adapter. |
| `InterruptCast` | Cancels the target's in-progress cast and records the primitive's ID as the reason. |

---

## EffectValidationContext

```csharp
public sealed class EffectValidationContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Read-only catalog passed to IEffectResolver.Validate while compiled
content is being built. A resolver checks its authored PropertySet
against this catalog; any error in the returned report aborts
compilation.

**Constructors**

`public EffectValidationContext(CompiledBattleContent content)`

:   Binds the context to the catalog being compiled.
    - `content` &mdash; Non-null compiled catalog used to validate effect properties and every definition they reference.

**Properties**

`public CompiledBattleContent Content`

:   The catalog an authored property value must resolve against - the status, resource, or skill an effect entry names. Checking those IDs here is what turns a typo into a compile diagnostic rather than a primitive that quietly does nothing mid-battle.

---

## FormulaAttribution

```csharp
public sealed class FormulaAttribution
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

The complete, immutable account of one formula evaluation: the inputs
it read, every step it applied, every random draw it took, and the
values it ended on. This object is what
`CanonicalBattleSerializer.HashFormulaAttribution` hashes, so the
hash carried by a damage, healing or miss event can be checked against
the arithmetic it stands for.

**Constructors**

`public FormulaAttribution()`

:   Records one evaluation. Throws when the source, target or effect-entry identifier is invalid, when the primitive index is out of range, or when a collection exceeds its structural limit.
    - `formula` &mdash; Identity and contract version of the formula implementation that performed the evaluation.
    - `primitiveIndex` &mdash; Position of the resolved primitive within its effect entry's planned primitives.
    - `inputs` &mdash; The named input values the formula read, such as base stat, potency, defense, chances and the endpoint bounds.
    - `contributions` &mdash; The steps the formula applied, in the order it applied them; that order is preserved and is part of the canonical hash.
    - `randomSamples` &mdash; The draws the formula took, in draw order.
    - `clampContribution` &mdash; The signed adjustment the endpoint clamp contributed, that is `finalResult` minus `roundedResult`.
    - `effectEntryId` &mdash; Valid identifier of the effect entry whose planned primitive requested this formula evaluation.
    - `finalResult` &mdash; Endpoint amount returned to the simulation after rounding and clamping; zero represents a miss where applicable.
    - `roundedResult` &mdash; Whole endpoint amount after the formula's rounding stage but before its clamp.
    - `sourceId` &mdash; Valid combatant identifier whose stats and outgoing modifiers supplied source-side inputs.
    - `targetId` &mdash; Valid combatant identifier whose defense and incoming modifiers supplied target-side inputs.
    - `unclampedResult` &mdash; Fixed-point value reached by formula arithmetic before whole-number rounding and endpoint limits.

**Properties**

`public Fixed64 ClampContribution`

:   The signed adjustment the endpoint clamp contributed, that is `FinalResult` minus `RoundedResult`.

`public FrozenList<FormulaContribution> Contributions`

:   The steps the formula applied, in the order it applied them.

`public StableId EffectEntryId`

:   The effect entry being resolved. Together with `PrimitiveIndex` it names the exact primitive this evaluation belongs to.

`public Fixed64 FinalResult`

:   The value the evaluation ended on: the amount the formula reported back to the simulation, and zero for a miss.

`public MechanicsImplementationReference Formula`

:   Identity and contract version of the formula implementation that performed the evaluation.

`public PropertySet Inputs`

:   The named input values the formula read, such as base stat, potency, defense, chances and the endpoint bounds.

`public int PrimitiveIndex`

:   Position of the resolved primitive within its effect entry's planned primitives.

`public FrozenList<FormulaRandomSample> RandomSamples`

:   The draws the formula took, in draw order. Empty when the evaluation consumed no randomness.

`public Fixed64 RoundedResult`

:   The value after rounding, before the endpoint clamp.

`public StableId SourceId`

:   The combatant the evaluation was performed for, whose stats and outgoing modifiers fed it.

`public StableId TargetId`

:   The combatant the value was worked out against, whose defence and incoming modifiers fed it. Always set, including for an evaluation that missed.

`public Fixed64 UnclampedResult`

:   The value reached before rounding and clamping.

---

## FormulaAttributionTrace

```csharp
public sealed class FormulaAttributionTrace
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

Consumer-owned evidence linking full formula attribution bytes to the
gameplay event that references their hash. This record is deliberately
excluded from authoritative battle state and its canonical hash.

**Constructors**

`public FormulaAttributionTrace()`

:   Pairs an attribution with the coordinates of the event that references it. Throws unless the event type is a formula-result event, the effect-entry and primitive coordinates match `attribution`, and `attributionHash` is the canonical hash of that attribution.
    - `tick` &mdash; Tick of the reduction that produced the evaluation.
    - `eventTypeId` &mdash; The referencing event type: `BattleIds.EffectMissed`, `BattleIds.DamageResolved` or `BattleIds.HealingResolved`.
    - `rootActionSequence` &mdash; Sequence number of the action whose resolution produced the evaluation; must be nonzero.
    - `primitiveIndex` &mdash; Position of the resolved primitive within its effect entry.
    - `attributionHash` &mdash; The hash the event carries; must equal the canonical hash of `attribution`.
    - `attribution` &mdash; Complete non-null evaluation record whose canonical bytes must hash to `attributionHash`.
    - `effectEntryId` &mdash; Valid effect-entry coordinate that must exactly match `FormulaAttribution.EffectEntryId` on the attribution.

**Properties**

`public FormulaAttribution Attribution`

:   The full account of the evaluation the referencing event only carries a hash of. Never null, and its canonical bytes are checked against `AttributionHash` on construction, so it can be presented as the arithmetic behind that event without re-deriving it.

`public Sha256Digest AttributionHash`

:   The hash the referencing event carries. It matches `Attribution`, which is checked on construction.

`public StableId EffectEntryId`

:   The effect entry being resolved. It always matches `FormulaAttribution.EffectEntryId` on `Attribution`, which construction checks.

`public StableId EventTypeId`

:   The formula-result event type that references this trace: `BattleIds.EffectMissed`, `BattleIds.DamageResolved` or `BattleIds.HealingResolved`.

`public int PrimitiveIndex`

:   Position of the resolved primitive within its effect entry.

`public ulong RootActionSequence`

:   Sequence number of the action whose resolution produced the evaluation. Use it to group every trace of one action together.

`public long Tick`

:   Tick of the reduction that produced the evaluation, which is the tick the referencing event was emitted on.

---

## FormulaAttributionTraceBatch

```csharp
public sealed class FormulaAttributionTraceBatch
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

Bounded immutable formula evidence returned to one consumer call.
OmittedCount is nonzero only when a long aggregate operation produced
more traces than the documented result-memory bound.

**Properties**

`public static FormulaAttributionTraceBatch Empty`

:   A shared batch holding no traces and nothing omitted, returned for an operation that recorded no formula evidence.

`public bool IsTruncated`

:   Whether anything was dropped, that is `OmittedCount` is not zero. Check it before treating `Traces` as the complete evidence for an operation.

`public long OmittedCount`

:   How many further traces the operation produced but the batch could not hold. It is nonzero only when a long aggregate operation ran past the result-memory bound; a single step never omits anything.

`public FrozenList<FormulaAttributionTrace> Traces`

:   The traces this call collected, in the order the engine recorded them, and never more than `SimulationLimits.FormulaAttributionTracesPerResult`.

---

## FormulaContext

```csharp
public sealed class FormulaContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Every input one formula evaluation is allowed to read, frozen before the
first draw. The authoritative reducer and preview build the same context
from the same builder, which is why a formula must derive its result from
this object alone and never from live state: a preview has no snapshot and
no RNG behind it.

**Constructors**

`public FormulaContext()`

:   Freezes one set of formula inputs. Modifiers may be supplied in any order; the constructor sorts them into canonical order.
    - `effectEntryId` &mdash; Authored effect entry this primitive belongs to.
    - `primitiveIndex` &mdash; Position of the primitive inside its effect plan, used to keep attribution and traces addressable.
    - `baseStat` &mdash; Current value of the authored source stat, before any modifier in modifiers has been applied.
    - `potency` &mdash; Skill potency multiplier, in Fixed64 raw units.
    - `defense` &mdash; Target defense reading, already zero when the primitive bypasses defense.
    - `hitChance` &mdash; Chance the primitive lands. Guaranteed and impossible both resolve without consuming a draw.
    - `criticalChance` &mdash; Chance of a critical result, already zero when criticals are disallowed for this primitive.
    - `criticalMultiplier` &mdash; Multiplier applied on a critical, after outgoing modifiers.
    - `varianceMinimum` &mdash; Inclusive low end of the seeded variance multiplier, in Fixed64 raw units. Must not be negative.
    - `varianceMaximum` &mdash; Inclusive high end of the same range. Bounds that are equal mean the evaluation consumes no variance draw.
    - `endpointMinimum` &mdash; Low end of the clamp applied after rounding.
    - `endpointMaximum` &mdash; High end of the clamp applied after rounding.
    - `modifiers` &mdash; Modifier inputs in any order. More entries than the attribution contribution limit are rejected.
    - `sourceId` &mdash; Valid combatant identifier supplying base stats and outgoing modifier inputs.
    - `targetId` &mdash; Valid combatant identifier supplying defense and incoming modifier inputs.

**Properties**

`public Fixed64 BaseStat`

:   Source stat value before any modifier in Modifiers is applied.

`public Chance64 CriticalChance`

:   Already zero when criticals are disallowed for this primitive, in which case no critical draw is consumed.

`public Fixed64 CriticalMultiplier`

:   The multiplier to apply when the critical roll succeeds, in Fixed64 raw units. The built-in formulas fold it in after the outgoing modifiers; whatever a formula does with it must end up inside `FormulaResult.Value`, since callers never apply it themselves.

`public Fixed64 Defense`

:   Target defense reading, already zero when this primitive bypasses defense.

`public StableId EffectEntryId`

:   The authored effect entry this evaluation belongs to. With `PrimitiveIndex` it addresses one exact primitive, which is how a trace points back at the content that produced it.

`public Fixed64 EndpointMaximum`

:   High end of the clamp applied to the rounded result.

`public Fixed64 EndpointMinimum`

:   Low end of the clamp applied to the rounded result.

`public Chance64 HitChance`

:   The chance this primitive lands. A guaranteed or impossible chance is resolved without a draw, which is why a formula's hit input is normally declared conditional.

`public FrozenList<FormulaModifierInput> Modifiers`

:   Modifier inputs in canonical order: priority, then status ID, then application sequence, then modifier index.

`public Fixed64 Potency`

:   The potency multiplier carried by the skill, in Fixed64 raw units where 10,000 equals 1.0. The built-in formulas apply it after the flat and multiplicative modifiers and before the outgoing ones.

`public int PrimitiveIndex`

:   Position of this primitive inside its effect plan.

`public StableId SourceId`

:   The combatant the evaluation is resolved from. It is carried into the attribution and the resulting event, so a recorded number can be traced back to who produced it.

`public StableId TargetId`

:   The combatant the evaluation is resolved against. Their defense and incoming modifiers have already been read into this context, so a formula never needs to look the combatant up - and could not, having no state view.

`public Fixed64 VarianceMaximum`

:   Inclusive high end of the seeded variance multiplier.

`public Fixed64 VarianceMinimum`

:   Inclusive low end of the seeded variance multiplier, in Fixed64 raw units. Equal bounds mean no variance draw.

---

## FormulaContribution

```csharp
public readonly struct FormulaContribution
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

One recorded step of a formula evaluation: the value that entered the
step and the value that left it. In the built-in formulas each step's
`Output` is the next step's `Input`, so reading
a contribution list in order replays the arithmetic that produced the
result.

**Constructors**

`public FormulaContribution()`

:   Records one step. Throws when `kind` is not a defined value or `sourceId` is invalid.
    - `sourceId` &mdash; What produced the step: the status definition behind a modifier, or the formula's own identifier for a step the formula performed.
    - `priority` &mdash; Ordering priority of the modifier that produced the step; zero for steps the formula performed itself.
    - `input` &mdash; Value entering the step.
    - `output` &mdash; Value leaving the step.
    - `kind` &mdash; Defined evaluation stage explaining how to interpret the source, priority, input, and output fields.

**Properties**

`public Fixed64 Input`

:   Value entering the step.

`public FormulaContributionKind Kind`

:   Which step of the evaluation this record stands for. It also says how to read `SourceId`: a modifier stage names the status behind the modifier, every other stage names the formula itself.

`public Fixed64 Output`

:   Value leaving the step.

`public int Priority`

:   Ordering priority of the modifier that produced the step; zero for steps the formula performed itself.

`public StableId SourceId`

:   What produced the step: the status definition behind a modifier, or the formula's own identifier for a step the formula performed.

---

## FormulaContributionKind

```csharp
public enum FormulaContributionKind : byte
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

Classifies individual formula contribution kind stages recorded by formula attribution. Each value identifies where an input changed the final fixed-point result.

| Value | Meaning |
| --- | --- |
| `BaseStat` | The unmodified value the formula started from. |
| `FlatModifier` | An additive modifier contributed by a status on the acting combatant. |
| `MultiplicativeModifier` | A multiplying modifier contributed by a status on the acting combatant, applied after the additive ones. |
| `Potency` | The potency multiplier carried by the effect being resolved. |
| `OutgoingModifier` | A multiplying modifier from a status on the acting combatant that scales what it deals, applied after potency. |
| `CriticalMultiplier` | The critical multiplier. |
| `Defense` | The reduction the target's defense applied. |
| `IncomingModifier` | A multiplying modifier from a status on the target that scales what it receives, applied after defense. |
| `Variance` | The variance multiplier for this evaluation, drawn from the variance range when that range is wider than a single value. |
| `Rounding` | Rounding of the unclamped value to a whole endpoint amount. |
| `Clamp` | The endpoint clamp. |

---

## FormulaEvaluationRequest

```csharp
public sealed class FormulaEvaluationRequest
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Formulas/BattleFormulaService.cs</small>

Immutable coordinates for one formula primitive. The same request can be
evaluated by the live reducer or previewed without consuming RNG.

**Constructors**

`public FormulaEvaluationRequest()`

:   Names one primitive to evaluate and the pair it runs between. Throws when any ID is invalid or when the primitive is not a damage or healing primitive.
    - `effectEntryId` &mdash; Authored effect entry the primitive was planned from.
    - `primitiveIndex` &mdash; Position of the primitive inside its effect plan. It must be below the planned-primitives-per-effect limit.
    - `primitive` &mdash; The planned primitive. Its tag must be CalculateAndDamage or CalculateAndHeal; any other tag is rejected.
    - `sourceId` &mdash; Valid combatant identifier whose stats and outgoing status modifiers feed the formula.
    - `targetId` &mdash; Valid combatant identifier whose defense, resistances, and incoming modifiers constrain the result.

**Properties**

`public StableId EffectEntryId`

:   Authored effect entry the primitive was planned from. It is carried into the result's attribution, so a number shown to a player can be traced back to the entry that produced it.

`public EffectPrimitive Primitive`

:   The planned primitive: the formula to run and the properties it reads, such as an overridden source stat, potency, hit chance, and whether a critical is allowed. Always a damage or healing primitive.

`public int PrimitiveIndex`

:   Position of this primitive inside its effect plan.

`public StableId SourceId`

:   The combatant the primitive acts from. Its stat supplies the base value the formula scales, and its statuses supply the outgoing and critical contributions.

`public StableId TargetId`

:   The combatant the primitive acts on. Its defence stat and its incoming modifiers are read unless the primitive bypasses them.

---

## FormulaModifierInput

```csharp
public readonly struct FormulaModifierInput
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

One status-supplied modifier already resolved into a formula input. The
ordering key - priority, then status ID, then application sequence, then
modifier index - is what makes a stack of modifiers apply in the same
order on every machine, and FormulaContext sorts by it on construction.

**Constructors**

`public FormulaModifierInput()`

:   Captures one modifier contribution and its deterministic sort key.
    - `kind` &mdash; Which formula stage consumes this modifier. Only the flat, multiplicative, outgoing, and incoming modifier kinds are accepted.
    - `priority` &mdash; Authored ordering weight inside the stage; lower sorts first.
    - `statusDefinitionId` &mdash; ID of the status that supplies the modifier.
    - `applicationSequence` &mdash; Application sequence of the status instance supplying the modifier, so older applications sort first. Zero is rejected.
    - `modifierIndex` &mdash; Position of the modifier inside its status definition's modifier list.
    - `value` &mdash; Added for a flat contribution and multiplied for a multiplicative one, in Fixed64 raw units where 10,000 equals 1.0.

**Properties**

`public ulong ApplicationSequence`

:   Application sequence of the status instance that supplies this modifier. Older applications sort ahead of newer ones.

`public FormulaContributionKind Kind`

:   Which stage of the formula consumes this modifier. Only the flat, multiplicative, outgoing, and incoming kinds can appear here; the other contribution kinds describe steps a formula performs itself rather than inputs a status supplies.

`public int ModifierIndex`

:   Position of the modifier within its status definition's modifier list, and the last tie-break in the canonical sort. Two modifiers from one status instance are separated only by this value.

`public int Priority`

:   Authored ordering weight within the stage, lower first. It is the first key in the canonical sort, so it decides order before the status ID and application sequence are consulted.

`public StableId StatusDefinitionId`

:   The status definition supplying the modifier, and the second sort key. Because it is a stable ID rather than a runtime reference, two modifiers of equal priority land in the same order on every machine.

`public Fixed64 Value`

:   Added for a flat contribution and multiplied for a multiplicative one, in Fixed64 raw units where 10,000 equals 1.0.

---

## FormulaPreview

```csharp
public sealed class FormulaPreview
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

What a formula would produce, reported for tooltips and other passive
display: the value range of a use that lands, plus the chances the
formula reports. A preview is computed without a random source, so
asking for one cannot draw from the battle RNG or advance the battle.

**Constructors**

`public FormulaPreview()`

:   Reports a forecast. Throws when `minimum` is greater than `maximum`.
    - `minimum` &mdash; Lowest value a use that lands can produce.
    - `maximum` &mdash; Highest value a use that lands can produce.
    - `statusChance` &mdash; Chance of an accompanying status application. The built-in damage and healing formulas leave this zero; status odds come from `BattleFormulaService.PreviewStatusApplication`.
    - `criticalChance` &mdash; Probability of the landing use receiving its critical multiplier, without consuming a preview-time draw.
    - `hitChance` &mdash; Probability that the use lands at all; the minimum and maximum describe only this successful-hit branch.

**Properties**

`public Chance64 CriticalChance`

:   Chance the use also rolls critical. The built-in damage formula derives `Maximum` with the critical roll assumed to succeed, so the upper bound already carries the critical multiplier and should not be scaled by it again.

`public Chance64 HitChance`

:   Chance the use lands at all. `Minimum` and `Maximum` describe only the landing case, so a tooltip that ignores this overstates what the use is worth on average.

`public bool IsExact`

:   Whether the forecast is a single value rather than a spread, that is `Minimum` equals `Maximum`. Show a range in a tooltip only when this is false.

`public Fixed64 Maximum`

:   Highest value a use that lands can produce.

`public Fixed64 Minimum`

:   Lowest value a use that lands can produce. A miss is reported by `HitChance`, not by this bound.

`public Chance64 StatusChance`

:   Chance of an accompanying status application. The built-in damage and healing formulas leave this zero; status odds come from `BattleFormulaService.PreviewStatusApplication`.

---

## FormulaPreviewContext

```csharp
public sealed class FormulaPreviewContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Marks an evaluation as a preview: the same inputs as the live call, but no
RNG and no state change. A preview that attempts a draw raises a
draw-contract diagnostic, so a formula must reach its answer analytically
or by evaluating a context whose chances and variance are pinned.

**Constructors**

`public FormulaPreviewContext(FormulaContext context)`

:   Wraps the inputs a preview is allowed to read.
    - `context` &mdash; Non-null frozen evaluation inputs exposed to preview logic without an authoritative RNG or mutable snapshot.

**Properties**

`public FormulaContext Context`

:   The same frozen inputs `IFormula.Evaluate` would read. Nothing here is a preview-specific variant, so a formula can reuse its evaluation path over a copy of this context with the chances and variance bounds pinned, which is how the built-in formulas produce a range without drawing.

---

## FormulaRandomBoundKind

```csharp
public enum FormulaRandomBoundKind : byte
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

How a declared random input states the exclusive upper bound its draw
will use.

| Value | Meaning |
| --- | --- |
| `Fixed` | A literal bound, known when content compiles. |
| `VarianceWidth` | The inclusive width of the evaluation context's variance range, so the bound is resolved per evaluation instead of being authored. |

---

## FormulaRandomInputDescriptor

```csharp
public readonly struct FormulaRandomInputDescriptor
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

One RNG draw a formula promises to take, in the order it will be taken.
The engine turns a formula's declared list into a cursor and walks it as
the formula evaluates, so this is a contract rather than a hint: bounds
must match, order must match, and a non-conditional entry that is never
drawn fails the step. Content compilation rejects more than eight inputs
for one formula, a duplicate input ID, or a zero fixed bound.

**Constructors**

`public FormulaRandomInputDescriptor(StableId inputId, uint exclusiveUpperBound, bool conditional)`

:   Declares a draw whose bound is known when content compiles.
    - `inputId` &mdash; Identifies the sample this draw produces in formula attribution. It must be unique among one formula's declared inputs.
    - `exclusiveUpperBound` &mdash; The bound the formula will pass to NextBelow. Zero is rejected.
    - `conditional` &mdash; True when the formula may legitimately skip this draw, as a guaranteed or impossible chance does. A non-conditional input must be drawn exactly once per evaluation.

**Properties**

`public FormulaRandomBoundKind BoundKind`

:   Whether the bound is the authored literal or the width of the evaluation context's variance range. Call `ResolveExclusiveUpperBound` instead of branching on this yourself; it handles both kinds.

`public bool Conditional`

:   True when the formula may skip this draw for some inputs. A non-conditional draw is mandatory on every evaluation.

`public uint ExclusiveUpperBound`

:   The authored bound for a Fixed input, and zero for a VarianceWidth input. Call ResolveExclusiveUpperBound rather than reading this when the bound kind is not known.

`public StableId InputId`

:   Names the sample this draw produces in formula attribution. It is what lets a recorded sample be matched back to the draw that took it, so it must be unique among one formula's declared inputs.

**Methods**

`public static FormulaRandomInputDescriptor ForVarianceWidth(StableId inputId, bool conditional)`

:   Declares a draw whose bound is the inclusive width of the evaluation context's variance range and therefore unknown until evaluation.
    - `inputId` &mdash; Identifies the sample this draw produces in formula attribution. It must be unique among one formula's declared inputs.
    - `conditional` &mdash; True when the formula may skip this draw, as equal variance bounds do.
    - **Returns** &mdash; A descriptor whose bound is resolved from each evaluation's inclusive variance width and whose fixed bound field is zero.

`public uint ResolveExclusiveUpperBound(FormulaContext context)`

:   Resolves the bound this draw must use for one evaluation: the authored bound for a Fixed input, or the inclusive raw width of the context's variance range for a VarianceWidth input.
    - `context` &mdash; Supplies the variance range. Required only for a VarianceWidth input; a Fixed input returns its authored bound without reading it.
    - **Returns** &mdash; The exclusive upper bound the next draw is expected to use.

---

## FormulaRandomSample

```csharp
public readonly struct FormulaRandomSample
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Trace/FormulaTrace.cs</small>

One random draw a formula took, recorded as the bound it asked for and
the raw value it received. A draw is recorded only where the formula
actually consumed randomness: a guaranteed or impossible chance is
resolved without drawing and leaves no sample behind.

**Constructors**

`public FormulaRandomSample(StableId inputId, uint exclusiveUpperBound, uint sample)`

:   Records one draw. Throws when `inputId` is invalid, the bound is zero, or the sample is not below the bound.
    - `inputId` &mdash; Which random input declared by the formula this draw belongs to.
    - `exclusiveUpperBound` &mdash; The bound the formula asked the random source for.
    - `sample` &mdash; The raw value returned, always below the bound.

**Properties**

`public uint ExclusiveUpperBound`

:   The bound the formula asked the random source for.

`public StableId InputId`

:   Which random input declared by the formula this draw belongs to.

`public uint Sample`

:   The raw value drawn. Read it against `ExclusiveUpperBound`; it is not a probability.

---

## FormulaResult

```csharp
public sealed class FormulaResult
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

What one formula evaluation produced: whether it landed, whether it crit,
the final clamped magnitude, and the attribution the engine hashes into
the resulting event. Value is a magnitude rather than a delta - how much
of it shields and health absorb is the engine's decision, not the
formula's.

**Constructors**

`public FormulaResult(bool hit, bool critical, Fixed64 value, FormulaAttribution attribution)`

:   Records one evaluation outcome together with its evidence.
    - `hit` &mdash; False makes the engine emit a miss and ignore value.
    - `critical` &mdash; Reported to callers and traces. Any critical multiplier must already be folded into value.
    - `value` &mdash; Result after rounding and endpoint clamping.
    - `attribution` &mdash; Required. The ordered contributions and the samples actually consumed; the engine hashes it into the battle event.

**Properties**

`public FormulaAttribution Attribution`

:   The ordered contributions the formula applied and the samples it actually drew. The engine hashes this into the battle event, so it is part of the recorded outcome rather than optional debug detail: an account that does not match the arithmetic produces an event that will not reconcile on replay.

`public bool Critical`

:   Whether the evaluation crit. It reaches callers and traces only: the critical multiplier is already folded into `Value` and must not be applied a second time.

`public bool Hit`

:   Whether the primitive landed. False makes the engine emit a miss and disregard `Value`, so a miss is reported here rather than as a zero result.

`public Fixed64 Value`

:   Magnitude after rounding and endpoint clamping. Zero on a miss, and still subject to shield absorption and health limits when applied.

---

## FormulaValidationContext

```csharp
public sealed class FormulaValidationContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Read-only catalog passed to IFormula.Validate while compiled content is
being built. A formula checks its authored PropertySet against this
catalog; any error in the returned report aborts compilation. No
snapshot and no RNG are reachable from here.

**Constructors**

`public FormulaValidationContext(CompiledBattleContent content)`

:   Binds the context to the catalog being compiled.
    - `content` &mdash; Non-null compiled catalog against which formula property IDs and referenced definitions are checked.

**Properties**

`public CompiledBattleContent Content`

:   The catalog an authored property value must resolve against - a stat, resource, or skill the formula was configured to read. It is the only state a validating formula can reach, so a check that would need a live battle belongs in `IFormula.Evaluate` instead.

---

## IAiPolicy

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IAiPolicy : IMechanicsImplementation
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Proposes, in preference order, the skill uses an AI-controlled combatant
would like to make. The engine then puts each candidate through the same
preflight a player command goes through and acts on the first one that
survives.

!!! note "Remarks"
    A policy describes intent only: it cannot draw RNG, submit a command, or
    mutate state. Because the engine takes the first legal candidate, the
    returned order is the decision, and it must be deterministic - never
    dependent on dictionary or hash-set enumeration order. Every candidate must
    name a rule that exists in the policy definition and the skill that rule
    declares; a candidate that does not is rejected and traced.

**Properties**

`public int AiContractVersion`

:   Contract version. It must equal ContractVersion or registration fails.

`public StableId PolicyId`

:   Registry identity. It must equal ImplementationId or registration fails.

**Methods**

`public AiCandidatePlan BuildCandidates(AiContext context, PropertySet properties)`

:   Derives build candidates from the supplied immutable context. Missing or illegal inputs produce the contract's typed empty/failure result.
    - `context` &mdash; Actor, the compiled policy definition with its rules, catalog, and a read-only state view.
    - `properties` &mdash; Authored configuration for this policy use.
    - **Returns** &mdash; Candidates in preference order, within the per-decision candidate limit. Returning null fails the decision.

`public ValidationReport Validate(AiValidationContext context, PropertySet properties)`

:   Checks one authored property set while content compiles. Any error in the returned report aborts compilation.
    - `context` &mdash; Catalog the properties refer into.
    - `properties` &mdash; Authored configuration for this policy use.
    - **Returns** &mdash; Errors and warnings. Must not be null.

---

## IEffectResolver

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IEffectResolver : IMechanicsImplementation
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Expands one authored effect entry into the ordered primitives the engine
will execute: damage, healing, resource change, shield, status apply or
remove, dispel, scheduler adjustment, interrupt. A resolver decides what
should happen; the engine decides how much of it actually lands.

!!! note "Remarks"
    Plan must be a pure function of its context and properties: no RNG, no
    mutation of state, no events. It can be called more than once for the same
    action - target fallback re-plans the remaining suffix from the current
    state - so the same inputs must yield the same primitives in the same
    order. State arrives as a read-only view; the authoritative snapshot is
    deliberately not reachable.

**Properties**

`public int EffectContractVersion`

:   Contract version. It must equal ContractVersion or registration fails.

`public StableId ResolverId`

:   Registry identity. It must equal ImplementationId or registration fails.

**Methods**

`public EffectPlan Plan(EffectPlanningContext context, PropertySet properties)`

:   Derives plan from the supplied immutable context. Missing or illegal inputs produce the contract's typed empty/failure result.
    - `context` &mdash; Source, target, effect entry ID, catalog, and a read-only state view.
    - `properties` &mdash; Authored configuration for this effect entry.
    - **Returns** &mdash; An ordered plan within the per-effect primitive limit; it must not be null. A plan carrying diagnostics fails the step with the first of them and restores the snapshot the engine started from.

`public ValidationReport Validate(EffectValidationContext context, PropertySet properties)`

:   Checks one authored property set while content compiles. Any error in the returned report aborts compilation.
    - `context` &mdash; Catalog the properties refer into.
    - `properties` &mdash; Authored configuration for this effect entry.
    - **Returns** &mdash; Errors and warnings. Must not be null.

---

## IFormula

:material-star: **Start here** &middot; :material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IFormula : IMechanicsImplementation
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Turns battle inputs into a damage or healing number. This is the main
extension point for changing how combat maths feel: register an
implementation, and any authored effect can reference it by ID and
version. The built-in standard damage, healing, and scalar formulas are
registered through the same interface, with no privileged path.

!!! note "Remarks"
    A formula is the only mechanics extension allowed to consume RNG, and it
    must consume exactly the draws it declared, in the declared order. It must
    be stateless and deterministic - no floating point, no clock, no Unity
    API, no per-instance mutation - because the same call is made again during
    replay, forecast, and batch analysis and must return the same result.
    Content compilation calls Validate, DescribeRandomInputs, and Preview once
    per authored use and refuses to compile if any of them throws or returns
    null. A failure raised later, during Evaluate, restores the snapshot the
    engine started the call from and reports a fatal invariant.

**Properties**

`public int FormulaContractVersion`

:   Contract version. It must equal ContractVersion or registration fails.

`public StableId FormulaId`

:   Registry identity. It must equal ImplementationId or registration fails.

**Methods**

`public FrozenList<FormulaRandomInputDescriptor> DescribeRandomInputs(PropertySet properties)`

:   Declares every draw Evaluate may take for these properties, in the order it will take them. The engine builds its draw cursor from this list, and content compilation rejects more than eight entries or a duplicate input ID.
    - `properties` &mdash; Authored configuration for this use of the formula.
    - **Returns** &mdash; The declared draws in evaluation order, or an empty list when the formula never draws. Must not be null.

`public FormulaResult Evaluate(FormulaContext context, PropertySet properties, IMechanicsRandomSource random)`

:   Produces the authoritative result for one primitive. Read inputs from context only, take draws in declared order, and report the contributions and samples actually used in the result's attribution.
    - `context` &mdash; Frozen inputs for this evaluation.
    - `properties` &mdash; Authored configuration for this use of the formula.
    - `random` &mdash; Engine-owned draw cursor, valid only for the duration of this call. It must not be stored, shared, or used after returning.
    - **Returns** &mdash; Hit, critical, final magnitude, and attribution. Must not be null.

`public FormulaPreview Preview(FormulaPreviewContext context, PropertySet properties)`

:   Reports the range the same inputs could produce, without drawing and without changing anything. Tooltips, range previews, and the Workbench call this; a draw attempted here fails, so pin the context instead - the built-in formulas evaluate twice with the variance bounds held equal.
    - `context` &mdash; Preview wrapper around the inputs Evaluate would read.
    - `properties` &mdash; Authored configuration for this use of the formula.
    - **Returns** &mdash; Minimum and maximum results plus the chances shown to a player. Must not be null, and the range must cover every value Evaluate can return for those inputs.

`public ValidationReport Validate(FormulaValidationContext context, PropertySet properties)`

:   Checks one authored property set while content compiles. Return ValidationReport.Valid when every key is understood and in range; any error aborts compilation and surfaces the diagnostic you returned.
    - `context` &mdash; Catalog the properties refer into.
    - `properties` &mdash; Authored configuration for this use of the formula.
    - **Returns** &mdash; Errors and warnings. Must not be null.

---

## IMechanicsImplementation

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IMechanicsImplementation
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Identity carried by every mechanics extension registered in a
BattleMechanicsRegistry. Implementations are resolved by exact ID and
contract version, never by an implicit latest-version fallback, so
changing behaviour means registering a new version rather than editing
a shipped one.

!!! note "Remarks"
    An implementation must be stateless and deterministic: one registry may
    be shared by concurrently running engines, and identical inputs must
    produce identical results on every machine and on every replay. An
    extension returns immutable descriptions only; it must not mutate a
    snapshot, emit events, advance the scheduler, submit commands, retain an
    RNG instance, or let its collection order depend on hashing.

**Properties**

`public int ContractVersion`

:   Positive version matched exactly at resolution. It must equal the category version alias on the same object.

`public StableId ImplementationId`

:   Registry identity. It must equal the category alias on the same object - FormulaId, ResolverId, or PolicyId - or registration fails.

---

## IMechanicsRandomSource

```csharp
public interface IMechanicsRandomSource
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

The engine-owned draw cursor handed to a formula for one evaluation.
Every draw is checked against that formula's declared random inputs, so
an undeclared bound or an out-of-order draw fails the step instead of
silently diverging a replay. Formulas are the only extensions that
receive an RNG, and the instance must not outlive the call it arrived on.

**Properties**

`public int DrawCount`

:   Draws consumed from this source so far. A preview source stays at zero because previewing may not draw at all.

**Methods**

`public uint NextBelow(uint exclusiveUpperBound)`

:   Consumes the next declared draw and returns a uniform value in the range 0 (inclusive) to exclusiveUpperBound (exclusive).
    - `exclusiveUpperBound` &mdash; Must match the bound declared for this position by DescribeRandomInputs. A mismatch that cannot be skipped as a conditional input raises a draw-contract diagnostic.
    - **Returns** &mdash; A value below the bound, taken from authoritative battle RNG.

---

## IReactionRule

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface IReactionRule : IMechanicsImplementation
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Decides whether a queued reaction actually fires when a tagged effect
resolves, and which pair of combatants it fires between. Reaction rules are
the counter-attack and on-hit layer; the engine keeps them terminating with
depth, count, and once-per-root budgets.

!!! note "Remarks"
    Signature is what lets bounded reactions be proven before a battle runs:
    content compilation builds a graph from each rule's declared emitted tags
    to every rule's declared trigger tags and refuses cycles it cannot bound.
    Declare every tag the rule can emit - declaring extra tags is merely
    conservative, declaring too few defeats the analysis. Evaluate itself is
    pure: no RNG, no mutation, no events.

**Properties**

`public int ReactionContractVersion`

:   Contract version. It must equal ContractVersion or registration fails.

`public ReactionSignature Signature`

:   The effect tags this rule reacts to and the effect tags it can emit. It must not be null and must declare at least one trigger tag; compilation rejects the rule otherwise.

**Methods**

`public ReactionEvaluation Evaluate(ReactionContext context, PropertySet properties)`

:   Decides eligibility for one candidate reaction and names the source and target it will use, which need not be the pair that triggered it.
    - `context` &mdash; The triggering effect tag, trigger phase, root action sequence, current reaction depth, catalog, and a read-only state view.
    - `properties` &mdash; Authored configuration for this reaction definition.
    - **Returns** &mdash; An eligible evaluation, or an ineligible one carrying the reason. Must not be null; declining to fire is a normal outcome, not an error.

`public ValidationReport Validate(ReactionValidationContext context, PropertySet properties)`

:   Checks one authored property set while content compiles. Any error in the returned report aborts compilation.
    - `context` &mdash; Catalog the properties refer into.
    - `properties` &mdash; Authored configuration for this reaction definition.
    - **Returns** &mdash; Errors and warnings. Must not be null.

---

## ITargetResolver

:material-puzzle: **Extension point** &mdash; implement this yourself to change behaviour

```csharp
public interface ITargetResolver : IMechanicsImplementation
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Decides which combatants a skill may hit and whether the targets a player
or an AI asked for are legal. Selection is split in three: a request
contract the engine enforces before asking the resolver anything, a
candidate set, and validation of the actual request.

!!! note "Remarks"
    Neither method may draw RNG or mutate state. The engine performs random
    selection itself, without replacement, over the sorted candidate set, so a
    "random" resolver declares a count rather than picking. Candidates are
    deduplicated, StableId-sorted, and bounded by the engine afterwards, so
    return order does not affect the battle - but every ID must be valid and
    the count must stay inside the resolved-target limit, or the command is
    rejected.

**Properties**

`public TargetRequestContract RequestContract`

:   The request shape the engine enforces before this resolver is consulted: how many IDs may be requested, whether an empty request means automatic selection, how many random picks the engine makes, and which combatants are eligible. It must not be null and must not describe a different shape from one call to the next.

`public StableId ResolverId`

:   Registry identity. It must equal ImplementationId or registration fails.

`public int TargetContractVersion`

:   Contract version. It must equal ContractVersion or registration fails.

**Methods**

`public FrozenList<StableId> GetCandidates(TargetContext context, PropertySet properties)`

:   Lists every combatant this resolver currently considers eligible. Called before taunt-style restrictions narrow the set and before any requested IDs are validated.
    - `context` &mdash; Actor, skill, catalog, and a read-only state view.
    - `properties` &mdash; Authored configuration for this resolver use.
    - **Returns** &mdash; Candidate IDs in any order; the engine sorts and deduplicates them. An empty result means the skill has no legal target right now.

`public ValidationReport Validate(TargetValidationContext context, PropertySet properties)`

:   Checks one authored property set while content compiles. Any error in the returned report aborts compilation.
    - `context` &mdash; Catalog the properties refer into.
    - `properties` &mdash; Authored configuration for this resolver use.
    - **Returns** &mdash; Errors and warnings. Must not be null.

`public TargetRequestResult ValidateRequested(TargetContext context, PropertySet properties, FrozenList<StableId> requested)`

:   Accepts or rejects a request and returns the set the engine should lock. A rejection here is an ordinary command rejection, not an error.
    - `context` &mdash; Actor, skill, catalog, and a read-only state view.
    - `properties` &mdash; Authored configuration for this resolver use.
    - `requested` &mdash; Exactly what the command asked for, in authored order. Empty means the caller wants automatic selection: when the request contract allows that, accept the automatic set, or accept an empty set when the contract declares a random count, because the engine owns those draws.
    - **Returns** &mdash; An accepted result carrying the targets to lock, or a rejection carrying the diagnostic reported to the caller. Must not be null.

---

## MechanicsCategoryTag

```csharp
public enum MechanicsCategoryTag : byte
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/BattleMechanicsRegistry.cs</small>

Which of the five mechanics extension interfaces an implementation was
registered under. A registry entry is keyed by category, ID, and contract
version together, so naming the right ID under the wrong category is
reported as a wrong-category diagnostic rather than as a missing entry.

| Value | Meaning |
| --- | --- |
| `Formula` | An IFormula: turns battle inputs into a number. |
| `Effect` | An IEffectResolver: expands an authored effect entry into primitives. |
| `Target` | An ITargetResolver: decides which combatants a skill may hit. |
| `Ai` | An IAiPolicy: proposes skill uses in preference order. |
| `Reaction` | An IReactionRule: decides whether a queued reaction fires. |

---

## MechanicsDiagnosticIds

```csharp
public static class MechanicsDiagnosticIds
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsDiagnostics.cs</small>

The IDs the mechanics layer reports its diagnostics under: registry binding
failures, rejected authored properties, missing or over-large content, formula
contract violations, unusable effect plans, structural limits, and the reasons a
reaction or AI candidate was declined.

A `Diagnostic` is identified by its ID rather than by its text, so
comparing against these constants is how a caller tells one failure from another
without parsing messages. Not all of them are errors: the condition-false and
once-per-root entries name ordinary outcomes that a rule is expected to report
when it declines. A custom formula, effect resolver, target resolver, AI policy, or
reaction rule should reuse these IDs so it refuses in the same vocabulary the
built-in mechanics use.

**Fields**

`public static readonly StableId AiConditionFalse`

:   Expected policy-decline code when a deterministic AI condition rejects the current actor, skill, target set, or battle state.

`public static readonly StableId AiPlanInvalid`

:   Automatic-decision code when a policy emits an unusable skill, malformed targets, or another command plan that cannot be validated.

`public static readonly StableId ContentInvalid`

:   General compilation code for structurally inconsistent mechanics content not covered by a more precise property or reference code.

`public static readonly StableId ContentLimitExceeded`

:   Compilation code when an authored mechanics collection exceeds its documented deterministic structural limit.

`public static readonly StableId ContentReferenceMissing`

:   Compilation code when authored mechanics content names a formula, effect, status, skill, stat, or other definition absent from the catalog.

`public static readonly StableId EffectPlanInvalid`

:   Runtime code when an effect resolver produces null, malformed, over-large, or semantically invalid primitive instructions.

`public static readonly StableId FormulaDrawContract`

:   Runtime code when a formula consumes a different number of RNG draws than its registered draw contract declares.

`public static readonly StableId FormulaInvariant`

:   Runtime code when a resolved formula violates its value-domain contract or returns an otherwise impossible deterministic result.

`public static readonly StableId PrimitiveExecutionLimitExceeded`

:   Safety-budget code when one root action would execute more effect primitives than the simulation permits.

`public static readonly StableId PropertyMissing`

:   Content-validation code when a formula, effect, resolver, reaction, or policy omits a required authored property.

`public static readonly StableId PropertyRangeInvalid`

:   Content-validation code when a correctly typed property lies outside the implementation's supported numeric or cardinality bounds.

`public static readonly StableId PropertyTagInvalid`

:   Content-validation code when a known property key carries a value of the wrong union tag, such as an ID where an integer is required.

`public static readonly StableId PropertyUnknown`

:   Content-validation code when a property set contains a key that its selected mechanics implementation does not recognize.

`public static readonly StableId ReactionConditionFalse`

:   Expected decline code when the reaction rule's deterministic condition does not match the triggering event and snapshot.

`public static readonly StableId ReactionCountLimit`

:   Suppression code when a root action has already queued the maximum permitted number of reactions.

`public static readonly StableId ReactionDefinitionMissing`

:   Resolution code when a queued reaction references a rule or action definition absent from the compiled mechanics catalog.

`public static readonly StableId ReactionDepthLimit`

:   Suppression code when enqueuing a reaction would exceed the maximum nesting depth for its root action.

`public static readonly StableId ReactionOncePerRoot`

:   Expected decline code when a rule marked once-per-root has already fired anywhere in the same action cascade.

`public static readonly StableId ReactionSignatureUnsafe`

:   Compilation code when a reaction can reproduce its own trigger signature without a once-per-root or other terminating guard.

`public static readonly StableId ReactionSourceInvalid`

:   Expected decline or validation code when a reaction cannot derive a valid living source under its source-selection policy.

`public static readonly StableId ReactionTargetInvalid`

:   Expected decline or validation code when a reaction cannot derive targets satisfying its target-selection contract.

`public static readonly StableId RegistryDuplicate`

:   Registration failure code when the same mechanics ID, category, and contract version tuple is already bound.

`public static readonly StableId RegistryEntryInvalid`

:   Registration failure code for a null implementation, invalid ID, undefined mechanics category, or non-positive contract version.

`public static readonly StableId RegistryMissing`

:   Resolution failure code when no implementation exists under the requested stable mechanics identifier.

`public static readonly StableId RegistryVersionUnsupported`

:   Resolution failure code when the requested mechanics identifier and category exist but not at the required contract version.

`public static readonly StableId RegistryWrongCategory`

:   Resolution failure code when an identifier is registered, but only for a mechanics category other than the requested one.

`public static readonly StableId ShieldLimitExceeded`

:   Safety-limit code when adding a shield would exceed the bounded number of live shield applications.

`public static readonly StableId StatusLimitExceeded`

:   Safety-limit code when applying a status would exceed the per-combatant or battle-wide live status capacity.

`public static readonly StableId TargetRequestInvalid`

:   Command-validation code when requested target IDs violate the selected resolver's count, eligibility, uniqueness, or ordering contract.

---

## MechanicsIds

```csharp
public static class MechanicsIds
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsIds.cs</small>

The stable IDs the shipped formulas, effect resolvers, target resolvers, AI
policies, and reaction rules register themselves under, together with the property
keys those implementations read out of authored content and the input names they
attribute formula contributions to.

An implementation is found by ID and contract version, never by C# type name, so
these are the exact values authored content has to carry to reach the built-in
mechanics. Quoting a member here rather than retyping its string turns a typo into
a compile error instead of a missing-implementation diagnostic much later. A custom
implementation that wants to accept the same authored arguments should reuse the
property keys rather than invent its own spelling of them.

**Fields**

`public static readonly StableId AdjustSchedulerEffect`

:   Effect-resolver key that emits a deterministic scheduler adjustment for a combatant.

`public static readonly StableId AllAlliesTarget`

:   Target-resolver key that returns every eligible ally in canonical order.

`public static readonly StableId AllCombatantsTarget`

:   Target-resolver key that returns all eligible combatants across both sides.

`public static readonly StableId AllEnemiesTarget`

:   Target-resolver key that returns every eligible enemy in canonical order.

`public static readonly StableId ApplyStatusEffect`

:   Effect-resolver key that attempts to attach a status definition to a target.

`public static readonly StableId CompositeEffectExample`

:   Effect-resolver key reserved for the sample composite-effect implementation.

`public static readonly StableId ConditionalAi`

:   AI-policy key that evaluates authored conditions before choosing an action.

`public static readonly StableId CustomAiExample`

:   AI-policy key reserved for the sample custom decision implementation.

`public static readonly StableId CustomFormulaExample`

:   Registry key reserved for the sample custom formula implementation.

`public static readonly StableId CustomReactionExample`

:   Reaction-rule key reserved for the sample custom reaction implementation.

`public static readonly StableId CustomTargetExample`

:   Target-resolver key reserved for the sample custom targeting implementation.

`public static readonly StableId DamageEffect`

:   Effect-resolver key that calculates and applies hit-point damage.

`public static readonly StableId DispelEffect`

:   Effect-resolver key that removes statuses matching polarity, tags, and count filters.

`public static readonly StableId EffectTagReaction`

:   Reaction-rule key that responds when an emitted effect tag matches its authored trigger.

`public static readonly StableId FormationRowTarget`

:   Target-resolver key that expands a selected combatant to its formation row.

`public static readonly StableId FormationSideTarget`

:   Target-resolver key that expands a selected combatant to its full formation side.

`public static readonly StableId FormulaInputBaseStat`

:   Formula-trace input label for the source statistic before potency and modifiers.

`public static readonly StableId FormulaInputCriticalChance`

:   Formula-trace input label for the evaluated critical probability.

`public static readonly StableId FormulaInputCriticalMultiplier`

:   Formula-trace input label for the multiplier applied after a critical roll succeeds.

`public static readonly StableId FormulaInputDefense`

:   Formula-trace input label for the target defense value used by mitigation.

`public static readonly StableId FormulaInputEndpointMaximum`

:   Formula-trace input label for the inclusive upper endpoint of a bounded result.

`public static readonly StableId FormulaInputEndpointMinimum`

:   Formula-trace input label for the inclusive lower endpoint of a bounded result.

`public static readonly StableId FormulaInputHitChance`

:   Formula-trace input label for the probability tested by the hit roll.

`public static readonly StableId FormulaInputPotency`

:   Formula-trace input label for the authored fixed-point potency multiplier.

`public static readonly StableId FormulaInputVarianceMaximum`

:   Formula-trace input label for the upper bound of deterministic result variance.

`public static readonly StableId FormulaInputVarianceMinimum`

:   Formula-trace input label for the lower bound of deterministic result variance.

`public static readonly StableId HealEffect`

:   Effect-resolver key that calculates and applies hit-point restoration.

`public static readonly StableId InterruptEffect`

:   Effect-resolver key that interrupts a pending scheduled action.

`public static readonly StableId OneAllyTarget`

:   Target-resolver key that selects one living ally, including the actor when eligible.

`public static readonly StableId OneEnemyTarget`

:   Target-resolver key that selects one living opposing combatant.

`public static readonly StableId OneOtherAllyTarget`

:   Target-resolver key that selects one living ally other than the actor.

`public static readonly StableId PriorityAi`

:   AI-policy key that chooses the first usable action in authored priority order.

`public static readonly StableId PropertyAdjustmentKind`

:   Authored property key selecting the scheduler operation applied by an adjustment effect.

`public static readonly StableId PropertyAllowCritical`

:   Authored property key indicating whether a damage or healing effect may critically resolve.

`public static readonly StableId PropertyAmount`

:   Authored property key carrying a fixed-point quantity applied by an effect.

`public static readonly StableId PropertyBypassDefense`

:   Authored property key indicating that damage skips the defense formula.

`public static readonly StableId PropertyBypassIncomingModifiers`

:   Authored property key indicating that target-side incoming modifiers are ignored.

`public static readonly StableId PropertyBypassShield`

:   Authored property key indicating that damage applies directly without consuming shields.

`public static readonly StableId PropertyChance`

:   Authored property key carrying the probability of status application or another conditional effect.

`public static readonly StableId PropertyDelta`

:   Authored property key carrying a signed resource or scheduler adjustment.

`public static readonly StableId PropertyEmitTag`

:   Authored property key naming the tag emitted by a reaction-produced effect.

`public static readonly StableId PropertyFormationId`

:   Authored property key naming the formation used by row- or side-based targeting.

`public static readonly StableId PropertyFormulaId`

:   Authored property key naming the formula implementation used by an effect.

`public static readonly StableId PropertyFormulaVersion`

:   Authored property key carrying the requested formula contract version.

`public static readonly StableId PropertyHitChance`

:   Authored property key carrying the base probability that an effect hits.

`public static readonly StableId PropertyLinkedStatusId`

:   Authored property key linking a shield or effect to a status identity.

`public static readonly StableId PropertyMaximumCount`

:   Authored property key limiting how many matching statuses a dispel may remove.

`public static readonly StableId PropertyPolarity`

:   Authored property key selecting beneficial, harmful, or neutral status polarity.

`public static readonly StableId PropertyPotency`

:   Authored property key carrying the fixed-point potency multiplier.

`public static readonly StableId PropertyPriority`

:   Authored property key carrying deterministic ordering priority for shields or reactions.

`public static readonly StableId PropertyReasonId`

:   Authored property key naming the deterministic reason recorded with a scheduler change.

`public static readonly StableId PropertyResourceId`

:   Authored property key naming the combatant resource changed by an effect.

`public static readonly StableId PropertyShieldId`

:   Authored property key naming the shield pool to create or change.

`public static readonly StableId PropertySourceStatId`

:   Authored property key naming the source combatant stat supplied to a formula.

`public static readonly StableId PropertyStatusId`

:   Authored property key naming the status definition to apply or remove.

`public static readonly StableId PropertyTags`

:   Authored property key carrying the tag set used by filtering and reactions.

`public static readonly StableId PropertyTargetCount`

:   Authored property key limiting or requesting the number of resolved targets.

`public static readonly StableId PropertyTeamScope`

:   Authored property key scoping a formation row or side to one team. Optional; omitting it keeps the board-wide behaviour, which is what a battlefield hazard wants and what a sword swing does not.

`public static readonly StableId PropertyTriggerTag`

:   Authored property key naming the effect tag that activates a reaction rule.

`public static readonly StableId RandomAllTarget`

:   Target-resolver key that samples from all eligible combatants with the battle RNG.

`public static readonly StableId RandomAllyTarget`

:   Target-resolver key that samples one eligible ally with the battle RNG.

`public static readonly StableId RandomEnemyTarget`

:   Target-resolver key that samples one eligible enemy with the battle RNG.

`public static readonly StableId RemoveStatusEffect`

:   Effect-resolver key that removes instances of one authored status identity.

`public static readonly StableId ResourceEffect`

:   Effect-resolver key that changes a combatant's named resource by an authored delta.

`public static readonly StableId SelfTarget`

:   Target-resolver key that returns only the acting combatant.

`public static readonly StableId ShieldEffect`

:   Effect-resolver key that adds or updates a named damage-absorbing shield.

`public static readonly StableId StandardCriticalFormula`

:   Registry key selecting the shipped critical-hit chance and multiplier calculation.

`public static readonly StableId StandardDamageFormula`

:   Registry key selecting the shipped damage calculation from potency, offense, defense, variance, and critical inputs.

`public static readonly StableId StandardDefenseFormula`

:   Registry key selecting the shipped defense mitigation calculation.

`public static readonly StableId StandardHealingFormula`

:   Registry key selecting the shipped healing calculation from potency, source stat, and variance inputs.

`public static readonly StableId StandardStatusChanceFormula`

:   Registry key selecting the shipped status-application probability calculation.

`public static readonly StableId TeamScopeAllies`

:   Value for `PropertyTeamScope`: only the actor's own side.

`public static readonly StableId TeamScopeAny`

:   Value for `PropertyTeamScope`: everyone in the row or side, both teams. The default.

`public static readonly StableId TeamScopeEnemies`

:   Value for `PropertyTeamScope`: only combatants opposing the actor.

`public static readonly StableId WeightedAi`

:   AI-policy key that samples among usable actions by deterministic authored weights.

---

## MechanicsRegistryBinding

```csharp
public readonly struct MechanicsRegistryBinding : IEquatable<MechanicsRegistryBinding>
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/BattleMechanicsRegistry.cs</small>

The full key one registry entry is filed under: category, implementation
ID, and contract version. All three take part in equality, so a second
version of the same ID is a separate entry that lives alongside the first
instead of replacing it.

**Constructors**

`public MechanicsRegistryBinding(MechanicsCategoryTag category, StableId implementationId, int contractVersion)`

:   Builds a binding key, rejecting an undefined category, an invalid implementation ID, or a version that is not positive.
    - `contractVersion` &mdash; Matched exactly at resolution; there is no latest-version fallback. Must be greater than zero.
    - `category` &mdash; Defined mechanics interface family under which resolution must search.
    - `implementationId` &mdash; Valid persistence-safe registry key recorded by compiled content and replay data.

**Properties**

`public MechanicsCategoryTag Category`

:   Which extension interface the implementation was filed under. Lookups match on it as well as the ID, so the same ID may be registered once in each category without the two entries colliding.

`public int ContractVersion`

:   Contract version matched exactly at resolution, never approximately.

`public StableId ImplementationId`

:   The ID compiled content and replays record in place of a type name. Renaming or moving the implementing class leaves stored content readable; changing this ID does not.

**Methods**

`public bool Equals(MechanicsRegistryBinding other)`

:   Compares category, implementation ID, and contract version; two bindings are equal only when all three match.
    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Compares against a boxed binding on the same three parts. Anything that is not a binding is unequal, including null.
    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override int GetHashCode()`

:   Mixes all three parts of the key, so two registrations of the same ID at different contract versions do not share a bucket.
    - **Returns** &mdash; A deterministic hash code for this value.

---

## MechanicsResolveResult

```csharp
public sealed class MechanicsResolveResult
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/BattleMechanicsRegistry.cs</small>

The outcome of one registry lookup: either the implementation or the
diagnostic explaining why it could not be resolved, never both. Only the
registry creates these, so a result is always in one of those two shapes
and is never null.

**Properties**

`public Diagnostic Diagnostic`

:   Why the lookup failed. On success this is the default Diagnostic, whose Id is not valid.

`public T Implementation`

:   The resolved implementation, or null when the lookup failed.

`public bool IsSuccess`

:   Whether the lookup produced an implementation. Test it before reading `Implementation`; when it is false the reason is in `Diagnostic`.

---

## ReactionValidationContext

```csharp
public sealed class ReactionValidationContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Read-only catalog passed to IReactionRule.Validate while compiled content
is being built. A rule checks its authored PropertySet against this
catalog - including that authored trigger and emit tags stay inside its
declared signature - and any error aborts compilation.

**Constructors**

`public ReactionValidationContext(CompiledBattleContent content)`

:   Binds the context to the catalog being compiled.
    - `content` &mdash; Non-null compiled catalog used to verify reaction properties, references, and signature-covered tags.

**Properties**

`public CompiledBattleContent Content`

:   The catalog an authored property value must resolve against, and the reference point for the check that authored trigger and emit tags stay inside the rule's declared `IReactionRule.Signature`. Letting a tag slip past that check is what would defeat the compile-time bounding of reaction chains.

---

## SchedulerAdjustmentKind

```csharp
public enum SchedulerAdjustmentKind : byte
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Effects/EffectPlan.cs</small>

The timing value an AdjustScheduler primitive moves. A scheduler
advertises which kinds its adjustment adapter supports, so a plan can
only use the kind that matches the scheduler the battle runs.

| Value | Meaning |
| --- | --- |
| `ReadyTickDelta` | Moves the actor's ready tick by the delta - negative acts sooner - and never earlier than the current tick. |
| `GaugeDelta` | Moves the actor's gauge by the delta in gauge units, clamped to zero and to the fill threshold; a positive delta that reaches the threshold grants a ready opportunity at the curren... |

---

## StatusApplicationPreview

```csharp
public sealed class StatusApplicationPreview
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Formulas/BattleFormulaService.cs</small>

RNG-free status application calculation used by runtime and tooltips.

**Properties**

`public Chance64 BaseChance`

:   Chance authored on the applying effect, before resistance and immunity are considered.

`public Chance64 FinalChance`

:   Base chance after resistance, and zero whenever `Immune` is true. This is the chance the engine rolls against.

`public bool Immune`

:   True when the target's definition is immune to this status by ID or by one of its tags. The application is refused outright rather than rolled.

`public Chance64 Resistance`

:   The target's matching resistances summed and clamped to at most 100%. Entries that match the status by definition and entries that match one of its tags both count, and it is still reported when the target turns out to be immune.

`public StableId StatusId`

:   The status definition whose odds these are. Both its ID and its tags are matched against the target's resistance and immunity entries.

`public StableId TargetId`

:   The combatant the odds were resolved for. Its combatant definition supplied the resistances and immunities applied here, so the same status previews differently against different targets.

---

## TargetValidationContext

```csharp
public sealed class TargetValidationContext
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/MechanicsContracts.cs</small>

Read-only catalog passed to ITargetResolver.Validate while compiled
content is being built. A resolver checks its authored PropertySet
against this catalog; any error in the returned report aborts
compilation.

**Constructors**

`public TargetValidationContext(CompiledBattleContent content)`

:   Binds the context to the catalog being compiled.
    - `content` &mdash; Non-null compiled catalog available for validating authored target-resolver configuration.

**Properties**

`public CompiledBattleContent Content`

:   The catalog an authored property value must resolve against. It describes content only: combatants and teams exist just once a battle starts, so anything about who is actually on the field is decided in `ITargetResolver.GetCandidates`.

---

## ValidationReport

```csharp
public sealed class ValidationReport
```

`TurnGauge.Simulation` &middot; <small>TurnGauge/Runtime/Simulation/Mechanics/ValidationReport.cs</small>

What a validator found: the diagnostics that make the thing unusable, and
the ones that are merely worth saying.

The two lists are kept apart so a caller can refuse to run on errors while
still surfacing every warning it collected. Only `Errors`
decides `IsValid`, so a report can be valid and still carry
diagnostics worth showing the author.

**Constructors**

`public ValidationReport()`

:   Collects errors and warnings into one immutable report.
    - `errors` &mdash; Diagnostics that make the validated thing unusable. Copied on the way in, so the caller may keep reusing its own collection afterwards.
    - `warnings` &mdash; Diagnostics worth reporting that still leave the thing usable.

**Properties**

`public FrozenList<Diagnostic> Errors`

:   Everything that makes the validated thing unusable. A non-empty list is exactly what makes `IsValid` false.

`public bool IsValid`

:   Whether there are no errors. Warnings are deliberately ignored here.

`public static ValidationReport Valid`

:   The clean report, with nothing to say at all. It is one shared instance rather than a fresh object, which is why a validator that finds nothing costs no allocation.

`public FrozenList<Diagnostic> Warnings`

:   Everything worth telling the author about that still leaves the thing usable. These never affect `IsValid`, so a caller that only checks validity will drop them silently.

**Methods**

`public static ValidationReport Error(StableId id, string detail = null)`

:   Appends a error diagnostic with a stable ID and human detail. Callers branch on the ID/severity, not the text.
    - `id` &mdash; The identity of the failure, which is what callers branch on.
    - `detail` &mdash; Context for a human reader, such as the offending id; null becomes empty.
    - **Returns** &mdash; An invalid report containing exactly one error diagnostic and no warnings.

`public static ValidationReport Warning(StableId id, string detail = null)`

:   Appends a warning diagnostic with a stable ID and human detail. Callers branch on the ID/severity, not the text.
    - `id` &mdash; The identity of the concern being raised.
    - `detail` &mdash; Context for a human reader; null becomes empty.
    - **Returns** &mdash; A report whose `IsValid` is still true, because warnings do not fail validation.

---

