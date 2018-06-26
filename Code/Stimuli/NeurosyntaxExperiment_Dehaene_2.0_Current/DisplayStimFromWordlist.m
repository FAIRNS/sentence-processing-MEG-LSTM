% DisplayStimFromWordlist.m

BlockStrs={'Loc','MainAndJab'};
BlockType=BlockStrs{curBlockType};
switch curBlockType
    case 1
        StimFile={outfile_Loc{ibl}};
    case 2
        StimFile={outfile_Main{ibl},outfile_Jab{ibl}};
end
isTrain=0;
InitOutputFile2
nsentences=length(wordlist);

ExpBlock_Passive
saveBlockDur      % can't do this inside ExpBlock, because we can exit it unpredictably given an escapekey input from the patient
if ~isempty(KbName(keyCode)) && ismember( KbName(keyCode),escapekey )
    EndOverallExperiment
    return
end

