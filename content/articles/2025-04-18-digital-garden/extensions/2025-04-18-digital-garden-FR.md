---
date: 2025-04-18
image: digital-garden.jpg
excerpt: "J'ai lu à propos des jardins numériques et j'ai aimé l'idée. J'ai donc commencé à réfléchir à la manière dont je mettrais en place un tel jardin - et bien sûr, j'ai utilisé l'aide de l'IA..."
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:28:02.299784
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-04-18-digital-garden/2025-04-18-digital-garden.md
Generated-By: automatic-translation-plugin
---

![Jardin numérique](digital-garden.jpg)

[TOC]

J'ai lu à propos des Jardins Numériques sur [heise (en allemand)](https://www.heise.de/hintergrund/Nerd-Trend-Digitaler-Garten-Die-eigene-Website-als-persoenliches-Wissensarchiv-10344169.html) et j'ai vraiment aimé l'idée. Les principales différences avec mon blog actuel auxquelles j'ai pensé sont :

- L'idée de noter des idées et de commencer des articles immédiatement - et de les avoir dans le jardin immédiatement. C'est une grande différence par rapport à l'attitude de "Je dois finir l'article avant de le publier".
- L'idée de lier à d'autres articles et de créer un réseau d'articles. C'est quelque chose que je peux déjà faire dans mon blog, mais le processus est délicat : si je renomme ou déplace un article, les liens vers celui-ci sont cassés. De plus, l'idée de rétroliens est frappante.
- Mettre les sujets plus en avant plutôt que la date : Mon blog est principalement structuré et présenté par date. Avoir le(s) sujet(s) davantage comme structure de navigation semble attrayant. Bien sûr, je laisserais toujours la date de création, ainsi que la date de la dernière modification.

# Exigences

Comme d'habitude, j'ai tendance à commencer par regarder le côté technique 😀. J'ai donc noté mes exigences et demandé de l'aide à ChatGPT.

Mes exigences pour un système de jardin numérique :

- Les articles sont basés sur des fichiers markdown.
- Construit comme un site web généré statiquement.
- Un article dans un répertoire avec ses ressources : images, PDFs, autres fichiers. De cette façon, le rendu local par article a du sens, très utile lors de l'édition. J'éditerais les articles avec VScode ou un autre éditeur prenant en charge le markdown.
- Les articles (c'est-à-dire leurs répertoires) peuvent être dans une structure d'arborescence de répertoires. Leur structure de répertoire décrit la catégorie. Par exemple /tech/dev/data_science
- Écrit en Python, pour que je puisse bidouiller.
- Le pipeline de construction peut être complété : une étape pour vérifier les liens internes.
- Liens internes sous forme de _[ [liens] ]_. Et montrer les rétroliens dans les articles liés.
- Je veux créer facilement des types d'articles spécifiques avec une structure, des champs, un rendu spéciaux. Des exemples sont RECETTE, LIEU ou EMPLACEMENT, AVENTURE DE VOYAGE, …
- Beau site ! Pas comme un jardin désordonné et nerd ! S'inspirer de beaux blogs comme ghost.
- Multilingue, avec des langues remplies par l'IA si non fournies par l'auteur.
- Différents droits d'accès : certains contenus sont publics, d'autres pour la famille & les amis ou d'autres groupes d'utilisateurs.
- Rôles d'accès, par exemple : les articles non publiés ne peuvent être vus que par les utilisateurs avec le rôle ÉDITEUR.
- Permettre plusieurs pages d'index : tags, index historique (peut-être aussi par tag), les plus lus, les plus étoilés… Les pages d'index peuvent être générées mais aussi faites à la main. Spécifiquement la page d'accueil.

# Technologie et Architecture

[Ceci est ce que ChatGPT a produit](https://chatgpt.com/share/68026bb5-d040-8009-9f79-ec0fd35880f4) (Je pense que c'est vraiment bien, donc je le colle ici en entier) :

Parfait. Je vais explorer les meilleurs générateurs de sites statiques basés sur Python et l'architecture pour construire un jardin numérique magnifiquement stylé, piloté par markdown avec prise en charge du contrôle d'accès, de la vérification des liens internes, du support multilingue et de la personnalisation des types d'articles. Je m'assurerai également que le système prend en charge votre flux d'édition local préféré, génère du HTML simple et fonctionne bien avec GitHub Pages.

Je reviendrai vers vous avec une pile recommandée, un diagramme d'architecture et des suggestions sur la façon de mettre en œuvre vos exigences en douceur.

_Recherché pendant 11m 16s \* 23 sources_

# ChatGPT : Construire un Jardin Numérique Alimenté par Python : Pile & Architecture

## Générateur de Site Statique & Organisation du Contenu

Pour un **générateur de site statique basé sur Python**, **Pelican** est un excellent choix. Pelican est activement maintenu et bien documenté, prenant en charge le contenu Markdown et la publication multilingue par défaut ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). Il génère un site HTML simple (pas besoin de React/Vue) et dispose d'un riche écosystème de plugins pour étendre les fonctionnalités ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)).

**Structure du Contenu :** Organisez le contenu du jardin numérique dans une hiérarchie de répertoires logique sous le dossier `content/` de Pelican. Chaque article vit dans son propre sous-répertoire avec ses ressources. Par exemple :

```text
content/
├── tech/
│   └── dev/
│        └── data_science/
│             └── my-article/
│                  ├── index.md        # Article en Markdown
│                  ├── figure1.png     # Images/PDFs liés à l'article
│                  └── data.pdf
└── travel/
    └── trip-to-paris/
         ├── index.md
         └── eiffel.jpg
```

Dans cette disposition, chaque article (`index.md`) est regroupé avec ses médias. Pelican peut gérer des “bundles de pages” comme celui-ci en traitant ces sous-dossiers à la fois comme des chemins de contenu et statiques. Nous configurons les paramètres de Pelican pour inclure chaque dossier dans `ARTICLE_PATHS` et `STATIC_PATHS` afin que les fichiers markdown soient traités et que les ressources soient copiées dans la sortie ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,directory%20reserved%20for%20static%20files)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=generated%20site,in%20earlier%20versions%20of%20Pelican)). La **syntaxe d'attachement** de Pelican permet de lier facilement des fichiers locaux : en Markdown, utilisez `{attach}` pour référencer des fichiers dans le même dossier. Par exemple : `![Figure]({attach}figure1.png)` dans `my-article/index.md` copiera _figure1.png_ dans le répertoire de sortie de l'article et y fera un lien ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,sibling%20of%20the%20linking%20document)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Title%3A%20Test%20Post%20Category%3A%20test,31)). Cela permet de garder les images/PDFs co-localisés avec leur article et garantit que les liens ne sont pas cassés après la construction statique ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=output%20%E2%94%94%E2%94%80%E2%94%80%202014%20%E2%94%9C%E2%94%80%E2%94%80%20archive,post.html)).

