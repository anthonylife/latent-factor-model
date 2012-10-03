function ret = plotUserDis(people_loc)
% This function put user points accroding to their longitude and latitude
% Input:
%      people_loc: m*2 matrix.
%                  m stands for number of people in the group
%                  2 longitude and latitude
% Output:
%      To be specified

% file name of the output picture
%pic_file = './'

% number of people
m = length(people_loc);

% maximum and mimum of longitude and latitude
max_lon_lat = max(people_loc);
min_lon_lat = min(people_loc);

% plot
figure(1);
plot(people_loc(:, 2), people_loc(:, 1), 'b');

% pause
pause;
close all;
%print(1, '-djpeg', )
