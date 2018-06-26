% setdelays_NYU.m      

soa = 0.3; % stimulus onset asynchrony between successive words
inttrial= 0.3; % duration w fix point off after a response    
fixwait= 0.3;   % duration w fix point on before the trial starts 

PD_Dur=.033;  %secs;   

% note that half of the soa is added to the true delay because of the word offset time... 
DelayDurs=[0.4 0.4 0.4];    % per BlockType   