Pelican prend également en charge l'utilisation des noms de dossiers comme catégories automatiquement. Par défaut, le dossier parent immédiat devient la catégorie (par exemple, “data_science” dans le chemin ci-dessus) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)). Nous pouvons préserver un emboîtement plus profond dans les URLs en personnalisant le chemin de sauvegarde. Par exemple, en définissant `ARTICLE_SAVE_AS = '{category}/{slug}/index.html'` et une `ARTICLE_URL` similaire, chaque article sera enregistré comme un `index.html` dans un dossier correspondant à sa catégorie/slug. Cela donne des URLs propres comme `/tech/dev/data_science/my-article/` reflétant la structure de répertoire. (Le `USE_FOLDER_AS_CATEGORY=True` par défaut de Pelican utilise le dossier le plus bas comme catégorie ; pour une taxonomie à plusieurs niveaux, on peut soit combiner le chemin en une catégorie, soit traiter les dossiers supérieurs comme sections et utiliser des tags pour la sous-classification.)

## Édition Markdown & Prévisualisation Locale

Tous les articles sont écrits en **Markdown** simple (avec front matter YAML/TOML pour les métadonnées) afin que vous puissiez rédiger confortablement le contenu dans VS Code ou tout autre éditeur. Chaque fichier Markdown commence par des métadonnées comme le titre, la date, les tags, etc. Pelican ne nécessite qu'un titre (il peut en dériver d'autres si nécessaire) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)), mais nous utiliserons les métadonnées de manière intensive pour un comportement personnalisé (nous en parlerons plus tard). Un exemple de front matter pour un article pourrait être :

```markdown
Title: Mon Voyage en Science des Données  
Date: 2025-04-10  
Category: data_science  
Tags: python, analytics  
Slug: mon-voyage-en-science-des-données  
Status: published
```

