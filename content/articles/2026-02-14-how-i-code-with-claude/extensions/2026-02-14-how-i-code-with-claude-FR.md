---
date: 2026-02-14
image: claude.png
excerpt: Un aperçu de ma façon de coder avec Claude Code (à ce jour, mi-février 2026). Attendez-vous à ce que ce soit obsolète dès mars '26 😉
tags: code
translation: fr
source_language: en
source_hash: c1b098ab5de9c363bc2e25d9798aa85422774ea318267a39100bc64c2686076f
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:52.814858+00:00
generated_by: simplified-translation-system
---

Comme je l'ai présenté plusieurs fois, et comme on me l'a demandé encore plus souvent, voici un bref aperçu de ma méthode de travail lorsque je code avec Claude Code. C'est un flux de travail simple, sans fioritures. Il se concentre d'abord sur le cahier des charges, en les itérant avant de lancer le codage proprement dit.

Voici comment cela fonctionne :

- Je commence par noter un bref cahier des charges (par exemple dans `spec.md`). Souvent juste une seule ligne de texte, suivie d'une liste à puces avec mes réflexions. Tout cela sous forme de fichier markdown.
- Ensuite, je lance ma commande `/spec-build-out` : `/spec-build-out spec.md` (Remarque : je travaille souvent dans le terminal intégré de VScode, et là, vous pouvez glisser-déposer le fichier md dans le terminal et il collera le nom complet du fichier).
- Cela développe et affine mon `spec.md`. Je le lis, le révise et l'annote. Je marque mes notes avec `->`.
- Ensuite, je lance la commande `/spec-iterate` : Cela intègre mes annotations et nettoie à nouveau `spec.md`.
- Puis j'annote à nouveau, lance `/spec-iterate` à nouveau, et ainsi de suite.
- Quand je sens que tout est en ordre, je commence une nouvelle conversation avec `/new` et lance `/spec-ready-or-not spec.md`.
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
## Flux de travail des spécifications

Lors de l'itération sur les documents de spécification :

1. Recherchez toujours les annotations de l'utilisateur (par exemple, des flèches '->', des balises comme [ACCEPTED], [REJECTED]) dès le PREMIER passage — ne nécessitez pas de relance.
2. Lors de la consolidation d'une spécification, supprimez entièrement les options rejetées et gardez le document concis.
3. Après la finalisation de la spécification, confirmez que toutes les questions ouvertes sont résolues avant de passer à l'implémentation.
```