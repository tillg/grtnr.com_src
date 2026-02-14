---
date: 2026-02-14
excerpt: An overview of how I code with claude code (as of today, mid-Feb 2026). Expect it to be outdated as of March '26 😉
Tags: code
image: claude.png
---

Since I presented it a couple of times, and since I got asked even more often, here is a short overview of how I work when coding with Claude Code. It's a simple workflow, nothing fancy. It focusses on the spec first, iterating them before launching the actual coding.

Here is how it works:

- I start by jotting down a brief spec (e.g. in `spec.md`). Often just a single line of text, followed by a bullet list with my thoughts. All as a markdown file.
- Then I run my `/spec-build-out` command: `/spec-build-out spec.md` (Note: I often work in the integrated terminal in VScode, and there you can drag-and-drop the md file into the terminal and it will paste in the entire file name).
- This expands and refines my `spec.md`. I read it, revise it, and annotate it. I mark my notes with `->`.
- Then I run the `/spec-iterate` command: This incorporates my annotations and cleans up `spec.md` again.
- Then I annotate again, run `/spec-iterate` again, and so on.
- When I feel like everything looks right, I start a `/new` conversation and run `/spec-ready-or-not spec.md`.
- This appends any open issues it found to the end of `spec.md`.
- Same game: annotate `spec.md`, then `/spec-iterate`.
- At some point I'm satisfied. Then I commit the specs and let Claude implement them. Sometimes I start with a `/new` first, to begin with a clean, fresh context.

My `/`-commands:

- [/spec-build-out](spec-build-out.md)
- [/spec-iterate](spec-iterate.md)
- [/spec-ready-or-not](spec-ready-or-not.md)
- [/spec-finish](spec-finish.md)

### Comments, notes and thoughts

When I ran the Claude `/insights` I got complimented for the **Disciplined Spec-Driven Development Cycle** 😉

I played around a bit with the explanation to Claude about how long the `spec.md` should be. Without any guidance it became huge, contained almost all the code it planned to insert in the code base. Once I added a `Please keep the document short! Add code snippets only if they are REALLY key!!` it became shorter - sometimes too short.

`/insights` also suggested the following addition to my `claude.md`:

```markdown
## Spec Workflow

When iterating on spec documents:

1. Always look for user annotations (e.g., '->' arrows, tags like [ACCEPTED], [REJECTED]) on the FIRST pass — do not require re-prompting.
2. When consolidating a spec, remove rejected options entirely and keep the document concise.
3. After spec finalization, confirm all open questions are resolved before moving to implementation.
```
