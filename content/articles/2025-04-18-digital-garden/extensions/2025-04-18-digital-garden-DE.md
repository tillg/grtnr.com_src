---
date: 2025-04-18
image: digital-garden.jpg
excerpt: "Ich las über digitale Gärten und mochte die Idee. Also begann ich darüber nachzudenken, wie ich einen solchen Garten einrichten würde - und nutzte natürlich KI-Hilfe..."
translation: de
source_language: en
source_hash: 27d94eba5245e1f0cbf5e91be3c4d19f0bccb6093a661585a7699f97a5e4e2e8
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T21:53:49.579983
generated_by: simplified-translation-system
---

![Digitaler Garten](digital-garden.jpg)

[TOC]

Ich las über Digitale Gärten auf [heise (auf Deutsch)](https://www.heise.de/hintergrund/Nerd-Trend-Digitaler-Garten-Die-eigene-Website-als-persoenliches-Wissensarchiv-10344169.html) und fand die Idee wirklich gut. Die wesentlichen Unterschiede zu meinem aktuellen Blog, die mir einfielen, sind:

- Die Idee, Ideen sofort aufzuschreiben und Artikel direkt zu beginnen - und sie sofort im Garten zu haben. Das ist ein großer Unterschied zur Einstellung: "Ich muss den Artikel fertigstellen, bevor ich ihn veröffentliche."
- Die Idee, auf andere Artikel zu verlinken und ein Netzwerk von Artikeln zu schaffen. Das ist etwas, das ich bereits in meinem Blog tun kann, aber der Prozess ist heikel: Wenn ich einen Artikel umbenenne oder verschiebe, sind die Links darauf kaputt. Auch die Idee von Backlinks ist bemerkenswert.
- Die Themen mehr in den Vordergrund zu stellen als das Datum: Mein Blog ist hauptsächlich nach Datum strukturiert und präsentiert. Die Themen mehr als Navigationsstruktur zu verwenden, erscheint verlockend. Natürlich würde ich das Erstellungsdatum sowie das Datum der letzten Änderung beibehalten.

# Anforderungen

Wie üblich neige ich dazu, mit der technischen Seite zu beginnen 😀. Also habe ich meine Anforderungen notiert und ChatGPT um Hilfe gebeten.

Meine Anforderungen an ein digitales Gartensystem:

- Artikel basieren auf Markdown-Dateien.
- Als statisch generierte Website aufgebaut.
- Ein Artikel in einem Verzeichnis zusammen mit seinen Ressourcen: Bilder, PDFs, andere Dateien. Auf diese Weise macht das lokale Rendering pro Artikel Sinn, sehr hilfreich beim Bearbeiten. Ich würde die Artikel mit VScode oder einem anderen Editor bearbeiten, der Markdown unterstützt.
- Artikel (d.h. ihre Verzeichnisse) können in einer Verzeichnisbaumstruktur sein. Ihre Verzeichnisstruktur beschreibt die Kategorie. Zum Beispiel /tech/dev/data_science
- In Python geschrieben, damit ich herumtüfteln kann.
- Der Build-Prozess kann abgeschlossen werden: eine Phase zur Überprüfung interner Links.
- Interne Links als _[ [links] ]_. Und Backlinks in verlinkten Artikeln anzeigen.
- Ich möchte leicht spezifische Artikeltypen mit spezieller Struktur, Feldern, Rendering erstellen. Beispiele sind REZEPT, ORT oder LOCATION, REISEABENTEUER, …
- Schöne Seite! Nicht wie ein unordentlicher Nerd-Garten! Lassen Sie sich von schönen Blogs wie Ghost inspirieren.
- Mehrsprachig, mit Sprachen, die von KI ausgefüllt werden, wenn sie nicht vom Autor bereitgestellt werden.
- Unterschiedliche Zugriffsrechte: Einige Inhalte sind öffentlich, andere für Familie & Freunde oder andere Benutzergruppen.
- Zugriffsrollen, zum Beispiel: Artikel, die unveröffentlicht sind, können nur von Benutzern mit der Rolle EDITOR gesehen werden.
- Erlauben Sie mehrere Indexseiten: Tags, historischer Index (vielleicht auch pro Tag), am meisten gelesen, am meisten bewertet… Indexseiten können generiert, aber auch handgefertigt werden. Insbesondere die Startseite.

# Technologie und Architektur

[Dies ist, was ChatGPT produziert hat](https://chatgpt.com/share/68026bb5-d040-8009-9f79-ec0fd35880f4) (Ich finde es wirklich gut, also füge ich es hier vollständig ein):

Großartig. Ich werde die besten Python-basierten statischen Site-Generatoren und Architekturen erkunden, um einen schön gestalteten, markdown-gesteuerten digitalen Garten mit Unterstützung für Zugriffskontrolle, interne Linküberprüfung, mehrsprachige Unterstützung und Artikeltyp-Anpassung zu erstellen. Ich werde auch sicherstellen, dass das System Ihren bevorzugten lokalen Bearbeitungsfluss unterstützt, einfaches HTML generiert und gut mit GitHub Pages funktioniert.

Ich melde mich mit einem empfohlenen Stack, einem Architekturdiagramm und Vorschlägen zurück, wie Sie Ihre Anforderungen reibungslos umsetzen können.

_Recherchiert für 11m 16s \* 23 Quellen_

# ChatGPT: Aufbau eines Python-basierten digitalen Gartens: Stack & Architektur

## Statischer Site-Generator & Inhaltsorganisation

Für einen **Python-basierten statischen Site-Generator** ist **Pelican** eine ausgezeichnete Wahl. Pelican wird aktiv gepflegt und ist gut dokumentiert, unterstützt Markdown-Inhalte und mehrsprachige Veröffentlichungen von Haus aus ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). Es generiert eine einfache HTML-Site (kein Bedarf für React/Vue) und hat ein reichhaltiges Plugin-Ökosystem zur Erweiterung der Funktionalität ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)).

