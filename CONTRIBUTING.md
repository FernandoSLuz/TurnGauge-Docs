# Updating these docs

This site is the documentation a buyer learns from. It is written for a designer who does
not read C#, and for a teenager who follows tutorials by looking at the pictures. Both of
those readers are the point, not a nice-to-have.

## Where things live

```
docs/
  index.md
  tutorials/     numbered, start to finish, a picture under every step
  how-to/        one task, assumes the reader already has a map
  explanation/   why it works this way; no steps
  reference/     GENERATED. Do not hand-edit. See "The API reference" below.
  assets/images/ every PNG the site embeds
mkdocs.yml       nav, theme, and the validation settings that make --strict mean something
tooling/         a vendored copy of the shared capture and reference generators
```

The Diataxis split is load-bearing. A tutorial that stops to explain a design decision loses
the reader it was written for; put the decision in `explanation/` and link to it.

There is a second documentation set inside the package itself, at
`Assets/TurnGauge/Documentation/*.md`. That one ships offline and is reference-shaped: API
catalogue, field reference, compatibility, troubleshooting. It links out here for the
illustrated walkthroughs. Do not duplicate tutorials into it, and do not move tutorials out
of here. `../DOCUMENTATION-HOME.md` in the AssetStore working tree records why.

## Publishing

Push to `rename/turngauge`. The workflow runs `mkdocs build --strict` and only deploys if it passes, so a
broken internal link or a missing image cannot reach the published site. Check it locally
first:

```bash
python -m mkdocs build --strict
```

`mkdocs.yml` promotes nav and link problems from INFO to WARNING on purpose. Without that,
`--strict` would happily pass a page dropped from the nav or a dead `#anchor`.

## Rules that will bite you

**ASCII only, in this repo and in the package.** The package's documentation gate test fails
the Unity build on a single non-ASCII byte, because Windows PowerShell and offline viewers
misdecode UTF-8. No em dashes, no smart quotes, no arrows. Write `-`, `'`, `"`, `->`.

**Never claim support you do not have evidence for.** Unity 2022.3.62f1 is the only verified
editor and Built-in the only verified pipeline. Everything else is pending, not assumed. A
page that says "2022.3 or newer" or "URP and HDRP work" is a defect, and one shipped that way
for weeks.

**Never tell a reader to write C# for something the editor does.** If a how-to says "call
`MapTraversalController.Initialize`", check whether `BattleRuntimeController` now does it. This
is the single most common way these pages go stale.

**Never make a designer type a registry key.** An implementation ID like
`effect.adjust-scheduler.v1` and a scheduler ID like `scheduler.atb.v1` are looked up in a
registry, so the editor already knows the legal set and offers it as a dropdown. A page that
instructs the reader to type one is describing a version of the product that had no picker.

**Say which turn model a page assumes.** Action Order effects adjust ready ticks and ATB
effects adjust a gauge; the two are mutually exclusive, and a catalog authored for one cannot
build an engine for the other. This is the sharpest edge in the product. The content compiler
now reports a mismatch as an authoring error naming both assets, but a page that shows an
effect without saying which family it belongs to will still mislead.

**Keep the working-name note.** `TurnGauge` is a working name pending legal, store and domain
clearance. Do not quietly drop the note from a page you are rewriting.

## Pictures

Screenshots are the reason this site exists in the shape it does, so they have their own
pipeline. Full detail is in `tooling/README.md`; this is the short version.

### Before anything: sync the ImportHost

`TurnGauge-ImportHost` holds a **byte-for-byte copy** of `Assets/TurnGauge`, not a
symlink. A change you made in the product is invisible to a capture run until it is mirrored,
which is how a fix can appear not to work when it was simply never copied.

```powershell
TurnGauge/Internal/Release/Sync-TurnGaugeImportHost.ps1          # mirror
TurnGauge/Internal/Release/Sync-TurnGaugeImportHost.ps1 -VerifyOnly   # check only
```

It must report `missing=0 extra=0 mismatch=0`. Do not hand-copy files: that leaves `.meta`
GUID drift that fails the release audit later.

### Maps, styles, and rendered content: headless, reproducible

```bash
DOCS_IMAGE_DIR=<this repo>/docs/assets/images \
DOCS_DOC_IMAGE_DIR=<product>/Assets/TurnGauge/Documentation/Images \
Unity.exe -batchmode -quit -projectPath <TurnGauge-ImportHost> \
  -executeMethod DocsCapture.BattleDocSet.CaptureAll
```

`DOCS_DOC_IMAGE_DIR` is optional. When set, the pictures the offline documentation embeds are
copied into the package and `Images/manifest.json` is rewritten with per-image hashes.

**Do not pass `-nographics`.** With no GPU every render comes back a byte-identical blank
image and the whole run looks like it worked.

Capture at the style's reference resolution, 1920x1080. At smaller logical sizes, regions
anchored to different corners overlap. A surface sized by a `ContentSizeFitter` has a zero
rect until a layout pass runs, so force layout and re-apply every surface, or the shader gets
a zero half-extent and draws nothing.

