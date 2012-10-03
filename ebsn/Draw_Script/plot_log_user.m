%% plot_log function: plot the distribution of y given x, value of asix and convert the X axis to be represented in log format

% name of raw data file
data_file = '/home/zhangwei/Code/Git/latent-factor-model/ebsn/Sta_Data/user_belong_group.sta';

% number of field for converting to log format
log_field = 1;

% name of output picture file
pic_file = './people_add_group';

% load data
points = load(data_file);

% calculate the summation of persons 
sum_person = sum(points(:, 2));

% create an x-axis semilog plot using the semilogx function
figure(1);
semilogx(points(:, 1), points(:, 2)/sum_person, 'color', 'r');

% set the axis limits
axis([min(points(:, 1)), max(points(:,1)), 0, max(points(:, 2))/sum_person]);

% add title and axis lables
%title('distribution of ')
xlabel('Number of group people added');
ylabel('Probability');

pause();

% save picture
print(1, '-djpeg', pic_file);

% close picture
close all;
