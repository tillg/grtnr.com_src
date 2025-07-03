---
source-language: en
target-language: de
last-created: 2025-07-03 17:23:23
hash-on-last-created: f74871d79814bc59a5b1c7171885bb67981c6fe570d92726c6e2abfd92f059f1
translation-type: automatic
---

[en→de] <p>I write or blog in different media:</p>
<ul>
<li>Twitter</li>
<li>Facebook</li>
<li>A private blog with restricted access (because it contains family pictures)</li>
<li>This <a href="http://tillgartner.com" rel="noopener noreferrer" target="_blank">blog</a></li>
</ul>
<p>From time to time I find it nice to scroll through my past. I do this most often on our family blog, because it contains the most interesting content and because it is easy to scroll through. I would like to be able to scroll through all my past across all media.</p>
<p>So this is what my software should do:</p>
<ul>
<li>Collect all entries I wrote in the social media:</li>
<li>Twitter</li>
<li>Facebook</li>
<li>Wordpress</li>
<li>Create one document per entry in a Github Repo</li>
<li>Handle properly duplicate content: Since some years my Twitter account is <em>linked</em> to my Facebook account in that Twitter entries are replicated to Facebook. That’s because I have people that I consider <em>audience</em> in both media.</li>
<li>Collect also the feedback to my posts</li>
<li>Nicely display them in a static way, including overview pages</li>
</ul>
<p>Some technical thoughts:</p>
<ul>
<li>I would write it in java because that’s what I know best</li>
<li>Would be a headless program i.e. no <span class="caps">UI</span></li>
<li>Input should be the date of the last recorded social media entry</li>
<li>It collects all the entries (including the comments to it) on the different social media channels since that date</li>
<li>It dedupes them (i.e. merges the ones that are the same or replicates of one another on different channels)</li>
<li>It creates one document / file per social media entry and writes them in an output directory</li>
<li>This directory is then replicated / added to a github account</li>
<li>Social media entry documents would be named like <code>2015-12-03-The_title_of_what_ I_wrote-TWITTER.json</code></li>
<li>There would be a <em>header file</em> with a fixed name, i.e. <code>sociologs.json</code>. This file would hold the first 20 logs and point to a file with the next logs.</li>
<li>The domain <code>sociolog.io</code> would be <a href="https://www.godaddy.com/domains/searchresults.aspx?&amp;checkAvail=1&amp;domainToCheck=sociolog.io" rel="noopener noreferrer" target="_blank">available</a> - as of today, Jan 4 2016.</li>
<li>The generated <code>index.html</code> would load the data via <span class="caps">JS</span>/<span class="caps">AJAX</span> requests and continue loading while the user scrolls down</li>
</ul>
<p>If anyone is interested, or has comment, please get in touch at till<code>dot</code>gartner<code>at</code>gmail<code>dot</code>com.</p>