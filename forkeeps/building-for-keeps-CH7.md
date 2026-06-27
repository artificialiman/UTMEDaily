# BUILDING FOR KEEPS
## Chapter 7: Every Single Line

*From wireframe to keystroke.*
*The four questions. The build tools. Where the idiosyncratic things go.*

---

### Before the first line

A wireframe is not a design. It is a question.

It asks: *what does this page need to show, and in what order does it need to show it?* It does not ask how. It does not ask which component. It asks only what — and the discipline of answering *what* before *how* is the discipline that separates code written with understanding from code written with momentum.

For UTMEDaily, the wireframe for the quiz page answers quickly:

```
[ Subject label          ]
[ Question counter       ]
[ Question text          ]
[ Option A               ]
[ Option B               ]
[ Option C               ]
[ Option D               ]
[ ——— after answer ———   ]
[ Score / next prompt    ]
```

Eight elements. Three states — pre-answer, post-answer, complete. One user action — selecting an option. This is the entire quiz page, described without a single line of code. Before any component is opened, the page is understood.

The wireframe is the contract. The code is the fulfilment.

---

### The four questions

Every line of code in this application answers one of four questions. Not metaphorically — literally. Every line. When a line cannot be assigned to one of these questions, it is either in the wrong file or it does not belong.

---

**1. What is this?**

The question of identity. Answered by type declarations, interface definitions, variable names, component names. Every named thing in the codebase answers this question at the moment of its naming.

```typescript
// What is this?
interface Question { ... }
let currentIndex = $state(0);
function handleAnswer(index: number) { ... }
```

`Question` is a question. `currentIndex` is a position. `handleAnswer` is a response to a user action. The names are the answer. A name that does not answer *what is this* clearly is a name that will cost someone time later — the time it takes to read the implementation to understand what the name was supposed to mean.

Name things for what they are. Not for what they do, not for what they contain, not for the type they happen to hold. For what they *are*, in the domain of the application. A quiz has questions, options, answers, scores. The code should speak that language.

---

**2. What does this own?**

The question of scope. Answered by the file a thing lives in, the component it belongs to, the module it is exported from. Ownership determines where a change must be made when something needs to change.

```
QuizOption.svelte    owns: appearance and state of one answer
QuizCard.svelte      owns: one question and its interaction
+page.svelte         owns: quiz session — progression and score
+page.js             owns: data loading and error handling
types.ts             owns: the shapes everything agrees on
app.css              owns: the visual law everything inherits
```

When a component owns too much, the question *what does this own?* cannot be answered in a sentence. This is the diagnostic. If you cannot describe a component's ownership in one sentence, the component is doing more than one job. Split it.

When ownership is clear, change is safe. You change the appearance of a correct answer in `QuizOption.svelte` and you know, with certainty, that nothing else is affected. You change the score calculation in `+page.svelte` and you know it changes for every subject simultaneously. Ownership is the map that makes the territory navigable.

---

**3. What does this show?**

The question of rendering. Answered by the markup — the Svelte template, the conditional blocks, the each loops, the component compositions. This question lives in one place per component, and it is always the bottom half of the file, below the script.

```svelte
{#if data.error}
  <p class="notice">Questions unavailable.</p>

{:else if isComplete}
  <ResultCard {score} total={data.questions.length} />

{:else}
  <QuizCard
    question={data.questions[currentIndex]}
    questionNumber={currentIndex + 1}
    total={data.questions.length}
    onAnswer={handleAnswer}
  />
{/if}
```

Three states. Three branches. Each one a complete answer to *what does this show* in the condition it handles. The markup does not compute. It does not fetch. It does not manage state. It reads state and renders the appropriate structure. The computation belongs to the script. The rendering belongs to the template. These are different jobs and they have different places.

When the markup begins to compute — when a `{#if}` condition is a complex expression rather than a derived boolean, when a loop contains logic that belongs in a function — the file has blurred the line between *what does this show* and *what does this own*. Redraw the line. Move the logic to a `$derived`. Keep the template honest.

---

**4. What does this need?**

The question of dependency. Answered by imports, props, load functions, and the type signatures that describe what flows in from outside. Every component that receives data from outside itself answers this question in its props declaration. Every page answers it in its load function.

```typescript
// What does QuizCard need?
let {
  question,        // the content
  questionNumber,  // its position
  total,           // the context
  onAnswer         // the callback
}: {
  question:       Question;
  questionNumber: number;
  total:          number;
  onAnswer:       (index: number) => void;
} = $props();
```

