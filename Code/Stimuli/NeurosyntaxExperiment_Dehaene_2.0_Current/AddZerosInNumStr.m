function InCell=AddZerosInNumStr(InCell)

% adds one 0 in front of any single digit in a string    
nC=length(InCell);
for iC=1:nC    
    nConsecDigs=0;
    AddZeroLocs=[];
    for ix=1:length(InCell{iC})
        if isdigit(InCell{iC}(ix))
            nConsecDigs=nConsecDigs+1;
        else
            if nConsecDigs==1
               AddZeroLocs=[AddZeroLocs ix-1];               
            end
            nConsecDigs=0;
        end
    end
    if nConsecDigs==1
        AddZeroLocs=[AddZeroLocs length(InCell{iC})];
    end
    
    while ~isempty(AddZeroLocs)
        InCell{iC}=[InCell{iC}(1:AddZeroLocs(1)-1) '0' InCell{iC}(AddZeroLocs(1):end)];  
        if length(AddZeroLocs)>1
            AddZeroLocs=AddZeroLocs(2:end)+1;
        else
            AddZeroLocs=[];
        end
    end
end

