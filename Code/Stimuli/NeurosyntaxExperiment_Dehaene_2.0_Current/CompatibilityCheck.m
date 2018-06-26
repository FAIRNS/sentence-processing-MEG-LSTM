function [d,wordusecount]=CompatibilityCheck(d,wordusecount,r)

FeatureToCheck={'$HAPPY','$SAD'};

[~, nodes]=ListTerminals(d,1,{},{}); % note: this is still just the sentence's deep structure, so the "words" are the stem of the word    

FoundNoun=0;
FoundVerb=0;
for in=1:length(nodes)
    FeatVal=intersect( FeatureToCheck,d.labels{ nodes{in} } );
    if ~isempty(FeatVal)
        if ismember( '$EMOTION',d.labels{ nodes{in} } ) && ~ismember( '$LOCATIVE',d.labels{ nodes{in} } )   ; 
            if ~FoundNoun
                FoundNoun=1;    % this means we found a happy or sad noun    
                NounFeat=FeatVal;               
            else
                % this is case where an emotion word was used for both a subject and object fo a sentences
                % to handle this: choose the FeatVal for the subject NP
                
                % so only replace what we already have if this word is the subject of the sentence (though with the sentence structures we've chosen, this should never happen
                if ismember( '$NOMINATIVE',d.labels{ nodes{in} } )
                    NounFeat=FeatVal;
                end
            end
        else % if not a noun, this would have to be a verb   
            FoundVerb=1;
            vn=nodes{in};
            VerbFeat=FeatVal;
        end
    end
end
    
if (FoundNoun && FoundVerb) && ~strcmp(NounFeat,VerbFeat)
    % conflict detected! change the verb to match the noun, to create a more pragmatic sentence     
    % we can choose the Lexical Switch Targ, originally created for the probe sentences       
    
    nr=length(r);
    for ir=nr:-1:1
        if strcmp( r{ir}.subst{1},d.node{vn} ) && all( ismember(r{ir}.addi{1},d.labels{vn}) )      %  the last part of the statement is needed because presently appear shows up twice in the word list
            newr=r{ir}.LexSwitchTargs( randi(length(r{ir}.LexSwitchTargs)) );
            d.node{vn}=r{newr}.subst{1};
            d.terminalword{vn}=d.node{vn};
            d.labels{vn}=r{newr}.addi{1}';
            
            wordusecount(ir)=wordusecount(ir)-1;
            wordusecount(newr)=wordusecount(newr)+1;
            break
        end
    end
    
end