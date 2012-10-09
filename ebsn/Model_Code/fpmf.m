% Feature-based Probabilistic Matrix Factorization for event-based group recommendation
%  
% Idea of model: probabilistic matrix factorization + linear discriminative model.
%        Tricks: 1.enhanced latent factor; 2.distance-based features; 3.social regularization
%         Train: Load features from hard disk. Use BRP framework to learning pairwise preference
%       Learning algorithm: Stochastic gradient descent algorithm
%
% Main procedures of program:
%             1. Hyperparamter and other global variabls setting (Note: It may need to do grid search.)
%             2. Model paramter allocation and random initialization
%             3. Loading heterogeneous relation information and store them in hash table (Note: save loading time)
%             4. Model paramter learning (enter in loops):
%                4.1 Compute MAP for training data based on the current paramters
%                4.2 BPR learing framework, loops over training data based on stochastic order(pseudo-random).
%                    4.2.1 Compute gradients
%                    4.2.2 Update latent variable and explicit feature paramters
%                4.3 Convergence judgement((1)maximum loops; (2)MAP differentials; (3)parameter differentials)
%             5. Compute MAP on test data
%
% Note: grid search should be added later.
%
% @author: anthonylife
% @date: 10/9/2012


% Global variable and hyper-parameter setting
% ===========================================

epsilon = 0.01;     % Learning rate(0.001, 0.0001 or decay by the loops)
lambda_e = 0.01;    % Regularization paramter for explicit feature parameters
lambda_l = 0.01;    % Regularization paramter for latent variables

maxepoch = 100;     % Maximum number of loops

num_u = 8273;       % Number of users
num_g = 3236;       % Number of groups
num_t = 1001;       % Number of tags
num_dimen = 40;     % Number of latent variables' dimensions(usually 10-200, )
