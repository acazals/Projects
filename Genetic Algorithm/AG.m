%%% GENETIC ALGORITHM

clear all

% Parameters de l'algorithme
% pb du cargo : individu = solution
K = 10000;      % Number of generations
M = 5;          % Size of tournaments
Pmut = 0.5;     % Probability of gene mutation



% Chargement des données de conteneursdata = readtable('data_container.txt', 'Delimiter', ','); 
data = readtable('data_container.txt', 'Delimiter', ','); % Load the data 
poids = data{:, 1};   
volume = data{:, 2}; 
prix = data{:, 3};    

size(data)       % 
size(poids)     % [30, 1]
size(volume)    %  [30, 1]
size(prix)      % [30, 1]

% Paramètres du cargo
Pmax = 800;  % Poids maximal
Vmax = 600;  % Volume maximal

% Paramètres de la population
N = 50;      % Taille de la population (nombre de solutions)
P = 30;  % Nombre de conteneurs disponibles

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initialisation de la population
population = zeros(P+1, N);  % Matrice de dimension P+1 x N, P+! : la fitness
fitness = zeros(1, N);     % Vecteur pour stocker la fitness de chaque individu

for i = 1:N
    % Génération aléatoire d'un individu
    % Un individu est un tableau binaire de taille P
    individu = randi([0, 1], P+1, 1);  % 0 ou 1 pour chaque conteneur
    individu(P+1) = 0 ; % on met le 0 a la fin pour y stocker la fitness

    % Calcul du poids total et du volume total
    poids_total = sum(individu(1:P) .* poids); % la somme des poids
    volume_total = sum(individu(1:P) .* volume); % la somme des volumes 
    
    % Vérifier si l'individu respecte les contraintes
    while poids_total > Pmax || volume_total > Vmax
        individu = randi([0, 1], P+1, 1);  % Regénérer l'individu si les contraintes ne sont pas respectées
        poids_total = sum(individu(1:P) .* poids);
        volume_total = sum(individu(1:P) .* volume);
    end
    population(:, i) = individu;  % Ajout de l'individu à la colonne i de la matrice population
    

end 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 


% A matrice de dimension N *(P+1) : nb de genes plus 1 * N taille de la
% population
% 30 premieres lignes : genes de l'individu, ligne 31 : la fitness en
% fonction des deux genes

fbest = 0; % on initialise fbest a 0
fplot = zeros(K,1); % sur chaque generation : on sotkce la meilleure valeur de la fitness trouvee
% cela nous donne sur les K generations K valeurs de fmax trouvees

%%% Boucle sur les générations
for i = 1:K
    % Evaluation de la fonction pour tous les individus
    % f appliquee a chaque colonne de A, 
    for j = 1:N  % Boucle à travers chaque individu de la population
        x = population(1:P, j);  % Extraire le j-ème individu (un vecteur colonne de taille 30x1)
        population(P + 1, j) = f(x, poids, volume, prix, Pmax, Vmax);  % Stocker la valeur de fitness
    end
    % on stock la fitness de l'individu i dans la ligne p+1
    
    % tri par ordre décroissant de f: premiere colonne le meilleur individu
    population = sortrows(population',-(P+1))';
    % A transposee, 
    % tri des individus, par ordre decroissant de fitness
    % puis on retranspose
    % finalement : premiere colonne contient le meilleur individu
    % donc les genes qui correspondent le mieux a la fitness
    
    % Update du meilleur et tracé si il a changé

    if population(P+1,1) > fbest % si la fitness du meilleur est mieux que fbest
        fbest = population(P+1,1); %meilleure fitness
        Abest = population(1:P,1); %genes du meilleur individu
        % on met a jour la fitness et les genes du meilleur individu
        


        % display : 
        % affiche : 
        % le numéro de la génération (i), la fitness maximale (f_max), 
        % et les gènes du meilleur individu (Genome).
        disp(strcat('Generation: ', num2str(i), ...
            '    f_max: ',      num2str(population(P+1,1),6), ...
            '    Genome: ',     mat2str(population(1:P,1),6) ))


%{
        % Plot du meilleur individu
        fplot(i) = fbest; % stock la meilleure fitness pour gene i dans fplot
        figure(2)
        loglog((1:i)*N,fplot(1:i),'k-'); % on trace figure 2 sur une echelle logarithmique
        xlim([1 K*N])
        xlabel('Number of evaluations')
        ylabel('Fitness')
        figure(1); hold on
        plot3(Abest(1),Abest(2),fbest,'ko')
%}
    end
    fplot(i) = fbest;% valeur actuelle sauvegardee pour la generation i
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % remplacement des mauvais individus
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % Selection : tournoi pour remplacer les N/2 moins bons
    % Croisement des deux individus gagnants pour echanger leurs genes
    Phold = population; % copie de la populationa ctuelle
    for j = ceil(N/2):N % sur les n/2 mauvais individus
        A1 = tournament(Phold,M); 
        A2 = tournament(Phold,M);
        
        % effectue un tournoi de taille M pour sélectionner deux parents. 
        % La fonction choisit des individus au hasard dans Aold et 
        % retourne celui qui a la meilleure fitness.
        % on prend les mauvais individus, et pour les modifier : 
        % on les remplace par des nouveaux individus generes par croisement, pour chaque individu a changer 
        % on effectue deux tournois, pour chaque tournoi on garde un des gagnants, 
        % ca nous donne deux parents et on mixe leurs genes pour 
        % obtenir les genes de celui qui rassemblera le mauvais gene

        population(:,j) = crossover(A1,A2,P); % on cree le nouvel individu
    end
    
    % Mutation pour tous sauf le meilleur
    for j = N:-1:2 % on commence du dernier jusqu au deuxieme individu
        jj = j-1; % on recuper l'individu precedent
        % puis on applique la mutation
        % et on en enregistre dans la colonne j de A
        % ligne p+1 de A non modifiee ici
        population(1:P,j) = mutation(population(1:P,jj),P,Pmut);
    end
end

% on affiche la figure 2
figure(2)
loglog((1:i)*N,fplot(1:i),'k-');
xlim([1 K*N])
xlabel('Number of evaluations')
ylabel('Fitness')

