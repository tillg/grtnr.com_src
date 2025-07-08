---
date: 2025-01-15
excerpt: J'utilise différents outils de développement (Java, Python, Docker...) mais je n'en utilise certains que rarement. Donc j'oublie comment je les ai installés, quel gestionnaire de versions j'ai utilisé, etc. Ceci est donc une note pour le moi du futur pour m'en souvenir.
image: dev_tools.png
tags: Mac
updates: 2025-05-05
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-08T08:08:40.497123
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-01-15-development-environment-on-mac/2025-01-15-development-environment-on-mac.md
Generated-By: automatic-translation-plugin
---

![Image amusante de l'IA](dev_tools.png)

Je ne suis pas un développeur professionnel, je le fais pour le plaisir. Et j'aime explorer, découvrir de nouvelles technologies, développer toutes sortes de petites choses. Parfois, j'ai besoin de Python, parfois de React/Typescript, Java et plus encore. Pour chaque outil de développement ou langage, il existe plusieurs options pour les installer et gérer leurs versions. Comme j'ai tendance à oublier des choses comme "Comment ai-je installé Python sur cette machine ?", ceci est une note pour le moi du futur, m'indiquant comment j'ai installé chaque outil de développement.

Comme la méthode d'installation de certains paquets peut changer au fil du temps, j'ajouterai des dates à mes choix d'installation.

[TOC]

## Xcode

Xcode est l'outil de développement de base sur Mac. Il contient git et d'autres outils et compilateurs de base.

Je l'installe depuis l'Apple App Store.

## Terminal

Mon terminal préféré est [iTerm2](https://iterm2.com), et je l'installe simplement depuis son site web. Voir [ici](/setting-up-my-terminal/) pour savoir comment je le configure.

## zsh shell

Sur un nouveau Mac, voici ce que je fais :

```shell
# Vérifier quel Shell j'ai
echo "$SHELL"

# Si ce n'est pas zsh, le définir comme par défaut
chsh -s "$(which zsh)"

```

## VSCode

... ou VSCode-insiders

## Docker

**Janvier 2025 :** J'ai abandonné [Docker Desktop](https://www.docker.com/products/docker-desktop/) pour [Rancher Desktop](https://rancherdesktop.io).

Note d'installation : J'ai téléchargé la version Apple Silicon, ouvert le DMG et l'ai copié dans mon répertoire Applications. Le seul détail que j'ai dû faire est de cocher la case "Accès Administratif" dans les paramètres.
![texte alternatif](rancher_prefs.png)

_Registry_: J'utilise différents registres lorsque je travaille sur différents projets.

_Question_: Comment configurer Docker pour qu'il télécharge des images depuis un registre spécifique ?

## Java

Voici les options que j'ai vues :

- [jenv](https://github.com/jenv/jenv)
- [SDK man](https://sdkman.io)

**Janvier 2025** : J'ai décidé d'utiliser SDK Man car il couvre également Maven.

**Mini-Cheatsheet**

- `sdk install java 17.0.12-jbr` installe cette version spécifique de Java
- `sdk list java` affiche toutes les versions de Java disponibles (disponibles à l'installation)
- Pour lister les versions de Java installées :
  - `sdk offline enable`, pour qu'il liste uniquement les versions installées localement
  - `sdk list java`
  - `sdk offline disable`
- `sdk default java 21.0.6-amzn` définit cette version comme par défaut
  Pour définir une version de Java par défaut dans un répertoire, voir la [commande Env](https://sdkman.io/usage/#env-command)

## Maven

J'utilise simplement `brew install maven`. Pour une version plus ancienne `brew install maven30` installe Maven 3.0.

## Gradle

**Janvier 2025** : J'ai décidé d'utiliser SDK Man pour Gradle également.

Raison : `brew install gradle` a installé la version 8.12.1 de Gradle, mais pour le projet actuel, j'avais besoin de la version 8.5.

- `sdk install gradle 8.5` : Installe cette version spécifique de Gradle
- `sdk use gradle 8.5`

## Node et npm

**Janvier 2025** J'ai décidé d'utiliser [nvm](https://github.com/nvm-sh/nvm).

**Mini-Cheatsheet**

- `nvm use 16`
- `node -v` affiche la version actuellement utilisée
- `nvm install 12` installe node 12 et l'utilise

## Python

- **Été 2024** : J'utilise [pyenv](https://github.com/pyenv/pyenv)
- Pour installer pyenv : `brew install pyenv`

**Mini-Cheatsheet**

Pour sélectionner une version de Python installée par Pyenv à utiliser, exécutez l'une des commandes suivantes :

```shell
pyenv install 3.12
pyenv shell <version> -- sélectionner uniquement pour la session shell actuelle
pyenv local <version> -- sélectionner automatiquement lorsque vous êtes dans le répertoire courant (ou ses sous-répertoires)
pyenv global <version> -- sélectionner globalement pour votre compte utilisateur
```

## Ruby

Pas encore réfléchi. Éviter Ruby en général... 😉