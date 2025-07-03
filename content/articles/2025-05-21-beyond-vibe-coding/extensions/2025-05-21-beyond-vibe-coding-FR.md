---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 6afa6c8efca11981762e933a16b098724592997958fb00720f7d8a71e54bd797
translation-type: automatic
---

[de→fr] <p><img alt="Filmz" src="/beyond-vibe-coding-redesigning-filmz/filmz.png" width="300"/></p>
<p>Some time ago I built a little iOS App called Filmz: keep track of films and shows you want to see or you have seen. Keep personal additional information like “how did I like it?” (I.e. my personal rating), “For what audience would I recommend it?” (Adults, kids, family) “When and where did I see it” etc. And then comes sharing: passing on film recommendations to friends, either one film at a time or lists.</p>
<p>As I didn’t know any Swift back then, I built it in a <em>vibe coding</em> style, fully supported by <span class="caps">AI</span> (back then mainly Cursor.ai). This gave me a fast start, but I was lost once I wanted to add more complex features that required a well structured code base. And since I didn’t know much about Swift, I couldn’t do it either. Vibe debugging doesn’t work - yet…</p>
<p>So here I start again, and with a different approach: I will try to work in a similar way as I would with a smart but junior peer developer. The focus will be on a stepwise approach, followed along with a proper documentation: Descriptions of the task at hand, description of the architecture changes, of the options that were inspected / thought of and what was chosen why…</p>
<p><a href="https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9" rel="noopener noreferrer" target="_blank">I worked with my <span class="caps">AI</span> friend ChatGPT</a>, and plan to start with a structure as described below.</p>
<div class="highlight"><pre><span></span><code>README.md                        # Project overview and setup instructions
docs/                     # Everything that is *not* source code lives here
├── index.md              # High-level functional overview (user-centric)
├── architecture.md       # High-level tech
├── glossary.md           # Domain vocabulary
├── features/             # One sub-dir *per* feature ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # “User story” or problem statement
│   │   ├── 02-ui-flow.md         # Wire-flow, screenshots, diagrams → keep PNG/Drawio *in same folder*
│   │   ├── 03-design.md          # Tech design &amp; pseudo-code
│   │   ├── 04-test-plan.md       # Acceptance &amp; edge-case list
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
</code></pre></div>
<p>2025-05-28: I take this as a starting point, work, and see what’s missing. And add the missing bits on the way.</p>