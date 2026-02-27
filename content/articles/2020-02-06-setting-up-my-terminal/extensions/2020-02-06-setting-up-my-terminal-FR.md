---
image: terminal.png
excerpt: Un guide pour configurer un terminal macOS avec zsh, Oh My Zsh, et powerlevel10k, en se concentrant sur l'intégration des éléments plutôt que sur une simple installation pas à pas.
title: Configuration de mon terminal
tags: tech, Mac
translation: fr
source_language: en
source_hash: 73903e9580cb1ea1f652ef2f6d4d2a0c623b05e7b5296a61c6114e14f28fc354
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:05:48.376918+00:00
generated_by: simplified-translation-system
---

Je sais, il existe de nombreux articles et explications sur la façon de configurer et de paramétrer votre terminal. Pourtant, il m'a fallu plus de 2 heures pour que tout fonctionne comme je le souhaitais. La raison en était que beaucoup d'articles et d'explications fournissent un guide étape par étape pour installer les éléments, mais peu d'informations de fond sur la manière dont les éléments sont liés et fonctionnent ensemble en arrière-plan. Et c'est ce qui me manquait...

Alors, voici un autre article. Ou plutôt une collection de fragments d'informations que j'ai trouvées précieuses.

## Mise en contexte

Mon installation cible et mes exigences sont simples :

- macOS (Catalina 10.15.2 au moment de l'écriture)
- iTerm2 (Version 3.3.8)
- zsh (fourni par Apple depuis quelques versions de macOS)
- Je veux une coloration correcte
- Je veux voir sur quelle branche Git je me trouve - si le répertoire courant est dans un dépôt git

## Les éléments en mouvement

Ce qui m'a fait perdre le fil, c'était l'absence de vue d'ensemble. Par conséquent, voici les différents éléments impliqués dans mon installation :

- **zsh** : Le shell
- **Oh My Zsh** : Un framework qui améliore le shell zsh avec des fonctions et un design.
- **powerlevel9k** : Un thème pour Oh My Zsh
- **Polices** requises par powerlevel9k pour afficher son texte et ses icônes

Les dépendances dans cette liste vont de haut en bas, c'est-à-dire que les polices sont requises par powerlevel9k qui fonctionne au-dessus de Oh My Zsh qui utilise zsh.

## Structure du répertoire

Avant de passer en revue les différents composants un par un, voici la structure du répertoire que nous aurons après avoir installé tous les éléments :

```text
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

J'utilisais bash dans le passé et j'en étais satisfait. Je lançais simplement mon Terminal Mac, et il était là. Plus tard, j'ai utilisé iTerm2, et il se lançait également avec bash. Alors pourquoi passer à zsh ?

Cet article l'explique bien et en détail. En résumé :

- Apple utilisait bash dans le passé car c'était le standard de facto
- En 2007, bash est passé à la [Licence Publique Générale GNU 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), ce qu'Apple n'a pas apprécié pour certaines raisons. Ils sont donc restés avec la version de bash d'avant 2007. Et c'est ancien - y compris [une vulnérabilité](<https://www.wikiwand.com/en/Shellshock_(software_bug)>) qui a forcé Apple à mettre à jour bash pour les Macs.
- zsh est progressivement devenu le nouveau standard de facto, donc Apple a suivi le mouvement.

Et bien sûr, [zsh offre des fonctionnalités modernes et intéressantes](https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/).

Donc, c'est le nouveau standard, il est esthétique - utilisons-le. Étant donné que c'est le nouveau shell standard de macOS, vous n'avez pas besoin de l'installer. Si vous avez un nouveau Mac livré avec Catalina pré-installé, vous utilisez déjà zsh. Si vous avez mis à jour votre Mac depuis Mojave, vous devez définir zsh comme shell de votre terminal ainsi :

```shell
chsh -s /bin/zsh
```

Cela définit zsh comme le Shell par défaut.

### Configuration

La configuration du shell zsh se fait via des entrées dans `.zshrc`, qui se trouve dans votre répertoire `$HOME`. Comme décrit ci-dessus, il y a plusieurs composants qui interagissent. Certains d'entre eux offrent des options de configuration et peuvent être configurés à différents endroits. Pour garder une vue d'ensemble, j'ai opté pour l'installation des composants dans leur emplacement par défaut respectif, et j'ai essayé d'avoir toutes les options de configuration dans le fichier `.zshrc`.

## Oh My Zsh

> Oh My Zsh est un framework open source, piloté par la communauté, pour gérer votre configuration zsh.
> -- <cite>[Site web Oh My Zsh](https://ohmyz.sh/)</cite>

Fondamentalement, Oh My Zsh rend votre terminal très esthétique (via [les thèmes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)) et propose de nombreux plugins utiles. Voici une liste d'exemples de leur [page GitHub](https://github.com/ohmyzsh/ohmyzsh) :

```bash
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

J'utilise actuellement le plugin git, qui offre des raccourcis pour les commandes git fréquemment utilisées.

### Configuration de Oh My Zsh

Comme mentionné, j'ai intégré toutes les configurations dans mon fichier `$HOME/.zshrc`. Les extraits pertinents de mon fichier `.zshrc` :

```shell
# Chemin vers votre installation oh-my-zsh.
export ZSH="/Users/tgartner/.oh-my-zsh"

# Définir le nom du thème à charger.
# Voir https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="powerlevel9k/powerlevel9k"

(...)

# Quels plugins souhaitez-vous charger ?
# Les plugins standards se trouvent dans ~/.oh-my-zsh/plugins/*
# Des plugins personnalisés peuvent être ajoutés à ~/.oh-my-zsh/custom/plugins/
# Format d'exemple : plugins=(rails git textmate ruby lighthouse)
# Ajoutez judicieusement, car trop de plugins ralentissent le démarrage du shell.
plugins=(git python)
```

## powerlevel10k

Note : J'utilisais [powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k), mais lors de l'installation de mon Mac en mai 2025, 9k était obsolète et pointait vers [powerlevel10k](https://github.com/romkatv/powerlevel10k).

Installez powerlevel10k en suivant leur [guide d'installation pour zsh](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh).