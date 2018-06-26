function d=ApplyToChildren_OfSameCase(d,i,addlabel,curcaselab)
%%% add the label 

DefCaseList     %sets the pre-dfined variable CaseList 
if nargin<4
    curcaselab=intersect(CaseList,d.labels{i});
end
tmpcaselab=intersect(CaseList,d.labels{i});

%%%% apply it to all children
if isequal( curcaselab,tmpcaselab )  % statement to decide blocking of propagation...n
    for inode=1:d.nchildren{i}
        d=ApplyToChildren_OfSameCase(d,d.children{i}(inode),addlabel,curcaselab);
    end    
    
    %%% apply it
    d.labels{i} = union(d.labels{i},addlabel);
end



