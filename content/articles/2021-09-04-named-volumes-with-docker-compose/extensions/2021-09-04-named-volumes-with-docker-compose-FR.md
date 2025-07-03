---
source-language: en
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: bece392770213a0b4ec0545c21f7c35f20ef22056dbd013d44b1aa26f5153339
translation-type: automatic
---

[en→fr] <p>While working on a side project that uses <strong>docker-compose</strong>, I stumbled over a problem. One that I had encountered before but had never properly investigated or solved.</p>
<p>Here is what I want to do:</p>
<ul>
<li>Have a bunch of services running within a docker-compose setup</li>
<li>Have those services use mounted shares - one share, used by more than one container.</li>
<li>The problematic thing: I want <strong>multiple containers</strong> to use the <strong>same volume</strong>!</li>
</ul>
<p>Make a long story short, here is how it works smoothly:</p>
<div class="highlight"><pre><span></span><code><span class="nx">version</span><span class="p">:</span><span class="w"> </span><span class="sc">'3'</span>
<span class="nx">services</span><span class="p">:</span>
<span class="w">  </span><span class="nx">service1</span><span class="p">:</span>
<span class="w">    </span><span class="nx">image</span><span class="p">:</span><span class="w"> </span><span class="nx">nginx</span>
<span class="w">    </span><span class="nx">container_name</span><span class="p">:</span><span class="w"> </span><span class="nx">service1</span>
<span class="w">    </span><span class="nx">ports</span><span class="p">:</span>
<span class="w">      </span><span class="o">-</span><span class="w"> </span><span class="err">'</span><span class="mi">81</span><span class="p">:</span><span class="mi">80</span><span class="err">'</span>
<span class="w">    </span><span class="nx">volumes</span><span class="p">:</span>
<span class="w">      </span><span class="o">-</span><span class="w"> </span><span class="nx">content</span><span class="p">:</span><span class="o">/</span><span class="nx">usr</span><span class="o">/</span><span class="nx">share</span><span class="o">/</span><span class="nx">nginx</span><span class="o">/</span><span class="nx">html</span>

<span class="w">  </span><span class="nx">service2</span><span class="p">:</span>
<span class="w">    </span><span class="nx">image</span><span class="p">:</span><span class="w"> </span><span class="nx">nginx</span>
<span class="w">    </span><span class="nx">container_name</span><span class="p">:</span><span class="w"> </span><span class="nx">service2</span>
<span class="w">    </span><span class="nx">ports</span><span class="p">:</span>
<span class="w">      </span><span class="o">-</span><span class="w"> </span><span class="err">'</span><span class="mi">82</span><span class="p">:</span><span class="mi">80</span><span class="err">'</span>
<span class="w">    </span><span class="nx">volumes</span><span class="p">:</span>
<span class="w">      </span><span class="o">-</span><span class="w"> </span><span class="nx">content</span><span class="p">:</span><span class="o">/</span><span class="nx">usr</span><span class="o">/</span><span class="nx">share</span><span class="o">/</span><span class="nx">nginx</span><span class="o">/</span><span class="nx">html</span>

<span class="nx">volumes</span><span class="p">:</span>
<span class="w">  </span><span class="nx">content</span><span class="p">:</span>
<span class="w">     </span><span class="nx">driver_opts</span><span class="p">:</span>
<span class="w">           </span><span class="k">type</span><span class="p">:</span><span class="w"> </span><span class="nx">none</span>
<span class="w">           </span><span class="nx">device</span><span class="p">:</span><span class="w"> </span><span class="p">.</span><span class="o">/</span><span class="nx">data</span><span class="o">/</span><span class="nx">content</span>
<span class="w">           </span><span class="nx">o</span><span class="p">:</span><span class="w"> </span><span class="nx">bind</span>
</code></pre></div>
<p>That’s what’s going on:</p>
<ul>
<li>We have 2 services of the same type: plain nginx containers for demo purposes.</li>
<li>They both expose their (internal) port 80 to port 81 resp. 82 to the outside world.</li>
<li>They both use a volume called <strong>content</strong> that is defined in the volumes section.</li>
</ul>
<p>The detail that I missed for so long was the <strong>volumes</strong> section with the <strong>driver_opts</strong>. And while I ran a couple of tests and everything behaved exactly the way I hoped, I couldn’t find any proper documentation. Here’s what the <a href="https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts" rel="noopener noreferrer" target="_blank">docker documentation</a> says about <strong>driver_opts</strong>:</p>
<blockquote>
<p>Specify a list of options as key-value pairs to pass to the driver for this volume. Those options are driver-dependent - consult the driver’s documentation for more information.</p>
</blockquote>
<p>When investigating how things are working, docker’s inspect tools give some insights: This is the <strong>Mounts</strong> part of <strong>docker inspect service1</strong></p>
<div class="highlight"><pre><span></span><code><span class="w"> </span><span class="s2">"Mounts"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span>
<span class="w">            </span><span class="p">{</span>
<span class="w">                </span><span class="s2">"Type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"volume"</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"Name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"docker-playground_content"</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"Source"</span><span class="p">:</span><span class="w"> </span><span class="s2">"/var/lib/docker/volumes/docker-playground_content/_data"</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"Destination"</span><span class="p">:</span><span class="w"> </span><span class="s2">"/usr/share/nginx/html"</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"Driver"</span><span class="p">:</span><span class="w"> </span><span class="s2">"local"</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"Mode"</span><span class="p">:</span><span class="w"> </span><span class="s2">"rw"</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"RW"</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="p">,</span>
<span class="w">                </span><span class="s2">"Propagation"</span><span class="p">:</span><span class="w"> </span><span class="s2">""</span>
<span class="w">            </span><span class="p">}</span>
<span class="w">        </span><span class="p">]</span>
</code></pre></div>
<p>At first I was sceptic because of this line:</p>
<div class="highlight"><pre><span></span><code><span class="s2">"Source"</span><span class="p">:</span><span class="w"> </span><span class="s2">"/var/lib/docker/volumes/docker-playground_content/_data"</span>
</code></pre></div>
<p>But it turns out my data is <strong>not</strong> in this docker-managed directory, but where I wanted it. In my case that’s in <strong>./data/content</strong>. Also the relative path works fine.</p>
<h3 id="sources">Sources</h3>
<p>Here are the original sources that helped me most</p>
<ul>
<li>Docker documentation - strange enough, it dodn’t help at all…</li>
<li>This was the most helpful <a href="https://stackoverflow.com/questions/35841241/docker-compose-named-mounted-volume" rel="noopener noreferrer" target="_blank">Stackoverflow article</a>.</li>
</ul>
<h3 id="versions">Versions</h3>
<p>Since these kind of setups might be version sensitive, here is my setup:</p>
<div class="highlight"><pre><span></span><code>docker-compose version 1.29.2, build 5becea4c
docker-py version: 5.0.0
CPython version: 3.9.0
OpenSSL version: OpenSSL 1.1.1h  22 Sep 2020
</code></pre></div>
<p>And it runs on my Mac with Big Sur Version 11.5.2 (wit h Intel <span class="caps">CPU</span> 😜).</p>
<p>The code can be found <a href="https://github.com/tillg/docker-compose-volumes-playground/" rel="noopener noreferrer" target="_blank">on Github</a>.</p>