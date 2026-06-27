# BUILDING FOR KEEPS
## Chapter 2: Symbols and Notation — The Characters, the Keywords, the Grammar

---

A new language announces itself in punctuation before it announces itself in words.

Before you understand what `$state` does, you see the `$` and you feel it. Before you understand what `+page.svelte` means, you see the `+` and you know it isn't decorative. The symbols are the framework's first sentences — and like all first sentences, they tell you more about the speaker than any explanation that follows.

This chapter is about learning to read before you learn to write.

---

### First: the reading environment

You cannot learn symbols in an environment that makes them all look the same.

This is where Monokai comes in — and I want to say something about it that most people skip past. Monokai is not a colour preference. It is a classification system. The colours are a legend, and the legend teaches you to read the map.

In Monokai:

| Colour | What it marks |
|---|---|
| **Yellow** | Functions, methods — things that *do* |
| **Green** | Strings — things that *say* |
| **Purple/pink** | Keywords — things that *govern* |
| **Orange** | Numbers, constants — things that *are fixed* |
| **Blue/cyan** | Types, classes — things that *describe* |
| **White/light** | Variables — things that *hold* |
| **Grey** | Comments — things that *explain* |

Read that table once. Now look at any SvelteKit file in a Monokai-themed editor, and you will see not code — you will see *roles*. You will see what governs, what does, what holds, what says. The syntax becomes a cast list.

For a beginner, this is not cosmetic. It is the difference between reading a sentence and reading a blur. When you are learning what `$derived` means, you should not also be working out whether it is a keyword or a variable. Monokai answers that before you ask.

For an experienced developer, it is the same gift at higher speed — a scan becomes a read, a read becomes a decision.

Install it early. Keep it. Let the colours do their quiet work while you do yours.

---

### The symbols that do not exist in vanilla

Vanilla has no special syntax. It is HTML, which has tags. It is CSS, which has selectors and properties. It is JavaScript, which has functions and variables and a few dozen reserved words. Nothing in that stack requires you to learn a new symbol.

SvelteKit introduces several. Each one earns its place.

---

**The `+` prefix — the file that belongs to the route**

In `src/routes/`, not every file is a page. SvelteKit uses `+` to mark the files that have meaning to the framework itself.

```
src/routes/
├── +page.svelte       ← this is a page
├── +layout.svelte     ← this wraps all pages below it
├── +page.js           ← this loads data for the page
└── +error.svelte      ← this handles failures
```

The `+` says: *I am not a component you import. I am a file the router reads.*

Everything without a `+` is yours — a component, a utility, a stylesheet. The `+` is the framework's handwriting in your folder.

In Monokai, these filenames in your sidebar carry no special colour — they live in the file tree, not the editor. But once you are inside a `+page.svelte`, the `+` convention has already told you what role this file plays. You arrive knowing.

---

**The `$` prefix — the rune**

This is SvelteKit's most striking symbol, and the one most worth slowing down for.

In Svelte 5, reactive state is declared with runes — compiler instructions that begin with `$`. There are three you will use constantly:

```svelte
<script>
  let score = $state(0);
  let doubled = $derived(score * 2);
  $effect(() => {
    console.log('score changed:', score);
  });
</script>
```

In Monokai, `$state`, `$derived`, and `$effect` will appear in **yellow** — they are functions. The values they hold or return will appear in **white**. The relationship between those two colours, on one line, tells the whole story: *a function wraps a value and gives it special behaviour.*

The mental model underneath the colours:

| Rune | What it is | What it does |
|---|---|---|
| `$state` | Source | Holds a value that can change |
| `$derived` | Calculated | Recomputes when its source changes |
| `$effect` | Consequence | Runs when something it watches changes |

State is the cause. Derived is the calculation. Effect is the consequence.

In vanilla, you would write event listeners, update functions, and manual DOM queries to produce this chain. The chain exists in both places — Svelte simply names its links.

---

**The `{}` — the expression in markup**

In HTML, curly braces mean nothing. In Svelte markup, they mean: *evaluate this*.

```svelte
<p>Question {currentIndex + 1} of {total}</p>
```

