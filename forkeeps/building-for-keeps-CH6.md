# BUILDING FOR KEEPS
## Chapter 6: The Routes

*The `<a href>` is thirty years of infrastructure.*
*The cost of replacing it never appears in the tutorial.*

---

Before there was a web, there were documents.

Before there were documents, there were addresses — the understanding that a thing located somewhere could be found by anyone who knew where to look. The URL is that understanding, formalised. It is not a technical detail. It is the web's most fundamental promise to its users: *this thing is here, at this address, and if you return to this address, this thing will be here again.*

The anchor tag — `<a href>` — is the mechanism by which one address points to another. It is the oldest navigational primitive on the web. It predates JavaScript. It predates CSS. It predates every framework that has ever claimed to improve upon it. When a user clicks an anchor, the browser takes over: it resolves the address, records the departure in the history stack, fetches the destination, and renders it. The back button works. The bookmark works. The shared link works. The search engine index works. All of this, from one tag, by doing nothing except letting the browser be the browser.

This is not a small thing to inherit. This is thirty years of infrastructure, battle-tested across every device, every connection, every accessibility tool ever built. And it is given to you for free, the moment you write `<a href>`.

The question this chapter asks is: what do you give up when you replace it?

---

### What JavaScript routing is

JavaScript routing is the practice of intercepting navigation — catching the moment a user would move to a new URL — and handling it in code rather than letting the browser handle it natively.

The reasons it exists are real. A single-page application that routes in JavaScript can transition between views without a full page reload. Transitions can be animated. State can persist across navigation. The experience, when it works, is fluid in a way that full-page navigation is not.

The costs are also real, and they accumulate in places the tutorial does not visit.

The browser's history stack must be managed manually — `pushState`, `replaceState`, `popstate` events, the careful maintenance of a parallel record of where the user has been. The back button, which the browser provides for free for anchor navigation, must be reconstructed for JavaScript navigation — and it must be reconstructed correctly, which means handling every edge case the browser already handled for three decades before your framework arrived.

Accessibility breaks at the seam. Screen readers announce page changes through native browser navigation. JavaScript routing that does not explicitly announce route changes — through ARIA live regions, through focus management, through the careful application of patterns the browser would have handled automatically — is JavaScript routing that has made the application invisible to users who depend on assistive technology. This is not a minor concern. This is a failure of the basic contract between software and the humans who use it.

Search engine indexing becomes conditional. A server-rendered or statically-generated page is indexable by default. A JavaScript-routed page that renders its content after the initial HTML loads is indexable only if the crawler waits for the JavaScript to execute — which some do, with varying degrees of fidelity, and some do not.

And none of this appears in the tutorial. The tutorial shows the transition animation and stops.

---

### What SvelteKit routing is

SvelteKit routing is file-system routing — the agreement that the structure of `src/routes/` is the structure of the application's URLs, and that the framework reads this structure rather than requiring you to declare it.

```
src/routes/
├── +page.svelte              →  /
├── +layout.svelte            →  wraps everything
├── quiz/
│   ├── +layout.svelte        →  wraps quiz pages
│   └── [subject]/
│       ├── +page.svelte      →  /quiz/mathematics
│       └── +page.js          →        /quiz/chemistry
│                                       /quiz/biology ...
└── results/
    └── +page.svelte          →  /results
```

The URL is the folder path, read directly. There is no routing table. There is no array of route objects to maintain. There is no registration step between creating a file and having a working route. The file exists. The route exists.

Navigation between these routes uses anchor tags. `<a href="/quiz/mathematics">`. The browser handles the rest. SvelteKit enhances anchor navigation with prefetching — on hover, the browser begins loading the destination before the click is complete, producing the feel of instant navigation — but the enhancement is additive. The anchor works without it. The enhancement makes it better. This is the correct relationship between a framework and a browser primitive.

---

### The `[subject]` — dynamic routing

The square brackets in `[subject]` are SvelteKit's notation for a dynamic segment — a part of the URL that is a variable rather than a fixed string.

`/quiz/mathematics` matches `[subject]` with `subject = "mathematics"`.
`/quiz/chemistry` matches `[subject]` with `subject = "chemistry"`.
`/quiz/biology` matches `[subject]` with `subject = "biology"`.

One folder. Infinite subjects. The parameter is available in the load function as `params.subject`, which is how the load function knows which question file to fetch.

```javascript
// src/routes/quiz/[subject]/+page.js
export async function load({ params }) {
  const res = await fetch(`/data/${params.subject}.json`);
  if (!res.ok) return { questions: [], error: true };
  return { questions: await res.json(), subject: params.subject };
}
```

In vanilla, the equivalent required either a separate HTML file per subject — with all the maintenance burden that entailed — or a single page that read the subject from a query parameter (`?subject=mathematics`) and adjusted its behaviour accordingly. The query parameter approach works, but it is a workaround: the URL `quiz.html?subject=mathematics` is less legible, less shareable, and less indexable than `/quiz/mathematics`. The clean URL communicates. The query parameter records.

