/*
#include <string> 
#include <stdexcept> // Pour std::out_of_range

#include "date.h"  // Inclure le fichier d'en-tête Date
#include "heure.h" // Inclure le fichier d'en-tête Heure

int main(){
    
    // d'abord un constructeur utilisateur
    //Rdv monrdv = Rdv(2);
    //monrdv.afficherRdv(); 
    
    // ensuite un constructeur par default et les methodes setparticipants ect
    Rdv monrdv2 = Rdv(); // constructeur par default
    monrdv2.setNombreDeParticipants(2); // deux participants
    date madate = date(15,10,2024); // on cree une date instance de la classe date
    monrdv2.setDate(madate); //on met la date dans l'instance de classe rdv monrdv2
    monrdv2.saisieLieu(); // l'utilisateur saisie le lieu
    heure monheure2 = heure(30, 18); // 18h30
    monrdv2.setHeure(monheure2); // on defini bien l'heure
    // on definit un string* pour les participants
    std::string* participants2 = new std::string[2];  // Allocation dynamique 
    participants2[0] = "adman";
    participants2[1] = "anto";
    monrdv2.setParticipants(participants2); // on a bien defini les participants
    monrdv2.afficherRdv();
    monrdv2.setParticipant(1, "Nino");
    monrdv2.afficherRdv();




    return 0;
} */

#include <iostream>
#include "Agenda.h" 
#include "RDV.h"
#include "date.h"
#include "heure.h"

int main() {
    // Créer  agenda
    Agenda monAgenda;

    // listes de participants pour chaque rendez-vous
    std::string participants1[] = {"Alice", "Bob"};
    std::string participants2[] = {"Charlie", "David", "Eve"};
    std::string participants3[] = {"Frank"};

    // RDV
    Rdv rdv1(date(22, 10, 2024), heure(0, 10), "Bureau A", 2, participants1);
    Rdv rdv2(date(21, 10, 2024), heure(30, 12), "Salle B", 3, participants2);
    Rdv rdv3(date(20, 10, 2024), heure(0, 9), "Café C", 1, participants3);

    // Agenda avec les RDVs
    monAgenda.ajouteRdv(rdv1);
    monAgenda.ajouteRdv(rdv2);
    monAgenda.ajouteRdv(rdv3);

    
    std::cout << "Agenda après ajout des rendez-vous : " << std::endl;
    monAgenda.AfficherlesRdv();

   
    std::cout << "\nSuppression du rendez-vous du 21/10/2024 à 12:30" << std::endl;
    monAgenda.enleverrdv(rdv2);

    // Afficher les RDVs restants
    std::cout << "\nAgenda après suppression d'un rendez-vous : " << std::endl;
    monAgenda.AfficherlesRdv();

    // Vider  l'agenda
    std::cout << "\nSuppression de tous les rendez-vous..." << std::endl;
    monAgenda.~Agenda();  // Appeler explicitement le destructeur pour vider la liste

    // Afficher l'agenda vide
    std::cout << "\nAgenda après suppression de tous les rendez-vous : " << std::endl;
    monAgenda.AfficherlesRdv();

    return 0;
}
