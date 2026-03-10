/* premium-auth.js — GrantApp AI Premium
   Owns: password validation, session management, watermark injection.
   Does NOT own: routing (HTML anchors), styling (premium-styles.css).
   Session: 3 hours via sessionStorage. Dies with tab. No persistence.
*/

'use strict';

/* ── PASSWORD REGISTRY ──────────────────────────────────────────────────────
   SHA-256 hashes only. Plaintext lives in OWNER_PASSWORDS_PRIVATE.txt (off-repo).
   To revoke: delete the entry. To add: append entry + push.
   Each hash maps to: { name, subject, hub }
*/
const PREMIUM_REGISTRY = {
  /* Conve */
  "2a0a29655a718f08c7d570690a97baba2efd24a9ab0aff058a6b1e96f8cafed3": { name: "Conve",    subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "3c186654c515264f131d68cff2f780daf4ea10158383f17f102eb2e41eef9a52": { name: "Conve",    subject: "english",   hub: "premium-english-hub.html"   },
  /* Kaosara */
  "52325707193ccf20a538d87234a8ed17260df970d580665cab8cda029a83cdc7": { name: "Kaosara",  subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "d99fce23ebebe0fd7f03553cff47aedfe34b908c25311110577d964038328876": { name: "Kaosara",  subject: "english",   hub: "premium-english-hub.html"   },
  /* Habibat */
  "e32f4d7152cd507caa3b0c58081936f3189059f34b89115dffdb39852c541618": { name: "Habibat",  subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "26a8f01afaa022662df7269b575993d62deb879768582ac9e63d57068680968f": { name: "Habibat",  subject: "english",   hub: "premium-english-hub.html"   },
  /* Oyin */
  "b0ce2a7c2f3539c0e1f52e48ba4a00159504f553ac11fe03c76bee3fa70e12eb": { name: "Oyin",     subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "7035c13955b75382010c0d0601caa07d30fab3967f6ccd5c816e3b855e74644b": { name: "Oyin",     subject: "english",   hub: "premium-english-hub.html"   },
  /* Dorcas */
  "05d9d182d4b7d22cd42fe87e4d92b93f6ae0a5bb494066058220f1d2cd78c4a2": { name: "Dorcas",   subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "d64ab31897783c56a4d4b45bb9921256fca9ba0a25519e1112a9afaf883e7674": { name: "Dorcas",   subject: "english",   hub: "premium-english-hub.html"   },
  /* Famous */
  "d1deca157a6e62522cf0b60a5d2cb1da19c4357e23836b6dbcc925132a365873": { name: "Famous",   subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "7df210ce678bba5e2025afe6389f0e9f24bbca1c4fae7f616535f6d82ed83b39": { name: "Famous",   subject: "english",   hub: "premium-english-hub.html"   },
  /* Obasesam */
  "36dc8e24107b582d3cf5e10dd30c1d42b97b0edb4217783068541f8ca08912b4": { name: "Obasesam", subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "d058f59e92ac68bc8210d39adc813153d7bf0dfdf4fc9f7d090d218ba77db232": { name: "Obasesam", subject: "english",   hub: "premium-english-hub.html"   },
  /* Prosper */
  "b7833bfa0b89ef6c04fbdfb7741f58b9fdb8d6cfd910f76af1d7ef0c9e485080": { name: "Prosper",  subject: "chemistry", hub: "premium-chemistry-hub.html" },
  "3d6519d11f3ac93bd37f760f0e79303e924ac7a0d05d3904cff42d3c953a8dfc": { name: "Prosper",  subject: "english",   hub: "premium-english-hub.html"   },
};

const SESSION_KEY     = 'ga_premium_session';
const SESSION_TTL_MS  = 3 * 60 * 60 * 1000; /* 3 hours */


/* ── SESSION HELPERS ────────────────────────────────────────────────────── */

function saveSession(record) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify({
    ...record,
    expires: Date.now() + SESSION_TTL_MS
  }));
}

function loadSession() {
  try {
    const raw = sessionStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    const s = JSON.parse(raw);
    if (Date.now() > s.expires) { sessionStorage.removeItem(SESSION_KEY); return null; }
    return s;
  } catch { return null; }
}

function clearSession() {
  sessionStorage.removeItem(SESSION_KEY);
}


/* ── SHA-256 ─────────────────────────────────────────────────────────────── */

async function sha256(str) {
  const buf    = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}


/* ── WATERMARK ───────────────────────────────────────────────────────────── */

function injectWatermark(name) {
  /* Diagonal tiled text watermark — low opacity, pointer-events none */
  const wm = document.createElement('div');
  wm.id = 'ga-watermark';
  wm.setAttribute('aria-hidden', 'true');

  const tile = `${name} · GrantApp AI · `;
  const row  = tile.repeat(8);
  let   html = '';
  for (let i = 0; i < 14; i++) html += `<span>${row}</span>`;
  wm.innerHTML = html;

  Object.assign(wm.style, {
    position:       'fixed',
    inset:          '0',
    zIndex:         '9999',
    pointerEvents:  'none',
    overflow:       'hidden',
    display:        'flex',
    flexDirection:  'column',
    gap:            '2.5rem',
    padding:        '1rem',
    transform:      'rotate(-22deg) scale(1.4)',
    transformOrigin:'center center',
    opacity:        '0.028',
    fontFamily:     "'DM Mono', monospace",
    fontSize:       '0.75rem',
    fontWeight:     '500',
    color:          '#f0eff4',
    letterSpacing:  '0.06em',
    whiteSpace:     'nowrap',
    userSelect:     'none',
    WebkitUserSelect: 'none',
  });

  document.body.appendChild(wm);
}


/* ── GREETING CHIP ───────────────────────────────────────────────────────── */

function injectGreetingChip(name, subject) {
  /* Injects a chip into any element with data-premium-greeting attribute */
  const targets = document.querySelectorAll('[data-premium-greeting]');
  targets.forEach(el => {
    el.textContent = `Hey, ${name}`;
    el.removeAttribute('hidden');
  });

  /* Also fill any data-premium-name span */
  document.querySelectorAll('[data-premium-name]').forEach(el => {
    el.textContent = name;
  });

  /* And data-premium-subject */
  document.querySelectorAll('[data-premium-subject]').forEach(el => {
    el.textContent = subject.charAt(0).toUpperCase() + subject.slice(1);
  });
}


/* ── GATE: call on every premium page except auth ────────────────────────── */
/* Usage: <script src="premium-auth.js"></script>
          <script>PremiumGate.require('chemistry');</script>
   If session is valid for that subject, injects watermark + greeting.
   If not, redirects to auth page.
*/

const PremiumGate = {
  require(subject) {
    const session = loadSession();
    if (!session || session.subject !== subject) {
      clearSession();
      window.location.href = 'premium-auth.html';
      return;
    }
    /* Session valid — personalise the page */
    document.addEventListener('DOMContentLoaded', () => {
      injectWatermark(session.name);
      injectGreetingChip(session.name, session.subject);
    });
  },

  /* Call on results screen to show name in result watermark area */
  getSession: loadSession,
};


/* ── AUTH PAGE CONTROLLER ────────────────────────────────────────────────── */
/* Only runs when #premium-auth-form exists in the DOM */

document.addEventListener('DOMContentLoaded', () => {
  const form    = document.getElementById('premium-auth-form');
  if (!form) return; /* Not the auth page */

  /* If already have a valid session, skip straight to hub */
  const existing = loadSession();
  if (existing) {
    window.location.href = existing.hub;
    return;
  }

  const input   = document.getElementById('premium-password-input');
  const btn     = document.getElementById('premium-auth-btn');
  const errMsg  = document.getElementById('premium-auth-error');
  const spinner = document.getElementById('premium-auth-spinner');

  function setError(msg) {
    errMsg.textContent = msg;
    errMsg.removeAttribute('hidden');
    input.setAttribute('aria-invalid', 'true');
  }

  function clearError() {
    errMsg.setAttribute('hidden', '');
    input.removeAttribute('aria-invalid');
  }

  async function attempt() {
    const pw = input.value.trim();
    if (!pw) { setError('Please enter your access password.'); return; }

    clearError();
    btn.disabled    = true;
    spinner.removeAttribute('hidden');

    const hash   = await sha256(pw);
    const record = PREMIUM_REGISTRY[hash];

    spinner.setAttribute('hidden', '');
    btn.disabled = false;

    if (!record) {
      setError("That password doesn't look right. Double-check and try again.");
      input.select();
      return;
    }

    saveSession(record);
    window.location.href = record.hub;
  }

  btn.addEventListener('click', attempt);

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') attempt();
  });

  input.addEventListener('input', clearError);
});
