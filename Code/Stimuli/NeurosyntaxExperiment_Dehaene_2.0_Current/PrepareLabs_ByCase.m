function s=PrepareLabs_ByCase(s)

caseswitches=1; %first node
while ~isempty(caseswitches)        
    [labs,newcaseswitches]=CollectFromChildren_OfSameCase(s,caseswitches(1));            
    s=ApplyToChildren_OfSameCase(s,caseswitches(1),labs);
   
    caseswitches=[caseswitches(2:end) newcaseswitches];
end

