---
date: 2026-02-27
image: hero.svg
excerpt: Où est passé mon espace disque ? Un processus en arrière-plan discret qui surveille les répertoires de votre Mac au fil du temps, afin que lorsque votre disque se remplit, vous sachiez réellement pourquoi.
title: DiskSpaceTracker
tags: tech, softwareweneed, Mac
translation: fr
source_language: en
source_hash: e6e3d5b71bde67af284ada3a80c67c01435c14f31288b1af7ca7a1eae9a0cea9
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:30:14.516437+00:00
generated_by: simplified-translation-system
---

Le disque de mon MacBook se remplit avec le temps. C'est toujours le cas. Et chaque fois que je reçois cette notification "Votre disque est presque plein", je n'ai aucune idée de ce qui s'est passé. Ai-je téléchargé quelque chose de volumineux ? Un cache a-t-il gonflé ? Une application a-t-elle silencieusement déversé des gigaoctets dans Library ? J'ouvre Utilitaire de disque, je fixe une barre colorée et je commence à deviner.

Ce n'est pas ainsi que cela devrait fonctionner. Je veux un processus qui suit discrètement l'utilisation de mon disque au fil du temps — répertoire par répertoire — afin que lorsque les choses se resserrent, je puisse consulter une chronologie et voir : _voici ce qui a augmenté, voici quand cela s'est produit, voici où chercher._

## Ce que DiskSpaceTracker ferait

Un démon léger en arrière-plan qui ne s'exécute que lorsque deux conditions sont remplies :

1. **Le Mac est inactif** — aucune entrée utilisateur active pendant N minutes
2. **Le Mac est sur secteur** — pas de décharge de la batterie pour la comptabilité

Lorsque les deux conditions sont vraies, il se réveille et prend un instantané.

## L'instantané

Un instantané parcourt l'arborescence des répertoires de haut en bas et enregistre, pour chaque répertoire :

- **Chemin** — le répertoire
- **Taille** — taille totale incluant les sous-répertoires
- **Hash du contenu** — un hash de la sortie `ls` (noms de fichiers, tailles, dates de modification)
- **Horodatage** — quand l'instantané a été pris

Le hash du contenu est l'idée clé. Si le hash d'un répertoire n'a pas changé depuis le dernier instantané, rien à l'intérieur n'a changé — passez les sous-répertoires. Cela rend le scan rapide même sur de grands disques. Vous ne creusez plus profondément que là où quelque chose a réellement bougé.

```text
/Users/till           2026-02-27T03:12  148.2 GB  a3f8c1...
/Users/till/Downloads 2026-02-27T03:12   23.1 GB  9e2b44...  ← changé
/Users/till/Library   2026-02-27T03:12   41.7 GB  7d1f09...  ← changé
/Users/till/Documents 2026-02-27T03:12   62.3 GB  a3f8c1...  ← inchangé, passez les enfants
```

## Format de stockage

Une base de données locale simple (SQLite conviendrait) avec une table :

| dir                        | date       | size_bytes  | content_hash |
| -------------------------- | ---------- | ----------- | ------------ |
| /Users/till/Downloads      | 2026-02-27 | 24851390464 | 9e2b44...    |
| /Users/till/Downloads      | 2026-02-20 | 19327352832 | f1a3c7...    |
| /Users/till/Library/Caches | 2026-02-27 | 8741281792  | 3bf812...    |

Chaque ligne est un instantané d'un répertoire à un moment donné. Interrogez-le comme vous le souhaitez — croissance par semaine, plus grands changements, répertoires apparus de nulle part.

Important : la base de données doit également enregistrer quand un répertoire a été _confirmé inchangé_. Si je scanne `/Users/till/Documents` et que le hash est le même que la semaine dernière, c'est un point de données — "vérifié, pas de changement." C'est fondamentalement différent d'un répertoire que je n'ai tout simplement pas regardé depuis des mois. Sans cette distinction, vous ne pouvez pas distinguer "stable" de "inconnu."

## Ce que je voudrais voir

Une simple interface en ligne de commande ou dans la barre de menus qui répond :

- **Ce qui a le plus augmenté** la semaine / le mois dernier ?
- **Quoi de neuf** — répertoires ou fichiers qui n'existaient pas auparavant ?
- **Chronologie** — comment `/Users/till/Library/Caches` a-t-il changé au cours des 6 derniers mois ?
- **Alertes** — avertissez-moi lorsqu'un répertoire unique augmente de plus de X GB en une semaine

Rien de sophistiqué. Quelques tableaux triés et peut-être un sparkline. Les données sont le produit — l'interface utilisateur est juste un moyen de poser des questions.

## Pourquoi cela n'existe pas (ou pourquoi les outils existants manquent le point)

Il existe des analyseurs d'espace disque — DaisyDisk, GrandPerspective, ncdu. Ils vous montrent ce qui est grand _en ce moment_. C'est utile pour un nettoyage ponctuel, mais cela ne vous dit pas ce qui a changé. Si `/Library/Developer/CoreSimulator` fait 30 GB, a-t-il toujours fait 30 GB ? Ou faisait-il 5 GB le mois dernier ? Sans historique, vous ne pouvez pas savoir.

Il existe également des outils de surveillance, mais ils suivent l'espace libre _total_ comme un seul chiffre. "Votre disque est passé de 40 GB libres à 12 GB libres en trois semaines." Super — mais _où_ ?

DiskSpaceTracker se situe entre les deux : il suit l'espace par répertoire au fil du temps. C'est la pièce manquante.

## Réflexions techniques

- **macOS-native** — utilise `NSProcessInfo` pour la détection d'inactivité, IOKit pour l'état de l'alimentation
- **Fonctionne comme un LaunchDaemon** — méthode standard macOS pour planifier le travail en arrière-plan
- **Stockage SQLite** — fichier unique, pas de serveur, facile à interroger, facile à sauvegarder
- **Liste d'exclusion** — ignorez `/System`, les instantanés Time Machine et d'autres chemins non exploitables
- **Empreinte minimale** — le saut basé sur le hash signifie que la plupart de l'arborescence n'est jamais touchée les jours calmes
- **Priorité de scan intelligente** — le scanner ne peut pas tout vérifier à chaque fois, il doit donc décider quoi regarder ensuite. Un algorithme simple qui pèse trois facteurs : les plus grands répertoires d'abord (c'est là que se trouve l'espace), les répertoires les moins récemment scannés ensuite (ne laissez pas de zones d'ombre), et les répertoires dont le hash parent a changé (quelque chose a bougé). De cette façon, les instantanés les plus précieux sont pris en premier, et au fil du temps, la couverture reste homogène.

Le tout pourrait être un seul binaire Swift sans dépendances. Ou un script Python avec des hooks `osascript`. Peu importe — l'idée est suffisamment simple pour que l'implémentation soit presque triviale. Ce qui importe, c'est qu'il fonctionne de manière cohérente et construise un historique.

C'est le logiciel que je veux. Pas un autre outil "ce qui est grand en ce moment" — un observateur discret qui construit une chronologie de l'endroit où va mon espace disque, afin que lorsque les choses se resserrent, la réponse soit déjà là.