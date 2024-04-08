package com.company;

public class Main {

    public static void main(String[] args) {
        Chanson c1 = new Chanson("La javanaise _______", "J'avoue j'en ai bav�...", 2, 50);
        Chanson c2 = new Chanson("La java des bombes atomiques___", "Mon oncle un fameux bricoleur...", 3, 32);
        Chanson c3= new Chanson("La Java de Broadway___", "Quand on fait la Java...",4,7);
        Chanson c4= new Chanson("Le Jazz et la Java___", "Quand le jazz est Quand le jazz est là La java s'en La java s'en va",2,25);

        EmissionCommentee e = new EmissionCommentee(6);
        e.ajoute(c1);
        e.ajoute(c2);
        e.ajoute(c3);
        e.ajoute(c4);
        e.passeTout();
    }
}
