---
date: 2025-04-18
image: digital-garden.jpg
excerpt: "Ich habe über digitale Gärten gelesen und mochte die Idee. Also begann ich darüber nachzudenken, wie ich einen solchen Garten einrichten würde - und habe natürlich KI-Unterstützung genutzt..."
translation: de
source_language: en
translator: gpt-4o
translate_date: 2025-07-09T14:55:32.710551
source_file: /Users/tgartner/git/grtnr.com_src/content/articles/2025-04-18-digital-garden/2025-04-18-digital-garden.md
generated_by: automatic-translation-plugin
---

![Digitaler Garten](digital-garden.jpg)

[TOC]

Ich habe über Digitale Gärten auf [heise (auf Deutsch)](https://www.heise.de/hintergrund/Nerd-Trend-Digitaler-Garten-Die-eigene-Website-als-persoenliches-Wissensarchiv-10344169.html) gelesen und fand die Idee wirklich gut. Die wichtigsten Unterschiede zu meinem aktuellen Blog, die mir eingefallen sind, sind:

- Die Idee, Ideen sofort aufzuschreiben und Artikel direkt zu beginnen - und sie sofort im Garten zu haben. Das ist ein großer Unterschied zur Einstellung "Ich muss den Artikel fertigstellen, bevor ich ihn veröffentliche".
- Die Idee, auf andere Artikel zu verlinken und ein Netzwerk von Artikeln zu schaffen. Das ist etwas, was ich bereits in meinem Blog tun kann, aber der Prozess ist heikel: Wenn ich einen Artikel umbenenne oder verschiebe, sind die Links darauf gebrochen. Auch die Idee von Backlinks ist beeindruckend.
- Die Themen mehr in den Vordergrund zu stellen als das Datum: Mein Blog ist hauptsächlich nach Datum strukturiert und präsentiert. Die Themen mehr als Navigationsstruktur zu verwenden, erscheint verlockend. Natürlich würde ich das Erstellungsdatum sowie das Datum der letzten Änderung beibehalten.

# Anforderungen

Wie üblich neige ich dazu, mit der technischen Seite zu beginnen 😀. Also habe ich meine Anforderungen notiert und ChatGPT um Hilfe gebeten.

Meine Anforderungen an ein digitales Gartensystem:

- Artikel basieren auf Markdown-Dateien.
- Erbaut als statisch generierte Website.
- Ein Artikel in einem Verzeichnis zusammen mit seinen Ressourcen: Bilder, PDFs, andere Dateien. Auf diese Weise macht das lokale Rendering pro Artikel Sinn, sehr hilfreich beim Bearbeiten. Ich würde die Artikel mit VScode oder einem anderen Editor bearbeiten, der Markdown unterstützt.
- Artikel (d.h. ihre Verzeichnisse) können in einer Verzeichnisbaumstruktur sein. Ihre Verzeichnisstruktur beschreibt die Kategorie. Zum Beispiel/tech/dev/data_science
- In Python geschrieben, damit ich herumtüfteln kann.
- Build-Pipeline kann abgeschlossen werden: eine Phase zur Überprüfung interner Links.
- Interne Links als _[ [Links] ]_. Und Backlinks in verlinkten Artikeln anzeigen.
- Ich möchte leicht spezifische Artikeltypen mit spezieller Struktur, Feldern, Rendering erstellen. Beispiele sind REZEPT, ORT oder LOCATION, REISEABENTEUER, …
- Schöne Seite! Nicht wie ein unordentlicher nerdiger Garten! Lassen Sie sich von schönen Blogs wie Ghost inspirieren.
- Mehrsprachig, mit Sprachen, die von KI ausgefüllt werden, wenn sie nicht vom Autor bereitgestellt werden.
- Unterschiedliche Zugriffsrechte: Einige Inhalte sind öffentlich, andere für Familie & Freunde oder andere Benutzergruppen.
- Zugriffsrollen, zum Beispiel: Artikel, die unveröffentlicht sind, können nur von Benutzern mit der Rolle EDITOR gesehen werden.
- Erlauben Sie mehrere Indexseiten: Tags, historischer Index (vielleicht auch pro Tag), am meisten gelesen, am meisten bewertet… Indexseiten können generiert, aber auch handgefertigt werden. Insbesondere die Startseite.

# Technologie und Architektur

[Das ist, was ChatGPT produziert hat](https://chatgpt.com/share/68026bb5-d040-8009-9f79-ec0fd35880f4) (Ich finde es wirklich gut, also füge ich alles hier ein):

Großartig. Ich werde die besten Python-basierten statischen Site-Generatoren und Architekturen erkunden, um einen schön gestalteten, markdown-gesteuerten digitalen Garten mit Unterstützung für Zugriffskontrolle, interne Linküberprüfung, mehrsprachige Unterstützung und Artikeltyp-Anpassung zu erstellen. Ich werde auch sicherstellen, dass das System Ihren bevorzugten lokalen Bearbeitungsfluss unterstützt, einfaches HTML generiert und gut mit GitHub Pages funktioniert.

Ich melde mich mit einem empfohlenen Stack, einem Architekturdiagramm und Vorschlägen zurück, wie Sie Ihre Anforderungen reibungslos umsetzen können.

_Recherchiert für 11m 16s \* 23 Quellen_

# ChatGPT: Aufbau eines Python-gestützten digitalen Gartens: Stack & Architektur

## Statischer Site-Generator & Inhaltsorganisation

Für einen **Python-basierten statischen Site-Generator** ist **Pelican** eine ausgezeichnete Wahl. Pelican wird aktiv gepflegt und ist gut dokumentiert, unterstützt Markdown-Inhalte und mehrsprachige Veröffentlichungen direkt ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). Es generiert eine einfache HTML-Site (kein Bedarf für React/Vue) und hat ein reichhaltiges Plugin-Ökosystem zur Erweiterung der Funktionalität ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)).

