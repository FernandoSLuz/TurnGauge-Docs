# Editor tools

2 types in this area.

## BattleSkinBrowserWindow

```csharp
public sealed class BattleSkinBrowserWindow : EditorWindow
```

`TurnGauge.Editor` &middot; <small>TurnGauge/Editor/Skins/BattleSkinBrowserWindow.cs</small>

Browse the shipped skins, preview them with the real shader, and turn any
of them into an editable asset in one click.

This window exists because the package previously offered no way to
discover or create a look: a customer had to create a blank asset and fill
in fields with no preview. "Create editable copy" is the intended entry
point for authoring a custom skin.

**Fields**

`public BattleSkinPreset Asset`

:   The asset this entry was loaded from, or null for a shipped skin. The actions that need a file on disk are disabled while it is null.

`public bool IsShipped`

:   Whether the look is defined in package code rather than by an asset. Shipped entries are listed first and cannot be edited in place, which is what `Create editable copy` is for.

`public CompiledBattleSkin Skin`

:   The compiled look this row previews. For a project asset it is a compile of that asset taken at refresh time, so an edit made elsewhere appears once the window regains focus, not before.

**Methods**

`public static void Open()`

:   Opens the skin browser, or brings it forward when it is already open. Also reachable from Tools > TurnGauge > Skin Browser.

`public void Refresh()`

:   Rebuilds the list from shipped skins plus project assets.

---

## CombatStudioSampleBuilder

```csharp
public static class CombatStudioSampleBuilder
```

`TurnGauge.Editor.CombatStudio` &middot; <small>TurnGauge/Editor/CombatStudio/CombatStudioSampleBuilder.cs</small>

Creates editable starter profiles and native view prefabs using
Unity's asset APIs. No serialized YAML is authored by the tool.

**Methods**

`public static void BuildSamples()`

:   Creates missing editable fantasy/science-fiction profiles and native view prefabs, repairs missing references in existing examples, and saves the assets. Requires an idle EditMode Editor with a starter catalog and no compilation errors; authored profile choices are retained.

`public static PresentationStagePreset GetOrCreateStagePreset(BattleLayoutIdentity identity)`

:   Creates an editable example using the shipped recipes and neutral art. Repeated calls preserve existing assets and all authored values. Camera movement starts disabled until its composition is validated.
    - `identity` &mdash; Fantasy or science-fiction example identity used to choose the native asset path.
    - **Returns** &mdash; The preserved or newly created editable preset for this identity.

---

