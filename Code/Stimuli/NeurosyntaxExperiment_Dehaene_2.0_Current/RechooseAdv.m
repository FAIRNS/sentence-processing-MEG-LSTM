function [d,wordusecount]=RechooseAdv(d,wordusecount,r,rmatchlist,language)

words=ListTerminals(d,1,{},{}); % note: this is still just the sentence's deep structure, so the "words" are the stem of the word    
switch language
    case 1
        curAdv='slowly';
    case 2
        curAdv='lentement';
end
if ismember( curAdv,words )
    LoadSlowIncompatibleVerbs
    
    if ~isempty( intersect( AvoidVerbs,words ) )
        % then swap out the adverb    
        
        MatchedrInds=find( strcmp('_ADV_P0',rmatchlist) );
                
        RemInds=[];
        for im=1:length( MatchedrInds )
            if strcmp( r{MatchedrInds(im)}.subst{1},curAdv )
                RepInd=MatchedrInds(im);
                RemInds=[RemInds im];
            end          
        end
        MatchedrInds(RemInds)=[];
        

        tmpchoice= ChooseFromCounts( wordusecount(MatchedrInds) );
        newr=MatchedrInds(tmpchoice);        
        
        for in=length(d.node):-1:1
            if strcmp(d.node{in},curAdv)
                d.node{in}= r{newr}.subst{1};
                d.terminalword{in}=d.node{in};
                
                % change label from $SLOW to $FAST     
                % find $SLOW label      
                SlowLab=find(strcmp( d.labels{in},'$SLOW' ));
                d.labels{in}{SlowLab}='$FAST';                                
            end
        end
        
        %adjust wordusecount
        wordusecount(RepInd)=wordusecount(RepInd)-1;
        wordusecount(newr)=wordusecount(newr)+1;        
    end            
end
    