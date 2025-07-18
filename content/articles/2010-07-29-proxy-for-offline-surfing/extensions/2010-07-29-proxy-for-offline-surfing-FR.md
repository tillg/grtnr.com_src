---
title: Un proxy pour naviguer hors ligne
tags: softwareweneed
translation: fr
source_language: en
source_hash: 89911d066379b74cbf18df8ca224757dce75e2fe0b679d46e6dea69cf823c7c3
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:16:12.305882
generated_by: simplified-translation-system
---

Voici un logiciel que j'aimerais avoir : un proxy qui fonctionne sur mon ordinateur portable et qui met en cache intelligemment certains sites web afin que je puisse les consulter lorsque je suis hors ligne.

Plus précisément :

- Un proxy qui fonctionne sur mon ordinateur portable
- Le proxy sait quelles pages/sites je souhaite avoir disponibles lorsque je suis hors ligne
- Lorsque le navigateur demande l'une de ces pages, le proxy vérifie si le site web est accessible. Si c'est le cas, il télécharge la page et l'envoie au navigateur. Si le proxy ne peut pas atteindre le site web, il essaie de servir la page à partir de son cache local.

De cette façon, je pourrais naviguer normalement lorsque je suis en ligne. Lorsque je suis hors ligne, je pourrais accéder à une petite partie d'internet – mais je pourrais toujours lire certaines pages.

Une fois cela réalisé, le proxy pourrait être amélioré :

- Pendant les périodes d'inactivité avec une connexion internet, il pourrait rafraîchir les pages de son cache
- En comptant les pages que j'accède souvent, il pourrait décider quelles pages il est judicieux de mettre en cache
- Il pourrait apprendre à quelle fréquence les pages changent et adapter les intervalles de rafraîchissement en conséquence
- …

Et voici les questions que je me pose :

- Quelqu'un connaît-il un outil qui offre cette fonctionnalité ?
- Quelqu'un verrait-il un problème majeur que j'aurais manqué ?
- Des idées intéressantes sur la façon dont cela pourrait être construit ?

Pour compléter l'information : j'utilise un MacBook, OS X 10.6. Les commentaires sont les bienvenus...

Passez une bonne soirée,

– Till.