If the subject is portrait-shaped, give the shot a `Crop`. Fitting a tall map into a 16:9
frame is arithmetically correct and produces an image that is two-thirds black.

### Editor windows: needs a real GUI session, and it works

```powershell
tooling/Capture-EditorWindows.ps1 `
  -ProjectPath <TurnGauge-ImportHost> -UnityExe <Unity.exe> `
  -OutDir <this repo>/docs/assets/images `
  -Targets @('BattleWorkbenchWindow|editor-workbench|1300|860|workbench')
```

A target is `TypeName|file-stem|width|height|fixture`. Sizes are logical points; the PNG comes
out at points times the display scale, so output size is machine-dependent by design.

Two things this pipeline learned the hard way and still guards:

- The first line of output reports the DPI awareness it achieved. If it ever says `UNAWARE`,
  **every image in that run is cropped** and must be discarded. PowerShell is DPI-unaware by
  default, and eight images shipped for weeks with their right-hand third missing before
  anyone noticed, because a cropped window looks like a window.
- A freshly opened window has no content assigned and photographs as an empty shell with every
  button greyed out: honest and useless. `EditorWindowFixtures` assigns shipped content first.
  A content ratio near 0.1 in the output means the panel had nothing to draw.

### Interface shots need the second test command

The package's suite takes **two** commands, and the second one is what proves anything draws:

```bash
Unity.exe -batchmode -nographics -projectPath <TurnGauge> -runTests -testPlatform EditMode ...
Unity.exe -batchmode -projectPath <TurnGauge> -runTests -testPlatform EditMode \
  -testFilter TurnGauge.Tests.EditMode.WidgetRenderCoverageTests ...
```

The second omits `-nographics` deliberately. Those tests render each widget into a
`RenderTexture` and assert a non-background pixel came out; with no graphics device they
**skip themselves** rather than fail, so the headless run alone reports success while the only
guard against shipping an invisible interface never executed. A run showing `skipped=13`
instead of `skipped=4` has not checked that anything draws. The bug this guards against -- a
surface built without a `CanvasRenderer`, so the entire battle interface produced no draw call
-- passed 1,110 data-asserting tests without a murmur.

### Then look at the picture

Open every new PNG and look at it. The render pipeline's own checks catch a blank image and a
crop; they do not catch a legible image that shows the wrong thing, is badly framed, or
photographs a button whose label changed. Five shipped presentation defects on this product
were found this way while more than a thousand assertions passed.

### Then check both directions

```bash
python - <<'EOF'
# every referenced image exists, and every existing image is referenced
EOF
```

A referenced-but-missing image fails `--strict`. An existing-but-unreferenced image is almost
always a section someone left un-illustrated, or a capture that was superseded and should be
deleted rather than left around to be reused by mistake.

## The API reference

`docs/reference/` is generated. Editing it by hand is wasted work.

```bash
python tooling/extract_docs.py <product>/Assets api.json
python tooling/generate_api.py api.json tooling/api-groups.json docs/reference TurnGauge tooling/api-tiers.json
```

Read `generate_api.py` for the exact argument order before running it.

`api-tiers.json` is the gate that decides what the reference publishes -- **not** the
`[EditorBrowsable]` attributes in the source. Update it *before* regenerating:

| Tier | Effect |
| --- | --- |
| `headline` | Listed first under **Start here**, and badged on its page |
| `extensionPoints` | Badged as something a buyer implements themselves |
| `hidden` | Left out of the reference entirely |
| `internal` | No longer public at all |

Most of a Unity package's public surface is public only because `internal` is per-assembly.
Listing all of it lists the wrong things. `BattleRuntimeController` belongs in `headline`: it is
the first type a designer meets, and it spent a release filed as an ordinary type where nobody
would find it.

The tiers file and the source attributes drift independently, so after any tier change check
that every `hidden` type still carries `[EditorBrowsable(Never)]` and no published type does.

## Gates in the package that fail when the docs fall behind

These live in the Unity test suite, not here, and they will fail the product build:

- `DocumentationGateTests.RuntimeFacadeReferenceNamesEveryExportedTypeAndMember` requires
  every exported type and public member of the `TurnGauge.Runtime` assembly to be named in
  `Assets/TurnGauge/Documentation/Runtime-Facade-API.md`. Add a public property to
  `BattleRuntimeController` and this goes red until you write it down. That is deliberate: the
  facade is the buyer-facing contract, and an undocumented member is one they have to infer.
- `DocumentationGateTests.OfflineDocumentationSetIsCompleteAsciiAndFreeOfMojibake` fails on a
  single non-ASCII byte anywhere in the package documentation set.
- `DocumentationGateTests` also refuses a `Compatibility-and-Release.md` that claims Unity 6
  support. Widening the supported range is an owner-approved release task, not a doc edit.

Adding public API without documenting it is what these catch. That is the intended workflow,
not an obstacle to route around.
