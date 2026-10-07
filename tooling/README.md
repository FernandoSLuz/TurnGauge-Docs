# Documentation capture tooling

Two capture paths, because Unity has two very different rendering surfaces.

## 1. Scene, map, and interface content -- reliable and headless

`DocsCapture.BattleSkinGallery` (TurnGauge-ImportHost) renders through a throwaway
camera into a `RenderTexture`.

```bash
DOCS_IMAGE_DIR=<docs>/docs/assets/images \
Unity.exe -batchmode -quit -projectPath <ImportHost> \
  -executeMethod DocsCapture.MapStyleGallery.CaptureAll
```

Notes learned the hard way:

- **Do not pass `-nographics`.** There is no GPU, so `camera.Render()` produces a
  uniformly blank image and every style comes out byte-identical.
- Capture at the skin's or style's **reference resolution** (1920x1080). At smaller
  logical sizes, regions anchored to different corners overlap.
- Surfaces sized by a content-size fitter have a **zero rect** until a layout pass
  runs. Force layout, then re-apply each surface, or the shader receives a zero
  half-extent and draws nothing.

## 2. Editor windows -- needs a GUI session, and it works

`EditorWindowShots` (in each ImportHost) plus `Capture-EditorWindows.ps1`.

```powershell
Capture-EditorWindows.ps1 `
  -ProjectPath <ImportHost> -UnityExe <Unity.exe> -OutDir <docs>/docs/assets/images `
  -Targets @('BattleWorkbenchWindow|editor-workbench|1300|860|workbench')
```

A target is `TypeName|file-stem|width|height|fixture`, everything after the stem optional.
Sizes are in **logical points**; the PNG comes out at points times the display scale.

### The exact shipped set

Recorded because it was not, and the eight images below then shipped cropped for weeks
with nobody able to reproduce the run that made them.

TurnGauge-ImportHost:

```
BattleWorkbenchWindow|editor-workbench|1300|860|workbench
ContentValidatorWindow|editor-content-validator|1120|300|validator
FormationEditorWindow|editor-formation-editor|1200|800|formation
BattleSkinBrowserWindow|editor-skin-browser|1180|620
BattleTemplateBrowserWindow|editor-battle-template-browser|1200|910
```

Heights are chosen so the window is filled rather than trailing dead space, which is a
judgement about each panel's content and has to be re-made if that content changes. The
Content Validator is the short one on purpose: with a valid catalog it draws a toolbar
and one verdict line, so a tall window is nine-tenths void.

### Display scaling silently cropped every one of these

**The failure.** PowerShell is DPI-unaware by default, so Windows virtualises what it is
told: `GetWindowRect` returns **logical points** while `PrintWindow` renders the window at
its true **physical pixel** size. The capture sized its bitmap from the first and filled it
with the second, so on this machine's 150% display a 1180-point window produced a 1193-pixel
bitmap holding the top-left two-thirds of a window that had rendered 1790 pixels wide.

**Why nobody saw it.** A cropped window is not a broken image. It is a plausible-looking
panel that happens to be missing its right-hand side, and `MinContentRatio` -- the only
check there was -- scores a crop as perfectly healthy. `editor-skin-browser.png` shipped
with "Apply to interfaces in open scen" cut mid-word.

**The fix** is not arithmetic on the scale factor: it is to stop being lied to.
`WindowCaptureLib.ps1` calls `SetProcessDpiAwarenessContext(PER_MONITOR_AWARE_V2)` at
dot-source time, before any window is measured. `GetWindowRect` then returns physical
pixels, the bitmap matches what `PrintWindow` draws, and no scaling correction is needed
anywhere. Both capture scripts report the awareness they achieved on the first line of
output; if it ever says `UNAWARE`, every image from that run is cropped.

**Output sizes are therefore machine-dependent**: 1300 points is 1950 pixels at 150% and
1300 at 100%. Same content, more pixels. That is the intended behaviour, not drift.

### Two checks, because the obvious one is not sufficient

`ExpectPoints{Width,Height}` is the real guard and it is arithmetic, not judgement: a
window of *W* points at scale *S* renders *W x S* pixels, so a smaller bitmap is a
photograph of part of it. The driver passes the size Unity itself reports, so the check
needs no agreement about frame or title-bar thickness.

`MaxEdgeBusy` is a backstop for crops from any other cause: the outermost row and column
of a whole window are its frame, which is a near-constant line, while a cut through the
middle of one is not. It is a backstop and not the guard because **it is not sufficient
on its own** -- measured against the eight images that actually shipped cropped, it scored
`editor-workbench` at 0.040 and `editor-content-validator` at 0.037 against 0.023 for a
correct capture, because both crops happened to land in an empty panel. It would have
passed two of the very images it was proposed to catch. The eight correct re-shoots all
score 0.000.

Comparing edge pixels for *equality* does not work either: DWM and PNG round-tripping put
three shades of `(243,243,24x)` along one title-bar line, which reads as 57% "content".
The comparison is against the line's median with a tolerance.

### How it is triggered

Not by `-executeMethod`. A domain-load hook in the editor watches for a request file and
drives the run from `EditorApplication.update`, with progress in `SessionState` so a domain
reload resumes rather than restarts. The handshake is files, not pipes: `request.json` ->
`ready.json` -> `done-N.marker` -> `finished.marker`.

