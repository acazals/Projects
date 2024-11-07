#include "date.h"
#include <iostream>
#include <cmath>

date::date(){ // constructeur par default
    day = 1;
    month = 1;
    year = 2000;
} 
date::date(int d, int m, int y){
    if (checkdate(d, m, y)){ // valeurs admissibles
        day =d;
        month = m;
        year =y;
    }
    else { // sinon par default
        day = 1;
        month =1;
        year = 2000;
    }
}

date::date(int n){
    while(true){
        std::cout << "veuillez rentrer le jour \n";
        int tempday;
        std::cin >> tempday;
        std::cout<< "veuillez saisir le mois : \n";
        int tempmonth;
        std::cin >> tempmonth;
        std::cout<< "veuillez saisir l'annee : \n";
        int tempyear;
        std::cin >> tempyear;

        if (checkdate(tempday, tempmonth, tempyear)) { // on verifie que c'est admissible
            // si l'horaire est admissible
            day = tempday;
            month = tempmonth;
            year  = tempyear;
            break;
         }
        else{
            std::cout << " une des choses saisies n'est pas valide. Veuillez réessayer.\n";
        } 
}
}

bool date::checkdate(int d, int m, int y){ 
    if (d >= 1 && d <= 31 && m >= 1 && m <= 12 && y >= 2000 && y <= 2050) {
        return true;
    }
    return false;
}


void date::affiche(){
    std::cout << day << "/" << month << "/" << year << "\n";
}

// getters et setters 

int date::getter_day(){
    return day;
}

int date::getter_month(){
    return month;
}

int date::getter_year(){
    return year;
}

void date::setter_day(int n){
    if (n>=1 && n <= 31){
        day = n;
    }
}

void date::setter_month(int m){
    if ( m>=1 && m <= 12) {
        month = m;
    }
}

void date::setter_year(int y){
    if (y>=2000 && y <=2050) {
        year = y;
    }
}

void date::saisiedate(){
    while(true){
        std::cout << "veuillez rentrer le jour \n";
        int tempday;
        std::cin >> tempday;
        std::cout<< "veuillez saisir le mois : \n";
        int tempmonth;
        std::cin >> tempmonth;
        std::cout<< "veuillez saisir l'annee : \n";
        int tempyear;
        std::cin >> tempyear;

        if (checkdate(tempday, tempmonth, tempyear)) { // on verifie que c'est admissible
            // si l'horaire est admissible
            day = tempday;
            month = tempmonth;
            year  = tempyear;
            break;
         }
        else{
            std::cout << " une des choses saisies n'est pas valide. Veuillez réessayer.\n";
        } 
}
}


bool date::estegale(date date2){
    return (day == date2.day && month == date2.month && year == date2.year);
}