---
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T17:02:45.924925
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2015-12-27-siteweightwatcher-keeps-your-website-slim/2015-12-27-siteweightwatcher-keeps-your-website-slim.md
Generated-By: automatic-translation-plugin
---

```markdown
---
layout: post
title: SiteWeightWatcher - hält Ihre Website schlank
slug: siteweightwatcher-haelt-ihre-website-schlank
date_published: 2015-12-27T00:00:00.000Z
date_updated: 2021-12-06T14:38:49.000Z
tags: Tech
image: kickz_dashboard.png
---

Gute Softwareentwickler testen ihre Sachen. Und die [TDD (Test Driven Development)](https://www.wikiwand.com/en/Test-driven_development)-Süchtigen sind wahre Fanatiker, wenn es ums Testen geht. Diese Leute denken normalerweise in Code, sei es Java, Python, nodeJS, Sie nennen es. TDD bedeutet, dass Sie zuerst Tests schreiben, dann nur so viel Code, wie nötig ist, um die Tests grün werden zu lassen. Dann überarbeiten Sie Ihren Code und erst dann beginnen Sie, Tests für neue Anforderungen zu schreiben.
![TDD-Prozess](tdd.png)

Das ist **sehr** testlastig. Meiner Meinung nach wird man, wenn man es so macht, wie es in den Büchern geschrieben und beschrieben wird, schrecklich langsam und es wird unsinnig. Aber das ist eine andere Diskussion, die ich hier nicht klären möchte...

Was bei den meisten Testansätzen, die ich in der Vergangenheit gesehen habe, fehlt, sind die folgenden zwei Dinge:

1. Die Testleute und Testwerkzeuge hören auf, die Software oder Website zu überwachen, sobald sie in Produktion gegangen ist. Irgendwie haben sie das Gefühl, dass ihre Verantwortung mit dem Livegang endet...
2. Sie testen die Software. Nicht den Rest, d.h. das Design, das HTML, das CSS usw. Und die Benutzererfahrung, das Gefühl, ob das, was ich sehe, berühre, durchsuche, navigiere, von guter Qualität ist, wird stark von dieser Verpackung der Softwarelogik beeinflusst.

Ich suche also nach einem Tool, um (webbasierte) Software zu testen, sobald sie in freier Wildbahn ist und während der gesamten Benutzererfahrung. Stellen Sie sich eine Website vor, einen einfachen Blog. Sie könnte perfekt sein, als sie gestartet wurde, aber im Laufe der Zeit verschlechtert sie sich einfach: Die Designer haben so viele Schnickschnack hinzugefügt, das Volumen des Inhalts ist gewachsen, sie wurde optimiert, um auf Mobilgeräten besser nutzbar zu sein... Und schließlich ist die Seite aufgebläht, schwer und langsam. Warum muss ich warten, bis meine Benutzer es mir sagen (das wäre Beschweren)?

Bei [mgm technology partners](https://mgm-tp.com) haben wir automatisierte Testsuiten, die jede Nacht laufen. So haben Entwickler, die Code eingebaut haben, der die Software verlangsamt, jeden Morgen einen Bericht in ihrem Posteingang.

Hier ist also, was mein SiteWeightWatcher tun sollte:

- Tests alle 5-30 Minuten gegen die Produktionsseite durchführen
- Alle Seiten überprüfen, nicht nur index.html
- Sofort berichten, wenn Seiten langsamer werden (das wäre langsamer als sie es früher waren)
- Wichtige Kennzahlen verfolgen und wie sie sich im Laufe der Zeit entwickeln:
  - Wie viel Daten werden für jede Seite übertragen?
  - Wie viele Anfragen gehen hin und her?
  - Wie viel Zeit benötigt die Produktsuche? Im Laufe der Zeit...
  - Wie gut ist die Seite für Benutzer in Deutschland, UK, USA oder Asien verbunden? Im Laufe der Zeit, denn diese Dinge ändern sich, ohne dass wir etwas getan haben.

Ich könnte mir vorstellen, dass ein Dashboard für einen Online-Shop wie [KICKZ.com](https://www.kickz.com/de) so aussehen könnte:
![Dashboard-Skizze](kickz_dashboard.png)Ein Dashboard, das zeigt, wie sich die Seitengrößen entwickeln

Und genau wie die normalen Testteams sollten sich auch diese Tests weiterentwickeln und immer besser an die Seite, ihre Funktionalität und ihre Benutzer anpassen. Wann immer wir ein echtes Problem oder einen Fehler da draußen haben, müssen wir sicherstellen, dass unser WeightWatcher es findet, falls es erneut auftreten oder passieren sollte.

Wie könnten wir beginnen, ein solches Tool zu bauen? Einige Gedanken:

- Wir haben Agenten und einen zentralen Server. Die Agenten befinden sich weltweit oder in verschiedenen Netzwerken (denken Sie an kleine Docker-Images, die in verschiedenen Clouds laufen). Sie berichten alle erfassten Daten an den zentralen Server. Hier werden die Berichte erstellt und interaktive Erklärungen der Daten bereitgestellt.
- Die Agenten beginnen, einfache Metriken zu sammeln:
  - Anzahl der HTTP-Anfragen pro Seite
  - Übertragene Daten pro Seite
  - Anzahl der JavaScript-Zeilen pro Seite
  - Zeit zum Laden der Daten
  - Zeit zur Ausführung von JavaScript
- Basierend darauf beginnen wir mit einfachen Berichten:
  - Wie groß ist die durchschnittliche Seitengröße?
  - Wie viele Anfragen gibt es durchschnittlich pro Seite?
  - Was sind meine _schwersten_ Seiten?
  - Ein Diagramm, das die Verfügbarkeit meiner Seite sowie die Ladezeit über eine 24-Stunden-Skala, eine Woche, einen Monat zeigt. Vielleicht erleben meine Benutzer nur abends langsames Laden.

Von dort aus erweitern wir die gesammelten Daten sowie die Berichte.

Ein solches Tool wäre großartig, um Websites zu überwachen, für die ich verantwortlich bin (d.h. Websites, die wir bei mgm entwickelt haben), könnte aber auch wertvolle Informationen über andere Marktteilnehmer liefern. Es könnte sowohl von technischen Personen als auch von den Marketing-Leuten genutzt werden - da sie _manchmal_ auch die Leistung beeinträchtigen. Ich wäre neugierig, solche Statistiken für Zalando zu sehen 😜

Kennt jemand ein solches Überwachungssystem? Bitte lassen Sie es mich wissen.
```