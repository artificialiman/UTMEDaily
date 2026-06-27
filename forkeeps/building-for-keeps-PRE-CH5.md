# BUILDING FOR KEEPS
## Pre-Chapter 5: The Legal Analogy in Full

*Codification. Solicitation. Lobbying. Forensics. Verdict. Litigation.*
*The architecture as a legal system — and the developer who learned it from the outside in.*

---

I want to tell you something about the kind of lawyer I am, before I tell you anything about the law.

I did not learn this profession in a courtroom. I learned it in the hours before the courtroom — in the dossiers, the contracts, the forensic reconstructions of what actually happened so that a jury of reasonable people could understand it without becoming lawyers themselves. I spent my time in lobbying rooms, where the outcome is shaped before the vote. In evidence files, where the case is built before the trial. On jury teams, where the question is not *who is right* but *what does the evidence, taken together, actually say.*

The developer who questions deeper than they code learned the same way. They do not arrive at a problem and start typing. They arrive at a problem and reconstruct how it came to exist — upstream, before the symptom, at the decision that made the symptom inevitable. They write the contract before the code, because a contract written after the fact is just a description of what happened, and a description is not a guarantee.

This is the role. Not the advocate performing certainty for an audience. The architect of certainty, working alone, long before the audience arrives.

---

### What computation is for

Before the analogy can hold, the foundation must be stated.

Computation exists for one reason at every level of abstraction: **closure.**

Not closure in the JavaScript sense — though we will get there. Closure in the oldest sense: the resolution of an open question. A computation begins with something unknown — a value to be calculated, a condition to be evaluated, a page to be rendered — and it ends with something known. The loop closes. The promise resolves. The answer is either correct or incorrect. The state that was pending becomes the state that is settled.

Every abstraction in software — every function, every component, every interface, every framework — exists to make closure more reliable, more locatable, more transferable from one context to another. A function closes over a computation and names it. A component closes over a piece of UI and makes it reusable. A type closes over a shape and makes it verifiable. A route closes over a URL and makes it navigable.

When software breaks — really breaks, not just throws an error but fails to be what it promised to be — it is always because closure was not achieved somewhere in the chain. Something that should have been settled was left open. A value that should have been typed was left loose. A route that should have resolved returned nothing. A component that should have rendered the right thing rendered its last known state, which was no longer the right state, because the update that should have closed the loop was never called.

Closure is not a feature. It is the purpose. Everything in this book is in service of closure — the reliable, locatable, transferable resolution of every open question your application will ever face.

And anything that breaks closure — anything that introduces ambiguity where there should be certainty, optionality where there should be contract, noise where there should be signal — is not a complexity to be managed. It is a saboteur to be refused.

You do not negotiate with saboteurs.

*The first verdict: complexity that resists closure is not a tradeoff. It is a threat to the thing computation exists to do. Refuse it at the gate.*

---

### Codification — the act of writing the law

In law, codification is the process by which practice becomes doctrine. Rules that existed as custom, as precedent, as the accumulated decisions of specific cases, are gathered, examined, reconciled, and written into a single authoritative text. The code of law. The thing you cite when someone challenges you.

In a SvelteKit project, codification is `types.ts`.

It is the file where every shape in the application is named and defined before it is used. Every interface. Every type alias. Every enum. The things that will be passed between components, loaded from databases, rendered to screens — named here, once, in the definitions section of the project's constitution.

```typescript
// types.ts — the codification layer

interface Question {
  id: number;
  text: string;
  options: string[];
  correctIndex: number;
  subject: string;
}

interface QuizSession {
  questions: Question[];
  answers: number[];
  startedAt: number;
  isComplete: boolean;
}
```

These are not merely TypeScript. They are the project's code of law. When a component receives a `Question`, it is not receiving *an object that probably has some text and some options* — it is receiving a defined term, with a known shape, verified by the compiler before the program runs.

