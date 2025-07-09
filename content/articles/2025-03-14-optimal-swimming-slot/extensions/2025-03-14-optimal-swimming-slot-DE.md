---
date: 2025-03-14
image: pools.png
excerpt: Ich würde gerne eine kleine Website erstellen, die meine Schwimmzeiten in den öffentlichen Schwimmbädern Münchens optimiert.
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:28:02.793333
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-03-14-optimal-swimming-slot/2025-03-14-optimal-swimming-slot.md
Generated-By: automatic-translation-plugin
---

![Schwimmbäder](pools.png)

Wie die meisten von Ihnen wahrscheinlich wissen, lebe ich in [München/Deutschland](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). Und seit wir in Vietnam gelebt haben, bin ich vom Schwimmen begeistert – vielleicht nicht wirklich süchtig, aber ich genieße es. Ich habe in Vietnam gelernt, über 1 km im Meer zu kraulen, und von Zeit zu Zeit arbeite ich daran, diese Fähigkeit hier in München aufrechtzuerhalten.

Das Problem ist, in München benötigt man ein öffentliches Schwimmbad (da ich kein privates habe 😉), und öffentliche Schwimmbäder sind oft voll und überfüllt. Glücklicherweise bieten die SWM (die Münchner Stadtwerke) eine [Website](https://www.swm.de/baeder/auslastung) an, die uns zeigt, wie ausgelastet die verschiedenen öffentlichen Schwimmbäder sind.

Obwohl ich 40 Stunden pro Woche arbeite (oder so…), habe ich möglicherweise etwas Flexibilität, wann ich schwimmen gehe: vor der Arbeit, nach der Arbeit, vielleicht sogar zur Mittagszeit. Und die Frage stellt sich, wann es am besten ist zu gehen. Wann sind die Schwimmbäder am wenigsten überfüllt?

Zum Beispiel: Ich vermute, dass es nicht die klügste Idee ist, so früh wie möglich am Morgen zu gehen, da viele sportliche Büroangestellte dies tun. Vielleicht ist es also klüger, morgens mit meiner Frau Tee zu trinken und dann schwimmen zu gehen und ins Büro.

Das Beste an diesem Problem: Es ist ein typisches Machine-Learning-Problem 😉

Also wäre dies der Plan:

- Einen Scraper entwickeln, der alle 10 Minuten die Auslastung der Schwimmbäder erfasst und irgendwo speichert
- Ein Machine-Learning-Modell mit diesen Daten trainieren
- Eine Benutzeroberfläche erstellen, die fragt, wann Sie gehen könnten, und Ihnen Ratschläge gibt, wann Sie gehen sollten
- Zusätzliche Funktionen: Berücksichtigung von Wochenenden und Feiertagen, Schwimmbad-Features (z. B. schwimme ich lieber in einem 50m-Becken)

Hat jemand Lust, ein solches Tool zu entwickeln? Schicken Sie mir eine E-Mail, wenn Sie Lust auf ein Hack haben 😉