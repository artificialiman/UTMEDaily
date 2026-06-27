# BUILDING FOR KEEPS
## Chapter 8: Change, Errors, Failure

*Written as questions.*
*A reader who answers them owns the architecture.*
*A developer who cannot answer them knows where to look next.*

---

There are no explanations in this chapter.

Only questions. Some of them you will answer immediately — the architecture is clear, the file is known, the answer arrives before you finish reading the sentence. Some of them will make you pause. The pause is the information. It tells you exactly where to return in the preceding chapters, exactly which file to open, exactly which ownership decision was not yet fully understood.

A reader who can answer every question in this chapter owns this architecture.

Begin.

---

### On beginner mistakes

When you installed SvelteKit and ran the project for the first time, what was the first thing you changed?

Did you understand why it worked before you changed it?

When something broke after your first change, did you read the error or did you search the error?

What is the difference between those two responses — and what does each one cost over time?

---

You reached for a `<div>` when the element you needed had a name. What was the name?

You wrote `class="active"` in JavaScript when Svelte had a directive for it. What was the directive?

You wrote `document.getElementById` in a Svelte component. What should you have written instead, and what did writing it that way cost the component's lifecycle?

---

You wrote a component and it worked. Then you needed the same component in a different context and it didn't work because it assumed something about the page it was on. What did it assume? Where did that assumption live? How do you remove it?

---

You named a variable `data`. Then you named another one `data`. Then a third. When something broke, which `data` was it?

What is the name that describes what the thing *is* rather than what it *contains*?

---

You put the logic in the template. The `{#if}` condition was fifteen words long and called two functions. What should those fifteen words have been? Where should those two functions have gone?

---

You pushed to an array. The component did not update. How long did it take you to find out why? How long will it take you next time?

---

You skipped `types.ts` because the application was small. When did small become the wrong word for it? What was the first thing that broke because the shape of the data was assumed rather than declared?

---

You wrote the component before you wrote the type. You wrote the page before you wrote the load function. You wrote the load function before you handled the error case. At which of these three moments did the debt begin, and how was it eventually paid?

---

You saw a framework you had never used and you installed it. What problem did it solve? Was that problem real before you installed it, or did it arrive with the installation?

---

You read a tutorial. The tutorial showed the happy path. What happened when you left the happy path?

---

### On change

You need to add a new subject — Physics. Name every file you touch. Name every file you do not touch. Which list is longer?

---

The colour of a correct answer needs to change from green to teal. Name the file. Name the line. Name every component that updates without being touched.

---

A new property needs to be added to the `Question` interface — `difficulty: 'easy' | 'medium' | 'hard'`. Where does it go first? What does the compiler tell you after you add it? What does that message mean, and why is it useful rather than annoying?

---

The quiz needs to support a timer. Where does the timer state live? Which component owns it? What does the load function need to change, if anything? What does `types.ts` need to change?

---

The results page needs to show a breakdown by topic, not just a total score. What shape does the data need to be? Where is that shape declared? What changes in the load function? What changes in the component?

---

You need to rename a route. `/quiz/[subject]` becomes `/practice/[subject]`. Name every file that moves. Name every file that changes. Name every file that is unaffected.

---

A design decision made in Chapter 1 of the project's life is now wrong. It affects every page. Where is it written? How many files does changing it touch directly? How many does it touch through inheritance?

---

You need to add a loading state — a spinner that shows while questions are being fetched. Where does it go? What does SvelteKit provide that makes this easier than you expect?

---

The JAMB data format changed. The source files now use a different structure for options. Which file absorbs this change first? Which files never know it happened?

---

### On failure

The quiz page is blank. No error. No spinner. Just white. What is the first file you open?

---

The load function returned successfully. The component received the data. The page is still blank. What does this tell you about where the problem is not?

---

A student reports that her score was wrong. The component rendered correctly — you can see it in the screenshot she sent. Where is the calculation? What are the three things that could make it wrong?

---

The correct answer is being marked incorrect for one subject but not the others. The data is the same shape. The component is the same component. Where do you look?

---

`params.subject` is `undefined`. The URL is correct. What happened in the file system?

---

The build succeeds. The preview works. The deployed site does not. What is the first question you ask about the deployment configuration?

---

A type error appears in a file you did not change. What does this mean? Is it a problem with the file the error is in, or with the file you changed?

---

The error says `Cannot read properties of undefined`. The line it points to looks correct. What is the question you ask about the line *above* it?

---

A component works in isolation. It breaks when composed inside another component. What is the first assumption to test?

---

The application worked yesterday. It does not work today. You changed nothing. What changed?

---

You fixed the bug. Two days later it returned. What did the fix address — the symptom or the cause? How do you tell the difference?

---

### On ownership

Which file owns the score?

Which file owns the question text?

Which file owns the colour of an incorrect answer?

Which file owns the decision about which subject to load?

Which file owns the navigation between quiz and results?

Which file owns the shape of what the navigation carries?

---

A component is doing three things. What are the three components it should become?

---

Two components share logic. Where does the shared logic go? What is it called? How does each component receive it?

---

The layout knows something about the page inside it. Should it? What should the relationship between a layout and its pages be, stated in one sentence?

---

A utility function grew. It now handles data fetching, text transformation, and score calculation. It lives in `utils.ts`. What are the three files it should become, and what does each one own?

---

`+page.svelte` is two hundred lines long. The four questions — *what is this, what does this own, what does this show, what does this need* — are all answered in the same file. What does this tell you, and what do you do about it?

---

### On doctrine

Why does the file creation order matter?

Why does a type written before a component produce a different kind of code than a type written after one?

Why is `strict: true` in `tsconfig.json` a kindness rather than a constraint?

Why does the URL matter to a user who never looks at the address bar?

Why is an `{:else}` branch in a template a form of respect?

Why does a component that knows too little about the world trust the world more fully than one that knows too much?

Why is a shared stylesheet more honest than a component-level override?

Why does naming a file `quirks.ts` make the rest of the codebase more trustworthy?

Why does closure matter — not as a JavaScript concept, but as the purpose of computation itself?

Why is the architecture that makes every failure locatable more valuable than the architecture that prevents most failures?

Why does the right tool for the job require knowing the job before knowing the tools?

Why does sensibility outlast every badge?

---

### The final question

What would you change about this architecture?

---

Nothing.

It remains a right tool for the job situation. The job was a quiz platform for ten thousand students, built by one developer, deployed as a static site, maintained over time without archaeology. The architecture serves that job. If the job changes — if the platform grows to require a server, a database with real-time features, authenticated sessions, a teacher dashboard — the architecture will change with it, because the doctrine does not change. The doctrine says: understand the job, choose the tool that fits it, build it once and build it well, let the structure hold the decisions so the developer doesn't have to hold them alone.

The tool changes. The doctrine holds.

This is what it means to build for keeps. Not that the code never changes. That the thinking underneath it is durable enough to know when change is warranted, what to change, and what to leave exactly as it is.

---

*The architecture does not prevent all failures.*
*It makes every failure locatable.*

*Everything in this book is in service of that click.*

---

**END**

