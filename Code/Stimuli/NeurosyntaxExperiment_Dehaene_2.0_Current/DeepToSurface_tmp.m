function s=DeepToSurface(s);

s=CorrectCaseNumberGender(s);

%% mark agreement of subject and verb
s=CorrectVerb(s);

%% conjugate the verb adequately
%s=ConjugateVerb(s,1);

%% mark the plurals and genders correctly
s=AgreementNounAdjDet(s);

%% remove empty branches
s=RemoveEmpty(s,1);

%% move words if needed
s=MoveWords(s);

%% clean-up phonological particulars e.g. a-->an, etc
s=PhonologicalCleanup(s);

%% prepare the additional terminal "labels" for a future analysis of activation induced by each word
%s=PrepareAnalysisLabels(s,1,{});

