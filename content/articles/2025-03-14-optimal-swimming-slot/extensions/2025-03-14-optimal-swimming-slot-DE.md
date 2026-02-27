---
date: 2025-03-14
image: pools.png
excerpt: Ich würde gerne eine kleine Website erstellen, die meine Schwimmzeiten in Münchens öffentlichen Schwimmbädern optimiert.
translation: de
source_language: en
source_hash: 1e537df304781d988060f741005dd61009713ccff9c32a05cdc91547f1cbf0c0
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:11:04.742098+00:00
generated_by: simplified-translation-system
---

![Schwimmbäder](pools.png)

Wie die meisten von Ihnen wahrscheinlich wissen, lebe ich in [München/Deutschland](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). Und seit wir in Vietnam gelebt haben, bin ich vom Schwimmen begeistert – vielleicht nicht wirklich süchtig, aber ich genieße es. Ich habe gelernt, über 1 km im Meer in Vietnam zu kraulen, und von Zeit zu Zeit arbeite ich daran, diese Fähigkeit hier in München aufrechtzuerhalten.

Das Problem ist, dass man in München ein öffentliches Schwimmbad braucht (weil ich kein privates habe 😉), und öffentliche Schwimmbäder neigen dazu, voll und überfüllt zu sein. Glücklicherweise bieten die SWM (die Münchner Stadtwerke) eine [Website](https://www.swm.de/baeder/auslastung) an, die uns zeigt, wie ausgelastet die verschiedenen öffentlichen Schwimmbäder sind.

Obwohl ich 40 Stunden pro Woche arbeite (oder so…), habe ich vielleicht etwas Flexibilität, wann ich schwimmen gehe: vor der Arbeit, nach der Arbeit, vielleicht sogar in der Mittagspause. Und die Frage stellt sich, wann es am besten ist zu gehen. Wann sind die Schwimmbäder am wenigsten überfüllt?

Zum Beispiel: Ich vermute, dass es nicht die klügste Idee ist, so früh wie möglich am Morgen zu gehen, da viele sportliche Büroangestellte das tun. Vielleicht ist es also klüger, morgens mit meiner Frau Tee zu trinken und dann schwimmen zu gehen und ins Büro zu fahren.

Das Beste an diesem Problem: Es ist ein typisches Machine-Learning-Problem 😉

Also wäre dies der Plan:

- Einen Scraper erstellen, der alle 10 Minuten die Belegung der Schwimmbäder erfasst und irgendwo speichert
- Ein Machine-Learning-Modell mit diesen Daten trainieren
- Eine Benutzeroberfläche erstellen, die fragt, wann Sie gehen könnten, und Ihnen Ratschläge gibt, wann Sie gehen sollten
- Zusätzliche Funktionen: Berücksichtigung von Wochenenden und Feiertagen, Schwimmbadmerkmale (z.B. ich schwimme lieber in einem 50m-Becken)

Hat jemand Lust, ein solches Tool zu entwickeln? Schicken Sie mir eine E-Mail, wenn Sie mitmachen möchten 😉