# BUILDING FOR KEEPS
## Chapter 1: Boilerplate — What the Framework Assumes Before You Speak

---

Svelte is about components.
SvelteKit is about routes and data.
Vanilla is about you managing both, yourself, every time.

That is the whole matchup. Everything else in this chapter is just those three sentences learning to breathe.

---

### What I needed to understand first

Before I wrote a single file, I needed to know what each of these three things *is* — not what it does, but what it *is*. Because a tool that you don't understand is just a habit waiting to become a liability.

So I asked the questions a beginner might reach after asking eleven others first.

---

**What is Svelte, actually?**

Svelte is a compiler. You write components — a piece of UI, some behaviour, some style — and Svelte turns that into plain JavaScript at build time. Not at runtime. At build time.

This matters because most frameworks send their engine to the browser and let it do the work. Svelte does the work before the browser ever sees the file. The browser receives output, not instructions.

A component in Svelte looks like this:

```svelte
<script>
  let score = 0;
</script>

<p>Your score: {score}</p>

<button on:click={() => score++}>
  Add point
</button>

<style>
  p { font-weight: bold; }
</style>
```

Script. Markup. Style. One file. Nothing imported to make it run.

That's Svelte. It holds one thing and holds it well.

---

**Then what is SvelteKit?**

SvelteKit is what you reach for when one component isn't enough — when you have pages, and the pages need data, and the data needs to come from somewhere, and the somewhere needs to know which page is asking.

SvelteKit is the house. Svelte is the room.

It handles routing — which URL maps to which page — without a single line of JavaScript written by you for that purpose. The folder is the route. The file is the page. The convention does the work.

It handles data loading, server logic, static export, and the relationship between what the server knows and what the browser shows. It does this through a small number of files with agreed names: `+page.svelte`, `+layout.svelte`, `+page.js`. You learn the names once. They hold for the whole project.

---

**And vanilla — the stack I started with?**

Plain HTML. CSS in a shared stylesheet. JavaScript in a file I kept extending because there was nowhere else logical to put it.

There is nothing wrong with this stack. It is honest. It is direct. The browser understands it natively — no compilation step, no build process, no config file telling other config files what to think.

What it asks of you, in return, is that you manage everything yourself. Every page is a new HTML file. Every shared behaviour is a script you include and hope stays in sync. Every route is a link you typed manually and a file you created to match it.

This is fine for a small thing. UTMEDaily was not going to stay small.

---

### The matchup, plainly

| What you're asking | Vanilla | Svelte | SvelteKit |
|---|---|---|---|
| Where does my UI live? | Scattered across HTML files | One `.svelte` component file | `src/lib/` components, called by pages |
| How do pages connect? | `<a href>` to hand-written files | N/A — Svelte has no routing | Folders in `src/routes/` |
| Where does data come from? | Inline, or a JS fetch you write | Props passed in | `+page.js` load functions |
| What does the build produce? | What you wrote | Compiled JS | Static files or server output |
| What do you manage yourself? | Everything | Component scope | Almost nothing structural |

---

### What the boilerplate is confessing

Every framework has a boilerplate — the files that exist before you write a word of your own. Most developers run the setup command and delete the examples without reading them. I think this is a mistake.

The boilerplate is the framework's doctrine, written in file structure.

SvelteKit's opening files say: *routes are folders, pages are files, layout is shared, data is loaded before render.* If you read that and it matches how you already think about building — you're home. If it doesn't, the friction will never fully leave.

Vanilla's opening files say: *nothing. You decide. All of it.*

Svelte's opening files say: *here is one component. Go.*

I needed SvelteKit's answer. Not because I couldn't manage the vanilla decision-making — I had been — but because I had ten thousand students and one developer, and I needed the framework to hold opinions so I didn't have to hold all of them alone.

---

### The files SvelteKit gives you, and what they mean

```
my-project/
├── src/
│   ├── routes/
│   │   └── +page.svelte     ← your home page
│   └── app.html             ← the one HTML shell
├── static/                  ← files served as-is
├── svelte.config.js         ← project configuration
└── package.json             ← dependencies and scripts
```

`app.html` is the only HTML file you will write. One. The rest is Svelte.

`svelte.config.js` is where you tell SvelteKit how to behave — including the fact that you want static output, deployable to GitHub Pages without a server. One line does this: `adapter-static`. We will return to this.

`src/routes/` is the entire navigation of your application. Every folder is a URL segment. Every `+page.svelte` is a page. If you want `/quiz/mathematics`, you create `src/routes/quiz/mathematics/+page.svelte`. The URL and the file are the same sentence.

---

### What vanilla asked me to do instead

In the UTMEDaily project before this, the equivalent structure was:

```
project/
├── index.html
├── quiz-mathematics.html
├── quiz-chemistry.html
├── science_clusters.html
├── quiz-app.js
└── quiz-styles.css
```

Each HTML file was its own world. `quiz-app.js` was loaded into each one and had to behave differently depending on which page was asking. The shared CSS held everything together visually. The shared JS held everything together functionally — until it needed to know too many things, and then it just grew.

There is a word for that growth. Not bad code. Not laziness. Just: the natural consequence of a structure that was never designed to hold more than it started with.

---

### The question underneath the chapter

The question I was really asking, before I knew how to ask it, was this:

*How much of my thinking do I want the tool to preserve, and how much do I want to do once and never again?*

Vanilla preserves nothing. Every project starts from scratch.
Svelte preserves component structure.
SvelteKit preserves the whole architecture — routing, data, layout, output.

I wanted the architecture preserved. That is the decision this chapter is the foundation of.

Everything that follows is built on it.

---

*Next: Chapter 2 — Symbols and Notation. The characters, the keywords, the grammar. What exists in SvelteKit that does not exist in vanilla, and why each one earns its place.*

