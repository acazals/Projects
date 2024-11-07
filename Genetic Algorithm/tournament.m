
%   A1 = TOURNAMENT(A,m) picks the best individual amongst m randomly
%   picked individuals.
function A1=tournament(A,m)
    [p,N]=size(A); % dimension de la matrice A
    B = zeros(p,m); % matrie avec les elements a choisir
    
    % m nb d'individus a selectionner

    for i = 1:m
        B(:,i) = A(:,randi(N));  %on selectionne m individus aleatoirement
    end
    A1t = sortrows(B',-p);  % on les tri ordre décroissant en fonction de la fitness decroissante

    A1 = A1t(1,:)';         % on garde le premier, ie le meilleur
    % on prend la premiere ligne : correspond a l'individu qui a la
    % meilleure fitness (on prend ses genes)
end 