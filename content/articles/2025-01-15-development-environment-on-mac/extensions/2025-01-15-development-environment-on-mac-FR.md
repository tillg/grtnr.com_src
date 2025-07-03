---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 7033de83ddf5f709d1c0537cf7c17d163ddf109292658515b549fc5ba7986c8f
translation-type: automatic
---

[de→fr] <p><img alt="Funny pic from AI" src="/development-environment-on-mac/dev_tools.png"/></p>
<p>I am not a professional developer, I do it for fun. And I like to play around, discover new technologies,. development all kinds of little things. So sometimes I need Python, sometimes React/Typescript, Java and more. For every development tool or langugae there are multiple options on how to install them and manage their versions. Since I tend to forget things like “How did I install Python oin this machine?”, this is a note to future me, telling me how I installed every development tool.</p>
<p>As the way how certain packages are installed might change over time, I will add dates to my installation choices.</p>
<div class="toc">
<ul>
<li><a href="#xcode">Xcode</a></li>
<li><a href="#terminal">Terminal</a></li>
<li><a href="#zsh-shell">zsh shell</a></li>
<li><a href="#vscode">VSCode</a></li>
<li><a href="#docker">Docker</a></li>
<li><a href="#java">Java</a></li>
<li><a href="#maven">Maven</a></li>
<li><a href="#gradle">Gradle</a></li>
<li><a href="#node-and-npm">Node and npm</a></li>
<li><a href="#python">Python</a></li>
<li><a href="#ruby">Ruby</a></li>
</ul>
</div>
<h2 id="xcode">Xcode</h2>
<p>Xcode is the basic dev tooling on Mac. It contains git and other basic tools and compilers.</p>
<p>I install it from the Apple App Store.</p>
<h2 id="terminal">Terminal</h2>
<p>My Terminal of choice is <a href="https://iterm2.com" rel="noopener noreferrer" target="_blank">iTerm2</a>, and I simply install it from it’s website. See <a href="/setting-up-my-terminal/">here</a> for how I configure it.</p>
<h2 id="zsh-shell">zsh shell</h2>
<p>On a new Mac, here is what I do:</p>
<div class="highlight"><pre><span></span><code><span class="c1"># Check what Shell I have</span>
<span class="nb">echo</span><span class="w"> </span><span class="s2">"</span><span class="nv">$SHELL</span><span class="s2">"</span>

<span class="c1"># In case it's not zsh, set it as default</span>
chsh<span class="w"> </span>-s<span class="w"> </span><span class="s2">"</span><span class="k">$(</span>which<span class="w"> </span>zsh<span class="k">)</span><span class="s2">"</span>
</code></pre></div>
<h2 id="vscode">VSCode</h2>
<p>… or VSCode-insiders</p>
<h2 id="docker">Docker</h2>
<p><strong>January 2025:</strong> I switched away from <a href="https://www.docker.com/products/docker-desktop/" rel="noopener noreferrer" target="_blank">Docker Desktop</a> to <a href="https://rancherdesktop.io" rel="noopener noreferrer" target="_blank">Rancher Desktop</a>.</p>
<p>Installation note: Downloaded the Apple Silicon version, opened the <span class="caps">DMG</span> and copied it into my Applications directory. The only detail I needed to do, is tick the “Administrative Access” checkbox in the setting.
<img alt="alt text" src="/development-environment-on-mac/rancher_prefs.png"/></p>
<p><em>Registry</em>: I use different registries when working on different projects.</p>
<p><em>Question</em>: How do I configure docker so that it pulls images from a specific registry?</p>
<h2 id="java">Java</h2>
<p>These are the option I saw:</p>
<ul>
<li><a href="https://github.com/jenv/jenv" rel="noopener noreferrer" target="_blank">jenv</a></li>
<li><a href="https://sdkman.io" rel="noopener noreferrer" target="_blank"><span class="caps">SDK</span> man</a></li>
</ul>
<p><strong>Januar 2025</strong>: I decided to use <span class="caps">SDK</span> Man as it also covers Maven.</p>
<p><strong>Mini-Cheatsheet</strong></p>
<ul>
<li><code>sdk install java 17.0.12-jbr</code> install this specific Jaa version</li>
<li><code>sdk list java</code> shows all available Java version (available to install)</li>
<li>To list the installed java versions:</li>
<li><code>sdk oofline enable</code>, so it will list only locally installed versions</li>
<li><code>sdk list java</code></li>
<li><code>sdk offline disable</code></li>
<li><code>sdk default java 21.0.6-amzn</code> sets this version as default
  To set a java version as default inside a directory, see the <a href="https://sdkman.io/usage/#env-command" rel="noopener noreferrer" target="_blank">Env command</a></li>
