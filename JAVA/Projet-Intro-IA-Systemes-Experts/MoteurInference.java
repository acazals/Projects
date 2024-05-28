import java.util.Arrays;
import java.util.ArrayList;


public class MoteurInference{

    private Bdf mesfaits;
    private Bdr mesregles;

    public MoteurInference(Bdf BaseFaits, Bdr BaseRegles){
        this.mesfaits = BaseFaits;
        this.mesregles = BaseRegles;
    }
    public boolean CondDansBdf(String Condition) {
        int n = mesfaits.GetTaille();
        ArrayList<String> contenu = this.mesfaits.GetContenu();
        for  (int i=0; i<n; i++) {
            String monfait = contenu.get(i);
            if (Condition.equals(monfait)) {
                return true;
            }
        }
        return false;
    }

    public boolean RegleDeclenchee(Regle R){
        int mataille = R.getTaille();
        String[] mesvaleurs = R.getValeurs();
        String MaConclusion = mesvaleurs[mataille -1];

        if ( !CondDansBdf(MaConclusion) ){ // conclusion pas dans la base de fait
            for (int i=0; i< mataille-1; i++){ // on parcoure toutes les conditions : les strings jusqu'a i-2 parce que i-1 est la conclusion
                if (!mesvaleurs[i].equals("")){ // si on ne s'adresse pas a une chaine vide
                    if (!CondDansBdf(mesvaleurs[i])){ // si cette condition non vide n'est pas dans la base de fait
                        return false; // alors au moins une condition de la regle n'est pas verifiee
                    }
                }
            }

            return true; // on renvoie le booleen
        }
        else {
            return true; // si conclusion deja dans la Bdf alors regle deja declenchee
        }


    }

    public Bdf ChainageAvant(){
        // on cree un tableau pour voir les regles qui ont deja ete declecnhees
        int n = mesregles.getTaille();
        boolean[] tableau_declenchement = new boolean[n];
        for (int i = 0; i < n; i++) {
            tableau_declenchement[i] = false;
        }
        ArrayList<Regle> contenu = mesregles.getContenu(); // ArrayList de Regles
        boolean Saturation = false;
        while (!Saturation){
            int compteur = 0;
            for (int i=0 ; i<mesregles.getTaille(); i++){ // on verifie la base de regles
                String maConclusion = contenu.get(i).getConclusion(); // on recupere la conclusion

                if ( RegleDeclenchee(contenu.get(i)) == true && !tableau_declenchement[i] ){// si la regle peut se declencher pour la premiere fois
                    tableau_declenchement[i] = true;
                    compteur=1;
                    if (!CondDansBdf(maConclusion)){  // on verifie que la conclusion ne soit pas deja dans la base de faits
                        mesfaits.AjoutBdf(maConclusion);
                    } //on ajoute la conclusion a la Base de faits
                }
            }
            if (compteur==0){
                Saturation = true;
            }
        }
        return mesfaits;
    }

    public boolean chainagearriere(String but){
        int n = mesregles.getTaille(); // longueur de la base des regles
        ArrayList<Regle> contenu = mesregles.getContenu(); // ArrayList de Regles
        if (CondDansBdf(but)){
            return true;
        }
        else {
            for (int i = 0; i<n; i++){ // pour chaque regle
                String maConclusion = contenu.get(i).getConclusion(); // on recupere la conclusion
                if (but.equals(maConclusion)) { // si on a trouve une regle qui a la bonne conclusion
                    if (verifier_regle_arriere(contenu.get(i))){
                        return true;
                    }; // recursivite
                }
            }

        }
        return false; // aucunes regles dont la conclusion permet d'arriver au but n'a   toutes ses conditions verifiees
    }

    public boolean verifier_regle_arriere(Regle  R) {
        int n = R.getTaille();
        String[] mesvaleurs = R.getValeurs();
        for (int i=0; i<n-1; i++){ // on parcourt toutes les conditions : on va jusqu a n-2
            if (!mesvaleurs[i].equals("")){ // si la condition est non vide
                if (!CondDansBdf(mesvaleurs[i])){ // si cette condition non nulle n'est pas verifiee
                    if (!chainagearriere(mesvaleurs[i])){
                        return false;
                    }; // recursivite imbriquee
                }
            }
        }
        return true;

    }


}
