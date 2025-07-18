---
Tags: tech, AI
Title: Au-delà du _vibe coding_ - Repenser Filmz
Date: 2025-05-21
image: filmz.png
summary: Il y a quelque temps, j'ai construit une petite application iOS appelée Filmz avec du _vibe coding_. Cela semble bien jusqu'à ce que vous finissiez par faire du _vibe debugging_. Je tente donc une nouvelle approche, en commençant de manière plus structurée.
translation: fr
source_language: en
source_hash: 6afa6c8efca11981762e933a16b098724592997958fb00720f7d8a71e54bd797
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T21:51:04.847498
generated_by: simplified-translation-system
---

<img src="filmz.png" alt="Filmz" width="300">

Il y a quelque temps, j'ai construit une petite application iOS appelée Filmz : suivre les films et séries que vous souhaitez voir ou que vous avez vus. Conserver des informations personnelles supplémentaires comme "comment l'ai-je aimé ?" (c'est-à-dire ma note personnelle), "À quel public le recommanderais-je ?" (Adultes, enfants, famille) "Quand et où l'ai-je vu" etc. Et ensuite vient le partage : transmettre des recommandations de films à des amis, soit un film à la fois, soit des listes.

Comme je ne connaissais pas Swift à l'époque, je l'ai construit dans un style de _vibe coding_, entièrement soutenu par l'IA (à l'époque principalement Cursor.ai). Cela m'a permis de démarrer rapidement, mais j'étais perdu une fois que je voulais ajouter des fonctionnalités plus complexes nécessitant une base de code bien structurée. Et comme je ne connaissais pas bien Swift, je ne pouvais pas le faire non plus. Le _vibe debugging_ ne fonctionne pas - encore...

Je recommence donc ici, avec une approche différente : je vais essayer de travailler de la même manière que je le ferais avec un développeur junior mais intelligent. L'accent sera mis sur une approche progressive, accompagnée d'une documentation appropriée : descriptions de la tâche à accomplir, description des changements d'architecture, des options qui ont été examinées / envisagées et ce qui a été choisi et pourquoi...

[J'ai travaillé avec mon ami IA ChatGPT](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9), et je prévois de commencer avec une structure comme décrite ci-dessous.

```text
README.md                        # Vue d'ensemble du projet et instructions de configuration
docs/                     # Tout ce qui n'est *pas* du code source se trouve ici
├── index.md              # Vue d'ensemble fonctionnelle de haut niveau (centrée sur l'utilisateur)
├── architecture.md       # Technologie de haut niveau
├── glossary.md           # Vocabulaire du domaine
├── features/             # Un sous-répertoire *par* fonctionnalité ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # “User story” ou énoncé du problème
│   │   ├── 02-ui-flow.md         # Wire-flow, captures d'écran, diagrammes → conserver PNG/Drawio *dans le même dossier*
│   │   ├── 03-design.md          # Conception technique & pseudo-code
│   │   ├── 04-test-plan.md       # Liste d'acceptation & cas limites
│   │   └── dark-mode.drawio.png  # Le diagramme se trouve à côté du texte qui y fait référence
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Modèle vide à copier lors de l'ajout d'une fonctionnalité
├── data-structure/            # Structures d'entité ou ERD inter-fonctionnalités, notes de migration
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architecture Decision Records
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # Historique de style “Keep a Changelog”
```

2025-05-28 : Je prends cela comme point de départ, je travaille et je vois ce qui manque. Et j'ajoute les éléments manquants en cours de route.