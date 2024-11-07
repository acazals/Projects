
%   A = CROSSOVER(A1,A2,p) builds the genome of the child A of the parents
%   A1 and A2
%{
function A=crossover(A1,A2,p)
    A = A2;
    q = randi(p);
    for i = 1:q,
        A(i) = A1(i);
    end
end
%}

function A = crossover(A1, A2, p)
    % A1, A2 : Les deux individus parents
    % p : Le nombre de gènes (excluant la fitness)

    % Initialiser A avec les gènes de A2, en excluant la fitness
    A = A2;

    % Choisir un point de croisement aléatoire entre 1 et p
    q = randi(p);

    % changer les gènes jusqu'au point q
    for i = 1:q
        A(i) = A1(i);
    end
    
    % Ne pas oublier d'inclure la fitness (non modifiée)
    A(end) = 0;  % réinitialiser la fitness à 0 pour la nouvelle solution
end