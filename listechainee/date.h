#ifndef DATE_H
#define DATE_H
#include <memory>  // Pour std::unique_ptr

class date {
private :
    int day;
    int month;
    int year;
public : 
    date();
    date(int n); // constructeur utilisateur
    date (int j, int m, int ); // constructeur par default
    static bool checkdate(int j, int m, int y); // on peut l'appeler sans creer d'instances de la classe
    void affiche();
    int getter_day();
    int getter_month();
    int getter_year();
    void setter_day(int d);
    void setter_month(int m);
    void setter_year(int y);
    void saisiedate();
    bool estegale(date date2);
    bool estavant(date date2) {
        int year1 = getter_year();
        int year2 = date2.getter_year();

        int month1 = getter_month();
        int month2 = date2.getter_month();

        int day1 = getter_day();
        int day2 = date2.getter_day();

        if (year1 < year2 || year1 == year2 && month1<month2 || year1==year2 && month1 == month2 &&  day1 < day2) { 
           return true;
        }

        return false;

    }   

    bool estapres(date date2){

        int year1 = getter_year();
        int year2 = date2.getter_year();

        int month1 = getter_month();
        int month2 = date2.getter_month();

        int day1 = getter_day();
        int day2 = date2.getter_day();

        if (year1 > year2 || year1 == year2 && month1>month2 || year1==year2 && month1 == month2 &&  day1 > day2) { 
           return true;
        }

        return false;

    }

};
#endif