#ifndef RDV_H
#define RDV_H

#include <string>   
#include "date.h"  // Inclure le fichier d'en-tête Date
#include "heure.h" // Inclure le fichier d'en-tête Heure

// classe RDV contient : date, heure, lieu(string), nb de participants, liste de participants string*, 

class Rdv : public date, public heure {
private:
    date madate;
    heure monheure; 
    std::string monlieu;
    int nbparticipants; // nb de participants
    std::string* mesparticipants; 


public:
    Rdv(); // constructeur par default : 0 participants, tableau de 10 elements
    Rdv(int n); // constructeur pour la saisie complete
    Rdv(int j, int m, int a, int h, int min, std::string lieu, int nbparticipants, std::string* participants);

    Rdv(date unedate, heure uneheure, std::string unlieu, int unnb, std::string* desparticipants ){
        madate = unedate;
        monheure = uneheure;
        monlieu = unlieu;
        nbparticipants = unnb;
        mesparticipants = desparticipants;

    }
    void afficherRdv();
    void saisieParticipants();
    void saisieLieu();
    void saisie(); // saisie complete
    void saisieNb();
    void saisieHeure();
    void saisieDate();
    void setDate(const date& daterdv);
    void setHeure(const heure& heurerdv);
    void setLieu(const std::string& lieuRdv);
    void setNombreDeParticipants(int nombreDeParticipants);
    void setParticipants(std::string* ps) ;
    void setParticipant(int i, std::string s);
    bool estcompatible(Rdv autrerdv);

    date getter_date(){
        return madate;
    } 

    heure getter_heure(){
        return monheure;
    }

    bool estapres( Rdv autreRdv){
        date date1 = madate;
        date date2  = autreRdv.getter_date();

        heure heure1 = monheure;
        heure heure2 = autreRdv.getter_heure();

        // si la date 1 est apres ou alors mm date mais heure plus tard
        if (date1.estapres(date2) || date1.estegale(date2) && heure1.estapres(heure2)){
            return true;

        }

        return false;
    }

    bool estegale(Rdv autreRdv){
        date date1 = madate;
        date date2  = autreRdv.getter_date();

        heure heure1 = monheure;
        heure heure2 = autreRdv.getter_heure();

        if (date1.estegale(date2) && heure1.estegale(heure2)) {
            return true;
        }
        return false;

    }
};

#endif
