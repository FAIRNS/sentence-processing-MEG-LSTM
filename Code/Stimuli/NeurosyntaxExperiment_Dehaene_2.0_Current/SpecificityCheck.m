function [d,wordusecount]=SpecificityCheck(d,wordusecount)

DefSpecNouns
Locn=[];    % not all sents have a locative, so initialize this to empty to be sure it exists   

nodes=FindInChildren(d,1,[],'_N_P0');
for in=1:length(nodes)
    if ismember( '$NOMINATIVE',d.labels{ nodes(in) } )
        Nomn=d.children{ nodes(in) };        
        NomSpec=ismember( d.node{Nomn},SpecNouns );
    elseif ismember( '$LOCATIVE',d.labels{ nodes(in) } )
        Locn=d.children{ nodes(in) };        
        LocSpec=ismember( d.node{Locn},SpecNouns );        
    end
end
    
if ~isempty(Locn) && LocSpec && ~NomSpec
    % Loc is more specific than subject! To improve pragmatics, swap the 2 nouns    
    NewNomNode=d.node{Locn};
    NewNomlabels=d.labels{Locn}(end-1:end); % the last 2 labs will be the ones specific to this word...    
    
    d.node{Locn}=d.node{Nomn};
    d.labels{Locn}(end-1:end)=d.labels{Nomn}(end-1:end);
    d.terminalword{Locn}=d.node{Locn};
    
    d.node{Nomn}=NewNomNode;
    d.labels{Nomn}(end-1:end)=NewNomlabels;
    d.terminalword{Nomn}=NewNomNode;
end
    