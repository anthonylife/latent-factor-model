function plot_group_user_event_dis(isSpecified)
% This Script plot the location distribution of the events each group holds and of the people each group has.
% 
% Function: Now, plot the group one by one. Future, specify the group id and plot.
%
% Input:
%   isSpecified: a mark about whether to plot one by one or accroding to the specified group id. (0: one by one, 1: specified)
%
%

% The file location of the users' location information and events' location
event_location_file = '../Meetup_geo/event_lon_lat.csv';
user_location_file = '../Meetup_geo/user_lon_lat.csv';
group_event_file = '../Sta_Data/group_has_event.csv';

if (~exist('isSpecified', 'var'))
    isSpecified = 0;
end

% Load location information of events and users
disp('Loading information data started!');
event_location = load(event_location_file);
user_location = load(user_location_file);
group_event = load(group_event_file);
disp('Loading information data finished!');

% The file: information about group having users and group having events
group_user_file = '../Sta_Data/group_has_user.dat';

% Read the group user information and group event information from files line by line
cache_group = 0;    % Cache the previous group id 
users = [];  % Users in current group
group_event_location = [];  % Events' location list of current group
group_user_location = [];   % Users' location list of current group

fid_gu = fopen(group_user_file, 'r');
while ~feof(fid_gu)
    line_gu = fgetl(fid_gu);    % Read the first group in both file
    line_gu
    if ~isempty(line_gu)
        [user, group_u] = strread(line_gu, '%d%d', 'delimiter', ',');
        if group_u ~= cache_group
            if cache_group ~= 0
                event = group_event(find(group_event(:, 2) == cache_group), 1);     %(Note: erratum the index of the event)
                %event
                %pause;
                % Get all the related events' location
                index = 1;
                for i=1:length(event)
                    event_location_idx = find(event_location(:, 1) == event(i));
                    if ~isempty(event_location_idx)
                        %event_location_idx
                        %event_location(event_location_idx, :)
                        %event_location(event_location_idx, 1)
                        %event_location(event_location_idx, 2)
                        %event_location(event_location_idx, 3)
                        %disp('pause');
                        %pause;
                        if event_location(event_location_idx, 2) ~= 0 || event_location(event_location_idx, 3) ~= 0
                            group_event_location(index, 1) = event_location(event_location_idx, 2);
                            group_event_location(index, 2) = event_location(event_location_idx, 3);
                            index = index + 1;
                        end
                    end
                end
                % Get all the users' location
                for i=1:length(users)
                    user_location_idx = find(user_location(:,1) == users(i));
                    if ~isempty(user_location_idx)
                        group_user_location(i, 1:2) = user_location(user_location_idx, 2:3);
                    end
                end
                % Plot the distribution
                %disp('event location');
                %group_event_location
                %disp('plot');
                %pause;
                figure(1);
                if ~isempty(group_user_location) && ~isempty(group_event_location)
                    min([group_user_location(:,1); group_event_location(:,1)])
                    max([group_user_location(:,1); group_event_location(:,1)])
                    min([group_user_location(:,2); group_event_location(:,2)])
                    max([group_user_location(:,2); group_event_location(:,2)])
                    plot(group_user_location(:, 1), group_user_location(:, 2), 'b^'); 
                    hold on;
                    plot(group_event_location(:, 1), group_event_location(:, 2), 'ro');  % plot event
                    axis([min([group_user_location(:,1); group_event_location(:,1)]), max([group_user_location(:,1); group_event_location(:,1)]), min([group_user_location(:,2); group_event_location(:,2)]), max([group_user_location(:,2); group_event_location(:,2)])]);
                    pause;
                    hold off;
                elseif ~isempty(group_user_location) && isempty(group_event_location)
                    %min(group_user_location(:,1))
                    %max(group_user_location(:,1))
                    %min(group_user_location(:,2))
                    %max(group_user_location(:,2))
                    %plot(group_user_location(:, 1), group_user_location(:, 2), 'b^');   % plot user
                    %axis([min(group_user_location(:,1)), max(group_user_location(:,1)), min(group_user_location(:,2)), max(group_user_location(:,2))]);
                elseif isempty(group_user_location) && ~isempty(group_event_location)
                    %min(group_event_location(:,1))
                    %max(group_event_location(:,1))
                    %min(group_event_location(:,2))
                    %max(group_event_location(:,2))
                    %plot(group_event_location(:, 1), group_event_location(:, 2), 'ro');  % plot event
                    %axis([min(group_event_location(:,1)), max(group_event_location(:,1)), min(group_event_location(:,2)), max(group_event_location(:,2))]);
                end
            end
            users = user; % Clear the users in previous group and store the user in the current group
            group_user_location = [];
            group_event_location = [];
            cache_group = group_u;
        else
            users = [users, user];
        end
    end
end

fclose(fid_gu);
