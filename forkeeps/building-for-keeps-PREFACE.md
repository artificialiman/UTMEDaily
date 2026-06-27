# BUILDING FOR KEEPS
### Sensibility over badge-hunting. The right tool for the job. Code like Buffett invests.

---

## Preface

I did not set out to write a manual.

I set out to build a quiz platform for students sitting the JAMB exam in Nigeria — the test that decides whether a seventeen-year-old gets into university or tries again next year. Ten thousand students. Real stakes. One developer. Me.

At some point in the building, I noticed I was also writing down why. Not just *this is how you create a route*, but *this is why routes should be folders and not JavaScript*. Not just *here is the config*, but *here is what the config is confessing about the framework's assumptions*. The why kept accumulating. This book is what happened when I stopped ignoring it.

---

I know HTML well. I mean that seriously — not as a humble brag caveat before admitting I actually live in React. I mean HTML is where I think first. Structure before style, always. When I encounter a new problem, my instinct is to reach for the element that already describes the thing, before I reach for any script that could simulate it.

CSS is, to me, the most satisfying layer of the stack. I am aware this is not a popular opinion in rooms where people talk about *real engineering*. I hold it anyway. CSS gives you immediate feedback. The community of people who care about it is unusually sane. It bends without breaking. It has a kind of grammar that rewards attention — and punishes contempt, which is fair.

JavaScript I use past a certain number of lines with the same caution I use when entering a building where the foundation is probably fine. Probably. I don't use it in routing. I don't use it in state management if I can help it. I reach for something with more opinions in those places — HTML, or a framework with TypeScript at its centre — because I've seen what happens when JavaScript is asked to govern itself at scale. It tends to produce more JavaScript.

TypeScript I came to late, and I came to it the way you come to a good law: reluctantly, then gratefully. It imposes. That's the point.

---

I want to say something about frameworks, and I want to say it plainly.

There is an economy built around complexity. Not the complexity of hard problems — that complexity is honest and I respect it. I mean the complexity that is manufactured and maintained because a stable, learnable, durable platform is bad for conference talks, bad for bootcamp curricula, bad for the consultants who bill by the migration. A fast-moving ecosystem is very good for that business. I am not angry about this. I simply noticed it, and once you notice it, you cannot un-notice it.

I chose SvelteKit for this project not because it is fashionable. I chose it because it is sensible. Because Svelte is about components and SvelteKit is about routes and data — full stop, no footnotes. Because the boilerplate confesses its assumptions rather than hiding them. Because I could see the floor.

This is Buffett's method, applied to tools. Don't follow the market. Don't follow the conference. Follow doctrine: what is this tool's actual value? What is it genuinely good at? What does it cost when it fails? If you can answer those questions, you can choose. If you cannot, you will be choosing by social proof — and social proof in software engineering is a lagging indicator dressed as a consensus.

---

The student who clicks *Submit* on a JAMB practice question at eleven o'clock at night, on a slow connection, on a phone that cost three months of savings — that student is why every architectural decision in this book is the way it is.

Not because the decisions are heroic. Because they are durable.

*Once and for all* is not perfectionism. It is the opposite of perfectionism. It is the discipline of building something you will not have to rebuild — because you understood it before you built it, because you chose the tool that fit the job, because you wrote the constitution carefully and let everything else inherit from it.

This book is that understanding, written down.

It will not make you a faster developer. It might make you a slower one, at first — slower because you stop and ask why before you ask how. But the things you build this way tend to stay built.

That is what I wanted. That is what this is.

---

*Everything in this book is in service of that click.*

