---
date: 2025-03-14
image: pools.png
excerpt: J'aimerais créer un petit site web qui optimise mes créneaux de natation dans les piscines publiques de Munich.
title: Créneau de Natation&nbsp;Optimal
translation: fr
source_language: en
source_hash: ac29ce78a5d2d0bf16cdac10f2b864be7d6090aa7351358d34d8d43507b2a2ef
translator: gpt-4o-2024-08-06
translate_date: 2026-02-14T10:54:42.165064
generated_by: simplified-translation-system
---

![Piscines](pools.png)

Comme la plupart d'entre vous le savent probablement, je vis à [Munich/Allemagne](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). Et depuis que nous avons vécu au Vietnam, je me suis pris de passion pour la natation - peut-être pas vraiment accro, mais je l'apprécie. J'ai appris à nager en crawl sur plus d'un kilomètre en mer au Vietnam, et de temps en temps, je m'efforce de maintenir cette compétence ici à Munich.

Le problème, c'est qu'à Munich, il faut une piscine publique (car je n'en ai pas de privée 😉), et les piscines publiques ont tendance à être pleines et bondées. Heureusement, le SWM (les services publics de Munich) fournit un [site web](https://www.swm.de/baeder/auslastung) qui nous indique à quel point les différentes piscines publiques sont fréquentées.

Même si je travaille 40 heures par semaine (ou à peu près...), j'ai peut-être une certaine flexibilité quant au moment où je peux aller nager : avant le travail, après le travail, peut-être même à l'heure du déjeuner. Et la question se pose, quand est-il préférable d'y aller ? Quand les piscines sont-elles les moins fréquentées ?

Par exemple : je soupçonne que se rendre à la piscine le plus tôt possible le matin n'est pas le plus judicieux, car de nombreux travailleurs en col blanc sportifs le font. Il est donc peut-être plus intelligent de prendre le thé avec ma femme le matin, puis d'aller nager avant de me rendre au bureau.

Le meilleur dans ce problème : c'est un problème typique d'apprentissage automatique 😉

Voici donc le plan :

- Construire un scraper qui recueille l'occupation des piscines toutes les 10 minutes et la stocke quelque part
- Entraîner un modèle d'apprentissage automatique sur ces données
- Construire une interface utilisateur qui demande quand vous pourriez y aller, et qui vous conseille quand vous devriez y aller
- Fonctionnalités supplémentaires : prendre en compte les week-ends et jours fériés, les caractéristiques des piscines (par exemple, je préfère nager dans une piscine de 50 m)

Quelqu'un est partant pour construire un tel outil ? Envoyez-moi un email si vous voulez coder 😉