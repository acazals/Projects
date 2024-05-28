import java.util.Arrays;


public class Regle{

    private String[] Schema;
    private String[] Valeurs;
    private int Taille;

    public Regle(String[] mesvaleurs){
        this.Valeurs = mesvaleurs;
        this.Taille= Valeurs.length;
        this.Schema =  new String[Taille];


        for (int i = 0; i < Schema.length; i++){
            Schema[i] = "condition["+i+"]";
        }
        this.Schema[Taille-1] = "Conclusion";
    }

    public int getTaille(){
        return this.Taille;
    }

    public String[] getValeurs(){
        return this.Valeurs;
    }

    public String getConclusion(){
        return this.Valeurs[Taille-1];
    }

    @Override
    public String toString() {
        return "Regle{" +
                "Schema=" + Arrays.toString(Schema) +
                ", Valeurs=" + Arrays.toString(Valeurs) +
                ", Taille=" + Taille +
                '}';
    }
}
