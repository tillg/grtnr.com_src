---
Tags: tech, AI
Title: Jenseits des Vibe-Codings - Neugestaltung von Filmz
Date: 2025-05-21
image: filmz.png
summary: Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz mit _Vibe-Coding_ erstellt. Das ist schön, bis man mit _Vibe-Debugging_ konfrontiert wird. Jetzt mache ich einen neuen Versuch und beginne auf eine strukturiertere Weise.
Translation: de
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T16:30:38.718740
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-21-beyond-vibe-coding/2025-05-21-beyond-vibe-coding.md
Generated-By: automatic-translation-plugin
---

<img src="filmz.png" alt="Filmz" width="300">

Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz erstellt: behalten Sie den Überblick über Filme und Serien, die Sie sehen möchten oder bereits gesehen haben. Bewahren Sie zusätzliche persönliche Informationen wie "Wie hat es mir gefallen?" (d.h. meine persönliche Bewertung), "Für welches Publikum würde ich es empfehlen?" (Erwachsene, Kinder, Familie) "Wann und wo habe ich es gesehen" usw. Und dann kommt das Teilen: Weitergeben von Filmempfehlungen an Freunde, entweder einen Film nach dem anderen oder Listen.

Da ich damals kein Swift kannte, habe ich es im _Vibe-Coding_-Stil erstellt, voll unterstützt von AI (damals hauptsächlich Cursor.ai). Das gab mir einen schnellen Start, aber ich war verloren, sobald ich komplexere Funktionen hinzufügen wollte, die eine gut strukturierte Codebasis erforderten. Und da ich nicht viel über Swift wusste, konnte ich es auch nicht tun. Vibe-Debugging funktioniert nicht - noch nicht...

Also fange ich hier wieder an, und mit einem anderen Ansatz: Ich werde versuchen, auf ähnliche Weise zu arbeiten, wie ich es mit einem intelligenten, aber junior Entwicklerkollegen tun würde. Der Fokus wird auf einem schrittweisen Ansatz liegen, begleitet von einer ordnungsgemäßen Dokumentation: Beschreibungen der aktuellen Aufgabe, Beschreibung der Architekturänderungen, der untersuchten / in Betracht gezogenen Optionen und warum was gewählt wurde...

[Ich habe mit meinem AI-Freund ChatGPT gearbeitet](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9) und plane, mit einer Struktur wie unten beschrieben zu beginnen.

```text
README.md                        # Projektübersicht und Setup-Anweisungen
docs/                     # Alles, was *nicht* Quellcode ist, lebt hier
├── index.md              # Hochrangige funktionale Übersicht (benutzerzentriert)
├── architecture.md       # Hochrangige Technik
├── glossary.md           # Fachvokabular
├── features/             # Ein Unterverzeichnis *pro* Funktion ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # "User Story" oder Problemstellung
│   │   ├── 02-ui-flow.md         # Wire-Flow, Screenshots, Diagramme → PNG/Drawio *im selben Ordner* aufbewahren
│   │   ├── 03-design.md          # Technisches Design & Pseudocode
│   │   ├── 04-test-plan.md       # Akzeptanz- & Randfallliste
│   │   └── dark-mode.drawio.png  # Diagramm liegt neben dem Text, der darauf verweist
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Leeres Skelett, das Sie kopieren, wenn Sie eine Funktion hinzufügen
├── data-structure/            # Querschnittsfeature, Entitätsstrukturen oder ERDs, Migrationsnotizen
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architektur-Entscheidungsprotokolle
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # Historie im Stil von "Keep a Changelog"
```

2025-05-28: Ich nehme dies als Ausgangspunkt, arbeite und sehe, was fehlt. Und füge die fehlenden Teile auf dem Weg hinzu.