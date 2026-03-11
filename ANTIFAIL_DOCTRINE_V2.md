# GrantApp AI — Antifail Doctrine v2
> **Rule Zero:** Every tool does one job. Never let a fix in one file bleed into another file's job.

**Repo:** `artificialiman/UTMEDaily`
**Question bank:** `artificialiman/Questt-resources`
**Last updated:** 2026-03-11

---

## 1. The Blame Doctrine — Routing

HTML routes. JS behaves. CSS styles. Python builds.

`<a href="filename.html">` is the only routing mechanism in this codebase. `window.location`, `onclick` navigation, and `history.pushState` are **banned**.

**Why:** If a plain anchor fails, the browser failed, the network failed, or the user's environment failed — that is acceptable and outside your control. If JS routing fails, it fails silently with no error the user can report and no trail you can follow. That failure is yours. We don't accept that.

**Exception — session gate only:** `window.location.href` is permitted **once** per premium hub/quiz page, inside the session validation block, to redirect unauthenticated users back to `premium-auth.html`. This is the only sanctioned use of JS navigation. It must always be at the top of the script, run before DOMContentLoaded, and be a one-way redirect only.

---

## 2. Question Embedding Contract

Every quiz file declares two globals in a `<script>` block:

```js
const DURATION = N;       // seconds
const QUESTIONS = [...];  // full question objects, shuffled at build time
```

`quiz-app.js` reads these for the free quiz tier. **Premium papers** are self-contained — they embed `const QUESTIONS = [...]` directly and carry all UI, timer, and scoring logic inline. They do not load `quiz-app.js`. This is intentional.

It fetches nothing. It loads nothing at runtime. If the page loads, it has everything it needs.

---

## 3. Build Contract

**Free quiz tier:** `build.py` is the single source of truth. Edit questions there → run `python build.py` → push output.

**Premium papers:** Python builds the question array at generation time (selection, deduplication, option shuffle, answer key balancing), then stamps it into the HTML template. The Python script is the build tool — the HTML is the output. Never hand-edit a generated premium paper.

- Fisher-Yates / `random.sample` shuffle happens at build time — JS never shuffles anything
- Answer key is explicitly balanced to A=13, B=13, C=12, D=12 per 50-question paper at build time
- No question enters any paper that hasn't been source-verified

---

## 4. Boilerplate Protection

The quiz HTML boilerplate is sacred. Never modify it directly. The build process stamps question data into it — that is the only thing that changes between quiz files.

**Parsing safety is mandatory.** All question strings must be escaped before embedding:
- Escape backslashes, double quotes, and newlines
- `esc()` function in the build script handles this — never bypass it
- A parsing error kills the entire quiz page silently. There will be no visible error.

---

## 5. File Ownership Map

| File | Owns | Must NOT touch |
|---|---|---|
| `build.py` | Free quiz question data, HTML generation, shuffle | Routing, CSS, UI behaviour |
| `quiz-app.js` | Free quiz UI, timer, PDF, scoring, answer state | Routing, question data |
| `quiz-styles.css` | Free quiz page styles | `styles.css` scope |
| `styles.css` | Landing, cluster, stream page styles | Quiz page styles |
| `index.html` | All-exams landing hub | JAMB-specific logic |
| `*_clusters.html` | Cluster/subject selection per stream | Quiz logic |
| `coming-soon.html` | Catches every dead link | Live quiz logic |
| `premium-auth.html` | Password entry, SHA-256 hashing, session creation | Everything else |
| `premium-chemistry-hub.html` | Chemistry paper listing, session gate | Auth logic, quiz logic |
| `premium-english-hub.html` | English paper listing, session gate | Auth logic, quiz logic |
| `Chemistry-paper-N.html` | Self-contained quiz — questions, UI, timer, scoring | Auth, routing, other papers |

---

## 6. CSS Scope Boundaries

```
styles.css        → index.html, jamb.html, *_clusters.html
quiz-styles.css   → all free quiz-*.html files
premium hub CSS   → inline in each premium hub HTML (self-contained)
premium paper CSS → inline in each Chemistry-paper-N.html (self-contained)
```

Never cross these boundaries. Premium files are self-contained — they carry their own CSS inline. Do not extract it to a shared sheet.

**Option state rule** (premium papers):
- `.opt:hover`  = amber border — "considering"
- `.opt.sel`    = amber fill — "committed"
- `.opt.ok`     = green — "correct"
- `.opt.no`     = red — "wrong"

---

## 7. Font Stack

