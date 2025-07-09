---
date: 2025-03-14
image: pools.png
excerpt: J’aimerais créer un petit site web qui optimise mes créneaux de natation dans les piscines publiques de Munich.
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T08:28:52.901154
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-03-14-optimal-swimming-slot/2025-03-14-optimal-swimming-slot.md
Generated-By: automatic-translation-plugin
---

![Piscines](pools.png)

Comme la plupart d'entre vous le savent probablement, je vis à [Munich/Allemagne](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). Et depuis que nous avons vécu au Vietnam, je me suis passionné pour la natation - peut-être pas vraiment passionné, mais je l'apprécie. J'ai appris à nager en crawl sur plus de 1 km en mer au Vietnam, et de temps en temps, je travaille à maintenir cette compétence ici à Munich.

Le problème est qu'à Munich, il faut une piscine publique (car je n'en ai pas une privée 😉), et les piscines publiques ont tendance à être pleines et bondées. Heureusement, les SWM (les services publics de Munich) fournissent un [site web](https://www.swm.de/baeder/auslastung) qui nous indique à quel point les différentes piscines publiques sont fréquentées.

Même si je travaille 40 heures par semaine (ou à peu près…), je pourrais avoir une certaine flexibilité quant au moment où je vais nager : avant le travail, après le travail, peut-être même à l'heure du déjeuner. Et la question se pose, quand est-il préférable d'y aller. Quand les piscines sont-elles le moins bondées ?

Par exemple : je soupçonne que se rendre à la piscine le plus tôt possible le matin n'est pas le plus intelligent, car de nombreux travailleurs en col blanc sportifs le font. Il est donc peut-être plus judicieux de prendre le thé avec ma femme le matin, puis d'aller nager et de me rendre au bureau.

Le meilleur dans ce problème : c'est un problème typique d'apprentissage automatique 😉

Voici donc le plan :

- Construire un scraper qui recueille l'occupation des piscines toutes les 10 minutes et la stocke quelque part
- Entraîner un modèle d'apprentissage automatique sur ces données
- Créer une interface utilisateur qui demande quand vous pourriez y aller, et qui vous conseille quand vous devriez y aller
- Fonctionnalités supplémentaires : prendre en compte les week-ends et les jours fériés, les caractéristiques des piscines (c'est-à-dire que je préfère nager dans une piscine de 50 m)

Quelqu'un est partant pour construire un tel outil ? Envoyez-moi un email si vous voulez coder 😉