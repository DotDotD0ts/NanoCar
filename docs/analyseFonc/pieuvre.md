- FP1: Permettre à l'utilisateur de visualiser et de suivre automatiquement une cible.
- FC1: Être autonome en énergie pour alimenter la Jetson et les moteurs.
- FC2: Se déplacer sur le sol sans glisser et franchir de petits obstacles.
- FC3: Transmettre les données et recevoir les commandes via Wi-Fi (Serveur Web).

```mermaid
graph 
    %% Le Système central
    System((<b>NanoCar</b>))

    %% Les Éléments extérieurs
    Utilisateur[Utilisateur / Opérateur]
    Cible[Personne Cible]
    Sol[Sol / Environnement]
    Energie[Énergie / Batterie]
    Reseau[Réseau / Interface Web]

    %% Relations pour les Fonctions Principales (FP)
    Utilisateur -- <b>FP1</b> --- System
    Cible -- <b>FP1</b> --- System

    %% Relations pour les Fonctions Contraintes (FC)
    Energie -- <b>FC1</b> --- System
    Sol -- <b>FC2</b> --- System
    Reseau -- <b>FC3</b> --- System

    %% Styles pour la lisibilité
    style System fill:#FFF9C4,stroke:#FBC02D,stroke-width:4px,color:#000
    style Utilisateur fill:#E1F5FE,stroke:#0288D1,color:#000
    style Cible fill:#E1F5FE,stroke:#0288D1,color:#000
    style Sol fill:#EEEEEE,stroke:#9E9E9E,color:#000
    style Energie fill:#FFEBEE,stroke:#D32F2F,color:#000
    style Reseau fill:#E8F5E9,stroke:#388E3C,color:#000
```
