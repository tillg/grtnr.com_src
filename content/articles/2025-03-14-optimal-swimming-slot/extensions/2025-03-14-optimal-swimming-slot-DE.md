---
date: 2025-03-14
image: pools.png
excerpt: Ich würde gerne eine kleine Webseite erstellen, die meine Schwimmzeiten in Münchens öffentlichen Schwimmbädern optimiert.
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:42:02.792632
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-03-14-optimal-swimming-slot/2025-03-14-optimal-swimming-slot.md
Generated-By: automatic-translation-plugin
---

![Schwimmbäder](pools.png)

Wie die meisten von Ihnen wahrscheinlich wissen, lebe ich in [München/Deutschland](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). Und seitdem wir in Vietnam gelebt haben, habe ich das Schwimmen für mich entdeckt - vielleicht nicht wirklich süchtig, aber ich genieße es. Ich habe gelernt, über 1 km im Meer in Vietnam Freistil zu schwimmen, und von Zeit zu Zeit arbeite ich daran, diese Fähigkeit hier in München am Leben zu erhalten.

Das Problem ist, in München braucht man ein öffentliches Schwimmbad (weil ich kein privates habe 😉), und öffentliche Schwimmbäder neigen dazu, voll und überfüllt zu sein. Glücklicherweise bietet die SWM (die Münchner Stadtwerke) eine [Webseite](https://www.swm.de/baeder/auslastung) an, die uns sagt, wie stark die verschiedenen öffentlichen Schwimmbäder ausgelastet sind.

Obwohl ich 40 Stunden/Woche (oder so...) arbeite, habe ich vielleicht etwas Flexibilität, wann ich schwimmen gehe: vor der Arbeit, nach der Arbeit, vielleicht sogar in der Mittagspause. Und die Frage stellt sich, wann ist der beste Zeitpunkt. Wann sind die Schwimmbäder am wenigsten überfüllt?

Zum Beispiel: Ich vermute, dass es nicht das Klügste ist, so früh wie möglich am Morgen zu gehen, da viele sportliche Büroangestellte dies tun. Vielleicht ist es klüger, morgens mit meiner Frau Tee zu trinken und dann schwimmen zu gehen und ins Büro zu fahren.

Das Beste an diesem Problem: Es ist ein typisches maschinelles Lernproblem 😉

Also wäre das der Plan:

- Einen Scraper erstellen, der alle 10 Minuten die Belegung des Schwimmbads erfasst und irgendwo speichert
- Ein maschinelles Lernmodell auf diesen Daten trainieren
- Eine Benutzeroberfläche erstellen, die fragt, wann Sie gehen könnten, und die Ihnen Ratschläge gibt, wann Sie gehen sollten
- Zusätzliche Funktionen: Wochenenden und Feiertage berücksichtigen, Pool-Eigenschaften (d.h. ich schwimme lieber in einem 50m Pool)

Hat jemand Lust, ein solches Tool zu erstellen? Schicken Sie mir eine E-Mail, wenn Sie mitmachen möchten 😉