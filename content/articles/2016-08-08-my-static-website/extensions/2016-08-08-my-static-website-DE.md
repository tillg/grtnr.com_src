---
layout: post
title: Meine statische Website
date_published: 2016-08-08T00:00:00.000Z
image: static_site.jpg
tags: Tech
excerpt: Statische Websites werden heutzutage zum Standard. Also habe ich mir das auch angesehen und einige Website-Generatoren verglichen.
translation: de
source_language: en
source_hash: abc8f2afa5ca8b18bbd09e77e2d20b6bcbaf8353c5a215dd2435191f52cbc396
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:24:17.150497
generated_by: simplified-translation-system
---

OK, jeder macht es, sogar ich mache es: Statische Websites. Sie sind schnell, sicher und erledigen die Berechnungen dort, wo sie hingehören (solange Sie keine ausgefallenen Anpassungen benötigen, warum sollte ein Server darüber nachdenken, wie die Seite zur Lesezeit aussieht?). Diese Seite hier ist statisch (erstellt mit [JBake](http://jbake.org/) und gehostet auf [Github](https://github.com/)). Es hat Spaß gemacht, sie einzurichten, sie funktioniert großartig - aber ich könnte meiner Mutter nicht erklären, wie man sie benutzt oder wie man Inhalte darauf veröffentlicht. Und genau darum sollte es bei einem CMS gehen: Es muss in erster Linie benutzbar sein.

Daher benötige ich ein anderes Setup. Ich plane, mir einige verschiedene Systeme für statische Websites anzusehen und eine Liste von Kriterien aufzustellen, anhand derer ich die verschiedenen Generatoren testen möchte...

## Kriterien

- Themes
  - Viele
  - Schön
  - Responsiv

- Einfach zu schreiben
  - Editor mit Vorschau
  - Einfache Handhabung und Referenzierung von Bildern
  - Bilder in der Vorschau
  - Videos
  - Tabellen
  - Code mit Syntax-Highlighting
  - Automatisierte Konsistenzprüfung, d.h. die generierte Website ist korrekt, vollständig, die Verweise zeigen nicht ins Nirwana...

- Fähigkeit, eine [Accelerated Mobile Page](https://www.ampproject.org/) zu erstellen
- Funktionale Features & Seiten
  - Tags, Tag-Seiten, Tag-Cloud (könnte auch eine Erweiterung sein)
  - Veröffentlichbar auf Github (es ist sehr schnell, kostenlos und zuverlässig)
  - Website privat machen, d.h. nur für registrierte Mitglieder zugänglich
  - Veröffentlichung per E-Mail
  - Kommentar per E-Mail
  - Nachrichten per E-Mail an registrierte Benutzer senden
  - Bilder für schnelle Lieferung verkleinern
  - Einfach neue Themes erstellen, Themes sollten nur CSS sein
  - Basierend auf anderem HTML, z.B. Bootstrap-Themes

- Erweiterbare Architektur
  - Erweiterungen hinzufügen können, z.B. Bildverarbeitungsprozess
  - Mindestens eine Programmiersprache, die ich ein wenig kenne - oder die ich neugierig bin zu lernen (das beschränkt es im Grunde auf Java und JavaScript)
  - Das generierte HTML sollte so einfach wie möglich sein. Alle Formatierungen befinden sich im CSS

## Generatoren

Beim Durchsuchen der Literatur (und Github) ist dies die Liste der Generatoren, die ich mir wahrscheinlich ansehen sollte:

- Jekyll - Erledigt
- Harp JS - Erledigt
- Hugo - Erledigt
- Metalsmith - Erledigt
- Nikola - Erledigt
- Octopress - Erledigt
- Hexo - Erledigt
- Hyde - Erledigt
- Pelican - Erledigt
- Nanoc - Erledigt
- Middleman - Erledigt
- Lektor - Erledigt
- Gatsby - Erledigt
- Expose - Erledigt
- Wintersmith - Erledigt
- Doc pad - Erledigt
- kirby - Erledigt

## Bewertungsmatrix

| Generator                                    | Programmiersprache      | Themes    | Formate                                        | Kommentar                                                                                                             |
| :------------------------------------------- | :---------------------- | :-------- | :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| [Jekyll](https://jekyllrb.com/)              | Ruby --                 | Viele ++  | Markdown, Textile, Liquid ++                   |                                                                                                                       |
| _[Harp JS](https://harpjs.com/)_             | NodeJS ++               | Einige 00 | Markdown, EJS, Jade, LESS, Stylus... ++        |                                                                                                                       |
| [Hugo](https://gohugo.io/)                   | GO --                   | Einige 00 | Markdown, asciidoc, reStructure ++             |                                                                                                                       |
| _[Metalsmith](http://www.metalsmith.io/)_    | Node JS --              |           |                                                | Sieht sehr flexibel aus. Siehe auch http://dbushell.com/2015/05/11/wordpress-to-metalsmith/                           |
| [Nikola](https://getnikola.com/)             | Python --               | Wenige -- | reStructuredText, Markdown,                    | Sieht nur so lala aus...                                                                                              |
| [Octopress](http://octopress.org/)           | Python --               | Einige 00 |                                                | Ist nur ein Paket um Jekyll.                                                                                          |
| _[Hexo](https://hexo.io/)_                   | Node JS ++              | Einige 00 | Markdown, verschiedene Geschmacksrichtungen, Jekyll Plugins ++ | Sieht sehr flexibel aus, nutzt Standard-Template-Engines (EJS, Jade, Swig...), erlaubt die Integration von Skripten und Plugins. ++ |
| [Hyde](http://hyde.github.io/)               | Python --               | Wenige -- |                                                |                                                                                                                       |
| [Pelican](http://blog.getpelican.com/)       | Python --               |           |                                                |                                                                                                                       |
| [Nanoc](http://nanoc.ws/)                    | Ruby --                 |           |                                                |                                                                                                                       |
| [Moddleman](https://middlemanapp.com/)       | Python --               |           |                                                |                                                                                                                       |
| [Lektor](https://www.getlektor.com/)         | Python --               |           |                                                |                                                                                                                       |
| [Gatsby](https://github.com/gatsbyjs/gatsby) | Node JS, React          | Keine --  | Markdown 00                                    | Sieht sehr flexibel aus, aber ziemlich komplex...                                                                     |
| [Expose](https://github.com/Jack000/Expose)  | Shell-Skripte --        |           | Markdown und Bildordner                        | Speziell für Bilderseiten.                                                                                            |
| _[Wintersmith](http://wintersmith.io/)_      | Node JS, CoffeeScript ++| Wenige -- | Markdown, Jade, ...                            | Sieht sehr flexibel aus, LESS, Sass, Stylus. Könnte etwas komplex sein...                                             |
| [DocPad](http://docpad.org/)                 | Node JS ++              | Keine --  | Markdown und andere ++                         | Sieht flexibel, aber komplex aus                                                                                      |
| [kirby](https://getkirby.com/)               | PHP --                  |           | Markdown                                       |                                                                                                                       |

Als Ergebnis sollte ich mir _[Harp JS](https://harpjs.com/)_, _[Metalsmith](http://www.metalsmith.io/)_, _[Hexo](https://hexo.io/)_ und _[Wintersmith](http://wintersmith.io/)_ genauer ansehen.

Nach einem schnellen Durchlesen der Websites der oben genannten Tools habe ich mich entschieden, es mit _[Metalsmith](http://www.metalsmith.io/)_ zu versuchen.

## Editoren

Wenn Sie an die Generierung einer statischen Website aus einer Basis von Markdown-Dateien denken, wird es schnell natürlich, nach einem guten Editor zu suchen. Was wir von unserem Editor erwarten:

- Markdown-Vorschau
- Vorschau einschließlich des CSS und anderer Transformationen, die unser Site-Generator verwendet - um sicherzustellen, dass wir dasselbe Ergebnis sehen, wie es in der Produktion angezeigt wird
- Vorschau einschließlich Bilder. Dies könnte nicht trivial sein, da die Bilder möglicherweise in einem anderen Pfad in DEV als in PROD liegen...
  Insgesamt bedeutet dies, dass der Editor einen Kompilierungs-/Kompositionsprozess starten muss, der die Webansicht jedes Mal erzeugt, wenn die Markdown-Quelle geändert wurde.

Editoren, die wir uns ansehen

| Editor                             | Markdown / HTML Vorschau | Kommentare                     |
| :--------------------------------- | :----------------------- | :----------------------------- |
| Visual Code                        | ?                        | Könnte etwas Passendes haben   |
| Atom                               |                          |                                |
| Brackets                           |                          |                                |
| [Caret.io](https://caret.io/)      |                          |                                |
| [IA Writer](https://ia.net/writer) | Behauptet es...          |                                |

... wahrscheinlich noch einige mehr...

# Geschichte

- August 2016: Diese Seite gestartet
- Jan 2017: Fortgesetzt während des Aufenthalts in Thailand mit der Familie, Tomi & Beate