---
layout: post
title: Mon site web statique
date_published: 2016-08-08T00:00:00.000Z
image: static_site.jpg
tags: Tech
excerpt: Les sites web statiques deviennent la norme de nos jours. J'ai donc également examiné cela et comparé certains générateurs de sites web.
translation: fr
source_language: en
source_hash: abc8f2afa5ca8b18bbd09e77e2d20b6bcbaf8353c5a215dd2435191f52cbc396
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:24:49.597068
generated_by: simplified-translation-system
---

D'accord, tout le monde le fait, moi aussi : les sites web statiques. C'est rapide, c'est sûr, cela effectue le calcul là où il doit être fait (tant que vous n'avez pas besoin de personnalisation sophistiquée, pourquoi un serveur devrait-il réfléchir à l'apparence de la page au moment de la lecture ?). Ce site même est statique (construit avec [JBake](http://jbake.org/) et hébergé sur [Github](https://github.com/)). C'était amusant de le mettre en place, ça fonctionne très bien - mais je ne pourrais pas expliquer à ma mère comment l'utiliser ou comment publier du contenu dessus. Et c'est ce qu'un CMS devrait être : il doit être utilisable en premier lieu.

Par conséquent, j'ai besoin d'une autre configuration. Je prévois d'examiner différents systèmes de sites web statiques et de dresser une liste de critères selon lesquels je prévois de tester les différents générateurs...

## Critères

- Thèmes
  - Nombreux
  - Beaux
  - Responsifs

- Facile à écrire
  - Éditeur avec aperçu
  - Gestion facile et référencement des images
  - Images dans l'aperçu
  - Vidéos
  - Tableaux
  - Code avec surlignage syntaxique
  - Vérification automatique de la cohérence, c'est-à-dire que le site web généré est correct, complet, les pointeurs ne pointent pas vers le Nirvana...