The forensic value here is profound. When something breaks — and something always breaks — the first question is: *did the data conform to its type?* If `types.ts` is honest and complete, this question has a verifiable answer. The evidence is there. The reconstruction is possible.

In a vanilla project without this layer, the forensic question becomes: *what shape was I expecting this object to be, and what shape was it actually?* These questions are answered by reading every file that touches the data and trying to infer the intended shape from the way it was used. This is archaeology. It is slow, it is error-prone, and it is entirely avoidable.

Codification is the choice to write the law before you need to cite it.

*The verdict: a codebase without a codification layer is a legal system without a code. Disputes will be resolved by whoever speaks loudest in the moment. Write types.ts before you write anything else.*

---

### Solicitation — the engagement of specialists

In law, solicitation is not a dirty word. It is the act of formally engaging someone with specific expertise for a specific purpose — a solicitor who handles the transaction you lack the standing or knowledge to handle alone. You bring in the specialist. You define the scope. You let them work within it.

In a SvelteKit project, solicitation is the ecosystem — the deliberate, scoped engagement of external tools for specific purposes they are built for.

Supabase is solicited for data persistence. It has standing in that jurisdiction. I do not write a database from scratch because I am not a database engineer and the problem has already been solved by people who are.

`adapter-static` is solicited for deployment to GitHub Pages. It has standing in that jurisdiction. I do not write a build pipeline from scratch.

Vite is solicited for bundling. TypeScript is solicited for type safety. These are specialists, engaged formally, for defined scopes.

```javascript
// svelte.config.js — the solicitation layer
import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: null
    })
  }
};
```

The config file is the retainer agreement. It defines what the specialist is engaged to do and under what conditions. A well-written config is a well-scoped engagement — the specialist does exactly what was asked and nothing more.

The failure mode of solicitation is scope creep. A tool engaged for one purpose that gradually assumes responsibilities it was never designed for. A CSS-in-JS library that started as a styling tool and became a state management system. A component library that started as a UI toolkit and became the application's routing layer. These are solicitors who have wandered outside their brief.

The specialist who wanders outside their brief is not a collaborator. They are a liability. The contracts that break most catastrophically are the ones where the scope was never clearly defined — where a dependency was invited in for one thing and stayed for everything, and became impossible to remove without rebuilding the rooms it had quietly colonised.

This is deliberate sabotage of closure, even when unintentional. The tool that knows too much closes nothing cleanly. It holds everything open, because its tentacles reach into too many jurisdictions to retract without consequence.

*The verdict: every dependency is a solicitation. Define the scope before you install the package. A tool that cannot be removed without rebuilding the application has exceeded its brief. That is not a dependency. That is a hostage situation.*

---

### Lobbying — the shaping of decisions before they are made

In law and governance, lobbying is the work that happens before the vote — the careful, persistent effort to shape the conditions under which decisions are made, so that the right decision becomes the natural decision, the easy decision, the one that requires no argument at the moment it is needed.

Good lobbying is invisible. By the time the vote happens, the outcome was already determined — not by force, but by the patient construction of a frame within which only one answer made sense.

In software, lobbying is architecture.

The file structure I choose lobbies for certain development decisions. When `src/routes/` mirrors the URL structure of the application, I am lobbying for the developer to think in routes — to make every new page a new folder rather than a new JavaScript condition in a routing table. The structure of the project is a persistent argument, made in silence, about how the project should be extended.

The naming conventions I choose lobby for consistency. When every data-loading file is `+page.js` and every page component is `+page.svelte`, I am lobbying for the next developer — or future me — to never have to wonder where the data for a page is loaded. The convention made the question unanswerable, and therefore never worth asking.

```
src/routes/
├── +layout.svelte          ← lobbying for shared structure
├── +page.svelte            ← lobbying for a home page
└── quiz/
    ├── +layout.svelte      ← lobbying for quiz-specific shell
    ├── mathematics/
    │   ├── +page.svelte    ← lobbying for one folder per subject
    │   └── +page.js        ← lobbying for data at the route level
    └── chemistry/
        ├── +page.svelte
        └── +page.js
```

