import java.util.ArrayList;
import java.util.Scanner; // Importation de la classe Scanner depuis le package java.util

public class Bdf{

    private ArrayList<String> contenu;
    private int taille;

    public Bdf (){
        this.taille = 0;
        contenu = new ArrayList<String>();
        String fait;
        do {
            System.out.println("Entrez le fait suivant :");
            Scanner entree = new Scanner(System.in);
            fait = entree.nextLine();
            contenu.add(fait);}
        while (!fait.equals("fin"));
        contenu.remove(contenu.size() -1);
        this.taille = contenu.size();

    }

    public void AjoutBdf(String fait){
        taille ++;
        this.contenu.add(fait);

    }

    public ArrayList<String> GetContenu() {
        return this.contenu;

    }

    public int GetTaille(){
        return this.taille;
    }


    public void setContenu(ArrayList<String> contenu) {
        this.contenu = contenu;
    }

    public void setTaille(int taille) {
        this.taille = taille;
    }

    public String toString() {
        return "BDF{" +
                "contenu=" + contenu +
                ", taille=" + taille +
                '}';
    }
}
