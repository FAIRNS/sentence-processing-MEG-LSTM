%global language;

switch language
    case 1 % English
        LoadRules_English_NonContent;
        if JabberFlag
            JabberwockyWords_English;
        else
            ContentWords_English;
        end
    case 2 % French
        %LoadRules_French;
        LoadRules_French_NonContent;
        if JabberFlag
            JabberwockyWords_English;
        else
            ContentWords_French;
        end
    case 3 % Dutch
        LoadRules_Dutch;
    case 4 % Spanish
        LoadRules_Spanish;
end

