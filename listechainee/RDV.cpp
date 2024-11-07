#include "RDV.h"
#include "date.h"  // Inclure le fichier d'en-tête Date
#include "heure.h" // Inclure le fichier d'en-tête Heure
#include <iostream>
#include <string> 
#include <stdexcept> // Pour std::out_of_range



Rdv::Rdv(){ // constructeur par default
    nbparticipants = 0;
    mesparticipants = new std::string[10];
}

void Rdv::afficherRdv(){
    std::cout << " \n \nla date du rdv est \n ";
    madate.affiche();
    std::cout << "l'heure du rdv est \n";
    monheure.affiche();
    std::cout << "le lieu du rdv est : " << monlieu << "\n";
    std::cout << "le nombre de participants est : " << nbparticipants << "\n";
    std::cout << "la liste des participants est : \n";
    for (int i=0; i<nbparticipants; i++) {
        std::cout << mesparticipants[i]<<"\n";
    }

}

void Rdv::saisieParticipants(){
    mesparticipants = new std::string[nbparticipants];
    std::cout << "veuillez rentrer les noms des " << nbparticipants << " participants \n";
    for (int i=0; i<nbparticipants; i++) {
        std::cin >> mesparticipants[i]; // je mets la avleur dans la case i du tableau
    }
}



void Rdv::saisieLieu(){
    std::cout << "veuillez saisir le lieu svp \n";
    std::cin >> monlieu;
}

void Rdv::saisieNb(){
    std::cout << "veuillez rentrer le nombre de participants \n";
    std::cin >> nbparticipants;
}

Rdv::Rdv(int n) {  // saisie complete du rdv
    // il faut que l'utilisateur entre la date, l'heure, le nb de participants, les participants, le lieu
    saisieNb();
    saisieLieu();
    saisieParticipants();
    // on herite des methodes saisie heure et saisie date
    madate =date(n);
    monheure = heure(n);
}

void Rdv::setDate(const date& dateRdv) {
    madate = dateRdv;

}

void Rdv::setHeure(const heure& heureRdv){
    monheure = heureRdv;
}

void Rdv::setLieu(const std::string& lieuRdv){
    monlieu = lieuRdv;
}

void Rdv::setNombreDeParticipants(int nombreparticipants){
    nbparticipants = nombreparticipants;
}

void Rdv::setParticipants(std::string* ps){
    mesparticipants = ps;
}

void Rdv::setParticipant(int i, std::string s){
    try {
        if (i < 0 || i >= nbparticipants) {  // si i est invalide
            throw std::out_of_range("Index hors des limites des participants."); // Lancer une exception
        }
        mesparticipants[i] = s; // Affectation comme prevue si l'index est valide
    } catch (const std::out_of_range& e) {
        std::cerr << "Erreur : " << e.what() << std::endl; // message d'erreur
    }
}

// pour cela je rajoute une methade estegale dans heure et date
bool Rdv::estcompatible(Rdv autrerdv){
    if (madate.estegale(autrerdv.madate) && monheure.estegale(autrerdv.monheure)){
        return false;
    }
    return true;
}  