**Prévisualisation Locale :** Pour activer la prévisualisation par article lors de l'édition, utilisez le serveur de développement intégré de Pelican. Le CLI/Makefile de Pelican prend en charge un serveur à rechargement automatique (par exemple, `make devserver` ou `pelican --autoreload --listen`) qui surveille les changements de fichiers et reconstruit pendant que vous écrivez. De cette façon, vous pouvez naviguer vers `http://localhost:8000/tech/dev/data_science/my-article/` et voir le HTML rendu se mettre à jour à chaque sauvegarde. Parce que Pelican effectue une écriture de sortie sélective et une mise en cache, les reconstructions sont rapides même pour les grands sites ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). Cela donne une prévisualisation quasi en temps réel de l'article dans le contexte du thème/modèle réel. Pour une itération rapide sur une seule page, la construction incrémentielle de Pelican détectera seulement que _my-article_ a changé et régénérera juste cette page, rendant la boucle de rétroaction rapide. VS Code peut également prévisualiser le Markdown, mais utiliser le serveur de Pelican garantit que le contenu est vu avec le style et la mise en page du site final.

## Liens Internes de Style Wiki & Rétroliens

Pour interconnecter les notes à la manière d'un wiki, nous activons le **[[lien de style Wiki]]** en Markdown. Pelican a un plugin communautaire appelé **Wikilinks** qui convertit automatiquement la syntaxe `[[Nom de la Page]]` en hyperliens appropriés entre les pages ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). Par exemple, écrire `Nous construisons sur des idées de [[Mon Voyage en Science des Données]]` dans un autre article fera un lien vers la page “Mon Voyage en Science des Données” (résolvant vers son slug ou nom de fichier). Le plugin Wikilinks prend en charge le texte d'affichage optionnel (par exemple, `[[Nom de la Page|texte personnalisé]]`) ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). En coulisses, il scanne les motifs `[[...]]` après le traitement markdown et les remplace par des liens `<a>` vers l'URL de la page cible ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=In%20basic%20usage%2C%20this%20allow,is%20finished)). Cela rend le référencement croisé du contenu aussi facile que dans des outils comme Obsidian ou Roam. (Nous imposerons des noms de fichiers uniques pour les notes afin d'éviter les liens ambigus ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Known%20Issues)).)

**Rétroliens :** Pour obtenir un lien bidirectionnel (voir ce qui renvoie à une page), nous pouvons créer un plugin Pelican personnalisé ou utiliser les métadonnées du site. Pendant la construction, nous pouvons collecter toutes les références de liens wiki : par exemple, maintenir un dictionnaire mappant chaque page cible à une liste de pages qui l'ont mentionnée. Ensuite, étendre le contexte de l'article de Pelican pour inclure une liste de “rétroliens” pour chaque article. Enfin, dans le modèle d'article, si des rétroliens existent, rendre une section “**Lié depuis :** …” listant ces pages référentes. Cela nécessite un plugin personnalisé qui s'intègre dans la phase de génération de Pelican (en utilisant des signaux comme `article_generator_finalized`) pour rassembler les liens et injecter les données. L'effort est gérable étant donné l'API de plugin de Pelican (hooks Python), et garantit que chaque page se termine par une liste d'autres notes qui y renvoient, renforçant la navigation de type wiki. Si l'on écrit un plugin à partir de zéro, nous analyserions chaque HTML d'article (ou utiliserions la carte de liens internes du plugin Wikilinks) pour identifier les `href` sortants pointant à l'intérieur du site, puis inverser cette cartographie.

La syntaxe de lien standard de Pelican (`{filename}target.md`) pourrait également être utilisée pour les liens internes ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=the%20other%20content%20will%20be,placed%20after%20site%20generation)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=,filename%7D%2Farticle2.md)), mais le style wiki est plus intuitif pour un flux de travail de jardin numérique. Avec le plugin Wikilinks et un plugin de rétroliens, le site aura des **pages entièrement connectées** avec des références automatiques.

## Types de Contenu Personnalisés & Modèles

L'un des points forts de Pelican est sa flexibilité en matière de métadonnées et de modélisation, que nous exploitons pour définir des **types d'articles personnalisés** comme `RECETTE` ou `VOYAGE`. Tous les fichiers Markdown peuvent inclure des champs de front-matter arbitraires (tant qu'ils ne sont pas en conflit avec des mots-clés réservés) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=This%20is%20the%20content%20of,my%20super%20blog%20post)) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=,false)). Nous définissons un champ de métadonnées `Type` (ou utilisons un tag/catégorie) pour indiquer le type de contenu, et ajoutons les champs personnalisés nécessaires. Par exemple, une recette pourrait avoir :

```markdown
Title: Cookies aux Pépites de Chocolat  
Date: 2025-03-01  
Type: recette  
Portions: 4  
Temps_Préparation: 15 min  
Temps_Cuisson: 10 min  
Ingrédients:

- Farine
- Sucre
- Pépites de chocolat
  Étapes:

1. Préchauffer le four…
2. Mélanger les ingrédients…  
   Template: recette <!-- utiliser un modèle Jinja personnalisé -->