---
title: Autocomplétion de mon Blog
tags: blog, tech, logicielsdontnousavonsbesoin
summary: J'ai maintenant un blog basé sur Pelican et je veux ajouter ou corriger automatiquement du contenu : Balises d'image, résumés d'articles, traductions... Enfin un moyen d'utiliser l'IA 🤖
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:11:56.844863
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-04-autocompleting-my-blog/2025-05-04-autocompleting-my-blog.md
Generated-By: automatic-translation-plugin
---

[TOC]

Depuis la semaine dernière, mon blog est basé sur [Pelican](https://getpelican.com), le générateur de blog statique basé sur Python. Maintenant que le blog est construit dans un langage que je maîtrise plus ou moins, je peux envisager d'améliorer le processus d'écriture et de construction par moi-même. Et bien sûr, il y a beaucoup d'outils auxquels je peux penser pour faciliter ma vie ainsi que celle de mes lecteurs. Voici donc quelques exemples de ces assistants.

## Outils que j'aimerais avoir

### Complétion des balises d'image (IA)

Chaque fois que j'ajoute une image sans texte alternatif, c'est mauvais pour les personnes malvoyantes. Mais je suis paresseux, alors pourquoi ne pas laisser une IA décrire l'image et l'ajouter comme texte ALT ?

### Vérificateur de liens

J'ai de nombreux liens pointant vers des emplacements externes. Et parfois, des pages web disparaissent, donc mes liens pourraient pointer vers le Nirvana. Ce serait bien si

- mon utilisateur n'avait pas à cliquer sur des liens cassés
- je recevais un conseil que je dois corriger un lien ou un autre
- je pouvais peut-être prévenir la situation en gardant une copie de la page vers laquelle je fais un lien dans mon propre blog. Ou est-ce du scraping malveillant et du vol de contenu ?

### Générateur d'extraits (IA)

Je rédige souvent des articles sans spécifier le résumé / extrait qui est affiché dans la liste des articles. Par défaut, Pelican (et d'autres générateurs statiques) prend le premier paragraphe ou les 30 premiers mots et l'utilise comme extrait.

Ne serait-il pas beaucoup plus agréable de demander à un LLM de générer un résumé raisonnable de 3 lignes ?

### Traducteur (IA-ish)

Dans mon blog, j'écris parfois des articles en anglais, parfois en allemand. Peut-être y a-t-il même un article en français ici et là. Ne serait-il pas agréable d'avoir chaque article dans chaque langue ? Il semble qu'aujourd'hui cela devrait être une norme, étant donné la bonne qualité des outils de traduction actuels.

Donc j'écris mes articles dans n'importe quelle langue qui sort de mon petit cerveau, et le système devrait générer les langues manquantes.

### Illustration d'article (IA)

J'essaie d'avoir des images pour la plupart de mes articles, car c'est tout simplement une expérience de lecture plus agréable et plaisante pour l'œil. Je trouve souvent quelque chose sur Internet, mais pas toujours - aussi parce que parfois je ne prends même pas la peine de chercher une image. Mais l'IA pourrait chercher, ou même générer une belle image pour mes articles _nus_.

## Nous avons besoin d'une chaîne de construction

Pour réaliser ces choses, je sens que j'ai besoin de quelque chose comme une _chaîne de construction_ :

![Chaîne de Construction](https://insights.mgm-tp.com/wp-content/uploads/2023/08/mgm-CI-CD-Pipeline.png)
_Une chaîne de construction CI/CD moderne, prise de [mgm technology partners](https://mgm-tp.com)_

Quelques réflexions sur la structure, le traitement et comment organiser les données.

### Données intermédiaires

Ce que fait Pelican, c'est prendre la source des articles, avec la configuration, et générer les pages web. Il le fait par son traitement standard et par des plugins potentiels. Les plugins peuvent être tiers ou développés en interne. Dans mon cas, j'ai les deux.

Beaucoup des outils que j'envisage créent des données supplémentaires, et souvent la création est coûteuse et chronophage. Pensez à créer un extrait d'un article : Le texte entier doit être envoyé à une IA et traité. Cela prend plusieurs secondes et coûte de l'argent réel. Par conséquent, ce n'est certainement pas quelque chose que nous voulons exécuter à chaque construction. Nous devrons donc conserver les données entre les différentes exécutions de construction.

### Intégrité du contenu rédigé

Une façon de résoudre ce problème pourrait être d'ajouter simplement l'extrait généré par l'IA au markdown original (dans ce cas, il irait dans le front matter en tant que champ `summary`).

Mais je n'aime pas ça du tout : Je ne veux pas que l'IA interfère avec le texte et le contenu que j'ai personnellement élaborés. Par conséquent, je veux définir la règle suivante pour mon système :

**Mes fichiers Markdown rédigés ne doivent jamais être modifiés par des outils automatisés.**

### Où conserver les données

Cela me laisse avec la question de savoir où conserver les données comme les résumés générés par l'IA. L'endroit naturel est de les garder à côté des fichiers markdown, mais dans leur propre fichier. Comme j'ai des répertoires séparés pour chacun de mes articles, je me retrouve avec cette structure de répertoires et de fichiers :

```file
content
    articles
    ...
    2025-04-18-digital-garden
        2025-04-18-digital-garden.md
        2025-04-18-digital-garden.picture-tags.json
        2025-04-18-digital-garden.summary.json
        digital-garden.jpg
```

Quelques réflexions et arguments pour cette structure :

- Chaque outil a son propre fichier pour garder les choses séparées.
- J'utilise des fichiers JSON : Faciles à traiter et à lire.
- Les fichiers sont à côté de l'article original, donc tout ce qui est lié est proche et _encapsulé_.
- Les fichiers JSON sont également contrôlés par version et stockés dans Git, donc que j'exécute le processus de construction sur ma machine de développement locale ou à l'intérieur de Github Actions ou un autre processeur CI/CD, il réutilise les données précédemment générées.

### Ordre de traitement

Cette disposition des données nécessite un processus de construction en plusieurs étapes :

1. **Créer des données supplémentaires :** générer les résumés, les descriptions d'images, les images, vérifier les liens (et stocker le résultat de ces vérifications)... Cette partie du processus est potentiellement chronophage, génère beaucoup de données supplémentaires et nécessite des mécanismes de mise en cache et de validation de cache intelligents. Par exemple, "Comment vérifier si je dois recréer le résumé d'un article ou si je peux utiliser celui du fichier JSON à côté de l'article markdown ?".
2. **Construire le site :** C'est le processus de création de base de Pelican tel que nous le connaissons, sauf qu'il doit également _intégrer_ les données supplémentaires qui sont maintenant dans les fichiers JSON. Je ferai cela avec un ou plusieurs plugins Pelican que je développerai.