# Numerics and determinism

8 types in this area.

!!! abstract "On this page"
    [CanonicalBattleSerializer](#canonicalbattleserializer) &middot; [Chance64](#chance64) &middot; [DeterministicRng](#deterministicrng) &middot; [Diagnostic](#diagnostic) &middot; [Fixed64](#fixed64) &middot; [FrozenList](#frozenlist) &middot; [Sha256Digest](#sha256digest) &middot; [StableId](#stableid)

## CanonicalBattleSerializer

```csharp
public static partial class CanonicalBattleSerializer
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Canonical/CanonicalBattleSerializer.B3.cs</small>

Encodes and decodes battle state as a canonical byte stream.

Canonical means one state has exactly one encoding: field order, integer
width and collection order are all fixed, so two machines that agree on the
state produce identical bytes. That is what makes the event-chain digest
comparable across platforms, and it is why nothing here may be reordered
for convenience.

A `BattleSnapshot` has no public constructor, so decoding
through here is one of only two ways to obtain one; the other is stepping a
`BattleEngine`.

**Properties**

`public static Sha256Digest EmptyEventChain`

:   Gets the domain-separated hash that anchors an event chain before its first event.

**Fields**

`public const int MaximumCanonicalBattleStateBytes`

:   Maximum byte length accepted for a canonical battle-state snapshot.

`public const int MaximumCanonicalSnapshotBytes`

:   Maximum byte length accepted for a canonical compiled-content snapshot.

`public const int MaximumCanonicalStartBytes`

:   Maximum byte length accepted for a canonical battle-start request.

**Methods**

`public static Sha256Digest AdvanceEventChain(Sha256Digest previous, BattleEvent battleEvent)`

:   Appends one canonical event to a domain-separated hash chain.
    - `battleEvent` &mdash; The next event whose canonical bytes are committed to the chain.
    - `previous` &mdash; The valid digest at the current end of the event chain.
    - **Returns** &mdash; The new chain digest covering the previous digest and appended event.

`public static BattleSnapshot DecodeBattleState(byte[] bytes)`

:   Strictly reads decode battle state and rejects malformed, trailing, unsupported, or incompatible data without a partial result.
    - `bytes` &mdash; The canonical byte payload to read.
    - **Returns** &mdash; The canonical battle snapshot reconstructed with built-in scheduler implementations.

`public static BattleSnapshot DecodeBattleState()`

:   Strictly reads decode battle state and rejects malformed, trailing, unsupported, or incompatible data without a partial result.
    - `bytes` &mdash; The canonical byte payload to read.
    - `schedulerRegistry` &mdash; The registry used to decode and verify scheduler-specific state.
    - **Returns** &mdash; The canonical battle snapshot reconstructed from the versioned payload.

`public static CompiledBattleContent DecodeCompiledSnapshot(byte[] bytes)`

:   Strictly reads decode compiled snapshot and rejects malformed, trailing, unsupported, or incompatible data without a partial result.
    - `bytes` &mdash; The canonical byte payload to read.
    - **Returns** &mdash; The compiled content reconstructed with the built-in mechanics registry.

`public static CompiledBattleContent DecodeCompiledSnapshot()`

:   Strictly reads decode compiled snapshot and rejects malformed, trailing, unsupported, or incompatible data without a partial result.
    - `bytes` &mdash; The canonical byte payload to read.
    - `mechanicsRegistry` &mdash; The registry used to resolve mechanics identities required by version-three content.
    - **Returns** &mdash; The compiled content reconstructed from the versioned canonical payload.

`public static BattleStartRequest DecodeStartRequest(byte[] bytes)`

:   Strictly reads decode start request and rejects malformed, trailing, unsupported, or incompatible data without a partial result.
    - `bytes` &mdash; The canonical byte payload to read.
    - **Returns** &mdash; The battle-start request reconstructed from the versioned canonical payload.

`public static byte[] EncodeBattleState(BattleSnapshot snapshot)`

:   Serializes a battle snapshot using its profile and built-in scheduler implementations.
    - `snapshot` &mdash; The complete deterministic battle state to encode.
    - **Returns** &mdash; The unique canonical byte representation of the battle state.

`public static byte[] EncodeBattleState()`

:   Serializes a battle snapshot while resolving B2 or B3 scheduler state through the supplied registry.
    - `schedulerRegistry` &mdash; The registry that supplies codecs for scheduler identities present in the snapshot.
    - `snapshot` &mdash; The complete deterministic battle state to encode.
    - **Returns** &mdash; The unique canonical byte representation of the battle state.

`public static byte[] EncodeCommand(BattleCommand command)`

:   Serializes a battle command into the versioned envelope that commits its identity, actor, targets, skill, and properties.
    - `command` &mdash; The command type, submission identity, actor, target, skill, and properties to encode.
    - **Returns** &mdash; The unique canonical byte representation of the command.

`public static byte[] EncodeCompiledSnapshot(CompiledBattleContent content)`

:   Serializes compiled battle content using its B1, B2, or B3 canonical schema and rejects unsupported profiles.
    - `content` &mdash; The validated compiled content whose profile determines the encoded schema version.
    - **Returns** &mdash; The unique canonical byte representation of `content`.

`public static byte[] EncodeEvent(BattleEvent battleEvent)`

:   Serializes a battle event with its tick, sequence identities, type, and payload.
    - `battleEvent` &mdash; The emitted event to place in the version-one canonical event envelope.
    - **Returns** &mdash; The unique canonical byte representation of the event.

`public static byte[] EncodeFormulaAttribution(FormulaAttribution attribution)`

:   Produces deterministic encode formula attribution output with stable ordering and invariant numeric formatting.
    - `attribution` &mdash; The formula identity, participants, inputs, intermediate values, and final result to encode.
    - **Returns** &mdash; The canonical version-one formula-attribution payload.

`public static byte[] EncodeStartRequest(BattleStartRequest start)`

:   Serializes a battle-start request using the canonical format selected by its profile.
    - `start` &mdash; The complete initial battle configuration to encode.
    - **Returns** &mdash; The unique canonical byte representation of the start request.

`public static Sha256Digest HashBattleState(BattleSnapshot snapshot)`

:   Computes the SHA-256 digest of a battle snapshot encoded with built-in schedulers.
    - `snapshot` &mdash; The complete deterministic battle state to canonicalize.
    - **Returns** &mdash; The digest identifying the canonical battle-state payload.

`public static Sha256Digest HashBattleState()`

:   Computes the SHA-256 digest of battle state encoded through a supplied scheduler registry.
    - `schedulerRegistry` &mdash; The registry that supplies codecs for scheduler identities present in the snapshot.
    - `snapshot` &mdash; The complete deterministic battle state to canonicalize.
    - **Returns** &mdash; The digest identifying the registry-compatible canonical state payload.

`public static Sha256Digest HashCommand(BattleCommand command)`

:   Computes the SHA-256 digest of a battle command's canonical bytes.
    - `command` &mdash; The command to canonicalize, including its submission metadata and payload.
    - **Returns** &mdash; The digest identifying the encoded command.

`public static Sha256Digest HashCompiledSnapshot(CompiledBattleContent content)`

:   Computes the SHA-256 digest of a compiled-content snapshot's canonical bytes.
    - `content` &mdash; The compiled content to serialize according to its contract profile.
    - **Returns** &mdash; The digest identifying the complete canonical compiled snapshot.

`public static Sha256Digest HashContentManifest(CompiledBattleContent content)`

:   Computes a domain- and schema-versioned manifest digest for compiled battle content.
    - `content` &mdash; The compiled content whose profile, schema version, and snapshot bytes enter the manifest.
    - **Returns** &mdash; The digest used to identify the content manifest.

`public static Sha256Digest HashEvent(BattleEvent battleEvent)`

:   Computes the SHA-256 digest of a battle event's canonical bytes.
    - `battleEvent` &mdash; The emitted event to canonicalize.
    - **Returns** &mdash; The digest identifying the event envelope and payload.

`public static Sha256Digest HashFormulaAttribution(FormulaAttribution attribution)`

:   Produces deterministic hash formula attribution output with stable ordering and invariant numeric formatting.
    - `attribution` &mdash; The complete formula evaluation trace to canonicalize.
    - **Returns** &mdash; The SHA-256 digest of the canonical formula-attribution payload.

`public static Sha256Digest HashPropertySet(PropertySet properties)`

:   Computes the canonical digest of a property set.
    - `properties` &mdash; The property names and tagged values to canonicalize and hash.
    - **Returns** &mdash; The SHA-256 digest of the property's unique canonical representation.

`public static Sha256Digest HashReplayCheckpoint(ReplayCheckpoint checkpoint)`

:   Computes a domain-separated digest over a replay checkpoint's position and integrity hashes.
    - `checkpoint` &mdash; The replay command count, clock position, event sequence, state hash, and chain hash to commit.
    - **Returns** &mdash; The digest identifying that exact replay checkpoint.

`public static Sha256Digest HashStartRequest(BattleStartRequest start)`

:   Computes the SHA-256 digest of a battle-start request's canonical bytes.
    - `start` &mdash; The initial battle configuration to canonicalize.
    - **Returns** &mdash; The digest identifying the complete canonical start request.

---

## Chance64

:material-star: **Start here**

```csharp
public readonly struct Chance64 : IEquatable<Chance64>, IComparable<Chance64>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Numerics/Chance64.cs</small>

A deterministic probability value where 1,000,000 raw units equal 100%.
This type is deliberately distinct from Fixed64.

**Constructors**

`public Chance64(long raw)`

:   Wraps a raw probability that is already inside the domain.
    - `raw` &mdash; Probability in raw units, where 0 is never and `Scale` is always; 500,000 is 50%.

**Properties**

`public bool IsGuaranteed`

:   Whether the event always occurs. It short-circuits sampling exactly as `IsImpossible` does, and costs no RNG draw either.

`public bool IsImpossible`

:   Whether the event can never occur. The built-in formulas and status application test this before sampling, so a zero chance consumes no draw from the battle RNG and therefore does not shift any later roll.

`public long Raw`

:   The probability in raw units. Divide by `Scale` only when presenting it; keep the raw value in anything the simulation reads, since converting to floating point is what would let two machines disagree.

**Fields**

`public static readonly Chance64 Guaranteed`

:   Certain probability equal to `Scale`, also resolved without consuming an RNG draw.

`public const long Scale`

:   Raw probability units spanning the closed interval from never to guaranteed; one million units equal 100%.

`public static readonly Chance64 Zero`

:   Impossible probability, which short-circuits sampling without consuming an RNG draw.

`public static bool operator`

:   Returns a new value computed from the operands without mutating either operand; numeric overflow follows the underlying contract.
    - `left` &mdash; First probability compared by exact raw units.
    - `right` &mdash; Second probability compared by exact raw units.
    - **Returns** &mdash; The value produced by applying the operator.

**Methods**

`public static Chance64 ApplyResistance(Chance64 baseChance, Chance64 resistance)`

:   Reduces a probability by a resistance, multiplying it by the resistance's complement.
    - `baseChance` &mdash; The unresisted probability.
    - `resistance` &mdash; How much of the chance the target shrugs off; `Guaranteed` resistance produces `Zero`.
    - **Returns** &mdash; The surviving probability. Resistances applied one after another are multiplicative, so two 50% resistances leave 25% rather than nothing.

`public static Chance64 Clamp(long raw)`

:   Converts a raw value into the domain by saturating rather than throwing.
    - `raw` &mdash; Raw probability, which may fall outside the domain.
    - **Returns** &mdash; `Zero` for anything at or below zero, `Guaranteed` for anything at or above `Scale`, and the exact value in between. This is the right entry point for a formula that stacks bonuses, where the sum passing 100% is expected.

`public int CompareTo(Chance64 other)`

:   Orders two probabilities by their raw units.
    - `other` &mdash; The probability to compare against.
    - **Returns** &mdash; A negative number, zero, or a positive number as this probability is lower than, equal to, or higher than `other`.

`public bool Equals(Chance64 other)`

:   Compares raw units, so equality is exact rather than approximate.
    - `other` &mdash; The probability to compare against.
    - **Returns** &mdash; True when both carry the same raw value.

`public override bool Equals(object obj)`

:   Compares against an arbitrary object, matching only another probability.
    - `obj` &mdash; The object to compare against.
    - **Returns** &mdash; True when `obj` is a boxed `Chance64` with the same raw value. Prefer the typed overload, which does not box.

`public override int GetHashCode()`

:   Folds the raw units into a hash by combining their two halves.
    - **Returns** &mdash; A deterministic hash code for this value.

`public static Chance64 Multiply(Chance64 left, Chance64 right)`

:   Combines two independent probabilities, as in "hits, and then also crits".
    - `left` &mdash; First probability.
    - `right` &mdash; Second probability.
    - **Returns** &mdash; The product, rounded rather than truncated, which is what stops a chain of multiplications biasing every result downwards. It can never leave the domain, because neither operand can.

`public override string ToString()`

:   Returns the raw units as invariant-culture digits, not a percentage: 50% prints as "500000". It is meant for logs, diagnostics, and canonical text, so format the value yourself for anything a player reads.
    - **Returns** &mdash; The raw probability units as invariant decimal digits, without percentage conversion or locale-dependent formatting.

---

## DeterministicRng

```csharp
public readonly struct DeterministicRng : IEquatable<DeterministicRng>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Numerics/DeterministicRng.cs</small>

The simulation's random source: a 128-bit xorshift-rotate generator over
four 32-bit words, computed with integer arithmetic only, so one seed
yields one sequence on every platform and on every replay.

!!! note "Remarks"
    This is an immutable value rather than an object. Every draw returns the
    advanced generator next to its value, and the caller must keep that
    return - rng = rng.NextBelow(bound, out value) - because drawing again
    from the receiver repeats the same value. The cursor is exposed as an
    `RngState` so a battle can be saved mid-sequence and resumed
    on the exact draw it stopped at.

**Properties**

`public RngState State`

:   The current position in the sequence. Persist it and hand it back to `TryRestore` to continue from here.

**Fields**

`public const uint ZeroSeedNormalization`

:   Seed value substituted when `FromSeed` is given 0.

**Methods**

`public bool Equals(DeterministicRng other)`

:   Compares position, not identity: two equal generators stand on the same draw and will produce the same remaining sequence.
    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value equality against any object; false for other types.
    - `obj` &mdash; The object to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public static DeterministicRng FromSeed(uint seed)`

:   Expands one seed into a full generator state.
    - `seed` &mdash; Any value. Seed 0 is replaced by `ZeroSeedNormalization`; every other seed is expanded as given.
    - **Returns** &mdash; A generator standing at the first draw of that seed's sequence.

`public override int GetHashCode()`

:   A hash over the four state words, so two generators standing on the same draw hash alike. It changes with every draw, which makes a generator unsuitable as a long-lived dictionary key.
    - **Returns** &mdash; A deterministic hash code for this value.

`public DeterministicRng NextBelow(uint exclusiveUpperBound, out uint value)`

:   Takes a value uniformly distributed from 0 inclusive to the bound exclusive. Draws that would skew the result are rejected and retaken, so one call can consume several 32-bit draws.
    - `exclusiveUpperBound` &mdash; Must be greater than zero; a bound of 0 throws `ArgumentOutOfRangeException`.
    - `value` &mdash; The drawn value, below the bound.
    - **Returns** &mdash; The generator advanced past every draw this call consumed.

`public DeterministicRng NextBelow(ulong exclusiveUpperBound, out ulong value)`

:   The 64-bit form of the unbiased draw. A bound that fits in 32 bits consumes exactly what the 32-bit overload would; a larger bound pairs two draws, high word first.
    - `exclusiveUpperBound` &mdash; Must be greater than zero; a bound of 0 throws `ArgumentOutOfRangeException`.
    - `value` &mdash; The drawn value, below the bound.
    - **Returns** &mdash; The generator advanced past every draw this call consumed.

`public DeterministicRng NextUInt32(out uint value)`

:   Takes the next value in the sequence, uniform across the whole 32-bit range.
    - `value` &mdash; The drawn value.
    - **Returns** &mdash; The generator advanced past this draw. Keep it; drawing again from the receiver returns the same value.

`public DeterministicRng SamplePercent(Fixed64 percent, out bool succeeded)`

:   Rolls a percentage chance. A percent at or below zero always fails and a percent at or above one hundred always succeeds; neither case draws, so a certain or impossible roll leaves the sequence exactly where it was.
    - `percent` &mdash; A percentage on `Fixed64`'s scale, where `Fixed64.OneHundredPercent` is 100%. The roll resolves to one ten-thousandth of a percent.
    - `succeeded` &mdash; True when the roll passed.
    - **Returns** &mdash; The generator advanced past the draw, or the receiver unchanged when the outcome was decided without one.

`public static bool TryRestore(RngState restored, out DeterministicRng rng, out Diagnostic diagnostic)`

:   Rebuilds a generator from a previously captured state, resuming the sequence at the draw that state was taken on.
    - `restored` &mdash; A state read earlier from `State`.
    - `rng` &mdash; The resumed generator, or the default value when this returns false.
    - `diagnostic` &mdash; rng.invalid-zero-state when every word is zero - that state is the generator's fixed point and would return 0 forever - and the default diagnostic otherwise.
    - **Returns** &mdash; False when the state is rejected, in which case nothing is restored.

---

## Diagnostic

```csharp
public readonly struct Diagnostic : IEquatable<Diagnostic>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Common/Diagnostic.cs</small>

One reported failure or warning: a stable id plus optional free-text
detail.

The id is the part callers branch on and the part that stays fixed across
versions; the detail exists for logs and inspector messages and is never
parsed. Wording a detail differently therefore cannot break code that
switches on `Id`. The ids the engine core raises are listed on
`DiagnosticIds`; the built-in mechanics raise their own, listed
on `MechanicsDiagnosticIds`.

**Constructors**

`public Diagnostic(StableId id, string detail = null)`

:   Records one diagnostic against a required id.
    - `id` &mdash; The identity callers match on. It must be a valid `StableId`, so a diagnostic can never be raised without something to match.
    - `detail` &mdash; Extra context for a human reader. Null is stored as the empty string, so `Detail` never has to be null-checked.

**Properties**

`public string Detail`

:   Human-readable context such as the offending id or index, or the empty string when none was supplied. Never null, and never meant to be parsed.

`public StableId Id`

:   What went wrong, as a stable id. Always valid on a constructed value, because the constructor rejects an invalid one.

**Methods**

`public bool Equals(Diagnostic other)`

:   Compares id and detail, both ordinally.
    - `other` &mdash; The diagnostic to compare against.
    - **Returns** &mdash; True only when the detail text matches as well, so two reports of the same failure about different content are not equal.

`public override bool Equals(object obj)`

:   Compares against any object, boxed diagnostics included.
    - `obj` &mdash; The value to compare against.
    - **Returns** &mdash; False for null and for anything that is not a diagnostic.

`public override int GetHashCode()`

:   Combines the id and detail hashes, so diagnostics can be collected in a set or dictionary to de-duplicate repeated reports.
    - **Returns** &mdash; A deterministic hash code for this value.

`public override string ToString()`

:   Formats the diagnostic for a log line.
    - **Returns** &mdash; `id: detail`, or just the id when there is no detail. A default value, which only `default(Diagnostic)` can produce, returns the empty string rather than throwing.

---

## Fixed64

:material-star: **Start here**

```csharp
public readonly struct Fixed64 : IEquatable<Fixed64>, IComparable<Fixed64>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Numerics/Fixed64.cs</small>

A signed fixed-point number carrying four decimal places, stored as a
64-bit integer in which 10,000 raw units make 1.0.

Every amount the simulation computes is this type rather than a float,
because integer arithmetic produces the same answer on every CPU and
platform and is therefore reproducible by a replay or a batch run. The
trade is a fixed domain: anything finer than 0.0001 cannot be
represented, arithmetic is checked and throws on overflow instead of
wrapping, and rounding is always half away from zero.

`ToString` prints the raw scaled integer rather than a
decimal, because that text feeds canonical encoding. Use
`BattleNumberFormat` for anything a player reads.

**Constructors**

`public Fixed64(long raw)`

:   Wraps an already-scaled integer. Nothing is scaled here, so `new Fixed64(5)` is 0.0005; use `FromInt32` to turn a whole number into 5.0.
    - `raw` &mdash; The scaled value, in units of one ten-thousandth. Any 64-bit value is accepted, including the extremes that `Abs` and `Negate` cannot handle.

**Properties**

`public long Raw`

:   The underlying scaled integer, 10,000 to the unit. Canonical serialisation, hashing, and comparison all read this value directly, so treat it as the stored form rather than as a number to show.

**Fields**

`public static readonly Fixed64 One`

:   Multiplicative identity representing exactly 1.0000, or `Scale` raw units.

`public static readonly Fixed64 OneHundredPercent`

:   Percentage-domain value representing exactly 100.0000 rather than the fractional ratio 1.0.

`public const long Scale`

:   Raw units per whole unit; four decimal places are represented because one unit is exactly 10,000 raw ticks.

`public static readonly Fixed64 Zero`

:   Additive identity with a raw representation of zero.

`public static bool operator`

:   Returns a new value computed from the operands without mutating either operand; numeric overflow follows the underlying contract.
    - `left` &mdash; First fixed-point value compared by its exact raw representation.
    - `right` &mdash; Second fixed-point value compared by its exact raw representation.
    - **Returns** &mdash; The value produced by applying the operator.

**Methods**

`public static Fixed64 Abs(Fixed64 value)`

:   Returns the magnitude of a value, dropping the sign.
    - `value` &mdash; The value to measure. As with `Negate`, the most negative raw value is refused instead of being returned unchanged, which is what a two's-complement absolute value would otherwise do.
    - **Returns** &mdash; The non-negative magnitude of `value`; the minimum raw value is outside the positive range and throws.

`public static Fixed64 Add(Fixed64 left, Fixed64 right)`

:   Adds two values exactly; no precision is lost and no rounding takes place. The `+` operator forwards here, so operator arithmetic is checked as well: a sum that leaves the raw range throws rather than wrapping into a wrong but plausible number that would then be hashed into a battle event.
    - `left` &mdash; First addend.
    - `right` &mdash; Second addend.
    - **Returns** &mdash; The exact fixed-point sum; raw overflow raises `OverflowException` instead of wrapping.

`public int CompareTo(Fixed64 other)`

:   Orders by the underlying scaled integer, which is the same as numeric order and gives a total, tie-free ordering for sorting.
    - `other` &mdash; Value compared against.
    - **Returns** &mdash; Negative, zero, or positive as this value sorts before, alongside, or after `other`.

`public static Fixed64 Divide(Fixed64 left, Fixed64 right)`

:   Divides one value by another, rounding half away from zero. The dividend is scaled up before the division, so it is the dividend alone that limits the range: above roughly 92 billion in unit terms the operation throws even when the answer would be small. There is no infinity or NaN to fall back on, which is why a zero divisor is an exception rather than a value.
    - `left` &mdash; Dividend.
    - `right` &mdash; Divisor.
    - **Returns** &mdash; The fixed-point quotient rounded half away from zero; a zero divisor or out-of-range scaled dividend throws.

`public bool Equals(Fixed64 other)`

:   Exact equality of the scaled integers. Because every representable value is stored exactly, there is no tolerance to reason about and no equivalent of a float's near-miss.
    - `other` &mdash; Value compared against.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Value comparison against a boxed amount; any other type is never equal.
    - `obj` &mdash; Candidate value, boxed.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public static Fixed64 FromInt32(int value)`

:   Scales a whole number up into fixed point, so 5 arrives as 5.0.
    - `value` &mdash; The whole number to convert. Every 32-bit value stays inside the raw range once scaled, so this conversion cannot overflow.
    - **Returns** &mdash; An exact fixed-point value whose raw field equals `value` multiplied by 10,000.

`public override int GetHashCode()`

:   Folds the two halves of the raw value together; consistent with `Equals(Fixed64)`.
    - **Returns** &mdash; A deterministic hash code for this value.

`public static Fixed64 Multiply(Fixed64 left, Fixed64 right)`

:   Multiplies two values and rescales the product back to four decimal places, rounding half away from zero. The raw factors are multiplied before the rescale, so the headroom is smaller than the type's range suggests: the two operands multiplied together must stay under roughly 92 billion in unit terms, or the intermediate product overflows and throws. Each multiplication rounds on its own, so the order of a chain of them can change the result.
    - `left` &mdash; First factor.
    - `right` &mdash; Second factor.
    - **Returns** &mdash; The rescaled product rounded half away from zero; an out-of-range intermediate product throws.

`public static Fixed64 Negate(Fixed64 value)`

:   Flips the sign, backing the unary `-` operator.
    - `value` &mdash; The value to negate. The most negative raw value has no positive counterpart and therefore cannot be negated.
    - **Returns** &mdash; The same magnitude with its sign reversed; the minimum raw value has no representable result and throws.

`public static Fixed64 ParseInvariant(string text)`

:   Reads a decimal literal such as `12.5` or `-0.0001` written in invariant form, and throws when the text is not one.
    - `text` &mdash; An optional leading minus, at least one digit, and at most four fractional digits. A leading plus, an exponent, a thousands separator, surrounding whitespace, a trailing character, and a fifth fractional digit are all rejected rather than tolerated or rounded, because authored and stored values must mean exactly one number.
    - **Returns** &mdash; The exact value the text denotes; nothing is rounded.

`public static Fixed64 Subtract(Fixed64 left, Fixed64 right)`

:   Subtracts one value from another exactly, backing the `-` operator.
    - `left` &mdash; Value subtracted from.
    - `right` &mdash; Value taken away.
    - **Returns** &mdash; The exact fixed-point difference; raw overflow raises `OverflowException` instead of wrapping.

`public int ToInt32Clamped(int minimum, int maximum)`

:   Rounds as `ToInt64Rounded` does and then confines the result to a 32-bit range. This is how an evaluated amount becomes the whole number the engine actually applies: the clamp is part of the conversion, so a value far outside the range is pulled to the nearest bound instead of throwing or wrapping at the call site.
    - `minimum` &mdash; Lowest value that may be returned. Pass 1 where zero would be a meaningless amount.
    - `maximum` &mdash; Highest value that may be returned.
    - **Returns** &mdash; The nearest whole number using half-away-from-zero rounding, then confined inclusively to `minimum` and `maximum`.

`public long ToInt64Rounded()`

:   Rounds to the nearest whole number, with an exact half going away from zero: 0.5 becomes 1 and -0.5 becomes -1.
    - **Returns** &mdash; The nearest whole value rather than the truncated one, so the result can be larger in magnitude than the fixed-point value it came from.

`public override string ToString()`

:   Writes the raw scaled integer in invariant culture, so 5.0 prints as `50000`. That is deliberate: this text feeds canonical encoding and hashing, and must never shift with a player's locale. It is not player-facing output - use `BattleNumberFormat` for that.
    - **Returns** &mdash; The signed raw integer in invariant decimal form, with no thousands separators or fixed-point decimal point.

`public static bool TryParseInvariant(string text, out Fixed64 result)`

:   Performs the same strict parse as `ParseInvariant` and reports failure instead of throwing, which is what importers and editor fields use while a value is still being typed.
    - `text` &mdash; The candidate literal. Beyond the grammar, a value whose magnitude would leave the raw range fails here rather than overflowing, and a signed zero such as `-0` is refused so that one number has one spelling.
    - `result` &mdash; The parsed value on success, and `Zero` on failure; it is always assigned.
    - **Returns** &mdash; True only when the whole string was consumed as an exact value.

---

## FrozenList

```csharp
public sealed class FrozenList
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Common/FrozenList.cs</small>

A list that copies what it is given once and then offers no way to change
it, used throughout compiled content, snapshots, and events wherever a
collection crosses a public boundary.

Because the copy happens on the way in and every read hands back either an
element or a fresh array, a caller can hold on to one of these without
being able to disturb the simulation, and the engine can share a single
instance between the snapshot, the serializer, and the presentation layer
rather than copying defensively at each hop.

**Constructors**

`public FrozenList(IEnumerable<T> source)`

:   Copies a sequence into a new list. The sequence is read once and never referenced again, so a later change to the source leaves this list alone.
    - `source` &mdash; The elements to copy; an empty sequence is legal.

`public FrozenList(params T[] source)`

:   Copies an array, or a comma-separated run of elements, into a new list. The array is cloned rather than adopted, so writing to it afterwards cannot reach inside this list.
    - `source` &mdash; The elements to copy; passing no arguments gives an empty list.

**Properties**

`public int Count`

:   How many elements the list holds; fixed once it is built.

`public static FrozenList<T> Empty`

:   The shared empty list, so a record with nothing in it costs no allocation.

**Methods**

`public IEnumerator<T> GetEnumerator()`

:   Walks the elements in the order they were copied in. Nothing can change the list underneath, so an enumeration can never be invalidated part way through.
    - **Returns** &mdash; An enumerator over the fixed membership in original copy order; it never observes later source-collection changes.

`public T[] ToArray()`

:   Copies the elements into a new array the caller owns outright.
    - **Returns** &mdash; A fresh array each call, so writing to it cannot reach back into the list - which is what makes it safe to hand to an API that expects a mutable array.

---

## Sha256Digest

```csharp
public readonly struct Sha256Digest : IEquatable<Sha256Digest>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Canonical/Sha256Digest.cs</small>

An immutable 32-byte SHA-256 digest, used to fingerprint a canonical
record so two runs can be compared for divergence. The default value is
not a digest: `IsValid` is false for it, it stringifies to
the empty string, and it compares equal only to another default.
Equality inspects all 32 bytes rather than exiting at the first
difference.

**Properties**

`public bool IsValid`

:   False only for the default value, which carries no digest.

**Fields**

`public const int ByteLength`

:   The digest length in bytes. Hex text must be exactly twice this long to parse.

`public static bool operator`

:   Returns a new value computed from the operands without mutating either operand; numeric overflow follows the underlying contract.
    - `left` &mdash; The digest on the left side of the equality comparison.
    - `right` &mdash; The digest on the right side of the equality comparison.
    - **Returns** &mdash; The value produced by applying the operator.

**Methods**

`public static Sha256Digest Compute(byte[] data)`

:   Hashes a canonical byte record with SHA-256.
    - `data` &mdash; The exact bytes to hash; not copied or modified.
    - **Returns** &mdash; The digest of `data`, always valid.

`public bool Equals(Sha256Digest other)`

:   Compares two digests byte for byte. Every byte is inspected, so the running time does not reveal where two digests first differ. Two default values are equal; a default never equals a real digest.
    - `other` &mdash; The value to compare with this instance.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public override bool Equals(object obj)`

:   Defers to `Equals(Sha256Digest)` when `obj` is a digest. Anything else, null included, is unequal.
    - `obj` &mdash; The candidate to compare with; a boxed digest is unboxed, anything else fails.
    - **Returns** &mdash; True when the supplied value is equal to this value; otherwise false.

`public static Sha256Digest FromBytes(byte[] source)`

:   Adopts a digest that was computed or stored elsewhere. The array is copied, so later writes to the caller's buffer cannot change this value.
    - `source` &mdash; Exactly 32 digest bytes; anything else throws.
    - **Returns** &mdash; A valid digest owning a defensive copy of the 32 input bytes.

`public override int GetHashCode()`

:   Derives a hash from the first four digest bytes, which is enough because the bytes of a SHA-256 value are already uniformly distributed. The default value hashes to zero. Two digests that agree on those four bytes share a bucket and are then separated by `Equals(Sha256Digest)`, which reads all 32.
    - **Returns** &mdash; A deterministic hash code for this value.

`public byte[] ToByteArray()`

:   Copies the 32 bytes out. The caller owns the returned array, so mutating it cannot corrupt this digest. Throws for the default value.
    - **Returns** &mdash; A new array containing the digest's 32 bytes.

`public override string ToString()`

:   Renders the digest as 64 lowercase hex characters, the exact form `TryParse` reads back. The default value renders as the empty string rather than 64 zeros, so an absent digest stays distinguishable from the digest of all-zero bytes.
    - **Returns** &mdash; Sixty-four lowercase hexadecimal characters, or an empty string for the default digest.

`public static bool TryParse(string text, out Sha256Digest digest)`

:   Reads back the form `ToString` produces. Parsing is strict: exactly 64 characters, and lowercase hex only, so uppercase text from another tool is rejected rather than silently accepted.
    - `text` &mdash; The candidate 64-character lowercase hex string.
    - `digest` &mdash; The parsed digest, or the default value on failure.
    - **Returns** &mdash; True when the text was a well-formed digest.

---

## StableId

:material-star: **Start here**

```csharp
public readonly struct StableId : IEquatable<StableId>, IComparable<StableId>
```

`TurnGauge.Simulation` &middot; <small>Runtime/Simulation/Common/StableId.cs</small>

The identifier every piece of content, state, and event in the simulation is
named by: 1 to 128 characters drawn from a-z, 0-9, and the three punctuation
characters '.', '_' and '-'.

The text is the identity, so nothing here normalises, trims, or lowercases
what you hand in; "Fireball" is rejected rather than repaired, which is what
stops two spellings of one name compiling into two different things.
Comparison and ordering are ordinal rather than cultural, so ids sort the
same way on every machine and in every locale, and that ordering is what
canonical encoding and hashing depend on. The default value of the struct
carries no text and is not a usable id; see `IsValid`.

**Constructors**

`public StableId(string value)`

:   Wraps identifier text that already satisfies the grammar.
    - `value` &mdash; The identifier text.

**Properties**

`public bool IsValid`

:   Whether this instance carries identifier text. It is false only for the default value, since no other instance can be constructed without valid text, so in practice this answers "was this id ever assigned".

`public string Value`

:   The identifier text, exactly as it was supplied.

**Fields**

`public const int MaximumLength`

:   Maximum accepted identifier length in ASCII characters, limiting serialized keys and lookup work to 128.

`public static bool operator`

:   Returns a new value computed from the operands without mutating either operand; numeric overflow follows the underlying contract.
    - `left` &mdash; First identifier compared by exact ordinal text, including the default invalid value.
    - `right` &mdash; Second identifier compared by exact ordinal text, including the default invalid value.
    - **Returns** &mdash; The value produced by applying the operator.

**Methods**

`public int CompareTo(StableId other)`

:   Orders two identifiers by ordinal comparison of their text, sorting the default value before every valid id.
    - `other` &mdash; The identifier to compare against.
    - **Returns** &mdash; A negative number, zero, or a positive number as this identifier sorts before, alongside, or after `other`. Ordering is by character code and never by culture, so a sorted list of ids reads the same on every machine.

`public bool Equals(StableId other)`

:   Compares identifier text ordinally, so equality is exact and case-sensitive.
    - `other` &mdash; The identifier to compare against.
    - **Returns** &mdash; True when both carry the same text, or when both are the default value.

`public override bool Equals(object obj)`

:   Compares against an arbitrary object, matching only another identifier.
    - `obj` &mdash; The object to compare against.
    - **Returns** &mdash; True when `obj` is a boxed `StableId` carrying the same text. Prefer the typed overload, which does not box.

`public override int GetHashCode()`

:   Returns an FNV-1a hash of the identifier text, and zero for the default value. The hash is computed here rather than delegated to `string.GetHashCode`, whose result the runtime is free to vary between processes. Anything keyed by an id therefore lands in the same bucket in every run and on every machine, which keeps the behaviour of hash-ordered structures reproducible alongside the rest of the simulation.
    - **Returns** &mdash; A deterministic hash code for this value.

`public static bool IsValidText(string text)`

:   Reports whether text would be accepted as an identifier, without building one. Use it to validate imported or authored data in bulk, or to drive the error state of an editor field as it is typed.
    - `text` &mdash; Candidate text; null and empty both fail.
    - **Returns** &mdash; True when the text is 1 to `MaximumLength` characters long and every character is a-z, 0-9, '.', '_' or '-'. Uppercase letters, spaces, and non-ASCII characters all fail.

`public override string ToString()`

:   Returns the identifier text, or an empty string for the default value. Unlike `Value` it never throws, which is what makes it the safe choice inside a log line or an exception message.
    - **Returns** &mdash; The exact identifier text, or an empty string for the invalid default struct value; this conversion never throws.

`public static bool TryParse(string text, out StableId id)`

:   Converts identifier text without throwing when it is rejected.
    - `text` &mdash; Candidate text; null is allowed and fails.
    - `id` &mdash; The identifier on success, otherwise the default value, which is not usable.
    - **Returns** &mdash; True when `text` satisfies the grammar.

---

