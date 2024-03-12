---
title: Image encoding in Node JS
layout: post
date_published: 2019-04-15T00:00:00.000Z
date_updated: 2021-12-06T09:47:26.000Z
tags: Tech
image: base64.png
---

**This article is work in progress!**

While programming on a side project, I had to deal with images in a node application. My application is using [Express](https://expressjs.com/), [Amazon Rekognition](https://aws.amazon.com/rekognition/) as well as [Pouchdb](https://pouchdb.com/).

I was dealing with different sources & targets:

- A user uploads a picture
- I read a picture from file, be it in JPEG or PNG format
- I send a picture to AWS
- I store a picture in my pouchDB

While browsing the different sources, I encountered various formats on how images can be handled in node:

- As buffer containing binary data
- As string conatining Base64 encoded data, starting with something like `data:image/jpeg;base64,` (or with `png`)
- As string containing base64 encoded data without the special beginning

These are the different operations I am doing and what they provide as output:

- Reading a file from disk with `fs`: return a `Buffer`with binary data
-

These are the sources and targets in/from which image data is transferred in my example:
![Image sources and targets](https://docs.google.com/drawings/d/e/2PACX-1vTaOoDUdKWZ9q05WH1LX1Yz_JbismNFdrYMoFYYsbU410xf23mi4GxRv_ZvhIQipnLDXunKU5eCh-Ju/pub?w=960&h=720)

## Reading

Helpful stuff I found about the topics:

- [How do I convert an image to a base64-encoded data URL in sails.js or generally in the servers side JavaScript? StackOverflow](https://stackoverflow.com/questions/24523532/how-do-i-convert-an-image-to-a-base64-encoded-data-url-in-sails-js-or-generally)
- [NodeJS base64 image encoding/decoding not quite working, StackOverflow](https://stackoverflow.com/questions/8110294/nodejs-base64-image-encoding-decoding-not-quite-working)
- [Inkjet, JPEG-image decoding, encoding & EXIF reading library for a browser and node.js, Github](https://github.com/gchudnov/inkjet/blob/master/README.md)
