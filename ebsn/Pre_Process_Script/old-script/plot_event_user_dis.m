% The script plot the location distribution of users joining each event

% Specify the file address
user_location_file = '../Meetup_geo/user_lon_lat.csv';
event_location_file = '../Meetup_geo/event_lon_lat.csv';
user_event_file = '../Sta_Data/event_has_user.csv';

% Load user and event location information
disp('Start loading information!');
event_location = load(event_location_file);
user_location = load(user_location_file);
disp('Loading information finished!');

fid = fopen(user_event_file, 'r');

% Process data line by line
cache_event = 0;
users = [];  % Users in current group
temp_event_location = [];  % Events' location list of current group
temp_user_location = [];   % Users' location list of current group

while ~feof(fid)
    line = fgetl(fid);
    if ~isempty(line)
        [user_id, event_id] = strread(line, '%d%d', 'delimiter', ',');
        if event_id ~= cache_event
            if cache_event ~= 0
                cache_event
                disp('users');
                users
                temp_event_location = event_location(find(event_location(:,1) == cache_event), 2:3);
                temp_event_location
                pause;
                if ~isempty(temp_event_location)
                    % Get the users location
                    index = 1;
                    length(users)
                    pause;
                    for i=1:length(users)
                        user_location_idx = find(user_location(:,1) == users(i));
                        if ~isempty(user_location_idx)
                            temp_user_location(index, 1:2) = user_location(user_location_idx, 2:3);
                            index = index + 1;
                        end
                    end
                    cache_event
                    users
                    temp_user_location
                    pause;
                    % Plot distribution
                    if ~isempty(temp_user_location)
                        figure(1);
                        plot(temp_event_location(1), temp_event_location(2), 'ro', 'LineWidth', 3, 'MarkerSize', 12);
                        hold on;
                        plot(temp_user_location(:,1), temp_user_location(:,2), 'b^', 'LineWidth', 2, 'MarkerSize', 7);
                        axis([min([temp_user_location(:,1); temp_event_location(1)]), max([temp_user_location(:,1); temp_event_location(1)]), min([temp_user_location(:,2); temp_event_location(2)]), max([temp_user_location(:,2); temp_event_location(2)])]);
                        hold off;
                        pause;
                    end
                end
            end
            users = user_id;
            cache_event = event_id;
            temp_user_location = [];
            temp_event_location = [];
        else
            users = [users, user_id];
        end
    end
end

fclose(fid);
