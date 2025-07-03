---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: e9efb8cbbfdf8c25b6429ef6055502c4d9c9ccffd0deece3f26bf5328cdb8392
translation-type: automatic
---

[de→fr] <p>Setting up Python on a Mac can by tricky. The number of options is big, and they might interact strangely. Also you have to remember which installation method you used once you want to change version or upgrade. This post should remind me how I did it 😉</p>
<h2 id="installing-python">Installing Python</h2>
<p>There are many ways to install Python on Mac and to manage it’s versions:</p>
<ul>
<li>The Python installed on MacOS</li>
<li><code>brew</code></li>
<li>Anaconda</li>
<li><code>pyenv</code></li>
<li>…</li>
</ul>
<p>What worked best for me is <strong>pyenv</strong>:</p>
<ul>
<li>Install it: <code>brew install pyenv</code>. I assume you have <a href="https://brew.sh" rel="noopener noreferrer" target="_blank">Homebrew</a> installed…</li>
<li>See the options and commands offered: <code>pyenv</code></li>
<li>List all Python versions available to pyenv: <code>pyenv versions</code></li>
<li>Install a version: <code>pyenv install 3.12</code> (That’s the Python version I currently use)</li>
<li>Set the version that is globally used: <code>pyenv global 3.12</code></li>
<li>Check what version is globally set: <code>pyenv global</code> or <code>python --version</code></li>
</ul>
<h2 id="create-working-directory">Create working directory</h2>
<p>Create the directory in which you want to work in the context of your project. I keep all my coding projects under <code>~/git</code>. This way I know that all the projects under <code>~/git</code> don’t need to be backed up as they are in a git repo.</p>
<p>Example:</p>
<div class="highlight"><pre><span></span><code><span class="nb">cd</span><span class="w"> </span>~/git
mkdir<span class="w"> </span>my_python_project
<span class="nb">cd</span><span class="w"> </span>my_python_project
</code></pre></div>
<h2 id="create-a-local-env">Create a local env</h2>
<p>In order to provide my project it’s own python environment I use <a href="https://docs.python.org/3/library/venv.html" rel="noopener noreferrer" target="_blank">Python’s Virtual Environments</a>:</p>
<div class="highlight"><pre><span></span><code><span class="nb">cd</span><span class="w"> </span>~/git/my_python_project
python3.12<span class="w"> </span>-m<span class="w"> </span>venv<span class="w"> </span>.venv
</code></pre></div>
<p>This way I have created an environement inside the <code>.env</code> sub-dir. To activate it use <code>source .venv/bin/activate</code>.</p>
<p><strong>Note</strong>: As my <code>.env</code> sub-directory should not be in the git repo, it needs to be listed in the <code>.gitignore</code> file.</p>
<h2 id="install-jupyter-lab">Install Jupyter Lab</h2>
<p>Now that I have the Python environment I can install Jupyter. Make sure I am in the right directory and the Python environment is activated:</p>
<div class="highlight"><pre><span></span><code><span class="c1"># Go in my project dir and activate it's Python environment</span>
<span class="nb">cd</span><span class="w"> </span>~/git/my_python_project
<span class="nb">source</span><span class="w"> </span>.venv/bin/activate

<span class="c1"># Install Jupyter Lab in this environment</span>
pip<span class="w"> </span>install<span class="w"> </span>jupyterlab

<span class="c1"># Very often it asks me to upgrade pip itself</span>
pip<span class="w"> </span>install<span class="w"> </span>--upgrade<span class="w"> </span>pip

<span class="c1"># Start Jupyter Lab</span>
jupyter<span class="w"> </span>lab
<span class="c1"># Now wait a bit and your browser should open on http://localhost:8888/lab</span>
</code></pre></div>
<h2 id="create-a-new-notebook">Create a new notebook</h2>
<p>Your browser should be open in a fresh Jupyter Lab environment:
<img alt="An empty Lab environment" src="/setting-up-jupyter-lab-on-mac/jupyter_overview.png"/></p>
<p>Click on <em>Notebook &gt; Python 3</em> and your first Notebook should be up <span class="amp">&amp;</span> running:</p>
<p><img alt="A fresh nbotebook" src="/setting-up-jupyter-lab-on-mac/jupyter_detail.png"/></p>
<p>To get going within Jupyter Lab, follow their <a href="https://jupyterlab.readthedocs.io/en/latest/user/interface.html" rel="noopener noreferrer" target="_blank">User Guide</a>.</p>