This structure is not the only possible structure. It is a structure that lobbies for a specific set of decisions: subjects are routes, data is loaded at the route level, quiz layout is inherited rather than repeated. Every new subject added to this project arrives already knowing where to go. The architecture made the right decision the obvious decision.

The developer I am — more hours in lobbying rooms than in courtrooms — understood early that the most powerful interventions happen before the disagreement. A well-structured project does not produce fewer debates because the developers are in agreement. It produces fewer debates because the structure already answered the questions before they arose.

This is closure at the architectural level. The project lobbied itself into coherence before anyone had to argue for it.

*The verdict: architecture is lobbying. If you have to explain your structure to every new contributor, the structure has not yet done its work. Lobby the project into the decisions you want, then let the structure make those decisions for everyone who comes after.*

---

### Forensics — the reconstruction of what actually happened

I spent more time in forensics than anywhere else. Not the television kind — the disciplined kind. The reconstruction of a sequence of events from available evidence, for the purpose of establishing what actually happened as opposed to what anyone claimed happened, felt, or remembered.

In law, forensic work precedes the verdict. In software, it precedes the fix.

Debugging is forensics. You arrive after the fact, at a system in a broken state, and you reconstruct the sequence of events that produced that state. The logs are your evidence. The types are your witness statements — when they are honest, they tell you what was expected; the runtime error tells you what arrived instead. The gap between them is the crime scene.

This is why I said earlier that `types.ts` has profound forensic value. A codebase with complete, honest types is a codebase that leaves evidence. Every type mismatch is a documented discrepancy. Every interface violation is a signed statement that something didn't conform to its contract. The forensic investigator — the debugging developer — can work backwards from the discrepancy to the cause with the confidence of someone who knows the evidence was not tampered with.

A codebase without types is a codebase that destroys evidence as it runs. The values pass between functions as shapeless objects, accumulating assumptions that were never written down, failing at the point of rendering rather than at the point of origin, leaving the developer to reconstruct intent from behaviour rather than from contract.

```typescript
// Without forensics — evidence destroyed
function renderQuestion(q) {
  return q.text; // What if q is undefined? 
                 // What if text is options?
                 // The error is wherever, for whatever reason.
}

// With forensics — evidence preserved
function renderQuestion(q: Question): string {
  return q.text; // If this breaks, the compiler already
                 // told you before it ran. Upstream.
                 // Before the student ever saw it.
}
```

The forensic developer reads the second function and knows: if something is wrong with `q`, the compiler found it before the user did. The case was closed upstream. That is the entire value of types stated in a single example.

The questions I ask before writing a line of code — the twelve questions that a beginner hasn't yet thought to ask — are forensic questions. What state can this component be in? What happens when the data doesn't arrive? What happens when the user submits twice? What happens when the network fails between the question load and the answer submit? These are not pessimism. They are the disciplined anticipation of a forensic mind that has seen what happens when the questions go unasked.

*The verdict: a codebase that cannot be reconstructed is a codebase that cannot be trusted. Write types. Write comments that explain intent, not mechanics. Leave evidence. The next person in the room — including you, six months from now — is a forensic investigator. Give them something to work with.*

---

### Verdict — the point at which the open question closes

A verdict is not an opinion. It is the formal resolution of an open question, by a designated authority, in a prescribed form, with documented reasoning. It closes the case. It does not merely suggest that the case might be considered closed.

In software, a verdict is a merge. A deployment. A release. The moment at which the code that was being considered becomes the code that is running — the code that students depend on, the code that must work.

The gap between *probably works* and *will work* is the gap between a legal argument and a verdict. An argument can be compelling and still fail. A verdict is final — until it is appealed, which is what we call a bug report.

