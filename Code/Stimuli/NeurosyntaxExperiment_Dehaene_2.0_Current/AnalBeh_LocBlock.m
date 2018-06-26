% AnalBeh_LocBlock.m

% ensure response is a column vector
[r,c]=size(response);   
if c>r;     response=response';     end

SameResp=strcmp( response,SameKey );
DiffResp=strcmp( response,DiffKey );

CorrectSame= samestruct & SameResp;
InCorrectSame= samestruct & ~SameResp;
CorrectDiff= ~samestruct & DiffResp;
InCorrectDiff= ~samestruct & ~DiffResp;

nCorrSame{iLoc}=sum(CorrectSame);
nInCorrSame{iLoc}=sum(InCorrectSame);
nCorrDiff{iLoc}=sum(CorrectDiff);
nInCorrDiff{iLoc}=sum(InCorrectDiff);

PctTotCor{iLoc}=(nCorrSame{iLoc}+nCorrDiff{iLoc}) / (nInCorrSame{iLoc} + nInCorrDiff{iLoc} + nCorrSame{iLoc}+nCorrDiff{iLoc}) *100;

RTs{iLoc}=cell2num(RT);
SameTrRT{iLoc}=mean( RTs{iLoc}(samestruct==1) );
DiffTrRT{iLoc}=mean( RTs{iLoc}(samestruct==0) );
TotRT{iLoc}=mean( RTs{iLoc} );