*The route is a sentence. The query parameter is a footnote.*

---

### The layout within the route

SvelteKit allows layouts to be nested — a layout that applies to all quiz pages, sitting inside the global layout that applies to everything.

```svelte
<!-- src/routes/quiz/+layout.svelte -->
<script lang="ts">
  import { page } from '$app/stores';
</script>

<div class="quiz-shell">
  <p class="subject-label">
    {$page.params.subject}
  </p>
  <slot />
</div>
```

Every quiz page — Mathematics, Chemistry, Biology, English — inherits this shell automatically. The subject label renders from the URL parameter, which means it is always accurate. Not accurate because a developer remembered to pass it correctly. Accurate because the URL is the source of truth, and the layout reads from the URL.

This is the routing system as a data source, not just a navigation mechanism. The URL knows where you are. The layout can read it. The page doesn't have to pass it. The information flows from the address itself — which is, again, what URLs were always for.

---

### `<svelte:window>` and the events that belong to no component

There is a category of event that does not belong to any element — keyboard shortcuts, scroll position, window resize, the pressing of Escape to close a modal. In vanilla, these are handled by `window.addEventListener`, attached somewhere in the JavaScript file, hopefully removed somewhere else, occasionally left running after the page moves on because the cleanup was forgotten.

In Svelte, `<svelte:window>` handles these without touching the global object directly:

```svelte
<svelte:window
  on:keydown={handleKeydown}
  bind:scrollY={scrollPosition}
/>
```

The binding is scoped to the component. When the component unmounts, the event listener is removed. Not because the developer remembered to remove it — because the component lifecycle manages it automatically. The window event is treated like any other event: declared, scoped, cleaned up.

In Monokai, `<svelte:window>` appears in the distinctive pale orange of built-in elements — a visual signal that this is the framework speaking, not you. The colour marks the boundary between your code and the infrastructure. You notice it. You do not mistake it for a component you wrote.

---

### The cost that never appears in the tutorial

I want to return to this, because it is the chapter's argument and it deserves to be stated without softening.

Every tutorial that teaches JavaScript routing shows you the happy path. The transition works. The animation plays. The state persists. The developer smiles. The tutorial ends.

What the tutorial does not show:

The user who opens your application in a browser with JavaScript disabled — a corporate browser, a locked-down school network, a browser extension that blocks scripts — and sees a blank page where content should be, because the routing and the rendering both depend on JavaScript that never ran.

The screen reader user who navigates to a new route and hears nothing — no announcement, no focus movement, no indication that the page changed — because the JavaScript router moved the content without telling the accessibility tree.

The search engine crawler that indexes your application's shell and nothing inside it, because the content was rendered after the initial HTML by JavaScript that the crawler did not wait for.

The user on a slow connection who clicks a link and waits — not for the browser to load a page, which it is very good at — but for the JavaScript bundle to download, parse, execute, and then render the route, which adds latency at every step compared to a simple document load.

These are not hypothetical failures. They are the documented, consistent, well-understood costs of moving navigation responsibility from the browser to JavaScript. They are paid by users, not developers. They do not appear in benchmarks. They do not appear in conference talks. They appear in accessibility audits and support tickets and the quiet attrition of users who simply leave rather than report the friction.

SvelteKit does not eliminate JavaScript routing — it uses it, enhanced over anchor navigation, with server-side rendering and static generation ensuring that the content exists before JavaScript runs. The framework was designed by people who understood the costs and built the architecture to pay as few of them as possible.

But the principle behind the design is worth stating plainly, because it applies beyond any framework: *a browser primitive that already does the job well is not a problem waiting to be solved. It is infrastructure waiting to be used.*

Use the anchor. Add the enhancement. In that order. Always in that order.

---

### The route as a contract

Every route in a SvelteKit application is a contract with the user.

`/quiz/mathematics` promises: *if you arrive here, you will find a mathematics quiz.* The load function fulfils the promise by fetching the data. The page component fulfils the promise by rendering it. The layout fulfils the promise by providing the shell. The type definitions fulfil the promise by ensuring that what was loaded is what was expected.

A broken route is a broken promise. The user came to an address that the application advertised — through a link, through a bookmark, through a URL shared by a friend — and arrived to find something other than what was promised. An error. An empty page. A loading spinner that never resolves.

The architecture of this chapter is the architecture of promise-keeping. The file system is honest: the route exists only when the file exists. The load function is honest: it handles failure before the page renders. The types are honest: the data conforms to its contract before any component receives it. The anchor is honest: it goes where it says it goes, and the browser's history stack records the journey accurately.

Honesty in routing is not a virtue. It is the minimum viable trust between an application and a user who has nowhere else to be right now except here, trying to learn something, on a phone, at whatever hour the studying finally happens.

Keep the promise.

---

*Next: Chapter 7 — Every Single Line. From wireframe to keystroke. The four questions every line answers. What each build tool resents. Where the idiosyncratic things go.*

