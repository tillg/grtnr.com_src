---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 461e5070de4765bf346a97f04b0d0c6e121fb394aaa26206a062ec3a3b53a392
translation-type: automatic
---

[de→fr] <p>So this is the situation I am facing: I use an internet access that doesn’t feel reliable. Sometimes it’s really fast, sometimes it just feels being very unreliable. And I never know what part exactly is just failing: Is the the application that is slow, is it the <span class="caps">WIFI</span>, is it the Internet access.</p>
<p>So want I have been looking for is a reliable, long-term measurement of internet access speed. By speed I mean mainly round-trip time / latency. I looked at many tools, large ones (the ones that come from complete eco systems like Nagios or ecinga) small one (i.e. network usage tracking directly on your <span class="caps">PC</span> or Mac). The big ones are too much work and too much stuff that needs to be learned, understood, installed. The small ones don’t answer my question since they don’t do long term tracking and recording. And I don’t like complex stuff.</p>
<p>Then found something that is in the essence exactly what I have been looking for. Re-phrtase: If I would have started putting something together myself, this is what I would have built: It’s called <a href="http://www.medienvilla.com/entwicklung.html#pinganalyse" rel="noopener noreferrer" target="_blank">Ping Visualization and Analysis</a> and it is based on 2 components;</p>
<ul>
<li>One simple script that logs ping times (and by simple I mean <em>realy simple!</em>)</li>
<li>One <span class="caps">HTML</span> page with some JavaScript that visualizes the ping times over time.</li>
</ul>
<p>You can let the ping-logger run on stupid simple hardware. It can run day <span class="amp">&amp;</span> night, gathering data. The format is <em>plain</em>. A sample:</p>
<div class="highlight"><pre><span></span><code>Fri Jan  8 15:14:49 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=89 ttl=53 time=310.716 ms
Fri Jan  8 15:14:54 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=90 ttl=53 time=310.349 ms
Fri Jan  8 15:14:59 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=91 ttl=53 time=312.787 ms
Fri Jan  8 15:15:04 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=92 ttl=53 time=312.805 ms
Fri Jan  8 15:15:09 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=93 ttl=53 time=311.273 ms
Fri Jan  8 15:15:14 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=94 ttl=53 time=311.371 ms
Fri Jan  8 15:15:19 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=95 ttl=53 time=312.096 ms
Fri Jan  8 15:15:24 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=96 ttl=53 time=313.387 ms
Fri Jan  8 15:15:29 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=97 ttl=53 time=310.404 ms
Fri Jan  8 15:15:34 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=98 ttl=53 time=311.076 ms
Fri Jan  8 15:15:39 ICT 2016: 64 bytes from 185.40.248.50: icmp_seq=99 ttl=53 time=312.640 ms
</code></pre></div>
<p>Pretty simple, uh?! A simple <code>ping</code> with a timestamp in front. And the <span class="caps">JS</span> stuff reads it and makes a simple graph from it:</p>
<p><img alt="graph" src="/ping-visualization-and-analysis/ping.png"/></p>
<p>I just had to fix some small things to make it run on my Mac (the <code>ping</code> syntax was from another Unix slang).</p>
<h2 id="what-next">What next?</h2>
<p>So here is what I plan to improve (let’s see wether this really happens):</p>
<ul>
<li>Have the Sources GITted</li>
<li>Improve the graph:</li>
<li>The colors are a bit strange to me…</li>
<li>It feels upside down</li>
<li>Have labels on the y axis</li>
<li>May be have them more <a href="http://pinglogger.co.uk/index.php/screenshots/" rel="noopener noreferrer" target="_blank">like so</a></li>
<li>May be look into <a href="https://www.elastic.co/products/logstash" rel="noopener noreferrer" target="_blank">log stash</a> as visualization…</li>
</ul>
<h2 id="addendum">Addendum</h2>
<p>Also within the context, and because <a href="http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html" rel="noopener noreferrer" target="_blank">Java is the development language of the year 2015</a>: <a href="http://pastebin.com/1qnCXDw7" rel="noopener noreferrer" target="_blank">A java program to track the ping times to multiple end points</a></p>