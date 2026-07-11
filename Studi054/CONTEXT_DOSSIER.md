# Context Dossier: Report Page / Transcript Business
**Prepared for: collaborating agents on this project**
**Owner: Manchi (Studi054 Systems) — GitHub: artificialiman**
**Repo: UTMEDaily**

---

## 1. What this project is

A system that turns raw CSV broadsheets (exported from a separate school-admin
site and a teacher's results site) into individual, password-gated **student
report/transcript pages** — one page per student, viewable online.

This is a **paid service business**: schools generate CSVs elsewhere, and this
project's job is to synthesize those CSVs into polished, print-ready,
web-hosted transcripts carrying the school's own branding.

Right now the CSV → report-page step is done **manually**. Part of the
ongoing work is building repeatable tooling to shorten that manual step
without losing per-school customization (letterhead, watermark, grading
scale, subject list all differ by client).

---

## 2. Current client in focus: Tender Care Comprehensive College (TCC)

- **Full name:** Tender Care Comprehensive College
- **Address:** Kamalo Labori Sagamu Road, Gbaga, Ogun State
- **Phone:** 08149135960 / 08085042982
- **Term in scope:** Second Term Examination
- **Class in scope:** SS3 Science (a graduating class)

### Brand assets on file
| Asset | Path in repo | Notes |
|---|---|---|
| Logo (vector, traced) | `Studi054/Tccsvg.svg` | Potrace-traced silhouette, single-fill (`#000000`), viewBox `0 0 312.517888 359.467970`. Solid single-color shape — ideal for a low-opacity watermark since it's not a multi-color raster. |
| Logo (raster, as used in Word letterhead) | inside `11teenth/TENDER CARE HEADER -ORG.docx` → `word/media/image1.jpeg` | The crest as it currently appears on the school's official exam letterhead. |
| Letterhead reference doc | `11teenth/TENDER CARE HEADER -ORG.docx` | Header layout: crest image, "TENDER CARE" + "COMPREHENSIVE COLLEGE" title, address line, phone line, "SECOND TERM EXAMINATION", then subject/duration/class fields. This is the print letterhead pattern already in use for TCC exam papers — the web report page should echo this identity (not necessarily this exact layout). |

**Explicit design requirement:** the TCC logo must appear as a **watermark
on every generated page** (not just a header logo) — low-opacity, behind
content, on all student report pages for this client.

---

## 3. Data: SS3 Science broadsheet

**Source file:** `Notes/broadsheet_SS3_Science_2026-06-10 (1).csv`

- 22 student rows (S/N 1–22), 2 header rows (subject names, then
  CA/Exam/Total/Max sub-columns).
- **Student ID format:** `TCH-2025-###` (sequential).
- **Columns per subject:** CA (max 30) / Exam (max 70) / Total (max 100).
- **Subjects listed in header:** English, Mathematics, Physics, Chemistry,
  Biology, Further Math, History, Agriculture, Livestock, Commerce,
  Marketing, Citizenship and Heritage, Economics, Data Processing.
- **Subjects actually populated for this class:** English, Mathematics,
  Physics, Chemistry, Biology, Citizenship and Heritage, Economics —
  the rest (History, Agriculture, Livestock, Commerce, Marketing, Further
  Math, Data Processing) are blank for every student in this file, meaning
  this Science-track class wasn't offered/scored on those subjects.
- **Summary columns:** `Sum of Totals`, `Overall Grade` (letter grades seen:
  D7, E8, F9 — WAEC/NECO-style grading scale).
- **Incomplete rows:** 2 students (Dorcas – S/N 4, Habitat – S/N 10) have
  no scores at all — likely absent/withdrawn; needs confirmation before
  generating their report page (blank transcript vs. exclude vs. flag).

This CSV is the direct input for the SS3 Science round of transcript
generation.

---

## 4. Data: full class roster (as of this pass)

The repo's `Notes/` folder contains 9 broadsheet CSVs across 5 classes:
JSS1A, JSS3B, SS1 Actuarial, SS1 Science, SS3 Science. All but JSS1A have
**two versions** of the same class (a plain filename and a `(1)` suffixed
one).

**Important — do not auto-merge duplicate versions.** For every class with
two versions, the pair is NOT a true duplicate: each version has a
different subset of students populated vs. blank (e.g. one file has rows
1–3 blank and 11–21 scored, the other has the opposite). The real broadsheet
for that class is effectively the union of both files, but the merge isn't
always simple positional overlap (seen one case, SS1 Actuarial, where a
student's row shifted rather than lining up 1:1). **Policy: Claude does not
attempt to merge these automatically. Manchi will supply the merged/clean
file per class when needed.** Treat any two-version class as incomplete
until a merged file is provided.

**Column schema is consistent in structure, but subject list varies by
class/track** — this confirms the multi-school/multi-class scaling risk
flagged earlier:
- JSS1A / JSS3B (junior classes): Basic Science, CCA, CRS, IRS,
  Horticulture, PHE, Yoruba, French, plus DT/BT (JSS1A) or NVE/Computer
  (JSS3B).
- SS1 Actuarial: Government, Accounting, Literature — no Physics/Chemistry.
- SS1 Science / SS3 Science: Physics, Chemistry, Further Math (science
  track).

Generator logic must read whichever subject columns are actually populated
for a given class file, not assume a fixed subject list across all classes.

---

## 5. Access & security requirements

- Each student's report page is **individually password-gated**.
- **Passwords already exist / are already assigned per student** — this is
  not a new feature to design, it's an existing constraint to build around.
  Do not propose a fresh auth scheme; integrate with what's already set.
- Student **portrait photo** is shown on each page, but must be delivered in
  the **least intrusive, most load-efficient way possible** — i.e.
  prioritize lazy-loading, compressed/appropriately-sized images, and avoid
  anything that blocks or slows initial page render. This is a hard
  constraint, not a nice-to-have.

---

## 6. House style / conventions carried over from adjacent projects

(For consistency — these are established patterns in Manchi's broader
Studi054 / UTMEDaily body of work, not necessarily mandates for this
specific project, but useful defaults absent other instruction.)

- **HTML/CSS-first, browser-to-print pipeline** preferred over native
  document formats when layout control matters.
- For anti-malpractice exam docs, a known technique is direct **docx XML
  manipulation** (unpack → splice between letterhead and `sectPr` → repack)
  to preserve watermarks/formatting without library abstraction — relevant
  if transcripts are ever also needed as downloadable/printable Word docs.
  Given this project already has a raw watermark-bearing docx letterhead
  reference, this route is available if a print/Word export of transcripts
  is later requested.
  - Pandoc reads docx as markdown; XML unpack path is used for surgical
    edits that preserve formatting exactly.
- **Dark-glass UI aesthetic** (inspired by `index.html` in the Testy repo)
  is Manchi's preferred visual direction for dashboards/admin tools in this
  ecosystem — worth checking against Gracefield's `gracefield.css` design
  language if TCC wants something in the same family, though TCC has its
  own identity (crest, address, phone) that should take precedence for
  this client's transcripts.
- GitHub raw URL fetching (`raw.githubusercontent.com/...`) is the
  established pattern for referencing design systems/templates across
  projects.
- Communication style: terse, directive, execution-over-explanation.

---

## 7. Remarks: AI-generated, not human-authored

Both remark fields on the report page are **AI-generated at build time**,
once per CSV row, and baked into the static HTML (not generated live at
page-view time — no runtime API dependency).

- **Teacher's comment** = behavioral recommendations, generated from the
  student's performance pattern.
- **Principal's comment** = student-friendly result analysis — plain,
  encouraging language, written *to* the student as primary reader (not to
  the parent), summarizing how the term went.

**Signal to drive generation, per student:**
- Margin between the student's highest and lowest subject score.
- The student's average compared to the class average (i.e. class-level
  aggregates must be computed once per class/CSV before per-student
  generation, so each student's remark can reference relative standing).

**Tone requirement:** very warm, and concise. Not clinical, not padded.

**Implication for the pipeline:** class-average and other cohort-level
stats (high/low margin per student, class average) need to be computed as
a **pre-pass over the whole class CSV** before remark generation runs, since
remarks are comparative (student vs. class), not just derived from a single
row in isolation. This pre-pass output (per-student margin + class-average
comparison) becomes the actual input to the generation prompt, not the raw
CSV row.

**Guardrail to design in before scaling:** since this is student-facing and
carries the principal's formal sign-off, generation should be constrained
against factual errors (e.g. praising a subject the student failed) —
worth deciding whether to spot-check generated output before full rollout,
even though the design intent is zero manual review at steady state.

---

## 8. Scaling plan (5,000 students, multiple schools)

Agreed order of operations — do not jump straight to full scale:

1. **Class-by-class first.** One template (`reportSP_v2.html` as base),
   one generator script per class: CSV row → rendered HTML file, keyed by
   Student ID. Remarks generation (see §7) plugs in here as a pre-pass
   (class aggregates) + per-row generation step, run once at build time.
2. **Multi-class, multi-school next.** This is a config problem, not a new
   template: each school's identity (letterhead text, crest asset, address,
   phone, grading scale) becomes injected variables. Must confirm whether
   all schools/classes share one CSV column schema before assuming one
   generator script works everywhere — this is the most likely hidden
   source of manual work at this stage.
3. **Full 5,000-student scale last**, after 1 and 2 are proven on at least
   one full school.

This section reflects agreed direction, not yet built.

---

## 9. Open questions / things to confirm before building

1. What should happen to the 2 blank-score students (Dorcas, Habitat) —
   generate an empty/placeholder transcript, or exclude them entirely?
2. Where do student portrait photos currently live (path/CDN/repo folder)?
   Not yet located in this dossier pass.
2b. What is the actual password mechanism already in place (per-student
   static password list? hashed? tied to Student ID?) — needs the existing
   implementation, not a new design.
3. Is the target output web-only, or does TCC also need a printable/Word
   version of the transcript (same watermark logic would carry over from
   the docx XML-splice pattern used elsewhere)?
4. Confirm whether "Overall Grade" scale (F9/E8/D7/…) needs a legend on the
   report page itself (likely yes, for parent-facing clarity).

---

## 10. Summary for a new agent picking this up

You're building **one HTML report page per student**, for TCC's SS3 Science
class, Second Term, from a CSV broadsheet. Every page is password-gated
(passwords already exist — just wire into them), shows the student's
portrait as lightly/efficiently as possible, and carries the TCC crest
(`Tccsvg.svg` or the letterhead JPEG) as a **background watermark on every
page**, echoing the identity already established in TCC's official exam
letterhead (address + phone + crest). Grading data comes straight from the
broadsheet CSV — CA/Exam/Total per subject plus Sum of Totals and Overall
Grade.
