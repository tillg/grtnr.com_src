---
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:43:13.656405
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-02-05-cursor-magic/2025-02-05-cursor-magic.md
Generated-By: automatic-translation-plugin
---

```markdown
---
date: 2025-02-05
image: david_cursor_magic.png
excerpt: Ich habe dieses Video eines Entwicklers mit VIELEN hilfreichen Tipps zur Nutzung von Cursor gefunden - hier sind meine Erkenntnisse.
---

[TOC]

Letztes Wochenende entdeckte ich dieses Video von David Ondrej: [I spent 400+ hours in Cursor, here’s what I learned](https://youtu.be/gYLNxUxVomY?si=1Q2x2UWgqy1RHvLt). Der Titel ist nicht besonders ansprechend, aber der Inhalt war für mich sehr hilfreich. Hier sind also meine Notizen, damit ich all seine Tipps nutzen und die verschiedenen Prompts und Snippets zur Hand haben kann, wenn ich programmiere.

<iframe width="560" height="315" src="https://www.youtube.com/embed/gYLNxUxVomY?si=xQAMyMvQCsSwWztk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Prompt-Struktur

Die allgemeine Prompt-Struktur, die Deavid vorschlägt:

1. was wir tun
2. relevante Dateien taggen
3. wie ausführen // was nicht zu tun ist
4. Kontext-Dump
5. Kernanweisung wiederholen
6. Ausgabeformat

## Cursorrules

`.cursorrules.md` ist eine Datei, die Sie im obersten Verzeichnis Ihres Projekts ablegen, um der KI mehr Kontext über Ihr Projekt zu geben. Hier ist die Struktur der Datei, die David vorschlägt:

```markdown
# PROJEKTÜBERSICHT

# PERSÖNLICHKEIT

# TECH STACK

- wählen Sie einen Tech-Stack mit sehr populären Sprachen

# FEHLERBEHEBUNGSPROZESS

Schritt 1: Erklären Sie den Fehler in einfachen Worten
Schritt 2: Erklären Sie die Lösung in einfachen Worten
Schritt 3: Zeigen Sie, wie der Fehler behoben wird

# BAUPROZESS

# Unsere - Umgebungsvariablen

backend/.env
frontend/. env

# AKTUELLE DATEISTRUKTUR

Hier fügen Sie den Inhalt dieses Befehls ein, damit Cursor über Ihre Projektstruktur Bescheid weiß:
tree -L 4 -a -I 'node*modules | -git|\_pycache*|.DS\_$

# GITHUB PUSH-PROZESS

# WICHTIG

- Wiederholen Sie die wichtigsten Anweisungen.
```

Er empfiehlt auch dringend, eine `.cursorignore` zu haben, in der Sie Ihre `.env`-Dateien auflisten. Dies verhindert, dass Chat und Composer versehentlich in diese Dateien schreiben.

## KI-Regeln in den Cursor-Einstellungen

KI-Regeln sollten in den Cursor-Einstellungen festgelegt werden. Sie sollten nichts Projektspezifisches enthalten, sondern nur Programmierprinzipien, die Sie immer anwenden möchten. Das ist der Unterschied zu den `.cursorrules`, die auch projektspezifische Details enthalten.

Ein Beispiel:

```markdown
# Grundlegende Prinzipien

- Schreiben Sie sauberen, einfachen, lesbaren Code
- Implementieren Sie Funktionen auf die einfachste mögliche Weise
- Halten Sie Dateien klein und fokussiert (<200 Zeilen)
- Testen Sie nach jeder bedeutenden Änderung
- Konzentrieren Sie sich auf die Kernfunktionalität vor der Optimierung
- Verwenden Sie klare, konsistente Benennungen
- Denken Sie gründlich nach, bevor Sie programmieren. Schreiben Sie 2-3 Überlegungsabsätze.
- Schreiben Sie IMMER einfachen, sauberen und modularen Code.
- Verwenden Sie klare und leicht verständliche Sprache. Schreiben Sie in kurzen Sätzen.

# Fehlerbehebung

- SPRINGEN SIE NICHT ZU SCHLUSSFOLGERUNGEN! Berücksichtigen Sie mehrere mögliche Ursachen, bevor Sie sich entscheiden.
- Erklären Sie das Problem in einfachem Englisch
- Machen Sie die minimal notwendigen Änderungen und ändern Sie so wenige Codezeilen wie möglich
- Bei seltsamen Fehlern bitten Sie den Benutzer, eine Perplexity-Websuche durchzuführen, um die neuesten Informationen zu erhalten

# Bauprozess

- ﻿﻿Überprüfen Sie jede neue Funktion, indem Sie dem Benutzer mitteilen, wie er sie testen kann
- ﻿﻿Schreiben Sie KEINEN komplizierten und verwirrenden Code. Wählen Sie den einfachen und modularen Ansatz.
- ﻿﻿Wenn Sie nicht sicher sind, was zu tun ist, bitten Sie den Benutzer, eine Websuche durchzuführen

# Kommentare