**Inhaltsstruktur:** Organisieren Sie den Inhalt des digitalen Gartens in einer logischen Verzeichnishierarchie unter Pelicans `content/`-Ordner. Jeder Artikel lebt in seinem eigenen Unterverzeichnis zusammen mit seinen Assets. Zum Beispiel:

```text
content/
├── tech/
│   └── dev/
│        └── data_science/
│             └── mein-artikel/
│                  ├── index.md        # Artikel in Markdown
│                  ├── abbildung1.png  # Bilder/PDFs im Zusammenhang mit dem Artikel
│                  └── daten.pdf
└── reisen/
    └── reise-nach-paris/
         ├── index.md
         └── eiffelturm.jpg
```

In diesem Layout wird jeder Artikel (`index.md`) mit seinen Medien gruppiert. Pelican kann „Seitenbündel“ wie dieses behandeln, indem es diese Unterordner sowohl als Inhalt als auch als statische Pfade behandelt. Wir konfigurieren die Pelican-Einstellungen so, dass jedes Verzeichnis in `ARTICLE_PATHS` und `STATIC_PATHS` enthalten ist, sodass Markdown-Dateien verarbeitet und Assets in die Ausgabe kopiert werden ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,directory%20reserved%20for%20static%20files)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=generated%20site,in%20earlier%20versions%20of%20Pelican)). Pelicans **attach-Syntax** ermöglicht es, lokale Dateien einfach zu verlinken: In Markdown verwenden Sie `{attach}`, um Dateien im selben Ordner zu referenzieren. Zum Beispiel: `![Abbildung]({attach}abbildung1.png)` in `mein-artikel/index.md` kopiert _abbildung1.png_ in das Ausgabeverzeichnis des Artikels und verlinkt darauf ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,sibling%20of%20the%20linking%20document)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Title%3A%20Test%20Post%20Category%3A%20test,31)). Dies hält Bilder/PDFs zusammen mit ihrem Artikel und stellt sicher, dass Links nach dem statischen Build nicht gebrochen sind ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=output%20%E2%94%94%E2%94%80%E2%94%80%202014%20%E2%94%9C%E2%94%80%E2%94%80%20archive,post.html)).