**Inhaltsstruktur:** Organisieren Sie den Inhalt des digitalen Gartens in einer logischen Verzeichnishierarchie im `content/`-Ordner von Pelican. Jeder Artikel lebt in seinem eigenen Unterverzeichnis zusammen mit seinen Ressourcen. Zum Beispiel:

```text
content/
├── tech/
│   └── dev/
│        └── data_science/
│             └── mein-artikel/
│                  ├── index.md        # Artikel in Markdown
│                  ├── abbildung1.png  # Bilder/PDFs zum Artikel
│                  └── daten.pdf
└── reisen/
    └── reise-nach-paris/
         ├── index.md
         └── eiffelturm.jpg
```

In diesem Layout wird jeder Artikel (`index.md`) mit seinen Medien gruppiert. Pelican kann solche „Seitenbündel“ behandeln, indem es diese Unterordner sowohl als Inhalt als auch als statische Pfade behandelt. Wir konfigurieren die Pelican-Einstellungen so, dass jeder Ordner in `ARTICLE_PATHS` und `STATIC_PATHS` enthalten ist, sodass Markdown-Dateien verarbeitet und Ressourcen in die Ausgabe kopiert werden ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,directory%20reserved%20for%20static%20files)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=generated%20site,in%20earlier%20versions%20of%20Pelican)). Pelicans **attach syntax** ermöglicht das einfache Verlinken zu lokalen Dateien: In Markdown verwenden Sie `{attach}`, um auf Dateien im selben Ordner zu verweisen. Zum Beispiel: `![Abbildung]({attach}abbildung1.png)` in `mein-artikel/index.md` kopiert _abbildung1.png_ in das Ausgabeverzeichnis des Artikels und verlinkt darauf ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,sibling%20of%20the%20linking%20document)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Title%3A%20Test%20Post%20Category%3A%20test,31)). Dies hält Bilder/PDFs zusammen mit ihrem Artikel und stellt sicher, dass Links nach dem statischen Build nicht gebrochen sind ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=output%20%E2%94%94%E2%94%80%E2%94%80%202014%20%E2%94%9C%E2%94%80%E2%94%80%20archive,post.html)).

