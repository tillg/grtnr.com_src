---
layout: post
title: Benannte Volumes mit docker-compose
slug: benannte-volumes-mit-docker-compose
date_published: 2021-09-04T12:51:55.000Z
date_updated: 2021-09-04T19:24:42.000Z
tags: Tech
date: 2021-09-04
excerpt: Wie man ein Volume innerhalb von docker-compose erstellt, das von vielen Containern und an einem bestimmten Ort auf dem Host verwendet wird.
image: types-of-mounts-volume.png
translation: de
source_language: en
source_hash: bece392770213a0b4ec0545c21f7c35f20ef22056dbd013d44b1aa26f5153339
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:29:13.717769
generated_by: simplified-translation-system
---

Während ich an einem Nebenprojekt arbeitete, das **docker-compose** verwendet, stieß ich auf ein Problem. Eines, dem ich schon früher begegnet war, das ich aber nie richtig untersucht oder gelöst hatte.

Hier ist, was ich tun möchte:

- Eine Reihe von Diensten innerhalb eines docker-compose Setups laufen lassen
- Diese Dienste sollen gemountete Freigaben verwenden - eine Freigabe, die von mehr als einem Container genutzt wird.
- Das Problematische: Ich möchte, dass **mehrere Container** dasselbe **Volume** verwenden!

Um es kurz zu machen, so funktioniert es reibungslos:

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

Das passiert hier:

- Wir haben 2 Dienste desselben Typs: einfache nginx-Container zu Demonstrationszwecken.
- Beide geben ihren (internen) Port 80 an Port 81 bzw. 82 zur Außenwelt frei.
- Beide verwenden ein Volume namens **content**, das im Volumes-Abschnitt definiert ist.

Das Detail, das ich so lange übersehen hatte, war der **volumes** Abschnitt mit den **driver_opts**. Und während ich ein paar Tests durchführte und alles genau so funktionierte, wie ich es mir erhofft hatte, konnte ich keine ordentliche Dokumentation finden. Hier ist, was die [docker Dokumentation](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts) über **driver_opts** sagt:

> Geben Sie eine Liste von Optionen als Schlüssel-Wert-Paare an, die an den Treiber für dieses Volume übergeben werden. Diese Optionen sind treiberabhängig - konsultieren Sie die Dokumentation des Treibers für weitere Informationen.

Beim Untersuchen, wie die Dinge funktionieren, geben die Inspektionswerkzeuge von Docker einige Einblicke: Dies ist der **Mounts** Teil von **docker inspect service1**

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

Zunächst war ich skeptisch wegen dieser Zeile:

    "Source": "/var/lib/docker/volumes/docker-playground_content/_data"

Aber es stellt sich heraus, dass sich meine Daten **nicht** in diesem von Docker verwalteten Verzeichnis befinden, sondern dort, wo ich sie haben wollte. In meinem Fall ist das in **./data/content**. Auch der relative Pfad funktioniert einwandfrei.

### Quellen

Hier sind die ursprünglichen Quellen, die mir am meisten geholfen haben

- Docker Dokumentation - seltsamerweise hat sie überhaupt nicht geholfen...
- Dies war der hilfreichste [Stackoverflow-Artikel](https://stackoverflow.com/questions/35841241/docker-compose-named-mounted-volume).

### Versionen

Da diese Art von Setups möglicherweise versionsabhängig sind, hier ist mein Setup:

    docker-compose version 1.29.2, build 5becea4c
    docker-py version: 5.0.0
    CPython version: 3.9.0
    OpenSSL version: OpenSSL 1.1.1h  22 Sep 2020

Und es läuft auf meinem Mac mit Big Sur Version 11.5.2 (mit Intel CPU 😜).

Der Code ist [auf Github](https://github.com/tillg/docker-compose-volumes-playground/) zu finden.