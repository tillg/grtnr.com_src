---
layout: post
title: Volumes nommés avec docker-compose
slug: named-volumes-with-docker-compose
date_published: 2021-09-04T12:51:55.000Z
date_updated: 2021-09-04T19:24:42.000Z
tags: Tech
date: 2021-09-04
excerpt: Comment créer un volume avec docker-compose, utilisé par plusieurs conteneurs et situé à un emplacement spécifique sur l'hôte.
image: types-of-mounts-volume.png
translation: fr
source_language: en
source_hash: bece392770213a0b4ec0545c21f7c35f20ef22056dbd013d44b1aa26f5153339
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:29:30.272753
generated_by: simplified-translation-system
---

En travaillant sur un projet annexe utilisant **docker-compose**, je suis tombé sur un problème. Un problème que j'avais déjà rencontré mais que je n'avais jamais vraiment étudié ou résolu.

Voici ce que je veux faire :

- Avoir un ensemble de services fonctionnant dans une configuration docker-compose
- Faire en sorte que ces services utilisent des partages montés - un partage, utilisé par plus d'un conteneur.
- Le problème : je veux que **plusieurs conteneurs** utilisent le **même volume** !

Pour faire court, voici comment cela fonctionne parfaitement :

    version: '3'
    services:
      service1:
        image: nginx
        container_name: service1
        ports:
          - '81:80'
        volumes:
          - content:/usr/share/nginx/html

      service2:
        image: nginx
        container_name: service2
        ports:
          - '82:80'
        volumes:
          - content:/usr/share/nginx/html

    volumes:
      content:
         driver_opts:
               type: none
               device: ./data/content
               o: bind

Voici ce qui se passe :

- Nous avons 2 services du même type : des conteneurs nginx simples à des fins de démonstration.
- Ils exposent tous deux leur port interne 80 vers le port 81 respectivement 82 vers l'extérieur.
- Ils utilisent tous deux un volume appelé **content** qui est défini dans la section volumes.

Le détail que j'ai manqué pendant si longtemps était la section **volumes** avec les **driver_opts**. Et bien que j'aie effectué quelques tests et que tout se soit comporté exactement comme je l'espérais, je n'ai pas pu trouver de documentation appropriée. Voici ce que dit la [documentation de docker](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts) à propos des **driver_opts** :

> Spécifiez une liste d'options sous forme de paires clé-valeur à transmettre au pilote pour ce volume. Ces options dépendent du pilote - consultez la documentation du pilote pour plus d'informations.

En examinant comment les choses fonctionnent, les outils d'inspection de docker donnent quelques aperçus : voici la partie **Mounts** de **docker inspect service1**

     "Mounts": [
                {
                    "Type": "volume",
                    "Name": "docker-playground_content",
                    "Source": "/var/lib/docker/volumes/docker-playground_content/_data",
                    "Destination": "/usr/share/nginx/html",
                    "Driver": "local",
                    "Mode": "rw",
                    "RW": true,
                    "Propagation": ""
                }
            ]

Au début, j'étais sceptique à cause de cette ligne :

    "Source": "/var/lib/docker/volumes/docker-playground_content/_data"

Mais il s'avère que mes données ne sont **pas** dans ce répertoire géré par docker, mais là où je le voulais. Dans mon cas, c'est dans **./data/content**. De plus, le chemin relatif fonctionne bien.

### Sources

Voici les sources originales qui m'ont le plus aidé

- Documentation Docker - assez étrange, elle ne m'a pas aidé du tout...
- Voici l'article [Stackoverflow](https://stackoverflow.com/questions/35841241/docker-compose-named-mounted-volume) le plus utile.

### Versions

Étant donné que ce type de configurations peut être sensible aux versions, voici ma configuration :

    docker-compose version 1.29.2, build 5becea4c
    docker-py version: 5.0.0
    CPython version: 3.9.0
    OpenSSL version: OpenSSL 1.1.1h  22 Sep 2020

Et cela fonctionne sur mon Mac avec Big Sur Version 11.5.2 (avec CPU Intel 😜).

Le code peut être trouvé [sur Github](https://github.com/tillg/docker-compose-volumes-playground/).