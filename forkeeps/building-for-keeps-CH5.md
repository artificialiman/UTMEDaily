# BUILDING FOR KEEPS
## Chapter 5: The Living Files

*The order in which files are created is the order in which the project learns what it is.*

---

A file is not inert.

The moment you create it, it makes a claim — about what the application owns, what it knows, what it promises to do. A file created too early makes promises the project isn't ready to keep. A file created too late makes the files that came before it carry weight they were never designed for. The order matters. Not as ceremony, but as architecture.

This chapter is the creation order. Each file named in the sequence it should arrive, with the reason it arrives then and not before or after. By the end, you will have a project that knows what it is — not because you told it, but because each file you added confirmed and extended what the previous files already established.

---

### Before the first file: what you are building

You are building a quiz platform. It will serve students. It will load questions from structured data. It will present one question at a time, record answers, calculate a score, and display a result. It will do this for multiple subjects. It will be deployed as a static site on GitHub Pages. It will be fast, because the students it serves are often on slow connections. It will be durable, because you will not be rebuilding it every time a framework releases a major version.

That is the constitution. Every file that follows is a clause within it.

---

### File 1: `package.json`
**What it is:** The project's identity document.
**What it owns:** The name, the version, the dependencies, the scripts.
**Why it comes first:** Because nothing else can exist without it. This file is the project declaring itself to the Node ecosystem. Before you have a single route or component, you have a name and a set of tools you have formally agreed to use.

```json
{
  "name": "utmedaily",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

The scripts are small pieces of legislation. `dev` opens the courtroom. `build` renders the verdict. `preview` reviews it before it is filed.

---

### File 2: `svelte.config.js`
**What it is:** The project's architectural declaration.
**What it owns:** The adapter, the preprocessor, the output target.
**Why it comes second:** Because everything the framework does flows from this file. The adapter is the solicitation — `adapter-static` formally engages the tool that will produce a deployable static site. This is the retainer agreement, signed early, before any work begins.

```javascript
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: null
    })
  }
};
```

`fallback: null` is a verdict rendered early. It says: every route must be a real file. No client-side routing fallbacks. If the page does not exist, it does not exist. This is the kind of decision that saves a weekend three months from now.

---

### File 3: `tsconfig.json`
**What it is:** The mathematical constitution.
**What it owns:** The rules by which TypeScript evaluates correctness.
**Why it comes third:** Because before you write a single type, you need to establish the standard by which types are judged. A `tsconfig` without `strict: true` is a legal system that allows perjury. Write it once, make it strict, and let it hold everything that follows.

```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": {
    "strict": true,
    "moduleResolution": "bundler"
  }
}
```

`strict: true` is not pedantry. It is the refusal to negotiate with the ambiguity that produces production incidents. Every additional strictness flag you disable is a clause you removed from the constitution because it was inconvenient. Constitutions weakened for convenience do not hold under pressure.

---

### File 4: `src/app.html`
**What it is:** The one HTML file.
**What it owns:** The shell that every page inhabits.
**Why it comes fourth:** Because the project now knows its tools, its output target, and its type rules. It is ready to declare its visual container. This file exists once. The entire application renders inside `%sveltekit.body%`.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    %sveltekit.head%
  </head>
  <body>
    %sveltekit.body%
  </body>
</html>
```

In vanilla, this file was replicated across every subject — `quiz-mathematics.html`, `quiz-chemistry.html`, each one a copy of this shell with different content inside. Here it is written once. The content changes. The shell does not.

---

### File 5: `src/app.css`
**What it is:** The design system's codification.
**What it owns:** The tokens, the resets, the rules that every component inherits.
**Why it comes fifth:** Because before you build any UI, you establish the visual law. The colours, the spacing, the typographic scale — these are the decisions that must be made once and inherited everywhere. Every component written before this file exists is a component that will eventually contradict it.

```css
:root {
  --correct:   #4caf50;
  --incorrect: #f44336;
  --pending:   #757575;
  --bg:        #1e1e1e;
  --surface:   #2d2d2d;
  --text:      #f8f8f2;
  --accent:    #66d9e8;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
}
```

In Monokai, `--accent: #66d9e8` is the cyan — the same cyan that marks types and classes in the editor. This is not coincidence you engineer. It is harmony you notice and keep.

---

### File 6: `src/lib/types.ts`
**What it is:** The codification layer — the definitions section.
**What it owns:** Every shape the application will pass between its parts.
**Why it comes sixth:** Because now you are about to build components and routes, and they will need to agree on what a question is, what a session is, what a result looks like. The agreement must precede the building. Types written after components are types written to describe what already happened — archaeology, not architecture.

