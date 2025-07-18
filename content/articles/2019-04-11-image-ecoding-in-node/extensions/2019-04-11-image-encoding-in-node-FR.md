---
title: Encodage d'image dans Node JS
layout: post
date_published: 2019-04-15T00:00:00.000Z
date_updated: 2021-12-06T09:47:26.000Z
tags: Tech
image: base64.png
excerpt: Lors de la gestion d'images dans une application node, j'ai dû apprendre à lire et potentiellement décoder les données d'image.
translation: fr
source_language: en
source_hash: 6ea1e653541e40ff79fe22531cc7177e4ece5d7e49f0645f7e445ebe89755089
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:25:11.925049
generated_by: simplified-translation-system
---

**Cet article est en cours de rédaction !**

En programmant un projet annexe, j'ai dû gérer des images dans une application node. Mon application utilise [Express](https://expressjs.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition/) ainsi que [Pouchdb](https://pouchdb.com/).

Je gérais différentes sources et cibles :

- Un utilisateur télécharge une image
- Je lis une image à partir d'un fichier, qu'il soit au format JPEG ou PNG
- J'envoie une image à AWS
- Je stocke une image dans mon pouchDB

En parcourant les différentes sources, j'ai rencontré divers formats sur la manière dont les images peuvent être traitées dans node :

- Comme un buffer contenant des données binaires
- Comme une chaîne contenant des données encodées en Base64, commençant par quelque chose comme `data:image/jpeg;base64,` (ou avec `png`)
- Comme une chaîne contenant des données encodées en base64 sans le début spécial

Voici les différentes opérations que je fais et ce qu'elles fournissent en sortie :

- Lecture d'un fichier depuis le disque avec `fs` : retourne un `Buffer` avec des données binaires
-

Voici les sources et cibles à partir desquelles et vers lesquelles les données d'image sont transférées dans mon exemple :
![Sources et cibles d'image](https://docs.google.com/drawings/d/e/2PACX-1vTaOoDUdKWZ9q05WH1LX1Yz_JbismNFdrYMoFYYsbU410xf23mi4GxRv_ZvhIQipnLDXunKU5eCh-Ju/pub?w=960&h=720)

## Lecture

Informations utiles que j'ai trouvées sur les sujets :

- [Comment convertir une image en URL de données encodées en base64 dans sails.js ou généralement en JavaScript côté serveur ? StackOverflow](https://stackoverflow.com/questions/24523532/how-do-i-convert-an-image-to-a-base64-encoded-data-url-in-sails-js-or-generally)
- [Encodage/décodage d'image base64 dans NodeJS ne fonctionne pas tout à fait, StackOverflow](https://stackoverflow.com/questions/8110294/nodejs-base64-image-encoding-decoding-not-quite-working)
- [Inkjet, bibliothèque de décodage, encodage d'images JPEG et lecture EXIF pour un navigateur et node.js, Github](https://github.com/gchudnov/inkjet/blob/master/README.md)