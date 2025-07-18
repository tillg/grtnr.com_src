---
title: Wie ich zu GitHub & JBake gewechselt bin
tags: tech, webSite
image: github.png
date: 2015-11-30
translation: de
source_language: en
source_hash: fc01f1f9e9e83ae138752a97264aff842fedb402ae12947d5e1806d51ce49b7c
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:19:24.615172
generated_by: simplified-translation-system
---

**\*** Diese Seite ist ~~im Aufbau~~ unvollständig... **\***

Zuerst: Es ist nicht meine Erfindung! Viele haben es schon vorher gemacht, es gibt viele Beschreibungen da draußen. Es hat trotzdem einige Zeit gedauert ;)

[Dieser](http://alexcican.com/post/guide-hosting-website-dropbox-github/) und [dieser](http://alexcican.com/post/blog-dropbox-scriptogram) Beitrag waren die inspirierendsten Quellen und die einfachste Erklärung (die Vertrauen gibt ;) ).

# Einrichtung

So sieht das Gesamtkonzept aus, das ich habe:

- Ein Verzeichnis auf meinem Mac, das den Inhalt enthält. Ich verwende die grundlegende Struktur, die [JBake](http://jbake.org) verwendet.
- Ein git-geklontes Verzeichnis auf meinem Mac mit dem Output des JBake-Prozesses
- Ein kleines Skript, das ich jedes Mal ausführe, wenn ich etwas geändert habe. Das Skript übernimmt das Backen und das Veröffentlichen auf Git
- Und natürlich die Einstellungen im DNS, um meinen Domainnamen auf die GitHub-IPs zu verweisen

## JBake

Warum benutze ich JBake? Ich mag das Prinzip und fühle mich in Java wohler als in anderen Programmiersprachen. Ich habe den internen Code von JBake nicht angefasst, aber ich bin zuversichtlich, dass ich es könnte.
Die Arbeitsweise von JBake ähnelt dem berühmten [Jekyll](https://jekyllrb.com/): Es analysiert Inhaltsdateien und erstellt daraus (statische) HTML-Dateien. Die Inhaltsdateien können Markdown oder andere Formate enthalten; ich verwende nur Markdown.

Meine Verzeichnisstruktur sieht folgendermaßen aus:

```text
.
|-- assets
|   |-- favicon.gif
|   |-- robots.txt
|   |-- img
|   |   |-- logo.png
|   |-- js
|   |   |-- custom.js
|   |-- css
|       |-- style.css
|
|-- content
|   |-- about.html
|   |-- 2013
|       |-- 01
|       |   |-- hello-world.html
|       |-- 02
|           |-- weekly-links-1.ad
|           |-- weekly-links-2.md
|
|-- templates
|   |-- index.ftl
|   |-- page.ftl
|   |-- post.ftl
|   |-- feed.ftl
|
|-- jbake.properties
```

Standardmäßig erzeugt JBake das Ausgabeverzeichnis in diesem Baum. In meinem Fall backe ich meine Sachen in ein Verzeichnis, das mit Git synchronisiert wird.

## Die GitHub-Einrichtung

## Die DNS-Einstellungen

# Als Nächstes

Es gibt ein paar Dinge, die ich ändern möchte.