```typescript
export interface Question {
  id: number;
  text: string;
  options: string[];
  correctIndex: number;
  subject: string;
  year?: number;
}

export interface QuizSession {
  subject: string;
  questions: Question[];
  answers: number[];
  startedAt: number;
  isComplete: boolean;
}

export interface QuizResult {
  score: number;
  total: number;
  percentage: number;
  subject: string;
}
```

Every `?` in this file is a considered decision — a property acknowledged as optional rather than assumed as present. A `year` that may not be available for every question is not a missing value. It is a documented uncertainty. The forensic investigator — future you — will know exactly where the uncertainty was acknowledged and exactly where it was not.

---

### File 7: `src/lib/components/QuizOption.svelte`
**What it is:** The first component — the atom of the quiz UI.
**What it owns:** One answer option. Its appearance, its states, its single responsibility.
**Why it comes seventh:** Because the types exist. The design tokens exist. This component can now be written knowing what it will receive and how it will look.

```svelte
<script lang="ts">
  import type { } from '$lib/types';

  let {
    text,
    index,
    selected = false,
    correct = null,
    onSelect
  }: {
    text: string;
    index: number;
    selected?: boolean;
    correct?: boolean | null;
    onSelect: (index: number) => void;
  } = $props();
</script>

<button
  class="option"
  class:selected
  class:correct={correct === true}
  class:incorrect={selected && correct === false}
  on:click={() => onSelect(index)}
  disabled={correct !== null}
>
  {text}
</button>

<style>
  .option {
    background: var(--surface);
    color: var(--text);
    border: 1px solid transparent;
    padding: 0.75rem 1rem;
    width: 100%;
    text-align: left;
    cursor: pointer;
    border-radius: 4px;
    transition: border-color 0.15s;
  }
  .selected  { border-color: var(--accent); }
  .correct   { border-color: var(--correct); background: color-mix(in srgb, var(--correct) 15%, var(--surface)); }
  .incorrect { border-color: var(--incorrect); background: color-mix(in srgb, var(--incorrect) 15%, var(--surface)); }
</style>
```

Notice what this component does not know. It does not know the total number of questions. It does not know the subject. It does not know the score. It knows one thing: how to display an answer option in any of its four possible states — neutral, selected, correct, incorrect. That narrowness is its strength. A component that knows only one thing can be trusted completely in that one thing.

---

### File 8: `src/lib/components/QuizCard.svelte`
**What it is:** The question container — the molecule.
**What it owns:** One question with all four of its options.
**Why it comes eighth:** Because the atom — `QuizOption` — exists. The molecule assembles atoms. This is the natural order of composition.

```svelte
<script lang="ts">
  import QuizOption from './QuizOption.svelte';
  import type { Question } from '$lib/types';

  let {
    question,
    questionNumber,
    total,
    onAnswer
  }: {
    question: Question;
    questionNumber: number;
    total: number;
    onAnswer: (index: number) => void;
  } = $props();

  let selected = $state<number | null>(null);
  let revealed = $state(false);

  function handleSelect(index: number) {
    if (revealed) return;
    selected = index;
    revealed = true;
    onAnswer(index);
  }
</script>

<div class="card">
  <p class="counter">{questionNumber} of {total}</p>
  <p class="question">{question.text}</p>

  {#each question.options as option, i}
    <QuizOption
      text={option}
      index={i}
      selected={selected === i}
      correct={revealed ? i === question.correctIndex : null}
      onSelect={handleSelect}
    />
  {/each}
</div>
```

The question number. The question text. The four options, composed from the atom. State managed at the card level — `selected` and `revealed` — because the card owns the answer interaction. Not the page. Not the layout. The card.

---

### File 9: `src/routes/+layout.svelte`
**What it is:** The application shell.
**What it owns:** Everything every page inherits — navigation, global styles, the document's persistent structure.
**Why it comes ninth:** Because the components exist. The routes are about to be built. Before the first page is written, the frame that holds all pages must exist.

```svelte
<script lang="ts">
  import '../app.css';
</script>

<header>
  <a href="/" class="logo">UTMEDaily</a>
  <nav>
    <a href="/quiz">Practice</a>
    <a href="/about">About</a>
  </nav>
</header>

<main>
  <slot />
</main>

<footer>
  <p>Built for keeps. For the student who clicks Submit.</p>
</footer>
```

The layout lobbies for consistency. Every page that lives below this file in the route tree will wear this header and this footer without being asked to. The pages do not know the layout. The layout does not know the pages. The slot is where they meet, silently, without negotiation.

