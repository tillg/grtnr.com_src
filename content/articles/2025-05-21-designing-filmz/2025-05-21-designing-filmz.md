---
Tags: tech, AI
Title: An alternative AI peer programming approach - Redesigning Filmz
Date: 2025-05-21
image: filmz.png
summary: Some time ago I built a little iOS App called Filmz with _vibe_coding_. Turns out that's nice until you end up _vibe debugging_. So now I take a new attempt, starting in a more structured way.
---

<img src="filmz.png" alt="Filmz" width="300">

Some time ago I built a little iOS App called Filmz: keep track of films and shows you want to see or you have seen. Keep personal additional information like "how did I like it?" (I.e. my personal rating), "For what audience would I recommend it?" (Adults, kids, family) "When and where did I see it" etc. And then comes sharing: passing on film recommendations to friends, either one film at a time or lists.

As I didn’t know any Swift back then, I built it in a _vibe coding_ style, fully supported by AI (back then mainly Cursor.ai). This gave me a fast start, but I was lost once I wanted to add more complex features that required a well structured code base. And since I didn’t know much about Swift, I couldn’t do it either. Vibe debugging doesn’t work - yet…

So here I start again, and with a different approach: I will try to work in a similar way as I would with a smart but junior peer developer. The focus will be on a stepwise approach, followed along with a proper documentation: Descriptions of the task at hand, description of the architecture changes, of the options that were inspected / though of and what was chosen why...

[I worked with my AI friend ChatGPT](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9), and plan to start with a structure as described below.

```text
README.md                        # Project overview and setup instructions
docs/                     # Everything that is *not* source code lives here
├── index.md              # High-level functional overview (user-centric)
├── architecture.md       # High-level tech
├── glossary.md           # Domain vocabulary
├── features/             # One sub-dir *per* feature ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # “User story” or problem statement
│   │   ├── 02-ui-flow.md         # Wire-flow, screenshots, diagrams → keep PNG/Drawio *in same folder*
│   │   ├── 03-design.md          # Tech design & pseudo-code
│   │   ├── 04-test-plan.md       # Acceptance & edge-case list
│   │   └── dark-mode.drawio.png  # Diagram sits next to the text that references it
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Empty skeleton you copy when adding a feature
├── data-structure/            # Cross-feature, Entity structures or ERDs, migration notes
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architecture Decision Records
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # “Keep a Changelog” style history
```

2025-05-28: I take this as a starting point, work, and see what's missing. And add the missing bits on the way.
