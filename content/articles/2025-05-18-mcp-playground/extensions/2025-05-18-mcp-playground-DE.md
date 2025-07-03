---
source-language: en
target-language: de
last-created: 2025-07-03 17:23:23
hash-on-last-created: 1c3aa9204681ea87c2ca715d9af8e740b8cb8c72ceb2b9f76e05481d19cc10f3
translation-type: automatic
---

[en→de] <p>Notes about findings and <em>understandings</em> around <a href="https://modelcontextprotocol.io/introduction" rel="noopener noreferrer" target="_blank">Model Context Protocol aka _MCP</a>.</p>
<div class="toc">
<ul>
<li><a href="#questions">Questions</a></li>
<li><a href="#accessing-a-mcp-server">Accessing a <span class="caps">MCP</span> server</a></li>
<li><a href="#mcp-servers"><span class="caps">MCP</span> Servers</a><ul>
<li><a href="#filesystem-mcp-server">Filesystem <span class="caps">MCP</span> Server</a></li>
</ul>
</li>
<li><a href="#mcp-servers_1"><span class="caps">MCP</span> Servers</a><ul>
<li><a href="#filesystem-access">FileSystem Access</a></li>
<li><a href="#xcode-build">Xcode Build</a></li>
</ul>
</li>
</ul>
</div>
<h2 id="questions">Questions</h2>
<p>Open questions that I have.</p>
<ul>
<li>Can I run Claude with different <span class="caps">MCP</span> Server configurations? I.e. I have one configuration per project, say one for my Python project (including access only to my Python project directory), one for my Swift/Xcode project (with a different dir and different tools).</li>
<li>Test: Play around with <span class="caps">MCP</span> Inspector and <a href="https://github.com/cameroncooke/XcodeBuildMCP" rel="noopener noreferrer" target="_blank">Xcode Build <span class="caps">MCP</span> Server</a>.</li>
</ul>
<h2 id="accessing-a-mcp-server">Accessing a <span class="caps">MCP</span> server</h2>
<p>When searching and eventually finding an <span class="caps">MCP</span> server for my use case, I find it helpful to play around with them, in order to <em>understand</em> what tooling the <span class="caps">LLM</span> gets. The easiest way to do this is with the <a href="https://github.com/modelcontextprotocol/inspector" rel="noopener noreferrer" target="_blank"><span class="caps">MCP</span> Inspector</a>.</p>
<p>Get going:</p>
<div class="highlight"><pre><span></span><code><span class="c1"># Make sure you have installed a recent version of nodeJs (in my case with nvm)</span>
nvm<span class="w"> </span>use<span class="w"> </span><span class="m">24</span>
npx<span class="w"> </span>@modelcontextprotocol/inspector<span class="w"> </span>node<span class="w"> </span>build/index.js

<span class="c1"># It downloads &amp; starts the MCP UI Client and serves it locally.</span>
</code></pre></div>
<p><strong>Configuration</strong></p>
<p>The Inspector keeps whatever you type in the sidebar in localStorage, but for repeatable setups you can save a tiny <span class="caps">JSON</span> file and point the <span class="caps">CLI</span> to it:</p>
<div class="highlight"><pre><span></span><code><span class="c1">// mcp.json</span>
<span class="p">{</span>
<span class="w">  </span><span class="nt">"mcpServers"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="w">    </span><span class="nt">"filesystem"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="w">      </span><span class="nt">"command"</span><span class="p">:</span><span class="w"> </span><span class="s2">"npx"</span><span class="p">,</span>
<span class="w">      </span><span class="nt">"args"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span>
<span class="w">        </span><span class="s2">"-y"</span><span class="p">,</span>
<span class="w">        </span><span class="s2">"@modelcontextprotocol/server-filesystem"</span><span class="p">,</span>
<span class="w">        </span><span class="s2">"/Users/yourname/Projects"</span><span class="p">,</span><span class="w"> </span><span class="c1">// read/write</span>
<span class="w">        </span><span class="s2">"/Users/yourname/Notes"</span><span class="p">,</span><span class="w"> </span><span class="c1">// read/write</span>
<span class="w">        </span><span class="s2">"/Users/yourname/Code"</span><span class="w"> </span><span class="c1">// read-only? add ',ro' if you use Docker</span>
<span class="w">      </span><span class="p">]</span>
<span class="w">    </span><span class="p">}</span>
<span class="w">  </span><span class="p">}</span>
<span class="p">}</span>
</code></pre></div>
<p>Then run <code>npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem</code></p>
<h2 id="mcp-servers"><span class="caps">MCP</span> Servers</h2>
<p><span class="caps">MCP</span> Servers I used or looked at:</p>
<h3 id="filesystem-mcp-server">Filesystem <span class="caps">MCP</span> Server</h3>
<ul>
<li><a href="https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem" rel="noopener noreferrer" target="_blank">Filesystem <span class="caps">MCP</span> Server</a></li>
<li>One of the <a href="https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#-reference-servers" rel="noopener noreferrer" target="_blank">Reference Servers</a></li>
</ul>
<p>Main config:</p>
<div class="highlight"><pre><span></span><code><span class="p">{</span>
<span class="w">  </span><span class="nt">"mcpServers"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="w">    </span><span class="nt">"filesystem"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span>
<span class="w">      </span><span class="nt">"command"</span><span class="p">:</span><span class="w"> </span><span class="s2">"npx"</span><span class="p">,</span>
<span class="w">      </span><span class="nt">"args"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span>
<span class="w">        </span><span class="s2">"-y"</span><span class="p">,</span>
<span class="w">        </span><span class="s2">"@modelcontextprotocol/server-filesystem"</span><span class="p">,</span>
<span class="w">        </span><span class="s2">"/Users/username/Desktop"</span><span class="p">,</span>
<span class="w">        </span><span class="s2">"/path/to/other/allowed/dir"</span>
<span class="w">      </span><span class="p">]</span>
<span class="w">    </span><span class="p">}</span>
<span class="w">  </span><span class="p">}</span>
<span class="p">}</span>
</code></pre></div>
<h2 id="mcp-servers_1"><span class="caps">MCP</span> Servers</h2>
<p><span class="caps">MCP</span> Servers I tested or plan to test.</p>
<h3 id="filesystem-access">FileSystem Access</h3>
<h3 id="xcode-build">Xcode Build</h3>
<p><img alt="Xcode Build" src="/mcp-playground/xcode_build.png"/></p>
<ul>
<li>Enables Xcode build actions.</li>
<li>https://github.com/cameroncooke/XcodeBuildMCP</li>
</ul>