Pelican unterstützt auch die automatische Verwendung von Ordnernamen als Kategorien. Standardmäßig wird der unmittelbare übergeordnete Ordner zur Kategorie (z.B. „data_science“ im obigen Pfad) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)). Wir können tiefere Verschachtelungen in URLs beibehalten, indem wir den Speicherpfad anpassen. Beispielsweise wird durch Festlegen von `ARTICLE_SAVE_AS = '{category}/{slug}/index.html'` und ähnlichem `ARTICLE_URL` jeder Beitrag als `index.html` in einem Ordner gespeichert, der seiner Kategorie/Slug entspricht. Dies ergibt saubere URLs wie `/tech/dev/data_science/mein-artikel/`, die der Verzeichnisstruktur entsprechen. (Pelicans `USE_FOLDER_AS_CATEGORY=True` verwendet standardmäßig den niedrigsten Ordner als Kategorie; für eine mehrstufige Taxonomie kann man entweder den Pfad zu einer Kategorie kombinieren oder die obersten Ordner als Abschnitte behandeln und Tags für die Unterklassifizierung verwenden.)

## Markdown-Bearbeitung & Lokale Vorschau

Alle Artikel werden in einfachem **Markdown** geschrieben (mit YAML/TOML-Frontmatter für Metadaten), sodass Sie Inhalte bequem in VS Code oder einem beliebigen Editor erstellen können. Jede Markdown-Datei beginnt mit Metadaten wie Titel, Datum, Tags usw. Pelican benötigt nur einen Titel (es kann andere ableiten, wenn nötig) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)), aber wir werden Metadaten umfassend für benutzerdefiniertes Verhalten verwenden (mehr dazu später). Ein Beispiel für eine Frontmatter eines Artikels könnte sein:

```markdown
Title: Meine Reise in die Datenwissenschaft  
Date: 2025-04-10  
Category: data_science  
Tags: python, analytics  
Slug: meine-reise-in-die-datenwissenschaft  
Status: published
```

**Lokale Vorschau:** Um eine Vorschau pro Artikel während der Bearbeitung zu ermöglichen, verwenden Sie Pelicans integrierten Entwicklungsserver. Pelicans CLI/Makefile unterstützt einen Auto-Reload-Server (z.B. `make devserver` oder `pelican --autoreload --listen`), der auf Dateiänderungen wartet und beim Schreiben neu aufbaut. Auf diese Weise können Sie zu `http://localhost:8000/tech/dev/data_science/mein-artikel/` navigieren und das gerenderte HTML bei jedem Speichern aktualisieren sehen. Da Pelican selektives Ausgabeschreiben und Caching durchführt, sind Neubauten auch für große Sites schnell ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). Dies gibt eine nahezu Echtzeit-Vorschau des Artikels im Kontext des tatsächlichen Themas/Templates. Für schnelle Iterationen auf einer einzelnen Seite wird Pelicans inkrementeller Build nur _mein-artikel_ erkennen, dass sich geändert hat, und nur diese Seite neu generieren, was den Feedback-Zyklus schnell macht. VS Code kann auch Markdown-Vorschauen anzeigen, aber die Verwendung von Pelicans Server stellt sicher, dass der Inhalt mit dem endgültigen Styling und Layout der Site gesehen wird.

## Wiki-Stil Interne Verlinkung & Backlinks

Um Notizen im Wiki-Stil zu verknüpfen, aktivieren wir **[[Wiki-Stil]] Verlinkung** in Markdown. Pelican hat ein Community-Plugin namens **Wikilinks**, das automatisch `[[Seitenname]]`-Syntax in richtige Hyperlinks zwischen Seiten umwandelt ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). Zum Beispiel wird das Schreiben von `Wir bauen auf Ideen aus [[Meine Reise in die Datenwissenschaft]]` in einem anderen Artikel auf die Seite „Meine Reise in die Datenwissenschaft“ verlinken (auflösend zu seinem Slug oder Dateinamen). Das Wikilinks-Plugin unterstützt optionalen Anzeigetext (z.B. `[[Seitenname|benutzerdefinierter Text]]`) ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). Im Hintergrund scannt es nach `[[...]]`-Mustern nach der Markdown-Verarbeitung und ersetzt sie durch `<a>`-Links zur URL der Zielseite ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=In%20basic%20usage%2C%20this%20allow,is%20finished)). Dies macht das Querverweisen von Inhalten so einfach wie in Tools wie Obsidian oder Roam. (Wir werden eindeutige Dateinamen für Notizen erzwingen, um mehrdeutige Links zu vermeiden ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Known%20Issues)).)

