# GrantApp AI — Project Context Dossier
> For agents picking up this project. Read fully before touching anything.

---

## 1. Brand & Vision

**Brand:** GrantApp AI (`grantapp.ai`)
**Tagline:** The best matriculation exam prep site in Africa.
**Product name:** GrantApp (never "UTMEDaily" — that was a working repo name, not the brand)
**Design voice:** Dark, premium, technical. Think Linear/Vercel energy but for African students.
**Repo:** `https://github.com/artificialiman/UTMEDaily` (rename pending — treat as temporary)
**Question bank repo:** `https://github.com/artificialiman/Questt-resources`

---

## 2. Tech Stack & Architecture Principles

**Stack:** Pure static HTML + CSS + Vanilla JS. Zero frameworks, zero bundlers, zero fetches at runtime.

**Rules the owner cares about deeply:**
- Markup and scripting are separated cleanly: HTML for structure, JS only for behaviour, CSS for style
- JS is NEVER used for routing or state management across pages — that's HTML's job (`<a href="">`)
- Questions are embedded directly in each quiz HTML file as a `const QUESTIONS = [...]` array
- `DURATION` (seconds) is declared at the top of each quiz file
- `quiz-app.js` is shared and handles all quiz UI behaviour — it reads `QUESTIONS` and `DURATION` from the page
- No page should ever dead-end on GitHub's 404 — all broken links go to our own `coming-soon.html`

**Fonts:** Syne (headings, 800/700/600) + DM Sans (body, 300/400/500) — Google Fonts CDN
**Icons:** Font Awesome 6.0.0 — `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css`

---

## 3. File Inventory (Raw GitHub URLs)

### Core App Files
```
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-app.js
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-styles.css
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/styles.css
```

### Landing & Stream Selection
```
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/index.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/science_clusters.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/commercial_clusters.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/art_clusters.html
```

### Existing Quiz Files (Live)
```
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-science-bepc.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-commerce-a.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-chemistry.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-mathematics.html
```

### Example Cluster File (reference for cluster architecture)
```
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-science-bepc.html
https://raw.githubusercontent.com/artificialiman/UTMEDaily/refs/heads/main/quiz-commerce-a.html
```

### Question Bank (Raw txt — one file per subject, 35 questions each)
```
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_English_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Biology_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Chemistry_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Physics_Q1-35.txt  ← (built from this, file may not exist in repo yet)
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Government_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Literature_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_CRS_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Accounting_Q1-35.txt
https://raw.githubusercontent.com/artificialiman/Questt-resources/refs/heads/main/archive/day-1-2/JAMB_Commerce_Q1-35.txt
```
> Economics, Mathematics, History, Geography question bank files do NOT exist yet — must be authored from scratch.

---

## 4. Files Built This Session (Not Yet in Repo)

All 5 files are ready to deploy to repo root:

| File | Type | Questions | Duration | Subjects |
|---|---|---|---|---|
| `quiz-physics.html` | Individual | 35 | 15 min | Physics |
| `quiz-mathematics.html` | Individual | 35 | 15 min | Mathematics |
| `quiz-arts-cluster-a.html` | Cluster | 140 | 60 min | English + Literature + Government + CRS |
| `quiz-commercial-b.html` | Cluster | 140 | 60 min | English + Maths + Economics + Government |
| `quiz-commercial-c.html` | Cluster | 140 | 60 min | English + Economics + Government + Commerce |

---

## 5. JAMB Stream Map (Current State)

### Science Stream (`science_clusters.html`)
| Code | Cluster File | Subjects | Status |
|---|---|---|---|
| BEPC | `quiz-science-bepc.html` | Eng + Bio + Physics + Chem | ✅ Live |
| BMPC | `quiz-science-bmpc.html` | Eng + Bio + Maths + Chem | ❌ Missing |
| EMPC | `quiz-science-empc.html` | Eng + Maths + Physics + Chem | ❌ Missing |
| EMPB | `quiz-science-empb.html` | Eng + Maths + Physics + Bio | ❌ Missing |

