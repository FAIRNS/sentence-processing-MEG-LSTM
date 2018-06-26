function [d,inode]=PrepareLabs_Matt(d,inode,currentlabels,caselab)

CaseList={'$NOMINATIVE'  '$ACCUSATIVE'  '$LOCATIVE'};

tmpcaselab=intersect(CaseList,d.labels{inode});
if ~isempty(tmpcaselab)
    if ~strcmp( caselab,tmpcaselab ) 
        % foud a new case, start over with the currentlabels          
        currentlabels=unique( d.labels{inode} );
        caselab = tmpcaselab;
    else
        %accrue the current labels
        currentlabels=intersect( currentlabels,d.labels{inode} );         
    end
end
        
% recursively search children    
for ich=1:d.nchildren{inode}
    [d,inode]=PrepareLabs_Matt(d,inode,currentlabels,caselab)
end
