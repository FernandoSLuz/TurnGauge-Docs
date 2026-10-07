# Combatants, teams and encounters

This page takes you from a combatant asset to an encounter the engine can start: who fights, how it
decides, which side it is on, and what ends the fight. Stats, effects, statuses and skills come first.

## Combatants

**Assets > Create > TurnGauge > Combatant**. A combatant is a template, not a participant: teams
instantiate it, so one asset can appear on both sides of a battle.

| Field | What it does |
| --- | --- |
| `BaseStats` | Stat asset plus a raw value. Sets what the formulas read. |
| `ResourceDefaults` | Starting value for each spendable pool the combatant uses. |
| `Tags` | Free-form identifiers other content can match against. |
| `GrantedSkills` | The only skills this combatant may ever use. |
| `DefaultAiPolicy` | The policy used when a team member is Automatic and does not override it. |
| `Resistances` | A chance to refuse a status, matched by status asset or by status tag. |
| `ImmuneStatuses`, `ImmuneStatusTags` | Statuses that never apply at all. |
| `IntrinsicReactions` | Reactions the combatant always carries, without a status granting them. |

### Raw values and the two required stats

Stat values and resistance chances are scaled integers, shown unscaled in the inspector. Stats use a
scale of 10 000, so `ValueRaw: 1200000` is 120 health; resistance chances use 1 000 000; resource
values are plain integers. Compilation fails unless the combatant carries a positive value for the
two stats your Battle Rules asset names as `MaximumHealthStat` and `SpeedStat`, and maximum health
must be a whole number - a multiple of 10 000. Every other stat is optional and reads as zero.

## AI policies

**Assets > Create > TurnGauge > AI Policy**. A policy is an implementation reference, a property set
and an ordered list of rules. Each rule names one skill, a priority, a weight, its conditions and the
target IDs it requests.

| Implementation ID | How it picks |
| --- | --- |
| `ai.priority.v1` | The legal rule with the highest `Priority`. No random draw. |
| `ai.conditional.v1` | Selects the same way; the difference is that its rules carry conditions. |
| `ai.weighted.v1` | A weighted random draw over the legal rules. `Weight: 0` rules are dropped. |
| `ai.custom-example.v1` | A worked example of a registered policy, selecting by priority. |

Every built-in refuses properties: a non-empty `Properties` list on one of these is a compile error.
As with effects and targets, the policy asset offers those implementations as a dropdown and
creates the arguments the chosen one requires. Nothing here has to be typed from memory:

![The Inspector on an authoring asset, showing the implementation dropdown, the one-line summary of the chosen implementation, and an Arguments section whose keys were created by choosing it](../assets/images/editor-implementation-picker.png){ .shot }

Rules are the whole vocabulary. Four policy assets ship to copy - `ai.priority-brawler`,
`ai.conditional-healer`, `ai.weighted-caster` and `ai.weighted-random`.

### Rule conditions

A rule is legal only when every condition on it passes **and** the resulting command survives the
engine's own checks on cost, cooldown, restrictions and target availability. Seven condition kinds
ship: `ActorHealthAtMost`, `ActorResourceAtLeast`, `ActorHasStatus`, `AllyCountAtMost`,
`EnemyCountAtLeast`, `SkillReady` and `TargetAvailable`. Each carries a threshold and, where needed,
a resource, status or skill operand. Counts include only living combatants, the actor as its own ally.

!!! note "Only weighted policies consume randomness"
    Priority and conditional selection draw nothing from the battle RNG. A weighted policy takes one
    draw per decision, over the total weight of the legal rules - so switching a policy between
    weighted and priority changes every later number in a seeded battle.

## Reactions

**Assets > Create > TurnGauge > Reaction**. A reaction fires off another effect's tags rather than
off a skill, so it belongs to whichever combatant carries it. Beyond its resolver `Implementation`,
its `Effects` and a `Priority` that orders it against reactions on the same effect, four fields
decide when it fires.

| Field | What it does |
| --- | --- |
| `TriggerPhase` | `BeforeEffect` or `AfterEffect`. A guard shields before damage lands; thorns answer after. |
| `RequiredStatus` | The reaction fires only while the carrier holds this status. |
| `ConsumeRequiredStatusOnEnqueue` | Spends that status when the reaction is queued, so it fires once. |
| `OncePerRoot` | Defaults to on. Limits the reaction to one firing per root action. |

