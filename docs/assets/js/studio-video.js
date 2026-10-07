(function () {
  "use strict";

  var controllers = new WeakMap();
  var playingVideo = null;

  function controlsFor(attribute, video, callback) {
    document.querySelectorAll("[" + attribute + "]").forEach(function (element) {
      if (element.getAttribute(attribute) === video.id) callback(element);
    });
  }

  function controllerFor(video) {
    if (controllers.has(video)) return controllers.get(video);
    var state = { step: null };

    state.status = function (message) {
      controlsFor("data-studio-status", video, function (element) {
        element.textContent = message;
      });
    };

    state.refresh = function () {
      var atStartOrEnd = video.currentTime <= 0 || video.ended ||
        (Number.isFinite(video.duration) && video.currentTime >= video.duration - 0.1);
      controlsFor("data-studio-continue", video, function (button) {
        button.textContent = !video.paused ? "Pause" :
          atStartOrEnd ? "Play full tutorial" : "Continue full tutorial";
      });
    };

    state.play = function () {
      var playback = video.play();
      if (playback && typeof playback.catch === "function") {
        playback.catch(function () {
          state.step = null;
          state.status("Playback could not start. Use the video controls to try again.");
          state.refresh();
        });
      }
    };

    state.complete = function () {
      var completed = state.step;
      if (!completed) return;
      state.step = null;
      video.pause();
      video.currentTime = Math.min(completed.end, video.duration);
      state.status("Step complete: " + completed.title + ". Select another step or continue the full tutorial.");
      state.refresh();
    };

    video.addEventListener("timeupdate", function () {
      if (state.step && !video.seeking && video.currentTime >= state.step.end) state.complete();
    });
    video.addEventListener("seeking", function () {
      if (state.step && (video.currentTime < state.step.start - 0.1 || video.currentTime > state.step.end + 0.1)) {
        state.step = null;
        state.status("Step playback ended after seeking. Continue from the current position.");
      }
    });
    video.addEventListener("play", function () {
      if (playingVideo && playingVideo !== video) playingVideo.pause();
      playingVideo = video;
      state.refresh();
    });
    video.addEventListener("ended", function () {
      if (state.step) state.complete();
      state.refresh();
    });
    video.addEventListener("emptied", function () { state.step = null; state.refresh(); });
    video.addEventListener("error", function () {
      state.step = null;
      state.status("This video could not be loaded. Use the video download or transcript below.");
      state.refresh();
    });
    ["pause", "seeked", "loadedmetadata"].forEach(function (event) {
      video.addEventListener(event, state.refresh);
    });
    controllers.set(video, state);
    state.refresh();
    return state;
  }

  function bindStudioVideo() {
    if (playingVideo && !playingVideo.isConnected) {
      playingVideo.pause();
      playingVideo = null;
    }
    document.querySelectorAll("[data-studio-time]").forEach(function (button) {
      var videoId = button.getAttribute("data-studio-video") || "studio-authoring-video";
      var video = document.getElementById(videoId);
      if (!video || button.dataset.studioVideoBound === videoId) return;
      var state = controllerFor(video);
      button.dataset.studioVideoBound = videoId;
      button.addEventListener("click", function () {
        var start = Number(button.getAttribute("data-studio-time"));
        var endAttribute = button.getAttribute("data-studio-end");
        var end = endAttribute === null ? null : Number(endAttribute);
        if (!Number.isFinite(start) || start < 0 ||
            (end !== null && (!Number.isFinite(end) || end <= start))) {
          state.status("This chapter has invalid timings. Use the video controls or transcript.");
          return;
        }
        var title = button.getAttribute("data-studio-title") || button.textContent.trim();
        state.step = end === null ? null : { start: start, end: end, title: title };
        video.currentTime = start;
        state.status(state.step ? "Watching one step: " + title + ". Playback pauses at the end." :
          "Playing the tutorial from the selected chapter.");
        video.scrollIntoView({ block: "center", behavior: "auto" });
        state.play();
      });
    });
    document.querySelectorAll("[data-studio-continue]").forEach(function (button) {
      var videoId = button.getAttribute("data-studio-continue");
      var video = document.getElementById(videoId);
      if (!video || button.dataset.studioContinueBound === videoId) return;
      var state = controllerFor(video);
      button.dataset.studioContinueBound = videoId;
      button.addEventListener("click", function () {
        if (!video.paused) { video.pause(); return; }
        state.step = null;
        if (video.ended || video.currentTime >= video.duration - 0.1) video.currentTime = 0;
        state.status("Playing the full tutorial from the current position.");
        state.play();
      });
      state.refresh();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindStudioVideo, { once: true });
  } else {
    bindStudioVideo();
  }
  if (typeof document$ !== "undefined") document$.subscribe(bindStudioVideo);
}());
