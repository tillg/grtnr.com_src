---
date: 2016-01-08
image: ping.png
excerpt: Ein einfaches Zwei-Komponenten-Tool für langfristiges Ping-Logging und -Visualisierung, das endlich klärt, ob es das WLAN, der Internetzugang oder die Anwendung ist, die langsam ist.
title: Ping-Visualisierung und -Analyse
tags: tech
translation: de
source_language: en
source_hash: b8e1c642e2db4162fd47dde0b595cbafa4804738e699aec9408da33124f7fbb3
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:26:40.832106+00:00
generated_by: simplified-translation-system
---

Das ist die Situation, mit der ich konfrontiert bin: Ich nutze einen Internetzugang, der sich nicht zuverlässig anfühlt. Manchmal ist er wirklich schnell, manchmal fühlt er sich einfach sehr unzuverlässig an. Und ich weiß nie genau, welcher Teil gerade versagt: Ist es die Anwendung, die langsam ist, ist es das WLAN, ist es der Internetzugang.

Was ich also gesucht habe, ist eine zuverlässige, langfristige Messung der Internetzugangsgeschwindigkeit. Mit Geschwindigkeit meine ich hauptsächlich Round-Trip-Zeit / Latenz. Ich habe mir viele Tools angeschaut, große (die aus kompletten Ökosystemen wie Nagios oder Icinga stammen) und kleine (z.B. Netzwerküberwachung direkt auf deinem PC oder Mac). Die großen sind zu viel Arbeit und zu viel, was gelernt, verstanden und installiert werden muss. Die kleinen beantworten meine Frage nicht, da sie kein langfristiges Tracking und Aufzeichnen machen. Und ich mag keine komplexen Sachen.

Dann habe ich etwas gefunden, das im Wesentlichen genau das ist, wonach ich gesucht habe. Anders formuliert: Wenn ich selbst etwas hätte zusammenstellen müssen, wäre es das, was ich gebaut hätte: Es heißt [Ping-Visualisierung und -Analyse](http://www.medienvilla.com/entwicklung.html#pinganalyse) und basiert auf 2 Komponenten:

- Ein einfaches Skript, das Ping-Zeiten loggt (und mit einfach meine ich _wirklich einfach!_)
- Eine HTML-Seite mit etwas JavaScript, das die Ping-Zeiten über die Zeit visualisiert.

Du kannst den Ping-Logger auf unglaublich einfacher Hardware laufen lassen. Er kann Tag und Nacht laufen und Daten sammeln. Das Format ist _einfach_. Ein Beispiel:

```no-highlight
Fri Jan  8 15:14:49 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=89 ttl=53 time=310.716 ms
Fri Jan  8 15:14:54 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=90 ttl=53 time=310.349 ms
Fri Jan  8 15:14:59 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=91 ttl=53 time=312.787 ms
Fri Jan  8 15:15:04 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=92 ttl=53 time=312.805 ms
Fri Jan  8 15:15:09 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=93 ttl=53 time=311.273 ms
Fri Jan  8 15:15:14 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=94 ttl=53 time=311.371 ms
Fri Jan  8 15:15:19 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=95 ttl=53 time=312.096 ms
Fri Jan  8 15:15:24 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=96 ttl=53 time=313.387 ms
Fri Jan  8 15:15:29 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=97 ttl=53 time=310.404 ms
Fri Jan  8 15:15:34 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=98 ttl=53 time=311.076 ms
Fri Jan  8 15:15:39 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=99 ttl=53 time=312.640 ms
```

Ziemlich einfach, oder?! Ein einfaches `ping` mit einem Zeitstempel davor. Und das JS-Zeug liest es und erstellt daraus einen einfachen Graphen:

![Graph](ping.png)

Ich musste nur ein paar kleine Dinge anpassen, damit es auf meinem Mac läuft (die `ping`-Syntax stammte aus einem anderen Unix-Dialekt).

## Was als Nächstes?
Hier ist, was ich plane zu verbessern (mal sehen, ob das wirklich passiert):

- Die Quellen in GIT einpflegen
- Den Graphen verbessern:
  - Die Farben sind mir ein bisschen seltsam...
  - Es fühlt sich verkehrt herum an
  - Beschriftungen auf der y-Achse hinzufügen
  - Vielleicht mehr [so in der Art](http://pinglogger.co.uk/index.php/screenshots/)
- Vielleicht mal [log stash](https://www.elastic.co/products/logstash) als Visualisierung ausprobieren...

## Nachtrag
Auch im Kontext, und weil [Java die Programmiersprache des Jahres 2015 ist](http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html): [Ein Java-Programm, um die Ping-Zeiten zu mehreren Endpunkten zu verfolgen](http://pastebin.com/1qnCXDw7)