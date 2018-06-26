% InitOutputFile.m  

clear response RT wordonset wordoffset choicescreen startfix

% if ~isTrain
%     load(StimFile,'wordlist','nsentences')
% end

% saving the time when the block STARTED as its label   *
%outfile = [ 'ExperimentalRun_' BlockShortLabs{curBlockType} TrainLabs{isTrain+1} sprintf('_%d',fix(clock)) '.mat' ];
outfile = [ savedir filesep 'ExperimentalRun_' sprintf('_%d',fix(clock)) '.mat' ];

% saving here just the StimFile name, which tells the user where they can go to to get more information about the stimuli     
if isTrain
    save(outfile,'SameKey','DiffKey','wordlist','samestruct') % for training blocks, the wordlistmayhave been adjusted from what is in the stimulus file
else
    wordlist_ExpRun=wordlist;
    save(outfile,'SameKey','DiffKey','StimFile','StimFilePerSent','SentNumInStimFile','PressTrs','wordlist_ExpRun','BlockType')     
end
%%% need to save StimFile...   