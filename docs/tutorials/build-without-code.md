# 2. Build your combat without code

This tutorial uses the editor to create a playable battle, change its numbers, add a
combatant and author a skill. The deterministic core and data source remain compatible
with Unity 2022.3; the native templates, adapters and editor workflow described here are
currently validated on Unity 6000.3.25f1 (Unity 6.3) with the Built-in render pipeline.
TurnGauge is a working name pending legal, store and domain clearance.

## Before you start

Import TextMeshPro Essential Resources once in the project:

**Window > TextMeshPro > Import TMP Essential Resources**

The current source workflow also expects the package's editor menus to be present in that
validated native configuration. If a menu or field named below is absent, stop at that
step and check the editor/package version. This page records the source workflow; it is
not evidence of native support in another editor or a release approval.
A new profile starts with **Dados da equipe nas laterais** disabled. This presentation-only
option is the `UseSideInformationBanks` field. The supplied Fantasy uGUI and Fantasy UI
Toolkit sample profiles enable it; other new profiles keep the default disabled until you
choose it.

## Step 1 - Create the playable battle

1. Open a scene, or create a new one.
2. Choose **Tools > TurnGauge > Create Playable Battle**.
3. Leave `StarterCatalog` selected and choose **Playable Battle**.
4. Click **Create Playable Battle**, then press **Play**.

The wizard creates the runtime controller, presenter, UI root and required input service.
The opening encounter is a 3 v 3: Vanguard, Ranger and Mender versus Duelist, Adept and
Colossus. When a human-controlled member is ready, the battle pauses for a choice.

## Step 2 - Learn the asset chain

TurnGauge compiles the assets listed in a **Battle Content Catalog**. Each asset must be
in the catalog before the runtime can use it, and every asset keeps its Stable ID even if
its filename changes.

| Asset | Role |
| --- | --- |
| Stat | A value such as Power or Maximum Health |
| Resource | A pool a skill spends, such as Energy |
| Effect | One result, such as damage, healing or a shield |
| Target | The resolver that chooses who an effect reaches |
| Skill | Cost, timing, target and effects shown as one choice |
| Combatant | Stats and granted skills for one actor |
| Team | Combatant members and their Human or Automatic control |
| Formation Preset | The authored slots where members stand |
| Encounter | Two teams, their formation and their scheduler |
| Battle Content Catalog | The set compiled for a battle |

Create assets from **Assets > Create > TurnGauge > ...**. Use the starter assets as
working examples, or duplicate the starter content before editing it.

## Step 3 - Change a number

Open `combatant.vanguard`, find `stat.maximum-health` under **Base Stats**, and raise its
value. Press **Play** again to see the change.

To change damage, open `effect.damage.strike` and edit **Potency**. Potency is fixed
point: `10000` means `1.0`, while `7000` means `0.7`. Keep changes small while tuning.
Then use **Tools > TurnGauge > Content Validator** to catch missing references before
starting another battle.

## Step 4 - Add a combatant

1. Choose **Assets > Create > TurnGauge > Combatant**.
2. Give it a new Stable ID, for example `combatant.pyromancer`.
3. Add `stat.maximum-health` and the source stats its skills will read.
4. Add existing skills under **Granted Skills**.
5. Add the combatant to the catalog.
6. Open a Team, add a member row, set a unique Combatant Instance ID, and choose
   **Human** or **Automatic** control.
7. Open the Encounter and assign the member to a formation slot.

Control belongs to the member row. A team can therefore mix one human leader with
automatic companions.

## Step 5 - Add a skill

Create an **Effect** and choose its implementation from the editor dropdown. Common
choices are Damage, Heal, Apply Status, Shield, Resource, Dispel, Interrupt and
Scheduler Adjust. Create a **Target** separately, then create a **Skill** that refers to
both.

For the Skill, set:

- **Minimum / Maximum Requested Targets** to `1` / `1` when the player must pick one;
  use `0` / `0` when the resolver chooses automatically.
- **Cast Ticks** for wind-up time and **Recovery Ticks** for the next action delay.
- **Costs** for resource IDs and amounts.
- A unique **Entry ID** for every effect entry.

Formation Row and Formation Side targets need a Team Scope. Set an enemy scope for an
attack that must not hit the acting party. Check that the target can still resolve when
the row is nearly empty.

Add the skill to the catalog and to a combatant's **Granted Skills**, then run the
validator before pressing Play.

## Step 6 - Choose the targeting interaction

On the skin's **Targeting** section, choose the interaction that fits the device:

| Preset | Use it when |
| --- | --- |
| `Reticle` | Keyboard or controller selection is the primary interaction |
| `Direct` | Stage clicks or touch should select the combatant |
| `SlotGrid` | Many combatants or overlapping sprites need a stable button row |
| `AutoConfirm` | The resolver makes the choice and no target prompt is wanted |

This changes presentation and input flow only. Target legality remains the resolver's
simulation contract.

## Step 7 - Validate and tune

Run **Tools > TurnGauge > Content Validator**. It reports broken references and illegal
content before runtime. Then open **Tools > TurnGauge > Battle Workbench** to inspect the
order, legal targets and formula traces, or run Monte Carlo batches over multiple seeds.

## Step 8 - Make the result yours

Open **Tools > TurnGauge > Skin Browser**, choose a shipped look and use **Create editable
copy...**. Assign the resulting skin to `BattleUiRoot`. The browser flow is shown in the
[Skin Browser walkthrough](skinning-your-battle.md#the-authoring-loop). A skin changes presentation only;
it does not change battle hashes.

For a complete reference to the runtime boundary, see [Run a battle from code](run-a-battle-from-code.md),
[Combat Studio](combat-studio.md), and [Validation and Troubleshooting](../how-to/troubleshooting.md).
