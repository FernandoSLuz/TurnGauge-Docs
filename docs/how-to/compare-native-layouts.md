# Compare native HUD layouts

Use this page to compare the two native HUD backends at the same decision state, identity and
screen shape. The comparison is a set of still captures from Unity 6.3 sessions. It is useful
for checking hierarchy, reading order, safe spacing and the location of the decision controls.

These current reference presets were captured in Unity 6000.3.25f1 with three combatants on
each side. Fantasy uses side information cards; science fiction keeps its existing stage
composition. The captures cover action choice and a selected target at both screen shapes.
They demonstrate native rendering and the same authoritative command result across backends.
The association between cards and bodies, science-fiction staging, larger formations and
continuous motion still need their own review; these stills do not approve those aspects.


<div class="native-layout-comparison" data-native-layout-comparison>
  <fieldset class="native-layout-comparison__controls" data-native-layout-controls disabled hidden>
    <legend>Native HUD comparison filters</legend>
    <label>Identity
      <select data-native-layout-identity aria-label="Choose the example identity">
        <option value="Fantasy">Fantasy</option>
        <option value="ScienceFiction">Science fiction</option>
      </select>
    </label>
    <label>Backend
      <select data-native-layout-backend aria-label="Choose the native UI backend">
        <option value="UGUI">UGUI</option>
        <option value="UIToolkit">UI Toolkit</option>
      </select>
    </label>
    <label>Screen shape
      <select data-native-layout-aspect aria-label="Choose the capture aspect">
        <option value="1920_1080">16:9 (1920 × 1080)</option>
        <option value="1920_1200">16:10 (1920 × 1200)</option>
      </select>
    </label>
    <label>Decision state
      <select data-native-layout-state aria-label="Choose the decision state">
        <option value="initial-action">Initial action</option>
        <option value="selected-target">Selected target</option>
      </select>
    </label>
  </fieldset>
  <figure class="native-layout-comparison__figure">
    <a data-native-layout-full href="../../assets/images/native-profiles/initial-action-Fantasy-UGUI-1920_1080.png">
      <img class="off-glb" data-native-layout-image
        src="../../assets/images/native-profiles/initial-action-Fantasy-UGUI-1920_1080.png"
        alt="Fantasy UGUI native HUD capture at initial action, 16:9 (1920 × 1080)">
    </a>
    <figcaption class="native-layout-comparison__caption" data-native-layout-caption>
      Still capture from a Unity 6.3 session: initial action · Fantasy · UGUI · 16:9 (1920 × 1080).
      Motion is not demonstrated by this image. Open full-size capture.
    </figcaption>
  </figure>
  <p class="native-layout-comparison__status" data-native-layout-status aria-live="polite">
    Selected initial action, Fantasy, UGUI, 16:9 (1920 × 1080).
  </p>
</div>


The screen is read from the player's point of view. The roster and turn timeline establish who
is acting and what is coming next; the stage keeps the combatants readable; the skill tray and
feedback area reserve a clear place for the next decision and its result. Compare captures at the
same aspect before judging density: a 16:10 frame has more vertical room, so it should not be
read as evidence that the 16:9 layout is missing content.

## How to use the comparison

1. Choose a decision state, identity and backend, then choose the screen shape that matches your target window.
2. Check the first read: can you find the active combatant, the next turn, the available action,
   and the result of the last action without hunting across the screen?
3. Check the second read: do labels, bars, status marks and button states remain legible at the
   same distance and contrast?
4. Record the choice in the profile you are editing. The capture is evidence for a layout choice,
   not a replacement for trying the battle in your own window.

Still images expose the decision state because that is what the frame proves. Full-motion and
reduced-motion are separate clip variants: when clips are supplied, expose both variants and label
the clip links explicitly; do not infer motion from a still.

For the meaning of each region, see [What each interface region draws](interface-regions.md).
For screen fitting and safe-area placement, see [Fit the battle to your screen](interface-layout.md).
For a native authoring preview, follow [Explore Combat Studio](../tutorials/combat-studio.md),
then use **Apply** to keep a profile or **Discard** to drop the draft. Those actions change the
authoring profile; this comparison page only changes its selected capture.

## If a capture is unavailable

The image paths are intentionally explicit so a missing capture is visible during documentation
review. A missing file means that combination has not been supplied to this checkout; it is not a
claim that the backend, aspect, or motion behavior is unsupported. The default image remains a
plain reference to the 16:9 Fantasy UGUI capture when JavaScript is disabled. The filters are
available when JavaScript is enabled; otherwise, the default capture remains visible.
