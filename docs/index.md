---
hide:
 - navigation
---

<div class="hero" markdown>

# TurnGauge

<p class="tagline">Deterministic, replayable turn and tempo battles for Unity. Action-order
or ATB scheduling, formations, statuses, reactions, AI policies, a Monte Carlo balancing
workbench, and a battle interface you can restyle from one asset.</p>

</div>

<figure markdown>
  ![A battle drawn with the Slate Nocturne skin](assets/images/hero-battle.png){ .shot }
  <figcaption>Slate Nocturne, the default skin. Roster, turn-order strip, skill tray, tooltip,
  log and the bars above each combatant are drawn by a signed-distance-field shader, so the
  interface ships no texture and no font. <strong>Character art is yours:</strong> this frame
  binds none, which is why each combatant is a name, its bars and its status pips over empty
  ground.</figcaption>
</figure>

---

## Choose your path

<div class="cards" markdown>

<div markdown>

### See it work

Run the shipped demo scene, then prove with your own seed that the same inputs replay.

[Install and run the demo ->](tutorials/first-battle.md)

</div>

<div markdown>

### Drive it from my code

Compile a catalog, create an engine from an encounter and a seed, pump it from a MonoBehaviour.

[Run a battle from code ->](tutorials/run-a-battle-from-code.md)

</div>

<div markdown>

### Match my game

Turn a shipped skin into an asset you own, then put every interface region where you want it.

[Restyle the interface ->](tutorials/skinning-your-battle.md)

</div>

<div markdown>

### Make it fair

Step a battle tick by tick, read the formula trace behind a number you did not expect.

[Step a battle in the Workbench ->](how-to/balance-with-the-workbench.md)

</div>

</div>

Looking for a type rather than a task? The [API reference](reference/index.md) lists 417 public
types, grouped by what they are for and filterable as you type.

## What it does

You author content as assets. A compiler freezes it. The engine runs a battle from content, an
encounter and a seed, and returns events plus a snapshot. A presenter draws them. The interface
offers legal choices and raises intent; your driver submits the command.

### What determinism buys you

The same encounter, scheduler, formation and seed produce the same battle every time, so a bug
report can be a seed and a replay file rather than a description. That holds structurally:

- `TurnGauge.Simulation` is compiled with `noEngineReferences: true`. It cannot reach
  `UnityEngine.Random`, `Time` or a `GameObject`, even by accident.
- Amounts are `Fixed64` and chances are `Chance64`, both integer-backed. No float reaches a
  value that feeds a hash. Their `ToString` returns the raw scaled integer used by canonical
  encoding, so [text a player reads](tutorials/take-player-input.md) goes through
  `BattleNumberFormat`.
- Pause, speed and skip scale the visual clock only. No presentation value changes an outcome.

### The shape of the code

=== "Running a battle"

    ```csharp
    var result = new BattleContentCompiler().Compile(
        AuthoringCompileRequest.WithBuiltIns(catalog));

    var encounter = result.CatalogSnapshot.Encounters[0].Value;

    var engine = BattleEngine.Create(
        result.CatalogSnapshot.BattleContent, encounter.StartRequest, seed: 12345u);

    var step = engine.AdvanceTicks(ticks);   // Events, Snapshot, Outcome
    ```

=== "The interface submits nothing"

    ```csharp
    ui.CommandChosen += choice =>
    {
        var snapshot = engine.GetSnapshot();

        engine.Submit(new BattleCommand(     // only the driver submits
            snapshot.NextCommandSequence, snapshot.Tick, BattleIds.UseSkillCommand,
            choice.ActorId, choice.SkillId, choice.Targets, PropertySet.Empty));
    };
    ```

## Requirements

| Requirement | Detail |
| --- | --- |
| Core engine | Engine-free data and simulation assemblies are designed for Unity 2022.3 compatibility |
| Native editor | Presentation, Studio and adapters are currently validated on Unity 6000.3.25f1 (Unity 6.3), Built-in |
| Other pipelines/editors | Pending verification |
| Dependencies | None. No DRM, no telemetry, no online activation |

!!! note "What you still bring"
    TurnGauge draws the interface, the stage and the bars. Character art, animation and audio
    stay yours. The sample scene binds placeholder tokens, status icons and sound effects so you
    can see the presentation layer working before you replace them.

!!! note "Working name and evidence"
    TurnGauge is a working name pending legal, store and domain clearance. The current
    source guides describe editor workflows; they do not establish release approval or
    native-editor support beyond the validated Unity 6.3 configuration above. The native
    runtime profile gallery has a fresh English capture pass; real-mouse editor workflow video
    evidence remains a separate pending requirement.

## Next

- [Install and run the demo](tutorials/first-battle.md) &mdash; a battle on screen, then the
  same battle again from the same seed.
- [Architecture](explanation/architecture.md) &mdash; the three roles and the one boundary.
- [Author content in the right order](how-to/author-content.md) &mdash; the asset layers.
