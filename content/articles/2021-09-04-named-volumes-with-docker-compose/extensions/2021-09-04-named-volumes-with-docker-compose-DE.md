---
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:42:05.323827
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2021-09-04-named-volumes-with-docker-compose/2021-09-04-named-volumes-with-docker-compose.md
Generated-By: automatic-translation-plugin
---

```markdown
---
layout: post
title: Benannte Volumes mit docker-compose
slug: named-volumes-with-docker-compose
date_published: 2021-09-04T12:51:55.000Z
date_updated: 2021-09-04T19:24:42.000Z
tags: Tech
date: 2021-09-04
excerpt: Wie man ein Volume innerhalb von docker-compose erstellt, das von vielen Containern und an einem bestimmten Ort auf dem Host verwendet wird.
image: types-of-mounts-volume.png
---

Während ich an einem Nebenprojekt arbeitete, das **docker-compose** verwendet, stieß ich auf ein Problem. Eines, dem ich schon früher begegnet war, das ich aber nie richtig untersucht oder gelöst hatte.

Hier ist, was ich tun möchte:

- Eine Reihe von Diensten innerhalb eines docker-compose Setups ausführen
- Diese Dienste sollen gemountete Freigaben verwenden - eine Freigabe, die von mehr als einem Container genutzt wird.
- Das Problematische: Ich möchte, dass **mehrere Container** das **gleiche Volume** verwenden!

Um es kurz zu machen, so funktioniert es reibungslos:

```yaml
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
```

Das passiert hier:

- Wir haben 2 Dienste des gleichen Typs: einfache nginx-Container zu Demonstrationszwecken.
- Beide geben ihren (internen) Port 80 an Port 81 bzw. 82 zur Außenwelt frei.
- Beide verwenden ein Volume namens **content**, das im Volumes-Abschnitt definiert ist.

Das Detail, das ich so lange übersehen hatte, war der **volumes**-Abschnitt mit den **driver_opts**. Und während ich einige Tests durchführte und alles genau so funktionierte, wie ich es mir erhofft hatte, konnte ich keine ordentliche Dokumentation finden. Hier ist, was die [docker Dokumentation](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts) über **driver_opts** sagt:

> Geben Sie eine Liste von Optionen als Schlüssel-Wert-Paare an, die an den Treiber für dieses Volume übergeben werden. Diese Optionen sind treiberabhängig - konsultieren Sie die Dokumentation des Treibers für weitere Informationen.

Beim Untersuchen, wie die Dinge funktionieren, geben die Inspektionswerkzeuge von Docker einige Einblicke: Dies ist der **Mounts**-Teil von **docker inspect service1**

```json
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
```

Zuerst war ich skeptisch wegen dieser Zeile:

```json
"Source": "/var/lib/docker/volumes/docker-playground_content/_data"
```

Aber es stellt sich heraus, dass meine Daten **nicht** in diesem von Docker verwalteten Verzeichnis sind, sondern dort, wo ich sie haben wollte. In meinem Fall ist das in **./data/content**. Auch der relative Pfad funktioniert einwandfrei.

### Quellen

Hier sind die ursprünglichen Quellen, die mir am meisten geholfen haben

- Docker Dokumentation - seltsamerweise hat sie überhaupt nicht geholfen...
- Dies war der hilfreichste [Stackoverflow-Artikel](https://stackoverflow.com/questions/35841241/docker-compose-named-mounted-volume).

### Versionen

Da diese Art von Setups versionsabhängig sein können, hier mein Setup:

```plaintext
docker-compose version 1.29.2, build 5becea4c
docker-py version: 5.0.0
CPython version: 3.9.0
OpenSSL version: OpenSSL 1.1.1h  22 Sep 2020
```

Und es läuft auf meinem Mac mit Big Sur Version 11.5.2 (mit Intel CPU 😜).

Der Code ist auf [Github](https://github.com/tillg/docker-compose-volumes-playground/) zu finden.
```