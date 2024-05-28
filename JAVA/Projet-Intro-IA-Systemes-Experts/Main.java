import java.util.ArrayList;

public class Main {
    public static void main(String[] args){
        Bdf baseDeFaits = new Bdf();
        System.out.println(baseDeFaits);
        Bdr baseDeRegles = new Bdr();
        System.out.println(baseDeRegles);
        MoteurInference monMoteur = new MoteurInference(baseDeFaits, baseDeRegles);
        System.out.println("la nouvelle base de faits est "+monMoteur.ChainageAvant());
        System.out.println(monMoteur.chainagearriere("peut_faire_une_oeuvre_d'art"));

    }

}