- Capable de créer une [Page Mobile Accélérée](https://www.ampproject.org/)
- Fonctionnalités et pages fonctionnelles
  - Tags, pages de tags, nuage de tags (pourrait aussi être une extension)
  - Publier sur Github (c'est très rapide, gratuit et fiable)
  - Rendre le site privé, c'est-à-dire accessible uniquement aux membres enregistrés
  - Publier par email
  - Commenter par email
  - Envoyer des nouvelles aux utilisateurs enregistrés par email
  - Redimensionner les images pour une livraison rapide
  - Facile à créer de nouveaux thèmes, les thèmes devraient être juste du CSS
  - Basé sur d'autres HTML, c'est-à-dire des thèmes Bootstrap

- Architecture extensible
  - Peut ajouter des éléments, c'est-à-dire processus de redimensionnement d'image
  - Au moins un langage de programmation que je connais un peu - ou que je suis curieux d'apprendre (cela se résume essentiellement à Java et JavaScript)
  - Le HTML généré doit être aussi simple que possible. Toute la mise en forme se trouve dans le CSS

## Générateurs

En parcourant la littérature (et Github), voici la liste des générateurs que je devrais probablement examiner :

- Jekyll - Fait
- Harp JS - Fait
- Hugo - Fait
- Metalsmith - Fait
- Nikola - Fait
- Octopress - Fait
- Hexo - Fait
- Hyde - Fait
- Pelican - Fait
- Nanoc - Fait
- Middleman - Fait
- Lektor - Fait
- Gatsby - Fait
- Expose - Fait
- Wintersmith - Fait
- Doc pad - Fait
- kirby - Fait

## Matrice d'évaluation

| Générateur                                    | Langage de programmation | Thèmes    | Formats                                        | Commentaire                                                                                                           |
| :-------------------------------------------- | :----------------------- | :-------- | :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| [Jekyll](https://jekyllrb.com/)               | Ruby --                  | Beaucoup ++ | Markdown, Textile, Liquid ++                   |                                                                                                                       |
| _[Harp JS](https://harpjs.com/)_              | NodeJS ++                | Quelques 00 | Markdown, EJS, Jade, LESS, Stylus... ++        |                                                                                                                       |
| [Hugo](https://gohugo.io/)                    | GO --                    | Quelques 00 | Markdown, asciidoc, reStructure ++             |                                                                                                                       |
| _[Metalsmith](http://www.metalsmith.io/)_     | Node JS --               |           |                                                | Semble très flexible. Voir aussi http://dbushell.com/2015/05/11/wordpress-to-metalsmith/                              |
| [Nikola](https://getnikola.com/)              | Python --                | Peu --    | reStructuredText, Markdown,                    | Semble juste moyen...                                                                                                 |
| [Octopress](http://octopress.org/)            | Python --                | Quelques 00 |                                                | N'est qu'un package autour de Jekyll.                                                                                 |
| _[Hexo](https://hexo.io/)_                    | Node JS ++               | Quelques 00 | Markdown, différentes saveurs, Plugins Jekyll ++ | Semble très flexible, utilise des moteurs de template standard (EJS, Jade, Swig...), permet d'intégrer des scripts et des plugins. ++ |
| [Hyde](http://hyde.github.io/)                | Python --                | Peu --    |                                                |                                                                                                                       |
| [Pelican](http://blog.getpelican.com/)        | Python --                |           |                                                |                                                                                                                       |
| [Nanoc](http://nanoc.ws/)                     | Ruby --                  |           |                                                |                                                                                                                       |
| [Middleman](https://middlemanapp.com/)        | Python --                |           |                                                |                                                                                                                       |
| [Lektor](https://www.getlektor.com/)          | Python --                |           |                                                |                                                                                                                       |
| [Gatsby](https://github.com/gatsbyjs/gatsby)  | Node JS, React           | Non --    | Markdown 00                                    | Semble très flexible, mais assez complexe...                                                                          |
| [Expose](https://github.com/Jack000/Expose)   | Scripts Shell --         |           | Dossiers Markdown et images                    | Spécifiquement pour les sites d'images.                                                                               |
| _[Wintersmith](http://wintersmith.io/)_       | Node JS, CoffeeScript ++ | Peu --    | Markdown, Jade, ...                            | Semble très flexible, LESS, Sass, Stylus. Pourrait être un peu complexe...                                            |
| [DocPad](http://docpad.org/)                  | Node JS ++               | Non --    | Markdown et autres ++                          | Semble flexible mais complexe                                                                                         |
| [kirby](https://getkirby.com/)                | PHP --                   |           | Markdown                                       |                                                                                                                       |

En conséquence, je devrais examiner de plus près _[Harp JS](https://harpjs.com/)_, _[Metalsmith](http://www.metalsmith.io/)_, _[Hexo](https://hexo.io/)_ et _[Wintersmith](http://wintersmith.io/)_.

Après avoir rapidement parcouru les sites web des outils ci-dessus, j'ai décidé d'essayer avec _[Metalsmith](http://www.metalsmith.io/)_.

## Éditeurs

Lorsque vous pensez à la génération d'un site statique à partir d'une base de fichiers Markdown, il devient rapidement naturel de chercher un bon éditeur. Ce que nous attendons de notre éditeur :

- Aperçu Markdown
- Aperçu incluant le CSS et les autres transformations que notre générateur de site utilise - pour s'assurer que nous voyons le même résultat que celui qui sera affiché en production
- Aperçu incluant les images. Cela pourrait être non trivial puisque les images pourraient être situées sur un chemin différent en DEV qu'en PROD...
  Dans l'ensemble, cela signifie que l'éditeur doit lancer un processus de compilation / composition qui produit la vue web chaque fois que la source Markdown a été modifiée.

Éditeur que nous examinons

| Éditeur                             | Aperçu Markdown / HTML | Commentaires                   |
| :---------------------------------- | :--------------------- | :----------------------------- |
| Visual Code                         | ?                      | Pourrait avoir quelque chose de convenable |
| Atom                                |                        |                                |
| Brackets                            |                        |                                |
| [Caret.io](https://caret.io/)       |                        |                                |
| [IA Writer](https://ia.net/writer)  | Le prétend...          |                                |

... probablement quelques autres...

# Historique

- Août 2016 : Début de cette page
- Jan 2017 : Continué pendant un séjour en Thaïlande avec la famille, Tomi & Beate