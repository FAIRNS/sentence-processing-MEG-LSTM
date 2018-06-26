function d=ApplyToChildren_tmp(d,i,addlabel,curcase)
%%% add the label 


%let case block label propagation    

%%%% apply it to all children
if ~ismember(d.node{i},blocknodes)  %%% these nodes block number propagation
    for inode=1:d.nchildren{i}
        [d,addlabel] =ApplyToChildren(d,d.children{i}(inode),addlabel,blocknodes);
    end    
    
    %%% apply it
    d.labels{i} = union(d.labels{i},addlabel);
end




