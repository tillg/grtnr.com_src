---
Tags: tech, AI
Title: Jenseits von Vibe Coding - Neugestaltung von Filmz
Date: 2025-05-21
image: filmz.png
summary: Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz mit _vibe_coding_ entwickelt. Das ist schön, bis man beim _vibe debugging_ landet. Jetzt starte ich einen neuen Versuch, beginnend mit einer strukturierteren Herangehensweise.
title: Jenseits von Vibe Coding - Neugestaltung&nbsp;von Filmz
translation: de
source_language: en
source_hash: 0baaf964bfafb9b9e052524c58a4afed5b3780f25dcc06689b1641e6e60f822a
translator: gpt-4o-2024-08-06
translate_date: 2026-02-14T10:52:29.202262
generated_by: simplified-translation-system
---

<img src="filmz.png" alt="Filmz" width="300">

Vor einiger Zeit habe ich eine kleine iOS-App namens Filmz entwickelt: Behalten Sie den Überblick über Filme und Serien, die Sie sehen möchten oder bereits gesehen haben. Halten Sie persönliche Zusatzinformationen fest wie „Wie hat es mir gefallen?“ (d.h. meine persönliche Bewertung), „Für welches Publikum würde ich es empfehlen?“ (Erwachsene, Kinder, Familie), „Wann und wo habe ich es gesehen?“ usw. Und dann kommt das Teilen: Filmempfehlungen an Freunde weitergeben, entweder einen Film nach dem anderen oder Listen.

Da ich damals kein Swift konnte, habe ich es im _vibe coding_ Stil entwickelt, vollständig unterstützt von KI (damals hauptsächlich Cursor.ai). Das gab mir einen schnellen Start, aber ich war verloren, als ich komplexere Funktionen hinzufügen wollte, die eine gut strukturierte Codebasis erforderten. Und da ich nicht viel über Swift wusste, konnte ich es auch nicht umsetzen. Vibe Debugging funktioniert noch nicht...

Also starte ich hier erneut, und zwar mit einem anderen Ansatz: Ich werde versuchen, ähnlich zu arbeiten, wie ich es mit einem klugen, aber unerfahrenen Junior-Entwickler tun würde. Der Fokus wird auf einem schrittweisen Ansatz liegen, begleitet von einer ordentlichen Dokumentation: Beschreibungen der aktuellen Aufgabe, Beschreibung der Architekturänderungen, der inspizierten / in Betracht gezogenen Optionen und warum welche gewählt wurde...

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
│   └── _TEMPLATE/               # Leeres Gerüst, das Sie beim Hinzufügen eines Features kopieren
├── data-structure/            # Übergreifende Feature-, Entitätsstrukturen oder ERDs, Migrationshinweise
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Architektur-Entscheidungsprotokolle
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # „Keep a Changelog“ Stil Historie
```

2025-05-28: Ich nehme dies als Ausgangspunkt, arbeite und sehe, was fehlt. Und füge die fehlenden Teile unterwegs hinzu.