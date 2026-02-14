---
date: 2026-02-14
excerpt: Un aperçu de ma façon de coder avec Claude Code (à ce jour, mi-février 2026). Attendez-vous à ce que ce soit obsolète dès mars '26 😉
Tags: code
image: claude.png
title: Comment je code avec&nbsp;Claude
translation: fr
source_language: en
source_hash: 2a66ea615ac944fd5d9a6942aed81ef4504c5126213f75c514c87ed4000a8d8a
translator: gpt-4o-2024-08-06
translate_date: 2026-02-14T10:47:57.688118
generated_by: simplified-translation-system
---

Puisque je l'ai présenté plusieurs fois, et que l'on me l'a demandé encore plus souvent, voici un bref aperçu de ma méthode de travail lorsque je code avec Claude Code. C'est un flux de travail simple, rien de sophistiqué. Il se concentre d'abord sur la spécification, en l'itérant avant de lancer le codage proprement dit.

Voici comment cela fonctionne :

- Je commence par noter une brève spécification (par exemple dans `spec.md`). Souvent juste une seule ligne de texte, suivie d'une liste à puces avec mes réflexions. Tout cela sous forme de fichier markdown.
- Ensuite, je lance ma commande `/spec-build-out` : `/spec-build-out spec.md` (Remarque : je travaille souvent dans le terminal intégré de VScode, et là, vous pouvez glisser-déposer le fichier md dans le terminal et il collera le nom complet du fichier).
- Cela développe et affine mon `spec.md`. Je le lis, le révise et l'annote. Je marque mes notes avec `->`.
- Ensuite, je lance la commande `/spec-iterate` : Cela intègre mes annotations et nettoie à nouveau `spec.md`.
- Puis j'annote à nouveau, lance `/spec-iterate` à nouveau, et ainsi de suite.
- Quand je sens que tout est en ordre, je démarre une conversation `/new` et lance `/spec-ready-or-not spec.md`.
- Cela ajoute toutes les questions ouvertes qu'il a trouvées à la fin de `spec.md`.
- Même jeu : annoter `spec.md`, puis `/spec-iterate`.
- À un moment donné, je suis satisfait. Ensuite, je valide les spécifications et laisse Claude les implémenter. Parfois, je commence par un `/new` d'abord, pour commencer avec un contexte propre et frais.

Mes commandes `/` :

- [/spec-build-out](spec-build-out.md)
- [/spec-iterate](spec-iterate.md)
- [/spec-ready-or-not](spec-ready-or-not.md)
- [/spec-finish](spec-finish.md)

### Commentaires, notes et réflexions

Quand j'ai exécuté le Claude `/insights`, j'ai été complimenté pour le **Cycle de Développement Disciplinaire Axé sur les Spécifications** 😉

J'ai un peu joué avec l'explication à Claude sur la longueur que devrait avoir le `spec.md`. Sans aucune directive, il devenait énorme, contenant presque tout le code qu'il prévoyait d'insérer dans la base de code. Une fois que j'ai ajouté un `Veuillez garder le document court ! Ajoutez des extraits de code uniquement s'ils sont VRAIMENT essentiels !!`, il est devenu plus court - parfois trop court.

`/insights` a également suggéré l'ajout suivant à mon `claude.md` :

```markdown
## Flux de Travail des Spécifications

Lors de l'itération sur les documents de spécification :

1. Recherchez toujours les annotations de l'utilisateur (par exemple, les flèches '->', les balises comme [ACCEPTED], [REJECTED]) lors du PREMIER passage — ne nécessitez pas de relance.
2. Lors de la consolidation d'une spécification, supprimez entièrement les options rejetées et gardez le document concis.
3. Après la finalisation de la spécification, confirmez que toutes les questions ouvertes sont résolues avant de passer à l'implémentation.
```