function s=DeepToSurface(language,s)


%% mark agreement of subject and verb
s=CorrectVerb(s);

%% conjugate the verb adequately
s=ConjugateVerb(language,s,1);

%% prepare the additional terminal "labels" for a future analysis of activation induced by each word
%s=PrepareAnalysisLabels(s,1,{});

s=PrepareLabs_ByCase(s);

%% mark the plurals and genders correctly
s=AgreementNounAdjDet(language,s);

%% remove empty branches
s=RemoveEmpty(s,1);

%% move words if needed
s=MoveWords(language,s);

%% clean-up phonological particulars e.g. a-->an, etc
s=PhonologicalCleanup(language,s);


