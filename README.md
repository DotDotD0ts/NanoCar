# NanoCar

Projet pour l'option prototypage de mon école. Je veux créer un petit véhicule électrique (style voiture radiocommandé) avec une carte jetson nano et une caméra pi dans le but de faire de la reconnaissance d'objet pour suivre une cible. La jetson hostera aussi un serveur web contenant un retour caméra ainsi que des controles pour le véhicule.
Le prototype sera développé en Python pour un dévelopement rapide et fonctionnel. 

## To do list

**Management**
- [x] Définition du besoin
- [x] Création du cahier des charges
    - [x] Analyse fonctionnelle
    - [x] Planning prévisionnel
    - [x] Diagramme fast
- [x] Commande du matériel
- [x] WBS (a mettre au propre)
- [x] Mise en place du Gantt
- [x] Budget (a mettre au propre)

**Réalisation physique**
- [x] Réflexion sur la partie direction du véhicule (une bille a l'avant et direction avec un differentiel de rotation dans les roues arrieres)
- [x] Conception 3D
    - [x] Jetson nano
    - [x] LiPo
    - [x] Moteur
    - [x] Driver
    - [x] Camera
    - [x] Regulateur
    - [x] Roue
    - [x] Chassis
    - [x] Roue avant
    - [x] Supports pour l'assemblage
        - [x] Batterie
        - [x] Moteurs
        - [x] Caméra
    - [x] Persage des trous de vis (fixation composants)
    - [x] Assemblage 3D
- [x] Fabrication
- [x] Assemblage
- [x] Branchements

**Réalisation logiciel**
- [x] Setup du wifi de la Jetson Nano (10.42.0.1:3000)
- [x] Ajout d'une connexion ssh pour un accès simple à la Jetson Nano
- [x] Mise en place d'un serveur sur la jetson nano
    - [x] Serveur flask
    - [x] Implémentation des commandes
- [x] Création de l'interface utilisateur
- [x] Mise en place du flux vidéo
- [x] Controle des moteurs
- [x] Control manuel du véhicule
    - [x] Différentiel des moteurs pour la direction
    - [x] Paramétrage de l'accéleration / décéleration
- [x] Intégration d'un modèle open source de reconnaissance d'objet
    - [x] Haar Cascade : reconnaissance de visage (CPU only) très lent, latence de plusieurs secondes + 2-3 FPS max
    - [x] SSD Mobilenet v2 : https://github.com/dusty-nv/jetson-inference, detecte le corps humain (GPU accelerated) latence 1-2 secondes, 60 FPS
- [x] Control autonome du véhicule
- [x] Mode recherche de cible si aucune cible dans le visuel (Ajout d'un boulean pour activer ou non)
- [x] Démarage automatique du serveur (crontab)
- [x] Esquive d'obstacles

**Problèmes**
- [x] Méthode Haar Cascade pour reconaissance de visage trop lente (2-3 fps)
- [x] Support caméra n'a pas d'angle, les visages ne sont reconnu que s'ils sont au niveau du sol

**User experience**
- [x] Syncroniser le slider de speed avec le backend
- [x] Réduire la taille de la cible pour que le robot reste plus loin

**Livrable**
- [x] Création d'un poster de présentation du projet
- [x] Rédaction d'une documentation utilisateur 
- [ ] Rédaction d'une documentation technique permettant de refaire le projet de zéro

## info livrable

- 41,47g de plastique pour les impressions des supports. cout : 1,04eur
- 57585,835mm2 soit 575,85cm2 soit 0,057585m2 surface de planche
