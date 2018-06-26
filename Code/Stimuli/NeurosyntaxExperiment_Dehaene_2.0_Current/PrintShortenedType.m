function PrintShortenedType(Probe)

if Probe.SameOrDiff==1
    str='Same';
else
    str='Diff';
    if Probe.Diff_GrammOrLexChange==1
        switch Probe.GrammSwitchType
            case 1;     str=[str ' Gender Switch'];
            case 2;     str=[str ' Number Switch'];
            case 3;     str=[str ' Tense Switch'];
        end
    else
        str=[str ' Lexical Change'];
        switch Probe.LexChangeCat
            case 1;     str=[str ' Noun'];
            case 2;     str=[str ' Verb'];
            case 3;     str=[str ' Adjective'];
            case 4;     str=[str ' Adverb'];
        end
    end
end
disp(str);