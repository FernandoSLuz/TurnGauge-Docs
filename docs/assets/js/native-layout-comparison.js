/*
 * Native HUD comparison controls.
 *
 * The files are still captures, not a live Unity preview. Keep this small and
 * dependency-free so the page remains useful when scripts are unavailable.
 */
(function () {
  'use strict';

  function setup() {
    var root = document.querySelector('[data-native-layout-comparison]');
    if (!root || root.dataset.bound === '1') {
      return;
    }
    root.dataset.bound = '1';

    var state = root.querySelector('[data-native-layout-state]');
    var identity = root.querySelector('[data-native-layout-identity]');
    var backend = root.querySelector('[data-native-layout-backend]');
    var aspect = root.querySelector('[data-native-layout-aspect]');
    var image = root.querySelector('[data-native-layout-image]');
    var fullSize = root.querySelector('[data-native-layout-full]');
    var caption = root.querySelector('[data-native-layout-caption]');
    var status = root.querySelector('[data-native-layout-status]');
    var controls = root.querySelector('[data-native-layout-controls]');

    if (!state || !identity || !backend || !aspect || !image || !fullSize || !caption || !status || !controls) {
      return;
    }

    // Resolve captures from the page's stable default image. This survives
    // navigation.instant swaps, where document.baseURI may still be the page
    // that was shown before this comparison page.
    var imageRoot = new URL('.', image.src).href;

    state.value = 'initial-action';
    identity.value = 'Fantasy';
    backend.value = 'UGUI';
    aspect.value = '1920_1080';
    controls.hidden = false;
    controls.disabled = false;

    function update() {
      var stateName = state.options[state.selectedIndex].textContent;
      var identityName = identity.options[identity.selectedIndex].textContent;
      var backendName = backend.options[backend.selectedIndex].textContent;
      var aspectName = aspect.options[aspect.selectedIndex].textContent;
      // Values identify files; labels may change for typography or localization.
      var filename = state.value + '-' + identity.value + '-' + backend.value + '-' + aspect.value + '.png';
      var path = new URL(filename, imageRoot).href;

      image.src = path;
      fullSize.href = path;
      image.alt = identityName + ' ' + backendName + ' native HUD capture at ' + stateName.toLowerCase() + ', ' + aspectName + '.';
      caption.innerHTML = 'Still capture from a Unity 6.3 session: ' + stateName.toLowerCase() + ' / ' + identityName + ' / ' + backendName + ' / ' + aspectName + '. Motion is not demonstrated by this image. <a href="' + path + '">Open full-size capture.</a>';
      status.textContent = 'Selected ' + stateName.toLowerCase() + ', ' + identityName + ', ' + backendName + ', ' + aspectName + '.';
    }

    [state, identity, backend, aspect].forEach(function (control) {
      control.addEventListener('change', update);
    });
    image.addEventListener('error', function () {
      status.textContent = 'The selected capture is not present in this checkout yet: ' + image.getAttribute('src');
    });
    update();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(setup);
  }
})();
