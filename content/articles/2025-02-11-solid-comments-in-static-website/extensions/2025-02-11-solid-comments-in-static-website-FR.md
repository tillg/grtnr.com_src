---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 2874836d1997d93f99163c8d5920e3aa86f8eb8e596cd57752d40a8b3f87c875
translation-type: automatic
---

[de→fr] <p><strong><span class="caps">TL</span>;<span class="caps">DR</span>:</strong> I added comments to my static website. Here’s how I did it - including some technical details. I researched amongst different possible solutions for the most solid one, integrated it for all posts and added a counter of the number of comments in the post overview page.</p>
<p><strong>2025-05-23 Update</strong> Since I moved from Jekyll to <a href="https://getpelican.com" rel="noopener noreferrer" target="_blank">Pelican</a>, I updated some details.</p>
<h2 id="selecting-a-solution">Selecting a solution</h2>
<p>As i planned to play around with the new <a href="https://openai.com/index/introducing-deep-research/" rel="noopener noreferrer" target="_blank">Deep Research Model from OpenAI</a> I gave it a spin with this topic: <a href="https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776" rel="noopener noreferrer" target="_blank">feel free to read here</a>. Overall the research was helpful and I ended up using <a href="https://giscus.app/" rel="noopener noreferrer" target="_blank">Giscus</a> for the comments. Partly because it felt the most robust and reliable, partly because I had really bad expoerience with disqus some years ago.</p>
<p>The choice was based on the set of criteria I gave to the model. Here are the most important ones:</p>
<ul>
<li>No self-hosted server – I don’t want to manage (and pay 😉) a server.</li>
<li>Data portability – the comments can exported.</li>
<li>Privacy-friendly – no extra trackers or ads beyond what I already use (e.g. Google Analytics).</li>
<li>Markdown support – allow rich formatting (code blocks, etc.) suited for technical discussions.</li>
<li>Spam protection – has measures to reduce spam, especially if allowing anonymous or unauthenticated comments.</li>
</ul>
<p>The tools that Deep Research <em>analyzed</em> were</p>
<ul>
<li>Giscus</li>
<li>Utterances</li>
<li>Staticman</li>
<li>Commento</li>
<li>Hyvor Talk</li>
<li>Disqus</li>
<li>Some <em>self made</em> solutions</li>
</ul>
<h2 id="integrating-giscus">Integrating Giscus</h2>
<p>In the follow up to it’s research I asked the model to give me a step by step guide on how to integrate the solution. This was far less reliable than the first research, but still helpful.</p>
<p>Here is the executive summary (the details are in the <a href="https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776" rel="noopener noreferrer" target="_blank">chat I had with the <span class="caps">AI</span></a>):</p>
<ul>
<li>Step 1: Enable GitHub Discussions for Your Repository. That means the repo into which the static site is generated (which sometimes is not the same as the source).</li>
<li>Go to your GitHub repository</li>
<li>Navigate to Settings &gt; General.</li>
<li>Scroll down to the Discussions section and enable it.</li>
<li>Step in between, that the <span class="caps">AI</span> missed to mention: Install giscus for all or some of your repos. <a href="https://github.com/apps/giscus/installations/select_target" rel="noopener noreferrer" target="_blank">Here</a>
<img alt="alt text" src="/solid-comments-in-static-website/image.png"/></li>
<li>Step 2: Install Giscus and Configure It</li>
<li>Visit the Giscus setup page: https://giscus.app/.</li>
<li>Under “Repository”, enter your repo name. You now should see the green check mark that your repo meets all the criteria for using giscus.</li>
<li>The “Page discussion mapping” option dictates a relationship between your pages, e.g an article, and a GitHub discussion. I selected, the pathname</li>
<li>For the discussions category I selected “general”.
    Set the Theme to “Match <span class="caps">OS</span>” or manually define light and dark mode.
    Click “Copy Code” once you’ve generated the <script></script></li></ul>