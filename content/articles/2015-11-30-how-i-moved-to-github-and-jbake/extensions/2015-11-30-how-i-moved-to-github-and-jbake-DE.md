---
source-language: en
target-language: de
last-created: 2025-07-03 17:23:23
hash-on-last-created: fc01f1f9e9e83ae138752a97264aff842fedb402ae12947d5e1806d51ce49b7c
translation-type: automatic
---

[en→de] <p><strong>*</strong> This page is ~~under construction~~ unfinished… <strong>*</strong></p>
<p>First: It’s not my invention! Many did it before, there are lots of description out there. It still took me some time ;)</p>
<p><a href="http://alexcican.com/post/guide-hosting-website-dropbox-github/" rel="noopener noreferrer" target="_blank">This</a> and <a href="http://alexcican.com/post/blog-dropbox-scriptogram" rel="noopener noreferrer" target="_blank">this</a> was the most inspiring source and easiest explanation (that gives confidence ;) ).</p>
<h1 id="setup">Setup</h1>
<p>So this is the overall setup I have:</p>
<ul>
<li>A directory on my Mac that holds the content. I use the basic structure that <a href="http://jbake.org" rel="noopener noreferrer" target="_blank">Jbake</a> uses.</li>
<li>A git-cloned directory on my Mac with the output of the jBake-process</li>
<li>A little script that I run every time I modified something. The script does the baking and the git-publishing</li>
<li>And of course the settings in the <span class="caps">DNS</span> to point my Domain name to the Github IPs</li>
</ul>
<h2 id="jbake">JBake</h2>
<p>Why do I use JBake? I like the principle and I feel more comfortable in Java than in other programming languages. I haven’t touched the JBake internal code, but I feel confident that I could.
The principle way that JBake operates is similar to the famous <a href="https://jekyllrb.com/" rel="noopener noreferrer" target="_blank">Jekyll</a>: It parses content files and creates (static) <span class="caps">HTML</span> files out of it. The content files can contain Markdown or some other formats; I just use Markdown.</p>
<p>My directory structure looks like this:</p>
<div class="highlight"><pre><span></span><code>.
|-- assets
|   |-- favicon.gif
|   |-- robots.txt
|   |-- img
|   |   |-- logo.png
|   |-- js
|   |   |-- custom.js
|   |-- css
|       |-- style.css
|
|-- content
|   |-- about.html
|   |-- 2013
|       |-- 01
|       |   |-- hello-world.html
|       |-- 02
|           |-- weekly-links-1.ad
|           |-- weekly-links-2.md
|
|-- templates
|   |-- index.ftl
|   |-- page.ftl
|   |-- post.ftl
|   |-- feed.ftl
|
|-- jbake.properties
</code></pre></div>
<p>By default JBake produces the output directory into this tree. In my case I bake my stuff into a directory that is git-synced.</p>
<h2 id="the-github-setup">The GitHub setup</h2>
<h2 id="the-dns-settings">The <span class="caps">DNS</span> settings</h2>
<h1 id="next-up">Next up</h1>
<p>There are a couple of things I plan to change.</p>