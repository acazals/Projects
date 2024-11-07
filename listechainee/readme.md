# TP C++ : Agenda Ordonné de Rendez-vous

## Description

Gestion d'un agenda en C++ avec des rendez-vous triés par date et heure. Utilisation d’une **liste chaînée ordonnée** pour organiser les rendez-vous, chaque élément de la liste (un **NoeudRDV**) contient un rendez-vous et un pointeur vers le suivant. Cela permet d'ajouter, de supprimer, et de consulter les rendez-vous de manière efficace tout en maintenant un ordre chronologique.

### Fonctionnalités :
- Ajouter un rendez-vous.
- Supprimer un rendez-vous.
- Afficher les rendez-vous.
- Vider l’agenda.

### Classes :
- **Agenda** : Gère la liste chaînée ordonnée de rendez-vous.
  - `ajoute(RDV r)` : Ajoute un rendez-vous à la liste en maintenant l'ordre.
  - `enleve(RDV r)` : Supprime un rendez-vous en ajustant les pointeurs des éléments voisins.
  - `afficher()` : Affiche tous les rendez-vous dans l’ordre chronologique.
  - `vider()` : Vide l’agenda en réinitialisant la liste.

- **NoeudRDV** : Contient un rendez-vous et un pointeur vers le suivant dans la liste.
  
- **RDV** : Représente un rendez-vous avec une date et une heure.
  - `estEgal(const Date&)` : Compare deux dates.
  - `estSuperieur(const Date&)` : Vérifie si une date est postérieure.
  - `estEgal(const Heure&)` : Compare deux heures.
  - `estSuperieur(const Heure&)` : Vérifie si une heure est postérieure.
  - `estEgal(const RDV&)` : Compare deux rendez-vous.
  - `estSuperieur(const RDV&)` : Vérifie si un rendez-vous est postérieur à un autre.

### Liste Chaînée et Pointeurs

L'agenda utilise une **liste chaînée** pour organiser les rendez-vous. Chaque élément de la liste (un **NoeudRDV**) contient un rendez-vous et un pointeur vers le suivant. Cela permet :
- D'ajouter facilement un rendez-vous au bon endroit tout en gardant l’ordre chronologique.
- De supprimer un rendez-vous en ajustant les pointeurs des éléments voisins.
- D'éviter un réajustement coûteux de toute la liste à chaque insertion ou suppression.


