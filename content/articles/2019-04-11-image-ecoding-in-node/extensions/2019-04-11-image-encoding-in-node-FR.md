---
image: base64.png
excerpt: En traitant des images dans une application node, j'ai dû apprendre à lire et potentiellement décoder les données d'image.
title: Encodage d'image dans Node JS
tags: Tech
translation: fr
source_language: en
source_hash: 6ea1e653541e40ff79fe22531cc7177e4ece5d7e49f0645f7e445ebe89755089
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:04:12.845798+00:00
generated_by: simplified-translation-system
---

**Cet article est en cours de rédaction !**

En programmant sur un projet parallèle, j'ai dû gérer des images dans une application node. Mon application utilise [Express](https://expressjs.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition/) ainsi que [Pouchdb](https://pouchdb.com/).

Je traitais différentes sources et cibles :

- Un utilisateur télécharge une image
- Je lis une image à partir d'un fichier, qu'elle soit au format JPEG ou PNG
- J'envoie une image à AWS
- Je stocke une image dans mon pouchDB

En explorant les différentes sources, j'ai rencontré divers formats sur la manière dont les images peuvent être traitées dans node :

- Comme un buffer contenant des données binaires
- Comme une chaîne contenant des données encodées en Base64, commençant par quelque chose comme `data:image/jpeg;base64,` (ou avec `png`)
- Comme une chaîne contenant des données encodées en base64 sans le début spécial

Voici les différentes opérations que je réalise et ce qu'elles fournissent comme sortie :

- Lecture d'un fichier depuis le disque avec `fs` : retourne un `Buffer` avec des données binaires
-

Voici les sources et cibles à partir desquelles les données d'image sont transférées dans mon exemple :
![Sources et cibles d'image](https://docs.google.com/drawings/d/e/2PACX-1vTaOoDUdKWZ9q05WH1LX1Yz_JbismNFdrYMoFYYsbU410xf23mi4GxRv_ZvhIQipnLDXunKU5eCh-Ju/pub?w=960&h=720)

## Lecture

Ressources utiles que j'ai trouvées sur les sujets :

- [Comment convertir une image en URL de données encodées en base64 dans sails.js ou généralement dans le JavaScript côté serveur ? StackOverflow](https://stackoverflow.com/questions/24523532/how-do-i-convert-an-image-to-a-base64-encoded-data-url-in-sails-js-or-generally)
- [Encodage/décodage d'image base64 dans NodeJS ne fonctionne pas tout à fait, StackOverflow](https://stackoverflow.com/questions/8110294/nodejs-base64-image-encoding-decoding-not-quite-working)
- [Inkjet, bibliothèque de décodage, encodage d'image JPEG et de lecture EXIF pour un navigateur et node.js, Github](https://github.com/gchudnov/inkjet/blob/master/README.md)