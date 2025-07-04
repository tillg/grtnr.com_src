---
title: Autocomplétion de mon Blog
tags: blog, tech, logicielquenousavonsbesoin
summary: J'ai maintenant un blog basé sur Pelican et je veux ajouter ou corriger du contenu automatiquement : balises d'images, résumés d'articles, traductions... Enfin une façon d'utiliser l'IA 🤖
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:42:01.956568
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-04-autocompleting-my-blog/2025-05-04-autocompleting-my-blog.md
Generated-By: automatic-translation-plugin
---

[TOC]

Depuis la semaine dernière, mon blog est basé sur [Pelican](https://getpelican.com), le générateur de blogs statiques basé sur Python. Maintenant que le blog est construit dans un langage que je maîtrise plus ou moins, je peux penser à améliorer le processus d'écriture et de construction moi-même. Et bien sûr, il y a beaucoup d'outils auxquels je peux penser pour faciliter ma vie ainsi que celle de mes lecteurs. Voici donc quelques exemples de ces aides.

## Outils que j'aimerais avoir

### Complétion de balise d'image (IA)

Chaque fois que j'ajoute une image sans un texte alternatif, c'est mauvais pour les personnes aveugles. Mais je suis paresseux, alors pourquoi ne pas laisser une IA décrire l'image et l'ajouter comme texte ALT ?

### Vérificateur de liens

J'ai beaucoup de liens pointant vers des emplacements externes. Et parfois, des pages web disparaissent, donc mes liens pourraient pointer vers le Nirvana. Ce serait bien si

- mon utilisateur n'avait pas à cliquer sur des liens brisés
- je recevais un conseil que je dois réparer un lien ou un autre
- je pourrais peut-être prévenir la situation en gardant une copie de la page vers laquelle je fais un lien dans mon propre blog. Ou est-ce du scraping malveillant et du vol de contenu ?

### Générateur d'extraits (IA)

Je rédige souvent des articles sans spécifier le résumé / extrait qui est affiché dans la liste des articles. Par défaut, Pelican (et d'autres générateurs statiques) prend le premier paragraphe ou les 30 premiers mots et l'utilise comme extrait.

Ne serait-il pas beaucoup plus agréable de demander à un LLM de générer un résumé raisonnable de 3 lignes ?

### Traducteur (IA'ish)

Dans mon blog, j'écris parfois des articles en anglais, parfois en allemand. Peut-être y a-t-il même un article en français ici et là. Ne serait-il pas agréable d'avoir chaque article dans chaque langue ? Il semble qu'aujourd'hui cela devrait être une norme, étant donné la bonne qualité des outils de traduction actuels.

Donc, j'écris mes articles dans la langue qui me vient à l'esprit, et le système devrait générer les langues manquantes.

### Illustration d'article (IA)

J'essaie d'avoir des images pour la plupart de mes articles, car c'est simplement une expérience de lecture plus agréable et agréable pour les yeux. Je trouve souvent quelque chose sur internet, mais pas toujours - aussi parce que je ne prends parfois même pas la peine de chercher une image. Mais l'IA pourrait chercher, ou même générer une belle image pour mes articles _nus_.

## Nous avons besoin d'un pipeline de construction

Pour obtenir ces choses construites, j'ai l'impression d'avoir besoin de quelque chose comme un _Pipeline de Construction_ :

![Pipeline de Construction](https://insights.mgm-tp.com/wp-content/uploads/2023/08/mgm-CI-CD-Pipeline.png)
_Un pipeline de construction CI/CD moderne, pris de [mgm technology partners](https://mgm-tp.com)_

Quelques réflexions sur la structure, le traitement et l'organisation des données.

### Données intérimaires

Ce que fait Pelican, c'est de prendre la source des articles, avec la configuration et de générer les pages web. Il le fait par son traitement standard et par des plugins potentiels. Les plugins peuvent être de tiers ou développés par moi-même. Dans mon cas, j'ai les deux.

Beaucoup des outils que j'envisage créent des données supplémentaires, et souvent la création est coûteuse et prend du temps. Pensez à créer un extrait d'un article : tout le texte doit être envoyé à une IA et traité. Cela prend plusieurs secondes et coûte de l'argent réel. Par conséquent, ce n'est certainement pas quelque chose que nous voulons exécuter à chaque construction. Nous devrons donc conserver les données entre les différentes exécutions de construction.

### Intégrité du contenu rédigé

Une façon dont nous pourrions penser à résoudre cela, c'est d'ajouter simplement l'extrait généré par l'IA au markdown original (dans ce cas, il irait dans la matière frontale comme champ `summary`).

Mais je n'aime pas du tout cela : je ne veux pas que l'IA s'immisce dans le texte et le contenu que j'ai personnellement élaborés. Par conséquent, je veux définir la règle suivante pour mon système :

**Mes fichiers Markdown rédigés ne doivent jamais être modifiés par des outils automatisés.**

### Où conserver les données

Cela me laisse avec la question de savoir où conserver les données comme les résumés générés par l'IA. L'endroit naturel est de les conserver à côté des fichiers markdown, mais dans leur propre fichier. Comme j'ai des répertoires séparés pour chacun de mes articles, je finis par avoir cette forme de répertoires et de fichiers :

```file
content
    articles
    ...
    2025-04-18-jardin-numerique
        2025-04-18-jardin-numerique.md
        2025-04-18-jardin-numerique.picture-tags.json
        2025-04-18-jardin-numerique.summary.json
        jardin-numerique.jpg
```

Quelques réflexions et arguments pour cette structure :

- Chaque outil a son propre fichier pour garder les choses séparées.
- J'utilise des fichiers JSON : Faciles à traiter et à lire.
- Les fichiers sont à côté de l'article original, donc tout ce qui est lié est à proximité et _encapsulé_.
- Les fichiers JSON sont également contrôlés par version et stockés dans Git, donc que je lance le processus de construction sur ma machine de développement locale ou à l'intérieur des Actions Github ou d'un autre processeur CI/CD, il réutilise les données précédemment générées.

### Ordre de traitement

Cette disposition des données nécessite un processus de construction en plusieurs étapes :

1. **Créer des données supplémentaires :** générer les résumés, les descriptions d'images, les images, vérifier les liens (et stocker le résultat de ces vérifications)... Cette partie du processus est potentiellement longue, génère beaucoup de données supplémentaires et nécessite des mécanismes de mise en cache intelligents et de validation du cache. Par exemple, "Comment vérifier si je dois recréer le résumé d'un article ou si je peux utiliser celui qui se trouve dans le fichier JSON à côté de l'article markdown ?".
2. **Construire le site :** Il s'agit du processus de création de base de Pelican tel que nous le connaissons, à l'exception qu'il doit également _intégrer_ les données supplémentaires qui sont maintenant dans les fichiers JSON. Je le ferai avec un ou plusieurs plugins Pelican que je développerai.