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
- [x] Rédaction d'une documentation technique permettant de refaire le projet de zéro

## Documentations

Cette documentation a été réalisé sur l'outil fabmanager comme demandé par l'école. Pour voir le rendu correct de cette doc, veillez-vous rendre sur [ce lien](https://cesi-fabmanager.duckdns.org/#!/projects/nanocar)

# NanoCar

![Illustration](https://fabmanager-cesi.duckdns.org/uploads/project_image/26/project_image.jpg)

La robotique autonome est le domaine consistant à concevoir  
des systèmes capables d'interagir avec leur environnement. Il  
s’agit d’un point clé avec énormément d’enjeux pour l’industrie  
et la mobilité de demain. L’intelligence artificielle, prenant de  
plus en plus d’importance, permet désormais d'intégrer de la  
vision par ordinateur complexe sur de petits systèmes  
embarqués. C’est pour cela que je vous présente mon robot  
autonome Nanocar. Il a pour but de suivre une personne sans  
intervention extérieur.

Vous pouvez retrouver l’entièreté des fichiers concernant ce projet dans le repo&nbsp;[Github NanoCar](https://github.com/DotDotD0ts/NanoCar)



## Étapes

### Étape 1 : Documentation utilisateur

Dans un premier temps, voici la documentation utilisateur qui vous permettra d'utiliser ce prototype :

1. Branchez la batterie LiPo au connecteur jaune sur le côté du robot. Ce connecteur permet d'alimenter l'entièreté du robot.
2. Vérifiez que la LED du driver clignote en bleu sinon chargez la batterie, cette LED indique que la LiPo est suffisamment chargé pour ne pas perdre en durée de vie. (Le driver est la carte électronique brancher directement à la batterie par le connecteur jaune)
3. Utilisez un appareil pour vous connecter au réseau Wifi NanoCar.
4. Ouvrez un navigateur internet et connectez-vous à l'adresse [http://10.42.0.1:3000/](http://10.42.0.1:3000/.)&nbsp;. Cela vous permettra d'avoir l'accès à la page de contrôle du robot.

Utilisation du robot à partir de la page de contrôle :

- Utilisez les flèches directionnelles sur l'écran de contrôle ou sur votre clavier pour faire bouger le robot. (La touche espace permet de freiner)
- Changez la vitesse du robot à l'aide du slider en dessous des boutons.
- Le bouton MODE permet de changer entre les 2 modes du robot : le mode manuel (par défaut) où vous contrôlez le robot à l'aide de l'interface et le mode automatique où une IA va prendre le contrôle du robot est va essayer de suivre une personne. Dans le mode automatique, vous remarquerez que le retour caméra affiche des informations sur ce que l'IA reconnais.&nbsp;
- Le bouton SEARCH permet, en mode automatique, au robot de chercher sa cible au lieu d'attendre qu'elle passe dans son champ de vision.

Enfin pour éteindre le robot il suffit de débrancher le connecteur jaune de la batterie.



![Image 1](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/24/project_step_image.jpg)

### Étape 2 : La liste de course

Pour ce projet, j'ai réutilisé un maximum de composants d'autres projets du Fablab, vous n'êtes en aucun cas obligé de réutiliser les mêmes références. La seul nécessité est que le driver des moteurs accepte une communication série bien particulière. Il reste possible d'adapter le code pour la communication entre la Jetson Nano et le driver.

Voici les composants / matériaux utilisés :

- Une planche de bois de 6mm d'épaisseur.
- 42g de PLA.
- Une multitude de petit câble mâle vers mâle et femelle vers mâle.
- Une multitude de vis et d'écrou m2 et m3
- 2 roues avec une vis permettant de sécuriser la roue à l'axe du moteur.
- 1 ball caster pour la roue avant.
- 2 moteurs DC. Ici des&nbsp;[313 RPM HD Premium Planetary Gear Motor w/Encoder](https://www.servocity.com/313-rpm-hd-premium-planetary-gear-motor-w-encoder/). Ils sont beaucoup trop puissant par rapport aux attentes du prototype.
- Un driver pour contrôler les moteurs. Ici une Sabertooth 2x25. De même pas besoin d'un contrôleur aussi poussé. Si vous ne souhaitez pas toucher au code, il vous faudra un driver qui peut être contrôlé par une communication série de la même façon que la Sabertooth. (Vérifiez que la partie simplified serial de la documentation de votre driver corresponde à la&nbsp;[documentation Sabertooth](https://www.dimensionengineering.com/datasheets/Sabertooth2x25.pdf)). Sinon vous pouvez toujours adapter le fichier command.py pour que la communication corresponde à votre driver.
- Une Jetson Nano (le cerveau du robot qui permet de faire tourner un modèle de reconnaissance d'objet).
- Une carte micro SD de 32Go.
- Une caméra Pi camera v2.1. Dans le cas où vous voulez en utiliser une autre il faudra modifier l'initialisation de la caméra dans le fichier camera.py pour que la librairie OpenCV puisse récupérer l'image.
- Un&nbsp;[dongle Wifi](https://www.amazon.fr/Cudy-Adaptateur-WU300-Hotspot-compatible/dp/B0FR443YP5?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1X55UOTPPWB8L&dib=eyJ2IjoiMSJ9.B7dflptUIcEv6lOPyZBst1Jep_q5H8rd42xS56UKp7iB8e8VZjCAwITwhe7Wo6t4DmLAF-moSbWHSwQv6-TpoE-_jmoUwVtNkpPI-ykR0VV_fNrticMW3VLCUgpCE4oH557o73ekHm9reciHxCYD2VBBoFL0qTcd1FJcHFu0Snnabl4shaOLigFEBxYYITZ7_3alKqPmprimUef3027U-R4PZTH4pzPDd5EzuIGBoFCE5MqiUC5wIUjXp1FCUzbADcDGCKXq1jYtCC0qwnF6XKxGHBkEE-2U1MPySORK2qk.Gu4BUI-1lQBr5BeH2_cBHVz_RMgHF7InncUQtTpSuUk&dib_tag=se&keywords=dongle+wifi+AP+linux&qid=1768555222&sprefix=dongle+wifi+ap+linu%2Caps%2C253&sr=8-7) qui fait Access point et qui fonctionne sur Linux. Vérifiez bien les 2 mentions à l'achat.
- Une batterie LiPo 4S.
- Un connecteur XT60 femelle pour connecter le driver à la LiPo.
- Un régulateur de courant pour faire descendre le 14V de la batterie en 5V pour l'alimentation de la Jetson Nano.
- Un cable d'alimentation 5V 4A pour alimenter la Jetson Nano.
- Dans le cas où votre driver est contrôlé par du 5V comme sur la Sabertooth, il vous faudra un level shifter 3V vers 5V pour éviter de cramer la Jetson Nano. Il est nécessaire de protéger la Jetson Nano qui ne prend que du 3V sur les pins I/O.


### Étape 3 : Préparation de la Jetson Nano

Maintenant que nous avons tous les composants, commençons la réalisation.

Brancher le dongle Wifi sur la Jetson Nano ainsi que la carte micro SD et la caméra.

Dans un premier temps, il vous faudra installer l'OS sur la Jetson Nano. Pour cela, je vous laisse suivre le guide fourni par Nvidia : [https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit). Je vous conseille de définir le nom d'utilisateur en tant que 'nano' vu que c'est celui qui sera utiliser pour le reste de la documentation.

Pour la suite, il va être important d'être connecter à internet. Pour cela, utilisez l'utilitaire graphique d'Ubuntu en haut à droite de l'écran ou nmtui si vous utilisez une connexion serial ou ssh à la carte.

Une fois connecté à un réseau Wifi ayant un accès internet, à l'aide d'un terminal, exécuter les commandes suivantes :

Mettre en place le DNS :

    sudo echo "nameserver 8.8.8.8" > /etc/resolv.conf
    sudo systemctl restart NetworkManager

Installer les dépendances :

    sudo apt-get update
    sudo apt-get install python3-pip cmake git  
    pip3 install flask libpython3-dev python3-numpy

Pour préparer git pour récupérer le code source du projet ainsi que celui des dépendances. Vous pouvez mettre ce que vous souhaitez en nom utilisateur et email :&nbsp;

    git config --global user.name "[votre nom d'utilisateur]"
    git config --global user.email "[votre email]"

Installer Jetson Inference est nécessaire pour la partie reconnaissance d'objet du projet :

    sudo apt-get install git cmake libpython3-dev python3-numpy
    git clone --recursive --depth=1 https://github.com/dusty-nv/jetson-inference
    cd jetson-inference
    mkdir build
    cd build
    cmake ../
    make -j$(nproc)
    sudo make install
    sudo ldconfig

Voici le lien de la documentation d'où viennent les commandes : [https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md).

Ensuite, copier le répertoire Github de NanoCar avec la commande :

    git clone[https://github.com/DotDotD0ts/NanoCar.git](https://github.com/DotDotD0ts/NanoCar.git)

Enfin, pour que le code se lance à chaque démarrage, nous allons configurer l'utilitaire linux crontab :

    sudo crontab -e

Cette commande va vous ouvrir un fichier dans lequel il va falloir mettre la ligne suivante :&nbsp;

    @reboot python3 /home/nano/NanoCar/src/main.py

Sauvegardez le fichier avec Ctrl + o puis fermez le avec Ctrl + x.

Maintenant, plus besoin de connexion internet, nous pouvons préparer la carte à créer son propre réseau Wifi pour si connecter.

Pour cela, ouvrez un terminal puis entrez les commandes suivantes :

    # 1. Création de la connexion et du nom du réseau (SSID = NanoCar)sudo nmcli con addtypewifi ifname wlan0 con-name NanoCar autoconnect yes ssid NanoCar# 2. Force le mode Point d'Accèssudo nmcli con modify NanoCar 802-11-wireless.mode ap# 4. Configuration IP (Serveur DHCP)sudo nmcli con modify NanoCar ipv4.method shared# 5. Force la bande 2.4GHz (Plus stable)sudo nmcli con modify NanoCar 802-11-wireless.bandbg  
      
    # 6. Rendre l'adresse IP statique  
    sudo nmcli con modify NanoCarHotspot ipv4.addresses 10.42.0.1/24
      
    # 7. Activer l'interface  
    sudo nmcli con up NanoCar

Maintenant, il est possible de se connecter à la carte avec un ordinateur. Pour cela, connectez l'ordinateur au réseau Wifi NanoCar puis ouvrez un terminal et connectez-vous en SSH :

    ssh nano@10.42.0.1

Le mot de passe du compte utilisateur vous sera demandé.

Cette connexion SSH vous permettra de faire des modifications au code source en cas de besoin.



### Étape 4 : Fabrication

Prenez votre planche en bois, une découpeuse laser et utilisez le CAD du châssis (retrouvable sur le Github dans le dossier CAD) ou le pdf pour découper le châssis dans la planche en bois. Vous pouvez aussi graver les emplacements des différents composants pour rendre l'assemblage plus simple.

Imprimez les supports en PLA à partir des modèles 3D. (vous retrouverez aussi les CAD dans le Github).

Prenez un crayons fin et long puis placez les différents composants, supports imprimés et le ball caster sur la planche en bois. Vous pouvez ainsi marquer les trous à faire pour les vis. Pour placer les composants, référez-vous au CAD NanoCar assemblage ou à l'image de la réalisation finale.

Avec votre châssis marqué, utilisez la perceuse à colonne pour faire des trous de 2 et 3 mm de diamètre. L'image ci-dessus vous permettra de savoir quelles trous doivent être de quelle diamètre.

Il va falloir régler le régulateur de courant, pour cela équipez-vous d'un petit tournevis plat, d'une alimentation 14V (vous pouvez utilisez la batterie directement) et d'un multimètre. Branchez l'alimentation au borne IN + et - du régulateur, réglez votre multimètre en mode voltmètre 20V en courant continu, poser les bornes de votre multimètre sur la sortie OUT + et - puis tourner le potentiomètre bleu à l'aide du tournevis plat jusqu'à ce que vous lisiez 5V sur le multimètre. Cette étape est extrêmement importante pour ne pas griller la Jetson Nano.

Sur la Sabertooth 2x25, vous allez retrouver 6 switchs qui permettent de configurer le driver, je vous laisse lire la&nbsp;[documentation officielle](https://www.dimensionengineering.com/datasheets/Sabertooth2x25.pdf)&nbsp;pour comprendre ce que la configuration suivante fait :&nbsp;

1. ON : Sélection du mode
2. OFF : Sélection du mode
3. ON : Option de protection de la batterie Lithium
4. OFF : Sélection du baud rate
5. ON&nbsp;: Sélection du baud rate
6. ON : Sélection du mode simple serial

Maintenant pour la dernière étape avant l'assemblage final, il va vous falloir souder 6 files sur le level shifter. Du côté LV, il vous faudra des mâles vers femelles et du côté HV il vous faudra des mâles vers mâles.



![Image 1](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/64/project_step_image.jpg)

![Image 2](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/65/project_step_image.jpg)

### Étape 5 : Assemblage

Voici maintenant les étapes de l'assemblage. Vous retrouverez dans les images un schéma électroniques ainsi que toutes les étapes de l'assemblage dans l'ordre.

Vu qu'aucun pas de vis n'est mis en place, nous utiliserons une vis ainsi qu'un écrou pour serrer à chaque fois que j'indique "Vissez".

1. Vissez le régulateur de courant sur le châssis.
2. Connectez le câble d'alimentation 5V pour la Jetson Nano en sortie (le rouge sur le OUT+ et le noir sur le OUT-) et 2 files mâles vers mâles en entrée.
3. Vissez la Jetson Nano.
4. Connectez le driver au level shifter, 5V -\> HV, 0V -\> GND côté HV et le S1 -\> HV1. Vissez le driver.
5. Vissez les supports moteurs sans les serrer puis placer les moteurs. Enfin, serrer les supports pour que les moteurs ne puissent pas bouger. Vissez les supports de la batterie à l'avant.
6. Vissez le support caméra, ne le serré pas trop fort, la batterie viendra aligner la caméra.
7. Branchez le câble d'alimentation 5V à la Jetson Nano. Branchez le connecteur XT60 femelle ainsi que le régulateur de courant au driver, rouge -\> B+ et noir -\> B- ainsi que IN+ -\> B+ et IN- -\> B-. Branchez le level shifer à la JetsonNano, LV -\> 3.3V, GND -\> GND, LV1 -\> pin 8.
8. Branchez les moteurs au driver, Moteur B (à gauche sur l'image) : rouge -\> MB+, noir -\> MB-, Moteur A (à droite sur l'image) : rouge -\> MA+, noir -\> MA-. Vissez les roues sur les moteurs arrière et le ball caster à l'avant.
9. Glissez la batterie dans son emplacement avec le connecteur vers le driver. Enfin, connectez le connecteur jaune XT60 femelle au connecteur de la batterie. Une LED bleu devrait clignoter sur le driver, une LED rouge devrait s'allumer sur le régulateur de courant ainsi que sur la Jetson Nano.

Vous devriez maintenant vous retrouver avec un prototype fonctionnel.



![Image 1](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/66/project_step_image.png)

![Image 2](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/67/project_step_image.jpg)

![Image 3](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/68/project_step_image.jpg)

![Image 4](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/69/project_step_image.jpg)

![Image 5](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/70/project_step_image.jpg)

![Image 6](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/71/project_step_image.jpg)

![Image 7](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/72/project_step_image.jpg)

![Image 8](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/73/project_step_image.jpg)

![Image 9](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/74/project_step_image.jpg)

![Image 10](https://fabmanager-cesi.duckdns.org/uploads/project_step_image/75/project_step_image.jpg)

### Étape 6 : Programmation

Avec ce prototype enfin fonctionnel, il est temps de rentrer dans les détails de la logique. Si vous souhaitez modifier le code source, connectez-vous à l'aide de la connexion SSH comme expliqué à la fin de l'étape 3. Dans le cas où vous n'arrivez pas à vous connecter par le Wifi du robot, il reste possible de brancher directement un câble Ethernet entre le robot et votre PC puis de se connecter en SSH par l'ip de cette connexion.

Pour votre information, les technologies suivantes sont indispensable à ce projet :

- Jetson inference plus précisément SSD-Mobilnet-V2 qui est le modèle d'IA utilisé
- OpenCV une librairie très connu pour son efficacité dans le traitement d'image, ici utilisé pour récupérer le flux vidéo de la caméra
- Flask une libraire permettant de mettre en place très facilement un serveur web
- Enfin, pour la simplicité du langage et la rapidité d'écriture, tout le code est écris en python&nbsp;

Vous retrouverez tous les fichiers dans le dossier src du projet Github.

* * *

**Mise en place du serveur web (voir le fichier main.py)**

Vous pouvez retrouver le point d'entré de ce programme qui lance tout simplement le serveur web.&nbsp;

Dans ce fichier, nous retrouvons aussi la définition des routes du serveur web :

- La route par défaut /, amène sur l'écran de contrôle
- La route /videoFeed, envoie le flux caméra depuis le serveur
- La route /command, permet d'envoyer des commandes au serveur
- La route /currentSpeed, permet la synchronisation de la vitesse entre l'affichage et la vitesse réel du robot&nbsp;

Si vous souhaitez modifier l'écran de contrôle, vous retrouverez le fichier home.html dans le dossier page.

* * *

**Contrôle du véhicule (voir le fichier command.py)**

Dans ce fichier il y a la définition du pin de contrôle de la Jetson Nano avec la variable driverPin, ainsi que l'ouverture de la communication série entre la Jetson et le driver. Le serial port est définit dans la data sheet de la Jetson Nano et le baud rate doit correspondre à la configuration du driver.

La fonction driveMotor permet de transformer une simple vitesse avec un id de moteur en instruction compréhensible par le driver.

Enfin, la fonction execCommand recense toutes les commandes que le serveur peut recevoir et exécute le code permettant d'effectuer cette commande.

* * *

**Un accès simple à des valeurs (voir fichier globalVar.py)**

Pour transmettre facilement une valeur entre des fichiers python, la solution la plus simple reste d'avoir un fichier qui contient les variables à partager en tant que variable globale et d'importer ce fichier.

* * *

**IA et caméra (voir le fichier camera.py)**

Ce fichier rassemble la récupération du flux caméra ainsi que l'exécution de l'IA avec un post traitement pour afficher ce que l'IA a reconnue.

Dans un premier temps, nous ouvrons un chemin entre notre programme est la caméra à l'aide d'OpenCV que l'on va appeler un stream. Cette partie d'initialisation se fait à l'aide d'une chaîne de caractère très particulière qui indique à la Jetson Nano la qualité de l'image, le format de celle-ci ainsi que la fréquence d'image. Ici notre caméra peut se permettre de filmer dans une multitude de qualité dont de la 4k, mais pour notre utilisation, nous préférons la qualité la plus basse soit de la HD mais avec une fréquence d'image bien plus importante. Cela permet à l'IA de prendre beaucoup moins de temps à trouver sa cible et aussi à la suivre de façon plus précise.

Nous retrouvons ensuite l'initialisation du modèle d'IA SSD-Mobilnet-V2 avec un threshold définit ici à 60%. Ce threshold correspond à la confiance du modèle IA dans la reconnaissance d'un objet. Ce paramètre permet de contrôler les faux positifs. Si vous avez beaucoup de faux positif, augmentez le threshold sinon dans le cas contraire où le modèle ne reconnais pas de cible, baisser le.

Puis viennent quelques configuration :

- FRAME\_WIDTH correspond à la largeur du retour caméra définit plus haut.
- DEAD\_ZONE\_X correspond aux nombres de pixels autour du centre qui vont être considéré comme le centre. Cela évite que le robot oscille quand il essaie de pointer vers une cible.
- TARGET\_AREA correspond aux nombres de pixels chercher par le robot pour s’arrêter. Cela va contrôler la distance d'arrêt du robot par rapport à la cible. Si le robot se rapproche trop, réduisez ce nombre, sinon s'il s'éloigne trop, augmentez ce nombre.
- AREA\_TOLERANCE correspond aux nombres de pixels autour de la TARGET\_AREA qui vont être considéré comme la cible. Similairement à la variable DEAD\_ZONE\_X, cela permet d'éviter que le robot oscille d'avant en arrière lorsqu'il est à distance d'arrêt de la cible.&nbsp;&nbsp;

La fonction generateFrames est la fonction qui va permettre au serveur web d'envoyé le flux vidéo à l'écran de contrôle.

Enfin la fonction followTarget permet de passer l'image à l'IA qui nous donne une liste d'objets détectés ainsi que leur position. Nous cherchons dans cette liste la cible définit par globalVar.target\_class\_id (ici 1, si vous souhaitez que la cible soit autre chose qu'un humain, je vous laisse chercher le class id correspondant dans la&nbsp;[documentation du modèle](https://github.com/dusty-nv/jetson-inference/blob/master/data/networks/ssd_coco_labels.txt) est le remplacer). En priorité nous essayons d'esquiver l'obstacle le plus proche s'il est plus proche que la cible. Puis nous allons dans la direction de la cible. Pour finir, nous mettons à jour l'image du flux vidéo en y dessinant un rectangle vert pour la cible et des rectangles rouges pour les obstacles ainsi que leur catégorie



### Étape 7 : Conclusion

Dans l'ensemble, ce prototype est sorti comme imaginer au début du projet. Il correspond au CAD réalisé, toutes les fonctionnalités du cahier des charges sont présentes enfin la réalisation a pris moins de temps que prévu.

Le seul problème rencontré est la remonté d'un courant 5V par l'input S1 du driver dans le pin 8 (3,3V) de la Jetson Nano, ce qui a brulé un composant de celle-ci. Une solution simple a était trouvé rapidement avec l'ajout d'un level shifter.

Malgré un prototype fonctionnel de multiples améliorations sont possibles. Voici une liste non exhaustive d'idées pour améliorer ce prototype :

- Améliorer la logique d'esquive d'obstacles
- Ajouter une sélection de la cible
- Réduire la latence en mode automatique
- Revoir les contrôles du véhicules (par exemple une fonction lerp) pour rendre les contrôles moins brute, plus réalistes (accélération / décélération)
- Permettre à l'IA de faire plusieurs actions à la fois (tourner et avancer en même temps)
- Créer une petite dance de la victoire une fois que le robot à atteint sa cible

Avec cette documentation technique, vous pouvez maintenant modifié ce robot pour lui ajouter d'autres fonctionnalités que ce soit logiciel (enregistrement du flux vidéo) ou électronique (ajout d'un bras robotisé). Ce prototype a pour objectif final de servir de base pour réaliser des projets plus complexes avec plus de temps.



## Auteur

Nicolas Ridoire

## Thématiques

Robotique, Prototypage

## Fichiers CAD

![support_moteur.stl](https://fabmanager-cesi.duckdns.org/uploads/project_cao/21/support_moteur.stl)

![support_camera.stl](https://fabmanager-cesi.duckdns.org/uploads/project_cao/22/support_camera.stl)

![Support_batterie.stl](https://fabmanager-cesi.duckdns.org/uploads/project_cao/23/Support_batterie.stl)

![pdf_chassi.pdf](https://fabmanager-cesi.duckdns.org/uploads/project_cao/63/pdf_chassi.pdf)

## Statut

Terminé

## Machines utilisées

Découpeuse laser, Bambu Lab H2S

## Matériaux utilisés

Bois Contre plaqué, Filament PLA

## Licence

Attribution + Pas d'Utilisation Commerciale (BY NC)
