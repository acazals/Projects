#include "heure.h"
#include <iostream>

heure::heure(){
    maminute = 0;
    monheure = 0;
}
heure::heure(int m, int h){
    if (checkhour(m,h)){
        maminute = m;
        monheure =h;
    }
    else {
        maminute = 0;
        monheure=0;
    }
}

heure::heure(int n){
    while(true){
        std::cout << "veuillez rentrer les minutes \n";
        int temporaryint;
        std::cin >> temporaryint;
        std::cout<< "veuillez saisir l'heure de 0 a 23 : \n";
        int temporaryint2;
        std::cin >> temporaryint2;

        if (checkhour(temporaryint, temporaryint2)) { // d'abord les minutes ensuite les heures
            // si l'horaire est admissible
            monheure = temporaryint2;
            maminute = temporaryint;
            break;
         }
        else{
            std::cout << "L'heure ou les minutes saisies ne sont pas valides. Veuillez réessayer.\n";
        } 
}

}

bool heure::checkhour(int m, int h){
    if ( m>=0 && m<=59 && h>=0 && h<=23) { // heure admissible
        return true;
    }
    else {
        return false;
    }
}

int heure::getter_heure(){
    return monheure;
}

int heure::getter_minute(){
    return maminute;
}

void heure::setter_heure(int h){
    if (h>=0 && h<=23) {
        monheure = h;
    }
}

void heure::setter_minute(int m){
    if (m>=0 && m<=59){
        maminute = m;
    }
}
void heure::affiche(){
    std::cout << monheure << " : " << maminute << "\n" ;
}


// boucle infinie pour que l'utilisateur rentre bien des horaires admissibels
void heure::saisieHeure(){
    while(true){
        std::cout << "veuillez rentrer les minutes \n";
        int temporaryint;
        std::cin >> temporaryint;
        std::cout<< "veuillez saisir l'heure de 0 a 23 : \n";
        int temporaryint2;
        std::cin >> temporaryint2;

        if (checkhour(temporaryint, temporaryint2)) { // d'abord les minutes ensuite les heures
            // si l'horaire est admissible
            monheure = temporaryint2;
            maminute = temporaryint;
            break;
         }
        else{
            std::cout << "L'heure ou les minutes saisies ne sont pas valides. Veuillez réessayer.\n";
        } 
}
}

bool heure::estegale(heure heure2){
    return (monheure == heure2.monheure && maminute == heure2.maminute);
}