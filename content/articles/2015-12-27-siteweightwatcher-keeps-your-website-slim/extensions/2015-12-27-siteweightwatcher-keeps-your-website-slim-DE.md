---
image: kickz_dashboard.png
excerpt: Eine Idee für ein Überwachungstool, das kontinuierlich Produktionswebsites auf Leistungsverschlechterung testet und das Seitengewicht sowie die Ladezeiten im Laufe der Zeit verfolgt.
title: SiteWeightWatcher - hält Ihre Website schlank
tags: Tech
translation: de
source_language: en
source_hash: 3c6a5c65a064281016f8b02137e4555a5d125847a26804b6331f1c60d94eac2a
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:01:52.209513+00:00
generated_by: simplified-translation-system
---

Gute Softwareentwickler testen ihre Sachen. Und die [TDD (Test Driven Development)](https://www.wikiwand.com/en/Test-driven_development) Süchtigen sind wahre Fanatiker, wenn es ums Testen geht. Diese Leute denken normalerweise in Code, sei es Java, Python, nodeJS, Sie nennen es. TDD bedeutet, dass Sie zuerst Tests schreiben und dann nur so viel Code schreiben, wie nötig ist, um die Tests grün werden zu lassen. Dann überarbeiten Sie Ihren Code und erst dann beginnen Sie, Tests für neue Anforderungen zu schreiben.
![TDD-Prozess](tdd.png)

Das ist **sehr** testlastig. Meiner Meinung nach wird man, wenn man es so macht, wie es in den Büchern geschrieben steht, schrecklich langsam und es wird unsinnig. Aber das ist eine andere Diskussion, die ich hier nicht klären möchte...

Was bei den meisten Testansätzen, die ich in der Vergangenheit gesehen habe, fehlt, sind die folgenden zwei Dinge:

1. Die Testleute und Testwerkzeuge hören auf, die Software oder Website zu überwachen, sobald sie in Produktion gegangen ist. Irgendwie haben sie das Gefühl, dass ihre Verantwortung mit dem Live-Gang endet...
2. Sie testen die Software. Nicht den Rest, d.h. das Design, das HTML, das CSS usw. Und die Benutzererfahrung, das Gefühl, ob das, was ich sehe, berühre, durchsuche und navigiere, von guter Qualität ist, wird stark von dieser Verpackung der Softwarelogik beeinflusst.

Ich suche also nach einem Tool, um (webbasierte) Software zu testen, sobald sie in der freien Wildbahn ist und während der gesamten Benutzererfahrung. Stellen Sie sich eine Website vor, einen einfachen Blog. Sie könnte perfekt gewesen sein, als sie gestartet wurde, aber mit der Zeit verschlechtert sie sich: Die Designer haben so viele Schnickschnack hinzugefügt, das Volumen des Inhalts ist gewachsen, es wurde optimiert, um auf Mobilgeräten besser nutzbar zu sein... Und schließlich ist die Seite aufgebläht, schwer und langsam. Warum muss ich darauf warten, dass meine Benutzer es mir sagen (das wäre Beschweren)?

Bei [mgm technology partners](https://mgm-tp.com) haben wir automatisierte Test-Suiten, die jede Nacht laufen. So haben Entwickler, die Code eingebaut haben, der die Software verlangsamt, jeden Morgen einen Bericht in ihrem Posteingang.

Also, hier ist, was mein SiteWeightWatcher tun sollte:

- Alle 5-30 Minuten Tests gegen die Produktionsseite durchführen
- Alle Seiten überprüfen, nicht nur index.html
- Sofort melden, wenn Seiten langsam werden (langsamer als sie es früher waren)
- Schlüsselkennzahlen verfolgen und wie sie sich im Laufe der Zeit entwickeln:
- Wie viel Daten werden für jede Seite übertragen?
- Wie viele Anfragen gehen hin und her?
- Wie viel Zeit benötigt die Produktsuche? Im Laufe der Zeit...
- Wie gut ist die Seite für Benutzer in Deutschland, Großbritannien, den USA oder Asien verbunden? Im Laufe der Zeit, denn diese Dinge ändern sich, ohne dass wir etwas getan haben.

Ich könnte mir vorstellen, dass ein Dashboard für einen Online-Shop wie [KICKZ.com](https://www.kickz.com/de) so aussehen könnte:
![Dashboard-Skizze](kickz_dashboard.png)Ein Dashboard, das zeigt, wie sich die Seitengrößen entwickeln

Und genau wie die normalen Testteams sollten sich auch diese Tests weiterentwickeln und immer mehr an die Seite, ihre Funktionalität und ihre Benutzer anpassen. Wann immer wir ein echtes Problem oder einen Fehler dort draußen haben, müssen wir sicherstellen, dass unser WeightWatcher es findet, falls es erneut auftreten sollte.

Wie könnten wir beginnen, ein solches Tool zu bauen? Einige Gedanken:

- Wir haben Agenten und einen zentralen Server. Die Agenten sind weltweit oder in verschiedenen Netzwerken verteilt (denken Sie an kleine Docker-Images, die auf verschiedenen Clouds laufen). Sie berichten alle ihre erfassten Daten an den zentralen Server. Hier werden die Berichte erstellt und die interaktive Erklärung der Daten bereitgestellt.
- Die Agenten beginnen, einfache Metriken zu sammeln:
- Anzahl der HTTP-Anfragen pro Seite
- Übertragene Datenmenge pro Seite
- Anzahl der JavaScript-Zeilen pro Seite
- Zeit zum Laden der Daten
- Zeit zur Ausführung von JavaScript
- Basierend darauf beginnen wir mit einfachen Berichten:
- Wie groß ist die durchschnittliche Seitengröße?
- Wie viele Anfragen gibt es durchschnittlich pro Seite?
- Was sind meine _schwersten_ Seiten?
- Ein Diagramm, das die Verfügbarkeit meiner Seite sowie die Ladezeit über eine 24-Stunden-Skala, eine Woche, einen Monat zeigt. Vielleicht erleben meine Benutzer langsames Laden nur abends.

Von dort aus erweitern wir die gesammelten Daten sowie die Berichte.

Ein solches Tool wäre großartig, um Websites zu überwachen, für die ich verantwortlich bin (d.h. Websites, die wir bei mgm entwickelt haben), könnte aber auch wertvolle Informationen über andere Marktteilnehmer liefern. Es könnte sowohl von technischen Leuten als auch von den Marketing-Leuten genutzt werden - da sie _manchmal_ auch die Leistung beeinträchtigen. Ich wäre neugierig, solche Statistiken für Zalando zu sehen 😜

Kennt jemand ein solches Überwachungssystem? Bitte lassen Sie es mich wissen.