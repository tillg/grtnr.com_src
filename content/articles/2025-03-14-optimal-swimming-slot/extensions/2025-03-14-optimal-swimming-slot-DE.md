---
source-language: en
target-language: de
last-created: 2025-07-03 17:23:23
hash-on-last-created: 1e537df304781d988060f741005dd61009713ccff9c32a05cdc91547f1cbf0c0
translation-type: automatic
---

[en→de] <p><img alt="Pools" src="/optimal-swimming-slot/pools.png"/></p>
<p>As Most of u probably know I live in <a href="https://maps.app.goo.gl/QXy56tXkBf6tJ2s98" rel="noopener noreferrer" target="_blank">Munich/Germany</a>. And since we lived in Vietnam I got hooked on swimming - maybe not really hooked, but I enjoy it. I learned to freestyle for over 1 km in the sea in Vietnam, and from time to time I work on keeping alive this skill here in Munich.</p>
<p>The problem is, in Munich u need a public pool (because I don’t have a private one 😉), and public pools tend to be full <span class="amp">&amp;</span> crowded. Luckily, the <span class="caps">SWM</span> (the Munich public services) provide a <a href="https://www.swm.de/baeder/auslastung" rel="noopener noreferrer" target="_blank">website</a> that tells us how busy the different public swimming pools are.</p>
<p>Even thow I work 40 hours / week (or so…), I might have some flexibility as of when I go swimming: before work, after work, maybe even at lunchtime. And the question arises, when best to go. When are the pools the less crowded?</p>
<p>For example: I suspect that going as early as possible in the morning is not the smartest, as many sportive white-collar worker do so. So maybe it’s smarter to have tea with my wife in the morning, and then go for a swim and to the office.</p>
<p>The best about this problem: it’s a typical machine learning problem 😉</p>
<p>So this would be the plan:</p>
<ul>
<li>Build a scraper that gathers the pool occupancy every 10 minutes and stores it somewhere</li>
<li>Train a machine learning model on that data</li>
<li>Build a <span class="caps">UI</span> that asks when u could go, and that gives u advice when u should go</li>
<li>Extra features: take into account week-ends and public holidays, pool-features (i.e. I prefer swimming in a 50m pool)</li>
</ul>
<p>Anyone up for building such a tool? Send me an email if u want to hack 😉</p>