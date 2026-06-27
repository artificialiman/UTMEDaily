# BUILDING FOR KEEPS
## Chapter 3: UI/UX, DX/DI — Who Does the Work So Others Don't Have To

---

There is a kind of generosity that operates beneath the surface of every well-built thing.

You feel it when a door opens the way your hand expected it to — when the handle is shaped for a grip before you consciously formed one. You feel it when a sentence ends exactly where your breath does. You feel it in software when a button is where you looked before you looked, when an error message tells you not just what broke but what to do next, when a page loads so cleanly that you forget it loaded at all. This generosity is not accidental. Someone put it there — quietly, deliberately, usually without credit — so that you wouldn't have to work for something that shouldn't require work.

This chapter is about who that someone is. In software, the answer is layered, and each layer of the answer is a discipline with its own name.

---

### Four initials and what they actually mean

**UI** — User Interface. The surface. What a person sees, touches, reads, and clicks. The button. The form. The colour of the error state. The spacing between the question and its four possible answers. UI is the frontier between the human and the machine, and everything that happens at that frontier is either a small welcome or a small rejection.

**UX** — User Experience. Not the surface — the journey across it. Not the button, but the sequence of states that leads a person to press it with confidence rather than hesitation. UX is the architecture of feeling: the way a form makes you feel capable, or makes you feel interrogated. The way a loading state makes you feel attended to, or abandoned. UX is what the user carries away after the interface has gone dark.

**DX** — Developer Experience. The same questions, asked one layer inward. What does it feel like to build this thing? Is the file structure legible? Do the errors point at the problem or perform obscurity? Is the boilerplate honest? When something breaks, can you find it in under a minute? DX is UX for the person who builds the UI — and it is just as consequential, because a developer in friction produces software in friction.

**DI** — Developer Interface. The API. The component contract. The function signature. The shape of the thing another developer touches when they use what you made. If UX is the journey, DI is the map you hand to the next cartographer. A clean DI means the next person doesn't have to reverse-engineer your thinking. They read the interface and the interface speaks.

---

These four are not separate concerns. They are a single concern at four different distances from the human being who, eventually, will sit with a phone and a quiet kind of hope and try to answer a question correctly.

The student does not know what a component is. She knows whether the quiz feels fair.
The developer does not know what she felt. He knows whether the component was easy to write.
The architect does not know what the developer felt. She knows whether the system made good components easy to write and bad ones hard.

Every layer is in service of the one further from the machine. This is the direction of generosity in software — it flows outward, toward the human, and it is built inward, toward the foundation.

---

### The five levels — a stack made of decisions

I think of UI/UX/DX/DI not as a flat list of concerns but as a vertical stack. Each level performs work that the level above it inherits. Each level, when it does its job well, makes the next level lighter. When it does its job poorly, the weight falls upward — and eventually, it lands on the user, who should never have had to carry it.

---

**Level 1 — The design system: decisions made once**

At the foundation is the decision about what things look like and why. Colours, typographic scale, spacing units, border radii, the specific shade of red that means *wrong* and the specific shade of green that means *correct*. These are not aesthetic choices. They are contracts. Once they are made, every layer above inherits them without negotiating them.

In UTMEDaily, this level lives in `quiz-styles.css`. A shared stylesheet that every quiz page loads. The colour of a correct answer is decided once, in one place, and every quiz in every subject honours it. A student who moves from Mathematics to Chemistry does not have to learn a new visual language. The consistency is the welcome.

In SvelteKit, this level can live in `src/app.css` — global styles that the layout inherits — or in design tokens, CSS custom properties declared at `:root` and referenced everywhere below. The mechanism differs from vanilla. The discipline is identical.

```css
:root {
  --correct: #4caf50;
  --incorrect: #f44336;
  --neutral: #2d2d2d;
  --text: #f8f8f2;
}
```

Four lines. Every component that references these variables is speaking the same language. Change `--correct` once and every correct answer on every page changes with it. This is DX in its quietest form — you made a decision so that future-you, or someone else entirely, would not have to make it again in a moment of distraction.

---

**Level 2 — The component: decisions made reusable**

Above the design system is the component — the unit of UI that holds a piece of behaviour and a piece of appearance together, names them, and offers them to anyone who needs them.