Individual subjects needed: Biology ✅, Chemistry ✅, Physics ✅ ready, Mathematics ✅ ready, Further Maths ❌

### Commercial Stream (`commercial_clusters.html`)
| Code | Cluster File | Subjects | Status |
|---|---|---|---|
| EACE | `quiz-accounting.html` | Eng + Acct + Commerce + Econ | ⚠️ Live but MISLEADING — no Maths, can't get into university Accounting |
| EMEG | `quiz-commercial-b.html` | Eng + Maths + Econ + Govt | ✅ Ready (not yet deployed) |
| EEGC | `quiz-commercial-c.html` | Eng + Econ + Govt + Commerce | ⚠️ Ready — valid only for narrow courses (Insurance, HR Mgmt, Public Admin) |

Individual subjects needed: English ✅, Maths ✅, Economics ❌, Commerce ✅, Accounting ✅, Government ✅

### Arts Stream (`art_clusters.html`)
| Code | Cluster File | Subjects | Status |
|---|---|---|---|
| ELGC | `quiz-arts-cluster-a.html` | Eng + Lit + Govt + CRS | ✅ Ready (not yet deployed) |

Individual subjects needed: English ✅, Literature ❌, Government ✅, CRS ✅

### Missing JAMB Combos (Priority Order)
1. **EHGE** — Eng + Govt + Hist + Econ → Political Science, Public Admin, History & Int'l Studies, Criminology *(biggest gap, most popular courses)*
2. **EGEG** — Eng + Govt + Econ + Geog → Town Planning, Urban Planning, Demography, Geography
3. **EMPB** — Eng + Maths + Physics + Bio → Computer Science, Computer Engineering

Question bank files needed for these: History, Geography, Economics — all must be authored.

---

## 6. New Index Page Vision (In Progress)

The current `index.html` is JAMB-only stream selector. It needs to become the **All Matriculatory Exams** hub.

### New page architecture:
```
index.html  ← ALL exams landing (hero + exam stream cards + community + reviews)
    │
    ├── jamb.html  ← current index.html content (moved, not deleted)
    │       ├── science_clusters.html
    │       ├── commercial_clusters.html
    │       └── art_clusters.html
    │
    ├── wassce.html  ← coming soon (collect contact)
    ├── ap-exams.html  ← coming soon (collect contact) — ALL AP subjects, not just chemistry
    ├── sat.html  ← future
    ├── ib.html  ← future
    └── 10k-mastery.html  ← coming soon (collect contact) — 10,000 questions mastery mode
```

### Sections on new index.html:
1. **Hero** — "Africa's best exam prep platform" energy
2. **Exam stream cards** — JAMB (live), WASSCE (coming soon), AP Exams (coming soon), 10K Mastery (coming soon) — paginated if list grows
3. **Community section** — smaller than stream cards, extremely polished CSS
4. **Reviews/Social proof** — media placeholder carousel (mechanism later)

### Community links (live):
- WhatsApp Group: `https://chat.whatsapp.com/BVloVed0PIDIbojLeRMQCU?mode=gi_t`
- WhatsApp Channel: `https://whatsapp.com/channel/0029VbCMrEVIyPtLYUrc7I3K`
- TikTok: placeholder (handle TBD)

### Coming Soon cards behaviour:
- Must collect contact details (name + WhatsApp number or email)
- Store or display gracefully (no backend yet — could be a WhatsApp pre-fill link or formspree)
- Must NOT link to GitHub 404 under any circumstance

---

## 7. coming-soon.html (Needed)

All dead links site-wide must route here. Does not exist yet. Must be:
- Branded GrantApp AI
- Beautiful — not a lazy placeholder
- Ideally collects email/WhatsApp for waitlist
- Links back to index.html

---

## 8. Design System (from live files)

