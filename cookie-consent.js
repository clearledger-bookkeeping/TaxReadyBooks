(function () {
  "use strict";
  var KEY = "trb_cookie_consent_v1";
  var styles = `
    #trb-cookie-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;display:none;max-width:820px;margin:auto;padding:20px;border:1px solid rgba(255,255,255,.18);border-radius:16px;background:#1B1F3B;color:#FAFAF7;box-shadow:0 18px 55px rgba(0,0,0,.3);font:14px/1.55 Inter,system-ui,sans-serif}
    #trb-cookie-banner.trb-show{display:block}
    #trb-cookie-banner *{box-sizing:border-box}
    .trb-cookie-inner{display:flex;align-items:center;justify-content:space-between;gap:20px}
    .trb-cookie-copy{max-width:510px}.trb-cookie-copy strong{display:block;font-size:16px;margin-bottom:5px}
    .trb-cookie-copy p{margin:0 0 8px}.trb-cookie-copy a{color:#F2A33A;text-decoration:underline;text-underline-offset:3px}
    .trb-cookie-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
    .trb-cookie-actions button,#trb-cookie-preferences{font:600 13px/1.2 Inter,system-ui,sans-serif;border:1px solid rgba(255,255,255,.45);border-radius:9px;padding:11px 13px;background:transparent;color:#FAFAF7;cursor:pointer}
    .trb-cookie-actions .trb-cookie-accept{background:#F2A33A;color:#1B1F3B;border-color:#F2A33A}
    #trb-cookie-settings{display:none;margin-top:15px;padding-top:14px;border-top:1px solid rgba(255,255,255,.2)}
    #trb-cookie-settings.trb-open{display:block}
    .trb-cookie-toggle{display:flex;gap:9px;align-items:flex-start;margin:10px 0}
    .trb-cookie-toggle input{accent-color:#F2A33A;margin-top:4px}
    #trb-cookie-preferences{position:fixed;right:16px;bottom:16px;z-index:2147482999;display:none;background:#1B1F3B;color:#FAFAF7;box-shadow:0 5px 20px rgba(0,0,0,.2)}
    #trb-cookie-preferences.trb-show{display:block}
    @media(max-width:640px){.trb-cookie-inner{display:block}.trb-cookie-actions{margin-top:14px}.trb-cookie-actions button{flex:1 1 auto}#trb-cookie-banner{padding:16px}}
    @media(prefers-reduced-motion:reduce){#trb-cookie-banner{scroll-behavior:auto}}
  `;
  function init() {
    if (document.getElementById("trb-cookie-banner")) return;
    var style = document.createElement("style");
    style.id = "trb-cookie-consent-style";
    style.textContent = styles;
    document.head.appendChild(style);
    var banner = document.createElement("section");
    banner.id = "trb-cookie-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-modal", "false");
    banner.setAttribute("aria-labelledby", "trb-cookie-title");
    banner.innerHTML = '<div class="trb-cookie-inner"><div class="trb-cookie-copy"><strong id="trb-cookie-title">Your cookie choices</strong><p>We use essential browser storage to remember your choice. This site currently does not load optional analytics or advertising cookies. Read our <a href="/cookie-policy.html">Cookie Policy</a> and <a href="/privacy-policy.html">Privacy Policy</a>.</p></div><div class="trb-cookie-actions"><button type="button" class="trb-cookie-accept" data-trb-consent="all">Accept cookies</button><button type="button" data-trb-consent="reject">Reject optional</button><button type="button" data-trb-consent="settings">Settings</button></div></div><div id="trb-cookie-settings"><p><strong>Cookie settings</strong></p><label class="trb-cookie-toggle"><input type="checkbox" checked disabled><span><strong>Essential storage</strong> — always on; needed to remember your privacy choice and support basic site functions.</span></label><label class="trb-cookie-toggle"><input id="trb-optional-cookies" type="checkbox"><span><strong>Optional analytics / advertising</strong> — currently not loaded by this website. Your choice will be remembered.</span></label><div class="trb-cookie-actions"><button type="button" class="trb-cookie-accept" data-trb-consent="save">Save choices</button><button type="button" data-trb-consent="reject">Reject optional</button></div></div>';
    document.body.appendChild(banner);
    var prefs = document.createElement("button");
    prefs.type = "button";
    prefs.id = "trb-cookie-preferences";
    prefs.textContent = "Cookie preferences";
    prefs.setAttribute("aria-label", "Open cookie preferences");
    document.body.appendChild(prefs);

    function readConsent() {
      try { return JSON.parse(window.localStorage.getItem(KEY) || "null"); } catch (_) { return null; }
    }
    function save(optional) {
      var value = { essential: true, optional: !!optional, savedAt: new Date().toISOString(), version: 1 };
      try { window.localStorage.setItem(KEY, JSON.stringify(value)); } catch (_) {}
      banner.classList.remove("trb-show");
      prefs.classList.add("trb-show");
    }
    function openBanner() {
      var c = readConsent();
      document.getElementById("trb-optional-cookies").checked = !!(c && c.optional);
      document.getElementById("trb-cookie-settings").classList.remove("trb-open");
      banner.classList.add("trb-show");
      prefs.classList.remove("trb-show");
    }
    banner.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-trb-consent]");
      if (!button) return;
      var action = button.getAttribute("data-trb-consent");
      if (action === "all") save(true);
      else if (action === "reject") save(false);
      else if (action === "settings") document.getElementById("trb-cookie-settings").classList.toggle("trb-open");
      else if (action === "save") save(document.getElementById("trb-optional-cookies").checked);
    });
    prefs.addEventListener("click", openBanner);
    if (readConsent()) prefs.classList.add("trb-show");
    else openBanner();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();