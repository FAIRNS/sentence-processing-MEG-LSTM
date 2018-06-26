%InitRemCounts.m
RemCounts=struct;

% These ocunts count down from the number of remaining uses, unlike the terminal word counts, which count up     

% the only input paramter that matters here is nsentences  

% set SentTypeCounts     
% 6 sent types, counting trans or intrans as a sent type
RemCounts.SentTypes=DistCounts(nsentences,6,SentTypeRates); %  DistCounts( TotNum,numTypes );  

RemCounts.TransAnim=DistCounts(nsentences/2,4);   % animacy of subj crossed w animacy of obj     
RemCounts.InTransAnimAndVerb=DistCounts(nsentences/2,4);   % animacy of subj only crossed w erg vs unaccus 
RemCounts.PPAnim=DistCounts( sum(RemCounts.SentTypes([1:2 4:6])),2 );

% bc unerg w inanim subject is impossible, later in the code we will merge the unerg and unaccus possibilities for inanimate subjects       

if isempty(TotRemCounts)
    TotRemCounts=RemCounts;
else
    fieldlist=fieldnames(TotRemCounts);
    for ifld=1:length(fieldlist)
        TotRemCounts.( fieldlist{ifld} )=TotRemCounts.( fieldlist{ifld} )+RemCounts.( fieldlist{ifld} );
    
        % coordinate to make sure remainder counts didn't go to the same options across blocks   
        [minCount,minCountInds]= min( TotRemCounts.( fieldlist{ifld} ) );
        while any(TotRemCounts.( fieldlist{ifld} )) > minCount+1
            OverInds= find( TotRemCounts.( fieldlist{ifld} ) > minCount+1 );
            ri=randi( length(OverInds) );
            TotRemCounts.( fieldlist{ifld} )( OverInds(ri) )=TotRemCounts.( fieldlist{ifld} )( OverInds(ri) ) -1;
            RemCounts.( fieldlist{ifld} )( OverInds(ri) )=RemCounts.( fieldlist{ifld} )( OverInds(ri) ) -1;

            % choose randomly from a minInd
            if isempty(minCountInds)
                [minCount,minCountInds]= min( TotRemCounts.( fieldlist{ifld} ) );
            end
            ToAddToInd=randi( length(minCountInds) );
            
            RemCounts.( fieldlist{ifld} )( ToAddToInd )=RemCounts.( fieldlist{ifld} )( ToAddToInd ) +1;
            TotRemCounts.( fieldlist{ifld} )( ToAddToInd )=TotRemCounts.( fieldlist{ifld} )( ToAddToInd ) +1;            
        end        
    end
end
    