</ul>
<h2 id="maven">Maven</h2>
<p>I simply use <code>brew install maven</code>. For older version <code>brew install maven30</code> installs Maven 3.0.</p>
<h2 id="gradle">Gradle</h2>
<p><strong>January 2025</strong>: I decide to use <span class="caps">SDK</span> Man for Gradle as well.</p>
<p>Reason: <code>brew install gradle</code> installed Gradle Version 8.12.1, but for the current Project I needed 8.5.</p>
<ul>
<li><code>sdk install gradle 8.5</code>: Installs teh specific gradle version</li>
<li><code>sdk use gradle 8.5</code></li>
</ul>
<h2 id="node-and-npm">Node and npm</h2>
<p><strong>January 2025</strong> I decided to use <a href="https://github.com/nvm-sh/nvm" rel="noopener noreferrer" target="_blank">nvm</a>.</p>
<p><strong>Mini-Cheatsheet</strong></p>
<ul>
<li><code>nvm use 16</code></li>
<li><code>node -v</code> shows the version currently being used</li>
<li><code>nvm install 12</code> installs node 12 and uses it</li>
</ul>
<h2 id="python">Python</h2>
<ul>
<li><strong>Summer 2024</strong>:I use <a href="https://github.com/pyenv/pyenv" rel="noopener noreferrer" target="_blank">pyenv</a></li>
<li>To install pyenv: <code>brew install pyenv</code></li>
</ul>
<p><strong>Mini-Cheatsheet</strong></p>
<p>Select a Pyenv-installed Python as the version to use, run one of the following commands:</p>
<div class="highlight"><pre><span></span><code>pyenv<span class="w"> </span>install<span class="w"> </span><span class="m">3</span>.12
pyenv<span class="w"> </span>shell<span class="w"> </span>&lt;version&gt;<span class="w"> </span>--<span class="w"> </span><span class="k">select</span><span class="w"> </span>just<span class="w"> </span><span class="k">for</span><span class="w"> </span>current<span class="w"> </span>shell<span class="w"> </span>session
pyenv<span class="w"> </span><span class="nb">local</span><span class="w"> </span>&lt;version&gt;<span class="w"> </span>--<span class="w"> </span>automatically<span class="w"> </span><span class="k">select</span><span class="w"> </span>whenever<span class="w"> </span>you<span class="w"> </span>are<span class="w"> </span><span class="k">in</span><span class="w"> </span>the<span class="w"> </span>current<span class="w"> </span>directory<span class="w"> </span><span class="o">(</span>or<span class="w"> </span>its<span class="w"> </span>subdirectories<span class="o">)</span>
pyenv<span class="w"> </span>global<span class="w"> </span>&lt;version&gt;<span class="w"> </span>--<span class="w"> </span><span class="k">select</span><span class="w"> </span>globally<span class="w"> </span><span class="k">for</span><span class="w"> </span>your<span class="w"> </span>user<span class="w"> </span>account
</code></pre></div>
<h2 id="ruby">Ruby</h2>
<p>Not thought yet. Avoid Ruby in general… 😉</p>