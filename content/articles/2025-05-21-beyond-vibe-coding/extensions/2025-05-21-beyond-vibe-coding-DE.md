---
date: 2025-05-21
image: filmz.png
excerpt: Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz mit _vibe_coding_ entwickelt. Das ist schön, bis man beim _vibe_debugging_ landet. Jetzt starte ich einen neuen Versuch, diesmal auf eine strukturiertere Weise.
title: Jenseits von Vibe Coding - Neugestaltung von Filmz
tags: tech, AI
translation: de
source_language: en
source_hash: 6afa6c8efca11981762e933a16b098724592997958fb00720f7d8a71e54bd797
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:14:40.131761+00:00
generated_by: simplified-translation-system
---

<img src="filmz.png" alt="Filmz" width="300">

Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz entwickelt: Behalten Sie den Überblick über Filme und Serien, die Sie sehen möchten oder bereits gesehen haben. Speichern Sie persönliche Zusatzinformationen wie „Wie hat es mir gefallen?“ (d.h. meine persönliche Bewertung), „Für welches Publikum würde ich es empfehlen?“ (Erwachsene, Kinder, Familie) „Wann und wo habe ich es gesehen“ usw. Und dann kommt das Teilen: Weitergabe von Filmempfehlungen an Freunde, entweder ein Film nach dem anderen oder Listen.

Da ich damals kein Swift konnte, habe ich es im _vibe_coding_-Stil entwickelt, vollständig unterstützt von KI (damals hauptsächlich Cursor.ai). Das gab mir einen schnellen Start, aber ich war verloren, als ich komplexere Funktionen hinzufügen wollte, die eine gut strukturierte Codebasis erforderten. Und da ich nicht viel über Swift wusste, konnte ich es auch nicht umsetzen. Vibe Debugging funktioniert noch nicht...

Also starte ich hier erneut, und zwar mit einem anderen Ansatz: Ich werde versuchen, ähnlich zu arbeiten, wie ich es mit einem klugen, aber unerfahrenen Entwicklerkollegen tun würde. Der Fokus wird auf einem schrittweisen Ansatz liegen, begleitet von einer ordentlichen Dokumentation: Beschreibungen der anstehenden Aufgabe, Beschreibung der Architekturänderungen, der Optionen, die geprüft / bedacht wurden, und was warum gewählt wurde...

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
│   │   ├── 03-design.md          # Technisches Design & Pseudo-Code
│   │   ├── 04-test-plan.md       # Akzeptanz- & Randfallliste
│   │   └── dark-mode.drawio.png  # Diagramm befindet sich neben dem Text, der darauf verweist
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Leeres Gerüst, das Sie beim Hinzufügen eines Features kopieren
├── data-structure/            # Übergreifende Feature-, Entitätsstrukturen oder ERDs, Migrationshinweise
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architektur-Entscheidungsprotokolle
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # „Keep a Changelog“-Stil Verlauf
```

2025-05-28: Ich nehme dies als Ausgangspunkt, arbeite und sehe, was fehlt. Und füge die fehlenden Teile auf dem Weg hinzu.