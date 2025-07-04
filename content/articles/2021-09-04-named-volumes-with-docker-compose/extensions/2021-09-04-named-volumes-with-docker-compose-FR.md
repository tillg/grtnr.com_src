---
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T17:02:42.525335
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2021-09-04-named-volumes-with-docker-compose/2021-09-04-named-volumes-with-docker-compose.md
Generated-By: automatic-translation-plugin
---

```markdown
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
---

En travaillant sur un projet annexe utilisant **docker-compose**, je suis tombé sur un problème. Un problème que j'avais déjà rencontré auparavant mais que je n'avais jamais vraiment investigué ou résolu.

Voici ce que je veux faire :

- Avoir un ensemble de services fonctionnant dans une configuration docker-compose
- Faire en sorte que ces services utilisent des partages montés - un partage, utilisé par plus d'un conteneur.
- Le problème : je veux que **plusieurs conteneurs** utilisent le **même volume** !

Pour faire court, voici comment cela fonctionne sans problème :

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
- Ils exposent tous deux leur port (interne) 80 aux ports 81 et 82 respectivement vers l'extérieur.
- Ils utilisent tous deux un volume appelé **content** qui est défini dans la section volumes.

Le détail que j'ai manqué pendant si longtemps était la section **volumes** avec les **driver_opts**. Et bien que j'aie effectué quelques tests et que tout se soit comporté exactement comme je l'espérais, je n'ai pas pu trouver de documentation appropriée. Voici ce que dit la [documentation de docker](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts) à propos des **driver_opts** :

> Spécifiez une liste d'options sous forme de paires clé-valeur à transmettre au pilote pour ce volume. Ces options dépendent du pilote - consultez la documentation du pilote pour plus d'informations.

En enquêtant sur le fonctionnement des choses, les outils d'inspection de docker donnent quelques aperçus : Voici la partie **Mounts** de **docker inspect service1**

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

- Documentation Docker - assez étrangement, elle ne m'a pas du tout aidé...
- Voici l'article [Stackoverflow](https://stackoverflow.com/questions/35841241/docker-compose-named-mounted-volume) le plus utile.

### Versions

Étant donné que ces types de configurations peuvent être sensibles aux versions, voici ma configuration :

    docker-compose version 1.29.2, build 5becea4c
    docker-py version: 5.0.0
    CPython version: 3.9.0
    OpenSSL version: OpenSSL 1.1.1h  22 Sep 2020

Et cela fonctionne sur mon Mac avec Big Sur Version 11.5.2 (avec un CPU Intel 😜).

Le code peut être trouvé [sur Github](https://github.com/tillg/docker-compose-volumes-playground/).
```