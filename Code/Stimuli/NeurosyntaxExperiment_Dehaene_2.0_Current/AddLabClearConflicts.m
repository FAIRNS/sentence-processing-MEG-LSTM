function Labs=AddLabClearConflicts( Labs,NewLabs )
%Adds New labels while clearing up existing conflicts   

LoadLabConflicts;
ncon=length(LabConflicts);

Labs=union(Labs,NewLabs);

for icon=1:ncon
    if length(intersect( Labs,LabConflicts{icon} ))>1
        % conflict detected
        % find out which came from the NewLab and keep only that one

        [~, inds] = intersect( Labs,LabConflicts{icon} );
        ninds=length(inds);
        RemList=[];
        for ii=1:ninds        
            if ~ismember( Labs{inds(ii)},NewLabs )
                RemList(end+1)=ii;
            end
        end
        
        Labs(inds( RemList ))=[];   
    end
end
        