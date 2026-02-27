---
date: 2015-11-30
image: github.png
excerpt: Comment j'ai configuré mon blog en utilisant JBake comme générateur de site statique et GitHub Pages pour l'hébergement.
title: Comment j'ai migré vers GitHub & JBake
tags: tech, webSite
translation: fr
source_language: en
source_hash: 390e4b560ef27f0c86fd9724582e98d9a83910759c6d7fd671eb722749d2bc0d
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:00:30.961306+00:00
generated_by: simplified-translation-system
---

**\*** Cette page est ~~en construction~~ inachevée... **\***

D'abord : Ce n'est pas mon invention ! Beaucoup l'ont fait avant moi, il y a de nombreuses descriptions disponibles. Cela m'a tout de même pris un certain temps ;)

[Ceci](http://alexcican.com/post/guide-hosting-website-dropbox-github/) et [cela](http://alexcican.com/post/blog-dropbox-scriptogram) ont été les sources les plus inspirantes et les explications les plus simples (qui donnent confiance ;) ).

# Configuration

Voici donc la configuration générale que j'ai :

- Un répertoire sur mon Mac qui contient le contenu. J'utilise la structure de base que [Jbake](http://jbake.org) utilise.
- Un répertoire cloné par git sur mon Mac avec le résultat du processus jBake
- Un petit script que je lance chaque fois que je modifie quelque chose. Le script effectue la génération et la publication sur git
- Et bien sûr, les paramètres DNS pour pointer mon nom de domaine vers les IPs de Github

## JBake

Pourquoi j'utilise JBake ? J'aime le principe et je me sens plus à l'aise en Java que dans d'autres langages de programmation. Je n'ai pas touché au code interne de JBake, mais je suis confiant que je pourrais le faire.
Le principe de fonctionnement de JBake est similaire au célèbre [Jekyll](https://jekyllrb.com/) : il analyse les fichiers de contenu et crée des fichiers HTML (statiques) à partir de ceux-ci. Les fichiers de contenu peuvent contenir du Markdown ou d'autres formats ; j'utilise simplement Markdown.

Ma structure de répertoire ressemble à ceci :

```text
.
|-- assets
|   |-- favicon.gif
|   |-- robots.txt
|   |-- img
|   |   |-- logo.png
|   |-- js
|   |   |-- custom.js
|   |-- css
|       |-- style.css
|
|-- content
|   |-- about.html
|   |-- 2013
|       |-- 01
|       |   |-- hello-world.html
|       |-- 02
|           |-- weekly-links-1.ad
|           |-- weekly-links-2.md
|
|-- templates
|   |-- index.ftl
|   |-- page.ftl
|   |-- post.ftl
|   |-- feed.ftl
|
|-- jbake.properties
```

Par défaut, JBake produit le répertoire de sortie dans cet arbre. Dans mon cas, je génère mes fichiers dans un répertoire synchronisé par git.

## La configuration GitHub

## Les paramètres DNS

# Prochaines étapes

Il y a quelques éléments que je prévois de changer.