**Backlinks:** Um bidirektionale Verlinkung (zu sehen, was auf eine Seite zurückverlinkt) zu erreichen, können wir ein benutzerdefiniertes Pelican-Plugin erstellen oder die Metadaten der Site nutzen. Während des Builds können wir alle Wiki-Link-Referenzen sammeln: z.B. ein Wörterbuch pflegen, das jede Zielseite einer Liste von Seiten zuordnet, die sie erwähnt haben. Dann erweitern wir Pelicans Artikelkontext, um eine „Backlinks“-Liste für jeden Artikel einzuschließen. Schließlich, im Artikel-Template, wenn Backlinks existieren, einen Abschnitt „**Verlinkt von:** …“ rendern, der diese referenzierenden Seiten auflistet. Dies erfordert ein benutzerdefiniertes Plugin, das sich in Pelicans Generierungsphase einhakt (mithilfe von Signalen wie `article_generator_finalized`), um Links zu sammeln und die Daten einzufügen. Der Aufwand ist überschaubar angesichts von Pelicans Plugin-API (Python-Hooks) und stellt sicher, dass jede Seite mit einer Liste anderer Notizen endet, die darauf verlinken, was die Wiki-ähnliche Navigation verstärkt. Wenn Sie ein Plugin von Grund auf neu schreiben, würden wir das HTML jedes Artikels parsen (oder die interne Linkkarte vom Wikilinks-Plugin verwenden), um ausgehende `href`s zu identifizieren, die innerhalb der Site zeigen, und dann diese Zuordnung umkehren.

Pelicans Standard-Verlinkungssyntax (`{filename}ziel.md`) könnte auch für interne Links verwendet werden ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=the%20other%20content%20will%20be,placed%20after%20site%20generation)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=,filename%7D%2Farticle2.md)), aber der Wiki-Stil ist intuitiver für einen digitalen Garten-Workflow. Mit dem Wikilinks-Plugin und einem Backlinks-Plugin wird die Site **vollständig vernetzte Seiten** mit automatischen Referenzen haben.

## Benutzerdefinierte Inhaltstypen & Templates

Eine Stärke von Pelican ist seine flexible Metadaten- und Template-Verwendung, die wir nutzen, um **benutzerdefinierte Artikeltypen** wie `REZEPT` oder `REISE` zu definieren. Alle Markdown-Dateien können beliebige Frontmatter-Felder enthalten (solange sie nicht mit reservierten Schlüsselwörtern kollidieren) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=This%20is%20the%20content%20of,my%20super%20blog%20post)) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=,false)). Wir definieren ein Metadatenfeld `Type` (oder verwenden ein Tag/Kategorie), um den Inhaltstyp zu kennzeichnen, und fügen alle benötigten benutzerdefinierten Felder hinzu. Zum Beispiel könnte ein Rezept haben:

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
   Template: rezept <!-- Verwenden Sie ein benutzerdefiniertes Jinja-Template -->
```

In diesem Fall setzen wir `Template: rezept`, was Pelican anweist, diese Seite mit `rezept.html` anstelle des Standard-Templates zu rendern ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=match%20at%20L131%20,to%20use%20for%20this%20article%2Fpage)). Wir werden separate Jinja2-Templates erstellen (z.B. `rezept.html`, `reise.html`) im Thema. Diese Templates erweitern das Basislayout, präsentieren den Inhalt jedoch auf eine spezialisierte Weise. Zum Beispiel kann **`rezept.html`** die Zutatenliste als Check