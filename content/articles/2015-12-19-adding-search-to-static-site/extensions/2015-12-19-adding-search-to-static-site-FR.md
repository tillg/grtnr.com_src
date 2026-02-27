---
date: 2015-12-19
image: search.jpg
excerpt: Comment ajouter une fonctionnalité de recherche à un site statique en utilisant Google Custom Search Engine et une barre de navigation Bootstrap.
title: Ajouter une recherche à un site statique
translation: fr
source_language: en
source_hash: aebd3204dffe603f26df3504a07cc2c5c408ca3517c4e1c4e8b36207f8aa6cef
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:01:30.085862+00:00
generated_by: simplified-translation-system
---

J'ai maintenant un site statique généré par jBake. Jusqu'ici tout va bien. Mais qu'est-ce qu'un site sans recherche ? La recherche est indispensable. Alors, comment ajouter une fonctionnalité de recherche à un site statique ? Facile : Nous utilisons la fonctionnalité Custom Search des géants de la recherche ;)

Voici les étapes que j'ai suivies pour y parvenir :

## Créer le moteur de recherche personnalisé

Rien de plus simple : Il suffit d'aller sur la [page Google CSE](http://www.google.com/cse) et de le créer. Le processus est explicite : Vous avez besoin d'un nom pour votre moteur de recherche, vous indiquez quel contenu doit être rendu disponible. Dans mon cas, ce serait tout le contenu de [tillgartner.com](https://tillgartner.com) et c'est à peu près tout. Nous reviendrons à la fin sur ce site afin d'affiner l'apparence des résultats.

![Administration Google CSE](Custom_Search_-_Basic.jpg)

La seule chose dont nous avons besoin ici est le code pour intégrer la recherche. Vous obtenez ce code en cliquant sur le bouton "**Get Code**".

## Ajouter le champ de recherche

Ensuite, nous avons besoin d'une boîte de recherche sur nos pages. Je veux une boîte de recherche en haut à droite de chaque page de l'ensemble du site. Je l'ajoute donc au modèle Freemarker qui crée le menu.

Dans mon cas, le `menu.ftl` ressemble à ceci :

```javascript
    <!-- Barre de navigation fixe -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Basculer la navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
          <a class="navbar-brand" href="/">tillgartner.com</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="/recipe/recipe.html">Recettes</a></li>
            <li><a href="/about.html">À propos</a></li>
          </ul>
          <div class="col-sm-3 col-md-3 pull-right">
              <form class="navbar-form" role="search" action="/search.html">
            <div class="input-group">
                <input type="text" class="form-control" placeholder="Rechercher" name="q">
                <div class="input-group-btn">
                    <button class="btn btn-default" type="submit">
                        <i class="glyphicon glyphicon-search"></i>
                    </button>
                </div>
            </div>
         </form>
         </div>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    <div class="container">
```

_Remarque :_ J'ai corrigé le code sur mon site et dans le code ci-dessus le 29.12.2015. Le code pour le bouton qui apparaît lorsque la largeur de l'écran fait s'effondrer le menu manquait. Juste au cas où vous auriez lu ceci plus tôt et vous vous demanderiez pourquoi c'est différent maintenant...

J'ai trouvé que la partie du menu et comment elle s'effondre n'était pas triviale. La meilleure explication que j'ai trouvée était [cette vidéo](https://bootstrapbay.com/blog/bootstrap-tutorial-navbar/).

C'est le menu standard de Bootstrap. Ce qui est spécial dans notre cas, c'est l'attribut `action` dans le formulaire qui lie à la page de résultats de recherche (appelée `search.html` dans mon cas).

Le résultat est une petite boîte de recherche en haut à droite :

![Boîte de recherche](search_box.jpg)

## Page de résultats de recherche

Enfin, nous avons besoin de la page de résultats de recherche. Cette page sera appelée (c'est-à-dire liée) à partir du formulaire de recherche que nous venons de créer. Son URL sera quelque chose comme

```url
http://tillgartner.com/search.html?q=huhu
```

Dans mon cas, la page de résultats de recherche ne contiendra **que** le résultat de la recherche. Si l'utilisateur souhaite modifier sa recherche, il a toujours la boîte de recherche omniprésente en haut à droite.
La page de résultats de recherche contiendra le code que nous avons copié lors de la configuration du moteur de recherche personnalisé. Dans mon cas, l'ensemble du fichier Markdown ressemble à ceci :

```javascript
title=Search
type=page
date=2015-12-17
status=published
~~~~~~

<script>
  (function() {
    var cx = 'XXX_Your_code:goes_here_XXX';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
</script>
<div markdown = "0"><gcse:searchresults-only>Résultats de recherche...</gcse:searchresults-only></div>
```

Il m'a fallu un certain temps pour comprendre comment dire à markdown que c'est du pur HTML et qu'il doit le prendre tel quel sans le transformer ni le citer. La solution était la balise `<div markdown="0">`.

## Ressources

Quelques lectures qui m'ont aidé à trouver mon chemin :

- [Créez votre propre moteur de recherche](http://www.google.com/cse)
- [Comment intégrer une fenêtre contextuelle de recherche personnalisée Google dans une barre de navigation Bootstrap](http://www.cambiaresearch.com/articles/84/how-to-integrate-a-google-custom-search-popup-in-a-bootstrap-navbar)
- [Implémentation de la boîte de recherche, par Google](https://developers.google.com/custom-search/docs/tutorial/implementingsearchbox)