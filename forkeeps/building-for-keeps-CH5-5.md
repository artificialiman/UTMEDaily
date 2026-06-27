# BUILDING FOR KEEPS
## Chapter 5.5: The Side-by-Side

*An honest comparison. Subtle hints as to which is better at what.*
*No verdict. Conditions.*

---

Before this chapter begins, a confession that is also a credential.

I am not a lawyer. I have never entered a courtroom. I have never filed a brief, cross-examined a witness, or stood before a judge with anything at stake. Every legal framework in this book — the codification, the solicitation, the lobbying, the forensics, the verdicts — came from television. From writers who, I will say plainly, do a considerably better job portraying the legal mind than television has ever done portraying the developer one.

I watched the thinking. I recognised it. I kept it.

This is, I think, the most honest demonstration of the book's central argument: you do not need to be credentialed in a discipline to use its best ideas. You need to understand what the ideas are actually doing — underneath the vocabulary, underneath the setting, underneath the drama — and then apply them where they fit.

The developer who has never taken a computer science course but understands closure is a better developer than the one who passed the exam and still writes untypes functions. The thinker who borrowed from law without entering a courtroom built a more durable architecture than the one who treated frameworks as fashion.

Sensibility over badge-hunting. Every time.

Now — the side-by-side.

---

### What we are comparing

The UTMEDaily platform, in two forms.

The form it was: plain HTML, shared CSS, a JavaScript file that grew because there was nowhere else to put things, one HTML file per quiz subject, navigation managed by hand, state managed by the DOM.

The form it became: SvelteKit, TypeScript, components, routes as folders, data loaded before render, one shell for the whole application, static output to GitHub Pages.

Same students. Same questions. Same purpose. Different architectures.

The comparison will not be fair — no honest comparison is. Each architecture has genuine advantages that the other genuinely lacks. The goal is not to arrive at a winner. It is to arrive at conditions — the specific circumstances under which each approach is the right tool for the job.

---

### Starting a new subject

**Vanilla:**

To add Chemistry to the platform, you create `quiz-chemistry.html`. You copy the structure from `quiz-mathematics.html`. You update the title. You update the subject variable at the top of the embedded script. You make sure `quiz-app.js` is included in the `<head>`. You make sure `quiz-styles.css` is included. You add a link to the new page from `science_clusters.html`. You test that the link works. You test that the questions load. You discover that the script expects a variable name that you spelled differently in this copy. You fix it.

Six steps, one of which contains a silent error that only reveals itself at runtime.

**SvelteKit:**

You create `src/routes/quiz/chemistry/+page.svelte`. You copy `+page.js` from an adjacent subject folder and change nothing, because the load function uses `params.subject` dynamically. You add `{ name: 'Chemistry', slug: 'chemistry' }` to the subjects array on the home page.

Two steps, one of which is a single line in an existing file.

*The subtle hint:* the SvelteKit version does not require you to remember what the vanilla version requires you to remember. The convention holds the knowledge so the developer doesn't have to. At two subjects, this difference is minor. At twelve subjects, it is the difference between a platform that grows cleanly and one that accumulates small inconsistencies until one of them becomes a visible defect in front of a student.

---

### Changing the appearance of a correct answer

**Vanilla:**

The correct answer state is styled somewhere in `quiz-styles.css`. You find it. You change it. You open every quiz HTML file in a browser to verify the change applied. You discover that one quiz file was loading a different version of the CSS because someone added an inline style override at some point, for a reason that is no longer obvious.

**SvelteKit:**

The correct answer state is styled in `QuizOption.svelte`, using `var(--correct)` from `app.css`. You change the value of `--correct` in `app.css`. Every component that references it updates. You open one page in the browser. The change is everywhere.

*The subtle hint:* vanilla CSS works. Shared stylesheets work. The problem is not the CSS — the problem is the discipline of using it consistently across multiple files that each make their own decisions about what to include and what to override. SvelteKit does not make inconsistency impossible. It makes consistency the path of least resistance. This is the architecture lobbying for the right decision.

---

### Handling a broken data load

**Vanilla:**

`quiz-app.js` fetches question data. If the fetch fails, the script throws an error. The error is caught — or it isn't — in a try/catch that may or may not exist depending on when the file was written and whether the developer was thinking about failure at that moment. The student sees either an empty quiz or a JavaScript console error that she was never meant to see.

**SvelteKit:**

The `+page.js` load function returns `{ questions: [], error: true }` when the fetch fails. The `+page.svelte` has an `{#if data.error}` branch that renders a clear, human message. The student sees: *Questions unavailable. Please try another subject.* The error was handled at the data layer, before the page existed, by a developer who was thinking about failure when it was still cheap to think about it.

*The subtle hint:* SvelteKit does not make error handling automatic. It makes the right place for error handling obvious — the load function, before render — and separates it from the component that renders the result. In vanilla, the right place for error handling is wherever the developer happened to be when they remembered to add it. These are not equivalent disciplines.

---

### Reading the codebase six months later

