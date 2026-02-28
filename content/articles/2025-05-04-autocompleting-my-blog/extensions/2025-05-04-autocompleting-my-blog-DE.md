---
date: 2025-05-04
image: hero.svg
excerpt: Ich habe jetzt einen auf Pelican basierenden Blog und möchte Inhalte automatisch hinzufügen oder korrigieren: Bild-Tags, Artikelzusammenfassungen, Übersetzungen... Endlich eine Möglichkeit, KI zu nutzen
title: Autovervollständigung meines Blogs
tags: blog, tech, softwareweneed
translation: de
source_language: en
source_hash: 2c49a690dcd66ccbd5e686a22673cc07dd65e13e84c82147db6c49b55b7897ed
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:40:41.747529+00:00
generated_by: simplified-translation-system
---

[TOC]

Seit letzter Woche basiert mein Blog auf [Pelican](https://getpelican.com), dem Python-basierten statischen Blog-Generator. Jetzt, da der Blog in einer Sprache erstellt wird, die ich mehr oder weniger beherrsche, kann ich darüber nachdenken, den Prozess des Schreibens und Erstellens selbst zu verbessern. Und natürlich gibt es viele Tools, die mir einfallen, um mein Leben sowie das meiner Leser einfacher zu machen. Hier sind einige Beispiele für diese Helfer.

## Tools, die ich gerne hätte

### Bild-Tag-Vervollständigung (KI)

Immer wenn ich ein Bild ohne Alt-Text hinzufüge, ist das schlecht für blinde Menschen. Aber ich bin faul, also warum nicht eine KI das Bild beschreiben lassen und es als ALT-Text hinzufügen?

### Link-Checker

Ich habe viele Links, die auf externe Seiten verweisen. Und manchmal verschwinden Webseiten, sodass meine Links ins Nirwana führen könnten. Es wäre schön, wenn

- meine Benutzer nicht auf kaputte Links klicken müssten
- ich einen Hinweis bekäme, dass ich den einen oder anderen Link reparieren muss
- ich vielleicht die Situation verhindern könnte, indem ich eine Kopie der Seite, auf die ich verlinke, in meinem eigenen Blog behalte. Oder ist das böses Scraping und Content-Diebstahl?

### Auszug-Generator (KI)

Ich schreibe oft Artikel, ohne die Zusammenfassung / den Auszug anzugeben, der in der Artikelliste angezeigt wird. Standardmäßig nimmt Pelican (und andere statische Generatoren) den ersten Absatz oder die ersten 30 Wörter und verwendet sie als Auszug.

Wäre es nicht viel schöner, ein LLM zu bitten, eine vernünftige 3-zeilige Zusammenfassung zu erstellen?

### Übersetzer (KI-mäßig)

In meinem Blog schreibe ich manchmal englische, manchmal deutsche Artikel. Vielleicht gibt es hier und da sogar einen französischen Artikel. Wäre es nicht schön, jeden Artikel in jeder Sprache zu haben? Es fühlt sich an, als ob das heutzutage Standard sein sollte, angesichts der guten Qualität der heutigen Übersetzungstools.

Also schreibe ich meine Artikel in welcher Sprache auch immer, die gerade aus meinem kleinen Gehirn kommt, und das System sollte die fehlenden Sprachen generieren.

### Artikel-Illustration (KI)

Ich versuche, für die meisten meiner Artikel Bilder zu haben, da es einfach ein angenehmeres Leseerlebnis ist und angenehm fürs Auge. Ich finde oft etwas im Internet, aber nicht immer – auch weil ich manchmal nicht einmal die Mühe mache, ein Bild zu suchen. Aber die KI könnte suchen oder sogar ein schönes Bild für meine _nackten_ Artikel generieren.

## Wir brauchen eine Build-Pipeline

Um diese Dinge zu erstellen, brauche ich etwas wie eine _Build-Pipeline_:

![Build Pipeline](https://insights.mgm-tp.com/wp-content/uploads/2023/08/mgm-CI-CD-Pipeline.png)
_Eine moderne CI/CD-Build-Pipeline, entnommen von [mgm technology partners](https://mgm-tp.com)_

Einige Gedanken zur Struktur, Verarbeitung und wie man Daten organisiert.

### Zwischen-Daten

Was Pelican macht, ist, die Quelle der Artikel zusammen mit der Konfiguration zu nehmen und die Webseiten zu generieren. Dies geschieht durch die Standardverarbeitung und durch potenzielle Plugins. Plugins können von Drittanbietern oder selbst entwickelt sein. In meinem Fall habe ich beides.

Viele der Tools, die ich mir vorstelle, erstellen zusätzliche Daten, und oft ist die Erstellung teuer und zeitaufwendig. Denke an das Erstellen eines Auszugs eines Artikels: Der gesamte Text muss an eine KI gesendet und verarbeitet werden. Dies dauert mehrere Sekunden und kostet echtes Geld. Daher ist es sicherlich nichts, was wir bei jedem Build ausführen möchten. Also müssen wir die Daten zwischen den verschiedenen Build-Läufen behalten.

### Integrität der erstellten Inhalte

Eine Möglichkeit, dies zu lösen, wäre, den von der KI generierten Auszug einfach dem ursprünglichen Markdown hinzuzufügen (in diesem Fall würde er im Front Matter als `summary`-Feld landen).

Aber das gefällt mir überhaupt nicht: Ich möchte nicht, dass die KI in den Text und Inhalt eingreift, den ich persönlich erstellt habe. Daher möchte ich die folgende Regel für mein System definieren:

**Meine erstellten Markdown-Dateien sollten niemals von automatisierten Tools verändert werden.**

### Wo Daten aufbewahren

Das lässt mich mit der Frage, wo ich die Daten wie von der KI generierte Zusammenfassungen aufbewahren soll. Der natürliche Ort ist, sie neben den Markdown-Dateien zu behalten, aber in einer eigenen Datei. Da ich für jeden meiner Artikel separate Verzeichnisse habe, endet es mit dieser Verzeichnis- und Dateistruktur:

```file
content
    articles
    ...
    2025-04-18-digital-garden
        2025-04-18-ditigal-garden.md
        2025-04-18-digital-garden.picture-tags.json
        2025-04-18-digital-garden.summary.json
        digital-garden.jpg
```

Einige Gedanken und Argumente für diese Struktur:

- Jedes Tool hat seine eigene Datei, um die Dinge getrennt zu halten.
- Ich verwende JSON-Dateien: Einfach zu verarbeiten und einfach zu lesen.
- Die Dateien befinden sich neben dem Originalartikel, sodass alles, was zusammengehört, nah beieinander und _gekapselt_ ist.
- Die JSON-Dateien werden auch versioniert und in Git gespeichert, sodass, egal ob ich den Build-Prozess auf meiner lokalen Entwicklungsmaschine oder innerhalb von Github Actions oder einem anderen CI/CD-Prozessor ausführe, die zuvor generierten Daten wiederverwendet werden.

### Verarbeitungsreihenfolge

Dieses Datenlayout erfordert einen mehrstufigen Build-Prozess:

1. **Zusätzliche Daten erstellen:** Erstelle die Zusammenfassungen, die Bildbeschreibungen, die Bilder, überprüfe die Links (und speichere das Ergebnis dieser Überprüfungen)... Dieser Prozess ist potenziell zeitaufwendig, generiert viele zusätzliche Daten und erfordert intelligente Caching- und Cache-Validierungsmechanismen. Z.B. "Wie überprüfe ich, ob ich die Zusammenfassung eines Artikels neu erstellen muss oder ob ich die im JSON-Datei neben dem Markdown-Artikel verwenden kann?".
2. **Die Seite bauen:** Dies ist der grundlegende Pelican-Erstellungsprozess, wie wir ihn kennen, außer dass er auch die zusätzlichen Daten integrieren muss, die jetzt in den JSON-Dateien vorhanden sind. Ich werde dies mit einem oder mehreren Pelican-Plugins tun, die ich entwickeln werde.