A component is a promise. It says: *give me this, and I will give you that, and I will look like this, and I will do it the same way every time.* A `QuizOption` component that receives a string and an `isCorrect` boolean and renders a styled, interactive answer option — that is a promise kept four times per question, dozens of times per quiz, thousands of times across the platform.

The component's value is not that it saves typing. It is that it localises decisions. If the answer option needs a hover state, that decision lives in one file. If the correct-answer colour needs to change, it changes in one file. The student sees the change everywhere. The developer made it once.

```svelte
<script>
  let { text, isCorrect, onSelect } = $props();
</script>

<button
  class="option"
  class:correct={isCorrect}
  on:click={onSelect}
>
  {text}
</button>
```

This component knows three things: what to display, whether it is correct, and what to do when clicked. It knows nothing else. This is not minimalism for its own sake — it is the discipline of scope. A component that knows too much becomes a component that is hard to reuse, hard to test, and hard to reason about when something goes wrong. Narrow knowledge is durable knowledge.

---

**Level 3 — The layout: decisions made structural**

A layout is what happens when several pages need to agree on something without talking to each other.

In vanilla, this agreement is manual — a nav bar copied into every HTML file, a footer pasted at the bottom of each, a CSS file included in every `<head>`. The agreement holds as long as no one forgets. It breaks the moment someone updates the nav on nine files and misses the tenth.

In SvelteKit, the layout is a file: `+layout.svelte`. It wraps every page below it in the file tree. It renders once. It holds the nav, the footer, the shared state, the font, the scroll behaviour — everything that belongs to the shell rather than the page. The page renders inside it without knowing or caring what the shell contains.

```svelte
<!-- src/routes/+layout.svelte -->
<nav>
  <a href="/">Home</a>
  <a href="/quiz">Practice</a>
</nav>

<slot />

<footer>UTMEDaily — built for keeps.</footer>
```

`<slot />` is where the page goes. The page doesn't know about the nav. The nav doesn't know about the page. The layout holds the relationship so neither of them has to.

This is structural DX: the developer who writes a new quiz page writes only the quiz. The shell is already there. The agreement was made at the layout level and the page inherits it without lifting a hand.

---

**Level 4 — The route: decisions made navigable**

Navigation is older than the web. It is older than software. The instinct to know where you are, how you arrived, and how to leave — this is not a UX pattern. It is a human need.

A route, well designed, answers all three. It tells the user where they are through the URL, which is honest and legible — `utmedaily.com/quiz/mathematics` says more than any breadcrumb component ever will. It records how they arrived, implicitly, in the browser's history. It makes leaving effortless through the back button, which the browser provides for free if you let it.

In vanilla, routing is a file system and a set of links you maintain by hand. In SvelteKit, routing is the same file system — but the framework reads it. You create `src/routes/quiz/mathematics/+page.svelte` and the URL `/quiz/mathematics` exists. You did not register it. You did not map it. You filed it, and the framework understood.

The DX here is the absence of a step. There is no routing table. There is no `app.js` with a switch statement. There is a folder, and the folder is the route, and the route is the URL, and the URL is what the user sees in the address bar and trusts or does not trust based on whether it looks like it knows where it is going.

A URL that knows where it is going is a small piece of confidence given to a user who is already doing the hard work of learning something.

---

**Level 5 — The data contract: decisions made honest**

The deepest level is the one most beginners defer the longest, and the deferral always costs something eventually.

Data has a shape. A question has text, options, a correct answer, maybe an explanation. A student has a score, a subject, a session. These shapes are real whether or not you name them — but if you don't name them, you discover them in the moment something breaks, which is the worst possible time for discovery.

TypeScript is the tool for naming these shapes. But the discipline underneath TypeScript is older than TypeScript: it is the commitment to knowing what you are passing before you pass it, and to making that knowledge visible to everyone who will ever touch the code.

```typescript
interface Question {
  id: number;
  text: string;
  options: string[];
  correctIndex: number;
}
```

This interface is not code that runs. It is a contract that holds. Every component that receives a `Question` now knows what a question is. The editor knows. The compiler knows. Future-you knows, six months from now, when you have forgotten what you were thinking in the moment you wrote it.

In Monokai, this interface declaration is a study in colour clarity: `interface` in **purple** — it governs. `Question` in **blue** — it describes. The property names in **white** — they hold. The type annotations in **blue** again — they describe what the holders contain. The whole thing reads as a map of roles before you read it as code.