Pelican unterstützt auch die automatische Verwendung von Ordnernamen als Kategorien. Standardmäßig wird der unmittelbare übergeordnete Ordner zur Kategorie (z.B. „data_science“ im obigen Pfad) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)). Wir können tiefere Verschachtelungen in URLs bewahren, indem wir den Speicherpfad anpassen. Zum Beispiel, indem wir `ARTICLE_SAVE_AS = '{category}/{slug}/index.html'` und ähnliche `ARTICLE_URL` festlegen, wird jeder Beitrag als `index.html` in einem Ordner gespeichert, der seiner Kategorie/Slug entspricht. Dies ergibt saubere URLs wie `/tech/dev/data_science/mein-artikel/`, die die Verzeichnisstruktur widerspiegeln. (Pelicans `USE_FOLDER_AS_CATEGORY=True` verwendet standardmäßig den untersten Ordner als Kategorie; für eine mehrstufige Taxonomie kann man entweder den Pfad zu einer Kategorie kombinieren oder die obersten Ordner als Abschnitte behandeln und Tags für die Unterklassifizierung verwenden.)

## Markdown-Bearbeitung & Lokale Vorschau

Alle Artikel werden in einfachem **Markdown** geschrieben (mit YAML/TOML-Frontmatter für Metadaten), sodass Sie Inhalte bequem in VS Code oder einem beliebigen Editor verfassen können. Jede Markdown-Datei beginnt mit Metadaten wie Titel, Datum, Tags usw. Pelican erfordert nur einen Titel (es kann andere ableiten, wenn nötig) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)), aber wir werden Metadaten umfassend für benutzerdefiniertes Verhalten verwenden (mehr dazu später). Ein Beispiel für ein Frontmatter für einen Artikel könnte sein:

```markdown
Title: Meine Reise in die Datenwissenschaft  
Date: 2025-04-10  
Category: data_science  
Tags: python, analytics  
Slug: meine-reise-in-die-datenwissenschaft  
Status: published
```

**Lokale Vorschau:** Um eine Vorschau pro Artikel während der Bearbeitung zu ermöglichen, verwenden Sie Pelicans integrierten Entwicklungsserver. Pelicans CLI/Makefile unterstützt einen Auto-Reload-Server (z.B. `make devserver` oder `pelican --autoreload --listen`), der auf Dateiänderungen achtet und beim Schreiben neu baut. Auf diese Weise können Sie zu `http://localhost:8000/tech/dev/data_science/mein-artikel/` navigieren und sehen, wie sich das gerenderte HTML bei jedem Speichern aktualisiert. Da Pelican selektives Output-Schreiben und Caching durchführt, sind Neubauten auch für große Sites schnell ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). Dies gibt eine nahezu Echtzeit-Vorschau des Artikels im Kontext des tatsächlichen Themas/Templates. VS Code kann auch Markdown anzeigen, aber die Verwendung von Pelicans Server stellt sicher, dass der Inhalt mit dem endgültigen Styling und Layout der Site gesehen wird.

## Wiki-Style Interne Verlinkung & Backlinks

