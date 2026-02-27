---
image: base64.png
excerpt: Beim Umgang mit Bildern in einer Node-Anwendung musste ich lernen, wie man Bilddaten liest und möglicherweise dekodiert.
title: Bildkodierung in Node JS
tags: Tech
translation: de
source_language: en
source_hash: 6ea1e653541e40ff79fe22531cc7177e4ece5d7e49f0645f7e445ebe89755089
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:04:03.522017+00:00
generated_by: simplified-translation-system
---

**Dieser Artikel ist in Arbeit!**

Während ich an einem Nebenprojekt programmierte, musste ich mich mit Bildern in einer Node-Anwendung auseinandersetzen. Meine Anwendung verwendet [Express](https://expressjs.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition/) sowie [Pouchdb](https://pouchdb.com/).

Ich hatte es mit verschiedenen Quellen und Zielen zu tun:

- Ein Benutzer lädt ein Bild hoch
- Ich lese ein Bild von einer Datei, sei es im JPEG- oder PNG-Format
- Ich sende ein Bild an AWS
- Ich speichere ein Bild in meiner PouchDB

Beim Durchsuchen der verschiedenen Quellen stieß ich auf verschiedene Formate, wie Bilder in Node behandelt werden können:

- Als Buffer, der Binärdaten enthält
- Als String, der Base64-kodierte Daten enthält, beginnend mit etwas wie `data:image/jpeg;base64,` (oder mit `png`)
- Als String, der Base64-kodierte Daten ohne den speziellen Anfang enthält

Dies sind die verschiedenen Operationen, die ich durchführe, und was sie als Ausgabe liefern:

- Lesen einer Datei von der Festplatte mit `fs`: Rückgabe eines `Buffer` mit Binärdaten
-

Dies sind die Quellen und Ziele, in/von denen Bilddaten in meinem Beispiel übertragen werden:
![Bildquellen und -ziele](https://docs.google.com/drawings/d/e/2PACX-1vTaOoDUdKWZ9q05WH1LX1Yz_JbismNFdrYMoFYYsbU410xf23mi4GxRv_ZvhIQipnLDXunKU5eCh-Ju/pub?w=960&h=720)

## Lesen

Nützliche Informationen, die ich zu den Themen gefunden habe:

- [Wie konvertiere ich ein Bild in eine base64-kodierte Daten-URL in sails.js oder allgemein in serverseitigem JavaScript? StackOverflow](https://stackoverflow.com/questions/24523532/how-do-i-convert-an-image-to-a-base64-encoded-data-url-in-sails-js-or-generally)
- [NodeJS base64 Bildkodierung/Dekodierung funktioniert nicht ganz, StackOverflow](https://stackoverflow.com/questions/8110294/nodejs-base64-image-encoding-decoding-not-quite-working)
- [Inkjet, JPEG-Bilddekodierung, Kodierung & EXIF-Lesebibliothek für Browser und node.js, Github](https://github.com/gchudnov/inkjet/blob/master/README.md)