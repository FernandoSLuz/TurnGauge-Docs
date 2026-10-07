# 8. Explore Combat Studio

Combat Studio previews semantic battle-interface slots while keeping rules and
simulation separate. Its native workflow is currently validated on Unity 6000.3.25f1
(Unity 6.3) with the Built-in render pipeline. The runtime profile gallery has a fresh
English capture pass for the rendered states; editor workflow video and release approval
remain separate requirements, so this guide describes the steps and gates without claiming
approval beyond that validation.

## Open a profile

1. Confirm that the verified editor configuration is available. If the Studio menu is
   missing, stop here and resolve the editor/package mismatch.
2. Choose **Tools > TurnGauge > Combat Studio > Open**.
3. Select a preset, then choose **Create copy** to save a profile you own.
4. Choose `uGUI` for Canvas, Button, Animator and prefab workflows, or `UI Toolkit`
   for UXML, USS and UI Builder workflows.
5. Choose the **Fantasy** or **Science Fiction** identity.

In the composition section, **Side team information** is the `UseSideInformationBanks`
presentation-only toggle. New profiles default to disabled; the supplied Fantasy uGUI and
Fantasy UI Toolkit profiles enable it. It groups the team information beside the stage and
never changes formation or simulation coordinates. The four starting combinations are only
layout examples. Keep the preview visible while changing the profile or test state.

## Place the semantic slots

The uGUI adapter expects `Roster`, `Timeline`, `Actions`, `Targets`, `Confirm`, `Cancel`,
`Concede`, `Feedback` and `Result`. UI Toolkit uses the lowercase names. Names are case
sensitive. Confirm, Cancel and Concede must be native Button controls.

Slots can be anywhere in the authored hierarchy. Missing or duplicate slots produce a
diagnostic; the adapter does not silently invent authored layout. An optional
`DecisionSummary` slot displays the selected action, cost and target count.

The adapter renders state and sends intents to `BattleViewSession`. The simulation still
validates every command. A pending submission remains pending until it is accepted or
rejected, so retry after the submission callback returns.

## Edit appearance

For UI Toolkit, open the assigned VisualTreeAsset in UI Builder and edit its USS. For
uGUI, open the prefab in Prefab Mode and place the semantic slots with native controls.
Use **Build Default Layout** only when you want a generated starting composition.

Theme controls can change colors, text size, sprites, materials and fonts. Keep
`ReduceMotion` available to the host: it snaps bars, suppresses token pulses and
compresses visual beats without changing the battle or selected command.

## Apply, discard and use a profile

During preview, Studio **Undo** and **Discard** operate on the session's working copy.
Only **Apply** writes the profile asset and records an asset Undo step. UI Builder saves its
UXML separately through its own editor workflow; Studio Discard does not undo an already
saved UXML. If the source asset changes externally while a draft exists, Apply refuses to
overwrite it; create a copy or discard the draft.

Assign the profile to the controller's **Presentation Profile** field. The equivalent
runtime setup is:

```csharp
controller.ConfigurePresentation(profile);
controller.ConfigureBattle(profile.Catalog, profile.EncounterId, 42u);
controller.StartBattle();
```

Choose the catalog and encounter that belong to the same scheduler family. Action Order
and ATB are separate authored variants, and Studio does not rewrite incompatible
mechanics for you.

## Presentation boundary

The preview stage receives the same snapshots and events as the native HUD. It does not
change simulation rules. A stage-preset swap changes visual playback only; stop the
battle before changing its presenter or UI technology.

For the engine and presenter split, see [Architecture](../explanation/architecture.md).
For the no-code authoring path, see [Build your combat without code](build-without-code.md).
