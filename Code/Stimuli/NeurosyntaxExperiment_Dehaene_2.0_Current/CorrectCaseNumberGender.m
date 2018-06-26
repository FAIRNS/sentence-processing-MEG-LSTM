function d=CorrectCaseNumberGender(d)

possiblelabels = {'$SINGULAR','$PLURAL','$MASC','$FEMI','$NOMINATIVE','$ACCUSATIVE','$LOCATIVE'};

blocknodes = {'_P_P2','_N_COMP'};

for i=FindInChildren(d,1,[],'_N_P2') %% find all NPs
    labels = CollectFromChildren(d,i,{},blocknodes);

    if ismember('$UNSPECIFIED',labels)
        labels = union(labels,possiblelabels(unidrnd(2)));
    end
    labels = intersect(labels,possiblelabels);
    
    d=ApplyToChildren(d,i,labels,blocknodes);
end

