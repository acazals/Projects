import java.util.ArrayList;

public class Bdr {
    private int taille;
    private ArrayList<Regle> contenu;


    public Bdr(){
        contenu =new ArrayList<Regle>();
        String [] t1={"personne_aisee","temps_libre","","","peut_voyager"};
        Regle R1=new Regle(t1);
        contenu.add(R1);
        String [] t2={"temps_libre","","","","peut_faire_de_la_poterie"};
        Regle R2=new Regle(t2);
        contenu.add(R2);
        String [] t3={"peut_peindre","","","","peut_faire_un_produit_artisanal"};
        Regle R3=new Regle(t3);
        contenu.add(R3);
        String [] t4={"peut_faire_de_la_poterie","","","","peut_faire_un_produit_artisanal"};
        Regle R4=new Regle(t4);
        contenu.add(R4);
        String [] t5={"peut_faire_un_produit_artisanal","artiste","","","peut_faire_une_oeuvre_d'art"};
        Regle R5=new Regle(t5);
        contenu.add(R5);

        taille=contenu.size();
    }


    public int getTaille(){
        return this.taille;
    }

    public ArrayList<Regle> getContenu() {
        return this.contenu;
    }

    @Override
    public String toString() {
        return "Bdr{" +
                "taille=" + taille +
                ", contenu=" + contenu +
                '}';
    }
}
