---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: d4e2f6c72df431d523448eec775c1c31c8e93ef1de0bbf69636297aa134ba4fc
translation-type: automatic
---

[de→fr] <p>I know, there are lots of articles and explanations out there on how to configure and set up your terminal. Yet, it took me more than 2 hours to get things working the way I wanted. Reason was, lots of the articles and explanations provide step by step guide on installing things, but to little background information on how things relate and work together in the background. And that’s what was missing to me…</p>
<p>So here I go with yet another article. Or rather a collection of snippets of the information that I found valuable.</p>
<h2 id="setting-the-scene">Setting the scene</h2>
<p>My target setup <span class="amp">&amp;</span> requirements are simple:</p>
<ul>
<li>macOS (Catalina 10.15.2 at the time of writing)</li>
<li>iTerm2 (Build 3.3.8)</li>
<li>zsh (as provided by Apple since a couple of macOS versions)</li>
<li>I want proper coloring</li>
<li>I want to see what Git branch I am in - if the current directory is within a git repo</li>
</ul>
<h2 id="the-moving-parts">The moving parts</h2>
<p>What made me get lost, was missing overview. Therefore, here are the different bits and pices that are involved in my setup:</p>
<ul>
<li><strong>zsh</strong>: The shell</li>
<li><strong>Oh My Zsh</strong>: A framework that enhances the zsh shell with functions and design.</li>
<li><strong>powerlevel9k</strong>: A theme for Oh My Zsh</li>
<li><strong>Fonts</strong> required by powerlevel9k to display it’s text and icons</li>
</ul>
<p>The dependencies in this list are from top to bottom, i.e. the fonts are required by powerlevel9k that runs on top of Oh My Zsh that uses zsh.</p>
<h2 id="directory-structure">Directory structure</h2>
<p>Before going thru the different components one by one, this is the directory structure we will have after installing all the bits <span class="amp">&amp;</span> pices:</p>
<div class="highlight"><pre><span></span><code>├── $HOME
│   └── .oh-my-zsh/
│   │   └── custom/
│   │   │   └── themes/
│   │   │       └── powerlevel9k/
│   │   └── themes/
│   └── .zsh/
├── .zshrc
</code></pre></div>
<h2 id="zsh">zsh</h2>
<p>I used bash in the past and I was happy with it. I simply started my Mac Terminal, and there it was. And later I used iTerm2, and it also fired up with bash. So why move over to zsh?</p>
<p>This article explains it nicely and extensively. In short:</p>
<ul>
<li>Apple used bash in the past as it was the de-facto standard</li>
<li>In 2007 bash switched to <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" rel="noopener noreferrer" target="_blank"><span class="caps">GNU</span> Public License 3.0</a>, which Apple didn’t like for some reasons. So they stayed with the pre-2007 release of bash. And that’s old - including <a href="https://www.wikiwand.com/en/Shellshock_(software_bug)" rel="noopener noreferrer" target="_blank">a vulnerabilty</a> that forced Apple to update bash for Macs.</li>
<li>zsh over time became the emerging de-facto standard, so Apple moved.</li>
</ul>
<p>And of course, <a href="https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/" rel="noopener noreferrer" target="_blank">zsh offers more modern, cool features</a>.</p>
<p>So anyways, it’s trhe new standard, it looks good - let’s use it. As it’s the new mac standard shell, you don’t need to install it. In case you got a new mac that came with Catalina pre-installed, you are using zsh already. In case you upgraded your Mac from Mojave, you need to set zsh as your terminal shell like so:</p>
<div class="highlight"><pre><span></span><code>chsh<span class="w"> </span>-s<span class="w"> </span>/bin/zsh
</code></pre></div>
<p>This sets zsh as the default Shell.</p>
<h3 id="configuration">Configuration</h3>
<p>Configuring the zsh shell is done via entries in <code>.zshrc</code>, which is located in your <code>$HOME</code> directory. As described above, there are a couple of components that interact. Some of them offer configuration options, and can be configured in different locations. In order to keep an overview, I opted for installing the components in their respective default location, and trying to have all the configuration option in the <code>.zshrc</code> file.</p>
<h2 id="oh-my-zsh">Oh My Zsh</h2>
<blockquote>
<p>Oh My Zsh is an open source, community-driven framework for managing your zsh configuration.
— <cite><a href="https://ohmyz.sh/" rel="noopener noreferrer" target="_blank">Oh My Zsh website</a></cite></p>
</blockquote>
<p>Bascically Oh My Zsh makes your terminal look very nice (via <a href="https://github.com/ohmyzsh/ohmyzsh/wiki/Themes" rel="noopener noreferrer" target="_blank">themes</a>) and offers lots of helpful plugins. An example list from their <a href="https://github.com/ohmyzsh/ohmyzsh" rel="noopener noreferrer" target="_blank">github page</a>:</p>
<div class="highlight"><pre><span></span><code><span class="nv">plugins</span><span class="o">=(</span>
<span class="w">  </span>git
<span class="w">  </span>bundler
<span class="w">  </span>dotenv
<span class="w">  </span>osx
<span class="w">  </span>rake
<span class="w">  </span>rbenv
<span class="w">  </span>ruby
<span class="o">)</span>
</code></pre></div>
<p>I currently use the git plugin, which offers shortcuts for often used git commands.</p>
<h3 id="configuring-oh-my-zsh">Configuring Oh My Zsh</h3>
<p>As mentioned, I have all the configurations integrated in my <code>$HOME/.zshrc</code> file. The relevant snippets from my <code>.zshrc</code>file:</p>
<div class="highlight"><pre><span></span><code><span class="c1"># Path to your oh-my-zsh installation.</span>
<span class="nb">export</span><span class="w"> </span><span class="nv">ZSH</span><span class="o">=</span><span class="s2">"/Users/tgartner/.oh-my-zsh"</span>

<span class="c1"># Set name of the theme to load.</span>
<span class="c1"># See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes</span>
<span class="nv">ZSH_THEME</span><span class="o">=</span><span class="s2">"powerlevel9k/powerlevel9k"</span>

<span class="o">(</span>...<span class="o">)</span>

<span class="c1"># Which plugins would you like to load?</span>
<span class="c1"># Standard plugins can be found in ~/.oh-my-zsh/plugins/*</span>
<span class="c1"># Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/</span>
<span class="c1"># Example format: plugins=(rails git textmate ruby lighthouse)</span>
<span class="c1"># Add wisely, as too many plugins slow down shell startup.</span>
<span class="nv">plugins</span><span class="o">=(</span>git<span class="w"> </span>python<span class="o">)</span>
</code></pre></div>
<h2 id="powerlevel10k">powerlevel10k</h2>
<p>Note: I used to use <a href="https://github.com/Powerlevel9k/powerlevel9k" rel="noopener noreferrer" target="_blank">powerlevel9k</a>, but when installing my Mac in May 2025, 9k was outdated and pointed to <a href="https://github.com/romkatv/powerlevel10k" rel="noopener noreferrer" target="_blank">powerlevel10k</a>.</p>
<p>Install powerlevel10k following their <a href="https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh" rel="noopener noreferrer" target="_blank">installation guide for zsh</a>.</p>