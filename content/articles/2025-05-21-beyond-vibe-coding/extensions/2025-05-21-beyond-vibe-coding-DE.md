---
date: 2025-05-21
image: filmz.png
excerpt: Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz mit _vibe_coding_ gebaut. Das ist schön, bis man beim _vibe_debugging_ landet. Jetzt starte ich einen neuen Versuch, diesmal auf eine strukturiertere Weise.
title: Jenseits von Vibe Coding - Filmz neu gestalten
tags: tech, AI
translation: de
source_language: en
source_hash: 6afa6c8efca11981762e933a16b098724592997958fb00720f7d8a71e54bd797
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:32.378526+00:00
generated_by: simplified-translation-system
---

<img src="filmz.png" alt="Filmz" width="300">

Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz gebaut: Behalte den Überblick über Filme und Serien, die du sehen möchtest oder die du gesehen hast. Halte persönliche Zusatzinformationen fest wie "Wie hat es mir gefallen?" (also meine persönliche Bewertung), "Für welches Publikum würde ich es empfehlen?" (Erwachsene, Kinder, Familie) "Wann und wo habe ich es gesehen" usw. Und dann kommt das Teilen: Filmempfehlungen an Freunde weitergeben, entweder einen Film nach dem anderen oder Listen.

Da ich damals kein Swift konnte, habe ich es im _vibe_coding_-Stil gebaut, voll unterstützt von KI (damals hauptsächlich Cursor.ai). Das verschaffte mir einen schnellen Start, aber ich war verloren, als ich komplexere Funktionen hinzufügen wollte, die eine gut strukturierte Codebasis erforderten. Und da ich nicht viel über Swift wusste, konnte ich es auch nicht machen. Vibe Debugging funktioniert nicht - noch nicht...

Also fange ich hier nochmal an, und zwar mit einem anderen Ansatz: Ich werde versuchen, ähnlich zu arbeiten, wie ich es mit einem klugen, aber noch unerfahrenen Entwicklerkollegen tun würde. Der Fokus wird auf einem schrittweisen Ansatz liegen, begleitet von einer ordentlichen Dokumentation: Beschreibungen der aktuellen Aufgabe, Beschreibung der Architekturänderungen, der Optionen, die geprüft / überlegt wurden, und was warum gewählt wurde...

[Ich habe mit meinem KI-Freund ChatGPT gearbeitet](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9) und plane, mit einer Struktur zu beginnen, wie unten beschrieben.

```text
README.md                        # Projektübersicht und Einrichtungshinweise
docs/                     # Alles, was *nicht* Quellcode ist, lebt hier
├── index.md              # Funktionale Übersicht auf hoher Ebene (nutzerzentriert)
├── architecture.md       # Technische Übersicht auf hoher Ebene
├── glossary.md           # Fachvokabular
├── features/             # Ein Unterverzeichnis *pro* Feature ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # „User Story“ oder Problemstellung
│   │   ├── 02-ui-flow.md         # Wireflow, Screenshots, Diagramme → PNG/Drawio *im selben Ordner* behalten
│   │   ├── 03-design.md          # Technisches Design & Pseudocode
│   │   ├── 04-test-plan.md       # Akzeptanz- & Randfallliste
│   │   └── dark-mode.drawio.png  # Diagramm sitzt neben dem Text, der darauf verweist
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Leeres Skelett, das du kopierst, wenn du ein Feature hinzufügst
├── data-structure/            # Übergreifende Feature-, Entitätsstrukturen oder ERDs, Migrationshinweise
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architektur-Entscheidungsprotokolle
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # „Keep a Changelog“-Stil Geschichte
```

2025-05-28: Ich nehme dies als Ausgangspunkt, arbeite und schaue, was fehlt. Und füge die fehlenden Teile unterwegs hinzu.