Um Notizen im Wiki-Stil zu verknüpfen, aktivieren wir **[[Wiki-Style]] Verlinkung** in Markdown. Pelican hat ein Community-Plugin namens **Wikilinks**, das `[[Seitenname]]`-Syntax automatisch in richtige Hyperlinks zwischen Seiten umwandelt ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). Zum Beispiel wird das Schreiben von `Wir bauen auf Ideen von [[Meine Reise in die Datenwissenschaft]]` in einem anderen Artikel auf die Seite „Meine Reise in die Datenwissenschaft“ verlinken (aufgelöst zu ihrem Slug oder Dateinamen). Das Wikilinks-Plugin unterstützt optionalen Anzeigetext (z.B. `[[Seitenname|benutzerdefinierter Text]]`) ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). Im Hintergrund scannt es nach `[[...]]`-Mustern nach der Markdown-Verarbeitung und ersetzt sie durch `<a>`-Links zur URL der Zielseite ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=In%20basic%20usage%2C%20this%20allow,is%20finished)). Dies macht das Querverweisen von Inhalten so einfach wie in Tools wie Obsidian oder Roam. (Wir werden eindeutige Dateinamen für Notizen durchsetzen, um mehrdeutige Links zu vermeiden ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Known%20Issues)).)

**Backlinks:** Um bidirektionales Verlinken (zu sehen, was auf eine Seite zurückverlinkt) zu erreichen, können wir ein benutzerdefiniertes Pelican-Plugin erstellen oder die Metadaten der Site nutzen. Während des Builds können wir alle Wiki-Link-Referenzen sammeln: z.B. ein Wörterbuch pflegen, das jede Zielseite einer Liste von Seiten zuordnet, die sie erwähnt haben. Dann erweitern wir den Artikelkontext von Pelican, um eine „Backlinks“-Liste für jeden Artikel einzuschließen. Schließlich, im Artikeltemplate, wenn Backlinks vorhanden sind, einen Abschnitt „**Verlinkt von:** …“ rendern, der diese verweisenden Seiten auflistet. Dies erfordert ein benutzerdefiniertes Plugin, das sich in die Generierungsphase von Pelican einhakt (unter Verwendung von Signalen wie `article_generator_finalized`), um Links zu sammeln und die Daten einzufügen. Der Aufwand ist überschaubar, angesichts der Plugin-API von Pelican (Python-Hooks), und stellt sicher, dass jede Seite mit einer Liste anderer Notizen endet, die darauf verlinken, was die wiki-ähnliche Navigation verstärkt. Wenn wir ein Plugin von Grund auf neu schreiben, würden wir das HTML jedes Artikels parsen (oder die interne Linkkarte des Wikilinks-Plugins verwenden), um ausgehende `href`s zu identifizieren, die innerhalb der Site zeigen, und dann diese Zuordnung umkehren.

Pelicans Standard-Verlinkungssyntax (`{filename}ziel.md`) könnte auch für interne Links verwendet werden ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=the%20other%20content%20will%20be,placed%20after%20site%20generation)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=,filename%7D%2Farticle2.md)), aber der Wiki-Stil ist für einen digitalen Garten-Workflow intuitiver. Mit dem Wikilinks-Plugin und einem Backlinks-Plugin wird die Site **vollständig vernetzte Seiten** mit automatischen Referenzen haben.

## Benutzerdefinierte Inhaltstypen & Templates

Eine Stärke von Pelican ist seine flexible Metadaten- und Templating-Funktion, die wir nutzen, um **benutzerdefinierte Artikeltypen** wie `REZEPT` oder `REISE` zu definieren. Alle Markdown-Dateien können beliebige Frontmatter-Felder enthalten (solange sie nicht mit reservierten Schlüsselwörtern kollidieren) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=This%20is%20the%20content%20of,my%20super%20blog%20post)) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=,false)). Wir definieren ein Metadatenfeld `Type` (oder verwenden ein Tag/Kategorie), um den Inhaltstyp zu kennzeichnen, und fügen alle erforderlichen benutzerdefinierten Felder hinzu. Zum Beispiel könnte ein Rezept haben:

```markdown
Title: Schokoladenkekse  
Date: 2025-03-01  
Type: rezept  
Portionen: 4  
Vorbereitungszeit: 15 min  
Backzeit: 10 min  
Zutaten:

- Mehl
- Zucker
- Schokoladenstückchen
  Schritte:

1. Ofen vorheizen…
2. Zutaten mischen…  
   Template: rezept <!-- benutze ein benutzerdefiniertes Jinja-Template -->