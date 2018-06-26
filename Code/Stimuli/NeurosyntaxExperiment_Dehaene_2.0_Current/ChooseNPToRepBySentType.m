%ChooseNPToRepBySentType.m

switch curSentType
    case 1
        if MustKeepObjOrSubj
            curType=ChooseFromCounts( Counts.Probe.NPToKeep110 );
            Counts.Probe.NPToKeep110( curType )=Counts.Probe.NPToKeep110( curType )+1;
        else
            curType=ChooseFromCounts( Counts.Probe.NPToKeep111 );
            Counts.Probe.NPToKeep111( curType )=Counts.Probe.NPToKeep111( curType )+1;
        end
        SentInfo(isent).Probe.NPToKeep=curType;     %1 for Subj, 2 for Obj, 3 for PP
    case {2,3}  % keeping only the NP in the PP is not possible here
        curType=ChooseFromCounts( Counts.Probe.NPToKeep110 );
        Counts.Probe.NPToKeep110( curType )=Counts.Probe.NPToKeep110( curType )+1;
        SentInfo(isent).Probe.NPToKeep=curType;     %1 for Subj, 2 for Obj, 3 for PP
    case {4,6}  % keeping only the NP in the PP is possible, but not for the Obj (the verbs are intransitive)
        curType=ChooseFromCounts( Counts.Probe.NPToKeep101 );
        Counts.Probe.NPToKeep101( curType )=Counts.Probe.NPToKeep101( curType )+1;
        if curType==1
            SentInfo(isent).Probe.NPToKeep=curType;     %1 for Subj, 2 for Obj, 3 for PP
        elseif curType==2
            SentInfo(isent).Probe.NPToKeep=3;     % 1 for Subj, 2 for Obj, 3 for PP
        end
    case 5
        SentInfo(isent).Probe.NPToKeep=1;   % must be the subj here
end

SentInfo(isent).Probe.NPToRep( SentInfo(isent).Probe.NPToKeep )=0;
