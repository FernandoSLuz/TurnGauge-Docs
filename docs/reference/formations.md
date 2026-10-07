# Formations

16 types in this area.

!!! abstract "On this page"
    [AspectRatio](#aspectratio) &middot; [CompiledEncounterFormationLayout](#compiledencounterformationlayout) &middot; [CompiledEncounterFormationTeam](#compiledencounterformationteam) &middot; [CompiledFormationAnchor](#compiledformationanchor) &middot; [CompiledFormationPreset](#compiledformationpreset) &middot; [CompiledFormationSlot](#compiledformationslot) &middot; [FormationArrangement](#formationarrangement) &middot; [FormationArrangements](#formationarrangements) &middot; [FormationFacing](#formationfacing) &middot; [FormationOccupancy](#formationoccupancy) &middot; [FormationPoint](#formationpoint) &middot; [FormationPresetDefinition](#formationpresetdefinition) &middot; [FormationSlotDefinition](#formationslotdefinition) &middot; [FormationVfxAnchorDefinition](#formationvfxanchordefinition) &middot; [FormationViewport](#formationviewport) &middot; [ProjectedFormationPoint](#projectedformationpoint)

## AspectRatio

```csharp
public readonly struct AspectRatio : IEquatable<AspectRatio>
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

The design aspect a formation was authored against, as an exact integer
fraction where `Numerator` is the width term and
`Denominator` the height term. The fraction is never reduced,
so 16/9 and 32/18 are different values. Components outside 1..10,000
(`AuthoringLimits.AspectComponentMaximum`) are reported as a
compile or projection diagnostic rather than rejected here.

**Constructors**

`public AspectRatio(int numerator, int denominator)`

:   Copies the width and height terms without reducing or range-checking the fraction. Compilation reports components outside 1..10,000.

    - `denominator` &mdash; Height term retained verbatim as the fraction's denominator.
    - `numerator` &mdash; Width term retained verbatim as the fraction's numerator.

**Properties**

`public int Denominator`

:   The height term, held to the same 1..`AuthoringLimits.AspectComponentMaximum` range as `Numerator`.

`public int Numerator`

:   The width term of the fraction. Projection and compilation accept 1..`AuthoringLimits.AspectComponentMaximum`; anything else is reported as a diagnostic, so a default-constructed ratio with a zero term fails rather than dividing by zero.

**Methods**

`public bool Equals(AspectRatio other)`

:   Equal only when both terms match, because the fraction is never reduced.

    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value comparison against a boxed ratio; any other type is never equal.

    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override int GetHashCode()`

:   Combines both terms; consistent with `Equals(AspectRatio)`.

    - **Returns** &mdash; A deterministic hash code for this value.

---

## CompiledEncounterFormationLayout

```csharp
public sealed class CompiledEncounterFormationLayout
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

The compiled formation for a whole encounter: exactly two teams, plus a
flattened and indexed view of every combatant's seat. This is the object
presentation builds a stage from, and it is fully immutable, so the same
layout can drive a live battle, a headless batch and an editor preview at
once.

**Properties**

`public StableId EncounterId`

:   The encounter this layout was compiled for, carried so a layout handed on its own can still be matched back to the encounter that produced it.

`public FrozenList<FormationOccupancy> Occupancy`

:   Both teams' bindings merged into one list, ascending by combatant id.

`public FrozenSortedIndex<StableId, FormationOccupancy> OccupancyByCombatant`

:   Combatant to seat, as a binary-searchable index over the same records held in `Occupancy`. Use it rather than scanning that list when placing a token or building a start request; every combatant in the encounter has an entry, because an unassigned member fails the compile.

`public FrozenSortedIndex<StableId, StableId> OccupancyBySlot`

:   Seat to occupant: the value is the combatant id standing in that slot, not a full occupancy record. Seats nobody was assigned to are absent.

`public FrozenList<CompiledEncounterFormationTeam> Teams`

:   Both teams, ascending by team id.

---

## CompiledEncounterFormationTeam

```csharp
public sealed class CompiledEncounterFormationTeam
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

One team's half of a compiled encounter layout: the preset it stands in
and which combatant holds which seat. Compilation only succeeds when every
member of the team is assigned to a free seat and all of those seats sit on
one side of the field.

**Properties**

`public FrozenList<FormationOccupancy> Occupancy`

:   This team's combatant-to-seat bindings, ascending by combatant id. Every member is present, because an unassigned member fails the compile.

`public CompiledFormationPreset Preset`

:   A deep copy of the preset the team was compiled against, so the layout stands alone once returned.

`public StableId ResolvedSideId`

:   The one side id shared by every seat this team occupies. Compilation fails if a team's seats disagree, or if both teams resolve to the same side.

`public StableId TeamId`

:   The team this half of the layout belongs to. It is what the two teams of a layout are sorted by, and the two must differ.

---

## CompiledFormationAnchor

```csharp
public readonly struct CompiledFormationAnchor
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

One named attachment point on a compiled slot. Presentation resolves a
beat's VFX position through these, so a slot can offer more than the one
point the combatant stands on. Only the formation compiler creates them,
and `Position` is in the same normalised design space as the
slot's own position.

**Properties**

`public StableId AnchorId`

:   The name a presentation beat asks for this anchor by. It is unique among the anchors of its slot but not across the preset, so two seats may both offer, say, a "muzzle" anchor.

`public FormationPoint Position`

:   Where the anchor sits, in the preset's normalised design space rather than as an offset from the slot, so it is projected exactly as the slot's own position is.

---

## CompiledFormationPreset

```csharp
public sealed class CompiledFormationPreset
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

A validated, immutable formation preset: the seats one team can occupy,
plus the design aspect their coordinates were authored against. Only the
formation compiler creates one, and it stores the slots ascending by slot
id, which is what lets `TryGetSlot` binary search instead of
scanning.

**Properties**

`public AspectRatio DesignAspect`

:   The aspect the slot coordinates were authored for. Projection fits the target viewport to this ratio before mapping any point, so the preset keeps its shape on screens it was not designed for.

`public StableId PresetId`

:   This preset's identity, carried into every `FormationOccupancy` compiled against it so a consumer can tell which preset a seated combatant was placed from.

`public FrozenList<CompiledFormationSlot> Slots`

:   Every seat in the preset, ascending by slot id.

**Methods**

`public bool TryGetSlot(StableId slotId, out CompiledFormationSlot slot)`

:   Looks up one seat by id with a binary search over `Slots`.

    - `slotId` &mdash; Id of the seat to find.
    - `slot` &mdash; The matching seat, or null when the preset declares no such slot.
    - **Returns** &mdash; True when a seat with that id exists.

---

## CompiledFormationSlot

```csharp
public sealed class CompiledFormationSlot
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

One validated seat in a compiled formation preset: where a combatant
stands, which way it faces, how it sorts against the other seats, and
where its anchors are. Only the formation compiler creates these, and
every value on a compiled slot is immutable, so one can be handed to the
stage, an editor preview and a batch run at the same time.

**Properties**

`public FrozenList<CompiledFormationAnchor> Anchors`

:   This seat's anchors, ascending by anchor id, and empty when the slot declares none.

`public FormationPoint ApproachPoint`

:   The point a step-in or approach beat targets, in the same normalised space as `Position`. It is authored per slot rather than derived, so an approach can lead in front of, behind or beside a seat.

`public FormationFacing Facing`

:   Which way the occupant is presented as facing. Compilation rejects any value other than `FormationFacing.Left` or `FormationFacing.Right`, so this is never the enum default.

`public FormationPoint Position`

:   Where the occupant stands, in the preset's normalised design space.

`public StableId RowId`

:   The row this seat belongs to. Rows are a grouping rather than an identity, so several seats normally share one row id, and it is carried through to the combatant's start state where row-based targeting matches on it.

`public StableId SideId`

:   The side of the field this seat sits on. Every seat a team actually occupies must agree on it, which is what stops a team straddling both sides, and it reaches the combatant's start state for side-based targeting.

`public StableId SlotId`

:   This seat's identity, unique within the preset. Encounter assignments name a seat by this id, and it is the key `CompiledFormationPreset.TryGetSlot` searches on.

`public StableId SortingLayerKey`

:   Identifier of the sorting layer this seat belongs to. The package carries it as data only; nothing here assigns it to a Unity sorting layer, so a custom stage decides how to map it.

`public int SortingOrder`

:   Draw order within the sorting layer. The compiler restricts it to -32,768..32,767 (`AuthoringLimits.SortingOrderMinimum` and `AuthoringLimits.SortingOrderMaximum`), so it always fits Unity's own sorting order range.

---

## FormationArrangement

```csharp
public enum FormationArrangement : byte
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationArrangements.cs</small>

The stage shapes a battle can be laid out in.

A formation preset is authored data, so these are not modes the engine
switches between at runtime: they are starting points
`FormationArrangements` can build a preset from, which you then
ship, edit in the Formation Editor, or ignore entirely in favour of placing
every seat by hand.

| Value | Meaning |
| --- | --- |
| `Rank` | One rank per side, standing shoulder to shoulder along a single baseline, in the manner of a party line-up in a 2D dungeon crawler. |
| `Column` | One column per side, stacked up the screen, in the manner of a classic console role-playing game party list. |
| `Stagger` | A column with every second seat pushed toward the centre, so the side reads as a diagonal rather than a straight stack. |
| `Perspective` | Two parallel lines per side, the back one raised and pushed toward the centre so the pair reads as a receding plane. |

---

## FormationArrangements

```csharp
public static class FormationArrangements
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationArrangements.cs</small>

Builds formation presets for the shipped stage arrangements.

The value here is not the coordinates, which anyone could type; it is that
the draw order comes out right. Formation space puts Y at the bottom of the
stage and increases upward, so a seat lower on screen is nearer the camera
and has to be drawn over the seats behind it. Authoring that by hand is easy
to get backwards, and it stays invisible until two silhouettes actually
overlap - by which point the art is in and the formation is hard to change.

**Fields**

`public const int CoordinateMaximum`

:   Normalized coordinate space is 0 to this value on both axes.

`public const int LeftTeamFrontSortingOrder`

:   Sorting order the front seat of the left team receives.

`public const int MaximumSlotsPerSide`

:   Largest number of seats per side these builders will produce.

`public const int RightTeamFrontSortingOrder`

:   Sorting order the front seat of the right team receives.

`public const string SortingLayerKey`

:   Sorting layer key every produced seat carries, matching the shipped starter presets. The compiler rejects an empty key, so this is not optional decoration.

`public const int StaggerInset`

:   How far `FormationArrangement.Stagger` pushes every second seat toward the centre. Wide enough that a broad silhouette still shows an edge past the one in front, narrow enough that the side still reads as one group rather than two.

**Methods**

`public static FormationPresetDefinition Build(string stableIdRaw, FormationArrangement arrangement, int slotsPerSide)`

:   Builds a preset for `arrangement` with `slotsPerSide` seats on each side.

    - `stableIdRaw` &mdash; Stable id for the produced preset.
    - `slotsPerSide` &mdash; Seats per side, 1 to `MaximumSlotsPerSide`.
    - `arrangement` &mdash; Rank, column, staggered-column, or perspective seat geometry to materialize.
    - **Returns** &mdash; A new unsaved preset with deterministic seat coordinates, facing, and front-to-back sorting.

---

## FormationFacing

```csharp
public enum FormationFacing : byte
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationDefinitions.cs</small>

Which way the occupant of a formation slot is presented as facing. It
reaches the battle through presentation only: the built-in 2D stage
mirrors the combatant token's sprite only when the slot facing differs
from its source-art facing (Right by default). Neither name is zero, so
default(FormationFacing) is not a facing at all and preset compilation
rejects any slot carrying a value other than these two.

| Value | Meaning |
| --- | --- |
| `Left` | Faces the formation slot toward decreasing X in projected stage space. |
| `Right` | Faces the formation slot toward increasing X in projected stage space. |

---

## FormationOccupancy

```csharp
public readonly struct FormationOccupancy
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

The resolved binding of one combatant to one seat, with the team, preset,
row and side that seat belongs to copied in so a consumer never has to
walk back to the preset to draw or query a combatant. The compiler
guarantees a combatant appears at most once and that no two combatants
share a slot.

**Properties**

`public StableId CombatantId`

:   The combatant standing in the seat. Every occupancy list is sorted on it and `CompiledEncounterFormationLayout.OccupancyByCombatant` is keyed on it; the seat-first index `CompiledEncounterFormationLayout.OccupancyBySlot` is keyed on the slot id instead and only carries this id as its value. It appears exactly once across the whole layout.

`public StableId PresetId`

:   The preset the seat was taken from, so a consumer holding only this record can still name the layout the combatant was placed by.

`public StableId RowId`

:   The seat's row, copied from the slot. The encounter compiler passes it straight into the combatant's start state, so row-based targeting in the battle matches on this value.

`public StableId SideId`

:   The seat's side, copied from the slot and likewise carried into the combatant's start state for side-based targeting. Every occupancy on a team shares it.

`public StableId SlotId`

:   The seat itself. Look it up in the team's preset to reach the position, facing, sorting values and anchors.

`public StableId TeamId`

:   The team the combatant fights for.

---

## FormationPoint

```csharp
public readonly struct FormationPoint : IEquatable<FormationPoint>
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

A resolution-independent position inside a formation preset. Both
components are integers from 0 to 1,000,000
(`AuthoringLimits.NormalizedCoordinateMaximum`), measured from
the bottom-left corner of the design rectangle, and the compiler rejects
any slot or anchor that falls outside that range. The space is integral on
purpose: projection uses integer arithmetic only, so the same preset lands
on the same pixels on every platform.

**Constructors**

`public FormationPoint(int x, int y)`

:   Copies authored X/Y coordinates in formation reference units. Range and overlap checks occur during compilation.

    - `x` &mdash; Horizontal position, 0 at the design rectangle's left edge.
    - `y` &mdash; Vertical position, 0 at the design rectangle's bottom edge.

**Properties**

`public int X`

:   Horizontal position, 0 at the design rectangle's left edge and `AuthoringLimits.NormalizedCoordinateMaximum` at its right, whatever pixel width the preset is eventually projected into.

`public int Y`

:   Vertical position on the same normalised scale, measured upward from the design rectangle's bottom edge.

**Methods**

`public bool Equals(FormationPoint other)`

:   Equal only when both components match.

    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value comparison against a boxed point; any other type is never equal.

    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override int GetHashCode()`

:   Combines both components; consistent with `Equals(FormationPoint)`.

    - **Returns** &mdash; A deterministic hash code for this value.

---

## FormationPresetDefinition

:material-star: **Start here**

```csharp
public sealed class FormationPresetDefinition : StableIdDefinition
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationPresetDefinition.cs</small>

Mutable Unity authoring data. Compilation snapshots every value and returns
engine-independent immutable records; this object is never retained.

**Properties**

`public int DesignAspectDenominator`

:   Denominator of that same authored aspect, under the same bounds.

`public int DesignAspectNumerator`

:   Numerator of the aspect ratio the slot coordinates were authored against. Projection fits the target viewport to this ratio before mapping any point, so the preset keeps its shape on screens it was not designed for. It must be between 1 and `AuthoringLimits.AspectComponentMaximum` to compile.

`public IReadOnlyList<FormationSlotDefinition> Slots`

:   The seats authored on this preset, in authored order. This is the live backing list rather than a copy, and it is null when the preset was built from a null sequence, which compilation reports as an error instead of reading as a preset with no seats.

**Methods**

`public static FormationPresetDefinition CreateTransient(string stableIdRaw, int aspectNumerator, int aspectDenominator, IEnumerable<FormationSlotDefinition> formationSlots, int schemaVersion = CurrentSchemaVersion)`

:   Explicit in-memory construction hook for tests and customer tooling. It creates no asset, GUID, or implicit persistent mutation.

    - `stableIdRaw` &mdash; Preset ID text, stored verbatim. It is not checked here: empty or invalid ID text becomes a compile diagnostic instead.
    - `aspectNumerator` &mdash; Numerator of the design aspect the slots are authored against.
    - `aspectDenominator` &mdash; Denominator of that design aspect.
    - `formationSlots` &mdash; The slots to copy. The copy is bounded, but not trimmed to a valid preset: a sequence longer than `AuthoringLimits.FormationSlotsPerPreset` compiles to a collection-limit error, and null leaves the preset with no slot list at all, which is an error of its own.
    - `schemaVersion` &mdash; Authoring schema version to stamp. Any value other than the current one fails validation rather than being migrated in place.
    - **Returns** &mdash; A new unsaved instance holding a copy of the slots. It belongs to no catalog, so the caller keeps it alive and adds it to one itself.

---

## FormationSlotDefinition

```csharp
public sealed class FormationSlotDefinition
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationDefinitions.cs</small>

Mutable Unity authoring data for one seat in a formation preset: where a
combatant stands, which way it faces, how it sorts against the other
seats, where a step-in beat leads, and which named VFX anchors it offers.
Compilation validates every value and snapshots it into an immutable
`CompiledFormationSlot`; this object is never retained. Its
four id fields are all stored as raw text and every one of them must parse
as a non-empty id, so a half-filled seat fails the preset rather than
compiling to a default.

**Constructors**

`public FormationSlotDefinition()`

:   Creates a seat with empty ids at the origin, facing `FormationFacing.Right` and declaring no anchors, as the inspector does when you add a list entry. Its empty ids fail compilation, so it has to be filled in before the preset builds.

`public FormationSlotDefinition(string slotIdRaw, string rowIdRaw, string sideIdRaw, int normalizedX, int normalizedY, FormationFacing formationFacing, string sortingLayerKeyRaw, int authoredSortingOrder, int normalizedApproachX, int normalizedApproachY, IEnumerable<FormationVfxAnchorDefinition> vfxAnchors)`

:   Creates a seat from authored values. Nothing is validated here: parsing, range and uniqueness checks belong to the deterministic compiler, so a bad value surfaces as a compile diagnostic rather than an exception from this call.

    - `slotIdRaw` &mdash; Seat id text. It must be non-empty, valid id text and unique within the preset; a duplicate is a compile error.
    - `rowIdRaw` &mdash; Grouping id for the row this seat sits in. It must be non-empty, valid id text, but it is shared freely: several seats normally carry the same row id.
    - `sideIdRaw` &mdash; Grouping id for the side of the field this seat sits on. It must be non-empty, valid id text, and every seat a team actually occupies has to agree on it, so a team cannot straddle two sides.
    - `normalizedX` &mdash; Horizontal stand position in normalised design space; see `PositionX`.
    - `normalizedY` &mdash; Vertical stand position in the same space; see `PositionY`.
    - `formationFacing` &mdash; Presented facing. It must be `FormationFacing.Left` or `FormationFacing.Right`; the enum's default value is not valid.
    - `sortingLayerKeyRaw` &mdash; Sorting layer id text, carried as data only. It must be non-empty, valid id text, but the package never assigns it to a Unity sorting layer: a custom stage decides what it maps to.
    - `authoredSortingOrder` &mdash; Draw order within that layer. Compilation restricts it to `AuthoringLimits.SortingOrderMinimum`..`AuthoringLimits.SortingOrderMaximum`, which is Unity's own sorting order range.
    - `normalizedApproachX` &mdash; Horizontal component of the approach point; see `ApproachX`.
    - `normalizedApproachY` &mdash; Vertical component of the approach point; see `ApproachY`.
    - `vfxAnchors` &mdash; Named anchors for this seat. The sequence is copied immediately, so later changes to it do not reach the slot, and enumeration stops one past `AuthoringLimits.VfxAnchorsPerSlot` so an over-long or endless sequence is reported by compilation instead of being read to exhaustion. Passing null leaves `Anchors` null, which compilation treats as an error rather than as an empty list.

**Properties**

`public IReadOnlyList<FormationVfxAnchorDefinition> Anchors`

:   The anchors authored on this seat, in authored order. This is the live backing list rather than a copy, and it is null when the slot was constructed from a null sequence, which compilation reports as an error instead of reading as an empty list.

`public int ApproachX`

:   Horizontal component of the point a step-in or approach beat targets, in the same normalised space as `PositionX`. It is authored rather than derived, so an approach can lead in front of, behind or beside the seat.

`public int ApproachY`

:   Vertical component of the approach point, in the same normalised space as `PositionY`.

`public FormationFacing Facing`

:   Which way the occupant of this seat is presented as facing. It reaches the battle through presentation only, where the built-in 2D stage mirrors the token's sprite only when this differs from its source-art facing (Right by default). It must be one of the two named values, because the enum's default is not a facing and compilation rejects it.

`public int PositionX`

:   Horizontal stand position in the preset's normalised design space, running 0 at the left edge to `AuthoringLimits.NormalizedCoordinateMaximum` at the right. Anything outside that range fails compilation; two seats sharing a position only warn.

`public int PositionY`

:   Vertical stand position in the same normalised space, measured upward from the bottom edge.

`public string RowIdRaw`

:   The authored row id as text, empty when unset.

`public string SideIdRaw`

:   The authored side id as text, empty when unset. Every seat a team occupies must carry the same side id, so this is what decides which side of the field the team lands on.

`public string SlotIdRaw`

:   The authored seat id as text, empty when unset and never null. It is unparsed: compilation turns it into the id assignments and lookups use.

`public string SortingLayerKeyRaw`

:   The authored sorting layer id as text, empty when unset. The package carries it as data only; nothing here assigns it to a Unity sorting layer, so a custom stage decides how to map it.

`public int SortingOrder`

:   Draw order within the sorting layer. Compilation restricts it to -32,768..32,767, which is Unity's own sorting order range.

---

## FormationVfxAnchorDefinition

```csharp
public sealed class FormationVfxAnchorDefinition
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationDefinitions.cs</small>

Mutable Unity authoring data for one named point on a formation slot that
a presentation beat can target instead of the slot itself. Compilation
validates every value and snapshots it into an immutable
`CompiledFormationAnchor`; this object is never retained.

**Constructors**

`public FormationVfxAnchorDefinition()`

:   Creates an anchor with an empty id at the origin, as the inspector does when you add a list entry. The empty id fails compilation, so an anchor created this way has to be filled in before the preset builds.

`public FormationVfxAnchorDefinition(string anchorIdRaw, int normalizedX, int normalizedY)`

:   Creates an anchor from authored values. Nothing is validated here: parsing and range checks belong to the deterministic compiler, so an out-of-range or unparsable value surfaces as a compile diagnostic rather than an exception from this call.

    - `anchorIdRaw` &mdash; Anchor id text. It must be non-empty, valid id text and unique among the anchors of its slot, or preset compilation fails. Null is stored as the empty string.
    - `normalizedX` &mdash; Horizontal position in the preset's normalised design space; see `PositionX`.
    - `normalizedY` &mdash; Vertical position in the same space; see `PositionY`.

**Properties**

`public string AnchorIdRaw`

:   The authored anchor id as text, empty when unset. It is never null, and it is unparsed: compilation turns it into the id the stage looks anchors up by.

`public int PositionX`

:   Horizontal position in the preset's normalised design space, running 0 at the left edge to `AuthoringLimits.NormalizedCoordinateMaximum` at the right. Anything outside that range fails compilation.

`public int PositionY`

:   Vertical position in the same normalised space, measured upward from the bottom edge.

---

## FormationViewport

```csharp
public readonly struct FormationViewport : IEquatable<FormationViewport>
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

The screen-space rectangle a formation is projected into, in pixels, with
the origin at `Left`/`Bottom` and Y increasing
upward. Width and height must both be positive or projection fails with a
diagnostic instead of throwing. The projector treats this rectangle as a
bound, not as the frame the slots land in: it first shrinks the rectangle
to the preset's design aspect and centres the result inside it.

**Constructors**

`public FormationViewport(int left, int bottom, int width, int height)`

:   Copies the viewport origin and size in integer pixels. Projection reports non-positive dimensions instead of dividing by them.

    - `left` &mdash; Left edge in pixels.
    - `bottom` &mdash; Bottom edge in pixels; the rectangle grows upward.
    - `width` &mdash; Width in pixels. Projection fails unless positive.
    - `height` &mdash; Height in pixels. Projection fails unless positive.

**Properties**

`public int Bottom`

:   Bottom edge in pixels. The rectangle grows upward from here, so this is the low Y edge rather than the top one.

`public int Height`

:   Height in pixels, under the same positive-value and overflow rules as `Width`.

`public int Left`

:   Left edge in pixels, with X increasing to the right.

`public int Width`

:   Width in pixels. Projection fails with a diagnostic when it is zero or negative, and also when `Left` plus this width would overflow, so a degenerate rectangle never reaches the slot mapping.

**Methods**

`public bool Equals(FormationViewport other)`

:   Equal only when all four edges match.

    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value comparison against a boxed viewport; any other type is never equal.

    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override int GetHashCode()`

:   Combines all four edges; consistent with `Equals(FormationViewport)`.

    - **Returns** &mdash; A deterministic hash code for this value.

---

## ProjectedFormationPoint

```csharp
public readonly struct ProjectedFormationPoint : IEquatable<ProjectedFormationPoint>
```

`TurnGauge.Authoring` &middot; <small>Runtime/Authoring/Formation/FormationModels.cs</small>

A formation point after projection, in the pixel space of the
`FormationViewport` it was fitted into. It is a separate type
from `FormationPoint` so normalised authoring coordinates and
projected screen coordinates cannot be passed for one another by mistake.

**Constructors**

`public ProjectedFormationPoint(int x, int y)`

:   Copies projected X/Y pixel coordinates for a concrete viewport. It carries no transform or scene reference.

    - `x` &mdash; Absolute horizontal pixel coordinate in the destination viewport's space.
    - `y` &mdash; Absolute vertical pixel coordinate in the destination viewport's space.

**Properties**

`public int X`

:   Horizontal pixel position, measured in the same space as the viewport that was projected into and already offset by that viewport's left edge, so it is an absolute coordinate rather than one relative to the formation.

`public int Y`

:   Vertical pixel position, offset by the viewport's bottom edge and increasing upward.

**Methods**

`public bool Equals(ProjectedFormationPoint other)`

:   Equal only when both components match.

    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value comparison against a boxed point; any other type is never equal.

    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override int GetHashCode()`

:   Combines both components; consistent with `Equals(ProjectedFormationPoint)`.

    - **Returns** &mdash; A deterministic hash code for this value.

---