- Versuchen Sie IMMER, mehr hilfreiche und erklärende Kommentare in unseren Code einzufügen.
- Löschen Sie NIEMALS alte Kommentare - es sei denn, sie sind offensichtlich falsch / veraltet.
- Fügen Sie VIELE erklärende Kommentare in Ihren Code ein. Schreiben Sie IMMER gut dokumentierten Code.
- Dokumentieren Sie alle Änderungen und deren Begründung IN DEN KOMMENTAREN, DIE SIE SCHREIBEN
- Verwenden Sie beim Schreiben von Kommentaren klare und leicht verständliche Sprache. Schreiben Sie kurze Sätze.
```

## Hilfreiche kleine Prompts

David bietet eine Liste hilfreicher kleiner Prompts oder Prompt-Snippets. Ich habe einige davon hier für die Copy&Paste-Nutzung kopiert:

```text
Vorgehen wie ein Senior Developer mit Fokus auf klare Architektur.

Je weniger Codezeilen, desto besser.

Beginnen Sie mit dem Schreiben von 3 Überlegungsabsätzen, die analysieren, was der Fehler sein könnte. SPRINGEN SIE NICHT ZU SCHLUSSFOLGERUNGEN.

HÖREN SIE NICHT AUF ZU ARBEITEN, bis…

Antworten Sie kurz

LÖSCHEN SIE KEINE KOMMENTARE

Sie sollten den Überlegungsabsatz mit viel Unsicherheit beginnen und allmählich Vertrauen gewinnen, während Sie mehr über das Thema nachdenken.
```

## Größere Prompts

### Zusammenfassung des aktuellen Stands

Wird verwendet, um einen Compose-Flow zusammenzufassen und zu einem neuen Compose-Dialog überzugehen.

```text
Bevor wir fortfahren, benötige ich eine Zusammenfassung des aktuellen Stands des Projekts.

Formatieren Sie dies als 3 prägnante Absätze, in denen Sie beschreiben, was wir gerade getan haben, was nicht funktioniert hat, welche Dateien aktualisiert/erstellt wurden, welche Fehler zu vermeiden sind, welche wichtigen Erkenntnisse/Lektionen wir gelernt haben, welche Probleme/Fehler wir haben,… und alles andere, was ein Programmierer benötigt, um produktiv an diesem Projekt zu arbeiten.

Schreiben Sie in einem gesprächigen, aber informativen Ton, ähnlich einer README-Datei auf GitHub, die sehr informationsdicht ist und ohne jeglichen Schnickschnack oder Lärm. Schließen Sie keine Annahmen oder Theorien ein, nur die Fakten.

Ich erwarte drei prägnante Absätze, geschrieben, als ob Sie einem anderen Programmierer Anweisungen geben würden und dies alles wäre, was Sie ihm sagen könnten.
```

### Unvoreingenommenes 50/50

```text
BEVOR SIE ANTWORTEN, möchte ich, dass Sie zwei detaillierte Absätze schreiben, die jeweils für eine dieser Lösungen argumentieren - springen Sie nicht zu Schlussfolgerungen, ziehen Sie beide Ansätze ernsthaft in Betracht

dann, nachdem Sie fertig sind, sagen Sie mir, ob eine dieser Lösungen offensichtlich besser ist als die andere und warum.
```

### Ein-Absatz-Suchanfrage

```text
Lassen Sie uns eine Websuche durchführen. Ihre Aufgabe ist es, eine ein-Absatz-Suchanfrage zu schreiben, als ob Sie einem menschlichen Forscher sagen würden, was zu finden ist, einschließlich aller relevanten Kontexte. Formatieren Sie den Absatz als klare Anweisungen und beauftragen Sie einen Forscher, das zu finden, wonach wir suchen. Fragen Sie nach Code-Snippets oder technischen Details, wenn relevant.
```

## Anweisungen

David schlägt vor, ein Verzeichnis `instructions` zu haben, das md-Dateien mit Tipps für die KI enthält. Auf diese Weise können Sie von der Composer-Eingabeaufforderung auf diese Dateien verweisen. Er bevorzugt diese Art von Anweisungsdateien gegenüber dem Verweis auf @Docs in Cursor, was anscheinend noch nicht so gut funktioniert.

Von ihm erwähnte Anweisungsdateien:

- `supabase.md`: Eine Datei, die die Struktur seiner Datenbank beschreibt, damit Cursor über Tabellen, Felder, Pflichtfelder usw. Bescheid weiß.
- `roadmap.md`: Eine Erklärung der Roadmap Ihres Projekts.

## Andere Werkzeuge

Neben Cursor verwendet David viele andere Werkzeuge. Einige der von ihm erwähnten:

- [ChatGPT](https://chatgpt.com)
- [Claude](https://claude.ai) für Nebendiskussionen mit einer fortgeschrittenen KI.
- [Perplexity](https://www.perplexity.ai) für intelligente Websuchen.
- [WisprFlow](https://wisprflow.ai) um zu sprechen, anstatt zu tippen
- [v0](https://v0.dev) ein Tool, um Web-Apps im Browser zu erstellen, indem man mit einer KI chattet.
- [Lovable](https://lovable.dev) für den Aufbau von Backends, insbesondere mit [Supabase](https://supabase.com)
- [Bolt](https://bolt.new) um Websites zu erstellen.
```