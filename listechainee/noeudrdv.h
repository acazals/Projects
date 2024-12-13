#ifndef NOEUDRDV_H
#define NOEUDRDV_H


#include <string>  
#include "RDV.h" 
#include "date.h"  
#include "heure.h" 

class NoeudRdv : public Rdv {
private :
    Rdv monrdv;
    NoeudRdv* suivant; //
public:

    // constructeur par default : 
    NoeudRdv(){
        monrdv = Rdv(); // constructeur par default de RDV
        suivant = nullptr;
    };
    // constructeur avec juste rdv comme parametre
    NoeudRdv(const Rdv& unrdv) {
    // attribut rdv avec un rdv passe en ref
        monrdv = unrdv;
        suivant = nullptr; // pointe vers aucuns autre element de la liste
    };
    
    // constructeur pour aussi initialiser le prochain
    NoeudRdv(const Rdv& unrdv, NoeudRdv* point_suivant ) {
        monrdv = unrdv;
        suivant = point_suivant;
    };

    Rdv getRdv(){
        return monrdv;
    }

    NoeudRdv* getSuivant(){
        return suivant;
    }

    void setterRdv(const Rdv& unrdv){
        monrdv = unrdv;
    }

    void setterSuivant(NoeudRdv* point_suivant){
        suivant = point_suivant;
    }

};
#endif
