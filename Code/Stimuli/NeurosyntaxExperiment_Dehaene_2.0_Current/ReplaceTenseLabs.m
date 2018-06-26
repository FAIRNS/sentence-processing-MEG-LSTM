function d=ReplaceTenseLabs( d,i,curTense )

DefTenseList

[~,labind] =intersect( d.labels{i},TenseList );
if ~isempty(labind)                
    d.labels{i}{labind}=curTense;
   
    for inode=1:d.nchildren{i}
        d=ReplaceTenseLabs(d,d.children{i}(inode),curTense);
    end 
end

