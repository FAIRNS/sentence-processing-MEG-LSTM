% setdelays_NYU.m      

soa = 0.5; % stimulus onset asynchrony between successive words
inttrial= 0.8; % duration w fix point off after a response    
fixwait= 0.6;   % duration w fix point on before the trial starts 

PD_Dur=.050;  %secs;   

% note that half of the soa is added to the true delay because of the word offset time... 
DelayDurs=[0.5 1.75 1.75];    % per BlockType   