This declaration is a bill of requirements. The component will not function without these four things. The types describe exactly what form each thing must take. The compiler verifies that any parent component passing these props is passing them correctly.

The discipline here is minimalism. A component should need only what it cannot derive itself. If it can calculate something from what it already has, it should — using `$derived`. If it needs something from outside, it should declare it explicitly and type it completely. The dependency list should be as short as it can be while remaining complete.

A component with a long dependency list is a component that knows too much about the world outside it. Shorten the list. Push the knowledge upward, to the component that actually owns it.

---

### What each build tool resents

The build pipeline — Vite, the TypeScript compiler, the SvelteKit preprocessor — is not passive. Each tool has opinions, and the opinions are expressed as errors and warnings when you work against them. Understanding what each tool resents is understanding how to work with it rather than against it.

---

**Vite resents:**

Imports that don't resolve. A path that looks right but points to nothing produces a build error that is entirely preventable — the file either exists or it doesn't, and the import should reflect reality. Vite also resents circular dependencies — module A imports module B which imports module A — and will warn you about them, because circular dependencies produce loading order problems that are difficult to debug and entirely avoidable through good ownership decisions.

```typescript
// Vite is fine with this
import type { Question } from '$lib/types';

// Vite resents this — if the file doesn't exist
import type { Question } from '$lib/typ'; // typo
```

---

**TypeScript resents:**

Untyped anything. The implicit `any` — the type that means *I don't know and I have decided not to care* — is TypeScript's most resented pattern, and with `strict: true` enabled, it is an error rather than a warning. TypeScript also resents type assertions that override the compiler's reasoning without justification — the `as` keyword used not because you know something the compiler doesn't, but because you want the error to stop without fixing the underlying problem.

```typescript
// TypeScript resents this
const q = data.question as Question; // are you sure?

// TypeScript prefers this
if (!data.question) return;
const q: Question = data.question; // now we're certain
```

The `as` keyword is a deposition you are filing against the compiler's evidence. Sometimes the evidence is wrong and the deposition is warranted. More often, the evidence is right and the deposition is a liability — a statement that something is true that may not be, recorded in the code, forgotten by the developer, discovered by a runtime error in production.

---

**Svelte resents:**

Reactive state that is mutated without reassignment. Svelte's reactivity tracks assignments — `score = score + 1` — not mutations — `scores.push(newScore)`. Pushing to an array does not trigger a reactive update because the array reference did not change, only its contents. The fix is reassignment: `answers = [...answers, newAnswer]`.

```svelte
<!-- Svelte resents this — no reactive update -->
<script>
  let answers = $state([]);
  function add(a) { answers.push(a); }
</script>

<!-- Svelte is fine with this -->
<script>
  let answers = $state([]);
  function add(a) { answers = [...answers, a]; }
</script>
```

Svelte also resents components that reach outside their scope — that read from the DOM directly, that access `window` without `<svelte:window>`, that manage their own event listeners without letting the lifecycle handle cleanup. These patterns work, often for a long time, until they produce a memory leak or a stale closure that nobody can locate because it was never declared in a place the framework could see it.

---

### Where the idiosyncratic things go

Every application has them. The function that does something slightly strange for a good reason. The CSS rule that overrides something in a way that seems wrong until you understand why. The data transformation that exists because the source data is not shaped the way the components expect.

These things are not problems. They are honest reflections of reality — of the fact that the world is not as clean as the architecture planned for, and that the architecture must accommodate the world without becoming as messy as it.

The discipline is location. Idiosyncratic things must live in a place that signals their idiosyncrasy — a file named for its purpose, commented with its reason, isolated from the code that should remain clean.

```
src/lib/
├── types.ts          ← clean — shapes that everything agrees on
├── utils.ts          ← honest — transformations and utilities
├── quirks.ts         ← idiosyncratic — the world as it actually is
└── components/       ← clean — UI that knows its job
```

`quirks.ts` is not a real SvelteKit convention. It is mine. The name is the signal. Any developer who opens it knows: *this file contains things that required special handling, for reasons documented within.* It is not where the clean architecture lives. It is where the clean architecture goes when the world refuses to cooperate.

Comment the quirks. Not the mechanics — the reason. Future-you reading a strange function six months from now does not need to know what it does. They can read it. They need to know why it does something strange, what it was working around, and whether that constraint still applies.