```css
:root {
  --bg: #0a0a0f;
  --surface: #111118;
  --border: #1e1e2e;
  --text: #f0eff4;
  --muted: #7a7a8c;
  --accent: #f59e0b;       /* amber — GrantApp brand */

  /* Stream colours */
  --science: #3b82f6;      /* blue */
  --science-glow: rgba(59,130,246,0.15);
  --arts: #a855f7;         /* purple */
  --arts-glow: rgba(168,85,247,0.15);
  --commerce: #10b981;     /* green */
  --commerce-glow: rgba(16,185,129,0.15);

  /* To assign for new streams */
  --wassce: TBD;
  --ap: TBD;
}
```

Card hover pattern (used everywhere):
```css
card:hover {
  transform: translateY(-4px);
  border-color: var(--stream-color);
  box-shadow: 0 0 30px var(--stream-glow);
}
card::before {
  /* radial gradient glow, opacity 0 → 1 on hover */
  background: radial-gradient(ellipse at top left, var(--stream-glow), transparent 60%);
}
```

---

## 9. Quiz File Template Pattern

Every quiz HTML file follows this exact structure — no exceptions:

```html
<!-- 1. Head: quiz-styles.css + FA icons -->
<!-- 2. <script> block FIRST in body: DURATION + QUESTIONS array -->
<!-- 3. <header class="quiz-header"> with subject name, timer SVG, calculator btn, submit btn -->
<!-- 4. .quiz-container with: -->
<!--      <aside class="quiz-sidebar"> — navigator, stats, palette, legend, Back button -->
<!--      <main class="quiz-main"> — question card + options + explanation + nav buttons -->
<!-- 5. .mobile-palette-trigger -->
<!-- 6. Modals: submitModal, timeUpModal, calculatorModal -->
<!-- 7. <script src="quiz-app.js"> LAST -->
```

**DURATION values:**
- Individual subject (35q): `900` (15 min)
- Cluster exam (140q): `3600` (60 min)

**Back button** in sidebar always points to the parent cluster page:
- Science quizzes → `science_clusters.html`
- Commercial quizzes → `commercial_clusters.html`
- Arts quizzes → `art_clusters.html`

**QUESTIONS array format:**
```js
{
  id: 1,
  subject: 'Chemistry',       // shown in cluster header badge
  text: 'Question text here',
  options: { A: '...', B: '...', C: '...', D: '...' },
  answer: 'B',
  explanation: 'Why B is correct.',   // optional but preferred
  exception: 'Common gotcha.',        // optional
}
```

---

## 10. Known Issues / Outstanding Fixes

| Issue | Priority | Notes |
|---|---|---|
| `quiz-accounting.html` (EACE cluster) is misleading | 🔴 High | Named "Accounting & Business" but no Maths — can't get into university Accounting. Fix: rename to "Business Studies" and target Cooperative Econ, Insurance, some polytechnic courses only |
| `quiz-commercial-c.html` (EEGC) needs accurate course targeting | 🟡 Medium | Valid for Insurance, Public Admin, HR Mgmt, Cooperative Econ — not general commerce |
| No `coming-soon.html` exists | 🔴 High | All dead links currently 404 on GitHub |
| Economics question bank doesn't exist | 🟡 Medium | Needed for EMEG, EEGC clusters and EHGE combo |
| History question bank doesn't exist | 🟡 Medium | Needed for EHGE combo |
| Geography question bank doesn't exist | 🟡 Medium | Needed for EGEG combo |
| `quiz-mathematics.html` may conflict with existing file in repo | 🟡 Medium | Verify before deploying — existing file may be different |

---

## 11. Immediate Next Steps (in order)

1. Deploy the 5 built files from this session to repo root
2. Build `coming-soon.html` (branded, beautiful, collects contact)
3. Fix EACE cluster description/course targets
4. Restructure `index.html` → new all-exams landing + move JAMB content to `jamb.html`
5. Build EHGE cluster (Eng + Govt + Hist + Econ) — needs Economics + History question banks
6. Build EGEG cluster (Eng + Govt + Econ + Geog) — needs Geography question bank
7. Build EMPB cluster (Eng + Maths + Physics + Bio)
