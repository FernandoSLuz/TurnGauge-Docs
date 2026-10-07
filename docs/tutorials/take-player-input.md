# 6. Take a decision from the player

A click in the skill tray becomes a command the battle accepts, a hover fills the tooltip with
previewed numbers, and every id on screen reads as a name.

---

## 1. Watch the tray fill itself

You have already seen this step work. When the engine reaches a decision that belongs to a
**human** actor, the interface compiles that actor's legal choices and draws one button each.

![The battle paused at a decision: the turn strip reads NOW Ember Vanguard and the tray offers Concede, Power Blow captioned one enemy, Rally captioned one ally, and Strike captioned auto enemy](../assets/images/04-runtime-human-decision.png){ .shot }

A skill reaches that tray only when:

- The first decision entry is a **human** control kind and its actor is living. Otherwise the
  result is `DecisionOptions.None` and the tray hides entirely.
- The actor has no cooldown entry for that skill.
- Every cost in the skill's timing is payable from the actor's current resources.
- No status on the actor restricts one of the skill's tags.
- The skill's target resolver resolves in the mechanics registry.

Offered skills are sorted by skill id, so button order is stable between frames and between runs.
The concede button appears only when the compiled content registers the concede command, and the
tray draws at most twelve buttons.

`DecisionOptions` is a display projection: compiling it reads a snapshot and a compiled catalog
and calls no engine mutator, so rebuilding it can never change a battle.

### The caption under each button

