# 9. Add custom mechanics

This tutorial adapts the shipped Custom Mechanics sample for the web documentation. It
uses deterministic C# extensions registered explicitly by the host. The core extension
contract is source-compatible with Unity 2022.3, while the native authoring flow is
currently validated on Unity 6000.3.25f1 (Unity 6.3) with the Built-in render pipeline.
No native editor capture or release build approval is claimed; run the validator and
Unity tests in the validated editor before treating a custom integration as ready.

## What the sample adds

- `CustomShieldEffectResolver` creates a shield from a target's missing health.
- `LowestHealthAllyTargetResolver` chooses the living ally with the lowest health ratio.

Both implementations use immutable contexts and fixed-point values. Ties use ordinal
Stable ID order, so the same catalog and seed resolve the same target.

## Configure the sample

1. Choose **Assets > Create > TurnGauge > Samples > Custom Mechanics Registry Provider**.
2. Create an Effect asset. In the **Implementation** picker, select the custom
   missing-health shield entry and set contract version `1`; do not type an implementation
   ID into a free text field. Configure:

   | Key | Type | Example |
   | --- | --- | --- |
   | `custom-shield-id` | StableId | `shield.custom-protection` |
   | `custom-shield-priority` | Int32 | `1` |
   | `custom-shield-ratio` | Fixed64 | raw `5000` (`0.5`) |

   The ratio must be in raw units from `1` through `10000`. Missing, extra or wrongly
   typed keys fail catalog compilation.
3. Create a Target asset. In the **Implementation** picker, select the custom
   lowest-health ally entry, set contract version `1`, and leave the property set empty.
   Registry IDs are shown here only as reference names; the editor picker is the authoring
   path.
4. Create a Skill that refers to the Effect and Target. Set minimum and maximum requested
   targets to `0`, Cast Ticks to `0`, and Recovery Ticks to a positive value such as `20`.
   Give the effect entry a unique Entry ID.
5. Add the Effect, Target and Skill to the same catalog. Add the Skill to the acting
   combatant's Granted Skills and keep all referenced teams, formations and encounters
   in that catalog.
6. Set one living ally to **Explicit Current Health**. At 50 of 100 health, the example
   ratio produces a shield of 25. A full-health target produces no shield event.
7. In Combat Studio, choose the catalog and encounter under **Rules**, select **Custom C#
   mechanics** as the provider, and choose **Restart Test**. In a scene, assign the
   provider to the runtime controller or Workbench `BattleRegistryProvider` field.

If any menu or field in these steps is absent, stop at that gate and verify the editor
and package source. Do not substitute a guessed registry key or claim the native flow is
currently approved.

## Register and replay

The provider is explicit; runtime does not scan assemblies. Create the registries and use
the same mechanics registry to read and execute a replay:

```csharp
var registries = provider.CreateRegistries();
var bytes = ReplaySerializer.Write(ReplayEnvelope.Capture(engine));
var read = ReplaySerializer.Read(bytes, registries.MechanicsRegistry);
if (read.Succeeded)
{
    var replayed = ReplayExecutor.Execute(
        read.Replay,
        registries.SchedulerRegistry,
        registries.MechanicsRegistry);
}
```

The built-ins-only replay overload rejects this custom content. Matching IDs and contract
versions identify an implementation, so preserve the behavior required by existing
replays or give changed behavior a new implementation identity.

## Validate the boundary

Compile the catalog with the provider's scheduler and mechanics registries. Then run the
focused custom-mechanics and replay tests in the product repository. A successful source
compile is evidence for that integration only; it does not establish release, platform,
or native-editor approval.

See [Effects and mechanics](../reference/effects-and-mechanics.md), [Replay](../reference/replay.md),
and [Build your combat without code](build-without-code.md).
