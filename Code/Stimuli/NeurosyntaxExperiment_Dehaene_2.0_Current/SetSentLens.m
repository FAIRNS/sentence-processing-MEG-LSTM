%SetSentLens.m   

nSentLens=diff(SentLenLims)+1;
nSentPerType=floor(nsentences/nSentLens);
nRem=nsentences-nSentLens*nSentPerType;

SentLens=zeros(nsentences,1);
for iSL=1:nSentLens
    SentLens( nSentPerType*(iSL-1)+1:nSentPerType*iSL )=SentLenLims(1)+iSL-1;
end
LeftOverCounts=zeros( nSentLens,1 );
for iRem=1:nRem
    curType=ChooseFromCounts( LeftOverCounts );
    LeftOverCounts( curType )=LeftOverCounts( curType )+1;
    
    SentLens(end-(iRem-1))=curType+ SentLenLims(1) -1;
end
SentLens=SentLens( randperm(nsentences) );