**Vanilla:**

You return to `quiz-app.js`. It is four hundred lines long. The first hundred handle quiz initialisation. The next hundred handle answer selection. Somewhere in the third hundred, there is logic that changes behaviour based on which page loaded the script — identified by checking `document.title`, or a global variable set in the HTML file, or a query parameter that was added for a reason the comment does not explain. The fourth hundred lines are a mixture of utility functions and event listeners that were added over time, each one reasonable in the moment, collectively forming a system that cannot be summarised in a sentence.

You need to change how the score is calculated. You find the calculation. You change it. You test it on the Mathematics page. You deploy. Two weeks later, you discover that Chemistry calculated scores differently because there was a second calculation buried in a subject-specific code path that you did not know existed.

**SvelteKit:**

You return to `src/routes/quiz/[subject]/+page.svelte`. It is eighty lines. The score is calculated in one `$derived` expression. You change it. It changes for every subject simultaneously, because every subject uses the same page component. The change is complete. The test is one page. The confidence is total.

*The subtle hint:* the vanilla version did not become difficult because of bad decisions. It became difficult because the architecture had no mechanism for enforcing separation of concerns — no natural place for each kind of logic to live that wasn't the same file where everything else already lived. SvelteKit does not enforce separation by law. It enforces it by making separation the obvious structure and everything else the workaround.

---

### What vanilla is genuinely better at

Honesty requires this section.

**Immediacy.** Open a text editor. Write HTML. Open it in a browser. Done. No build step. No config. No `npm install`. No waiting. For a single page, for a prototype, for a thing that will exist for one week and then be discarded, vanilla is the right tool. SvelteKit is infrastructure for a platform. Infrastructure for a page is overhead.

**Portability.** An HTML file can be emailed. It can be opened on any device with a browser. It requires no server, no build output, no understanding of what a `+page.svelte` is. There are real use cases for this — educational materials, one-off tools, documents that need to function independently of any platform.

**Legibility to non-developers.** A designer who knows HTML can read a vanilla template directly. They can find the class they want to change. They cannot necessarily read a Svelte component — not because Svelte is difficult, but because it adds a layer of abstraction that is invisible to someone who learned the web without frameworks. For a project that will be maintained by people who know HTML but not SvelteKit, vanilla may be the more durable choice, paradoxically — because the team can actually read it.

**No compilation.** The vanilla project that was UTMEDaily deploys directly to GitHub Pages as files. No build step, no generated output, no possibility of a build error blocking a deployment. When the compilation step is a risk you are not equipped to debug, the compilation step is a cost that may exceed its value.

---

### What SvelteKit is genuinely better at

**Scale without accumulation.** Each new subject is a folder. The folder does not know about the other folders. The other folders do not know about it. The platform can grow indefinitely without any single file accumulating the knowledge of the whole.

**Change without archaeology.** A design change propagates through tokens. A behavioural change propagates through components. A data change propagates through types. The developer who changes something knows where the change lives and what it will affect. This is not a small advantage. This is the difference between maintaining a platform and managing a codebase.

**Error handling as structure.** The load function separates data concerns from rendering concerns. The page knows what to show. The loader knows what to fetch and what to do when the fetch fails. These are different jobs. Keeping them in different files keeps the thinking clear.

**TypeScript as law.** The types describe what the application has agreed to. The compiler enforces the agreement. A broken contract produces an error before a user ever sees it. This is not a preference. For a platform serving ten thousand students, this is the minimum viable discipline.

---

### The agreement table

*Neither wins. Conditions decide.*

| Condition | Vanilla | SvelteKit |
|---|---|---|
| Single page, no growth planned | ✓ Better | — Overhead |
| Platform with multiple subjects | — Accumulates | ✓ Better |
| Team unfamiliar with frameworks | ✓ Legible | — Learning curve |
| Solo developer, long maintenance | — Archaeology | ✓ Better |
| Prototype in an afternoon | ✓ Better | — Setup cost |
| Production platform, real users | — Fragile at scale | ✓ Better |
| No build step acceptable | ✓ Better | — Requires build |
| Design system must be consistent | — Manual discipline | ✓ Better |
| Error states must be handled | — Ad hoc | ✓ Better |
| Deploy to GitHub Pages, static | ✓ Native | ✓ With adapter |

The vanilla project that UTMEDaily started as was not wrong. It was right for what it was at the time it was built — a working prototype that proved the concept, loaded the questions, displayed the quiz, and showed that students would use it. That is exactly what a vanilla project is for.

SvelteKit does not make the vanilla version wrong retroactively. It makes the better version accessible — the version that can serve ten thousand students without the developer spending their weekends debugging an inconsistency introduced when the ninth subject was added at midnight.

The tool changed because the job changed. That is not a betrayal of the original. It is the original's success, demanding a worthy successor.

---

*Next: Chapter 6 — The Routes. HTML routing versus JavaScript routing. Why `<a href>` is thirty years of infrastructure, and why the cost of replacing it never appears in the tutorial.*

