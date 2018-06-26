function OutCell=OrderFileNames(InCell)

OutCell=AddZerosInNumStr(InCell);
[~,sInds]=sort(OutCell);
OutCell=InCell(sInds);
    