Each panel is opened through **its own static opener** -- the method behind its Tools menu
item -- so the shot matches what a user sees and the window keeps the title it sets for
itself. It is then floated at an explicit size and photographed as its own top-level OS
window: no cropping, no surrounding editor chrome, and the same size on every run whatever
editor layout is saved.

### Fixtures matter more than the capture

A freshly opened Workbench has no catalog assigned and photographs as an empty shell with
every button disabled -- honest and useless. `EditorWindowFixtures` assigns the shipped
starter content through `SerializedObject`, which is the supported way to reach a
`[SerializeField] private` field, then runs the window's own action. The Workbench shot
shows a compiled session with its state chain hash; without the fixture it shows nothing.

### Why PrintWindow and not a screen read

`InternalEditorUtility.ReadScreenPixel` reads the **literal screen**. An automated run on a
machine in use captured a web browser that happened to overlap the Unity window, and nothing
in the Editor could detect it. A window title on a developer machine can also contain a
credential.

`PrintWindow` with `PW_RENDERFULLCONTENT` asks the window to render itself, so the result is
that window's content even when covered. Window enumeration is filtered by process id
**first**, so this can never reach another application's window.

### Two false conclusions recorded here previously

Both were wrong, and both were symptoms of one bug. `Start-Process -ArgumentList` joins its
elements **without quoting**, so a project path containing a space arrived at Unity as two
arguments. Unity logged `Couldn't set project path`, changed to the truncated string, opened
nothing, and exited 0.

- *"`-executeMethod` never fires in a GUI session."* It was never reached. Quote the path.
- *"`EnumWindows` returns nothing from a restricted shell."* It returns 17 windows here.
  There was no Unity window to find.

The lesson generalises: when a launcher reports success and the child did nothing, read the
child's own log before concluding anything about the API.

### Known limitations

- `MinContentRatio` rejects a blank capture. Treat a non-zero exit as "no screenshot", never
  as "good enough".
- A fixture that fails logs and continues, so a sparse shot is possible. Check the content
  ratio in the output: a value near 0.1 usually means the panel had nothing to draw.

## 3. The API reference surface

`extract_docs.py` reads the source, `generate_api.py` renders it. The third input is a
**tiers** file (`tooling/api-tiers.json`):

```bash
python tooling/extract_docs.py <package>/Assets api.json
python tooling/generate_api.py api.json tooling/api-groups.json docs/reference TurnGauge tooling/api-tiers.json
```

The extractor excludes `OptionalDemos` by source path. Those optional demonstration modules are staged independently and are not part of the base TurnGauge API reference.

Listing every public type lists the wrong things. Most of a Unity package's public surface is
public only because `internal` is per-assembly and the package spans several assemblies. The
tiers file separates that plumbing from the API:

| Tier | Effect |
| --- | --- |
| `headline` | Listed first under **Start here**, and badged on its page |
| `extensionPoints` | Badged as something a buyer implements themselves |
| `hidden` | Left out of the reference; carries `[EditorBrowsable(Never)]` in source |
| `internal` | No longer public at all |

### Three things about the `hidden` stamping

**It is complete in both directions.** Every `hidden` type carries the attribute and no
published type does. That is worth re-checking after any tier change, because the two halves
drift independently: a type promoted out of `hidden` keeps its attribute unless someone removes
it, and the reference will happily publish a type it has told the compiler to hide.

**Do not put `TurnGauge.InternalTools` types in the tiers at all.** `extract_docs.py` excludes
that directory by path, so those types are never extracted, never published, and stamping them
achieves nothing. Four had accumulated in `hidden` and were removed.

**Use the fully qualified attribute where `Component` is in scope.** Adding
`using System.ComponentModel;` to a file that also uses `UnityEngine.Component` makes the name
ambiguous and fails the build (CS0104). Those files carry
`[System.ComponentModel.EditorBrowsable(...)]` instead. The same hazard applies to `Container`,
`IContainer`, `ISite`, `License` and `TypeConverter`.

Worth remembering what this buys, which is less than it looks: Roslyn ignores `EditorBrowsable`
for source in the same solution, and an Asset Store package normally ships as source. So the
attribute documents intent and would work if the package ever shipped as DLLs, but the thing
actually keeping the surface small for a buyer is the reference exclusion, driven by the tiers
file.

The index states how many types are excluded and why, and coverage is measured over the
**published** surface. A reference that hides its own omissions is worse than one that admits
them.

### Regenerating the tiers

The tiers were decided by reading every type and, for each proposed removal, having a second
pass try to refute it. That refutation is the valuable part: of 258 types that looked
single-assembly and unreferenced, only **6** could actually be made `internal`. The rest
failed on one of two things worth remembering:

- TurnGauge has no blanket friend assembly for its public surface, so test usage of a
  type can block making that type internal.
- Inconsistent accessibility cascades. Internalising a type that appears in a still-public
  signature is CS0050/CS0051/CS0053, and internalising its container in turn breaks the tests
  that use *that*.

So `hidden` is where nearly everything lands, and that is the honest answer rather than a
compromise.
