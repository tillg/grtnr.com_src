---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: abc8f2afa5ca8b18bbd09e77e2d20b6bcbaf8353c5a215dd2435191f52cbc396
translation-type: automatic
---

[de→fr] <p><span class="caps">OK</span>, everytbody does it, even I do it: Static websites. It’s fast, it’s safe, it does the computing where it belongs (as long as you don’t need fancy customization, why should a server think about what the page looks like at read time?). This very site is static (built with <a href="http://jbake.org/" rel="noopener noreferrer" target="_blank">JBake</a> and hosted on <a href="https://github.com/" rel="noopener noreferrer" target="_blank">Github</a>). It was fun setting it up, it works great - but I couldn’t explain my mother how to use it or how to publish some content on it. And that’s what a CMs should be about: It has to be usable in the first place.</p>
<p>Therefore I need anotrher setup. I plan to have a look at some different static web site systems, and set up a list of criteria against which I plan to test the different generators…</p>
<h2 id="criteria">Criteria</h2>
<ul>
<li>Themes</li>
<li>Many</li>
<li>Beautiful</li>
<li>
<p>Responsive</p>
</li>
<li>
<p>Easy to write</p>
</li>
<li>Editor with preview</li>
<li>Easy handling and referencing of pics</li>
<li>Pictures in preview</li>
<li>Videos</li>
<li>Tables</li>
<li>Code with syntax highlighting</li>
<li>
<p>Automated checking of consistency, i.e. the generated website is correct, complete, the pointers don’t point to Nirwana…</p>
</li>
<li>
<p>Being able to create an <a href="https://www.ampproject.org/" rel="noopener noreferrer" target="_blank">Accelerated Mobile Page</a></p>
</li>
<li>Functional features <span class="amp">&amp;</span> pages</li>
<li>Tags, tag pages, tag cloud (could also be an extension)</li>
<li>Publishable on Github (it’s very fast, free and reliable)</li>
<li>Make website private. i.e. accessible only for registered members</li>
<li>Publish by email</li>
<li>Comment by email</li>
<li>Push news to registered users by email</li>
<li>Resize pics for fast delivery</li>
<li>Easy to create new themes, Themes should be just <span class="caps">CSS</span></li>
<li>
<p>Based on other <span class="caps">HTML</span>, i.e. Bootstrap themes</p>
</li>
<li>
<p>Extensible architecture</p>
</li>
<li>Can add stuff, i.e. Picture resizing process</li>
<li>At least a programming language I know a bit - or that I am curious to learn (that basically boils it down to Java and JavaScript)</li>
<li>The generated <span class="caps">HTML</span> should be as simple as possible. All formatting sits in the <span class="caps">CSS</span></li>
</ul>
<h2 id="generators">Generators</h2>
<p>When scanning the literature (and Github). this is the list of generators rthat I should probably have a look at:</p>
<ul>
<li>Jekyll - Done</li>
<li>Harp <span class="caps">JS</span> - Done</li>
<li>Hugo - Done</li>
<li>Metalsmith - Done</li>
<li>Nikola - Done</li>
<li>Octopress - Done</li>
<li>Hexo - Done</li>
<li>Hyde - Done</li>
<li>Pelican- Done</li>
<li>Nanoc - Done</li>
<li>Middleman - Done</li>
<li>Lektor - Done</li>
<li>Gatsby - Done</li>
<li>Expose - Done</li>
<li>Wintersmith - Done</li>
<li>Doc pad - Done</li>
<li>kirby - Done</li>
</ul>
<h2 id="evaluation-matrix">Evaluation Matrix</h2>
<table>
<thead>
<tr>
<th style="text-align: left;">Generator</th>
<th style="text-align: left;">Programming language</th>
<th style="text-align: left;">Themes</th>
<th style="text-align: left;">Formats</th>
<th style="text-align: left;">Comment</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><a href="https://jekyllrb.com/" rel="noopener noreferrer" target="_blank">Jekyll</a></td>
<td style="text-align: left;">Ruby —</td>
<td style="text-align: left;">Lots ++</td>
<td style="text-align: left;">Markdown, Textile, Liquid ++</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><em><a href="https://harpjs.com/" rel="noopener noreferrer" target="_blank">Harp <span class="caps">JS</span></a></em></td>
<td style="text-align: left;">NodeJS ++</td>
<td style="text-align: left;">Some 00</td>
<td style="text-align: left;">Markdown, <span class="caps">EJS</span>, Jade, <span class="caps">LESS</span>, Stylus… ++</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://gohugo.io/" rel="noopener noreferrer" target="_blank">Hugo</a></td>
<td style="text-align: left;"><span class="caps">GO</span> —</td>
<td style="text-align: left;">Some 00</td>
<td style="text-align: left;">Markdown, asciidoc, reStructure ++</td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><em><a href="http://www.metalsmith.io/" rel="noopener noreferrer" target="_blank">Metalsmith</a></em></td>
<td style="text-align: left;">Node <span class="caps">JS</span> —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;">Looks very flexible. Also see http://dbushell.com/2015/05/11/wordpress-to-metalsmith/</td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://getnikola.com/" rel="noopener noreferrer" target="_blank">Nikola</a></td>
<td style="text-align: left;">Python —</td>
<td style="text-align: left;">Few —</td>
<td style="text-align: left;">reStructuredText, Markdown,</td>
<td style="text-align: left;">Looks just so so…</td>
</tr>
<tr>
<td style="text-align: left;"><a href="http://octopress.org/" rel="noopener noreferrer" target="_blank">Octopress</a></td>
<td style="text-align: left;">Python —</td>
<td style="text-align: left;">Some 00</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">Is just a package around Jekyll.</td>
</tr>
<tr>
<td style="text-align: left;"><em><a href="https://hexo.io/" rel="noopener noreferrer" target="_blank">Hexo</a></em></td>
<td style="text-align: left;">Node <span class="caps">JS</span> ++</td>
<td style="text-align: left;">Some 00</td>
<td style="text-align: left;">Markdown, different flavors, Jekyll Plugins ++</td>
<td style="text-align: left;">Looks very flexible, uses standard template engines (<span class="caps">EJS</span>, Jade, Swig…), allows to integrate scripts and plugins. ++</td>
</tr>
<tr>
<td style="text-align: left;"><a href="http://hyde.github.io/" rel="noopener noreferrer" target="_blank">Hyde</a></td>
<td style="text-align: left;">Python —</td>
<td style="text-align: left;">Little —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="http://blog.getpelican.com/" rel="noopener noreferrer" target="_blank">Pelican</a></td>
<td style="text-align: left;">Python —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="http://nanoc.ws/" rel="noopener noreferrer" target="_blank">Nanoc</a></td>
<td style="text-align: left;">Ruby —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://middlemanapp.com/" rel="noopener noreferrer" target="_blank">Moddleman</a></td>
<td style="text-align: left;">Python —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://www.getlektor.com/" rel="noopener noreferrer" target="_blank">Lektor</a></td>
<td style="text-align: left;">Python —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://github.com/gatsbyjs/gatsby" rel="noopener noreferrer" target="_blank">Gatsby</a></td>
<td style="text-align: left;">Node <span class="caps">JS</span>, React</td>
<td style="text-align: left;">No —</td>
<td style="text-align: left;">Markdown 00</td>
<td style="text-align: left;">Looks very flexible, but pretty complex…</td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://github.com/Jack000/Expose" rel="noopener noreferrer" target="_blank">Expose</a></td>
<td style="text-align: left;">Shell scripts —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">Markdown and picture folders</td>
<td style="text-align: left;">Specifically for picture sites.</td>
</tr>
<tr>
<td style="text-align: left;"><em><a href="http://wintersmith.io/" rel="noopener noreferrer" target="_blank">Wintersmith</a></em></td>
<td style="text-align: left;">Node <span class="caps">JS</span>, CoffeeScript ++</td>
<td style="text-align: left;">Little —</td>
<td style="text-align: left;">Markdown, Jade, …</td>
<td style="text-align: left;">Looks very flexible, <span class="caps">LESS</span>, Sass, Stylus. Might be a bit complex…</td>
</tr>
<tr>
<td style="text-align: left;"><a href="http://docpad.org/" rel="noopener noreferrer" target="_blank">DocPad</a></td>
<td style="text-align: left;">Node <span class="caps">JS</span> ++</td>
<td style="text-align: left;">No —</td>
<td style="text-align: left;">Markdown and others ++</td>
<td style="text-align: left;">Looks flexible but complex</td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://getkirby.com/" rel="noopener noreferrer" target="_blank">kirby</a></td>
<td style="text-align: left;"><span class="caps">PHP</span> —</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">Markdown</td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>
<p>As a result I should have a closer look at <em><a href="https://harpjs.com/" rel="noopener noreferrer" target="_blank">Harp <span class="caps">JS</span></a></em>, <em><a href="http://www.metalsmith.io/" rel="noopener noreferrer" target="_blank">Metalsmith</a></em>, <em><a href="https://hexo.io/" rel="noopener noreferrer" target="_blank">Hexo</a></em> and <em><a href="http://wintersmith.io/" rel="noopener noreferrer" target="_blank">Wintersmith</a></em>.</p>
<p>After quickly reading thru the websites of the above tools I decided to give it a try with <em><a href="http://www.metalsmith.io/" rel="noopener noreferrer" target="_blank">Metalsmith</a></em>.</p>
<h2 id="editors">Editors</h2>
<p>When you think of a static site generation from a base of Markdown files, it quickly becomes natural to look for a good editor. What we want from our editor:</p>
<ul>
<li>Preview Markdown</li>
<li>Preview including the <span class="caps">CSS</span> and other transformations that our site generator uses - to make sure we see the same result as it will be displayed in production</li>
<li>Preview including images. This might be non trivial since the images might be located on a different path in <span class="caps">DEV</span> as in <span class="caps">PROD</span>…
  Overa ll this means the editor must launch a compilation / composition process that produces the web view every time the Markdown source has been modified.</li>
</ul>
<p>Editor we look at</p>
<table>
<thead>
<tr>
<th style="text-align: left;">Editor</th>
<th style="text-align: left;">Markdown / <span class="caps">HTML</span> Preview</th>
<th style="text-align: left;">Comments</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Visual Code</td>
<td style="text-align: left;">?</td>
<td style="text-align: left;">Might have something suitable</td>
</tr>
<tr>
<td style="text-align: left;">Atom</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">Brackets</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://caret.io/" rel="noopener noreferrer" target="_blank">Caret.io</a></td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><a href="https://ia.net/writer" rel="noopener noreferrer" target="_blank"><span class="caps">IA</span> Writer</a></td>
<td style="text-align: left;">Claims so…</td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>
<p>… probably some more…</p>
<h1 id="history">History</h1>
<ul>
<li>August 2016: Started this page</li>
<li>Jan 2017: Continued while being in Thailand with the family, Tomi <span class="amp">&amp;</span> Beate</li>
</ul>