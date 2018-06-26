function [d,wordusecount]=RechoosePrep(d,wordusecount,SentInfo,curSentType,r,rmatchlist)

% get the preposition   
words=ListTerminals(d,1,{},{});
CheckPrep= intersect( {'at','in','on'},words ); %  {'at','in','on'} are the preps to be potentially replaced...   

SmallObjNoun=0;
if ~isempty(CheckPrep)        
    % avoid the use of "at" in certain situations where it sounds weird
    if ismember(curSentType,[4 6]) && strcmp( 'at',CheckPrep ) && SentInfo.InTransUnErg  % laughing at something changes the menaing of at...
        SwitchPrep=1;
        AvoidPreps={'at'};
    else
        SwitchPrep=0;
        
        % find where if the N_PO in the PP is a small object
        for in=length(d.node):-1:1
            if strcmp(d.node{in},'_N_P0') && ismember('$LOCATIVE',d.labels{in})            % find the locative _N_P0
                child=d.children{in}(1);
                if ismember( '$SMALL_NOUN',d.labels{child} )
                    AvoidPreps={'at','in','on'};
                    SwitchPrep=1;
                else % for large nouns,                         
                    if SentInfo.NP_SingPlur(3)==2 && SentInfo.NP_SingPlur(1)==1         % avoid in or on when the large noun in the pp is plural, and the subj is singular     
                        AvoidPreps={'in','on'};
                        if ismember( CheckPrep,AvoidPreps )
                            SwitchPrep=1;
                        end
                    else
                        % check to avoid car/truck in/on a car/tuck ... exception: car on a truck is OK
                        AvoidPreps={};
                        for iin=length(d.node):-1:1 % find teh nominatice _N_P0
                            if strcmp(d.node{iin},'_N_P0') && ismember('$NOMINATIVE',d.labels{iin})            % find the locative _N_P0
                                child2=d.children{iin}(1);
                                if ismember( '$LARGE_NOUN',d.labels{child2} )
                                    % add in the exception here that car on a truck is OK, else change the preposition   
                                    if strcmp(d.node{child},'truck') && strcmp(d.node{child2},'car')
                                        AvoidPreps={'in'};
                                    else
                                        AvoidPreps={'in','on'};
                                    end
                                    break
                                end
                            end                                
                        end
                        if ismember( CheckPrep,AvoidPreps )
                            SwitchPrep=1;
                        end
                    end
                end
                break                
            end
        end
        
        % if we passed the above two tests, check for specific combinations of verb and prep that don't work               
        if ~SwitchPrep && ismember(curSentType,[4 6])
            LoadVerbPrepMismatches
            
            for in=length(d.node):-1:1
                if length(d.node{in})>=5 && strcmp(d.node{in}(end-4:end),'_V_P0')     % find the verb    
                    child=d.children{in}(1);
                    [tf, Vind]= ismember( d.node{child},Verbs );
                    if tf
                        if ismember( CheckPrep,AvoidPreps_wVerb{Vind} )
                            SwitchPrep=1;
                            AvoidPreps=AvoidPreps_wVerb{Vind};
                        end                        
                    end
                    break
                end
            end
        end
    end
    
    
    if SwitchPrep
        MatchedrInds=find( strcmp('_P_P0',rmatchlist) );
        
        RemInds=[];
        for im=1:length( MatchedrInds )
            if strcmp( r{MatchedrInds(im)}.subst{1},CheckPrep )
                RepInd=MatchedrInds(im);
            end
                        
            if ismember( r{MatchedrInds(im)}.subst{1},AvoidPreps )
                RemInds=[RemInds im];
            end            
        end
        MatchedrInds(RemInds)=[];
        

        tmpchoice= ChooseFromCounts( wordusecount(MatchedrInds) );
        newr=MatchedrInds(tmpchoice);        
        
        for in=length(d.node):-1:1
            if strcmp(d.node{in},CheckPrep)
                d.node{in}= r{newr}.subst{1};
                d.terminalword{in}=d.node{in};
            end
        end
        
        %adjust wordusecount
        wordusecount(RepInd)=wordusecount(RepInd)-1;
        wordusecount(newr)=wordusecount(newr)+1;
    end   
end