```typescript
// utils.ts

/**
 * JAMB question text occasionally includes LaTeX-style notation
 * from the source .txt files (e.g. "x^2 + y^2").
 * This function normalises it to plain Unicode for display.
 * If JAMB ever supplies clean data, this function becomes a passthrough.
 */
export function normaliseQuestionText(raw: string): string {
  return raw
    .replace(/\^(\d)/g, (_, n) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[n])
    .trim();
}
```

The comment is the forensic record. It names the constraint, names the source, and names the condition under which the function becomes unnecessary. When that condition is met, the function can be removed with confidence — not because someone remembered why it was there, but because it was written down.

---

### A note on JavaScript — and where it actually belongs

This book has been measured about JavaScript. Not hostile — measured. The concern has always been specific: JavaScript used in places where the browser already provides a better primitive. Routing. Navigation. State that should be a type. Structure that should be HTML.

But JavaScript aimed correctly is a different instrument entirely.

In cyber engineering — in the environments where unpredictability is a feature, where the adversary is an intelligent system trying to find the pattern in your behaviour, where the footgun is pointed at infrastructure rather than at users — JavaScript earns a reputation that this book has not yet given it. Its dynamism, which is a liability in a quiz platform, is an asset in a system designed to be difficult to reverse-engineer. Its flexibility, which accumulates into complexity in a growing codebase, becomes a tool for writing systems that behave differently every time they are observed.

This is not the chapter for that argument. But the argument is coming — and I want you to know, before we close this one, that the position of this book is not that JavaScript is wrong. It is that JavaScript is powerful enough to be dangerous when misapplied, and specific enough in its strengths that applying it anywhere other than those strengths is a cost you will eventually pay.

The right tool for the job. The job determines the tool. When the job changes, so does the answer.

---

### The complete file, assembled

What follows is the quiz page — `+page.svelte` — written in full, annotated against the four questions. Not as a tutorial. As a demonstration that the four questions, applied consistently, produce a file that is legible, honest, and complete.

```svelte
<script lang="ts">
  // — WHAT DOES THIS NEED? —
  import QuizCard from '$lib/components/QuizCard.svelte';
  import type { Question } from '$lib/types';

  let { data } = $props(); // questions[], subject, error?

  // — WHAT IS THIS? —
  let currentIndex = $state(0);
  let answers      = $state<number[]>([]);

  // — WHAT DOES THIS OWN? —
  function handleAnswer(selectedIndex: number) {
    answers      = [...answers, selectedIndex];
    setTimeout(() => { currentIndex++; }, 800);
  }

  // — WHAT IS THIS? (derived truth) —
  let isComplete = $derived(currentIndex >= data.questions.length);
  let score      = $derived(
    answers.filter(
      (a, i) => a === data.questions[i]?.correctIndex
    ).length
  );
</script>

<!-- — WHAT DOES THIS SHOW? — -->
{#if data.error}
  <p class="notice">
    No questions found for {data.subject}.
    <a href="/">Choose another subject.</a>
  </p>

{:else if isComplete}
  <div class="result">
    <h2>{score} / {data.questions.length}</h2>
    <p>
      {Math.round(score / data.questions.length * 100)}% correct
    </p>
    <a href="/" class="home">Try another subject</a>
  </div>

{:else}
  <QuizCard
    question={data.questions[currentIndex]}
    questionNumber={currentIndex + 1}
    total={data.questions.length}
    onAnswer={handleAnswer}
  />
{/if}

<style>
  .notice { color: var(--text); padding: 2rem; text-align: center; }
  .result  { text-align: center; padding: 3rem 1rem; }
  .result h2 { font-size: 3rem; color: var(--accent); }
  .home    { display: inline-block; margin-top: 1.5rem; }
</style>
```

Every section of this file answers one question. The imports answer *what does this need.* The state declarations answer *what is this.* The function and derived values answer *what does this own.* The template answers *what does this show.* The style answers *what does this look like.*

Five sections. Five questions. One file that can be read by a developer who has never seen it before, from top to bottom, without confusion — because the structure is honest, the names are accurate, and nothing is in the wrong place.

This is what *every single line* means. Not that every line is laboured over. That every line knows where it belongs.

---

*Next: Chapter 8 — Change, Errors, Failure. Written as questions. A reader who answers them owns the architecture. A developer who cannot answer them knows where to look next.*

