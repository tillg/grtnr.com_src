---
source-language: en
target-language: de
last-created: 2025-07-03 17:23:23
hash-on-last-created: 6ea1e653541e40ff79fe22531cc7177e4ece5d7e49f0645f7e445ebe89755089
translation-type: automatic
---

[en→de] <p><strong>This article is work in progress!</strong></p>
<p>While programming on a side project, I had to deal with images in a node application. My application is using <a href="https://expressjs.com/" rel="noopener noreferrer" target="_blank">Express</a>, <a href="https://aws.amazon.com/rekognition/" rel="noopener noreferrer" target="_blank">Amazon Rekognition</a> as well as <a href="https://pouchdb.com/" rel="noopener noreferrer" target="_blank">Pouchdb</a>.</p>
<p>I was dealing with different sources <span class="amp">&amp;</span> targets:</p>
<ul>
<li>A user uploads a picture</li>
<li>I read a picture from file, be it in <span class="caps">JPEG</span> or <span class="caps">PNG</span> format</li>
<li>I send a picture to <span class="caps">AWS</span></li>
<li>I store a picture in my pouchDB</li>
</ul>
<p>While browsing the different sources, I encountered various formats on how images can be handled in node:</p>
<ul>
<li>As buffer containing binary data</li>
<li>As string conatining Base64 encoded data, starting with something like <code>data:image/jpeg;base64,</code> (or with <code>png</code>)</li>
<li>As string containing base64 encoded data without the special beginning</li>
</ul>
<p>These are the different operations I am doing and what they provide as output:</p>
<h2 id="-reading-a-file-from-disk-with-fs-return-a-bufferwith-binary-data">- Reading a file from disk with <code>fs</code>: return a <code>Buffer</code>with binary data</h2>
<p>These are the sources and targets in/from which image data is transferred in my example:
<img alt="Image sources and targets" src="https://docs.google.com/drawings/d/e/2PACX-1vTaOoDUdKWZ9q05WH1LX1Yz_JbismNFdrYMoFYYsbU410xf23mi4GxRv_ZvhIQipnLDXunKU5eCh-Ju/pub?w=960&amp;h=720"/></p>
<h2 id="reading">Reading</h2>
<p>Helpful stuff I found about the topics:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/24523532/how-do-i-convert-an-image-to-a-base64-encoded-data-url-in-sails-js-or-generally" rel="noopener noreferrer" target="_blank">How do I convert an image to a base64-encoded data <span class="caps">URL</span> in sails.js or generally in the servers side JavaScript? StackOverflow</a></li>
<li><a href="https://stackoverflow.com/questions/8110294/nodejs-base64-image-encoding-decoding-not-quite-working" rel="noopener noreferrer" target="_blank">NodeJS base64 image encoding/decoding not quite working, StackOverflow</a></li>
<li><a href="https://github.com/gchudnov/inkjet/blob/master/README.md" rel="noopener noreferrer" target="_blank">Inkjet, <span class="caps">JPEG</span>-image decoding, encoding <span class="amp">&amp;</span> <span class="caps">EXIF</span> reading library for a browser and node.js, Github</a></li>
</ul>