---

### File 10: `src/routes/+page.svelte`
**What it is:** The home page — the entry point.
**What it owns:** The first thing a student sees.
**Why it comes tenth:** Because the shell exists. The home page lives inside it.

A home page for a quiz platform is a subject selector. Nothing more. The student arrives, chooses a subject, and is routed to the quiz. The home page's only job is to make that choice clear and the routing immediate.

```svelte
<script lang="ts">
  const subjects = [
    { name: 'Mathematics', slug: 'mathematics' },
    { name: 'Chemistry',   slug: 'chemistry'   },
    { name: 'Biology',     slug: 'biology'      },
    { name: 'English',     slug: 'english'      },
  ];
</script>

<h1>Choose your subject</h1>

<ul class="subjects">
  {#each subjects as subject}
    <li>
      <a href="/quiz/{subject.slug}">{subject.name}</a>
    </li>
  {/each}
</ul>
```

The navigation is an `<a>` tag. Not a button with a click handler. Not a router function. An anchor. The browser knows what to do with an anchor. It has known for thirty years. This is the right tool for the job — used once, without negotiation, because the question was never complicated.

---

### File 11: `src/routes/quiz/[subject]/+page.js`
**What it is:** The data contract for the quiz page.
**What it owns:** The loading of questions before the page renders.
**Why it comes eleventh:** Because the page that will use this data is about to be written. The data arrives before the page. Always. A page that renders before its data is a page that lies — it shows a structure before it can show the content, and the gap between structure and content is where the user's trust goes to die.

```javascript
export async function load({ params }) {
  const { subject } = params;

  const res = await fetch(`/data/${subject}.json`);

  if (!res.ok) {
    return { questions: [], error: true };
  }

  const questions = await res.json();

  return { questions, subject };
}
```

The `if (!res.ok)` is a verdict rendered before the page exists. The empty state is handled here — at the data layer — so that the page never has to wonder whether it received something or nothing. It receives a defined shape. Always. The type it was promised.

---

### File 12: `src/routes/quiz/[subject]/+page.svelte`
**What it is:** The quiz page — the thing the student sees.
**What it owns:** The quiz session, the progression through questions, the final result.
**Why it comes last in this sequence:** Because everything before it exists to make this file simple. The types describe what it receives. The components handle what it displays. The load function guarantees what it is given. The layout provides what it sits inside. This file should be the easiest file in the project to write, because eleven files came before it and did the work it would otherwise have had to do itself.

```svelte
<script lang="ts">
  import QuizCard from '$lib/components/QuizCard.svelte';
  import type { Question } from '$lib/types';

  let { data } = $props();

  let currentIndex = $state(0);
  let answers      = $state<number[]>([]);

  function handleAnswer(index: number) {
    answers = [...answers, index];
    setTimeout(() => {
      currentIndex++;
    }, 800);
  }

  let isComplete = $derived(currentIndex >= data.questions.length);
  let score      = $derived(
    answers.filter((a, i) => a === data.questions[i]?.correctIndex).length
  );
</script>

{#if data.error}
  <p>Questions unavailable. Please try another subject.</p>

{:else if isComplete}
  <div class="result">
    <h2>You scored {score} of {data.questions.length}</h2>
    <a href="/">Try another subject</a>
  </div>

{:else}
  <QuizCard
    question={data.questions[currentIndex]}
    questionNumber={currentIndex + 1}
    total={data.questions.length}
    onAnswer={handleAnswer}
  />
{/if}
```

Three states. Error. Complete. Active. Every possible state of this page is handled, named, and rendered appropriately. There is no blank screen. There is no undefined rendered as empty. Every verdict was written before this file shipped.

---

### The order as argument

Read the sequence again, not as a list of files but as a progression of commitment:

The project names itself. Declares its output. Establishes its type rules. Wraps its pages in one shell. Sets its visual law. Defines its data shapes. Builds its smallest UI unit. Assembles the unit into a card. Frames every page in a layout. Opens its front door. Loads its data. Renders its primary experience.

Each file made the next file possible. None of them were neutral. Every creation was a constitutional clause — a statement about what the application is and what it is not, written into the structure before the structure could be misread.

This is what it means to build a living codebase. Not one that changes constantly, but one that knows what it is — and makes that knowledge available to every developer, every component, every student who arrives expecting it to work.

It was written in this order because this order is the argument.

---

*Next: Chapter 5.5 — The Side-by-Side. The same application, in vanilla. An honest comparison. Subtle hints as to which is better at what — and a table at the end that does not declare a winner, because the conditions matter more than the verdict.*

