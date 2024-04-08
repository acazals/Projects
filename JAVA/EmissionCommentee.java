package com.company;

public class EmissionCommentee extends Emission{
    public EmissionCommentee(int m)
    {
        super(m);

    }


    public void passe(int i)
    {
        System.out.println(getChanson(i).getTitre());
        super.passe(i);
    }

    public void passeTout()
    {
        System.out.println("---Bonjour");
        super.passeTout();
        System.out.println("---Au revoir");
    }
}
