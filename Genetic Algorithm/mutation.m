
%   A = MUTATION(X,p,Pmut,dmut) mutates the genome of X into A, with Pmut the
%   probability of mutation of each gene and dmut the intensity of
%   mutation. Each gene is assumed to be in the interval [0, 1].

%{
function A=mutation(X,p,Pmut,dmut)
    mut = rand(p,1) < Pmut;       % vecteur de booleen 0 si < Pmut, 1 sinon
    A = X + dmut * mut.*randn(p,1);  % on modifie seulement les composantes
                                     % non-nules de mut, d'un facteur
                                     % dmut*loi nomale 
    A = min(max(A,0.0),1.0);       % on remet entre [0,1] au cas ou
end

%} 

% mutation pour les genes du cargo : On inverse la valeur du gène 
% si sa probabilité de mutation est inférieure à un certain seuil

function A = mutation(X, p, Pmut)
    mut = rand(p, 1) < Pmut;  % 1 pour les gènes à muter, 0 sinon
    A = X;                     % On part de la solution d'origine
    A(mut) = 1 - A(mut);       % On inverse seulement les gènes marqués pour mutation
end