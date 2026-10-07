# Statuses, targeting and reactions

11 types in this area.

!!! abstract "On this page"
    [CombatantStatState](#combatantstatstate) &middot; [ReactionContext](#reactioncontext) &middot; [ReactionEvaluation](#reactionevaluation) &middot; [ReactionSignature](#reactionsignature) &middot; [ShieldState](#shieldstate) &middot; [StatusInstanceState](#statusinstancestate) &middot; [TargetContext](#targetcontext) &middot; [TargetLifeState](#targetlifestate) &middot; [TargetRequestContract](#targetrequestcontract) &middot; [TargetRequestResult](#targetrequestresult) &middot; [TargetTeamRelation](#targetteamrelation)

## CombatantStatState

```csharp
public sealed class CombatantStatState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Statuses/MechanicsState.cs</small>

One combatant's base value for one stat, as carried by a snapshot. The engine seeds these from
the compiled combatant definition when the battle starts and does not rewrite them afterwards:
stats change in play through status modifiers, which are folded in when a formula reads the
stat. This is therefore the base value, not the effective one.

**Constructors**

`public CombatantStatState(StableId ownerId, StableId statId, Fixed64 value)`

:   Creates a stat entry. Throws when either ID is invalid; the value itself is not range-checked against the stat definition here.

    - `ownerId` &mdash; Valid combatant identifier that scopes the stat entry within the battle snapshot.
    - `statId` &mdash; Valid compiled stat identifier paired with `ownerId` for lookup.
    - `value` &mdash; Deterministic base amount before live status modifiers; definition-specific bounds are not checked here.

**Properties**

`public StableId OwnerId`

:   The combatant this value belongs to. Stats are held as one flat list for the whole battle, so an entry is found by owner and stat together rather than by position.

`public StableId StatId`

:   The stat definition this value is for. The battle rules name the stats formulas read - power, spirit, defence, critical chance - and those lookups match against this ID.

`public Fixed64 Value`

:   The base value, in deterministic fixed point, before any status modifier applies.

---

## ReactionContext

```csharp
public sealed class ReactionContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Reactions/ReactionContracts.cs</small>

Everything a reaction rule may look at while deciding one candidate: the triggering effect tag
and phase, the two combatants involved, the compiled catalog, and a read-only view of battle
state. It is an input, not a handle on the engine - nothing reachable from it can advance or
mutate the battle.

**Constructors**

`public ReactionContext(CompiledBattleContent content, BattleSnapshot snapshot, ulong rootActionSequence, int parentDepth, StableId sourceCombatantId, StableId targetCombatantId, StableId triggeringEffectTag, ReactionTriggerPhase phase)`

:   Creates a context. The snapshot is wrapped in a `BattleStateView`, so the authoritative snapshot is not reachable from the rule. Throws when content or snapshot is null, when `rootActionSequence` is zero, when `parentDepth` is negative or above `SimulationLimits.ReactionMaximumDepth`, or when any of the three IDs is invalid.

    - `rootActionSequence` &mdash; The root action whose resolution triggered this candidate. Reaction depth, count, and once-per-root budgets are all tracked per root action.
    - `parentDepth` &mdash; Reaction nesting depth of the execution that triggered this candidate; the reaction runs one level deeper if it fires.
    - `sourceCombatantId` &mdash; The combatant that owns the reaction being offered.
    - `targetCombatantId` &mdash; The other combatant of the triggering primitive.
    - `triggeringEffectTag` &mdash; The tag that matched; always one of the rule's declared trigger tags.
    - `content` &mdash; Non-null compiled catalog used for deterministic definition lookups while the candidate is evaluated.
    - `phase` &mdash; Before- or after-effect pass in which the triggering primitive offered this reaction.
    - `snapshot` &mdash; Non-null immutable battle state projected into a read-only `BattleStateView` for the rule.

**Properties**

`public CompiledBattleContent Content`

:   The compiled catalog the rule may read while judging this candidate, and the same instance the battle is running, so a definition looked up here is the one that will resolve if the reaction fires.

`public int ParentDepth`

:   Reaction nesting depth of the execution that triggered this candidate, counted from zero for a directly played action. The reaction runs at this depth plus one.

`public ReactionTriggerPhase Phase`

:   Whether this offer is the before-effect or after-effect pass around the triggering primitive. A candidate is only ever offered in the phase its reaction definition declares, so a rule that serves one definition always sees the same value here.

`public ulong RootActionSequence`

:   The root action whose resolution triggered this candidate. Every reaction budget is scoped to it, so two reactions of the same root share depth and count allowances.

`public BattleStateView Snapshot`

:   Read-only projection of battle state as of this evaluation. The authoritative snapshot is deliberately not reachable through it.

`public StableId SourceCombatantId`

:   The combatant that owns the reaction being offered. Reactions are offered to both sides of the triggering primitive, so this is not necessarily the actor that played the action.

`public StableId TargetCombatantId`

:   The other combatant of the triggering primitive, opposite `SourceCombatantId`.

`public StableId TriggeringEffectTag`

:   The effect tag that matched; always one of the rule's declared trigger tags.

---

## ReactionEvaluation

```csharp
public sealed class ReactionEvaluation
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Reactions/ReactionContracts.cs</small>

A reaction rule's verdict on one candidate: whether it fires, and the source and target it will
use if it does. Declining is a normal outcome, but an ineligible evaluation must name its reason
with a diagnostic.

**Constructors**

`public ReactionEvaluation(bool eligible, StableId sourceCombatantId, StableId targetCombatantId, Diagnostic diagnostic)`

:   Creates an evaluation. Throws when either ID is invalid, when an eligible evaluation carries a diagnostic, or when an ineligible one carries none.

    - `eligible` &mdash; Whether the reaction fires.
    - `sourceCombatantId` &mdash; The combatant the reaction acts as; it need not be the one the context offered.
    - `targetCombatantId` &mdash; The combatant the reaction acts on; it need not be the one the context offered.
    - `diagnostic` &mdash; Why the reaction declined. Pass `default` when `eligible` is true.

**Properties**

`public Diagnostic Diagnostic`

:   Why the reaction declined. Default, with an invalid ID, on an eligible evaluation.

`public bool Eligible`

:   Whether the reaction fires. Declining is a normal verdict rather than a failure, but an ineligible evaluation must say why through `Diagnostic`, so a reaction can never be silently dropped.

`public StableId SourceCombatantId`

:   The combatant the reaction will act as, which the rule may redirect away from the pair the context offered.

`public StableId TargetCombatantId`

:   The combatant the reaction will act on, which the rule may likewise redirect.

---

## ReactionSignature

```csharp
public sealed class ReactionSignature
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Reactions/ReactionContracts.cs</small>

The static contract an `IReactionRule` publishes: which effect tags may trigger it
and which effect tags it can go on to emit. Content compilation builds a graph from these
declarations and refuses content whose reaction cycles it cannot prove terminate, so the
signature is what buys bounded reaction chains before a battle ever runs.

**Constructors**

`public ReactionSignature(IEnumerable<StableId> triggerEffectTags, IEnumerable<StableId> emittedEffectTags, bool finiteByConstruction)`

:   Creates a signature. Both tag lists are sorted into canonical order; an invalid or repeated tag is rejected rather than collapsed, as is a list longer than `SimulationLimits.TagsPerCombatantDefinition`. Throws when `triggerEffectTags` yields no tags at all.

    - `triggerEffectTags` &mdash; Effect tags whose resolution may offer this rule. At least one is required.
    - `emittedEffectTags` &mdash; Every effect tag the rule can cause to resolve. Declaring extra tags is merely conservative; declaring too few defeats the cycle analysis.
    - `finiteByConstruction` &mdash; Declares that the rule cannot fire without bound on its own. See `FiniteByConstruction` for what compilation does with it.

**Properties**

`public FrozenList<StableId> EmittedEffectTags`

:   The effect tags the rule declares it can emit, sorted and unique. Compilation also folds in the tags of the effects each reaction definition actually authors, so this list only has to cover what the rule causes beyond those.

`public bool FiniteByConstruction`

:   Whether the rule guarantees it terminates by itself. A reaction cycle compiles only when every rule in it is once-per-root, consumes its required status on enqueue, or claims this.

`public FrozenList<StableId> TriggerEffectTags`

:   The effect tags that may offer this rule, sorted and unique. Never empty.

---

## ShieldState

```csharp
public sealed class ShieldState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Statuses/MechanicsState.cs</small>

One shield absorbing damage for a combatant. A combatant's shields are held in ascending
`Priority` order and damage is absorbed from the front of that order, so the lowest
priority value is spent first. A shield that reaches zero is removed rather than kept at zero,
which is why `RemainingAmount` is always positive.

**Constructors**

`public ShieldState(StableId shieldId, StableId ownerId, StableId sourceId, int priority, ulong applicationSequence, int remainingAmount, int maximumAuthoredAmount, ulong? linkedStatusApplicationSequence, ulong sourceRootActionSequence)`

:   Creates a shield. Throws when any of the three IDs is invalid, when either sequence is zero, when the remaining or maximum amount is not positive, when the remaining amount exceeds the maximum, or when a linked status sequence is supplied as zero.

    - `shieldId` &mdash; The authored shield identity from the effect that created it, which several applications may share; `applicationSequence` is what identifies this one.
    - `sourceId` &mdash; The combatant that applied the shield.
    - `priority` &mdash; Absorption order among the owner's shields; lower is spent first.
    - `applicationSequence` &mdash; Identity of this application, taken from the same snapshot counter as status applications.
    - `remainingAmount` &mdash; Absorption left. Must be positive and no greater than the maximum.
    - `maximumAuthoredAmount` &mdash; The granted size this shield is measured against. See `MaximumAuthoredAmount`.
    - `linkedStatusApplicationSequence` &mdash; The status application that owns this shield, or `null` when it stands alone.
    - `sourceRootActionSequence` &mdash; The root action that created this application.
    - `ownerId` &mdash; Valid combatant identifier whose incoming damage this shield absorbs.

**Properties**

`public ulong ApplicationSequence`

:   Identity of this application, drawn from the same snapshot counter as status applications, so shield and status sequences never collide.

`public ulong? LinkedStatusApplicationSequence`

:   The status application that owns this shield, or `null` when it stands alone. The link is reciprocal, and the shield is removed when that status is.

`public int MaximumAuthoredAmount`

:   The granted size this shield is measured against, never below `RemainingAmount` - use it as the denominator when drawing a shield bar. A reapplication resets it to the newly granted amount, except under a keep-higher linked status, where the larger of the two is kept.

`public StableId OwnerId`

:   The combatant the shield protects. Damage aimed at this combatant is absorbed here, in `Priority` order, before it reaches health.

`public int Priority`

:   Absorption order among the owner's shields: the lowest value absorbs damage first, ties broken by application sequence and then shield ID.

`public int RemainingAmount`

:   Absorption left, always positive: a spent shield is removed instead of being held at zero.

`public StableId ShieldId`

:   The authored shield identity from the effect that created it. It is not unique per instance; `ApplicationSequence` is.

`public StableId SourceId`

:   The combatant that applied the shield.

`public ulong SourceRootActionSequence`

:   The root action that created this application.

---

## StatusInstanceState

```csharp
public sealed class StatusInstanceState
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Statuses/MechanicsState.cs</small>

One live status application on one combatant: where it came from, how many stacks it carries, how
much duration is left, and when it next ticks. Instances are immutable, so the engine replaces
the entry whenever a status is refreshed, stacked, or ticked, and it is
`ApplicationSequence` - not the definition ID - that identifies one application.

**Constructors**

`public StatusInstanceState(StableId ownerId, StableId sourceId, StableId statusDefinitionId, ulong applicationSequence, ulong sourceRootActionSequence, int stackCount, StatusDurationClock durationClock, int remainingDuration, long nextPeriodicTick, ulong excludedOriginatingRootActionSequence, ulong? linkedShieldApplicationSequence, PropertySet instanceConfiguration)`

:   Creates a status instance. Throws when any of the three IDs is invalid, when either sequence is zero, when the stack count is outside 1..`SimulationLimits.IndependentStatusStacks`, when the duration clock is not a defined value, when the remaining duration is negative, above `SimulationLimits.TimingTicks`, or zero under any clock other than `StatusDurationClock.ElapsedTicks`, when the next periodic tick is negative, or when a linked shield sequence is supplied as zero.

    - `sourceId` &mdash; The combatant that applied the status.
    - `applicationSequence` &mdash; Identity of this application, taken from the snapshot's application counter and never reused.
    - `sourceRootActionSequence` &mdash; The root action that created this application.
    - `stackCount` &mdash; Stacks held by this one instance; see `StackCount` for how stacking policy affects it.
    - `remainingDuration` &mdash; Duration left, not duration elapsed. See `RemainingDuration`.
    - `nextPeriodicTick` &mdash; Absolute tick of the next periodic trigger, or 0 when the status has no elapsed-boundary periodic effect.
    - `excludedOriginatingRootActionSequence` &mdash; The root action that must not tick this status down. See `ExcludedOriginatingRootActionSequence`.
    - `linkedShieldApplicationSequence` &mdash; The shield application this status owns, or `null` when it owns none.
    - `instanceConfiguration` &mdash; Per-application properties. Must not be null; pass `PropertySet.Empty` for none.
    - `durationClock` &mdash; Boundary type that decrements `remainingDuration`: elapsed ticks, owner actions, or owner opportunities.
    - `ownerId` &mdash; Valid combatant identifier receiving modifiers and periodic effects from this application.
    - `statusDefinitionId` &mdash; Valid compiled definition identifier supplying stacking, duration, modifier, and periodic-effect rules.

**Properties**

`public ulong ApplicationSequence`

:   Identity of this application. Statuses and shields draw from the same snapshot counter, so the value is unique across both and is what a linked pair, a removal, or an event refers to.

`public StatusDurationClock DurationClock`

:   What `RemainingDuration` is counted in: elapsed ticks, or boundaries of the owner's own actions and opportunities. It therefore decides which event spends the status down, and under every clock except `StatusDurationClock.ElapsedTicks` the remaining duration must be at least one.

`public ulong ExcludedOriginatingRootActionSequence`

:   The root action that most recently applied or refreshed this status. Its duration does not decrement while that root action is still resolving, so a status cannot lose duration to the very action that granted it.

`public PropertySet InstanceConfiguration`

:   Per-application properties, carried unchanged through refreshes and shield relinking. Statuses the engine applies itself carry an empty set.

`public ulong? LinkedShieldApplicationSequence`

:   The application sequence of the shield this status owns, or `null`. The link is reciprocal: removing the status removes that shield too.

`public long NextPeriodicTick`

:   Absolute tick at which the next periodic trigger is due, or 0 when the status has no elapsed-boundary periodic effect. It is a tick number, not a countdown.

`public StableId OwnerId`

:   The combatant carrying the status. Its periodic effects are aimed here and its stat modifiers apply to this combatant's stats, whoever `SourceId` happens to be.

`public int RemainingDuration`

:   Duration left, not duration elapsed. Under the elapsed-ticks clock it is the number of ticks still to run from the tick this instance was written; under the owner-action clocks it drops by one at each matching boundary and the status expires when it would reach zero. Zero is legal only under `StatusDurationClock.ElapsedTicks`.

`public StableId SourceId`

:   The combatant that applied the status. Its periodic effects resolve with this combatant as the acting source and `OwnerId` as the target; the status's stat modifiers, by contrast, key on the owner carrying it.

`public ulong SourceRootActionSequence`

:   The root action that created this application. It stays fixed when the status is later refreshed, unlike `ExcludedOriginatingRootActionSequence`.

`public int StackCount`

:   Stacks held by this instance, at least one. Periodic effects run once per stack. A status whose policy is independent stacking keeps one instance per stack instead, each with a count of one.

`public StableId StatusDefinitionId`

:   The compiled status definition this application came from, which supplies its modifiers, periodic effects, and tags. Several instances on one combatant can share it, so on its own it does not identify an application - `ApplicationSequence` does.

---

## TargetContext

```csharp
public sealed class TargetContext
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Targeting/TargetContracts.cs</small>

Everything a target resolver is given about the situation it is choosing
for: the compiled catalog, who is acting, which skill is being used, and a
read-only projection of battle state. The authoritative snapshot is not
reachable from here, so a resolver cannot alter the battle it inspects.

**Constructors**

`public TargetContext(CompiledBattleContent content, BattleSnapshot snapshot, StableId actorId, CompiledSkillDefinition skill)`

:   Wraps the inputs for one resolver call. The snapshot is projected into a `BattleStateView`, so the resolver never receives the live snapshot.

    - `content` &mdash; The compiled catalog the skill and its IDs come from.
    - `snapshot` &mdash; Battle state to project; it is read, never retained or mutated.
    - `actorId` &mdash; The combatant whose skill use is being targeted.
    - `skill` &mdash; The skill definition whose target resolver is being consulted.

**Properties**

`public StableId ActorId`

:   The combatant whose skill use is being targeted. Team relations in the request contract are all measured from this combatant.

`public CompiledBattleContent Content`

:   The compiled catalog every ID in this context belongs to. A resolver should look definitions up here rather than holding its own, so it keeps working when the buyer recompiles their content.

`public CompiledSkillDefinition Skill`

:   The skill being used. A resolver may be consulted for more than one skill, so read the shape from here rather than assuming the skill it was authored against.

`public BattleStateView Snapshot`

:   A read-only projection of the battle as it stands. It is the resolver's only view of live state, and it exposes no way to change anything, so choosing targets cannot alter the battle being chosen for.

---

## TargetLifeState

```csharp
public enum TargetLifeState : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Targeting/TargetContracts.cs</small>

Which life state a combatant must be in to be an eligible target. This is
declared eligibility rather than a filter the engine reapplies on every
path: a resolver's own candidate list is expected to honour it, and the
engine applies it when it has to re-pick a target whose lock went stale.

| Value | Meaning |
| --- | --- |
| `Living` | Only combatants that are still alive. |
| `Dead` | Only combatants that are no longer alive. |
| `Any` | Life state does not narrow the candidate set. |

---

## TargetRequestContract

```csharp
public sealed class TargetRequestContract
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Targeting/TargetContracts.cs</small>

The declared shape of one target resolver's requests: how many target IDs
a command may carry, whether an empty request means the resolver selects,
how many targets the engine draws at random, and which combatants are
eligible. The engine reads it during command preflight, before it asks the
resolver anything, so a resolver must report the same shape on every call.

**Constructors**

`public TargetRequestContract(int minimumRequestedIds, int maximumRequestedIds, bool zeroRequestedInvokesAutomaticSelection, int randomCount, TargetLifeState allowedLifeState, TargetTeamRelation teamRelation, bool actorMayAppear)`

:   Declares a contract whose `MaximumResolvedTargets` is inferred: the requested-ID maximum when there is one, otherwise the random count when there is one, otherwise 1 for a `TargetTeamRelation.Self` contract and `SimulationLimits.ResolvedTargetsPerOperation` for any wider relation.

    - `minimumRequestedIds` &mdash; Fewest target IDs a command may carry; zero for a resolver that selects on the caller's behalf.
    - `maximumRequestedIds` &mdash; Most target IDs a command may carry, capped by `SimulationLimits.RequestedTargetsPerCommand`. Zero forbids caller-supplied IDs outright.
    - `zeroRequestedInvokesAutomaticSelection` &mdash; Whether an empty request asks the resolver to choose. When false, a command that ends up locking nothing is rejected.
    - `randomCount` &mdash; How many targets the engine itself draws from the candidate set when the command requests none. Zero means the engine draws nothing.
    - `allowedLifeState` &mdash; Life state an eligible combatant must be in.
    - `teamRelation` &mdash; Relation an eligible combatant must have to the acting combatant's team.
    - `actorMayAppear` &mdash; Whether the acting combatant may be one of its own targets.

`public TargetRequestContract(int minimumRequestedIds, int maximumRequestedIds, bool zeroRequestedInvokesAutomaticSelection, int randomCount, TargetLifeState allowedLifeState, TargetTeamRelation teamRelation, bool actorMayAppear, int maximumResolvedTargets)`

:   Declares a contract with an explicit `MaximumResolvedTargets`, for a resolver whose locked-set size is not implied by its requested-ID or random counts.

    - `minimumRequestedIds` &mdash; Fewest target IDs a command may carry; zero for a resolver that selects on the caller's behalf.
    - `maximumRequestedIds` &mdash; Most target IDs a command may carry, capped by `SimulationLimits.RequestedTargetsPerCommand`. Zero forbids caller-supplied IDs outright.
    - `zeroRequestedInvokesAutomaticSelection` &mdash; Whether an empty request asks the resolver to choose. When false, a command that ends up locking nothing is rejected.
    - `randomCount` &mdash; How many targets the engine itself draws from the candidate set when the command requests none. Zero means the engine draws nothing.
    - `allowedLifeState` &mdash; Life state an eligible combatant must be in.
    - `teamRelation` &mdash; Relation an eligible combatant must have to the acting combatant's team.
    - `actorMayAppear` &mdash; Whether the acting combatant may be one of its own targets.
    - `maximumResolvedTargets` &mdash; Most targets this resolver can end up locking, capped by `SimulationLimits.ResolvedTargetsPerOperation`.

**Properties**

`public bool ActorMayAppear`

:   Whether the acting combatant may be one of its own targets. It is the difference between "one ally" and "one ally other than me".

`public TargetLifeState AllowedLifeState`

:   The life state an eligible combatant must be in. It is declared eligibility rather than a filter reapplied everywhere: a resolver is expected to honour it in its own candidate list, and the engine leans on it when a locked target has to be re-picked.

`public int MaximumRequestedIds`

:   Most target IDs a command may carry. Zero together with a zero minimum means the caller supplies no IDs at all and selection is left to the resolver or to the engine's random draw.

`public int MaximumResolvedTargets`

:   Most targets this resolver can end up locking, which is not the same as `MaximumRequestedIds`: an automatic or random resolver takes no requested IDs yet still resolves several. The engine uses it to recognise a single-target hostile request, which is the only kind taunt-style statuses redirect.

`public int MinimumRequestedIds`

:   Fewest target IDs a command may carry. The engine rejects a command below this count before the resolver sees it.

`public int RandomCount`

:   How many targets the engine draws itself, without replacement, over the sorted candidate set when the command requests none. The resolver declares the count and never draws, which keeps the draw inside the engine's deterministic RNG stream.

`public TargetTeamRelation TeamRelation`

:   The relation an eligible combatant must have to the acting combatant's team. `TargetTeamRelation.Ally` covers the actor's own team including the actor, which is what `ActorMayAppear` then narrows.

`public bool ZeroRequestedInvokesAutomaticSelection`

:   Whether an empty request means "choose for me". When false, a command whose resolution locks no targets is rejected rather than run against nothing.

---

## TargetRequestResult

```csharp
public sealed class TargetRequestResult
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Targeting/TargetContracts.cs</small>

A target resolver's verdict on one request: either the set of targets to
lock, or the diagnostic explaining the refusal. A rejection is an ordinary
command rejection reported back to the caller, not an engine error, and it
leaves the battle untouched.

**Constructors**

`public TargetRequestResult(bool accepted, IEnumerable<StableId> lockedTargets, Diagnostic diagnostic)`

:   Builds a verdict. Prefer `Accept` and `Reject`, which keep the accepted flag and the diagnostic consistent for you.

    - `accepted` &mdash; Whether the request is legal.
    - `lockedTargets` &mdash; Targets to lock. They are sorted and deduplicated on the way in, so the order supplied here cannot affect the battle.
    - `diagnostic` &mdash; The refusal reason. It must be default for an accepted verdict and must carry a valid ID for a rejected one.

**Properties**

`public bool Accepted`

:   Whether the request is legal. A false verdict rejects the command that prompted it, which is an ordinary answer to the caller rather than an engine error, and leaves the battle exactly as it was.

`public Diagnostic Diagnostic`

:   Why the request was refused. It is the default diagnostic, whose ID is invalid, whenever `Accepted` is true.

`public FrozenList<StableId> LockedTargets`

:   The targets to lock, ascending and without duplicates. It is empty on a rejection, and also empty on an accepted request whose contract declares a random count, because the engine owns those draws.

**Methods**

`public static TargetRequestResult Accept(IEnumerable<StableId> lockedTargets)`

:   Accepts a request and names the targets to lock.

    - `lockedTargets` &mdash; Targets to lock, in any order; they are sorted and deduplicated. Pass an empty set when the contract declares a random count and the engine should draw instead.
    - **Returns** &mdash; An accepted verdict carrying no diagnostic.

`public static TargetRequestResult Reject(StableId reasonId, string detail = null)`

:   Refuses a request. The command is rejected and the battle is left as it was.

    - `reasonId` &mdash; The diagnostic ID reported to the caller. It must be valid, so a rejection can always be explained.
    - `detail` &mdash; Optional extra context, such as the offending target ID. It is diagnostic text and is not meant for players.
    - **Returns** &mdash; A rejected verdict with no locked targets.

---

## TargetTeamRelation

```csharp
public enum TargetTeamRelation : byte
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Targeting/TargetContracts.cs</small>

Which combatants a target request may reach, relative to the acting
combatant's team. `TargetTeamRelation.Ally` is "same team as
the actor", so it includes the actor itself unless
`TargetRequestContract.ActorMayAppear` excludes it.

| Value | Meaning |
| --- | --- |
| `Self` | The acting combatant and no one else. |
| `Ally` | Any combatant on the actor's own team. |
| `Enemy` | Any combatant on a team other than the actor's. |
| `Any` | Team membership does not narrow the candidate set. |

---
