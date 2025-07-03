---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 4937f2ac2f9ef24fe3dcf7afe89ab7a8221d93cf13b33a64eaaadbb57e5721c1
translation-type: automatic
---

[de→fr] <div class="toc">
<ul>
<li><a href="#tools-i-would-like-to-have">Tools I would like to have</a><ul>
<li><a href="#picture-tag-completion-ai">Picture tag completion (<span class="caps">AI</span>)</a></li>
<li><a href="#link-checker">Link checker</a></li>
<li><a href="#extract-generator-ai">Extract Generator (<span class="caps">AI</span>)</a></li>
<li><a href="#translator-aiish">Translator (<span class="caps">AI</span>’ish)</a></li>
<li><a href="#article-illustration-ai">Article illustration (<span class="caps">AI</span>)</a></li>
</ul>
</li>
<li><a href="#we-need-a-build-pipeline">We need a build pipeline</a><ul>
<li><a href="#interims-data">Interims data</a></li>
<li><a href="#integrity-of-authored-content">Integrity of authored content</a></li>
<li><a href="#where-to-keep-data">Where to keep data</a></li>
<li><a href="#processing-order">Processing order</a></li>
</ul>
</li>
</ul>
</div>
<p>Since last week my blog is based on <a href="https://getpelican.com" rel="noopener noreferrer" target="_blank">Pelican</a>, the Python based static blog generator. Now that the blog is built in a language that I master more or less, I can think of improving the process of writing and building things myself. And of course there are lots of tools that I can think of in order to make my life as well as the life of my readers easier. So here are some examples of these helpers.</p>
<h2 id="tools-i-would-like-to-have">Tools I would like to have</h2>
<h3 id="picture-tag-completion-ai">Picture tag completion (<span class="caps">AI</span>)</h3>
<p>Whenever I add a picture without an alt text, it’s bad for blind people. But I am lazy, so why not let an <span class="caps">AI</span> describe the picture and add it as <span class="caps">ALT</span> text?</p>
<h3 id="link-checker">Link checker</h3>
<p>I have many links pointing to external locations. And sometimes webpages disappear, so my links might point into Nirwana. It would be nice if</p>
<ul>
<li>my user wouldn’t have to click on broken links</li>
<li>I would get a tip that I need to fix one or the other link</li>
<li>I could maybe prevent the situation by keeping a copy of the page I link to in my own blog. Or is that evil scraping and content stealing?</li>
</ul>
<h3 id="extract-generator-ai">Extract Generator (<span class="caps">AI</span>)</h3>
<p>I often write articles without specifying the summary / excerpt that is shown in the article list. By default Pelican (and other static generators) take the first paragraph or the first 30 words and use it as excerpt.</p>
<p>Wouldn’t it be much nicer to ask an <span class="caps">LLM</span> to generate a reasonable 3 lines summary?</p>
<h3 id="translator-aiish">Translator (<span class="caps">AI</span>’ish)</h3>
<p>In my blog I sometimes write English, sometimes German articles. Maybe there is even a French article here and there. Wouldn’t it be nice to have every article in every language? It feels as if nowadays that should be a standard, given the good quality of today’s translation tools.</p>
<p>So I write my articles in whatever language just comes out of my little brain, and the system should generate the missing languages.</p>
<h3 id="article-illustration-ai">Article illustration (<span class="caps">AI</span>)</h3>
<p>I try to have pictures for most of my articles, as it’s just a nicer reading experiance and pleasant for the eye. I often find something in the internet, but not always - also because I sometimes don’t even bother searching an image. But the <span class="caps">AI</span> could search, or even generate a nice picture for my <em>naked</em> articles.</p>
<h2 id="we-need-a-build-pipeline">We need a build pipeline</h2>
<p>In order to get those things built, I feel I need something like a <em>Build Pipeline</em>:</p>
<p><img alt="Build Pipeline" src="https://insights.mgm-tp.com/wp-content/uploads/2023/08/mgm-CI-CD-Pipeline.png"/>
<em>A modern <span class="caps">CI</span>/<span class="caps">CD</span> build pipeline, taken from <a href="https://mgm-tp.com" rel="noopener noreferrer" target="_blank">mgm technology partners</a></em></p>
<p>Some thoughts about the structure, the processing and how to organize data.</p>
<h3 id="interims-data">Interims data</h3>
<p>What Pelican does, is to take the source of the articles, together with the configuration and generate the web pages. It does so by it’s standard processing and by potential plugins. Plugins can be third-party or delf-developed. In my case I have both.</p>
<p>Many of the tools I envisage create additional data, and often times the creation is expensive and time consuming. Think of creating an excerpt of an article: The entire text needs top be sent to an <span class="caps">AI</span> and processed. This takes multiple seconds and costs real money. Therefore it’s certainly not something we wnt to run on every build. So we will have to keep the data between the different build runs.</p>
<h3 id="integrity-of-authored-content">Integrity of authored content</h3>
<p>One way we could think of solving this, is to simply add the <span class="caps">AI</span> generated excerpt to the original markdown (in this case it would go in the front matter as <code>summary</code> field).</p>
<p>But I don’t like this at all: I don’t want the <span class="caps">AI</span> to mess around in the text and content I have been crafting personally. Therefore I want to define the following rule for my system:</p>
<p><strong>My authored Markdown files should never be modified by automated tools.</strong></p>
<h3 id="where-to-keep-data">Where to keep data</h3>
<p>That leaves me with the question where to keep the data like <span class="caps">AI</span> generated summaries. The natural place is to keep it next to the markdown files, but in it’s own file. As I have separate directories for each of my article, I end up with this shape of directories and files:</p>
<div class="highlight"><pre><span></span><code>content
    articles
    ...
    2025-04-18-digital-garden
        2025-04-18-ditigal-garden.md
        2025-04-18-digital-garden.picture-tags.json
        2025-04-18-digital-garden.summary.json
        digital-garden.jpg
</code></pre></div>
<p>Some thoughts and arguments for this structure:</p>
<ul>
<li>Every tool has it’s own file to keep things separate.</li>
<li>I use <span class="caps">JSON</span> files: Easy to process and easy to read.</li>
<li>The files are next to the original article, so everything that relates is close by and <em>encapsulated</em>.</li>
<li>The <span class="caps">JSON</span> files are also version controlled and stored in Git, so wether I run the build process on my local dev machine or inside Github Actions or another <span class="caps">CI</span>/<span class="caps">CD</span> processor, it re-uses the previously generated data.</li>
</ul>
<h3 id="processing-order">Processing order</h3>
<p>This data layout requires a multi-step build-process:</p>
<ol>
<li><strong>Create additional data:</strong> generate the summaries, the picture descriptions, the pictures, check the links (and store the result of those checks)… This process part is potentially time consuming, generates lots of additional data and requires intelligent caching and cache-validation mechanisms. I.e. “How do I check if I need to re-create the summary of an article or I can use the one in the <span class="caps">JSON</span> file alongside the markdown article?”.</li>
<li><strong>Build the site:</strong> This is the basic Pelican creation process as we know it, except that it also needs to <em>integrate</em> the additional data that is now in the <span class="caps">JSON</span> files. I will do this one or more Pelican plugins that I will develop.</li>
</ol>