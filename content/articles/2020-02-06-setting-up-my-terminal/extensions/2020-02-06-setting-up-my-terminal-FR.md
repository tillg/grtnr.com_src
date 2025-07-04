---
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:42:21.276896
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2020-02-06-setting-up-my-terminal/2020-02-06-setting-up-my-terminal.md
Generated-By: automatic-translation-plugin
---

```markdown
---
title: Configuration de mon terminal
tags: tech, Mac
image: terminal.png
---

Je sais, il existe de nombreux articles et explications sur la façon de configurer et de paramétrer votre terminal. Pourtant, il m'a fallu plus de 2 heures pour que tout fonctionne comme je le souhaitais. La raison en était que beaucoup d'articles et d'explications fournissent un guide étape par étape pour installer les éléments, mais peu d'informations de fond sur la façon dont les choses sont liées et fonctionnent ensemble en arrière-plan. Et c'est ce qui me manquait...

Alors voici un autre article. Ou plutôt une collection de fragments d'informations que j'ai trouvées précieuses.

## Mise en contexte

Mon installation cible et mes exigences sont simples :

- macOS (Catalina 10.15.2 au moment de l'écriture)
- iTerm2 (Build 3.3.8)
- zsh (tel que fourni par Apple depuis quelques versions de macOS)
- Je veux une coloration correcte
- Je veux voir sur quelle branche Git je me trouve - si le répertoire actuel est dans un dépôt git

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

J'ai utilisé bash dans le passé et j'en étais satisfait. Je lançais simplement mon Terminal Mac, et il était là. Plus tard, j'ai utilisé iTerm2, et il s'ouvrait également avec bash. Alors pourquoi passer à zsh ?

Cet article l'explique bien et en détail. En résumé :

- Apple utilisait bash dans le passé car c'était le standard de facto
- En 2007, bash est passé à la [Licence Publique Générale GNU 3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html), ce qu'Apple n'a pas apprécié pour certaines raisons. Ils sont donc restés avec la version pré-2007 de bash. Et c'est ancien - y compris [une vulnérabilité](<https://www.wikiwand.com/en/Shellshock_(software_bug)>) qui a forcé Apple à mettre à jour bash pour les Macs.
- zsh est devenu au fil du temps le nouveau standard de facto, donc Apple a fait le changement.

Et bien sûr, [zsh offre des fonctionnalités plus modernes et intéressantes](https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/).

Quoi qu'il en soit, c'est le nouveau standard, il est agréable - utilisons-le. Comme c'est le nouveau shell standard de mac, vous n'avez pas besoin de l'installer. Si vous avez un nouveau mac livré avec Catalina pré-installé, vous utilisez déjà zsh. Si vous avez mis à jour votre Mac depuis Mojave, vous devez définir zsh comme votre shell de terminal comme suit :

```shell
chsh -s /bin/zsh
```

Cela définit zsh comme le shell par défaut.

### Configuration

La configuration du shell zsh se fait via des entrées dans `.zshrc`, qui se trouve dans votre répertoire `$HOME`. Comme décrit ci-dessus, il y a plusieurs composants qui interagissent. Certains d'entre eux offrent des options de configuration et peuvent être configurés à différents endroits. Afin de garder une vue d'ensemble, j'ai opté pour l'installation des composants dans leur emplacement par défaut respectif, et pour essayer d'avoir toutes les options de configuration dans le fichier `.zshrc`.

## Oh My Zsh

> Oh My Zsh est un framework open source, dirigé par la communauté, pour gérer votre configuration zsh.
> -- <cite>[Site web Oh My Zsh](https://ohmyz.sh/)</cite>

Fondamentalement, Oh My Zsh rend votre terminal très agréable (via [thèmes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)) et offre de nombreux plugins utiles. Une liste d'exemples de leur [page github](https://github.com/ohmyzsh/ohmyzsh) :

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
# Les plugins standard peuvent être trouvés dans ~/.oh-my-zsh/plugins/*
# Des plugins personnalisés peuvent être ajoutés à ~/.oh-my-zsh/custom/plugins/
# Format d'exemple : plugins=(rails git textmate ruby lighthouse)
# Ajoutez judicieusement, car trop de plugins ralentissent le démarrage du shell.
plugins=(git python)
```

## powerlevel10k

Remarque : J'utilisais [powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k), mais lors de l'installation de mon Mac en mai 2025, 9k était obsolète et pointait vers [powerlevel10k](https://github.com/romkatv/powerlevel10k).

Installez powerlevel10k en suivant leur [guide d'installation pour zsh](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh).
```