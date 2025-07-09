---
Tags: tech, AI
Title: Jenseits des Vibe-Codings - Neugestaltung von Filmz
Date: 2025-05-21
image: filmz.png
summary: Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz mit _vibe_coding_ entwickelt. Das ist schön, bis man beim _vibe debugging_ landet. Jetzt starte ich einen neuen Versuch, diesmal auf eine strukturiertere Weise.
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:57:28.836542
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-21-beyond-vibe-coding/2025-05-21-beyond-vibe-coding.md
Generated-By: automatic-translation-plugin
---

<img src="filmz.png" alt="Filmz" width="300">

Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz entwickelt: Behalten Sie den Überblick über Filme und Serien, die Sie sehen möchten oder bereits gesehen haben. Halten Sie persönliche Zusatzinformationen fest wie „Wie hat es mir gefallen?“ (d.h. meine persönliche Bewertung), „Für welches Publikum würde ich es empfehlen?“ (Erwachsene, Kinder, Familie) „Wann und wo habe ich es gesehen?“ usw. Und dann kommt das Teilen: Weitergabe von Filmempfehlungen an Freunde, entweder einen Film nach dem anderen oder in Listen.

Da ich damals kein Swift konnte, habe ich es im _vibe coding_-Stil entwickelt, voll unterstützt von KI (damals hauptsächlich Cursor.ai). Das gab mir einen schnellen Start, aber ich war verloren, als ich komplexere Funktionen hinzufügen wollte, die eine gut strukturierte Codebasis erforderten. Und da ich nicht viel über Swift wusste, konnte ich es auch nicht umsetzen. Vibe-Debugging funktioniert noch nicht...

Also starte ich hier erneut, und mit einem anderen Ansatz: Ich werde versuchen, ähnlich zu arbeiten, wie ich es mit einem klugen, aber noch unerfahrenen Entwicklerkollegen tun würde. Der Fokus wird auf einem schrittweisen Ansatz liegen, begleitet von einer ordentlichen Dokumentation: Beschreibungen der aktuellen Aufgabe, Beschreibung der Architekturänderungen, der Optionen, die geprüft/überlegt wurden und was warum gewählt wurde...

[Ich habe mit meinem KI-Freund ChatGPT gearbeitet](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9) und plane, mit einer Struktur zu beginnen, wie unten beschrieben.

```text
README.md                        # Projektübersicht und Einrichtungshinweise
docs/                     # Alles, was *nicht* Quellcode ist, lebt hier
├── index.md              # Funktionale Übersicht auf hoher Ebene (benutzerzentriert)
├── architecture.md       # Technische Übersicht auf hoher Ebene
├── glossary.md           # Fachvokabular
├── features/             # Ein Unterverzeichnis *pro* Funktion ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # „User Story“ oder Problemstellung
│   │   ├── 02-ui-flow.md         # Wireflow, Screenshots, Diagramme → PNG/Drawio *im selben Ordner* behalten
│   │   ├── 03-design.md          # Technisches Design & Pseudocode
│   │   ├── 04-test-plan.md       # Akzeptanz- & Randfallliste
│   │   └── dark-mode.drawio.png  # Diagramm befindet sich neben dem Text, der darauf verweist
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Leeres Gerüst, das Sie beim Hinzufügen einer Funktion kopieren
├── data-structure/            # Übergreifende Funktionen, Entitätsstrukturen oder ERDs, Migrationshinweise
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architektur-Entscheidungsprotokolle
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # „Keep a Changelog“-Stil Historie
```

2025-05-28: Ich nehme dies als Ausgangspunkt, arbeite und sehe, was fehlt. Und füge die fehlenden Teile unterwegs hinzu.