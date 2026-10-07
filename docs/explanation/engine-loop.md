# The engine loop

After this page you can read a single `AdvanceTicks` call: what it consumed, what each
returned outcome obliges you to do next, and which questions the returned snapshot is the
authority on.

---

## Ticks are the unit of time

A tick is an integer. `AdvanceTicks(int count)` asks the engine to reach
`current tick + count`, and `AdvanceTicksResult.TargetTick` reports that target back.

Your driver owns the conversion from frame time to ticks:

```csharp
accumulator += Time.deltaTime * TicksPerSecond;
var ticks = (int)accumulator;
if (ticks <= 0) return;
accumulator -= ticks;

var step = engine.AdvanceTicks(ticks);
```

The fractional accumulator is yours alone. Only the integer count crosses into the engine,
which is why a battle at 4x speed, a battle at 15 fps, and a battle stepped by hand in the
Workbench all produce the same result. `ContractVersions.TicksPerSecond` is `30`, the rate
the shipped demo and the quick-start driver convert at; nothing in the simulation reads
seconds, so you may pick another rate.

`AdvanceTicks(0)` returns `ReachedTarget` with no events and an unchanged snapshot. A
negative count throws `ArgumentOutOfRangeException`; it is a programming error, not an
outcome.

!!! note
    `TargetTick` is what you asked for. `Snapshot.Tick` is where the battle actually got
    to, and the two differ whenever the call stopped early. Read `Snapshot.Tick` for
    anything you display.

## The five advance outcomes

`AdvanceTicksOutcome` has five members, all of them ordinary data rather than exceptions.

| Outcome | Meaning | What you do next |
| --- | --- | --- |
| `ReachedTarget` | The requested ticks were consumed; the battle continues | Keep pumping |
| `AwaitingCommand` | A player-controlled decision is waiting | `Submit` a command, then pump again |
| `Terminal` | A result was reached | Read `Snapshot.Result`; stop pumping |
| `NoScheduledWork` | Nothing left to schedule, and no result | Stop pumping; treat as a content fault |
| `FatalInvariant` | An invariant broke | Read `Diagnostic`; stop pumping |

`AwaitingCommand` only ever concerns a combatant the encounter marks as player-controlled.
An AI-controlled combatant's decision is resolved inside the engine from its AI policy, so
it never surfaces as a stop.

A terminal `Snapshot.Result.ResultId` is one of `battle.victory`, `battle.defeat`,
`battle.draw`, `battle.concession` or `battle.stalled`. `battle.stalled` is a result, not a
crash: when a battle passes the maximum root actions or maximum battle ticks its authored
battle rules allow, it ends cleanly instead of running forever. Once a battle is terminal
the tick stops moving and every further `AdvanceTicks` call returns `Terminal` again.

!!! warning
    On `FatalInvariant` the engine rolls its state back to the last event boundary and
    fills in `Diagnostic` instead of throwing. Stop the loop and report it. Pumping again
    will keep failing, because nothing about the state has changed.

## Commands in, events out

### Commands

A `BattleCommand` is intent going in. It carries a `CommandSequence`, the `RequestedTick`
it was decided at, a command type, the acting combatant, an optional skill, requested
targets and properties. Sequence and tick are explicit so that ordering never depends on
when a click arrived.

Build every command from the snapshot you were last handed:

```csharp
var snapshot = engine.GetSnapshot();
var command = new BattleCommand(
    snapshot.NextCommandSequence, snapshot.Tick, BattleIds.UseSkillCommand,
    choice.ActorId, choice.SkillId, choice.Targets, PropertySet.Empty);

var result = engine.Submit(command);
```

`CommandResult.Disposition` separates two very different failures:

| Disposition | Meaning |
| --- | --- |
| `TransportRejected` | The command never reached the rules: wrong sequence, or not at a submission boundary. Nothing changed |
| `Accepted` | A `command.accepted` event was emitted and the command was recorded |
| `Rejected` | The rules refused it. `ReasonId` says why, and the refusal is recorded too |
| `FatalInvariant` | An invariant broke during validation; the pre-submission state is restored |

Accepted and rejected commands both land in `Snapshot.RecordedCommands`, so a replay
reproduces a battle including the moves a player was not allowed.

### Events

A `BattleEvent` is a fact coming out: the tick it happened at, an `EventSequence`, the root
action it belongs to, a stable event type such as `damage.resolved`, `status.applied`,
`cast.started` or `combatant.died`, and its properties. `AdvanceTicksResult.Events` holds
them in order.

The driver hands both halves of a step to presentation and nothing else:

```csharp
presenter.EnqueueEvents(step.Events);
presenter.AdoptSnapshot(step.Snapshot);
```

## Snapshots

`AdvanceTicksResult.Snapshot` and `engine.GetSnapshot()` return the same immutable
`BattleSnapshot`. Every property is get-only and every collection is a frozen list, so
holding one from an earlier tick to diff against a later one is safe and cheap.

The snapshot is the authority on the battle's state, and only that:

- **Combat state** - teams, combatants, stats, statuses, shields, resources, cooldowns and
  actions in flight.
- **Timing state** - the tick, the scheduler's state, and the decision queue head-first.
- **Outcome** - `Result`, including which team won and why.
- **Identity** - the RNG position, the content manifest hash, the event chain hash and
  `StateHash`.

It holds nothing about presentation: no skin, no animation, no camera. That is why
restyling a battle cannot change its outcome.

Two hashes carry the weight. Compare `StateHash` between two runs to prove they agree.
`ContentManifestHash` records the compiled content a snapshot came from, and
`BattleEngine.Restore` refuses a snapshot whose hash does not match the content you hand it,
so a mismatched replay fails loudly rather than playing back wrongly.

## Next

- **[Schedulers and tempo](schedulers.md)** - what decides who is at the head of that
  decision queue.
- **[Determinism](determinism.md)** - the properties the loop above is protecting.
- **[Running a battle](../reference/running-a-battle.md)** - the full API surface for every
  type named here.
