function [d, ProbeFromToCounts]=FindAndSub(language,d,inode,ProbeInfo,r,ProbeFromToCounts)
%%% search for a node matching the variable nodetype, and whose labels
%%% match the variable nodelabels
%%% substitute it, creating a new node on the fly
%%% Return the new structure and the substituted node
DefCaseList
KeepSearching=0;

% check if current node matches a case label
FoundCase=intersect(d.labels{inode},CaseList);
if ~isempty(FoundCase)
    % determine what to do    
    curCase=find( strcmp(FoundCase,CaseList) );
    
    if ProbeInfo.NPToRep(curCase)
        if ProbeInfo.NPToGrammSwitch(curCase)
            SwitchInfo.Switch=1;
            SwitchInfo.GrammOrLex= ProbeInfo.Diff_GrammOrLexChange;
            SwitchInfo.GrammSwitchType= ProbeInfo.GrammSwitchType;            
        else
            SwitchInfo.Switch=0;
        end
            
        [d, ProbeFromToCounts]=SubsNode(language,d,inode,'_PRONOUN_SUB',curCase,SwitchInfo,[],ProbeFromToCounts);
    else                               
        if ProbeInfo.SameOrDiff ==2 && ProbeInfo.Diff_GrammOrLexChange==2 && ismember( ProbeInfo.LexChangeCat,([1 3]) ) && ProbeInfo.NPToLexChange==curCase    % if we're searching to change a Noun or an Adj in this NP       
            DefContentCatList
            if strcmp( ContentCatList{ ProbeInfo.LexChangeCat }, d.node{inode}  )
                %SwitchInfo.Switch=1;
                %SwitchInfo.GrammOrLex= ProbeInfo.Diff_GrammOrLexChange;
            
                [d, ProbeFromToCounts]=SubsNode(language,d,inode,'Lex_Switch',curCase,[],r,ProbeFromToCounts);
            else
                KeepSearching=1;
            end
        else
            KeepSearching=1;  % keep this NP as it is... so do nothing and end this branch of searching           
        end
    end    
elseif ProbeInfo.ElideAdv && strcmp( d.node{inode},'_ADV_P2' )  
    d=SubsNode(language,d,inode,'_Elided'); 
elseif strcmp( d.node{inode},'very' ) % needed to avoid a weird matlab bug           
    return
elseif strcmp( d.node{inode},'_T_P0' ) && ProbeInfo.SameOrDiff ==2 && ProbeInfo.Diff_GrammOrLexChange==1 && ProbeInfo.GrammSwitchType==3
    
    % change the verb conjugation        
    [d, ProbeFromToCounts]=SubsNode(language,d,inode,'_T_P0',[],[],[],ProbeFromToCounts);
    
    % change the terminal word of the verb back to infinitive form
    % find the verb
    curParents=FindParents(d,inode);  % note we need to search in this node's immediate Parent
    b=FindInChildren(d, curParents(1), [],'_V_P0');      
    b=d.children{b(1)}(1); 
    d.terminalword{ b }=d.node{ b }; % node stores the infinitive, so we rewrite that to the terminalword   
    
    % ConjugateVerb.m for the new tense will be called inside Substitute.m 
elseif ProbeInfo.SameOrDiff ==2 && ProbeInfo.Diff_GrammOrLexChange==2 && ( (ismember( ProbeInfo.LexChangeCat,([2]) ) && strcmp( d.node{inode}(end-4:end),'_V_P0' )) || (ismember( ProbeInfo.LexChangeCat,([4]) ) && strcmp( d.node{inode},'_ADV_P0' )) )     
    % for both Verb Lex Switch and Adv Lex Switch this will work      
    [d, ProbeFromToCounts]=SubsNode(language,d,inode,'Lex_Switch',[],[],r,ProbeFromToCounts);           
else
    % launch a search through all children   
    % we need a while loop not a for loop because the value of the numbers of children for each node can dynamically change when a substitution occurs   
    
    KeepSearching=1;
end
    
if KeepSearching
    ich=1;
    while ich<=d.nchildren{inode}
        [d, ProbeFromToCounts]=FindAndSub(language,d,d.children{inode}(ich),ProbeInfo,r,ProbeFromToCounts);        % keep searching
        ich=ich+1;
    end
end