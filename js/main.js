/* emanahmed.org: theme, navigation, citation copy. No dependencies. */
(function () {
  "use strict";

  var root = document.documentElement;

  /* --- Colour theme ----------------------------------------------------- */
  function current() {
    var set = root.getAttribute("data-theme");
    if (set) return set;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  var themeBtn = document.getElementById("theme");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  /* --- Mobile navigation ------------------------------------------------ */
  var burger = document.getElementById("burger");
  var nav = document.getElementById("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      nav.setAttribute("data-open", String(!open));
      burger.setAttribute("aria-expanded", String(!open));
      burger.setAttribute("aria-label", open ? "Open menu" : "Close menu");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.setAttribute("data-open", "false");
        burger.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.getAttribute("data-open") === "true") {
        nav.setAttribute("data-open", "false");
        burger.setAttribute("aria-expanded", "false");
        burger.focus();
      }
    });
  }

  /* --- Toast ------------------------------------------------------------ */
  var toast = document.getElementById("toast");
  var toastTimer;
  function say(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.setAttribute("data-show", "true");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.setAttribute("data-show", "false");
    }, 2600);
  }

  /* --- Copy citations --------------------------------------------------- */
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:absolute;left:-9999px;top:0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy") ? resolve() : reject();
      } catch (e) {
        reject(e);
      } finally {
        document.body.removeChild(ta);
      }
    });
  }

  /* --- Chart hover layer ------------------------------------------------ */
  /* Marks carry a native <svg:title>, which already works with no JS and for
     screen readers. This replaces the slow native tooltip with a styled one and
     leaves the title element in place as the fallback. */
  var tip;
  function ensureTip() {
    if (!tip) {
      tip = document.createElement("div");
      tip.className = "viztip";
      tip.setAttribute("role", "presentation");
      document.body.appendChild(tip);
    }
    return tip;
  }

  function markTitle(el) {
    var t = el.querySelector("title");
    return t ? t.textContent : null;
  }

  document.addEventListener("pointerover", function (e) {
    var el = e.target.closest && e.target.closest(".viz [data-tip], .viz circle, .viz rect");
    if (!el || !el.closest(".viz")) return;
    var text = el.getAttribute("data-tip") || markTitle(el);
    if (!text) return;
    var t = ensureTip();
    t.textContent = text;
    t.setAttribute("data-show", "true");
    var r = el.getBoundingClientRect();
    var x = r.left + r.width / 2 + window.scrollX;
    var y = r.top + window.scrollY;
    t.style.left = "0px";
    t.style.top = "0px";
    var tw = t.offsetWidth, th = t.offsetHeight, pad = 8;
    x = Math.min(Math.max(x - tw / 2, pad + window.scrollX),
                 window.scrollX + document.documentElement.clientWidth - tw - pad);
    t.style.left = x + "px";
    t.style.top = (y - th - 10) + "px";
  });

  document.addEventListener("pointerout", function (e) {
    if (!tip) return;
    var el = e.target.closest && e.target.closest(".viz");
    if (el) tip.setAttribute("data-show", "false");
  });

  window.addEventListener("scroll", function () {
    if (tip) tip.setAttribute("data-show", "false");
  }, { passive: true });

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy]");
    if (!btn) return;
    copy(btn.getAttribute("data-copy")).then(
      function () { say("Copied to clipboard"); },
      function () { say("Couldn't copy. Select the text and copy manually"); }
    );
  });
})();
