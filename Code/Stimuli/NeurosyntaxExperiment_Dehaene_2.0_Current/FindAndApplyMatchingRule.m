% FindAndApplyMatchingRule

FoundCompliment=0;

% recalc MatchedrInds as before
MatchedrInds=find( strcmp(s.node{inode},rmatchlist));
MatchedrInds( MatchedrInds==selrule )=[];
for im=1:length(MatchedrInds)    
    if isequal(r{MatchedrInds(im)}.addi, r{selrule}.addi)    % this tests that each cell of the addi array is identical   
        selrule_old=selrule;
        selrule=MatchedrInds(im);
        s.node{totnode} = r{selrule}.subst{ichild};     % but ichild will always be 1 here for rules ending in a terminal word  
        s.terminalword{totnode} = stripunderscore(s.node{totnode});
        
        FoundCompliment=1;
        break
    end
end


% deal with the potential case with 3 NPs where even this new word has already appeared in the sentence previously     
if FoundCompliment && sum(strcmp( s.terminalword{totnode},s.terminalword )) >1    %Note that if FoundCompliment==0, then only one matching word exists (For example, the word 'one'). Our strategy at the present is to just let this word appear twice if it comes up  
    % do as above, but here we'll go with a random choice of the other options that closest match the original word to be replaced
    
    MatchedrInds=find( strcmp(s.node{inode},rmatchlist));
    MatchedrInds( ismember( MatchedrInds,[selrule selrule_old] ) )=[];
    numequal=length(MatchedrInds);
    for im=1:length(MatchedrInds)
        numequal(im)=sum( ismember( r{selrule_old}.addi{1},r{MatchedrInds(im)}.addi{1} ) );
    end
    
    MatchedrInds=MatchedrInds( numequal==max(numequal) ); 
    im=ChooseFromCounts( wordusecount( MatchedrInds ) );
    
    selrule=MatchedrInds(im);
    s.node{totnode} = r{selrule}.subst{ichild};     % but ichild will always be 1 here for rules ending in a terminal word
    s.terminalword{totnode} = stripunderscore(s.node{totnode});
end