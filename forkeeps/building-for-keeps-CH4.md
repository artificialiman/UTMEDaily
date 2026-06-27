# BUILDING FOR KEEPS
## Chapter 4: Mathematics, Grammar, Law — The Three Disciplines of Programming

---

Programming is not one discipline wearing a lab coat.

It is three disciplines in a room together, each one occasionally irritated by the other two, each one occasionally saving the other two from themselves. The mathematician in the room wants everything provable. The grammarian wants everything legible. The lawyer wants everything to hold up under the worst possible conditions — edge cases, bad actors, the user who clicks Submit four times in a row because the first three times nothing happened.

All three are right. All three are necessary. The art is in knowing which one is speaking at any given moment — and in writing code that lets each of them do their work without the others getting in the way.

---

### Mathematics — the discipline of proof

Mathematics does not argue. It proves.

A mathematical statement is not an opinion about what should happen. It is a demonstration that something cannot be otherwise, given what was established before it. If A is true and B follows from A, then B is true — not probably, not usually, not under normal conditions. Unconditionally, completely, without exception.

This is what TypeScript is reaching for when it asks you to declare types. Not because the types make the program run — JavaScript runs perfectly well without them, and the browser does not care what shape you said your data would be. TypeScript asks for types because a type is a proof: a statement that this variable will hold a number, and that this function will receive a string and return a boolean, and that these facts are verified before the program ever runs.

```typescript
function scoreQuestion(
  selected: number,
  correct: number
): boolean {
  return selected === correct;
}
```

The types here are not decorative. They are a proof obligation. The compiler checks them the way a mathematician checks steps in a derivation — and if the proof fails, you hear about it before anyone else does. Before the student. Before the exam. Before the quiet disaster of a wrong answer marked correct.

The law weighs in here immediately: *a contract is only as strong as its terms.* In legal drafting, vague language is dangerous — not because it is unclear to the writer, but because it is ambiguous to the system that interprets it. A court that must guess at intent will guess wrong with predictable frequency. TypeScript is the discipline of removing guesswork from the interpretation of your code. `number` is not a guess. `string` is not an approximation. They are terms, and they hold.

The grammarian adds: *precision is not the same as legibility.* A type can be technically correct and still unreadable. `Record<string, Array<Partial<Question>>>` is precise the way a legal clause with seventeen subclauses is precise — nothing is ambiguous, and nothing is approachable. The mathematician and the grammarian must negotiate the type, together, until it is both provable and readable.

---

### Grammar — the discipline of structure

Grammar does not prove. It organises.

A grammatical sentence is not one that is true — it is one that can be understood. The subject performs the action on the object. The verb agrees with its subject in number. The clause that qualifies the noun lives close to the noun it qualifies, so the reader does not have to carry it across a long sentence in working memory and then resolve it at the end, exhausted.

In programming, grammar is the structure of your interfaces — the way you arrange what a component receives, what a function expects, what a module exports. Not whether these things are correct, but whether they communicate.

```typescript
interface QuizState {
  currentIndex: number;
  answers: number[];
  isComplete: boolean;
}
```

This interface is grammar. It says: *a quiz state is a thing that has a current position, a record of answers, and a completion status.* The sentence is complete. The subject is `QuizState`. The predicates are its properties. A developer reading this knows, before opening a single component, what a quiz carries at any point in its life.

The law speaks again: *definitions precede application.* Every legal document begins with a definitions section — not because the drafter assumes you are ignorant, but because language used without definition is language used without agreement. When the contract later says *the Student*, it means the thing defined on page one. There is no ambiguity, because the definition closed it. In TypeScript, the interface is the definitions section. When a component later receives a `QuizState`, it means the thing defined in `types.ts`. The interface closed the ambiguity before it could open.

The mathematician leans in: *an interface is a specification, not an implementation.* It describes what must be true without dictating how. The component that receives a `QuizState` does not care how the state was assembled — only that it conforms to the shape. This separation between specification and implementation is one of the oldest ideas in mathematics, and it is the same idea that makes interfaces more durable than concrete implementations. Change the implementation as much as you like. The interface holds. The contract holds. The student does not notice.

---

### Law — the discipline of consequence

Law does not prove and does not merely organise. Law governs.

A law is a rule with teeth — a statement that says not only what should happen but what happens when it doesn't. It anticipates failure. It names the failure. It specifies the response to the failure. A legal system without consequences is a style guide. A legal system with consequences is an architecture.

Programming is law in this sense more than in any other. The code does not ask. It does not suggest. It executes, and the execution has consequences — for the user who receives output, for the system that stores data, for the student whose score is recorded and remembered and reported. Every function is a small piece of legislation. Every component is a small jurisdiction.

And this is where the observation I keep returning to finds its fullest expression: *law is essentially programming where the engineers have to walk around and talk aloud about their process a lot more.*

Think about what a lawyer actually does. They read the existing code — the statutes, the precedents, the contracts already in force. They identify the relevant rules. They construct an argument from those rules toward a conclusion. They present that argument, out loud, to other people who are also thinking about the same rules, and they defend it against challenge. Then someone decides whether the argument holds.

A programmer does the same thing. Reads the existing codebase. Identifies the relevant functions, interfaces, component contracts. Constructs a solution from those materials toward a desired output. The difference — the only difference — is that the programmer does most of this silently, in a chair, with the argument written in a file rather than spoken in a room.

