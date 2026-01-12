# NanoCar

Projet pour l'option prototypage de mon école. Je veux créer un petit véhicule électrique (style voiture radiocommandé) avec une carte jetson nano et une caméra pi dans le but de faire de la reconnaissance d'objet pour suivre une cible. La jetson hostera aussi un serveur web contenant un retour caméra ainsi que des controles pour le véhicule.
Le prototype sera développé en Python pour un dévelopement rapide et fonctionnel. 

## To do list

**Management**
- [x] Définition du besoin
- [-] Création du cahier des charges
    - [x] Analyse fonctionnelle
    - [x] Planning prévisionnel
    - [ ] Diagramme fast
- [-] Commande du matériel
- [-] WBS (a mettre au propre)
- [x] Mise en place du Gantt
- [-] Budget (a mettre au propre)

**Réalisation physique**
- [x] Réflexion sur la partie direction du véhicule (une bille a l'avant et direction avec un differentiel de rotation dans les roues arrieres)
- [-] Conception 3D
    - [x] Jetson nano
    - [x] LiPo
    - [x] Moteur
    - [x] Driver
    - [x] Raspberry camera
    - [x] Regulateur
    - [x] Roue
    - [x] Chassis
    - [ ] Roue avant
    - [ ] Supports pour l'assemblage (batterie, caméra, moteurs)
    - [ ] Persage des trous de vis (fixation composants)
    - [ ] Assemblage de la conception 3D
- [-] Setup du wifi de la Jetson Nano
- [ ] Fabrication
- [ ] Assemblage

**Réalisation logiciel**
- [x] Ajout d'une connexion ssh pour un accès simple à la Jetson Nano
- [x] Mise en place d'un serveur sur la jetson nano
    - [x] Serveur flask
    - [x] Implémentation des commandes
- [x] Création de l'interface utilisateur
- [x] Mise en place du flux vidéo
- [x] Controle des moteurs
- [ ] Intégration d'un modèle open source de reconnaissance d'objet
    - [ ] check: https://github.com/nithin-aikkattumadathil/Live-Image-processing-on-Jetson-Nano-Developer-Kit

**Intégration** (Une fois l'assemblage fini)
- [ ] Paramétrage de l'accéleration / décéleration / marche arrière
- [ ] Différentiel des moteurs pour la direction
- [ ] Controle automatique (input de direction en fonction de la position de la cible)
- [ ] Mode recherche de cible si aucune cible dans le visuel

**Livrable**
- [ ] Rédaction d'une documentation utilisateur 
- [ ] Rédaction d'une documentation technique permettant de refaire le projet de zéro

## Questions

- Est ce que j'utilise mon budget ? 
Non, budget CESI.
- Est ce que je peux utiliser une Lipo pour alimenter la jetson avec un régulateur de courant et les moteurs ? 
Oui
- Est ce que je fais une archi monolithe ? Est ce que je sépars le serveur web, et le soft de controle du véhicule ? 
Monolithe (dire dans le rapport technique que séparer les services est préferable)
- Est ce que le schéma électronique semble correct ? 
Oui

