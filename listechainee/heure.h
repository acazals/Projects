#ifndef HEURE_H
#define HEURE_H

class heure {
private :
    int maminute;
    int monheure; //
public:
    heure(); // constructeur par default : minuit
    heure(int n); // constructeur utilisateur avec un argument pour le differencier de celui par default
    heure (int m, int h); //constructeur; avec par default : 00h00
    static bool checkhour (int m, int h); // on verifie que l'heure est coherente
    int getter_minute();
    int getter_heure();
    void setter_minute (int m);
    void setter_heure(int h);
    void affiche();
    void saisieHeure();
    bool estegale(heure heure2);
    bool estapres(heure heure2){
        int minute1 = maminute;
        int minute2 = heure2.getter_minute();

        int monheure1 = monheure;
        int monheure2 = heure2.getter_heure();

        if (monheure1 > monheure2 || monheure1 == monheure2 && minute1 > minute2){
            return true;
        }

        return false;
    }

};
#endif