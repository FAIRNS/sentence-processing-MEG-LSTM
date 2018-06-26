% InitCounts.m

% initialize the count arrays
wordusecount=zeros(nrules,1);
Counts.AnimEmotOrPhys=zeros(2,1);

Counts.AnimEmotList={};
Counts.AnimPhysList={};
Counts.InAnimPhysList={};  

for irule = 1:nrules      
    if strcmp( r{irule}.match,'_A_P0' )
        if ismember( '$EMOTION',r{irule}.addi{1} )
            Counts.AnimEmotList{end+1}=r{irule}.subst{1};
        elseif ismember( '$PHYSICAL',r{irule}.addi{1} )
            Counts.AnimPhysList{end+1}=r{irule}.subst{1};
            Counts.InAnimPhysList{end+1}=r{irule}.subst{1};
        end
    end
end 

Counts.AnimEmot=zeros( length(Counts.AnimEmotList),1 );
Counts.AnimPhys=zeros( length(Counts.AnimPhysList),1 );
Counts.InAnimPhys=zeros( length(Counts.InAnimPhysList),1 );
Counts.StayOrSwitch.EmotPhys=1;

Counts.AdjP_nWords=zeros(3,1);
Counts.AdvP_nWords=zeros(3,1);

% Determiner counts: number, sing/plural,        
Counts.NPPatterns111.SingPlural=zeros(8,1);
Counts.NPPatterns110.SingPlural=zeros(4,1);
Counts.NPPatterns101.SingPlural=zeros(4,1);

% Counts.NPPatterns111.NumOrNoNum=zeros(8,1);
% Counts.NPPatterns110.NumOrNoNum=zeros(4,1);
% Counts.NPPatterns101.NumOrNoNum=zeros(4,1);
Counts.NumOrNoNum=zeros(2,2);

Counts.NPPatterns111.DefType=zeros(27,1);
Counts.NPPatterns110.DefType=zeros(9,1);
Counts.NPPatterns101.DefType=zeros(9,1);
Counts.ThisVsThat=zeros(3,2);

% create cell-array lists for Det Feature Labels      
Counts.NP_SingPlur_List={'$SINGULAR','$PLURAL'};
Counts.NP_DefType_List={'$INDEFINITE','$DEFINITE','$DEMONSTRATIVE'};
Counts.NP_ThisOrThat_List={'$CLOSE_TO_SPEAKER','$FAR_FROM_SPEAKER'};

DefCaseList
Counts.CaseList=CaseList;


% for Probe
[Counts.Probe.SameOrDiff, Counts.Probe.Same_AllPronouns, Counts.Probe.Diff_GrammOrLexChange, Counts.Probe.Diff_NumTenseChange ...
    Counts.Probe.Diff_NPKept ] =deal( zeros(1,2) );

Counts.Probe.NPToKeep111=zeros(1,3);
Counts.Probe.NPToKeep110=zeros(1,2);
Counts.Probe.NPToKeep101=zeros(1,2);

[Counts.Probe.Diff_GenNumTenseChange] =deal( zeros(1,3) );     % gender or number or verb tense mismatches             

%  no pronouns in the pps...  
[Counts.Probe.NPGenSwitch11, Counts.Probe.NPNumSwitch11]= deal( zeros(1,2) );

DefContentCatList
if ProbeElideAdv
    ContentCatList( strcmp(ContentCatList,'_ADV_P0') )=[];
end
Counts.Probe.ContentCatList=ContentCatList;     
Counts.Probe.LexChange_PerCat=zeros( length(ContentCatList),1 );  
[Counts.Probe.LexChange_NperNP, Counts.Probe.LexChange_AperNP]=deal( zeros(3,1) );  


% counts for the specifc items being switched when switches can occur...   
ProbeFromToCounts.Tense=zeros(4,4); 
ProbeFromToCounts.Tense( VerbTenseSwitchesToAvoid==1 )=99;  % make the counts artificially high so these are never chosen...   
if AllowAnimacySwitch
    ProbeFromToCounts.Gender=zeros(3,3);
end

Counts.Probe.VerbEllipses=zeros(1,2);

