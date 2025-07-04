---
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T17:02:45.958845
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2024-04-08-setting-up-jupyter-lab-on-mac/2024-04-08-setting-up-jupyter-lab-on-mac.md
Generated-By: automatic-translation-plugin
---

```markdown
---
layout: post
date: 2024-04-08
excerpt: Configurer Python sur un Mac peut être délicat. Le nombre d'options est important, et elles peuvent interagir de manière étrange. De plus, vous devez vous souvenir de la méthode d'installation que vous avez utilisée lorsque vous souhaitez changer de version ou mettre à jour. Ce post devrait me rappeler comment je l'ai fait 😉
image: python_on_mac.png
tags: tech, Mac
---

Configurer Python sur un Mac peut être délicat. Le nombre d'options est important, et elles peuvent interagir de manière étrange. De plus, vous devez vous souvenir de la méthode d'installation que vous avez utilisée lorsque vous souhaitez changer de version ou mettre à jour. Ce post devrait me rappeler comment je l'ai fait 😉

## Installer Python

Il existe de nombreuses façons d'installer Python sur Mac et de gérer ses versions :

- Le Python installé sur MacOS
- `brew`
- Anaconda
- `pyenv`
- ...

Ce qui a le mieux fonctionné pour moi est **pyenv** :

- Installez-le : `brew install pyenv`. Je suppose que vous avez [Homebrew](https://brew.sh) installé...
- Consultez les options et commandes proposées : `pyenv`
- Listez toutes les versions de Python disponibles pour pyenv : `pyenv versions`
- Installez une version : `pyenv install 3.12` (C'est la version de Python que j'utilise actuellement)
- Définissez la version utilisée globalement : `pyenv global 3.12`
- Vérifiez quelle version est définie globalement : `pyenv global` ou `python --version`

## Créer un répertoire de travail

Créez le répertoire dans lequel vous souhaitez travailler dans le cadre de votre projet. Je garde tous mes projets de codage sous `~/git`. De cette façon, je sais que tous les projets sous `~/git` n'ont pas besoin d'être sauvegardés car ils sont dans un dépôt git.

Exemple :

```bash
cd ~/git
mkdir my_python_project
cd my_python_project
```

## Créer un environnement local

Afin de fournir à mon projet son propre environnement Python, j'utilise [les environnements virtuels de Python](https://docs.python.org/3/library/venv.html) :

```bash
cd ~/git/my_python_project
python3.12 -m venv .venv
```

De cette façon, j'ai créé un environnement à l'intérieur du sous-répertoire `.env`. Pour l'activer, utilisez `source .venv/bin/activate`.

**Remarque** : Comme mon sous-répertoire `.env` ne doit pas être dans le dépôt git, il doit être listé dans le fichier `.gitignore`.

## Installer Jupyter Lab

Maintenant que j'ai l'environnement Python, je peux installer Jupyter. Assurez-vous que je suis dans le bon répertoire et que l'environnement Python est activé :

```bash
# Allez dans mon répertoire de projet et activez son environnement Python
cd ~/git/my_python_project
source .venv/bin/activate

# Installez Jupyter Lab dans cet environnement
pip install jupyterlab

# Très souvent, il me demande de mettre à jour pip lui-même
pip install --upgrade pip

# Démarrez Jupyter Lab
jupyter lab
# Attendez un peu et votre navigateur devrait s'ouvrir sur http://localhost:8888/lab
```

## Créer un nouveau notebook

Votre navigateur devrait être ouvert dans un nouvel environnement Jupyter Lab :
![Un environnement Lab vide](jupyter_overview.png)

Cliquez sur _Notebook > Python 3_ et votre premier Notebook devrait être prêt à fonctionner :

![Un notebook vierge](jupyter_detail.png)

Pour commencer avec Jupyter Lab, suivez leur [Guide de l'utilisateur](https://jupyterlab.readthedocs.io/en/latest/user/interface.html).
```