No template engine import. No special syntax beyond the brace. Whatever is valid JavaScript fits inside. In Monokai, the contents of `{}` in markup shift colour — the string around them is **green**, the expression inside is **white** or **yellow** depending on what it contains. The boundary is visible without you looking for it.

---

**The `:` and `|` — directives and transitions**

Svelte extends HTML attributes with directives. They use a colon to mark themselves as more than plain attributes:

```svelte
<button on:click={handleAnswer}>
  Submit
</button>

<input bind:value={answer} />
```

`on:click` is not an HTML attribute. `bind:value` is not either. The `:` separates the directive type from its target. In Monokai, directive names take on the **purple/pink** of keywords — they govern behaviour, and the colour says so.

The `|` appears in transitions:

```svelte
<div transition:fade|local>
  {question}
</div>
```

The `|` is a modifier — it qualifies the transition. You will not use it every day, but when you see it, you will not confuse it for anything else. It is too specific to be accidental.

---

**The `#`, `/`, and `:` of logic blocks**

Svelte puts logic in the markup, not beside it. The syntax uses a small family of symbols:

```svelte
{#if answers.length > 0}
  <ul>
    {#each answers as answer}
      <li>{answer}</li>
    {/each}
  </ul>
{:else}
  <p>No answers yet.</p>
{/if}
```

`#` opens a block. `/` closes it. `:` continues it.

This mirrors HTML's own open/close convention — `<div>` and `</div>` — which is not accidental. Svelte's markup logic was designed to feel like HTML extended, not JavaScript inserted. In Monokai, `{#if}`, `{#each}`, `{/if}` appear in **purple** — they govern. The content between them returns to normal colours. The eye knows where the logic is and where the content is.

---

### What does not exist in SvelteKit that vanilla relied on

This is worth naming plainly, because the absence is as instructive as the presence.

| Vanilla pattern | SvelteKit equivalent | What disappeared |
|---|---|---|
| `document.getElementById()` | `bind:` directive | Manual DOM selection |
| `element.addEventListener()` | `on:` directive | Manual event wiring |
| `element.innerHTML = ...` | `{expression}` in markup | Manual DOM mutation |
| `window.location.href` | SvelteKit `goto()` or `<a href>` | Manual navigation |
| Multiple HTML files | `src/routes/` folders | Manual page management |

Everything in the left column still works in a browser. SvelteKit does not forbid it. It simply makes it unnecessary — and unnecessary things, when left in code, become questions that future-you has to answer.

---

### Reading code before writing it

The habit that symbols make possible — and that Monokai reinforces — is reading.

Before I write a new component, I read the ones nearby. Not for what to copy, but for what role each colour is playing. Yellow is working. Purple is governing. Green is speaking. White is holding.

A file where everything is one colour is a file where something has gone wrong — not in the code, necessarily, but in the thinking. When a variable is doing a function's job, or a string is doing a variable's job, the colours will tell you before the bug does.

This is the gift Monokai gives that no tutorial mentions: it makes architectural problems visible before they become runtime problems. The junior developer learns the symbols. The senior developer trusts the colours. The gap between them closes faster than either expects.

---

### The symbol table, complete

| Symbol | Location | Monokai colour | Means |
|---|---|---|---|
| `+` | Filename prefix | — (file tree) | Route-owned file |
| `$state` | Script | Yellow (function) | Reactive source value |
| `$derived` | Script | Yellow (function) | Calculated from state |
| `$effect` | Script | Yellow (function) | Side effect of state |
| `{}` | Markup | Shifts by content | Evaluate this expression |
| `on:` | Attribute | Purple (keyword) | Event directive |
| `bind:` | Attribute | Purple (keyword) | Two-way binding |
| `#` | Logic block open | Purple (keyword) | Begin block |
| `/` | Logic block close | Purple (keyword) | End block |
| `:` | Logic block continue | Purple (keyword) | Else / else-if |
| `\|` | Transition modifier | Purple (keyword) | Qualify a transition |

---

You do not need to memorise this table. You need to see it once, and then let the colours remember it for you.

The symbols are a grammar. Monokai is the reading glasses. Together they let you see a file for what it *is* — which is always the first step before you can change what it does.

---

*Next: Chapter 3 — UI/UX, DX/DI. Who does the work so others don't have to. The five levels of abstraction, and why the level you build at determines the experience of every level below.*

