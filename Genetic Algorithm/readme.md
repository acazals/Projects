# Algorithme Génétique pour l'Optimisation du Chargement d'un Cargo

Ce projet implémente un algorithme génétique visant à optimiser le processus de chargement d'un cargo en respectant des contraintes spécifiques de poids et de volume. L'objectif est de maximiser la valeur des configurations de chargement tout en respectant les limites de capacité imposées par les conteneurs.

## Description du Problème

L'objectif de l'algorithme est de sélectionner un sous-ensemble optimal de conteneurs, qui maximise la somme des valeurs de ces derniers tout en respectant les contraintes de poids et de volume du cargo. Chaque conteneur est défini par trois paramètres :
- `poids` : poids du conteneur
- `volume` : volume du conteneur
- `prix` : valeur du conteneur

Les contraintes du cargo sont les suivantes :
- Une capacité maximale en poids (`Pmax`)
- Une capacité maximale en volume (`Vmax`)

## Paramètres de l'Algorithme

- **K** : Nombre de générations à traiter (10 000)
- **N** : Taille de la population de solutions (50)
- **M** : Taille du tournoi de sélection (5)
- **P** : Nombre de conteneurs disponibles à charger (30)
- **Pmut** : Probabilité de mutation (0.5)

## Fonctionnement de l'Algorithme Génétique

1. **Initialisation** :  
   Une population initiale de `N` individus est générée de manière aléatoire. Chaque individu est un vecteur binaire représentant si un conteneur est inclus ou non dans la solution. Les valeurs de fitness sont initialisées à zéro.

2. **Calcul de la Fitness** :  
   La fitness d'un individu est calculée en fonction de la valeur totale des conteneurs sélectionnés, tout en respectant les limites de poids et de volume. Si un individu dépasse ces contraintes, sa solution est rejetée et régénérée.

3. **Sélection** :  
   Une sélection par tournoi est appliquée pour choisir les individus à conserver pour la prochaine génération. Les 50 % des meilleurs individus sont conservés.

4. **Croisement** :  
   Les individus sélectionnés subissent un croisement, ce qui permet de générer de nouveaux individus en combinant les caractéristiques des parents. Cela permet de potentiellement améliorer la fitness globale.

5. **Mutation** :  
   Chaque individu a une probabilité `Pmut` de subir une mutation, où un gène (un conteneur) peut être modifié, introduisant ainsi de nouvelles possibilités.

6. **Suivi de la Fitness** :  
   La meilleure solution trouvée à chaque génération est enregistrée et un graphique de la fitness est généré pour suivre l'évolution au fil des générations.

## Exécution

L'algorithme fonctionne pendant `K` générations. À chaque génération, les étapes de calcul de la fitness, sélection, croisement et mutation sont répétées. L'algorithme continue jusqu'à ce que le nombre de générations soit atteint.

## Résultats

À la fin de l'exécution, l'algorithme affiche une courbe représentant l'évolution de la fitness au fil des générations, permettant ainsi de suivre l'amélioration des solutions.

## Fichiers du Projet

- `data_container.txt` : Ce fichier contient les informations relatives aux conteneurs : poids, volume et prix.
- `AG.m` : Le fichier principal qui contient le code de l'algorithme génétique.

## Prérequis

- MATLAB ou Octave ( exécuter le code)
- Le fichier `data_container.txt` doit être présent dans le même répertoire que le script



