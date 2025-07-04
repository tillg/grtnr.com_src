---
Tags: tech, IA
Title: Au-delà du codage Vibe - Refonte de Filmz
Date: 2025-05-21
image: filmz.png
summary: Il y a quelque temps, j'ai créé une petite application iOS appelée Filmz avec le _codage_vibe_. C'est bien jusqu'à ce que vous finissiez par faire du _débogage vibe_. Alors maintenant, je fais une nouvelle tentative, en commençant de manière plus structurée.
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:43:14.925612
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-21-beyond-vibe-coding/2025-05-21-beyond-vibe-coding.md
Generated-By: automatic-translation-plugin
---

<img src="filmz.png" alt="Filmz" width="300">

Il y a quelque temps, j'ai créé une petite application iOS appelée Filmz : gardez une trace des films et des émissions que vous voulez voir ou que vous avez vus. Conservez des informations supplémentaires personnelles comme "qu'est-ce que j'en ai pensé ?" (c'est-à-dire ma note personnelle), "À quel public le recommanderais-je ?" (Adultes, enfants, famille) "Quand et où l'ai-je vu" etc. Et puis vient le partage : transmettre des recommandations de films à des amis, soit un film à la fois, soit des listes.

Comme je ne connaissais pas Swift à l'époque, je l'ai construit dans un style de _codage vibe_, entièrement soutenu par l'IA (à l'époque principalement Cursor.ai). Cela m'a permis de démarrer rapidement, mais j'étais perdu une fois que je voulais ajouter des fonctionnalités plus complexes qui nécessitaient une base de code bien structurée. Et comme je ne connaissais pas grand-chose à Swift, je ne pouvais pas le faire non plus. Le débogage vibe ne fonctionne pas - pas encore...

Alors voici que je recommence, et avec une approche différente : j'essaierai de travailler de la même manière que je le ferais avec un développeur junior mais intelligent. L'accent sera mis sur une approche par étapes, accompagnée d'une documentation appropriée : Descriptions de la tâche en cours, description des changements d'architecture, des options qui ont été inspectées / envisagées et ce qui a été choisi pourquoi...

[J'ai travaillé avec mon ami IA ChatGPT](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9), et je prévois de commencer avec une structure comme décrite ci-dessous.

```text
README.md                        # Vue d'ensemble du projet et instructions d'installation
docs/                     # Tout ce qui n'est *pas* du code source se trouve ici
├── index.md              # Vue d'ensemble fonctionnelle de haut niveau (centrée sur l'utilisateur)
├── architecture.md       # Tech de haut niveau
├── glossary.md           # Vocabulaire du domaine
├── features/             # Un sous-répertoire *par* fonctionnalité ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # "User story" ou énoncé du problème
│   │   ├── 02-ui-flow.md         # Wire-flow, captures d'écran, diagrammes → garder les PNG/Drawio *dans le même dossier*
│   │   ├── 03-design.md          # Conception technique & pseudo-code
│   │   ├── 04-test-plan.md       # Liste des cas d'acceptation & des cas limites
│   │   └── dark-mode.drawio.png  # Le diagramme se trouve à côté du texte qui le référence
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Squelette vide que vous copiez lors de l'ajout d'une fonctionnalité
├── data-structure/            # Cross-feature, structures d'entité ou ERDs, notes de migration
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Records de décisions d'architecture
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # Historique de style "Keep a Changelog"
```

2025-05-28: Je prends cela comme point de départ, je travaille, et je vois ce qui manque. Et j'ajoute les morceaux manquants en cours de route.