The data contract is the furthest point from the user and the closest point to truth. When it is right, every level above it is easier. When it is wrong — or worse, when it is absent — every level above it is secretly load-bearing in ways it was never designed to be.

---

### Who does the work

Let me answer the chapter's question directly, because it deserves a direct answer.

The designer does the work of Level 1, so the developer doesn't have to decide colours under deadline.
The component author does the work of Level 2, so the page author doesn't have to rewrite behaviour they've seen before.
The layout author does the work of Level 3, so every page author inherits a shell they didn't have to build.
The router — in SvelteKit's case, the framework itself — does the work of Level 4, so the developer only has to name the destination.
The type author does the work of Level 5, so everyone above them works with known quantities rather than assumptions.

And all of them, together, do the work so that the student — who knows none of this, who should know none of this — can click an answer at eleven o'clock at night and feel that the software is on her side.

That feeling is not accidental.
It is the accumulated generosity of every decision made well, at every level, by someone who understood that the work they were doing would eventually be invisible — and did it carefully anyway, precisely because of that.

---

### The abstraction failure modes

I want to name what goes wrong at each level, because knowing the failure is part of knowing the discipline.

Level 1 fails when the design system is inconsistent — when `--correct` means different things in different components, or when it doesn't exist and every component decides for itself. The user feels this as visual noise. The developer feels it as dread when asked to change a colour.

Level 2 fails when the component knows too much — when a `QuizOption` also manages the score, also knows the total number of questions, also decides when to show the results screen. The component becomes a place where everything happens, which means it is a place where nothing can be changed safely.

Level 3 fails when the layout doesn't exist — when shared structure is copy-pasted instead of inherited. The platform holds until someone updates nine files and misses the tenth, and the student on the tenth page sees something different and wonders, briefly, if she is in the right place.

Level 4 fails when routing is JavaScript — when navigation is a function call instead of a link, when the URL doesn't reflect where the user is, when the back button does something unexpected. The student presses back and arrives somewhere wrong and the trust that took a hundred correct interactions to build dissolves in one.

Level 5 fails when the data contract is absent or dishonest — when a function receives *something* and hopes it has the right shape. The failure here is usually silent until it isn't, and when it isn't, it is loud in the worst place: production, under load, in front of a student who just wanted to practice Chemistry.

---

### A word about CSS, since this is the right moment

I said in the preface that CSS is the most satisfying layer of the stack. I want to say more than that here, because I think the satisfaction is instructive — it is not just a feeling, it is a signal.

CSS gives you immediate feedback. You change a property and the result is there, in front of you, before you have formed a complete thought about what you expected. This immediacy trains a particular kind of thinking — iterative, visual, responsive to what you see rather than what you predicted. It is the closest thing in software development to working with your hands.

The community that has formed around CSS is, in my experience, unusually generous. The people who write about CSS write to share — they write about what they discovered, what surprised them, what they got wrong. There is less performance in CSS writing than in JavaScript writing. Less status. The subject does not attract the same economy of conferences and certifications and framework migrations. It is, perhaps because of this, a cleaner discipline.

And CSS barely has a boilerplate. You do not configure it. You do not instantiate it. You write a rule, and the rule holds. This is the quiet proof that a tool at Level 1 — the design system, the foundation — does not need to be complex to be powerful. It needs to be honest. CSS is honest. It does exactly what you tell it to do, no more and no less, and when it surprises you, the surprise is always in your understanding of what you told it, not in some hidden behaviour you couldn't have known about.

I think about CSS the way Buffett talks about businesses with simple, durable models. You can understand it fully. Its behaviour is predictable over time. It does not require constant maintenance to remain useful. These are not glamorous qualities. They are the best qualities.

---

### Before the next chapter

Chapter 4 will go deeper — into the mathematics, the grammar, and the law of the stack. These are not metaphors. They are three genuine disciplines that describe what programming actually is, and understanding them changes not what you build but how you think about building.

But the ground for that chapter was laid here, in this one. Every level of abstraction we walked through — from the design token to the data contract — is a small act of discipline in service of a large act of care. The mathematics will describe the types. The grammar will describe the interfaces. The law will describe the contracts.

All of it points outward. All of it ends at the user.

The user who, at some level, simply wants the right answer to be green.

---

*Next: Chapter 4 — Mathematics, Grammar, Law. The three disciplines of programming. Why types are proofs, interfaces are sentences, and architecture is legislation. And what it means to write a constitution for a codebase.*