Each [`SkillCommandShape`](../reference/interface-and-widgets.md#skillcommandshape) carries a
[`TargetShape`](../reference/interface-and-widgets.md#targetshape) from the compiled target
contract. It is what the player may aim at, not the engine's resolution, and it is what the
caption under the button says.

| Field | What it tells the player |
| --- | --- |
| `Relation` | `Self`, `Ally`, `Enemy` or `Any`. The caption says "one enemy", "3 ally", "auto self". |
| `LifeState` | Whether living, dead, or any combatants may be picked. |
| `MinimumTargets` / `MaximumTargets` | How many ids the command may carry. |
| `MaximumResolvedTargets` | How many combatants the effect can end up hitting. |
| `ActorMayAppear` | Whether the actor can be among its own targets. |
| `AutomaticSelection` | Sending no ids lets the resolver choose. The caption reads "auto". |

## 2. Let the controller submit the click

With a `BattleRuntimeController` in the scene there is nothing to write. It subscribes to the
interface, and every click arrives at the battle through one supported path:

1. The player clicks a skill, and picks a target when that skill needs one. Step 4 below covers
   the picker.
2. `BattleUiRoot` raises `CommandChosen` with a
   [`BattleUiCommandChoice`](../reference/interface-and-widgets.md#battleuicommandchoice): the
   pending actor, whether the player conceded, the chosen skill, and any targets picked.
3. The controller checks that the actor is still the pending human actor and that the skill is
   in the compiled legal shapes.
4. `BattleUiCommandTranslator` turns the choice into the exact command the engine expects.
5. The engine validates and applies it, or rejects it and leaves the battle exactly as it was.

![One turn later: a status pip over the hero token, the roster row reading 1 status, the log ending in Status Applied and Action Completed, and the tray waiting on the next decision](../assets/images/05-runtime-events-and-next-decision.png){ .shot }

The interface never touches the engine. That separation is what makes it incapable of
desynchronising a simulation, and it is why a rejected click costs you nothing.

## 3. Submit a choice from your own code

Anything that is not a click in the shipped tray goes through the same door: build a
`BattleUiCommandChoice` and hand it to `Submit`. A hotkey, your own buttons, a tutorial script
that plays the first legal skill, an AI you wrote for the player's side.

```csharp
using TurnGauge.Presentation;
using TurnGauge.Runtime;
using UnityEngine;

public sealed class MyBattleInput : MonoBehaviour
{
    [SerializeField] private BattleRuntimeController battle;

    public void ChooseFirstLegalSkill()
    {
        var options = battle.CurrentDecisionOptions;
        if (!options.HasActor || options.Skills.Count == 0) return;

        var result = battle.Submit(new BattleUiCommandChoice(
            options.ActorId,
            false,                      // true concedes, and carries no skill
            options.Skills[0].SkillId,
            null));                     // null means "resolve the targets for me"

        if (!result.Succeeded) Debug.LogWarning(result.Message);
    }
}
```

`CurrentDecisionOptions` is `DecisionOptions.None` unless the battle is waiting on a human, and
reading it has no side effect, so it is safe to poll.

Every operation returns a `BattleRuntimeOperationResult` rather than throwing:

| `Failure` | What happened |
| --- | --- |
| `BattleNotRunning` | There is no battle to submit to. |
| `CommandTranslationFailed` | The actor is stale, the skill is not currently offered, or the target contract could not be satisfied. |
| `CommandRejected` | The engine refused the command. The battle is untouched. |

`Message` is written to be shown to a developer, not swallowed. Leave the controller's
**Log Failures** on while you build.

## 4. Let the player pick the target

Clicking a skill does not always send it. What happens next is decided by that skill's target
contract, and the interface already handles both cases:

- **The caption starts with "auto".** The resolver selects for itself, so the choice is raised
  immediately with no targets.
- **Anything else.** The skill tray hides and the target picker takes its place, offering one
  button per combatant that skill may legally hit, with a health readout under each name. A
  single-target skill commits on the pick itself. A multi-target skill collects picks until
  **Confirm**, and clicking a picked candidate again unpicks it. **Back** returns to the tray
  with nothing submitted.

The candidate list is not guesswork. `BattlePresenter` asks each offered skill's own registered
resolver who is eligible and hands the answer to the interface before the decision is shown, so a
resolver you wrote governs the picker exactly as it governs the engine. If the picker cannot open
at all -- a skin that hides the picker region, or fewer eligible candidates than the skill's
minimum -- the choice is raised with an empty list and
[`BattleUiCommandTranslator`](../reference/other.md#battleuicommandtranslator) fills it
deterministically with the lowest eligible stable ids. A battle is never stranded on a pick the
player cannot make.

Explicit ids are preserved verbatim, checked against the same resolver, and still validated by
the engine.

### Driving the picker yourself

Every step of that flow is a public call, so your own interface can replace any part of it:

```csharp
ui.BeginTargeting(skillId);         // false when there is nothing to pick
ui.PickTarget(combatantId);         // safe to wire to a click on a stage token
ui.ConfirmTargets();                // commits, and raises CommandChosen
ui.CancelTargeting();               // back to the tray
ui.ChooseSkill(skillId, pickedIds); // skip the picker entirely with ids of your own
```

`PickedTargets` and `OfferedTargets` report what is picked and what is on offer, and
`SkillTrayView.SetSelected` and `ClearSelection` highlight the pending button.

!!! tip
    Number keys 1-9 pick a candidate, Enter confirms, and Escape backs out, but only when the
    legacy Input Manager is enabled (**Project Settings > Player > Active Input Handling**).
    Pointer input always works, and `BattleUiRoot.LegacyInputAvailable` reports which case you
    are in.

## 5. Fill a tooltip with a forecast

The tooltip panel renders a [`TooltipData`](../reference/interface-and-widgets.md#tooltipdata)
value verbatim and calls no preview API of its own. Compute one per offered skill and store it
with `SetTooltip`; a hover shows the stored value, and a skill with none stored shows nothing.
Nothing fills these for you: the runtime demo's driver does it, and that is why the demo has
tooltips and a freshly created scene does not.

![A battle with a tooltip open beside the tray, reading Power Blow, a damage range of 34-41, Hit 92%, Crit 15%, a cost of 12 energy, cast 8t recover 12t, and the target line one enemy](../assets/images/hero-battle.png){ .shot }

```csharp
var options = DecisionShapeCompiler.Compile(snapshot, compiled);

foreach (var shape in options.Skills)
{
    // Text-only is enough to ship: cost, timing, target shape.
    ui.SetTooltip(TooltipData.TextOnly(
        shape.SkillId, "12 stamina", "Cast 6t, recover 4t", "one enemy"));
}
```

Recompute only when the pending actor or tick changes, not every frame.

### Where the numbers come from

Plan the skill's effect through `MechanicsRegistry.ResolveEffect(...).Plan(...)`, then price one
planned primitive with [`BattleFormulaService`](../reference/effects-and-mechanics.md#battleformulaservice).
`Preview` returns `Minimum`, `Maximum`, `HitChance` and `CriticalChance` for a damage or healing
primitive; `PreviewStatusApplication` returns the `FinalChance` of a status landing after
resistance. Pass those into the full `TooltipData` constructor. The panel formats the range and
hides the crit and status rows when those chances are impossible.
`TurnGaugeDemoBootstrap.BuildTooltip` in the runtime demo is the worked example.

To answer "what happens if I do nothing", run
[`BattleForecast`](../reference/scheduling-and-tempo.md#battleforecast) with a
[`ForecastRequest`](../reference/other.md#forecastrequest) of tick, action and event budgets. It
runs a copy of the battle, so the live engine is untouched, and reports why it stopped:
`HorizonReached`, `Terminal`, `NoScheduledWork`, `ActionLimit`, `EventLimit`, or
`UnknownHumanDecision`.

!!! warning
    A forecast is not a promise. It stops at the first human decision because it cannot know what
    the player will choose, and a request outside the structural budgets returns `FatalInvariant`
    with a diagnostic instead of a partial answer.

## 6. Format numbers and names players read

`Fixed64` and `Chance64` hold raw scaled integers, so `ToString()` gives `50000`, not `5`. Their
string form feeds canonical encoding and must never drift, so format anything a player reads with
[`BattleNumberFormat`](../reference/interface-and-widgets.md#battlenumberformat):

```csharp
BattleNumberFormat.Amount(value);           // "5.25"
BattleNumberFormat.WholeAmount(value);      // "5"
BattleNumberFormat.AmountRange(min, max);   // "10-14", or "12" when both ends match
BattleNumberFormat.Percent(chance);         // "87.5%"
BattleNumberFormat.Ticks(12);               // "12t"
```

Names work the same way. Compiled snapshots carry no labels, so a
[`DisplayStringTable`](../reference/interface-and-widgets.md#displaystringtable) maps stable ids
to display text for the roster, timeline, tray, feedback log and result banner. Assign the table
asset in the controller's **Display Strings** field, or hand one to the presenter binding in a
direct integration. An unmapped id falls back to its raw id text rather than to an empty label.
The table never enters a hash and never affects an outcome, which is why it can be swapped per
language.

## Advanced: submit an exact command

A driver that owns the engine itself, without the controller, builds the
[`BattleCommand`](../reference/commands-events-and-snapshots.md#battlecommand) and submits it:

```csharp
var translated = BattleUiCommandTranslator.Translate(choice, engine.GetSnapshot(), compiled);
if (translated.Succeeded)
{
    var result = engine.Submit(translated.Command);
    if (result.CommandEvent != null) presenter.EnqueueEvents(new[] { result.CommandEvent });
    presenter.AdoptSnapshot(engine.GetSnapshot());
}
```

The returned [`CommandResult`](../reference/running-a-battle.md#commandresult) reports `Accepted`,
`Rejected`, `TransportRejected` or `FatalInvariant`, with `ReasonId` naming a rejection. Check the
snapshot's `PendingDecisionActorId` against the choice's actor before translating, so a click that
arrived after the pending actor changed is dropped rather than applied to the wrong combatant.
`BattleRuntimeController.Submit(BattleCommand)` takes a command you built this way when you want
the controller for everything else.

## Next

- **[7. Restyle the interface](skinning-your-battle.md)** -- make the tray and tooltip look like your game.
- **[What each interface region draws](../how-to/interface-regions.md)** -- what every region renders, and what it refuses to do.
- **[Step a battle in the Workbench](../how-to/balance-with-the-workbench.md)** -- when a previewed number is not the number you expected.
