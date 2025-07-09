---
date: 2025-02-05
image: david_cursor_magic.png
excerpt: J'ai trouvé cette vidéo d'un développeur avec BEAUCOUP de conseils utiles sur comment utiliser Cursor - voici mes conclusions.
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:28:03.161100
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-02-05-cursor-magic/2025-02-05-cursor-magic.md
Generated-By: automatic-translation-plugin
---

[TOC]

Le week-end dernier, j'ai découvert cette vidéo de David Ondrej : [J'ai passé plus de 400 heures sur Cursor, voici ce que j'ai appris](https://youtu.be/gYLNxUxVomY?si=1Q2x2UWgqy1RHvLt). Le titre n'est pas très accrocheur, mais le contenu m'a été très utile. Voici donc mes notes pour que je puisse utiliser tous ses conseils et avoir les différentes invites et extraits à portée de main lorsque je code.

<iframe width="560" height="315" src="https://www.youtube.com/embed/gYLNxUxVomY?si=xQAMyMvQCsSwWztk" title="Lecteur vidéo YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Structure de l'invite

La structure générale de l'invite que David suggère :

1. ce que nous faisons
2. taguer les fichiers pertinents
3. comment exécuter // ce qu'il ne faut pas faire
4. décharge de contexte
5. répéter l'instruction principale
6. format de sortie

## Cursorrules

`.cursorrules.md` est un fichier que vous placez dans le répertoire racine de votre projet qui donne à l'IA plus de contexte sur votre projet. Voici la structure du fichier que David suggère :

```markdown
# APERÇU DU PROJET

# PERSONNALITÉ

# TECH STACK

- choisir une pile technologique avec des langages très populaires

# PROCESSUS DE CORRECTION D'ERREURS

étape 1 : expliquer l'erreur en termes simples
étape 2 : expliquer la solution en termes simples
étape 3 : montrer comment corriger l'erreur

# PROCESSUS DE CONSTRUCTION

# Nos - variables d'environnement

backend/.env
frontend/. env

# STRUCTURE ACTUELLE DES FICHIERS

Ici, vous collez le contenu de cette commande, afin que Cursor connaisse la structure de votre projet :
tree -L 4 -a -I 'node*modules | -git|\_pycache*|.DS\_$

# PROCESSUS DE PUSH GITHUB

# IMPORTANT

- Répétez les instructions les plus importantes.
```

Il suggère également fortement d'avoir un `.cursorignore` dans lequel vous listez vos fichiers `.env`. Cela empêche le chat et Composer d'écrire accidentellement dans ces fichiers.

## Règles de l'IA dans les paramètres de Cursor

Les règles de l'IA doivent être définies dans les paramètres de Cursor. Elles ne doivent contenir rien de spécifique au projet, juste des principes de codage que vous voudriez toujours appliquer. C'est la différence avec le `.cursorrules` qui contient également des détails spécifiques au projet.

Un exemple :

```markdown
# Principes Fondamentaux

- Écrire un code propre, simple et lisible
- Implémenter les fonctionnalités de la manière la plus simple possible
- Garder les fichiers petits et ciblés (<200 lignes)
- Tester après chaque changement significatif
- Se concentrer sur la fonctionnalité principale avant l'optimisation
- Utiliser un nommage clair et cohérent
- Réfléchir soigneusement avant de coder. Écrire 2-3 paragraphes de raisonnement.
- TOUJOURS écrire un code simple, propre et modulaire.
- utiliser un langage clair et facile à comprendre. écrire en phrases courtes.

# Correction d'Erreurs

- NE PAS TIRER DE CONCLUSIONS HÂTIVES ! Considérer plusieurs causes possibles avant de décider.
- Expliquer le problème en anglais simple
- Apporter les modifications minimales nécessaires, en changeant le moins de lignes de code possible
- en cas d'erreurs étranges, demander à l'utilisateur d'effectuer une recherche web Perplexity pour obtenir les informations les plus récentes

# Processus de Construction

- ﻿﻿Vérifier que chaque nouvelle fonctionnalité fonctionne en indiquant à l'utilisateur comment la tester
- ﻿﻿NE PAS écrire de code compliqué et déroutant. Opter pour une approche simple et modulaire.
- ﻿﻿en cas de doute sur ce qu'il faut faire, dire à l'utilisateur d'effectuer une recherche sur le web

# Commentaires

- TOUJOURS essayer d'ajouter des commentaires plus utiles et explicatifs dans notre code.
- NE JAMAIS supprimer d'anciens commentaires - sauf s'ils sont manifestement erronés / obsolètes.
- Inclure BEAUCOUP de commentaires explicatifs dans votre code. TOUJOURS écrire un code bien documenté.
- Documenter tous les changements et leur raisonnement DANS LES COMMENTAIRES QUE VOUS ÉCRIVEZ
- lors de l'écriture de commentaires, utiliser un langage clair et facile à comprendre. écrire des phrases courtes.
```

