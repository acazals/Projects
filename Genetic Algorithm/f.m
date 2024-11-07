
% fonction f(x,y)= sin(2pix)sin(2piy) +x 
% le max global est en (0.75, 0.7754..)
% il y a en plus un max local et deux min
%{
function FF=f(x)
    x1 = x(1,:); x2 = x(2,:); x3 = x(3,:);
    FF= x1; % le poids
end
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % pour optimiser le poids

%{
function fitness_value = f(x, poids, Pmax)
    % x est un individu (colonne de 30 gènes)
    % poids est un vecteur contenant les poids des conteneurs
    % Pmax est la capacité maximale de poids

    % Calculer le poids total de l'individu
    poids_total = sum(x .* poids);  % Produit élément par élément et somme

    % Si le poids total dépasse Pmax, la fitness est 0
    if poids_total > Pmax ||  volume_total > Vmax
        fitness_value = 0;  % Individu non valide

   

    else
        fitness_value = poids_total;  % Fitness est la somme des poids
    end
end
%}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pour optimiser le volume :


%{
function fitness_value = f(x, poids, volume, Pmax, Vmax)
    % x est un individu (colonne de 30 gènes)
    % poids est un vecteur contenant les poids des conteneurs
    % Pmax est la capacité maximale de poids

    % debugage
    assert(iscolumn(x) && length(x) == 30, 'Error: x must be a 30x1 column vector.');
    assert(iscolumn(poids) && length(poids) == 30, 'Error: poids must be a 30x1 column vector.');
    assert(iscolumn(volume) && length(volume) == 30, 'Error: volume must be a 30x1 column vector.');
    % Calculer le poids total de l'individu
    volume_total = sum(x .* volume);  % Produit élément par élément et somme
    poids_total = sum(x .* poids);
    % Si le poids total dépasse Pmax, la fitness est 0

    if (poids_total > Pmax) ||  (volume_total > Vmax)
        fitness_value = 0;  % Individu non valide
    else
        fitness_value = volume_total;  % Fitness est la somme des volumes
    end
end

%}
 
%{

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pour optimiser le prix : 
% attention a bien rajouter le vecteur des prix dans les arguments pour
calculer les valeurs de fitness

function fitness_value = f(x, poids, volume, prix Pmax, Vmax)
    % x est un individu (colonne de 30 gènes)
    % poids est un vecteur contenant les poids des conteneurs
    % Pmax est la capacité maximale de poids

    % debugage 
    assert(iscolumn(x) && length(x) == 30, 'Error: x must be a 30x1 column vector.');
    assert(iscolumn(poids) && length(poids) == 30, 'Error: poids must be a 30x1 column vector.');
    assert(iscolumn(volume) && length(volume) == 30, 'Error: volume must be a 30x1 column vector.');

    % Calculer le poids total de l'individu
    volume_total = sum(x .* volume);  % Produit élément par élément et somme
    poids_total = sum(x .* poids);
    prix_total = sum(x .* prix);
    % Si le poids total dépasse Pmax, la fitness est 0

    if (poids_total > Pmax) ||  (volume_total > Vmax)
        fitness_value = 0;  % Individu non valide
    else
        fitness_value = prix_total;  % Fitness est la somme des volumes
    end
end

%}

%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% fonction pour tout optimiser : 
function fitness_value = f(x, poids, volume, prix, Pmax, Vmax)
    % pondération
    poids_rel = 0.4;   
    volume_rel = 0.3;  
    prix_rel = 0.3;   

    % Debug 
    assert(iscolumn(x) && length(x) == 30, 'Error: x must be a 30x1 column vector.');
    assert(iscolumn(poids) && length(poids) == 30, 'Error: poids must be a 30x1 column vector.');
    assert(iscolumn(volume) && length(volume) == 30, 'Error: volume must be a 30x1 column vector.');
    assert(iscolumn(prix) && length(prix) == 30, 'Error: prix must be a 30x1 column vector.');

    % sommes pondérées
    poids_total = sum(x .* poids);
    volume_total = sum(x .* volume);
    prix_total = sum(x .* prix);

    %  contraintes de capacité
    if (poids_total > Pmax) || (volume_total > Vmax)
        fitness_value = 0;  %  individu non valide
    else
        
        fitness_value = poids_rel * poids_total + ...
                        volume_rel * volume_total + ...
                        prix_rel * prix_total;
    end
end