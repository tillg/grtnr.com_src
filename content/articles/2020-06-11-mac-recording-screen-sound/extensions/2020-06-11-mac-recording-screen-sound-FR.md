---
date: 2020-06-11
image: MacSoundFlower.png
excerpt: Comment enregistrer l'écran de votre Mac avec le son système en utilisant Soundflower et QuickTime Player.
title: Mac : Enregistrer l'écran et le son
translation: fr
source_language: en
source_hash: bcc4d96f6e1758f39feebd99e7a7c3ae49209e922b6925af0eff06fe14ea80c0
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:26:48.056799+00:00
generated_by: simplified-translation-system
---

**Résumé** Pour enregistrer l'écran de votre Mac avec le son (par exemple, une session Zoom), vous pouvez utiliser Soundflower.

Voici ce que je voulais accomplir : Faire un enregistrement (vidéo) de ce qui se passe sur l'écran de mon Mac **y compris le son**. Tout cela, tout en entendant ce qui se passe en même temps. Dans mon cas, je voulais enregistrer un cours Zoom, mais je suppose que cette configuration pourrait être utile dans de nombreuses situations.

macOS est livré avec un excellent outil d'enregistrement d'écran intégré : [QuickTime Player](https://support.apple.com/en-us/HT208721) (oui, il enregistre, même si le nom indique _player_ 😀).

Lorsque vous utilisez QuickTime Player, le seul problème est le son : Les choix que vous avez sont _Microphone interne_ ou _Aucun_. Cela convient bien si vous souhaitez enregistrer un tutoriel où le son est ce que vous expliquez via le microphone, mais cela ne correspond pas à ma situation.

C'est là que [SoundFlower](https://github.com/mattingalls/Soundflower) entre en jeu. C'est un logiciel Open Source, mature et fiable (testé par moi et par des collègues bien plus expérimentés - et toujours très bien noté). SoundFlower tel qu'il est aujourd'hui (c'est l'été 2020) n'est pas un programme avec une interface utilisateur, mais seulement une extension système MacOS. C'est quelque chose que vous ne voyez pas en tant qu'utilisateur mais qui est très utile en arrière-plan.

Ce qu'il fait dans notre cas : Il crée un nouveau canal sonore virtuel qui divise le flux sonore en 2 autres flux. Dans mon cas, cela signifie que dans ma session Zoom, je sélectionne une sortie virtuelle au lieu du haut-parleur de mon Mac. J'ai appelé cette sortie _MacSpkr_SndFlwr_. Et ce flux virtuel divise la sortie vers le haut-parleur du Mac et le canal (logique) SoundFlower. Ensuite, je sélectionne le canal SoundFlower comme entrée pour mon enregistrement QuickTime Player et c'est tout.

![Flux](MacSoundFlower.svg)Les flux sonores

## Configuration

**Installer Soundflower** est bien décrit sur sa [page de téléchargement sur Github](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2). Le processus peut sembler un peu maladroit mais fonctionne bien si vous le suivez étape par étape. Notez qu'il m'a fallu un certain temps pour comprendre ce qu'ils voulaient dire par "_Une fois là, il devrait y avoir un bouton "Autoriser" (\*\*) sur lequel vous devrez cliquer pour donner l'autorisation d'utiliser Soundflower (développeur : MATT INGALLS)._". Je m'attendais à une boîte de dialogue contextuelle avec le bouton Autoriser, mais c'est simplement un bouton dans la fenêtre.

Notez également que vous devez redémarrer votre Mac après avoir installé Soundflower.

Une fois Soundflower installé, vous pouvez créer un périphérique audio logique qui divisera le flux sonore. Pour ce faire, ouvrez _Configuration Audio MIDI_. C'est un programme utilitaire macOS situé dans /Applications/Utilities. Vous pouvez également le lancer via Spotlight (appuyez sur Cmd + Espace) et entrez "_Audio Midi_"

![Lancement de l'application Midi](Screenshot-2020-06-11-at-11.47.25.png)

_Lancement de la Configuration Audio MIDI via Spotlight_

Une fois dans le programme Configuration Audio MIDI, créez un nouveau périphérique audio (logique) : appuyez sur le bouton "**+**" dans le coin inférieur gauche et sélectionnez "_Créer un périphérique de sortie multiple_". Dans le panneau qui apparaît à droite, sélectionnez "_Haut-parleur MacBook_" ET "_Soundflower (2ch)_".

![Paramètres](Screenshot-2020-06-11-at-11.14.46.png)

_Le nouveau périphérique de sortie multiple créé_

Ensuite, lancez votre QuickTime Player (celui-ci est préinstallé sur votre Mac) et créez un nouvel enregistrement d'écran : Menu _Fichier ➡ Nouvel enregistrement d'écran_. Dans la partie inférieure de l'écran, un menu flottant apparaît :

![Écran entier](macos-catalina-screenshot-menu-record.jpg)

_Le menu flottant lors de l'enregistrement avec QuickTime Player_

Ouvrez la liste des options et sélectionnez "Soundflower (2ch)" comme entrée pour l'enregistrement. Cliquez sur "Enregistrer" et c'est parti : Lancez maintenant votre session Zoom, maximisez la fenêtre et toute votre session Zoom sera enregistrée dans un fichier .mov.

J'espère que ces instructions vous ont été utiles ; n'hésitez pas à poser des questions si vous en avez.

### Références

- _Comment enregistrer l'écran de votre Mac_ depuis [Apple Support](https://support.apple.com/en-us/HT208721)
- [Explications sur Soundflower](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2)
- _Enregistrez l'écran de votre ordinateur avec du son sur un Mac_ depuis [c|net](https://www.cnet.com/how-to/record-your-computers-screen-with-audio-on-a-mac/)