---
date: 2026-02-14
image: claude.png
excerpt: Ein Überblick darüber, wie ich mit Claude Code programmiere (Stand Mitte Februar 2026). Erwartet, dass es ab März '26 veraltet ist 😉
tags: code
translation: de
source_language: en
source_hash: c1b098ab5de9c363bc2e25d9798aa85422774ea318267a39100bc64c2686076f
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:51.629685+00:00
generated_by: simplified-translation-system
---

Da ich es ein paar Mal vorgestellt habe und noch öfter danach gefragt wurde, hier ein kurzer Überblick darüber, wie ich arbeite, wenn ich mit Claude Code programmiere. Es ist ein einfacher Workflow, nichts Besonderes. Der Fokus liegt zuerst auf der Spezifikation, die iteriert wird, bevor das eigentliche Programmieren beginnt.

So funktioniert es:

- Ich beginne damit, eine kurze Spezifikation zu notieren (z.B. in `spec.md`). Oft nur eine einzelne Textzeile, gefolgt von einer Aufzählungsliste mit meinen Gedanken. Alles als Markdown-Datei.
- Dann führe ich meinen `/spec-build-out` Befehl aus: `/spec-build-out spec.md` (Hinweis: Ich arbeite oft im integrierten Terminal in VScode, und dort kann man die md-Datei per Drag-and-Drop ins Terminal ziehen, und es wird der gesamte Dateiname eingefügt).
- Das erweitert und verfeinert meine `spec.md`. Ich lese sie, überarbeite sie und kommentiere sie. Ich markiere meine Notizen mit `->`.
- Dann führe ich den `/spec-iterate` Befehl aus: Das integriert meine Anmerkungen und bereinigt `spec.md` erneut.
- Dann kommentiere ich erneut, führe `/spec-iterate` erneut aus, und so weiter.
- Wenn ich das Gefühl habe, dass alles richtig aussieht, starte ich ein `/new` Gespräch und führe `/spec-ready-or-not spec.md` aus.
- Das fügt alle offenen Probleme, die es gefunden hat, am Ende von `spec.md` hinzu.
- Gleiches Spiel: `spec.md` kommentieren, dann `/spec-iterate`.
- Irgendwann bin ich zufrieden. Dann committe ich die Spezifikationen und lasse Claude sie implementieren. Manchmal starte ich zuerst mit einem `/new`, um mit einem sauberen, frischen Kontext zu beginnen.

Meine `/`-Befehle:

- [/spec-build-out](spec-build-out.md)
- [/spec-iterate](spec-iterate.md)
- [/spec-ready-or-not](spec-ready-or-not.md)
- [/spec-finish](spec-finish.md)

### Kommentare, Notizen und Gedanken

Als ich das Claude `/insights` ausführte, wurde ich für den **Disziplinierten Spezifikationsgetriebenen Entwicklungszyklus** gelobt 😉

Ich habe ein bisschen mit der Erklärung an Claude herumgespielt, wie lang die `spec.md` sein sollte. Ohne Anleitung wurde sie riesig und enthielt fast den gesamten Code, den es in die Codebasis einfügen wollte. Sobald ich ein `Bitte halte das Dokument kurz! Füge Code-Snippets nur hinzu, wenn sie WIRKLICH wichtig sind!!` hinzufügte, wurde es kürzer - manchmal zu kurz.

`/insights` schlug auch folgende Ergänzung zu meiner `claude.md` vor:

```markdown
## Spezifikations-Workflow

Beim Iterieren von Spezifikationsdokumenten:

1. Achte immer auf Benutzeranmerkungen (z.B. '->' Pfeile, Tags wie [ACCEPTED], [REJECTED]) beim ERSTEN Durchgang — erneutes Auffordern ist nicht erforderlich.
2. Beim Konsolidieren einer Spezifikation entferne abgelehnte Optionen vollständig und halte das Dokument prägnant.
3. Nach der Finalisierung der Spezifikation sicherstellen, dass alle offenen Fragen geklärt sind, bevor zur Implementierung übergegangen wird.
```