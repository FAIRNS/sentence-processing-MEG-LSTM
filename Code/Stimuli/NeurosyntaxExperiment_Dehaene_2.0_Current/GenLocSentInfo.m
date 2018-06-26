%%%%%%%%%%%%%%%%%% User Inputs  

PPVsObjNPRate=.5;   % higher = more PPs   


%         1= PP 2= Obj 3 = 
CostsToAdd=[3 2 1][


%%%%%%%%%%%%%%%%%% End of User Inputs    

MinNWords=3;    % bare min for a sentence in this paradigm  

nwords=Loc.SentLens;
nExtraWords=Loc.SentLens(isent)-MinNWords;   % given num words, determine how many extra words


while nExtraWords
    if nExtraWords>=4
        % choose an Obj NP or a PP   
        
    
    




