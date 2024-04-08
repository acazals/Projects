package com.company;

public class Chanson {

    private String titre;
    private String texte;
    private int minutes;
    private int secondes;

    public String getTitre() { return titre;}// générer

    public Chanson(String ti, String te, int m, int s)
    {
        titre = ti;//this.titre=ti;
        texte = te;//this.texte=te;
        minutes = m;//this.minutes=m;
        secondes = s;//this.secondes=s;
    }

    public void passe()
    {
        System.out.println(texte);
    }

    public int duree()
    {
        return 60 * minutes + secondes;//return 60 * this.minutes + this.secondes;
    }

}
