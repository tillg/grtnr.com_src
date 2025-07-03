---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 59c33f06f55529f65a31b1127693101d592cf4babd8941f34b4abcc2856fcfc1
translation-type: automatic
---

[de→fr] <p>Good software developers test their stuff. And the <a href="https://www.wikiwand.com/en/Test-driven_development" rel="noopener noreferrer" target="_blank"><span class="caps">TDD</span> (Test Driven Development)</a> addicts are maniacs when it comes to testing. Those guys usually think in code, be it Java, Python, nodeJS, you name it. <span class="caps">TDD</span> means you write tests first, then you code just as much as it takes to let the tests become green. Then you rework your code and only then you start writing tests for new requirements.
<img alt="TDD Process" src="/siteweightwatcher-keeps-your-website-slim/tdd.png"/></p>
<p>This is <strong>very</strong> testy. My opinion is that if you do it the way it’s written and described in the books you become awfully slow and it turns into nonsense. But that’s another discussion, and not one I want to sort out here…</p>
<p>What’s missing with most of the test approaches I have seen in the past are the following two things:</p>
<ol>
<li>The test guys and test tools stop monitoring the software or website once it went into production. Somehow they feel that their responsibility ends with the going live…</li>
<li>They test the software. Not the rest, I.e. The design, the <span class="caps">HTML</span>, the <span class="caps">CSS</span> etc. And the user experience, the feeling wether what I see, touch, browse navigate is of good quality, is very much influenced by this packaging of the software logic.</li>
</ol>
<p>So I am looking for a tool to test (web based) software once it’s out in the wild and throughout the entire user experience. Imagine a website, a simple blog. It might be perfect when it got launched, but over time it just degrades: the designers have added so many bells and whistles, the volume of the content has grown, it was tweaked to be more useable on mobiles… And eventually the site is bloated, heavy and slow. Why do I have to wait for my users to tell me (that would be complaining)?</p>
<p>At <a href="https://mgm-tp.com" rel="noopener noreferrer" target="_blank">mgm technology partners</a> we have automated test suites that run every night. So developers that built in code that slows down the software have a report that tells them every morning in their inbox.</p>
<p>So here is what my SiteWeightWatcher should do:</p>
<ul>
<li>Run tests every 5-30 minutes against the production site</li>
<li>Check all the pages, not just index.html</li>
<li>Report immediately when pages become slow (that would be slower than they used to be)</li>
<li>Track key figures and how they evolve over time:</li>
<li>How much data is transferred for each page?</li>
<li>How many requests are going back <span class="amp">&amp;</span> forth?</li>
<li>How much time does it take searching for products? Over time…</li>
<li>How well connected is the site for users in Germany, <span class="caps">UK</span>, <span class="caps">US</span> or Asia? Over time, because those things change without us having done anything.</li>
</ul>
<p>I could imagine a dashboard for an online shop like <a href="https://www.kickz.com/de" rel="noopener noreferrer" target="_blank"><span class="caps">KICKZ</span>.com</a> to look may this way:
<img alt="Deshboard scribble" src="/siteweightwatcher-keeps-your-website-slim/kickz_dashboard.png"/>A Dashboard that shows how page sizes evolve</p>
<p>And just as the normal test teams do, these tests should also evolve and become more and more adapted to the site, it’s functionality and its users. Whenever we have a real problem or bug out there, we have to make sure that our WeightWatcher will find it in case it should appear or happen again.</p>
<p>How could we start to build such a tool? Some thoughts:</p>
<ul>
<li>We have agents and a central server. The agents are located all around the globe or in different networks (think of little Docker images that run on different clouds). They report all their captured data to the central server. This is where the reports are generated and where interactive explication of the data is provided.</li>
<li>The agents start collecting simple metrics:</li>
<li>No of <span class="caps">HTTP</span> requests per page</li>
<li>Data transferred per page</li>
<li>No of lines of JavaScript per page</li>
<li>Time to load the data</li>
<li>Time to execute JavaScript</li>
<li>Based on this we start with simple reports:</li>
<li>What’s the average page size?</li>
<li>What’s the average no of requests per page?</li>
<li>What are my <em>heaviest</em> pages?</li>
<li>A graph that shows availability of my site as well as load time over a 24h scale, a week scale, a month. May be my users only experience slow loading in the evenings.</li>
</ul>
<p>From there we we extend the data we collect as well as the reports.</p>
<p>Such a tool would be great to monitor sites that I am in charge of (I.e. websites that we have developed at mgm) but could also give valuable information about other market players. It could be used both by technical people as well as the marketing guys - since they also <em>sometimes</em> break performance. I would be curious to see this kind of stats for Zalando 😜</p>
<p>Does anyone know about such a monitoring system? Please let me know.</p>