## Petites invites utiles

David fournit une liste de petites invites utiles ou d'extraits d'invites. J'en ai copié certains ici pour une utilisation copier-coller :

```text
Agissez comme un développeur senior avec un accent sur une architecture claire.

Moins il y a de lignes de code, mieux c'est.

Commencez par écrire 3 paragraphes de raisonnement analysant ce que l'erreur pourrait être. NE PAS TIRER DE CONCLUSIONS HÂTIVES.

NE VOUS ARRÊTEZ PAS DE TRAVAILLER jusqu'à ce que…

Répondez brièvement

NE SUPPRIMEZ PAS LES COMMENTAIRES

Vous devriez commencer le paragraphe de raisonnement avec beaucoup d'incertitude, et gagner lentement en confiance à mesure que vous réfléchissez davantage à l'élément.
```

## Grandes invites

### Résumé de l'état actuel

Utilisé pour résumer un flux de composition et passer à un nouveau dialogue de composition.

```text
Avant de continuer, j'ai besoin que vous me donniez un résumé de l'état actuel du projet.

Formatez cela en 3 paragraphes concis, où vous décrivez ce que nous venons de faire, ce qui n'a pas fonctionné, quels fichiers ont été mis à jour/créés, quelles erreurs éviter, les idées clés/leçons que nous avons apprises, les problèmes/erreurs auxquels nous sommes confrontés,… et tout autre élément dont un programmeur pourrait avoir besoin pour travailler efficacement sur ce projet.

Écrivez dans un ton conversationnel mais informatif, comme un fichier README sur GitHub qui est très dense en informations et sans fioritures ni bruit. NE PAS inclure d'hypothèses ou de théories, juste les faits.

Je m'attends à voir trois paragraphes concis, écrits comme si vous donniez des instructions à un autre programmeur et que c'était TOUT ce que vous pouviez lui dire.
```

### Impartial 50/50

```text
AVANT DE RÉPONDRE, je veux que vous écriviez deux paragraphes détaillés, l'un argumentant pour chacune de ces solutions - ne tirez pas de conclusions hâtives, considérez sérieusement les deux approches

puis, après avoir terminé, dites-moi si l'une de ces solutions est évidemment meilleure que l'autre, et pourquoi.
```

### requête de recherche en un paragraphe

```text
effectuons une recherche sur le web. votre tâche est d'écrire une requête de recherche en un paragraphe, comme si vous disiez à un chercheur humain ce qu'il faut trouver, en incluant tout le contexte pertinent. formatez le paragraphe comme des instructions claires, commandant à un chercheur de trouver ce que nous recherchons. demandez des extraits de code ou des détails techniques si nécessaire
```

## Instructions

David suggère d'avoir un répertoire `instructions` qui contient des fichiers md avec des conseils pour l'IA. De cette façon, vous pouvez référencer ces fichiers depuis l'invite de Composer. Il préfère ce type de fichiers d'instructions plutôt que de référencer @Docs dans Cursor, ce qui ne semble pas encore très bien fonctionner.

Fichiers d'instructions qu'il a mentionnés :

- `supabase.md` : Un fichier qui décrit la structure de sa base de données, afin que Cursor connaisse les tables, les champs, les obligations, etc.
- `roadmap.md` : Une explication de la feuille de route de votre projet.

## Autres outils

En plus de Cursor, David utilise de nombreux autres outils. Certains de ceux qu'il a mentionnés :

- [ChatGPT](https://chatgpt.com)
- [Claude](https://claude.ai) pour des discussions parallèles avec une IA avancée.
- [Perplexity](https://www.perplexity.ai) pour des recherches web intelligentes.
- [WisprFlow](https://wisprflow.ai) pour parler plutôt que taper
- [v0](https://v0.dev) un outil pour créer des applications Web dans le navigateur en discutant avec une IA.
- [Lovable](https://lovable.dev) pour construire des backends, notamment avec [Supabase](https://supabase.com)
- [Bolt](https://bolt.new) pour créer des sites web.