---
title: Setting up my terminal
tags: tech, Mac
image: terminal.png
---

I know, there are lots of articles and explanations out there on how to configure and set up your terminal. Yet, it took me more than 2 hours to get things working the way I wanted. Reason was, lots of the articles and explanations provide step by step guide on installing things, but to little background information on how things relate and work together in the background. And that's what was missing to me...

So here I go with yet another article. Or rather a collection of snippets of the information that I found valuable.

## Setting the scene

My target setup & requirements are simple:

- macOS (Catalina 10.15.2 at the time of writing)
- iTerm2 (Build 3.3.8)
- zsh (as provided by Apple since a couple of macOS versions)
- I want proper coloring
- I want to see what Git branch I am in - if the current directory is within a git repo

## The moving parts

What made me get lost, was missing overview. Therefore, here are the different bits and pices that are involved in my setup:

- **zsh**: The shell
- **Oh My Zsh**: A framework that enhances the zsh shell with functions and design.
- **powerlevel9k**: A theme for Oh My Zsh
- **Fonts** required by powerlevel9k to display it's text and icons

The dependencies in this list are from top to bottom, i.e. the fonts are required by powerlevel9k that runs on top of Oh My Zsh that uses zsh.

## Directory structure

Before going thru the different components one by one, this is the directory structure we will have after installing all the bits & pices:

```
├── $HOME
│   └── .oh-my-zsh/
│   │   └── custom/
│   │   │   └── themes/
│   │   │       └── powerlevel9k/
│   │   └── themes/
│   └── .zsh/
├── .zshrc
```

## zsh

I used bash in the past and I was happy with it. I simply started my Mac Terminal, and there it was. And later I used iTerm2, and it also fired up with bash. So why move over to zsh?

This article explains it nicely and extensively. In short:

- Apple used bash in the past as it was the de-facto standard
- In 2007 bash switched to [GNU Public License 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), which Apple didn't like for some reasons. So they stayed with the pre-2007 release of bash. And that's old - including [a vulnerabilty](<https://www.wikiwand.com/en/Shellshock_(software_bug)>) that forced Apple to update bash for Macs.
- zsh over time became the emerging de-facto standard, so Apple moved.

And of course, [zsh offers more modern, cool features](https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/).

So anyways, it's trhe new standard, it looks good - let's use it. As it's the new mac standard shell, you don't need to install it. In case you got a new mac that came with Catalina pre-installed, you are using zsh already. In case you upgraded your Mac from Mojave, you need to set zsh as your terminal shell like so:

```shell
chsh -s /bin/zsh
```

This sets zsh as the default Shell.

### Configuration

Configuring the zsh shell is done via entries in `.zshrc`, which is located in your `$HOME` directory. As described above, there are a couple of components that interact. Some of them offer configuration options, and can be configured in different locations. In order to keep an overview, I opted for installing the components in their respective default location, and trying to have all the configuration option in the `.zshrc` file.

## Oh My Zsh

> Oh My Zsh is an open source, community-driven framework for managing your zsh configuration.
> -- <cite>[Oh My Zsh website](https://ohmyz.sh/)</cite>

Bascically Oh My Zsh makes your terminal look very nice (via [themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)) and offers lots of helpful plugins. An example list from their [github page](https://github.com/ohmyzsh/ohmyzsh):

```
plugins=(
  git
  bundler
  dotenv
  osx
  rake
  rbenv
  ruby
)
```

I currently use the git plugin, which offers shortcuts for often used git commands.

### Configuring Oh My Zsh

As mentioned, I have all the configurations integrated in my `$HOME/.zshrc` file. The relevant snippets from my `.zshrc`file:

```shell
# Path to your oh-my-zsh installation.
export ZSH="/Users/tgartner/.oh-my-zsh"

# Set name of the theme to load.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="powerlevel9k/powerlevel9k"

(...)

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git python)
```

## powerlevel10k 

Note: I used to use [powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k), but when installing my Mac in May 2025, 9k was outdated and pointed to [powerlevel10k](https://github.com/romkatv/powerlevel10k).

Install powerlevel10k following their [installation guide for zsh](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh).