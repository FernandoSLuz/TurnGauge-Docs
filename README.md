# TurnGauge

**Deterministic, replayable turn and tempo battles for Unity.** Action-order or ATB
scheduling, formations, statuses, reactions, AI policies, a Monte Carlo balancing
workbench, and a skinnable battle interface.

> Documentation only. The product source is not in this repository.

---

## Learn it from scratch

The site is published at <https://fernandosluz.github.io/TurnGauge-Docs/>. Read the tutorials in
order. Each one ends where the next begins.

| # | Tutorial | You will be able to |
| --- | --- | --- |
| 1 | **[Install and run the demo](docs/tutorials/first-battle.md)** | Create the 3 v 3 playable battle and prove the same seed replays |
| 2 | **[Build your combat without code](docs/tutorials/build-without-code.md)** | Author a combatant, skill, target and encounter from the editor |
| 3 | **[Put a battle in your scene](docs/tutorials/playable-battle-in-a-scene.md)** | Add the playable battle to your own scene |
| 4 | **[Run a battle from your own code](docs/tutorials/run-a-battle-from-code.md)** | Compile a catalog, create an engine, pump it from a MonoBehaviour |
| 5 | **[Draw the battle on screen](docs/tutorials/show-the-battle.md)** | Bind the presenter, forward events, frame the stage |
| 6 | **[Take a decision from the player](docs/tutorials/take-player-input.md)** | Offer legal choices, submit the command, fill a tooltip |
| 7 | **[Restyle the interface](docs/tutorials/skinning-your-battle.md)** | Make the interface look like *your* game |
| 8 | **[Explore Combat Studio](docs/tutorials/combat-studio.md)** | Preview semantic UI layouts and connect a profile |
| 9 | **[Add custom mechanics](docs/tutorials/custom-mechanics.md)** | Register deterministic effect and target extensions |

Then work by task:

| Task | Where |
| --- | --- |
| Create stats, effects, skills, combatants, encounters | **[Author content in the right order](docs/how-to/author-content.md)** |
| Place combatants and fit the interface to a screen | **[Formation Editor](docs/how-to/place-formations.md)** &middot; **[Fit the battle to your screen](docs/how-to/interface-layout.md)** |
| Step a battle, read formula traces, run Monte Carlo | **[Workbench](docs/how-to/balance-with-the-workbench.md)** &middot; **[Monte Carlo batches](docs/how-to/monte-carlo-batches.md)** |
| Fix the errors you are most likely to hit | **[Troubleshooting](docs/how-to/troubleshooting.md)** |
| Understand the driver, engine, presenter split | **[Architecture](docs/explanation/architecture.md)** |
| Look up any public type or member | **[API reference](docs/reference/index.md)** |

**If you have 10 minutes:** tutorial 1, then
[the four shipped skins](docs/tutorials/skinning-your-battle.md#the-four-shipped-skins).

---

## What it actually does

You author content as assets: stats, resources, skills, effects, statuses, reactions,
AI policies, formations, teams, encounters. A **compiler** freezes that catalog into
immutable content. The **engine** runs a battle from `(content, encounter, seed)` and
emits an event stream plus snapshots.

The same `(encounter, scheduler, formation, seed)` tuple **always** produces the same
state hashes and the same replay -- on every machine and platform. That is not a promise,
it is structural:

- `TurnGauge.Simulation` is compiled with `noEngineReferences: true`. It cannot touch a
  `GameObject`, a `Transform`, or `UnityEngine.Random` even by accident.
- Amounts are `Fixed64` and chances are `Chance64`, both integer-backed. No float ever
  reaches a value that feeds a hash.
- The presentation layer receives values and draws them. It never mutates a battle, and
  a purity audit enforces that in tests.

Pause, speed, and skip scale the *visual* clock only. A battle watched at 4x and one
watched paused-and-stepped produce identical results.

## What ships

- Two schedulers out of the box: **Action Order** and **ATB**, with a registry for your
  own.
- Effects, statuses, shields, resources, cooldowns, cast times, interrupts, reactions
  with cycle-safe validation, and pluggable AI policies.
- **Formations**: authored slot layouts projected to any viewport, with an editor.
- **Replays**: a versioned envelope with migrations, so a recorded battle still plays
  back after you ship a patch.
- **Battle Workbench**: step tick by tick, inspect the scheduler queue and every formula
  trace, and run Monte Carlo batches across many seeds.
- **Content Validator**: catches broken references and illegal content before runtime.
- Four shipped interface skins, plus a Skin Browser that turns any of them into an asset
  you own.
- No third-party dependencies. No DRM, no telemetry, no online activation.

## Requirements

- The core engine and data assemblies are engine-free and designed for Unity 2022.3
  compatibility.
- Native presentation, Studio and adapters are currently validated on Unity **6000.3.25f1**
  (Unity 6.3) with the Built-in render pipeline. Other editor versions and pipelines remain
  pending verification.

The interface is drawn with a signed-distance-field shader, so it stays crisp at any
resolution and ships no textures. Glow is drawn in-shader, which is why the package needs
no post-processing stack and cannot conflict with your volumes.

## Support

Open an issue on this repository for documentation problems. For product issues, include
your Unity version and the `(encounter, seed)` pair that reproduces it -- determinism
means that is usually enough to reproduce exactly.
