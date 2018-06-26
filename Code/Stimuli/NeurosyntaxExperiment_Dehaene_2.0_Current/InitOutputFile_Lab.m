% InitOutputFile.m  

clear response RT wordonset wordoffset choicescreen startfix

% saving the time when the block STARTED as its label   *
outfile = [ 'ExperimentalRun_' BlockShortLabs{curBlockType} TrainLabs{isTrain+1} '_' sprintf('_%d',fix(clock)) '.mat' ];
