---
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T17:02:44.871876
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2016-01-08-ping-analysis/2016-01-08-ping-analysis.md
Generated-By: automatic-translation-plugin
---

```markdown
---
title: Visualisation et Analyse du Ping
tags: tech
image: ping.png
---

Voici la situation à laquelle je fais face : j'utilise un accès Internet qui ne semble pas fiable. Parfois, il est très rapide, parfois il semble tout simplement très peu fiable. Et je ne sais jamais exactement quelle partie échoue : est-ce l'application qui est lente, est-ce le WIFI, est-ce l'accès Internet.

Ce que je recherche, c'est une mesure fiable et à long terme de la vitesse d'accès à Internet. Par vitesse, j'entends principalement le temps aller-retour / latence. J'ai examiné de nombreux outils, des grands (ceux qui proviennent d'écosystèmes complets comme Nagios ou ecinga) aux petits (c'est-à-dire le suivi de l'utilisation du réseau directement sur votre PC ou Mac). Les grands sont trop de travail et trop de choses à apprendre, comprendre, installer. Les petits ne répondent pas à ma question car ils ne font pas de suivi et d'enregistrement à long terme. Et je n'aime pas les choses complexes.

Puis j'ai trouvé quelque chose qui est en essence exactement ce que je cherchais. Reformulons : si j'avais commencé à créer quelque chose moi-même, c'est ce que j'aurais construit : cela s'appelle [Visualisation et Analyse du Ping](http://www.medienvilla.com/entwicklung.html#pinganalyse) et cela repose sur 2 composants :

- Un simple script qui enregistre les temps de ping (et par simple, je veux dire _vraiment simple !_)
- Une page HTML avec un peu de JavaScript qui visualise les temps de ping au fil du temps.

Vous pouvez laisser le journal de ping fonctionner sur du matériel extrêmement simple. Il peut fonctionner jour et nuit, collectant des données. Le format est _simple_. Un exemple :

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

Assez simple, n'est-ce pas ?! Un simple `ping` avec un horodatage devant. Et le JS lit cela et en fait un graphique simple :

![graphique](ping.png)

J'ai juste dû corriger quelques petites choses pour le faire fonctionner sur mon Mac (la syntaxe `ping` provenait d'un autre dialecte Unix).

## Et ensuite ?
Voici donc ce que je prévois d'améliorer (voyons si cela se réalise vraiment) :

- Mettre les sources sous GIT
- Améliorer le graphique :
  - Les couleurs me semblent un peu étranges...
  - Cela semble à l'envers
  - Ajouter des étiquettes sur l'axe y
  - Peut-être les avoir plus [comme ceci](http://pinglogger.co.uk/index.php/screenshots/)
- Peut-être examiner [log stash](https://www.elastic.co/products/logstash) pour la visualisation...

## Addendum
Également dans ce contexte, et parce que [Java est le langage de développement de l'année 2015](http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html) : [Un programme Java pour suivre les temps de ping vers plusieurs points de terminaison](http://pastebin.com/1qnCXDw7)
```