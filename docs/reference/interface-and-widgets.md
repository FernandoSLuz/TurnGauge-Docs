# Interface and widgets

26 types in this area.

!!! abstract "On this page"
    [BattleEventNarrator](#battleeventnarrator) &middot; [BattleNumberFormat](#battlenumberformat) &middot; [BattleUiCommandChoice](#battleuicommandchoice) &middot; [BattleUiRoot](#battleuiroot) &middot; [DecisionOptions](#decisionoptions) &middot; [DecisionShapeCompiler](#decisionshapecompiler) &middot; [DisplayStringTable](#displaystringtable) &middot; [DisplayStringTableProvider](#displaystringtableprovider) &middot; [FeedbackLogView](#feedbacklogview) &middot; [ResultBannerView](#resultbannerview) &middot; [SafeAreaFitter](#safeareafitter) &middot; [SkillCommandShape](#skillcommandshape) &middot; [SkillTitleView](#skilltitleview) &middot; [SkillTrayView](#skilltrayview) &middot; [SkinnedTokenPlate](#skinnedtokenplate) &middot; [SkinnedValueBar](#skinnedvaluebar) &middot; [SkinnedWidgetFactory](#skinnedwidgetfactory) &middot; [StatusRosterView](#statusrosterview) &middot; [TargetPickerView](#targetpickerview) &middot; [TargetShape](#targetshape) &middot; [TimelineStripView](#timelinestripview) &middot; [TooltipData](#tooltipdata) &middot; [TooltipPanelView](#tooltippanelview) &middot; [TransportBarView](#transportbarview) &middot; [UiStatusEntry](#uistatusentry) &middot; [UiTimelineEntry](#uitimelineentry)

## BattleEventNarrator

```csharp
public static class BattleEventNarrator
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/BattleEventNarrator.cs</small>

Turns one battle event into a sentence a player can read.

The feedback log used to render an event's raw type id followed by the
actor in brackets - `scheduler.combatant-ready [Clockwork Rival]` -
which is an engineer's log line shown to a customer as if it were game
text. The values needed to say it properly were always there: the event
carries the actor, the target, the skill, and the amount, and the display
string table has names for all of them.

Nothing here is authoritative. It reads an event that has already
happened and produces text; it resolves nothing, computes nothing, and
cannot change a hash. An event shape it does not recognise falls back to
the labelled type id, so a project that adds its own events still gets a
readable line rather than an empty one.

**Methods**

`public static string Describe(BattleEvent battleEvent, DisplayStringTable labels)`

:   Writes one log line for `battleEvent`.
    - `battleEvent` &mdash; The event to describe. Null returns an empty string.
    - `labels` &mdash; Display names for the ids in the event. Null, or an id the table does not carry, falls back to the raw id text, which is what keeps an unlabelled project readable rather than blank.
    - **Returns** &mdash; One sentence, already capitalised and punctuated. Never null.

`public static bool IsPlayerFacing(BattleEvent battleEvent)`

:   Whether an event belongs in the log a PLAYER reads. The engine emits its own bookkeeping alongside the things that happen in the fiction, and the log printed all of it. Roughly two lines in five were "command.accepted - Ember Vanguard", "reaction.suppressed - Pale Adept", or "Action Completed - Sable Ranger" -- engine vocabulary shown to a customer, burying the four lines that actually told them they were losing. Everything filtered here is still in the event stream, still in replays, and still shown in full by the Workbench; it is only kept out of the player's log.
    - `battleEvent` &mdash; The event to judge. Null is not player-facing.
    - **Returns** &mdash; True when the event is worth a line in the battle log.

---

## BattleNumberFormat

:material-star: **Start here**

```csharp
public static class BattleNumberFormat
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/BattleNumberFormat.cs</small>

Turns the simulation's fixed-point types into player-facing text.

`Fixed64` and `Chance64` deliberately expose only
raw scaled integers, because their `ToString` feeds canonical
encoding and must never drift. A tooltip that printed those directly would
show "50000" instead of "5" and "875000" instead of "87.5%", so display
formatting belongs here in the presentation layer.

Every conversion is integer arithmetic. No float ever touches a value that
could be mistaken for an authoritative number.

**Fields**

`public const int AmountDecimals`

:   Maximum decimal places shown for a fixed-point amount.

**Methods**

`public static string Amount(Fixed64 value)`

:   Formats a fixed-point amount, trimming trailing zeros: 5, 5.5, 5.25.
    - `value` &mdash; Signed fixed-point battle amount to render without culture-dependent separators.
    - **Returns** &mdash; Invariant decimal text with insignificant fractional zeroes removed.

`public static string AmountRange(Fixed64 minimum, Fixed64 maximum)`

:   Formats a range as "12" when both ends match, otherwise "10-14".
    - `maximum` &mdash; Upper fixed-point preview bound.
    - `minimum` &mdash; Lower fixed-point preview bound.
    - **Returns** &mdash; One rounded amount when bounds match, otherwise a hyphenated minimum-to-maximum range.

`public static string Percent(Chance64 value)`

:   Formats a chance as a percentage, trimming trailing zeros: 100%, 87.5%, 0.05%.
    - `value` &mdash; Million-scale probability to convert into percentage units.
    - **Returns** &mdash; Invariant percentage text with up to four fractional digits and no trailing zeroes.

`public static string Ticks(int ticks)`

:   Formats a tick count as a short duration, "12t".
    - `ticks` &mdash; Signed simulation tick count.
    - **Returns** &mdash; Invariant integer text followed by the `t` tick suffix.

`public static string WholeAmount(Fixed64 value)`

:   Formats a fixed-point amount rounded to a whole number, which is what damage and healing readouts usually want.
    - `value` &mdash; Signed fixed-point battle amount to round to the nearest integer.
    - **Returns** &mdash; Invariant whole-number text rounded with the simulation value's integer conversion.

---

## BattleUiCommandChoice

```csharp
public readonly struct BattleUiCommandChoice
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/BattleUiRoot.cs</small>

A player-chosen command the driver (not the UI) will submit.

**Constructors**

`public BattleUiCommandChoice()`

:   Records one choice for the driver to act on.
    - `actorId` &mdash; Pending human actor that owns the choice.
    - `isConcede` &mdash; True for a concession, which carries no skill.
    - `skillId` &mdash; Chosen skill, or null for concession.
    - `targets` &mdash; Target ids the player picked. Null becomes empty, and empty leaves exact target resolution to the driver.

**Properties**

`public StableId ActorId`

:   The combatant the command is for. It is taken from the pending decision rather than from whoever clicked, so it always matches the actor the engine is waiting on.

`public bool IsConcede`

:   True when the player conceded instead of picking a skill. Such a choice carries no `SkillId` and no `Targets`.

`public StableId? SkillId`

:   The skill the player picked; null when the choice is a concession.

`public FrozenList<StableId> Targets`

:   The targets the player picked, never null. Empty means the driver still owns target resolution; the shipped tray always raises choices empty.

---

## BattleUiRoot

:material-star: **Start here**

```csharp
public sealed class BattleUiRoot : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/BattleUiRoot.cs</small>

The battle interface. It offers the pending actor's legal command shapes,
surfaces the timeline, roster, feedback log, tooltips, and terminal
results verbatim from snapshots and events, and raises a plain C# event
with the chosen command for the DRIVER to submit.

It submits nothing, resolves no targets exactly, and invokes no simulation
or preview API; tooltips are supplied to it as computed
`TooltipData` values.

Every colour, size, font, animation timing, and region position comes from
a `BattleSkinPreset`, so the whole interface restyles from one
asset with no prefab editing. With no preset assigned it falls back to the
shipped default skin rather than rendering unstyled boxes.

**Properties**

`public CompiledSkinLayout ActiveLayout`

:   The layout actually in use, which is the skin's layout adapted to the current screen shape. Read this rather than `Skin.Layout` when you need to know where the interface really is, because a portrait screen stacks the bands and drops the side cells.

`public DecisionOptions CurrentDecision`

:   The decision currently on offer, or `DecisionOptions.None` when there is nothing to decide. Never null, so it can be read without a guard between battles.

`public IReadOnlyList<string> FeedbackLines`

:   The retained feedback log, oldest line first. A live view, capped at `MaximumFeedbackLines` by dropping the oldest lines.

`public string InputUnavailableMessage`

:   Empty, because shortcuts are available in this build.

`public string InputUnavailableMessage`

:   Display-ready explanation of why the keyboard shortcuts are missing and which project setting restores them. Empty in builds that have them.

`public bool IsChoosingTarget`

:   True while the player is choosing targets for a skill.

`public bool IsResultShown`

:   Whether the result banner is currently up. A `ShowResult` call whose result is null, not yet terminal, or carries no result id clears this again, which is what makes the call safe to repeat every frame.

`public BattleUiCommandChoice? LastCommandChoice`

:   The most recent choice raised through `CommandChosen`. Null until the player has chosen once, and never cleared afterwards.

`public bool LegacyInputAvailable`

:   Classic input is available; the demo polls it here.

`public bool LegacyInputAvailable`

:   The legacy input manager is disabled. The tray remains fully clickable through the graphic raycaster, so only the number-key shortcuts are unavailable; nothing throws.

`public IReadOnlyList<SkillCommandShape> OfferedSkills`

:   The skill shapes the tray is offering, in the order the decision supplied them. Empty whenever no actor is pending.

`public IReadOnlyList<StableId> OfferedTargets`

:   The candidates currently on offer in the picker, or an empty list when no target is being chosen.

`public bool OffersConcede`

:   Whether a concede button is offered. This is exactly the condition under which `ChooseConcede` raises anything, so a custom tray can use it to decide whether to draw the button at all.

`public IReadOnlyList<StableId> PickedTargets`

:   The picks made so far, in pick order. A live view of the interface's own list, emptied as soon as the pick is committed or abandoned.

`public bool PresentationVisible`

:   Shows only this view's owned visuals without disabling a shared host object.

`public StableId? ResultId`

:   The id of the surfaced result, or null while none is shown. This is the simulation's own result id, not a display string; use the label table to turn it into text.

`public string ResultText`

:   One-line text form of the surfaced result, with the winning team appended when there is one. Empty while no result is shown. The banner draws its own labels; this string is for logs and tests.

`public CompiledBattleSkin Skin`

:   The resolved skin this interface draws with.

`public Vector2 StageInsets`

:   The share of the screen the interface's full-width bands claim, as a (top, bottom) pair of fractions. This is what makes the protected stage a fact rather than an intention: `BattleStageFrame` reads it instead of carrying its own margins, so a skin that grows its rail cannot silently start drawing over the combatants.

`public IReadOnlyList<UiStatusEntry> StatusEntries`

:   The surfaced status rows, in snapshot order. A live view, rebuilt in place by every `UpdateStatus` call.

`public StableId? TargetingSkillId`

:   The skill targets are being chosen for, or null while none is.

`public IReadOnlyList<StableId> TimelineActors`

:   The actors on the timeline strip, in the order they were supplied. This is a live view of the interface's own list, so copy it if you need it to survive the next update.

`public RectTransform TransportMount`

:   A mount point for host-supplied controls such as the sample's scenario picker, placed by the skin's transport region.

`public Vector2 ViewportSize`

:   The size the interface is actually being drawn into. This is deliberately not `Screen`. A canvas can be smaller than the screen, can belong to a camera rendering into a texture, and in batch mode reports 640x480 whatever the render target really is - so a layout that switches on Screen switches on the wrong thing and cannot be checked at any resolution but the one the window happens to be. The canvas's own rect follows the real target, so it is what decides.
    - **Returns** &mdash; The canvas rect when it has one, then the camera's pixel rect, and only then the screen - each fallback used only when the one before it has not been established yet.

**Fields**

`public const int MaximumFeedbackLines`

:   Section 10 cap: feedback log lines retained.

**Events**

`public event Action<BattleUiCommandChoice> CommandChosen`

:   Raised when the player chooses a command; never submitted here.

**Methods**

`public void AppendFeedback(BattleEvent battleEvent, DisplayStringTable labels)`

:   Appends one feedback line from an event (bounded log).
    - `battleEvent` &mdash; The event to describe; null appends nothing. Its type id, plus the actor id when the event carries one, become the line.
    - `labels` &mdash; Display names for those ids. Any id the table does not cover, and every id at all when this is null, is written as the raw id text.

`public void ApplySkin(BattleSkinPreset preset)`

:   Replaces the skin and rebuilds the interface. Safe to call at runtime, which is what lets the Skin Browser preview a look live.
    - `preset` &mdash; The look to adopt, or null to fall back to the shipped default skin.

`public bool BeginTargeting(StableId skillId)`

:   Opens the target picker for one offered skill. It declines, and returns false, whenever there is nothing to pick: an automatic-selection resolver, a skill that requires no ids, a skin with the picker region hidden, or no supplied candidate list. A caller that gets false should raise the choice with no targets, which leaves resolution to the driver as it always did.
    - `skillId` &mdash; The offered skill to pick targets for.
    - **Returns** &mdash; True when the picker is now on screen.

`public void BindStage(BattleStage2D stage)`

:   Hands the interface the stage the reticle should sit on. The presenter calls this when it binds; a project driving the interface without a presenter can call it too, and leaving it unset simply means the cursor treatment falls back to the button row.
    - `stage` &mdash; The stage whose tokens the reticle points at.

`public void CancelTargeting()`

:   Abandons the pick in progress and puts the skill tray back. Safe to call when no target is being chosen.

`public void ChooseConcede()`

:   Raises a concession command for the driver. Silently does nothing unless the pending decision actually offers concession.

`public void ChooseSkill(StableId skillId, IReadOnlyList<StableId> targets)`

:   Raises the chosen-skill command for the driver. The UI submits nothing; it only surfaces the player's intent.
    - `skillId` &mdash; The skill the player picked. Nothing is raised while no actor is pending, and the id is not re-checked against the offer.
    - `targets` &mdash; Exact targets, copied into the choice. Null or empty hands target resolution to the driver, which is what the shipped tray does.

`public void ClearDecision()`

:   Clears any offered decision.

`public void ClearTargetCandidates()`

:   Forgets every supplied candidate list. Call it before supplying the lists for a new decision so a combatant that has since died cannot linger in the picker.

`public void ConfirmTargets()`

:   Commits the current picks and raises the skill choice. Does nothing while fewer targets are picked than the skill requires.

`public void Initialize()`

:   Builds the uGUI tree. Explicit so EditMode tests can call it. Awake already calls it, and a second call does nothing.

`public void MoveReticle(int delta)`

:   Steps the reticle to the next or previous candidate, wrapping at both ends. Does nothing under a preset that has no cursor.
    - `delta` &mdash; How many candidates to move; negative steps back.

`public void PickPointedTarget()`

:   Picks whoever the reticle is currently over. This is the confirm half of the cursor treatment; the direction keys are the other half.

`public void PickTarget(StableId combatantId)`

:   Picks or unpicks one combatant. Ignored unless a target is being chosen and the id is one of the offered candidates, so it is safe to wire straight to a click on a stage token. A single-target skill commits on the pick itself; a multi-target skill accumulates picks until `ConfirmTargets` is called.
    - `combatantId` &mdash; The combatant the player pointed at.

`public void SetCombatantPortrait(StableId combatantId, Sprite portrait)`

:   Supplies the portrait a combatant's rail chip crops its face from.
    - `combatantId` &mdash; Combatant the art belongs to.
    - `portrait` &mdash; The sprite to crop, or null to drop one already supplied. The interface never loads art itself, so a combatant with no portrait draws a chip with a plain surface instead.

`public void SetCombatantPortrait(StableId combatantId, Sprite portrait, FormationFacing sourceFacing)`

:   Supplies a portrait and its source-art direction. The UI derives the displayed
    direction from the combatant's current team row, then mirrors only when it differs from
    `sourceFacing`.
    - `combatantId` &mdash; Combatant the art belongs to.
    - `portrait` &mdash; The sprite to crop, or null to drop one already supplied.
    - `sourceFacing` &mdash; Direction encoded by the unmirrored source sprite.

`public void SetCombatantPortrait(StableId combatantId, Sprite portrait, FormationFacing sourceFacing, FormationFacing desiredFacing)`

:   Supplies a portrait with both directions explicit. Use this overload when a UI-only host needs
    a destination independent of its current team row. The portrait is mirrored only when the two
    values differ; `Left` to `Left` is intentionally unmirrored. Portrait crop and framing remain
    independent of token ground points, HUD elements and world-effect anchors.
    - `combatantId` &mdash; Combatant the art belongs to.
    - `portrait` &mdash; The sprite to crop, or null to drop one already supplied.
    - `sourceFacing` &mdash; Direction encoded by the unmirrored source sprite.
    - `desiredFacing` &mdash; Direction the portrait should face in the rail.

`public void SetPlayerTeam(StableId teamId)`

:   Names the team the rail and the health bars should read as "ours". Presentation only: it selects team colors and refreshes portraits whose destination is derived from the team row; explicit portrait destinations remain fixed.
    - `teamId` &mdash; The player's team. The default id makes every combatant read as an opponent, which is the honest answer when no perspective was supplied.

`public void SetTargetCandidates(StableId skillId, IReadOnlyList<StableId> candidates)`

:   Supplies the combatants one offered skill may legally hit. The driver reads these from the skill's registered target resolver - the same object the engine consults - and hands them in, which is what keeps the picker from offering a target the engine would then refuse. A skill nothing was supplied for is picked for by the driver exactly as it was before the picker existed.
    - `skillId` &mdash; The offered skill the list belongs to.
    - `candidates` &mdash; Legal picks in display order; null or empty leaves target resolution to the driver.

`public void SetTooltip(TooltipData tooltip)`

:   Updates set tooltip on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `tooltip` &mdash; Already-computed tooltip text. Ignored unless its skill id is valid, and it replaces any tooltip previously stored for that skill.

`public void ShowDecision(DecisionOptions options)`

:   Offers exactly the legal command shapes the snapshot exposes.
    - `options` &mdash; The shapes to offer; null withdraws the offer, as `ClearDecision` does.

`public void ShowResult(BattleResultState result, DisplayStringTable labels)`

:   Surfaces a terminal result verbatim (all five kinds).
    - `result` &mdash; The result to show. Null, not yet terminal, or carrying no result id all hide the banner instead, so this may be called every frame.
    - `labels` &mdash; Display names for the result and winning team ids. Uncovered ids, and all ids when this is null, are shown as raw id text.

`public void Tick(float presentationDeltaSeconds)`

:   Advances interface animation by a visual delta. The driver forwards its presentation delta here so pause and speed apply to the HUD exactly as they do to the stage.
    - `presentationDeltaSeconds` &mdash; Presentation seconds since the last call. Zero or negative is ignored, which is how a paused presentation freezes the HUD.

`public bool TryGetTooltip(StableId skillId, out TooltipData tooltip)`

:   Returns the tooltip previously supplied for a skill.
    - `tooltip` &mdash; The stored tooltip, or the default value when none was supplied.
    - `skillId` &mdash; Skill identity previously supplied to `SetTooltip`.
    - **Returns** &mdash; True when `SetTooltip` has stored data for this skill.

`public void UpdateStatus(BattleSnapshot snapshot, DisplayStringTable labels)`

:   Rebuilds the status panel from the snapshot.
    - `snapshot` &mdash; Source of health, shields, and status counts; null empties the panel. It is only read, never advanced.
    - `labels` &mdash; Display names for the rows. Null keeps the table from an earlier call, so labels never have to be resupplied.

`public void UpdateTimeline(FrozenList<DecisionEntry> decisions)`

:   Mirrors the currently-ready decision entries as the timeline.
    - `decisions` &mdash; Ready entries to mirror, kept in the order supplied; null or empty clears the strip. Only each entry's actor is read.

`public void UpdateTimeline(IReadOnlyList<StableId> order)`

:   Mirrors a full turn order onto the rail, soonest first.
    - `order` &mdash; Actors in the order they will act. Null or empty clears the rail. The order is drawn exactly as given: the interface neither sorts it nor asks a scheduler anything.

---

## DecisionOptions

```csharp
public sealed class DecisionOptions
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/DecisionShape.cs</small>

The complete set of legal command shapes for one pending decision:
filtered granted skills plus whether concession is offered. This is a
display projection, never a submission.

**Constructors**

`public DecisionOptions()`

:   Creates an option set. A null skill list becomes an empty one, so a caller never has to null-check `Skills`.
    - `hasActor` &mdash; False for the "nothing to decide" set; see `None`.
    - `canConcede` &mdash; Whether a concede command may be offered alongside the skills.
    - `actorId` &mdash; Pending actor, or the default ID when absent.
    - `skills` &mdash; Legal skills; null becomes an empty list.

**Properties**

`public StableId ActorId`

:   The combatant every entry in `Skills` belongs to, and the one whose command the engine will serve next.

`public bool CanConcede`

:   Whether a concede command may be offered alongside the skills. It reports only that the compiled content registers the concede command at all, so it does not vary from actor to actor within a battle.

`public bool HasActor`

:   Whether a decision is actually pending. It is the flag to test before reading `ActorId`, which carries the default ID in the empty set rather than any meaningful combatant.

`public static DecisionOptions None`

:   The empty set - no actor, no concession, no skills. Returned whenever there is nothing for a player to decide.

`public IReadOnlyList<SkillCommandShape> Skills`

:   The skills the actor may use at this moment, ordered by skill ID so a given decision always lays out the same way. Never null. A granted skill that is on cooldown, unaffordable, or restricted by a status is absent altogether rather than present and marked unusable, so a tray that draws greyed-out entries has to keep its own list of what the actor was granted.

---

## DecisionShapeCompiler

```csharp
public static class DecisionShapeCompiler
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/DecisionShape.cs</small>

Pure compiler of legal command shapes from a snapshot and compiled
catalog. It offers a granted skill only when the snapshot-visible
cooldowns, resource costs, and restriction tags allow it, and it reads
the target shape from the compiled target contract. It performs no exact
re-resolution and calls no engine mutator or preview API.

**Methods**

`public static DecisionOptions Compile()`

:   Builds the option set for the decision at the head of the snapshot's queue. Only that first entry is considered, and only when it is human-controlled, because it is the one the engine serves next. A granted skill is offered only when the snapshot shows no live cooldown for it, every resource cost is affordable from the actor's current pools, no status on the actor restricts one of the skill's tags, and its target resolver is registered. Concession is offered when the compiled content registers the concede command at all.
    - `snapshot` &mdash; State to read; nothing in it is mutated.
    - `catalog` &mdash; Compiled content the granted skills and target contracts are read from.
    - **Returns** &mdash; `DecisionOptions.None` for a null argument, an empty or non-human decision queue, a missing or dead actor, or a combatant definition the catalog does not contain; otherwise the legal shapes, ordered by skill id so the same decision always lays out the same way.

---

## DisplayStringTable

:material-star: **Start here**

```csharp
public sealed class DisplayStringTable
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/DisplayStringTable.cs</small>

A non-authoritative map from stable id to display text. Compiled
snapshots carry no labels (they are excluded from B3 compilation and
hashes), so the driver supplies this table from authoring
`DisplayLabel` metadata or a shipped serialized string table. The
table never enters any hash and never affects a simulation output.

**Constructors**

`public DisplayStringTable(IEnumerable<KeyValuePair<StableId, string>> pairs = null)`

:   Copies the supplied labels into a table. The pairs are read once here, so the table does not observe later changes to the source.
    - `pairs` &mdash; Id-to-label pairs; entries with an invalid id or a null label are dropped, and a repeated id keeps the last label. Null builds an empty table.

**Properties**

`public int Count`

:   How many ids carry a label. Pairs the constructor dropped as invalid, and repeats collapsed onto one id, are not counted, so a total below the number of pairs supplied is how those losses show up.

`public static DisplayStringTable Empty`

:   An empty table; every lookup falls back to the raw id.

**Methods**

`public string GetOrId(StableId id)`

:   Returns the label for an id, or the raw id text as a fallback.
    - `id` &mdash; Content identity to resolve, with its canonical text serving as the fallback.
    - **Returns** &mdash; The mapped non-empty label, or the raw stable-ID text when no label is available.

`public bool TryGet(StableId id, out string text)`

:   Looks up the label for an id without falling back to it.
    - `text` &mdash; The label, or null when the id is invalid or unlabelled.
    - `id` &mdash; Valid content identity whose localized or authored label is requested.
    - **Returns** &mdash; True when a label was found.

---

## DisplayStringTableProvider

```csharp
public abstract class DisplayStringTableProvider : ScriptableObject
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/DisplayStringTableProvider.cs</small>

Serialized, project-owned source of non-authoritative display labels.
Runtime hosts request a fresh immutable table when a battle is bound;
labels never enter simulation state, hashes, checkpoints, or replays.

**Methods**

`public abstract DisplayStringTable Build()`

:   Derives build from the supplied immutable context. Missing or illegal inputs produce the contract's typed empty/failure result.
    - **Returns** &mdash; An immutable ID-to-label table assembled from this provider's serialized source.

---

## FeedbackLogView

```csharp
public sealed class FeedbackLogView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/FeedbackLogView.cs</small>

The rolling battle log. It shows the most recent lines newest-last and
fades older entries so the newest line reads first.

The owning `BattleUiRoot` keeps the authoritative bounded line
list; this view only draws a window onto its tail, so the 512-line cap is
enforced in exactly one place.

**Fields**

`public const int VisibleLines`

:   Lines drawn at once. The log itself retains far more.

**Methods**

`public void Apply(IReadOnlyList<string> allLines)`

:   Draws the tail of `allLines`. The newest line is fully opaque and older ones fade toward the muted role.
    - `allLines` &mdash; The whole log, oldest first; only the last `VisibleLines` entries are drawn. Null or empty clears every row.

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the panel. Explicit so EditMode tests can drive it. A second call stores the new skin but does not restyle widgets already built.
    - `battleSkin` &mdash; Skin to draw with; null falls back to the shipped default.

---

## ResultBannerView

```csharp
public sealed class ResultBannerView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/ResultBannerView.cs</small>

The terminal result banner. It surfaces all five terminal kinds (victory,
defeat, draw, concession, and the stalled result) and tints itself by
outcome so the end state reads instantly.

It displays the result it is handed and decides nothing about the outcome.

**Properties**

`public bool IsShown`

:   True while the banner is displayed.

**Methods**

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the banner. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin to draw with; null falls back to the shipped default.

`public void Hide()`

:   Hides the banner.

`public void Show(StableId resultId, string headlineText, string detailText)`

:   Shows a terminal result. `headlineText` and `detailText` are already-localized display strings.
    - `resultId` &mdash; Terminal result id. It only picks the tint; an id the package does not ship still displays, in the neutral accent.
    - `detailText` &mdash; Second line; when null or empty the line is hidden rather than left blank.
    - `headlineText` &mdash; Primary result line, such as Victory or Defeat; null displays an empty headline.

`public void Tick(float deltaSeconds)`

:   Advances the fade-in by a visual delta.
    - `deltaSeconds` &mdash; Positive visual-frame duration consumed by the remaining fade time.

---

## SafeAreaFitter

```csharp
public sealed class SafeAreaFitter : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/SafeAreaFitter.cs</small>

Insets a `RectTransform` to the device safe area so HUD
regions never land under a notch, a punch-hole camera, or a home
indicator. It re-applies only when the screen or safe area actually
changes, so it costs nothing on desktop.

The whole HUD sits inside one of these, which means every skin region is
automatically safe-area correct without the buyer positioning anything
twice.

**Properties**

`public Rect AppliedNormalizedArea`

:   The normalized safe area currently applied.

**Methods**

`public bool Apply(int screenWidth, int screenHeight, Rect safeAreaPixels)`

:   Applies a safe area explicitly. Public and parameterised so EditMode tests can verify inset maths without a device.
    - `safeAreaPixels` &mdash; Device-safe rectangle expressed in bottom-left-origin screen pixels.
    - `screenHeight` &mdash; Full render-target height in pixels.
    - `screenWidth` &mdash; Full render-target width in pixels.
    - **Returns** &mdash; after valid normalized anchors are applied; otherwise for zero screen dimensions or an empty area.

---

## SkillCommandShape

```csharp
public sealed class SkillCommandShape
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/DecisionShape.cs</small>

One legal skill command shape offered to the pending actor.

**Constructors**

`public SkillCommandShape(StableId skillId, TargetShape target)`

:   Pairs a skill with the target shape its resolver declares.
    - `skillId` &mdash; Valid compiled skill identity represented by this command option.
    - `target` &mdash; Targeting rule the skill resolver requires before command submission.

**Properties**

`public StableId SkillId`

:   The skill this shape stands for, and the ID to carry in the command once the player commits to it.

`public TargetShape Target`

:   What this skill's resolver will accept: how many target IDs the command may carry and which combatants qualify. Read it to decide how many picks to collect before the command is submittable.

---

## SkillTitleView

```csharp
public sealed class SkillTitleView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/SkillTitleView.cs</small>

The skill title card: the name of what is being performed, announced as it
happens and gone again a moment later.

It draws with the same surface and typography tokens as every other region,
so it inherits whichever skin is applied without any per-skin work. Like the
result banner, it displays what it is handed and decides nothing.

**Properties**

`public float Alpha`

:   Current alpha, which is what a test can assert the fade against.

`public string CurrentTitle`

:   The text currently displayed, empty when the card is resting.

`public bool IsShown`

:   True while the card is on screen, fading counted as shown.

**Methods**

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the card. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin to draw with; null falls back to the shipped default.

`public void Hide()`

:   Takes the card down immediately.

`public void Show(string displayName, float holdSeconds, float fadeInOutSeconds)`

:   Announces a skill. Calling it again while a card is up replaces it and restarts the hold, so a fast chain of skills reads as the latest one rather than queueing cards the player will never see.
    - `displayName` &mdash; Already-localized skill name; empty hides the card.
    - `holdSeconds` &mdash; Total seconds on screen, fades included. Zero or less hides the card.
    - `fadeInOutSeconds` &mdash; Fade time at each end, clamped to half the hold.

`public void Tick(float deltaSeconds)`

:   Advances the fade and the hold on the presentation clock, so pause and speed reach the card the same way they reach everything else.
    - `deltaSeconds` &mdash; Elapsed presentation seconds; zero or less does nothing.

---

## SkillTrayView

```csharp
public sealed class SkillTrayView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/SkillTrayView.cs</small>

The command tray offered to a pending human actor: one button per legal
skill shape plus concede.

It raises plain C# events carrying the player's choice and submits
nothing. Target resolution, legality, and submission all stay with the
driver and the engine, which is what keeps the presenter-purity contract
intact while still giving the player something clickable.

**Properties**

`public int VisibleButtonCount`

:   Buttons currently visible.

**Fields**

`public SkinSurfaceGraphic Background`

:   The skinned surface behind the button. It is reskinned in place to show selection rather than swapped for another graphic.

`public Button Button`

:   The clickable component. Its listener is wired once when the entry is created and reads `SkillId` at click time, so rebinding the entry to another skill needs no rewiring.

`public TMP_Text Caption`

:   The short target description in the card's footer, such as "ONE ENEMY".

`public const float CardHeight`

:   Height of one skill card in reference pixels. The command deck is 280 tall, a 46-pixel log strip caps it, and the actor prompt takes a line above the cards, which is what leaves 196 rather than the 216 a card would take if it had the band to itself.

`public const float CardIconSize`

:   Edge of the icon plate in a card's top-left corner.

`public const float CardWidth`

:   Width of one skill card in reference pixels.

`public const float ConcedeCardWidth`

:   Width of the narrower concede card in reference pixels.

`public TMP_Text Cost`

:   The cost in the card's top-right corner. Always in the same place, so a player learns to look there once rather than reading each card.

`public LayoutElement Element`

:   The card's layout element, kept so the tray can re-measure the card against how many are being offered rather than pinning every deck to one fixed width.

`public GameObject Host`

:   The button's root object. Entries are pooled rather than destroyed, so this is deactivated when the tray offers fewer skills than it has already built.

`public SkinSurfaceGraphic Icon`

:   The icon plate in the card's top-left corner. It is recoloured per card rather than carrying art, so the deck ships no icon set and a project can drop its own sprite in without a layout change.

`public const int MaximumButtons`

:   Buttons drawn before the tray stops adding more.

`public const float MaximumCardWidth`

:   Widest a single card is allowed to grow when few skills are offered, in reference pixels. Without a ceiling a one-skill decision would hand the whole deck to one button.

`public TMP_Text Name`

:   The skill's display name, resolved through the display-string table and falling back to the raw ID text.

`public StableId SkillId`

:   The skill this entry currently stands for. It changes as the tray is reapplied, which is why the click and focus handlers read it rather than capturing it.

**Events**

`public event Action ConcedeChosen`

:   Raised when the player concedes. Never submitted here.

`public event Action<StableId> SkillChosen`

:   Raised when the player picks a skill. Never submitted here.

`public event Action SkillFocusCleared`

:   Raised when the pointer leaves every skill button.

`public event Action<StableId> SkillFocused`

:   Raised when the pointer enters a skill button.

**Methods**

`public void Apply(DecisionOptions options, DisplayStringTable labels)`

:   Offers exactly the shapes in `options`. An empty or non-human decision hides the tray entirely. Does nothing before `Build` has run, and never offers more than `MaximumButtons` skills however many are legal.
    - `labels` &mdash; Display names for the actor and skill ids; null, or an id the table does not carry, falls back to the raw id text.
    - `options` &mdash; Current actor's legal skill and target shapes used to populate the tray.

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the tray. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin every widget in the tray is drawn from; null falls back to `BattleSkinDefaults.Default`. Only the first call builds the widget tree - a later call stores the skin and returns.

`public void ClearSelection()`

:   Clears every button highlight.

`public void SetSelected(StableId skillId)`

:   Highlights the button for `skillId`.
    - `skillId` &mdash; Skill identity whose pooled button receives the selected visual state.

---

## SkinnedTokenPlate

```csharp
public sealed class SkinnedTokenPlate : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Widgets/SkinnedTokenPlate.cs</small>

The floating plate above one combatant: name, health, shield, cast
progress, scheduler gauge, and status pips.

It lives on a world-space canvas parented to the token, so it tracks the
token with no per-frame screen projection and works with any camera setup
the buyer already has. Everything it draws comes from values handed to it;
it reads no simulation state and computes nothing authoritative.

**Properties**

`public bool HasWorldTopOverride`

:   True when a caller has supplied a world-space top edge.

`public bool IsBuilt`

:   True once `Build` has run.

`public int VisiblePipCount`

:   Status pips currently visible.

**Fields**

`public const float CriticalHealthFraction`

:   Health fraction below which a combatant reads as in danger. The bar does not change colour there, because colour already means which side you are on. Instead its border lights and its fill pulses, which is a second channel rather than an overloaded one.

`public const int DefaultSortingOrder`

:   Builds the plate. Explicit so EditMode tests can construct one with no scene and no camera.
    - `battleSkin` &mdash; Skin the plate is dressed from; null falls back to the package default.
    - `unitsPerPixel` &mdash; World units one reference pixel is worth. It scales the whole plate, so `PlateWidth` only means 132 world units at a value of one.
    - `verticalOffsetPixels` &mdash; Height above the token in reference pixels. It is scaled by `unitsPerPixel` too, so the plate keeps its distance as the plate is resized.

`public const float PlateWidth`

:   Plate width in reference pixels.

**Methods**

`public void ApplyState()`

:   Mirrors health, shield, and status counts onto the plate. Does nothing until `Build` has run.
    - `health` &mdash; Current health, used only to derive the bar's fraction.
    - `maximumHealth` &mdash; Denominator for both the health and shield bars. Zero or less empties the health bar and hides the shield, since neither has a scale to be drawn against.
    - `shieldAmount` &mdash; Absorb remaining, drawn as a share of `maximumHealth` and clamped there. Zero hides the shield bar.
    - `statusCount` &mdash; Total statuses on the combatant, not the number of pips to draw. Anything beyond the skin's visible limit collapses into a single overflow pip.
    - `isDead` &mdash; Draws the health bar empty and mutes the name regardless of `health`.

`public void Build(CompiledBattleSkin battleSkin, float unitsPerPixel, float verticalOffsetPixels)`

:   Creates the plate's world-space canvas, backing, labels and bars once. Later calls retain the existing hierarchy and replace only the stored skin reference.
    - `battleSkin` &mdash; Skin used for initial typography and styling, or null for the default skin.
    - `unitsPerPixel` &mdash; Local world-space scale applied to each canvas pixel during the first build.
    - `verticalOffsetPixels` &mdash; Initial vertical offset from the parent origin, in canvas pixels scaled by unitsPerPixel.

`public void ClearWorldTopOverride()`

:   Restores the last ground-relative placement after a world-top override.

`public void Pulse(Transform target)`

:   Starts a scale pulse that always returns to rest. The previous implementation set a scale and never restored it, so tokens grew permanently every time they acted.
    - `target` &mdash; Transform to scale, normally the token root; null pulses this plate's own transform. A zero motion scale in the skin restores rest scale at once instead of animating.

`public void SetCast(float fraction, bool visible)`

:   Shows cast progress in [0,1], or hides the bar.
    - `fraction` &mdash; Normalized cast completion forwarded to the cast bar when visible.
    - `visible` &mdash; Whether the cast-progress row participates in layout.

`public void SetGauge(float fraction, bool visible)`

:   Shows the scheduler gauge in [0,1], or hides it.
    - `fraction` &mdash; Normalized scheduler readiness forwarded to the gauge bar.
    - `visible` &mdash; Whether the scheduler gauge participates in layout.

`public void SetGroundPlacement()`

:   Moves the plate to a combatant's ground line and sizes it to their art. A nameplate pinned to a fixed offset above the token origin worked only while every combatant was the same 84-pixel square. Once they are painted illustrations of different heights, the plate has to follow the body it belongs to or it ends up across somebody's chest.
    - `widthPixels` &mdash; Width to draw at, in reference pixels. It is widened to 1.4 times the art so the name has room beside the readout, and floored at `PlateWidth` so a narrow combatant still gets a legible plate. Zero or less keeps the current width.
    - `groundLinePixels` &mdash; Where the combatant's feet are, relative to the token origin, in reference pixels. Art pivoted at its feet reports zero here.
    - `overlapPixels` &mdash; How far the plate's top edge rises above that ground line. A small positive value tucks the plate under the body it belongs to.
    - `unitsPerPixel` &mdash; World units one reference pixel is worth.

`public void SetGroundPlacement()`

:   Places the plate using the visual ground line and its horizontal centre, both relative to the token root. The four-argument overload remains the compatibility path for callers that use the token origin.
    - `widthPixels` &mdash; Width to draw in reference pixels; zero keeps the current width.
    - `groundLinePixels` &mdash; Visual ground line relative to the token origin.
    - `overlapPixels` &mdash; How far the plate rises over the visual ground line.
    - `unitsPerPixel` &mdash; World units per reference pixel.
    - `centreXPixels` &mdash; Visual ground centre relative to the token origin.

`public void SetLabel(string text)`

:   Updates set label on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `text` &mdash; Combatant display name written to the plate; null becomes empty.

`public void SetSelectionHighlight(bool actor, bool target)`

:   Highlights this plate for actor or target selection without changing its authored type scale.

`public void SetSortingOrder(int order)`

:   Puts this plate on a specific order, still above the bodies.
    - `order` &mdash; Canvas sorting order to draw the plate at.

`public void SetTeamTint(Color tint)`

:   Tints the plate for a team. Keeps ally and enemy readable at a glance without requiring per-combatant art.
    - `tint` &mdash; Colour applied to the combatant's name label; the bars keep the colours the skin gave them.

`public void SetWorldTopOverride(Vector3? worldTop)`

:   Pins the plate's top edge to a world-space point. The authored canvas size and typography remain unchanged; only the plate position moves. Pass `null` to restore the normal ground-relative placement.
    - `worldTop` &mdash; World-space position of the plate top edge, or null to cancel the override.

`public void SetWorldTopOverride(Vector3? worldTop, float unitsPerPixel, float widthPixels)`

:   Sets a world-top override while cancelling token scale for authored plate sizing.
    - `worldTop` &mdash; World-space top edge, or null to restore ground placement.
    - `unitsPerPixel` &mdash; World units per authored pixel. Parent scaling is cancelled on both axes.
    - `widthPixels` &mdash; Optional authored width; zero preserves the current width.

`public void StopPulse()`

:   Cancels this plate's neutral pulse and restores its resting scale.

`public void Tick(float deltaSeconds)`

:   Advances plate animation. Driven by the presenter's visual clock so pause and speed apply, and so tests can step it deterministically.
    - `deltaSeconds` &mdash; Positive presentation-clock duration applied to all bars and the impact pulse.

---

## SkinnedValueBar

```csharp
public sealed class SkinnedValueBar : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Widgets/SkinnedValueBar.cs</small>

A skinned value bar: track, an optional trailing ghost showing the value
just lost, the live fill, and an optional numeric readout.

The bar animates toward its target rather than snapping, which is what
makes a hit legible at a glance. All motion is presentation-only and
derives from the skin, so `Reduce Motion` or a zero
`Motion Scale` makes every change instant without touching this code.

**Properties**

`public float DisplayedFraction`

:   The fraction currently drawn, in [0,1].

`public bool IsAnimating`

:   True while the fill is still moving toward its target.

`public TMP_Text Readout`

:   The numeric readout, or null when the bar was built without one.

`public float TargetFraction`

:   The fraction the bar is animating toward, in [0,1].

**Methods**

`public void Build(CompiledBattleSkin skin, SkinBarTokens barTokens, bool withReadout)`

:   Builds the bar's children. Explicit rather than done in Awake so EditMode tests can construct and drive a bar with no scene.
    - `barTokens` &mdash; Fill, ghost, track, border, glow, and animation tokens for this bar role.
    - `skin` &mdash; Compiled surface, typography, and motion tokens shared by the widget hierarchy.
    - `withReadout` &mdash; Whether to create centered numeric text over the fill.

`public void SetFillAlpha(float alpha)`

:   Fades the fill without changing its colour, which is what lets a critical bar breathe while still reading as its team's colour.
    - `alpha` &mdash; Opacity in zero to one applied to the fill graphic only.

`public void SetFillColor(Color primary)`

:   Replaces the fill colour, keeping shape, glow, and geometry.
    - `primary` &mdash; Replacement primary and secondary fill color.

`public void SetFraction(float fraction)`

:   Animates toward `fraction`. A decrease leaves a ghost at the previous value that catches up shortly after, so the player can see how much was just taken.
    - `fraction` &mdash; Target fill in normalized units; values outside zero to one are clamped.

`public void SetFractionImmediate(float fraction)`

:   Snaps to `fraction` with no animation.
    - `fraction` &mdash; Immediate fill and ghost value, clamped to zero through one.

`public void SetReadout(string text)`

:   Sets the numeric readout text, if the bar has one.
    - `text` &mdash; Numeric or status text to display; null becomes empty.

`public void SetTrackStrokeColor(Color stroke)`

:   Replaces the track's border colour, keeping every other value. This is the channel a bar uses to say "in danger" without touching its fill, which already means something else: on a team-coloured health bar the fill says whose side you are on, so the warning has to arrive somewhere other than the fill.
    - `stroke` &mdash; Replacement border colour for the bar's track.

`public void Tick(float deltaSeconds)`

:   Advances the bar's animation. Driven by the presenter's visual clock rather than `Update` so pause and speed apply consistently and so tests can step it deterministically.
    - `deltaSeconds` &mdash; Positive presentation-clock duration applied to fill and delayed ghost transitions.

---

## SkinnedWidgetFactory

```csharp
public static class SkinnedWidgetFactory
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Widgets/SkinnedWidgetFactory.cs</small>

Builds the skinned uGUI primitives the HUD is assembled from. Centralising
construction here is what lets the whole interface restyle from a
`CompiledBattleSkin`: no widget hardcodes a colour, a size, or
a font, and nothing depends on a shipped prefab.

**Methods**

`public static HorizontalLayoutGroup AddHorizontalLayout()`

:   Adds a horizontal layout group with skin-consistent spacing.
    - `alignment` &mdash; Placement of the non-expanding child row within available space.
    - `padding` &mdash; Left, right, top, and bottom content inset assigned to the group.
    - `rect` &mdash; Rect receiving the new HorizontalLayoutGroup component.
    - `spacing` &mdash; Reference-pixel gap between consecutive children.
    - **Returns** &mdash; A non-expanding horizontal layout group using the requested alignment.

`public static ContentSizeFitter AddVerticalFitter(RectTransform rect)`

:   Adds a content-size fitter so a region can size to content. A fitter measures `ILayoutElement` components on its OWN object, so `rect` must already carry the layout group whose content it should follow. On a rect with no layout group the preferred height resolves to zero and the region collapses.
    - `rect` &mdash; Rect already carrying the layout elements whose preferred height should drive it.
    - **Returns** &mdash; A new ContentSizeFitter constrained only to vertical preferred size.

`public static VerticalLayoutGroup AddVerticalLayout()`

:   Adds a vertical layout group with skin-consistent spacing.
    - `padding` &mdash; Left, right, top, and bottom content inset assigned to the group.
    - `rect` &mdash; Rect receiving the new VerticalLayoutGroup component.
    - `spacing` &mdash; Reference-pixel gap between consecutive children.
    - **Returns** &mdash; A width-expanding, content-height vertical group aligned to the upper left.

`public static void ApplyRegion(RectTransform rect, SkinRegionTokens region)`

:   Anchors a rect inside its parent according to a skin region, so a customer can move any HUD block by editing the preset alone.
    - `rect` &mdash; HUD region whose anchors, pivot, position, optional size, and scale are updated.
    - `region` &mdash; Compiled safe-area anchor, inward offset, size, stretch, and visibility-independent scale.

`public static TMP_Text CreateLabel()`

:   Creates a label using the skin's typography.
    - `alignment` &mdash; Horizontal and vertical text placement within the label rect.
    - `color` &mdash; Initial text color.
    - `fontSize` &mdash; Font size in reference pixels.
    - `name` &mdash; Unity hierarchy name assigned to the label GameObject.
    - `parent` &mdash; Transform that receives the new label child.
    - `skin` &mdash; Compiled font, line spacing, and optional outline settings.
    - **Returns** &mdash; A non-raycast, rich-text-disabled uGUI Text configured from the skin.

`public static RectTransform CreateRect(string name, Transform parent)`

:   Creates a child object with a `RectTransform`.
    - `name` &mdash; Unity hierarchy name assigned to the new child GameObject.
    - `parent` &mdash; Transform that owns the new rect while preserving local coordinates.
    - **Returns** &mdash; The RectTransform of a new child GameObject.

`public static SkinSurfaceGraphic CreateSurface()`

:   Creates the create surface asset/value from this template's explicit settings. The caller owns persistence and must supply any requested stable ID.
    - `name` &mdash; Unity hierarchy name assigned to the surface GameObject.
    - `parent` &mdash; Transform that receives the new non-raycast surface child.
    - `tokens` &mdash; Shape, fill, stroke, glow, and shadow settings applied immediately.
    - **Returns** &mdash; A new drawable surface with RectTransform, CanvasRenderer, and SkinSurfaceGraphic.

`public static void Fill(RectTransform rect, float inset = 0f)`

:   Stretches a rect to fill its parent with an optional uniform inset.
    - `inset` &mdash; Uniform inward offset in reference pixels; zero reaches every parent edge.
    - `rect` &mdash; Child rect whose anchors and offsets are rewritten to stretch.

`public static LayoutElement IgnoreLayout(RectTransform rect)`

:   Excludes `rect` from its parent's layout group, keeping the anchors it was given. Used for panel backgrounds that must stretch across a region whose children are otherwise laid out in a row or column.
    - `rect` &mdash; Background or overlay rect to exempt from its parent's layout calculation.
    - **Returns** &mdash; A new LayoutElement with `ignoreLayout` enabled.

---

## StatusRosterView

```csharp
public sealed class StatusRosterView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/StatusRosterView.cs</small>

The combatant roster: one row per combatant with name, health bar, shield
readout, and status count. Rows are pooled and reused, so a long battle
allocates nothing per update.

It mirrors supplied `UiStatusEntry` values verbatim and reads
no simulation state.

**Properties**

`public int VisibleRowCount`

:   Rows currently visible.

**Fields**

`public SkinSurfaceGraphic Background`

:   The plate drawn behind the row. Hidden while the combatant is down, so a dead row reads as an empty slot rather than a live one.

`public TMP_Text Detail`

:   The caption line to the right of the name, carrying shield and status counts, or `Down` alone once the combatant is dead.

`public SkinnedValueBar Health`

:   The health bar. It eases towards its new fraction rather than snapping, so `Tick` has to be called for the movement to be seen.

`public GameObject Host`

:   The row object itself. It is deactivated rather than destroyed when the roster shrinks, which is how the pool avoids reallocating.

`public const int MaximumRows`

:   Rows drawn before the rest collapse into a count on the last one. The roster docks into a fixed cell of the command deck, and the stage above it is protected, so it has a real ceiling rather than a preference. Past this many combatants the last row reports how many are not shown, which is more honest than a list that quietly runs off the top of its own panel.

`public TMP_Text Name`

:   The combatant label. Falls back to the raw id when the display string table has no name, and is drawn muted once the combatant is down.

**Methods**

`public void Apply(IReadOnlyList<UiStatusEntry> entries, DisplayStringTable labels)`

:   Rebuilds the roster from supplied entries, one row per entry in the order given. Rows are added as the roster grows and hidden, not destroyed, as it shrinks.
    - `entries` &mdash; Rows to draw; null or empty hides every row.
    - `labels` &mdash; Name source; null falls back to `DisplayStringTable.Empty`, which shows raw ids.

`public void Apply()`

:   Rebuilds the roster, colouring each health bar by whether the combatant is on `allyTeamId`.
    - `entries` &mdash; Rows to draw; null or empty hides every row.
    - `labels` &mdash; Name source; null falls back to `DisplayStringTable.Empty`, which shows raw ids.
    - `allyTeamId` &mdash; The team drawn as ours. The default id makes every row read as an opponent, which is the honest answer when no perspective was supplied.

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the panel. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin to draw with; null falls back to the shipped default.

`public void Tick(float deltaSeconds)`

:   Advances row bar animation by a visual delta.
    - `deltaSeconds` &mdash; Non-negative visual-frame duration used to advance every pooled value bar.

---

## TargetPickerView

```csharp
public sealed class TargetPickerView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/TargetPickerView.cs</small>

The target picker: one button per combatant the chosen skill may legally
hit, plus confirm and back.

It is the second half of choosing an action, and it is deliberately built
the same way as the skill tray - pooled buttons, skinned surfaces, plain
C# events - so a project restyles or replaces it exactly as it does the
tray. It decides nothing: the candidate list is handed to it, and pressing
a button raises an event for the interface to act on.

**Properties**

`public int VisibleButtonCount`

:   Candidate buttons currently visible.

**Fields**

`public SkinSurfaceGraphic Background`

:   The skinned surface behind the button, reskinned in place to show which candidates are currently picked.

`public TMP_Text Caption`

:   The health readout under the name.

`public StableId CombatantId`

:   The combatant this entry currently stands for. The click handler reads it rather than capturing it, so rebinding needs no rewiring.

`public GameObject Host`

:   The button's root object, pooled rather than destroyed so a battle with a changing candidate count does not churn objects.

`public const int MaximumButtons`

:   Legacy compatibility constant. The picker no longer truncates its candidates; every supplied candidate is placed in the scrolling row.

`public TMP_Text Name`

:   The candidate's display name.

**Events**

`public event Action Cancelled`

:   Raised when the player backs out to the skill tray.

`public event Action Confirmed`

:   Raised when the player commits the picks made so far.

`public event Action<StableId> TargetChosen`

:   Raised when the player presses one candidate. Never submitted here.

**Methods**

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the picker. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin every widget is drawn from; null falls back to `BattleSkinDefaults.Default`. Only the first call builds the widget tree - a later call stores the skin and returns.

`public void Hide()`

:   Takes the picker down.

`public void SetCandidatesVisible(bool visible)`

:   Shows or hides the candidate buttons while leaving the prompt up. The Direct preset picks on the stage, so the row would be a second way to do the same thing taking up the deck. The prompt still has to be there: it is the part that tells the player where to point.
    - `visible` &mdash; Whether the row of candidate buttons is drawn.

`public void SetPicked(IReadOnlyList<StableId> picked)`

:   Highlights exactly the candidates in `picked`.
    - `picked` &mdash; The ids picked so far; null or empty clears every highlight.

`public void Show()`

:   Offers exactly the candidates it is handed.
    - `prompt` &mdash; The line above the buttons, such as "Fireball: choose 1 enemy". Shown verbatim, so it is the caller's job to localize it.
    - `candidates` &mdash; The combatants that may be picked, in the order to draw them. Null or empty hides the picker, because a picker offering nothing is a dead end the player cannot leave.
    - `allowsMultiple` &mdash; True when the skill takes more than one target, which is what puts the Confirm button on screen. A single-target skill commits on the pick itself and needs no confirmation step.
    - `labels` &mdash; Display names for the candidates; null, or an id the table does not carry, falls back to the raw id text.
    - `status` &mdash; Current health rows used for the readout under each name. Null draws the names alone.

`public bool TryGetCandidate(int index, out StableId combatantId)`

:   Reports which combatant one visible button stands for.
    - `index` &mdash; Zero-based position in the drawn row.
    - `combatantId` &mdash; The candidate at that position, or the default id.
    - **Returns** &mdash; True when a visible button exists at that position.

---

## TargetShape

```csharp
public readonly struct TargetShape
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/DecisionShape.cs</small>

The display-only shape of a skill's target request, taken from the
compiled target contract. It describes what the player may pick; it is
never the engine's exact target resolution.

**Constructors**

`public TargetShape()`

:   Creates a shape from an already-resolved target contract. It copies the declared limits as given and validates nothing.
    - `relation` &mdash; Allowed team relation to the actor.
    - `lifeState` &mdash; Allowed living/dead state.
    - `minimumTargets` &mdash; Fewest ids a command must carry.
    - `maximumTargets` &mdash; Most ids a command may carry.
    - `maximumResolvedTargets` &mdash; Most combatants the resolver may finally reach, which can exceed `maximumTargets` when one pick spreads.
    - `actorMayAppear` &mdash; Whether the acting combatant is itself a legal pick.
    - `automaticSelection` &mdash; Whether a command carrying no ids is legal, leaving the pick to the resolver.

`public TargetShape()`

:   Copies target-count limits and pick policy with the resolver identity used for stage previews. Values are retained without validation; this shape neither resolves targets nor authorizes a command.
    - `relation` &mdash; Allowed team relation to the actor.
    - `lifeState` &mdash; Allowed living/dead state.
    - `minimumTargets` &mdash; Fewest ids a command must carry.
    - `maximumTargets` &mdash; Most ids a command may carry.
    - `maximumResolvedTargets` &mdash; Most combatants the resolver may finally reach.
    - `actorMayAppear` &mdash; Whether the acting combatant is itself a legal pick.
    - `automaticSelection` &mdash; Whether a command carrying no ids is legal.
    - `resolverId` &mdash; The target resolver's implementation id. The interface uses it to pick how the affected set should be DRAWN -- a whole-team scrim reads differently from a row band or a single ring -- and for nothing else.

**Properties**

`public bool ActorMayAppear`

:   Whether the acting combatant is itself a legal pick.

`public bool AutomaticSelection`

:   Whether a command carrying no ids is legal, leaving the pick to the resolver.

`public TargetLifeState LifeState`

:   Which life state a pick must be in. Copied from the compiled contract in the same way as `Relation`, and equally not re-derived here.

`public int MaximumResolvedTargets`

:   Most combatants the resolver may finally reach; can exceed `MaximumTargets` when one pick spreads.

`public int MaximumTargets`

:   Most ids a command may carry.

`public int MinimumTargets`

:   Fewest ids a command must carry.

`public TargetTeamRelation Relation`

:   Which combatants the skill may reach, relative to the acting combatant's team. It is the resolver's declared eligibility copied verbatim, so it is sound for shading legal picks but is not the check the engine performs when the command arrives.

`public StableId ResolverId`

:   Which resolver produced this shape, or the default id when the shape was built without one. Presentation-only: it decides how the affected set is drawn and never what is legal.

---

## TimelineStripView

```csharp
public sealed class TimelineStripView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/TimelineStripView.cs</small>

The turn-order rail: one chip per upcoming actor, left to right, with the
actor about to act raised, accented, and marked NOW.

This is the product's namesake and the one element present in every frame
of every encounter, so it is a full-bleed band rather than a strip in a
corner. A chip is a portrait, a team-coloured rim, a health underline, and
up to three status pips: four answers in one glance, which is what makes
the rail something a player plans against instead of something they
occasionally read.

Chips slide to their new positions rather than cutting. A chip that jumps
reads as a bug in the scheduler; a chip that slides reads as the feature
the scheduler is.

**Properties**

`public bool IsShifting`

:   True while chips are still sliding toward a new order.

`public int VisibleChipCount`

:   Chips currently visible.

**Fields**

`public const float ActingChipSize`

:   Edge of the acting chip in reference pixels.

`public SkinSurfaceGraphic Background`

:   The chip plate. Its stroke carries the team colour and its glow marks the actor about to act.

`public const float ChipGap`

:   Gap between chips in reference pixels.

`public const float ChipSize`

:   Edge of a resting chip in reference pixels.

`public const int ComfortableChips`

:   Chips past which the rail shrinks rather than wrapping.

`public const float CrowdedChipSize`

:   Edge of a chip once the rail is crowded, in reference pixels.

`public GameObject DeadCross`

:   The two struck diagonals shown once a combatant is down.

`public const float HeaderGutter`

:   Clearance held on the left of the band for the "TURN ORDER" title, in reference pixels. Named because the header, the chip row and the hairline all have to agree about it, and it used to be written out three times as a literal.

`public SkinSurfaceGraphic Health`

:   The health underline along the chip's bottom edge.

`public GameObject Host`

:   The chip object. Deactivated rather than destroyed when the order shortens, so the strip reuses its chips for the whole battle.

`public TMP_Text Label`

:   The name under the chip. It is drawn for the acting chip only: at 96 pixels a face and a rim identify a combatant faster than a name set small enough to fit under one.

`public const int MaximumChipPips`

:   Status pips drawn on one chip before the rest are dropped.

`public const int MaximumChips`

:   Chips drawn before the strip stops adding more.

`public GameObject NowTag`

:   The NOW tag, shown on the leading chip only.

`public Vector2 Origin`

:   Where the chip started the current slide from.

`public const float OverflowReachPixels`

:   Room the trailing "+n" counter needs past the last chip, in reference pixels.

`public readonly List<SkinSurfaceGraphic> Pips`

:   The status pips riding the chip's top-right corner.

`public Image Portrait`

:   The cropped portrait, hidden when the host supplied no art.

`public RectTransform PortraitFrame`

:   The rect the portrait is cropped inside.

`public RectTransform Rect`

:   The chip's rect, moved directly rather than by a layout group.

`public Vector2 Target`

:   Where the chip is sliding to, in the row's local space.

`public const float TransportGutter`

:   Clearance held on the right of the band for the transport cluster, in reference pixels.

**Methods**

`public void Apply(IReadOnlyList<StableId> actors, DisplayStringTable labels)`

:   Rebuilds the rail from the supplied actor order, with no side, health, or status information. Kept for hosts that only have an order to give.
    - `actors` &mdash; Decision order as the simulation reported it, soonest first: index 0 is the chip raised and marked NOW. Entries past `MaximumChips` collapse into a trailing counter, and null is treated as an empty order.
    - `labels` &mdash; Display names for the actors. A missing entry falls back to the actor's identifier, and null is treated as an empty table.

`public void Apply()`

:   Rebuilds the rail from full chip entries.
    - `entries` &mdash; Decision order, soonest first. Entries past `MaximumChips` collapse into a trailing counter rather than wrapping to a second line; null is an empty order.
    - `labels` &mdash; Display names for the actors; a missing entry falls back to the raw identifier.
    - `portraits` &mdash; Art to crop each chip's face from, keyed by combatant. Null, or a combatant with no entry, draws a chip with no face rather than a placeholder.

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the rail. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin the chips are dressed from; null falls back to the package default.

`public void Tick(float deltaSeconds)`

:   Advances the slide that follows a reorder. Driven by the presenter's visual clock, so pause and speed apply to the rail exactly as they do to the stage, and a reduced-motion skin snaps instead.
    - `deltaSeconds` &mdash; Positive presentation-clock duration. Non-positive values are ignored.

---

## TooltipData

```csharp
public readonly struct TooltipData
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/TooltipData.cs</small>

A passive tooltip value computed by the DRIVER through the public preview
surface (`BattleFormulaService.Preview` /
`PreviewStatusApplication`, `FormulaPreview`, and
`IEffectResolver.Plan`) and handed to the UI verbatim. The UI stores
and displays it; it never invokes a simulation or preview API itself.

**Constructors**

`public TooltipData()`

:   Captures one already-computed tooltip. Null text arguments are stored as empty strings, so a consumer never needs a null check.
    - `hasPreview` &mdash; True when the driver ran a numeric preview. While it is false the shipped tooltip panel hides the amount range and the hit and critical figures, and shows only the status chance.
    - `costText` &mdash; Driver-authored localized cost line; null hides the row.
    - `criticalChance` &mdash; Conditional critical probability for a landed use.
    - `hitChance` &mdash; Probability that the previewed use lands.
    - `previewMaximum` &mdash; Highest amount a landed use can produce.
    - `previewMinimum` &mdash; Lowest amount a landed use can produce.
    - `skillId` &mdash; Skill identity this tooltip must remain associated with.
    - `statusChance` &mdash; Probability that the accompanying status application succeeds.
    - `targetShapeText` &mdash; Driver-authored localized target-rule line; null hides the row.
    - `timingText` &mdash; Driver-authored localized timing line; null hides the row.

**Properties**

`public string CostText`

:   The cost line, worded and localised entirely by the driver. Nothing in the package parses it back, and an empty string hides the row rather than drawing a blank one.

`public Chance64 CriticalChance`

:   Odds of a critical on a use that lands. The shipped panel leaves the figure out altogether when it is impossible instead of printing zero, so a skill that cannot crit costs no tooltip space.

`public bool HasPreview`

:   True when the amount range and hit and critical figures are worth drawing.

`public Chance64 HitChance`

:   Odds that the use lands at all, meaningful only while `HasPreview` is true.

`public Fixed64 PreviewMaximum`

:   Highest amount a use that lands can produce. It equals `PreviewMinimum` when the formula has no spread, which is how a caller can decide to print one figure instead of a range.

`public Fixed64 PreviewMinimum`

:   Lowest amount a use that lands can produce. A miss is reported by `HitChance` rather than by this bound, and the value stands for nothing while `HasPreview` is false.

`public StableId SkillId`

:   The skill this value was computed for, so a tray entry can tell whether the tooltip it holds still belongs to the skill it draws.

`public Chance64 StatusChance`

:   Odds that the accompanying status applies. It comes from a separate preview call from the amount figures, so it can be worth drawing even while `HasPreview` is false - a pure status skill has odds but no amount range.

`public string TargetShapeText`

:   The line describing who the skill may be aimed at, worded by the driver. An empty string hides the row.

`public string TimingText`

:   The timing line, worded by the driver. An empty string hides the row.

**Methods**

`public static TooltipData TextOnly()`

:   A skill with no numeric preview still carries its cost, timing, and targeting copy.
    - `costText` &mdash; Driver-authored localized cost line.
    - `skillId` &mdash; Skill identity associated with the text-only tooltip.
    - `targetShapeText` &mdash; Driver-authored localized target-rule line.
    - `timingText` &mdash; Driver-authored localized timing line.
    - **Returns** &mdash; Tooltip data with numeric preview disabled and all amounts and chances set to zero.

---

## TooltipPanelView

```csharp
public sealed class TooltipPanelView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/TooltipPanelView.cs</small>

The skill tooltip: cost, timing, target shape, and the driver-computed
preview figures.

It renders a `TooltipData` value verbatim and calls no preview
or simulation API itself, which is what keeps the UI on the passive side
of the presenter contract.

**Properties**

`public bool IsShown`

:   True while a tooltip is displayed.

**Methods**

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the panel. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin the panel is dressed from; null falls back to the package default. The panel is left hidden.

`public void Hide()`

:   Hides the tooltip.

`public void Show(string title, TooltipData tooltip)`

:   Shows `tooltip` under `title`. Does nothing until `Build` has run.
    - `title` &mdash; Heading text, normally the skill's display name; null shows an empty heading.
    - `tooltip` &mdash; Values the driver already computed. Rows whose text is empty are hidden, the amount range and hit chance appear only when the value carries a preview, and the critical and status chances are each left out while impossible.

---

## TransportBarView

```csharp
public sealed class TransportBarView : MonoBehaviour
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/Regions/TransportBarView.cs</small>

Scenario picker, seed field, and playback controls, drawn with the skin.

This replaces an `OnGUI`/`GUI.skin.box` overlay. Immediate-mode
chrome is fine for an internal harness but it is the first thing a buyer
sees, it cannot be skinned, it ignores the canvas scaler, and it does not
exist on a touch device. Everything here is real uGUI and therefore
scales, skins, and works on mobile.

Pause, speed, and skip are presentation-only. They scale or halt the
visual clock and never a simulation value, so the same
(scenario, scheduler, formation, seed) tuple still reproduces identical
hashes.

**Events**

`public event Action NextRequested`

:   Raised when the player selects the next scenario.

`public event Action PauseToggled`

:   Raised when the player toggles pause.

`public event Action PreviousRequested`

:   Raised when the player selects the previous scenario.

`public event Action SkipRequested`

:   Raised when the player skips queued visuals.

`public event Action SpeedCycled`

:   Raised when the player cycles playback speed.

`public event Action<string> StartRequested`

:   Raised with the seed text when the player starts a battle.

**Methods**

`public void Build(CompiledBattleSkin battleSkin)`

:   Builds the bar. Explicit so EditMode tests can drive it.
    - `battleSkin` &mdash; Skin the bar is dressed from; null falls back to the package default.

`public void SetPaused(bool paused)`

:   Reflects the current pause state on the toggle.
    - `paused` &mdash; The state the host is now in, not the action to offer: true captions the button Resume.

`public void SetScenario(string text)`

:   Updates set scenario on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `text` &mdash; Name to show; null or empty shows a dash rather than a blank gap.

`public void SetSeedText(string text)`

:   Updates set seed text on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `text` &mdash; Seed characters written into the transport's editable field without submitting them.

`public void SetSpeed(float multiplier)`

:   Reflects the current playback speed.
    - `multiplier` &mdash; Visual speed multiplier, captioned as-is with an x suffix. Displaying it is all this does; the host owns the cycle order.

`public void SetStatus(string text)`

:   Updates set status on presentation state only. The call cannot submit a command, advance a tick, or change an authoritative hash.
    - `text` &mdash; Runtime lifecycle message shown beside the transport controls; null becomes empty.

---

## UiStatusEntry

```csharp
public readonly struct UiStatusEntry
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/BattleUiRoot.cs</small>

One combatant's surfaced status-panel row.

**Constructors**

`public UiStatusEntry()`

:   Records one row exactly as the snapshot reported it.
    - `combatantId` &mdash; Compiled combatant identity used for label and token lookup.
    - `health` &mdash; Current authoritative health reported by the snapshot.
    - `isDead` &mdash; Whether the snapshot marks the combatant as dead.
    - `maximumHealth` &mdash; Positive health capacity used to calculate the roster-bar fraction.
    - `shield` &mdash; Current shield amount displayed alongside health.
    - `statusCount` &mdash; Number of active statuses represented by roster pips.

`public UiStatusEntry()`

:   Records one row, including the team that decides its colour.
    - `combatantId` &mdash; Compiled combatant identity used for label and token lookup.
    - `health` &mdash; Current authoritative health reported by the snapshot.
    - `isDead` &mdash; Whether the snapshot marks the combatant as dead.
    - `maximumHealth` &mdash; Positive health capacity used to calculate the roster-bar fraction.
    - `shield` &mdash; Current shield amount displayed alongside health.
    - `statusCount` &mdash; Number of active statuses represented by roster pips.
    - `teamId` &mdash; Team the combatant belongs to, compared against the interface's player team to pick a bar colour.

**Properties**

`public StableId CombatantId`

:   Which combatant the row was built from. Look the display name up from this id; the row itself carries no text.

`public int Health`

:   Health exactly as the snapshot reported it; the row itself never interpolates. The roster's health bar eases toward the fraction this implies, and snaps only when the skin scales bar motion to zero, so the drawn bar can trail this value until `BattleUiRoot.Tick` advances it.

`public bool IsDead`

:   True when the snapshot no longer counts the combatant as living. Dead combatants keep their row, so the panel does not reshuffle as a battle thins out.

`public int MaximumHealth`

:   The health ceiling from the same snapshot, for drawing `Health` as a fraction.

`public int Shield`

:   Remaining shield summed over every shield the combatant owns.

`public int StatusCount`

:   How many status entries the snapshot lists for this combatant.

`public StableId TeamId`

:   The team this combatant fights for, or the default id when the row was built without one. It carries no simulation meaning here: it exists so the health bar can read as ours or theirs before any text is parsed.

---

## UiTimelineEntry

```csharp
public readonly struct UiTimelineEntry
```

`TurnGauge.Presentation` &middot; <small>Runtime/Presentation/UI/BattleUiRoot.cs</small>

One chip on the turn-order rail: who acts, whose side they are on, how much
of them is left, and whether they are still standing.

The rail is the element the product is named after, and a chip carrying only
a name answers one question out of four. This carries the other three, so a
single glance at the rail tells a player what is coming and whether it
matters.

**Constructors**

`public UiTimelineEntry()`

:   Records one chip from values the interface was already given.
    - `combatantId` &mdash; Combatant the chip stands for; also the portrait lookup key.
    - `healthFraction` &mdash; Remaining health in zero to one, drawn as the chip's underline.
    - `isAlly` &mdash; Whether the chip takes the ally rim or the enemy rim.
    - `isDead` &mdash; Whether the chip is greyed and struck through rather than removed.
    - `statusCount` &mdash; How many statuses ride the chip, capped when drawn.

**Properties**

`public StableId CombatantId`

:   The combatant this chip stands for.

`public float HealthFraction`

:   Remaining health in zero to one, already clamped.

`public bool IsAlly`

:   True when the chip belongs to the player's team.

`public bool IsDead`

:   True when the combatant is down. The chip stays in place regardless.

`public int StatusCount`

:   Active status count, already floored at zero.

---
