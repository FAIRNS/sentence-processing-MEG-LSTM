function [SentInfo,Counts]=ChooseSingAndDef( Counts,SentInfo,iNP )

curVal=ChooseFromCounts( Counts.SingPlural(iNP,:) );
Counts.SingPlural(iNP,curVal)=Counts.SingPlural(iNP,curVal)+1;
SentInfo.NP_SingPlur(iNP)=curVal;

curVal=ChooseFromCounts( Counts.DefType(iNP,:) );
Counts.DefType(iNP,curVal)=Counts.DefType(iNP,curVal)+1;
SentInfo.NP_DefType(iNP)=curVal;
if curVal==3
    % choose this vs that for the demonstratives
    curVal=ChooseFromCounts( Counts.ThisVsThat(iNP,:) );
    Counts.ThisVsThat(iNP,curVal)=Counts.ThisVsThat(iNP,curVal)+1;
    SentInfo.NP_ThisOrThat(iNP)=curVal;
end