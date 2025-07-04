---
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T17:02:45.924974
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2015-12-27-siteweightwatcher-keeps-your-website-slim/2015-12-27-siteweightwatcher-keeps-your-website-slim.md
Generated-By: automatic-translation-plugin
---

```markdown
---
layout: post
title: SiteWeightWatcher - garde votre site web léger
slug: siteweightwatcher-garde-votre-site-web-léger
date_published: 2015-12-27T00:00:00.000Z
date_updated: 2021-12-06T14:38:49.000Z
tags: Tech
image: kickz_dashboard.png
---

Les bons développeurs de logiciels testent leurs créations. Et les accros du [TDD (Test Driven Development)](https://www.wikiwand.com/en/Test-driven_development) sont des maniaques en matière de tests. Ces personnes pensent généralement en code, que ce soit Java, Python, nodeJS, vous l'appelez. TDD signifie que vous écrivez d'abord les tests, puis vous codez juste ce qu'il faut pour que les tests deviennent verts. Ensuite, vous retravaillez votre code et ce n'est qu'alors que vous commencez à écrire des tests pour de nouvelles exigences.
![Processus TDD](tdd.png)

C'est **très** axé sur les tests. Mon opinion est que si vous le faites comme c'est écrit et décrit dans les livres, vous devenez terriblement lent et cela tourne au non-sens. Mais c'est une autre discussion, et ce n'est pas une que je veux régler ici...

Ce qui manque dans la plupart des approches de test que j'ai vues dans le passé, ce sont les deux choses suivantes :

1. Les testeurs et les outils de test cessent de surveiller le logiciel ou le site web une fois qu'il est en production. D'une manière ou d'une autre, ils estiment que leur responsabilité s'arrête avec la mise en ligne...
2. Ils testent le logiciel. Pas le reste, c'est-à-dire le design, le HTML, le CSS, etc. Et l'expérience utilisateur, le sentiment de savoir si ce que je vois, touche, navigue est de bonne qualité, est très influencé par cet emballage de la logique logicielle.

Je cherche donc un outil pour tester les logiciels (basés sur le web) une fois qu'ils sont dans la nature et tout au long de l'expérience utilisateur. Imaginez un site web, un simple blog. Il pourrait être parfait lors de son lancement, mais avec le temps, il se dégrade : les designers ont ajouté tant de fioritures, le volume du contenu a augmenté, il a été ajusté pour être plus utilisable sur les mobiles... Et finalement, le site est gonflé, lourd et lent. Pourquoi dois-je attendre que mes utilisateurs me le disent (ce qui serait se plaindre) ?

Chez [mgm technology partners](https://mgm-tp.com), nous avons des suites de tests automatisés qui s'exécutent chaque nuit. Ainsi, les développeurs qui ont intégré du code ralentissant le logiciel reçoivent un rapport qui leur indique chaque matin dans leur boîte de réception.

Voici donc ce que mon SiteWeightWatcher devrait faire :

- Exécuter des tests toutes les 5 à 30 minutes sur le site de production
- Vérifier toutes les pages, pas seulement index.html
- Signaler immédiatement lorsque les pages deviennent lentes (c'est-à-dire plus lentes qu'elles ne l'étaient auparavant)
- Suivre les indicateurs clés et leur évolution dans le temps :
  - Quelle quantité de données est transférée pour chaque page ?
  - Combien de requêtes sont échangées ?
  - Combien de temps faut-il pour rechercher des produits ? Au fil du temps...
  - Quelle est la connectivité du site pour les utilisateurs en Allemagne, au Royaume-Uni, aux États-Unis ou en Asie ? Au fil du temps, car ces choses changent sans que nous ayons fait quoi que ce soit.

Je pourrais imaginer un tableau de bord pour une boutique en ligne comme [KICKZ.com](https://www.kickz.com/de) ressemblant à ceci :
![Esquisse du tableau de bord](kickz_dashboard.png)Un tableau de bord qui montre comment les tailles de page évoluent

Et tout comme les équipes de test normales le font, ces tests devraient également évoluer et s'adapter de plus en plus au site, à sa fonctionnalité et à ses utilisateurs. Chaque fois que nous avons un vrai problème ou un bug, nous devons nous assurer que notre WeightWatcher le détectera au cas où il apparaîtrait ou se reproduirait.

Comment pourrions-nous commencer à construire un tel outil ? Quelques réflexions :

- Nous avons des agents et un serveur central. Les agents sont situés partout dans le monde ou dans différents réseaux (pensez à de petites images Docker qui s'exécutent sur différents clouds). Ils rapportent toutes leurs données capturées au serveur central. C'est là que les rapports sont générés et où une explication interactive des données est fournie.
- Les agents commencent à collecter des métriques simples :
  - Nombre de requêtes HTTP par page
  - Données transférées par page
  - Nombre de lignes de JavaScript par page
  - Temps de chargement des données
  - Temps d'exécution du JavaScript
- À partir de cela, nous commençons avec des rapports simples :
  - Quelle est la taille moyenne des pages ?
  - Quel est le nombre moyen de requêtes par page ?
  - Quelles sont mes pages les _plus lourdes_ ?
  - Un graphique qui montre la disponibilité de mon site ainsi que le temps de chargement sur une échelle de 24 heures, une semaine, un mois. Peut-être que mes utilisateurs ne rencontrent des temps de chargement lents que le soir.

De là, nous étendons les données que nous collectons ainsi que les rapports.

Un tel outil serait formidable pour surveiller les sites dont je suis responsable (c'est-à-dire les sites web que nous avons développés chez mgm) mais pourrait également fournir des informations précieuses sur d'autres acteurs du marché. Il pourrait être utilisé à la fois par des personnes techniques ainsi que par les équipes marketing - car elles aussi _parfois_ compromettent la performance. Je serais curieux de voir ce genre de statistiques pour Zalando 😜

Quelqu'un connaît-il un tel système de surveillance ? Merci de me le faire savoir.
```