---
date: 2026-02-14
excerpt: Ein Überblick darüber, wie ich mit Claude Code programmiere (Stand heute, Mitte Februar 2026). Erwarten Sie, dass es ab März '26 veraltet ist 😉
Tags: code
image: claude.png
title: Wie ich mit&nbsp;Claude programmiere
translation: de
source_language: en
source_hash: 2a66ea615ac944fd5d9a6942aed81ef4504c5126213f75c514c87ed4000a8d8a
translator: gpt-4o-2024-08-06
translate_date: 2026-02-14T10:47:47.572452
generated_by: simplified-translation-system
---

Da ich es ein paar Mal vorgestellt habe und da ich noch öfter danach gefragt wurde, hier ein kurzer Überblick darüber, wie ich arbeite, wenn ich mit Claude Code programmiere. Es ist ein einfacher Workflow, nichts Kompliziertes. Er konzentriert sich zuerst auf die Spezifikation und iteriert diese, bevor das eigentliche Programmieren beginnt.

So funktioniert es:

- Ich beginne damit, eine kurze Spezifikation niederzuschreiben (z.B. in `spec.md`). Oft nur eine einzige Textzeile, gefolgt von einer Aufzählungsliste mit meinen Gedanken. Alles als Markdown-Datei.
- Dann führe ich meinen `/spec-build-out` Befehl aus: `/spec-build-out spec.md` (Hinweis: Ich arbeite oft im integrierten Terminal in VScode, und dort können Sie die md-Datei per Drag-and-Drop ins Terminal ziehen, und es wird der gesamte Dateiname eingefügt).
- Dies erweitert und verfeinert meine `spec.md`. Ich lese sie, überarbeite sie und kommentiere sie. Meine Anmerkungen markiere ich mit `->`.
- Dann führe ich den `/spec-iterate` Befehl aus: Dies integriert meine Anmerkungen und bereinigt `spec.md` erneut.
- Dann kommentiere ich erneut, führe `/spec-iterate` erneut aus, und so weiter.
- Wenn ich das Gefühl habe, dass alles richtig aussieht, starte ich ein `/new` Gespräch und führe `/spec-ready-or-not spec.md` aus.
- Dies fügt alle offenen Probleme, die es gefunden hat, am Ende von `spec.md` hinzu.
- Dasselbe Spiel: `spec.md` kommentieren, dann `/spec-iterate`.
- Irgendwann bin ich zufrieden. Dann committe ich die Spezifikationen und lasse Claude sie implementieren. Manchmal beginne ich zuerst mit einem `/new`, um mit einem sauberen, frischen Kontext zu starten.

Meine `/`-Befehle:

- [/spec-build-out](spec-build-out.md)
- [/spec-iterate](spec-iterate.md)
- [/spec-ready-or-not](spec-ready-or-not.md)
- [/spec-finish](spec-finish.md)

### Kommentare, Notizen und Gedanken

Als ich das Claude `/insights` ausführte, wurde ich für den **Disziplinierten Spezifikationsgetriebenen Entwicklungszyklus** gelobt 😉

Ich habe ein wenig damit experimentiert, Claude zu erklären, wie lang die `spec.md` sein sollte. Ohne jegliche Anleitung wurde sie riesig und enthielt fast den gesamten Code, den es in die Codebasis einfügen wollte. Sobald ich ein `Bitte halten Sie das Dokument kurz! Fügen Sie Code-Snippets nur hinzu, wenn sie WIRKLICH entscheidend sind!!` hinzufügte, wurde es kürzer - manchmal zu kurz.

`/insights` schlug auch die folgende Ergänzung zu meiner `claude.md` vor:

```markdown
## Spezifikations-Workflow

Beim Iterieren von Spezifikationsdokumenten:

1. Suchen Sie immer nach Benutzeranmerkungen (z.B. '->' Pfeile, Tags wie [ACCEPTED], [REJECTED]) beim ERSTEN Durchgang — erneutes Nachfragen ist nicht erforderlich.
2. Beim Konsolidieren einer Spezifikation entfernen Sie abgelehnte Optionen vollständig und halten Sie das Dokument prägnant.
3. Nach der Finalisierung der Spezifikation bestätigen Sie, dass alle offenen Fragen geklärt sind, bevor Sie zur Implementierung übergehen.
```