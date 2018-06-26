function [d, ProbeFromToCounts] = Substitute(language,d,ProbeInfo,r,ProbeFromToCounts)

[d, ProbeFromToCounts]=FindAndSub(language,d,1,ProbeInfo,r,ProbeFromToCounts);

%figure(36); DisplayTree(d,1);

if ProbeInfo.SameOrDiff==2 && ProbeInfo.Diff_GrammOrLexChange==1    % clean up for gramm changes  
    switch ProbeInfo.GrammSwitchType
        case 2      % pronouns sub number change
            if ProbeInfo.NPToGrammSwitch(1)
                d=ConjugateVerb(language,d,1);   % need to re-conjugate the verb to make the sentence grammatically correct    
            end
        case 3      % verb tense change      
            d=ConjugateVerb(language,d,1);
    end
end


if ProbeInfo.SameOrDiff==2 && ProbeInfo.Diff_GrammOrLexChange==2    % clean up for lex changes             
    switch ProbeInfo.LexChangeCat
        case {1}    %  in English, we only have to do this for the nouns...   
            %d=PrepareLabs_ByCase(d);
            d=AgreementNounAdjDet(language,d);
        case {2}
            d=ConjugateVerb(language,d,1);
    end
        
    d=PhonologicalCleanup(language,d);
end

if ProbeInfo.VerbEllipsis==1
    d=VerbEllipsis(language,d);
end