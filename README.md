# NanoCar

Projet pour l'option prototypage de mon école. Je veux créer un petit véhicule électrique (style voiture radiocommandé) avec une carte jetson nano et une caméra pi dans le but de faire de la reconnaissance d'objet pour suivre une cible. La jetson hostera aussi un serveur web contenant un retour caméra ainsi que des controles pour le véhicule.

## A discuter avec Jocelyn

- Est ce que j'utilise mon budget ? Budget CESI.
- Est ce que je peux utiliser une Lipo pour alimenter la jetson avec un régulateur de courant et les moteurs. Oui
- Est ce que je fais une archi monolithe ? Est ce que je sépars le serveur web, et le soft de controle du véhicule. Monolithe (dire dans le rapport technique que séparer les services est préferable)
- Est ce que le schéma électronique semble correct ? Oui

## To do list

**Management**
- [x] Définition du besoin
- [x] Création du cahier des charges
    - [x] Analyse fonctionnelle
    - [x] Planning prévisionnel
- [-] Commande du matériel
- [-] WBS (voir to do list)
- [ ] Mise en place du Gantt
- [-] Budget

**Réalisation physique**
- [x] Réflexion sur la partie direction du véhicule (une bille a l'avant et direction avec un differentiel de rotation dans les roues arrieres)
- [-] Conception 3D
    - [x] Jetson nano
    - [x] LiPo
    - [x] Moteur
    - [x] Driver
    - [x] Raspberry camera
    - [x] Regulateur
    - [ ] Roue avant
    - [ ] Chassis
    - [ ] Supports pour l'assemblage
    - [ ] Assemblage de la conception 3D
- [ ] Fabrication
- [ ] Assemblage

**Réalisation logiciel**
- [ ] Mise en place d'un websocket sur la jetson nano
- [ ] Création de l'interface utilisateur
- [ ] Mise en place du flux vidéo
- [ ] Mise en place des contrôles manuels
- [ ] Intégration d'un modèle open source de reconnaissance d'objet

**Livrable**
- [ ] Rédaction d'une documentation utilisateur 
- [ ] Rédaction d'une documentation technique permettant de refaire le projet de zéro