Reaction graphs are checked for cycles at compile time. A cycle fails the compile only when it is
unbounded - no member is `OncePerRoot`, none consumes a required status, and none is finite by its
resolver's construction. Leaving `OncePerRoot` on keeps a chain terminating.

## Teams

**Assets > Create > TurnGauge > Team**. A team is a list of members, and a member is one
participant in one battle.

| Field | What it does |
| --- | --- |
| `CombatantInstanceId` | The identity used all battle, in events and replays. Unique across *both* teams. |
| `Control` | `Human` or `Automatic`. |
| `AiPolicyOverride` | Replaces the combatant's default policy for this member only. |
| `StartingHealth` | `FullHealth`, or `ExplicitCurrentHealth` with a value you supply. |
| `Targetable` | Clear it to keep the member out of target resolution. |
| `ResourceOverrides` | Per-member starting values for named resources. |
| `InitialAtbGauge` | Head start on the ATB gauge. |
| `InitialStatuses` | Statuses applied before the first tick, with a stack count and optional source member. |

An `Automatic` member must resolve to a policy - its override, or the combatant's `DefaultAiPolicy`.
If neither exists the compile fails rather than the battle stalling. A `Human` member makes
`AdvanceTicks` return `AwaitingCommand` when its turn arrives, and the engine waits until your driver
submits. Every shipped sample team is fully `Automatic`, which is why the demo runs unattended.

!!! warning "Gauge and scheduler must agree"
    `InitialAtbGauge` must be zero under the action-order scheduler, and strictly below the ATB
    scheduler's `GaugeThresholdUnits` under ATB. Anything else is a compile error. See
    [Schedulers and tempo](../explanation/schedulers.md).

## Battle rules

**Assets > Create > TurnGauge > Battle Rules**. One rules asset serves a whole catalog: it hangs
off the catalog's `Rules` field, not off an encounter, so every encounter in that catalog shares it.

It names which of your Stat assets fill the seven semantic roles - maximum health, power, magic,
spirit, defense, speed, critical chance - and the five formula implementations for damage, healing,
defense, criticals and status chance. `CriticalMultiplierRaw`, the two variance bounds and the two
formula bounds are all scaled by 10 000. The shipped `rules.starter` uses a critical multiplier of
`15000` (x1.5) and equal variance bounds of `10000` (x1.0), removing damage variance entirely.

`MaximumReactionDepth` and `MaximumReactionCount` cap a reaction chain; `MaximumRootActions` and
`MaximumBattleTicks` cap the battle. `ResultPolicy` has one legal value, `LastLivingTeam`: no
living, unconceded team is a draw; exactly one is a victory if it is the encounter's
`PerspectiveTeam` and a defeat if it is not; two sides still standing when either limit is reached
is stalled.

## One runnable encounter

**Assets > Create > TurnGauge > Encounter**. An encounter has a scheduler, exactly two teams, and a
perspective team. Each team entry pairs one Team asset with one Formation Preset and the slot
assignments that place its members.

1. Author or pick two Team assets whose combined `CombatantInstanceId` values are all distinct.
2. Set `Scheduler` to an action-order or ATB Scheduler asset.
3. Fill both `Teams` entries. Give each a Formation Preset and one assignment per member; a member
   with no slot is a compile error. Lay the slots out in
   [the Formation Editor](place-formations.md).
4. Set `PerspectiveTeam` to one of those two teams. It is required, and it decides whether the
   surviving side reads as victory or defeat.
5. Add every new asset to your catalog, then run **Tools > TurnGauge > Content Validator**.

`encounter.tutorial-duel` in `Assets/TurnGauge/Samples/StarterContent/` is the smallest working
example: one member per side, both on `formation.duel`, action-order scheduling. After a successful
compile an encounter becomes a `CompiledEncounterSnapshot` carrying the `StartRequest` the engine
consumes and the `FormationLayout` the presenter draws.

## Next

- **[Place combatants with the Formation Editor](place-formations.md)** - the slots your assignments point at.
- **[Run a battle from your own code](../tutorials/run-a-battle-from-code.md)** - the compiled encounter as a live engine.
- **[Author content in the right order](author-content.md)** - the layers below this one, and the diagnostics that name the asset at fault.
