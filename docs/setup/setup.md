# Guide de setup

## Jetson Nano

1. Pour le setup de base (installation de l'OS et configuration), suivre la documentation officiel Nvidia : https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit
2. Pour pouvoir développer localement, l'utilisation d'une connexion ssh et la méthode la plus simple. Pour cela, connecter votre pc à la Jetson Nano via un câble ethernet et paramétrer les interfaces de chaque appareil de façon statique pour simplifier la communication.
```bash
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i enp4s0 -o wlan0 -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o enp4s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```
3. Ajouter les dns suivant pour avoir une résolution de nom qui fonctionne sur la Jetson Nano dans le fichier /etc/resolve.conf:
```
namespace 10.42.0.1
namespace 8.8.8.8
namespace 8.8.8.4
```
4. Pour tester le code sur la carte, utiliser git pour mettre à jour le repo