```
Syne       — headings (800/700/600) — Google Fonts CDN
DM Sans    — body (300/400/500)     — Google Fonts CDN
Space Mono — badges, mono labels    — Google Fonts CDN  [free tier]
DM Mono    — badges, mono labels    — Google Fonts CDN  [premium tier]
```

Never substitute these. Never load fonts from a non-CDN source.

---

## 8. Script Load Order (Free Quiz Pages)

```
question-parser.js    ← class definitions (QuestionParser)
jspdf.umd.min.js      ← PDF library (cdnjs CDN)
quiz-app.js           ← bootQuiz(), QuizState, QuizUI
```

**Premium pages:** Single inline `<script>` block only. No external JS dependencies. `window.print()` handles PDF — no jsPDF needed.

---

## 9. Scoring Rules

**Free tier:** Negative marking. If final score ends in `.5`, always round **up**. Never round down.

**Premium papers (UTME standard):** No negative marking. Correct = 1 point. Wrong/skipped = 0. Score displayed as percentage.

```
UTME: score% = (correct / 50) × 100
```

---

## 10. Premium Auth System

**File:** `premium-auth.html` — fully self-contained, no external JS.

**Flow:** Password input → SHA-256 via `crypto.subtle` (HTTPS required) → hash lookup against hardcoded registry → `sessionStorage` → redirect to subject hub.

**Session schema:**
```js
{
  name: "StudentName",
  subject: "chemistry" | "english",
  expires: Date.now() + 3 * 60 * 60 * 1000  // 3-hour TTL
}
```

**Session key:** `ga_premium_session`

**Gate on hub/quiz pages:** Check session exists AND `session.subject === 'chemistry'` (or 'english'). If not → redirect to `premium-auth.html`. This check uses `window.location.href` — the only permitted use (see Section 1).

**Passwords:** Per-student, per-subject. 8 students × 2 subjects = 16 passwords. SHA-256 hashes embedded in `premium-auth.html`. Plaintext passwords in `OWNER_PASSWORDS_PRIVATE.txt` — **never commit this file**.

---

## 11. Premium Paper Invariants

These must hold for every premium quiz paper. Verify with Python before delivering:

1. **Exactly 50 questions per paper** — no more, no fewer
2. **Answer key balanced** — A=13, B=13, C=12, D=12 per paper
3. **Zero cross-paper overlap** — no question text appears in more than one paper
4. **IDs reset to 1–50** — per paper, always start at 1
5. **Timer: 1800 seconds (30 minutes)** — `GLOBAL_SECS = 1800`
6. **No password gate** — session gate handled by hub, not quiz page
7. **Single inline `<script>` block** — JS syntax-checked with `node --check` before delivery
8. **Conservative watermark** — student name from sessionStorage, diagonal tiled, `opacity: 0.022`, no red bars

---

## 12. Dead Link Rule

No page on this site dead-ends on GitHub's 404. Every unbuilt track, every future feature, every broken link routes to `coming-soon.html`.

`coming-soon.html` must always exist and must always work with **zero JS dependencies**. It is a pure HTML/CSS page.

---

## 13. Adding a New Paper (Premium)

1. Confirm source questions (Ada file, MEPC file, or new source)
2. Run Python selection script — verify 50 questions, zero overlap with existing papers, balanced answer dist
3. Generate JS block via `esc()` — verify with `node --check`
4. Stamp into Paper 1 template via 3 string replacements (title, header, questions block)
5. Activate card in hub: `coming` → `live`, `btn-start-disabled` → `btn-start`, update href, `status-soon` → `status-live`
6. Run full cross-paper overlap check before pushing

---

## 14. Never-Do List

**CRITICAL — silent failures:**
- Never use JS for routing between pages (session gate redirect is the only exception)
- Never reference a script file that doesn't exist
- Never hand-edit any file the build script generates
- Never add unescaped special characters to question strings

**SERIOUS — data integrity:**
- Never reuse a question across papers
- Never deliver a paper without running `node --check` on its script block
- Never deliver a paper without verifying answer distribution is balanced
- Never commit `OWNER_PASSWORDS_PRIVATE.txt`

**HOUSEKEEPING:**
- Never inline CSS in premium papers except in the existing `<style>` block
- Never let any page route to GitHub's 404
- Never cross CSS scope boundaries
- Never substitute or remove fonts from the defined stack

---

## 15. Change Protocol

Before touching any file, answer three questions:

1. **What is the smallest file that owns this problem?** Only edit that file.
2. **Does this change affect the HTML boilerplate or script load order?** If yes, stop and think twice.
3. **Does this change affect build output?** If yes, rebuild and verify before pushing.
