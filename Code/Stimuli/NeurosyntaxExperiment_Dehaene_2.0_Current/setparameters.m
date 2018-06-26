%%%%% common to all sites
fontsizes=[24 36];


%%%%% set the parameters for each site

recordingsite = 4; 

% recordingsite = 1; % Stanford
% recordingsite = 2; % Paris
% recordingsite = 3; % MGH Boston
% recordingsite = 4; % New York
% recordingsite = 5; % Amsterdam


switch recordingsite        
    case 4 %% New York
        escapekey = 'esc';
        defaultlanguage = 1; %'English'
        TTLsending = 0;  %%% send TTL signals to parallel port 888
        Photodiode = true;
        fontscaling = 1; % this is a multiplier on font size. set to 1.5 or more to increase the size of letters on screen
        soa = 0.4; % stimulus onset asynchrony between successive words
        
        PlaceStr='NYU';        
end