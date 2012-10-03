%% This script draw plot-plot picture

M = load('../Sta_Data/dis_prob.txt');

figure;

loglog(M(:,1), M(:,2), 'color', 'r', 'linewidth', 2);

