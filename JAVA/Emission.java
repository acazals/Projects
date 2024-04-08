package com.company;

public class Emission {//ouverture diu bloc correspondant à la classe
    protected Chanson playlist[];
    protected int duree;// durée en minutes de l'émission
    protected int numero; //nombre de chansons dans la playlist
    protected int temps;//temps total des chansons dans la playlist en secondes

    public Emission(int m)
    {
        duree = m;
        playlist = new Chanson[m/2];//taille égale à la durée de l'émission /2, 
		//exemple en 20 minutes on estime que l'on ne pourra pas passer plus de 10 chansons
		//numero et temps ne sont pas initialisées ici car, comme ce sont des variables d'instance , 
		//elles le sont automatiquement lors de leur déclaration
    }

    public Chanson getChanson(int i) { return playlist[i]; }

    public boolean ajoute(Chanson c)
    {
        if(c.duree() + temps <= 60 * duree  && numero<duree/2)
			// si en ajoutant la chanson proposée on ne dépasse pas le temps de l'émission et  si il reste de la place dans playlist
        {
            playlist[numero] = c;//ajout de la chanson proposee dans playlist
            temps = temps + c.duree();// mise à jour du temps de la plylist
            numero = numero + 1;//mise à jour du nombre de chansons dans la playlist
            return true;
        }
        else
            return false;//on peut ajouter un message d'erreur
    }

    public void passe(int i)
    {
        playlist[i].passe();
		//on envoie à playlist[i] (qui est une chanson) ce message donc c'est la méthode passe() de Chanson qui sera déclenchée
    }

    public void passeTout()
    {
        int i;
        for(i = 0; i < numero; i++)
            passe(i);//ou this.passe(i) c'st dons la méthode définie juste avant celle-ci qui sera déclanchée
    }
}// fermeture du bloc class