The comments in your code are your oral argument. The commit message is your brief. The pull request description is your submission to the court. The code review is the trial. The merge is the verdict.

In law, this externalisation of reasoning is not optional — it is the discipline itself. A lawyer who cannot articulate their reasoning has no standing. Their argument may be correct in their head. It holds no weight until it is speakable, hearable, challengeable. This is why legal documents are long. Not because the law is inefficient — because every word that could be ambiguous must be made unambiguous, and every condition that could be disputed must be anticipated and addressed before the dispute arrives.

Good code aspires to this. The best code I have read reads like a document written by someone who expected to be challenged — someone who anticipated the next developer's questions and answered them in the naming of functions, the structure of modules, the discipline of types.

```svelte
<!-- +page.svelte — Mathematics quiz page -->
<!-- Receives: questions loaded by +page.js -->
<!-- Renders: one question at a time, tracks answers -->
<!-- Navigates to: /results on completion -->

<script>
  let { data } = $props();
  let state = $state({
    currentIndex: 0,
    answers: [],
    isComplete: false
  });
</script>
```

The comments here are oral argument. The structure is legislation. The types are proof. All three disciplines, in four lines of script.

---

### The spectrum between proof and governance

There is a line — not a clean one, but a real one — that runs from `types.ts` to `app.css`.

At the `types.ts` end, everything is mathematics. Provable, verifiable, binary. Either the type is satisfied or the compiler refuses. There is no negotiation.

At the `app.css` end, everything is closer to common law — accumulated conventions, community agreements, inherited wisdom about what works. The browser does not refuse malformed CSS the way TypeScript refuses malformed types. It guesses. It falls back. It does its best with what you gave it. The discipline here is not enforced by a compiler. It is enforced by the developer who cares enough to write it well.

Between those two ends lives grammar — the interfaces, the component contracts, the function signatures that are technically optional in JavaScript and absolutely essential in any codebase that will outlive the mood in which it was written.

```
types.ts ←————————————————————————→ app.css
[mathematics]    [grammar]    [law]
[proof]       [structure]  [governance]
[compiler]      [interface]    [convention]
```

Where you are on this spectrum at any moment determines what kind of thinking you need. Are you writing a type? Think like a mathematician — be precise, be complete, be unambiguous. Are you designing an interface? Think like a grammarian — be clear, be consistent, let the structure carry meaning. Are you making an architectural decision — where does this file go, what does this module own, how does this route behave under failure? Think like a lawyer — anticipate the edge, name the consequence, write the constitution carefully.

---

### The economy of complexity, and why this matters

The three disciplines also explain something I mentioned in the preface — the manufactured complexity of the JavaScript ecosystem — in a way that I find clarifying rather than cynical.

A mathematical discipline is stable. Once a proof is established, it does not need to be re-established next year in a new syntax. A grammatical discipline is stable. Good structure does not become bad structure because a new framework arrived. A legal discipline is stable. Well-written contracts do not expire because the industry shifted.

What is unstable is the layer of tools that sits above these disciplines and claims to embody them. A new testing library does not change what it means to write a provable function. A new CSS-in-JS solution does not change what it means to write a coherent design system. A new state management pattern does not change what it means to govern application state clearly. But the churn of tools creates the impression that the disciplines themselves are moving — that you need to keep up, keep learning, keep certifying, keep migrating.

You do not. The disciplines are old. They predate computers. They will outlast every framework currently competing for your attention. If you understand what mathematics is asking of your types, you can learn any type system. If you understand what grammar is asking of your interfaces, you can design in any language. If you understand what law is asking of your architecture, you can govern any codebase.

The right tool for the job is the one that lets these three disciplines do their work clearly. SvelteKit, for this project, is that tool. Not because it is the best tool in an absolute sense — because it is the tool that makes mathematics visible in TypeScript, grammar legible in component contracts, and law navigable in a file structure that mirrors the application's own logic.

---

### Write the constitution carefully

There is a principle that emerges from the legal discipline that I want to name before this chapter closes, because it is the principle that governs everything that follows.

In constitutional law, the founding document does not specify every case. It cannot — the cases it will face have not yet happened. What it specifies is the framework within which cases will be decided: the rights that cannot be overridden, the processes that must be followed, the values that hold when everything else is in dispute.

A SvelteKit project has a constitution. It is not a single file — it is the combination of `types.ts`, `svelte.config.js`, the layout structure, the data loading patterns, and the naming conventions that govern how routes are named and how components are shared. These files are written once, early, with care — and everything else in the project inherits from them.

The constitution does not prevent all failures. It makes every failure locatable. When something breaks, the question is not *where do I even begin* — it is *which clause of the constitution was violated, and where*. The mathematics failed: a type was wrong. The grammar failed: a component received a shape it wasn't expecting. The law failed: a route assumed data that wasn't loaded.

Locatable failures are fixable failures. Unlocatable failures are the ones that eat weekends.

Write the constitution carefully. Everything else inherits from it.

---

*Next: Pre-Chapter 5 — The Legal Analogy in Full. Before we open a single file, we walk the whole architecture as a legislature. Codification, solicitation, lobbying, verdict, litigation. The analogy extended until it holds the whole project.*