The architecture that makes verdicts reliable is the architecture that made its open questions legible before closing them. Every type was resolved before the merge. Every component received only what its interface promised. Every route loaded its data before its page rendered. Every edge case — the unanswered question, the empty state, the network failure — was handled in its proper place, not deferred to the runtime and the user's patience.

```svelte
<!-- The open question: what if data doesn't load? -->
<!-- Closed before the verdict: -->

{#if data.questions.length === 0}
  <p>No questions available for this subject.</p>
{:else}
  <Quiz questions={data.questions} />
{/if}
```

This is a small verdict. The question — *what does the page show when there are no questions?* — was open. The developer closed it. Explicitly. In the markup. Before the page was deployed. The student will never see an empty white screen and wonder if the application broke, because the verdict was rendered before she arrived.

Every `{:else}` is a verdict.
Every `try/catch` is a verdict.
Every TypeScript error resolved before commit is a verdict.
Every edge case handled in the load function rather than deferred to the component is a verdict.

The developer who renders verdicts continuously — who does not let open questions accumulate into a backlog of silent assumptions — is the developer whose codebase is trusted. Not because nothing ever breaks. Because when something breaks, the break is in a known place, for a known reason, and the path to a new verdict is clear.

*The verdict: close your questions before you ship. An open question in production is not a question anymore. It is a condition waiting to be triggered by the one user who arrives at exactly the wrong moment with exactly the wrong input.*

---

### Litigation — the case that had to be made in public

Litigation is what happens when private resolution failed.

In law, the courtroom is not the preferred venue. It is the venue of last resort — the place you end up when the contract was ambiguous, when the solicitor exceeded their scope, when the lobbying failed and the wrong decision was made, when the forensic evidence was insufficient to establish what happened without a trial. Litigation is expensive, slow, and public. The costs land on everyone.

In software, litigation is the production incident.

The all-hands call at two in the morning. The hotfix deployed without tests. The rollback that breaks three other things. The database query that was always inefficient but only becomes catastrophic at scale — at ten thousand concurrent users, at the exact moment a student population decides to practice simultaneously the night before the exam. The courtroom fills. The evidence is rushed. The verdict is pressured.

Every production incident is a failure of pre-litigation resolution. The type was not written. The edge case was not handled. The dependency was not scoped. The architecture did not lobby for the right decision. The open question was deferred until the worst possible moment to answer it — live, under load, in public.

I have been in those rooms. The forensic reconstruction that follows a production incident is always, without exception, traceable to an upstream decision that seemed manageable at the time. A loose type. An unhandled empty state. A dependency that knew too much and failed when one of the many things it knew changed without notice.

The students in Nigeria sitting JAMB practice tests do not know any of this. They do not know what a type is or what a route does or what a load function returns. They know whether the quiz worked. They know whether the answer registered. They know whether the score was right. And on the night before the most important exam of their young lives, they know — in the way you know things that have nothing to do with knowledge — whether the software was built by someone who was thinking about them, or by someone who was thinking about something else.

The litigation-free codebase is not built by people who never make mistakes. It is built by people who close their questions early, scope their dependencies tightly, lobby their architecture into coherence, leave forensic evidence in every type and comment, and render verdicts continuously — so that when the ten thousandth student clicks Submit at eleven o'clock at night, the system is not surprised.

It expected her. It was built for her. It closes.

*The final verdict: you do not negotiate with complexity that should have been refused at the gate. Not with the dependency that exceeds its scope. Not with the untyped value that might be anything. Not with the architecture that works until it doesn't. These are not tradeoffs to be managed. They are threats to closure — the only thing computation exists to achieve. Refuse them early, quietly, before they reach the courtroom. That is the work. That is the whole of it.*

---

*Next: Chapter 5 — The Living Files. The order in which files are created, and the intent each one carries. Every file is a constitutional clause. Some are foundational. Some are operational. None are neutral.*

