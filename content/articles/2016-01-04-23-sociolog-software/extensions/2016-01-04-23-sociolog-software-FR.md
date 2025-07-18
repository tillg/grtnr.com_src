---
title: sociolog - Votre parcours à travers les réseaux sociaux
tags: softwareWeNeed
layout: post
date: 2016-01-04
image: sociolog.png
excerpt: Un outil qui suit mes activités sur toutes les plateformes de réseaux sociaux.
translation: fr
source_language: en
source_hash: f74871d79814bc59a5b1c7171885bb67981c6fe570d92726c6e2abfd92f059f1
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:22:29.504243
generated_by: simplified-translation-system
---

J'écris ou je blogue sur différents médias :

- Twitter
- Facebook
- Un blog privé avec accès restreint (car il contient des photos de famille)
- Ce [blog](http://tillgartner.com)

De temps en temps, je trouve agréable de parcourir mon passé. Je le fais le plus souvent sur notre blog familial, car il contient le contenu le plus intéressant et parce qu'il est facile à parcourir. J'aimerais pouvoir faire défiler tout mon passé à travers tous les médias.

Voici donc ce que mon logiciel devrait faire :

- Collecter toutes les entrées que j'ai écrites sur les réseaux sociaux :
  - Twitter
  - Facebook
  - Wordpress
- Créer un document par entrée dans un dépôt Github
- Gérer correctement le contenu dupliqué : Depuis quelques années, mon compte Twitter est _lié_ à mon compte Facebook de sorte que les entrées Twitter sont répliquées sur Facebook. C'est parce que j'ai des personnes que je considère comme _audience_ sur les deux médias.
- Collecter également les retours sur mes publications
- Les afficher joliment de manière statique, y compris des pages de vue d'ensemble

Quelques réflexions techniques :

- Je l'écrirais en java car c'est ce que je connais le mieux
- Serait un programme sans interface utilisateur, c'est-à-dire sans UI
- L'entrée devrait être la date de la dernière entrée enregistrée sur les réseaux sociaux
- Il collecte toutes les entrées (y compris les commentaires) sur les différents canaux de réseaux sociaux depuis cette date
- Il élimine les doublons (c'est-à-dire fusionne celles qui sont identiques ou répliquées sur différents canaux)
- Il crée un document / fichier par entrée de réseau social et les écrit dans un répertoire de sortie
- Ce répertoire est ensuite répliqué / ajouté à un compte github
- Les documents d'entrée de réseau social seraient nommés comme `2015-12-03-Le_titre_de_ce_que_j'ai_écrit-TWITTER.json`
- Il y aurait un _fichier d'en-tête_ avec un nom fixe, c'est-à-dire `sociologs.json`. Ce fichier contiendrait les 20 premiers journaux et pointerait vers un fichier avec les journaux suivants.
- Le domaine `sociolog.io` serait [disponible](https://www.godaddy.com/domains/searchresults.aspx?&checkAvail=1&domainToCheck=sociolog.io) - à ce jour, le 4 janvier 2016.
- Le `index.html` généré chargerait les données via des requêtes JS/AJAX et continuerait à charger pendant que l'utilisateur fait défiler vers le bas

Si quelqu'un est intéressé ou a des commentaires, veuillez me contacter à till`point`gartner`arobase`gmail`point`com.