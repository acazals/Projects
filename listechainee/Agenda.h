#ifndef AGENDA_H
#define AGENDA_H

#include <iostream>
#include <string> 
#include "noeudrdv.h" 
#include "RDV.h" 
#include "date.h"  // Inclure le fichier d'en-tête Date
#include "heure.h" // Inclure le fichier d'en-tête Heure

class Agenda : public NoeudRdv {
private :
    int taille;
    NoeudRdv* genesis; // pointeur vers un objet NoeudRdv
public:

    Agenda(){ 
        taille = 0;
        genesis = nullptr; // un agenda vide : auncuns rdv, taille 0
    };

    // const car l'argument ne sera pas modifie
    Agenda(const Agenda& unagenda) { // constructeur de recopie
        taille = unagenda.getTaille();
        genesis = unagenda.getGenesis();

    }

    //destructeur : on parcourt tous les noeuds de la liste, on les supprime un par un
    ~Agenda() {
        NoeudRdv* pointeur_actuel = genesis;
        while (pointeur_actuel != nullptr) {
            NoeudRdv* pointeur_suivant = pointeur_actuel->getSuivant();
            // on stock l'adresse du prochain pointeur
            delete pointeur_actuel; // on supprimece qui est sauvegarde en memoire a cet endroit
            pointeur_actuel = pointeur_suivant; // on change le pinteur temporaire
        }
        taille = 0;
        genesis = nullptr;
         
    }

    // on met const pour pouvoir utiliser les getters dans le constructeur de recopie
    int getTaille() const {
        return taille;
    }

    NoeudRdv* getGenesis() const {
        return genesis;
    }

    void ajoute(Rdv unrdv){
        taille ++;

    }

/*
    void ajouteRdv( Rdv unrdv){
        // il faut le mettre bien a sa place : ordre chronologique;
        if (taille ==0){
            taille = 1;
            NoeudRdv monnoeud = NoeudRdv(unrdv); // on cree un instance de la classe noeud, 
            // ce noeud pointe vers nullptr car c'est le dernier de l'agenda
            NoeudRdv* pointeurvesNoeud = &monnoeud; // on cree un ponteur pour ce noeud
            genesis = pointeurvesNoeud; // genesis devient ce pointeur
        }

        else { // dans ce cas la l'agenda n'est pas vide
            Rdv rdvactuel = genesis-> getRdv(); // je recupere le premier rdv garce au pointeur genesis
            NoeudRdv* prochainrdvpointeur = genesis->getSuivant(); // je recupere le prochain pointeur
         
                
            while (unrdv.estapres(rdvactuel) && prochainrdvpointeur != nullptr){ 
                // on n'est pas sur le dernier rdv de l'agenda et le rdv a caser et apres celui que l'on regarde
                // alors on passe au prochain rdv

                // tant que le rdv a rajouter est apres le bloc que je regarde
                rdvactuel = prochainrdvpointeur->getRdv(); // je change le rdv que je regarde actuellement
                prochainrdvpointeur = prochainrdvpointeur->getSuivant();
                }

            // une fois cette boucle passee soit on a trouve le dernier rdv soit le prochain est apres celui que je veux caser 

            // je cree le nouveau noeud a rajouter
            NoeudRdv nouveauneud = NoeudRdv(unrdv, prochainrdvpointeur);

            // je fais un pointeur vers ce noeud
            NoeudRdv* nouveaupointeur = &nouveauneud; 

            // finalement, je change le pointeur du dernier rdv en date et je le change pour le nouveau qui se cale etre les deux
            prochainrdvpointeur->setterSuivant(nouveaupointeur);

            taille++; // finalement j'incremente taille de 1


         }

        } */

// ajouterdv deuxieme version

    void ajouteRdv(Rdv unrdv) {

    if (taille == 0) {// si agenda vide
        // Premier RDV à ajouter
        genesis = new NoeudRdv(unrdv); 
        taille = 1; 
    } else { // agenda pas vide
        NoeudRdv* courant = genesis; 
        NoeudRdv* precedent = nullptr;

        // si le rdv a inserer est apres notre rdv courant ou alors si on est deja au dernier rdv
        while (courant != nullptr && unrdv.estapres(courant->getRdv())) {
            precedent = courant; 
            courant = courant->getSuivant(); 
            // on decale le precedent et le courant de 1
        }

        // une fois la boucle while de passee n est au bon endroit ou mettre le noeud
        NoeudRdv* nouveauNoeud = new NoeudRdv(unrdv, courant); // on creer ce noeud

        
        if (precedent == nullptr) {
            // si on doit le mettre en premier
            genesis = nouveauNoeud; 
        } else {
            // Insérer entre precedent et courant
            precedent->setterSuivant(nouveauNoeud); // le precedent renvoi desormais au nouveau noeud
        }


        // Incrémenter la taille
        taille++;
        }   
    }

    void enleverrdv(Rdv unrdv){
        bool trouve = false;
        NoeudRdv* courant = genesis;
        NoeudRdv* precedent = nullptr;
        for (int i=0; i<taille; i++){
            Rdv rdvactuel = courant->getRdv();
            if (unrdv.estegale(rdvactuel)){ // si on trouve bien le rdv a supprimer

                precedent->setterSuivant(courant->getSuivant()); 
                taille--;
                // on change le pointeur du precedent 
                // il passe du rdv a supprimer a celui d'apres
                unrdv.afficherRdv();
                std::cout << "\n le rdv a bien ete supprime\n";
                trouve = true;
                break;


            }
            else {
                precedent = courant;
                courant = courant->getSuivant();
                
            }


            }

            if (trouve == false){
                unrdv.afficherRdv();
                std::cout << "\n RDV inexistant \n"; }
                
        
    }

    void AfficherlesRdv(){

        NoeudRdv* noeudactuel = genesis;

        for (int i=0; i<taille; i++){

            Rdv rdvactuel = noeudactuel->getRdv();

            rdvactuel.afficherRdv(); // on affiche
            noeudactuel = noeudactuel->getSuivant(); // on passe au suivant
            if (noeudactuel == nullptr){
                break;
            }
        }
    }



    };
#endif