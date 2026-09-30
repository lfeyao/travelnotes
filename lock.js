/* Travel Notes · password gate (client-side)
 *
 * The site is static hosting, so this is a courtesy lock: it keeps casual
 * visitors out but does NOT protect data/*.json from anyone who fetches the
 * URLs directly or reads page source. Real access control needs server-side
 * auth (e.g. Cloudflare Access) instead of GitHub Pages.
 *
 * The password is stored only as a SHA-256 hash below. To change the
 * password, replace PASS_HASH with the hex SHA-256 of the new password:
 *   echo -n "newpassword" | sha256sum
 */
(function () {
  "use strict";

  var PASS_HASH = "9809b3d3889afe52c6f55589fcd3cfda6ec265a5c61d94dc34227a852c98cc32";
  var SESSION_KEY = "tn_unlocked";

  function unlock() {
    document.body.classList.remove("locked");
    var lock = document.getElementById("lock");
    if (lock) lock.remove();
    try { sessionStorage.setItem(SESSION_KEY, "1"); } catch (e) {}
  }

  // Already unlocked in this tab session?
  try {
    if (sessionStorage.getItem(SESSION_KEY) === "1") { unlock(); return; }
  } catch (e) {}

  function hex(buf) {
    return Array.prototype.map.call(new Uint8Array(buf), function (b) {
      return ("0" + b.toString(16)).slice(-2);
    }).join("");
  }

  function sha256(str) {
    if (window.crypto && crypto.subtle) {
      return crypto.subtle.digest("SHA-256", new TextEncoder().encode(str)).then(hex);
    }
    // Fallback (non-secure contexts): plain compare is not available since we
    // only store the hash — fail closed.
    return Promise.resolve(null);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("lock-form");
    var input = document.getElementById("lock-pass");
    var err = document.getElementById("lock-error");
    var card = document.getElementById("lock-card");
    if (!form) { return; }
    input.focus();

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      err.hidden = true;
      card.classList.remove("shake");
      sha256(input.value).then(function (digest) {
        if (digest && digest === PASS_HASH) {
          input.value = "";
          unlock();
        } else {
          err.hidden = false;
          card.classList.add("shake");
          input.value = "";
          input.focus();
        }
      });
    });
  });
})();
