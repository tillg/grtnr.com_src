---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 808acda69ce684ba78bd588b96b519525ca314baca34f4809d03b60049bf8896
translation-type: automatic
---

[de→fr] <p><strong><span class="caps">TL</span>;<span class="caps">DR</span></strong> In order to record the screen of your Mac together with the sound (i.e. a Zoom session) you can use Soundflower.</p>
<p>Here is what I wanted to achieve: Make a (video) recording of what is happening on the screen of my Mac <strong>including the sound</strong>. All this, while still hearing what is happening at the same time. In my case I wanted to record a Zoom-Class, but I guess this is a setup that might be useful in many situations.</p>
<p>macOS comes with a great built-in screen recording tool:<a href="https://support.apple.com/en-us/HT208721" rel="noopener noreferrer" target="_blank">QuickTime Player</a> (yes, it records, even though the name says <em>player</em> 😀).</p>
<p>When using QuickTime Player the only problem is the sound: The choices you have are <em>Internal Microphone</em> or <em>None</em>. That fits well if you want to record a tutorial where the sound is what you explain through the microphone, but it doesn’t fit my situation.</p>
<p>This is where <a href="https://github.com/mattingalls/Soundflower" rel="noopener noreferrer" target="_blank">SoundFlower</a> comes in the picture. It’s Open Source, mature and reliable (tested by me and far more experienced fellows - and always got very good reviews). SoundFlower as it is today (that’s Summer 2020) is not a program with a User Interface, but only a MacOS system extension. That’s something you don’t see as a user but that is very helpful in the background.</p>
<p>What it does in our case: It creates a new, virtual sound channel that splits the sound stream into 2 other streams. In my case it means that in my Zoom session I select a virtual output instead of the speaker of my Mac. I called this output <em>MacSpkr_SndFlwr</em>. And this virtual stream splits the output to the Speaker of the Mac and the (logical) SoundFlower channel. Then I select the SoundFlower channel as input to my QuickTime Player Recording and that’s it.</p>
<p><img alt="Flow" src="/mac-recording-screen-sound/MacSoundFlower.svg"/>The Sound Streams</p>
<h2 id="setting-it-all-up">Setting it all up</h2>
<p><strong>Installing Soundflower</strong> is well described on it’s <a href="https://github.com/mattingalls/Soundflower/releases/tag/2.0b2" rel="noopener noreferrer" target="_blank">download page on Github</a>. The process might seem a bit clumsy but works well if you follow it step by step. Note that it took me a while to figure out what they meant by “<em>Once there, there should be an “Allow” button (**) that you will need to click on to give permission to use Soundflower (developer: <span class="caps">MATT</span> <span class="caps">INGALLS</span>).</em>” I was expecting a popup dialog with the Allow-button, but it’s simply a button within the window.</p>
<p>Also note that you need to reboot your Mac after installing Soundflower.</p>
<p>Once you have Soundflower installed you can create a logical Audio Device that will be slipping the sound stream. To do so, open <em>Audio <span class="caps">MIDI</span> Setup</em>. It is a macOS utility program located in /Applications/Utilities. You can also start it via Spotlight (hit Cmd + Space) and enter “<em>Audio Midi”</em></p>
<p><img alt="Midi app launch" src="/mac-recording-screen-sound/Screenshot-2020-06-11-at-11.47.25.png"/></p>
<p><em>Starting the Audio <span class="caps">MIDI</span> Setup via Spotlight</em></p>
<p>Once you are in the Audio <span class="caps">MIDI</span> Setup program, create a new (logical) Audio Device: hit the “<strong>+</strong>” button in the bottom left corner and select “<em>Create Multi Output Device</em>“. In the the panel that appears on the right, select “<em>MacBook Speaker</em>” <span class="caps">AND</span> “<em>Soundflower (2ch)</em>“.</p>
<p><img alt="Settings" src="/mac-recording-screen-sound/Screenshot-2020-06-11-at-11.14.46.png"/></p>
<p><em>The newly created Multi Output Device</em></p>
<p>Then launch your QuickTime Player (this one comes pre-installed on your Mac) and create a new Screen Recording: Menu <em>File ➡ New Screen Recording</em>. In the lower part of the screen a floating menu appears:</p>
<p><img alt="Entire screen" src="/mac-recording-screen-sound/macos-catalina-screenshot-menu-record.jpg"/></p>
<p><em>The floating menu when recording with QuickTime Player</em></p>
<p>Open the Options list and select “Soundflower (2ch)” as input for the recording. Click on “Record” and off you go: Now start your Zoom session, maximize the window and your entire Zoom session will be recorded in a .mov file.</p>
<p>I hope this instructions were helpful; feel free to ask questions if you have any.</p>
<h3 id="references">References</h3>
<ul>
<li><em>How to record the screen on your Mac</em> from <a href="https://support.apple.com/en-us/HT208721" rel="noopener noreferrer" target="_blank">Apple Support</a></li>
<li><a href="https://github.com/mattingalls/Soundflower/releases/tag/2.0b2" rel="noopener noreferrer" target="_blank">Soundflower explanations</a></li>
<li><em>Record your computer’s screen with audio on a Mac</em> from <a href="https://www.cnet.com/how-to/record-your-computers-screen-with-audio-on-a-mac/" rel="noopener noreferrer" target="_blank">c|net</a></li>
</ul>