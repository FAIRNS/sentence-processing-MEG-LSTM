% InitOutputFile.m  

clear response RT wordonset wordoffset choicescreen startfix

% saving the time when the block STARTED as its label   *
outfile = [ 'ExperimentalRun_' BlockShortLabs{curBlockType} TrainLabs{isTrain+1} '_' sprintf('_%d',fix(clock)) '.mat' ];

% just save the entire workspace at this point...
% that will include all the stimuli to be delivered for this block,   
% and it will include the pointers of what type of block this is, and which stimuli go with which blocks  
save(outfile)
