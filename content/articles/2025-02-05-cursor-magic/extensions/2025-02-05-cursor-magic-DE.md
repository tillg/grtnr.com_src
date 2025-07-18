---
date: 2025-02-05
image: david_cursor_magic.png
excerpt: Ich habe dieses Video eines Entwicklers mit VIELEN hilfreichen Tipps zur Nutzung von Cursor gefunden - hier sind meine Erkenntnisse.
translation: de
source_language: en
source_hash: 6f5f3859413aa8ee235065659ab80dc33db60f32d1c181831639b1989c52de3e
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T21:57:15.009446
generated_by: simplified-translation-system
---

[TOC]

Letztes Wochenende entdeckte ich dieses Video von David Ondrej: [I spent 400+ hours in Cursor, here’s what I learned](https://youtu.be/gYLNxUxVomY?si=1Q2x2UWgqy1RHvLt). Der Titel ist nicht besonders ansprechend, aber der Inhalt war für mich sehr hilfreich. Hier sind also meine Notizen, damit ich alle seine Tipps nutzen und die verschiedenen Prompts und Snippets zur Hand haben kann, um sie beim Programmieren zu verwenden.

<iframe width="560" height="315" src="https://www.youtube.com/embed/gYLNxUxVomY?si=xQAMyMvQCsSwWztk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Prompt-Struktur

Die allgemeine Prompt-Struktur, die David vorschlägt:

1. was wir tun
2. relevante Dateien taggen
3. wie ausführen // was nicht zu tun ist
4. Kontext-Dump
5. Kernanweisung wiederholen
6. Ausgabeformat

## Cursorrules

`.cursorrules.md` ist eine Datei, die Sie in Ihr Projektverzeichnis auf oberster Ebene legen, um der KI mehr Kontext über Ihr Projekt zu geben. Hier ist die Struktur der Datei, die David vorschlägt:

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
frontend/.env

# AKTUELLE DATEISTRUKTUR

Hier fügen Sie den Inhalt dieses Befehls ein, damit Cursor über Ihre Projektstruktur informiert ist:
tree -L 4 -a -I 'node*modules | -git|\_pycache*|.DS\_$

# GITHUB PUSH PROZESS

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
- IMMER einfachen, sauberen und modularen Code schreiben.
- Verwenden Sie klare und leicht verständliche Sprache. Schreiben Sie in kurzen Sätzen.

# Fehlerbehebung

- NICHT VORSCHNELL SCHLUSSFOLGERN! Berücksichtigen Sie mehrere mögliche Ursachen, bevor Sie sich entscheiden.
- Erklären Sie das Problem in einfachem Englisch
- Machen Sie nur die minimal notwendigen Änderungen, ändern Sie so wenige Codezeilen wie möglich
- Bei seltsamen Fehlern bitten Sie den Benutzer, eine Perplexity-Websuche durchzuführen, um die neuesten Informationen zu erhalten

# Bauprozess

- ﻿﻿Überprüfen Sie, ob jede neue Funktion funktioniert, indem Sie dem Benutzer sagen, wie er sie testen kann
- ﻿﻿Schreiben Sie KEINEN komplizierten und verwirrenden Code. Wählen Sie den einfachen und modularen Ansatz.
- ﻿﻿Wenn Sie nicht sicher sind, was zu tun ist, sagen Sie dem Benutzer, dass er eine Websuche durchführen soll

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

Beginnen Sie mit dem Schreiben von 3 Überlegungsabsätzen, in denen Sie analysieren, was der Fehler sein könnte. NICHT VORSCHNELL SCHLUSSFOLGERN.

NICHT AUFHÖREN ZU ARBEITEN, bis…

Antworten Sie kurz

LÖSCHEN SIE KEINE KOMMENTARE

Sie sollten den Überlegungsabsatz mit viel Unsicherheit beginnen und langsam Vertrauen gewinnen, während Sie mehr über das Element nachdenken.
```

## Größere Prompts

### Zusammenfassung des aktuellen Zustands

Wird verwendet, um einen Compose-Flow zusammenzufassen und zu einem neuen Compose-Dialog überzugehen.

```text
Bevor wir fortfahren, benötige ich von Ihnen eine Zusammenfassung des aktuellen Projektzustands.

Formatieren Sie dies als 3 prägnante Absätze, in denen Sie beschreiben, was wir gerade getan haben, was nicht funktioniert hat, welche Dateien aktualisiert/erstellt wurden, welche Fehler zu vermeiden sind, welche wichtigen Erkenntnisse/Lektionen wir gelernt haben, welche Probleme/Fehler wir haben,… und alles andere, was ein Programmierer benötigt, um produktiv an diesem Projekt zu arbeiten.

Schreiben Sie in einem gesprächigen, aber informativen Ton, ähnlich einer README-Datei auf GitHub, die sehr informationsdicht ist und ohne unnötigen Ballast. Schließen Sie keine Annahmen oder Theorien ein, nur die Fakten.

Ich erwarte drei prägnante Absätze, geschrieben, als ob Sie einem anderen Programmierer Anweisungen geben würden und dies alles wäre, was Sie ihm sagen könnten.
```

### Unvoreingenommen 50/50

```text
BEVOR SIE ANTWORTEN, möchte ich, dass Sie zwei detaillierte Absätze schreiben, die jeweils für eine dieser Lösungen argumentieren - ziehen Sie keine voreiligen Schlüsse, betrachten Sie ernsthaft beide Ansätze

dann, nachdem Sie fertig sind, sagen Sie mir, ob eine dieser Lösungen offensichtlich besser ist als die andere und warum.
```

### Ein-Absatz-Suchanfrage

```text
Lassen Sie uns eine Websuche durchführen. Ihre Aufgabe ist es, eine Ein-Absatz-Suchanfrage zu schreiben, als ob Sie einem menschlichen Forscher sagen würden, was zu finden ist, einschließlich aller relevanten Kontexte. Formatieren Sie den Absatz als klare Anweisungen, die einen Forscher dazu auffordern, zu finden, wonach wir suchen. Fragen Sie nach Code-Snippets oder technischen Details, wenn relevant.
```

## Anweisungen

David schlägt vor, ein Verzeichnis `instructions` zu haben, das md-Dateien mit Tipps für die KI enthält. Auf diese Weise können Sie von der Composer-Eingabeaufforderung auf diese Dateien verweisen. Er bevorzugt diese Art von Anweisungsdateien gegenüber dem Verweis auf @Docs in Cursor, was anscheinend noch nicht so gut funktioniert.

Erwähnte Anweisungsdateien:

- `supabase.md`: Eine Datei, die die Struktur seiner Datenbank beschreibt, sodass Cursor über Tabellen, Felder, Pflichtfelder usw. informiert ist.
- `roadmap.md`: Eine Erklärung der Roadmap Ihres Projekts.

## Andere Werkzeuge

Neben Cursor verwendet David viele andere Werkzeuge. Einige der von ihm erwähnten:

- [ChatGPT](https://chatgpt.com)
- [Claude](https://claude.ai) für Nebengespräche mit einer fortgeschrittenen KI.
- [Perplexity](https://www.perplexity.ai) für intelligente Websuchen.
- [WisprFlow](https://wisprflow.ai) um zu sprechen, anstatt zu tippen
- [v0](https://v0.dev) ein Tool, um Web-Apps im Browser zu erstellen, indem man mit einer KI chattet.
- [Lovable](https://lovable.dev) für den Aufbau von Backends, insbesondere mit [Supabase](https://supabase.com)
- [Bolt](https://bolt.new) um Websites zu erstellen.