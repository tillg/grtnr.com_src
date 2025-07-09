---
date: 2025-02-11
image: screenshot_comment.jpg
excerpt: J'ai ajouté des commentaires à mon site web statique. Voici comment j'ai procédé.
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:25:29.205889
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-02-11-solid-comments-in-static-website/2025-02-11-solid-comments-in-static-website.md
Generated-By: automatic-translation-plugin
---

**TL;DR :** J'ai ajouté des commentaires à mon site web statique. Voici comment j'ai procédé - y compris quelques détails techniques. J'ai recherché parmi différentes solutions possibles pour trouver la plus solide, je l'ai intégrée à tous les articles et j'ai ajouté un compteur du nombre de commentaires dans la page de vue d'ensemble des articles.

**Mise à jour du 2025-05-23** Depuis que je suis passé de Jekyll à [Pelican](https://getpelican.com), j'ai mis à jour certains détails.

## Sélection d'une solution

Comme je prévoyais d'expérimenter le nouveau [Modèle de Recherche Approfondie d'OpenAI](https://openai.com/index/introducing-deep-research/), je l'ai testé sur ce sujet : [n'hésitez pas à lire ici](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776). Globalement, la recherche a été utile et j'ai fini par utiliser [Giscus](https://giscus.app/) pour les commentaires. En partie parce que cela semblait le plus robuste et fiable, en partie parce que j'avais eu une très mauvaise expérience avec Disqus il y a quelques années.

Le choix était basé sur l'ensemble de critères que j'ai donné au modèle. Voici les plus importants :

- Pas de serveur auto-hébergé – Je ne veux pas gérer (et payer 😉) un serveur.
- Portabilité des données – les commentaires peuvent être exportés.
- Respect de la vie privée – pas de traqueurs ou de publicités supplémentaires au-delà de ce que j'utilise déjà (par exemple, Google Analytics).
- Support Markdown – permet une mise en forme riche (blocs de code, etc.) adaptée aux discussions techniques.
- Protection contre le spam – dispose de mesures pour réduire le spam, surtout si l'on autorise des commentaires anonymes ou non authentifiés.

Les outils que Deep Research a _analysés_ étaient

- Giscus
- Utterances
- Staticman
- Commento
- Hyvor Talk
- Disqus
- Quelques solutions _faites maison_

## Intégration de Giscus

Suite à sa recherche, j'ai demandé au modèle de me fournir un guide étape par étape sur la façon d'intégrer la solution. Cela s'est avéré moins fiable que la première recherche, mais néanmoins utile.

Voici le résumé exécutif (les détails sont dans le [chat que j'ai eu avec l'IA](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776)) :

- Étape 1 : Activer GitHub Discussions pour votre dépôt. Cela signifie le dépôt dans lequel le site statique est généré (qui parfois n'est pas le même que la source).
  - Allez dans votre dépôt GitHub
  - Naviguez vers Paramètres > Général.
  - Faites défiler jusqu'à la section Discussions et activez-la.
- Étape intermédiaire, que l'IA a omis de mentionner : Installer giscus pour tous ou certains de vos dépôts. [Ici](https://github.com/apps/giscus/installations/select_target)
  ![texte alternatif](image.png)
- Étape 2 : Installer Giscus et le configurer
  - Visitez la page de configuration de Giscus : https://giscus.app/.
  - Sous "Repository", entrez le nom de votre dépôt. Vous devriez maintenant voir la coche verte indiquant que votre dépôt répond à tous les critères pour utiliser giscus.
  - L'option “Page discussion mapping” dicte une relation entre vos pages, par exemple un article, et une discussion GitHub. J'ai sélectionné le chemin d'accès.
  - Pour la catégorie de discussions, j'ai sélectionné “général”.
    Définissez le thème sur "Match OS" ou définissez manuellement le mode clair et sombre.
    Cliquez sur "Copier le code" une fois que vous avez généré la balise <script>.

![Fonctionnalités de Giscus](giscus-features.png)

- Étape 3 : Ajouter Giscus à votre modèle de post Jekyll (ou Pelican 😀). - Étape 4 : Styliser Giscus pour correspondre au thème Lanyon. J'ai sauté cette étape, car le style me semblait déjà assez bon _nu_.
- Étape 5 : Afficher le nombre de commentaires dans les résumés des articles (voir ci-dessous)
- Étape 6 : Valider et pousser les modifications - Évidemment...
- Étape 7 : Tester votre configuration

## Ajout du compteur de commentaires

Après quelques ajustements et lissage des bords, tout fonctionnait bien. Mais il y avait une fonctionnalité qui me manquait : je voulais voir le nombre de commentaires qu'un article de blog avait dans la page de vue d'ensemble des articles.

![Compteur de commentaires](screenshot_comment_counter.jpg){: style="box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);"}

J'ai donc relancé ChatGPT et obtenu un autre [résultat de recherche](https://chatgpt.com/share/67ab5f69-4ddc-8009-8471-a35e00cb6a43). Les grandes étapes sont :

- Étape 1 : Ajouter un espace réservé pour le compteur de commentaires. Dans mon [`post_preview.html`](https://github.com/tillg/grtnr.com_2024/blob/main/_includes/post_preview.html), j'ai ajouté un `<span>` qui devait en fait être un peu différent de ce que l'IA avait suggéré :

  ```html
  <span class="comment-count" data-giscus-comments="{{ post.url }}">
    <span class="comment-num">Comptage des commentaires...</span>
  </span>
  ```

- Étape 2 : Ajouter du JavaScript pour récupérer le compteur de commentaires. J'ai ajouté un script qui récupère le compteur de commentaires de l'API GitHub Discussions et met à jour le compteur de commentaires. Le script suggéré nécessitait quelques corrections et a fini dans cet [Event Listener](https://github.com/tillg/grtnr.com_2024/blob/main/assets/js/giscus-comments.js). Ne soyez pas surpris par les deux lignes avec des tirets (---) en haut, je les expliquerai ci-dessous... À noter ici :
  - Gestion du `accessToken` (expliqué ci-dessous)
  - Cet argument de la requête grahQL : `categoryId: "DIC_kwDONYRp_c4Cm0cH"`. C'est l'ID de la catégorie qui contient les discussions du dépôt.
  - Remarque : Ce qui m'a aidé pour déboguer et corriger cette fonction est le [Github GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer).
- Étape 3 : Inclure le JavaScript dans votre site Jekyll. Dans mon cas, j'ai ajouté cette référence de script au bas du fichier de mise en page [`default.html`](https://github.com/tillg/grtnr.com_2024/blob/main/_layouts/default.html).
- Étape 4 : Tester le compteur de commentaires. Après quelques tests et corrections, cela a finalement fonctionné localement.

Les aspects suivants m'ont occupé une heure ou deux :

- Le `accessToken`, où et comment l'obtenir
- Comment publier le jeton d'accès sur Github sans que le scanner et le protecteur de jetons ne s'activent