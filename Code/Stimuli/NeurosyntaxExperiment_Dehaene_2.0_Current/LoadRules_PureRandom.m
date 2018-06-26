% LoadRules_PureRandom.m
%
% MJN 150202: This version will create purely random, top-down generated
% stimuli wihtout yoking verbs and nouns based on animacy. Howevre, that's
% not what we want to do with the Neurosyntax 2.0 stimuli, and so will use
% a different version

global language;

switch language
    case 1 % English
    LoadRules_English_PureRandom;
    case 2 % French
    LoadRules_French;
    case 3 % Dutch
    LoadRules_Dutch;
    case 4 % Spanish
    LoadRules_Spanish;
end

