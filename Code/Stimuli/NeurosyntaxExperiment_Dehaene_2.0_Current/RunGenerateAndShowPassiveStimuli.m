% RunGenerateAndShowPassiveStimuli.m
%
% This was modified from RunExperiment.m for the Neurosyntax 2.0 version   
%
%%%%% NeuroSyntax experiment of sentence reading and ellipsis judgment
%%%%% (c) Stanislas Dehaene, Matthew Nelson
%%%%%
%%%%% USAGE:
%%%%% RunExperiment()
%%%%%
%%%%% All parameters should be adjusted by changing the appropriate .m
%%%%% files. Changeable parameters are in the first lines of this code
%%%%% below, in the setparameters_xxx.m (ie setparameters_NYU.m) file, 
%%%%% and in the subscripts called by setparameters_xxx.m.  
%%%%%
%%%%% The program will first generate enough stimuli for several blocks 
%%%%% using StimulusGeneration.m. This may take 1 or 2 minutes. The program
%%%%% will then use the Matlab Psychophysics Toolbox to deliver the stimuli
%%%%% to the patient, recording responses after every trial. Data will be
%%%%% saved to the folder pre-specified in setparameters_xxx.m, or if 
%%%%% desired the experimenter will be prompted as to where to locally save
%%%%% the behavioral responses upon each run of the program.
%%%%% GeneratedSentences files will store the stimuli, while
%%%%% ExperimentalRun stimuli will store the stimuli and responses for each
%%%%% corresponding block.
%%%%%
%%%%% For questions, contact Matthew Nelson at
%%%%% matthew.nelson.neuro@gmail.com
%%%%% 2015-03-23

clear
Screen('Preference', 'SkipSyncTests', 1); 

%%%%%% ALL PARAMETERS ARE IN THE FOLLOWING FUNCTION -- they can be changed for a specific lab or other purpose:

subjectname='Texas_subject8';
language=1; %1=English; 2=French; 3=Dutch; 4=Spanish      

% just get the localizer block from the other patients...          
nsent_PerBl=40;     % 40;
                    % for Main and Jabber, we'll  generte this amount of
                    % trials each at once, then combine the two, making two total mixed blocks of this size      
nsent_PerLocBl=40;   %40;

  
nBlocksToGen=3;     % 3 for Main and Jabber blocks... will number of blocks will be twice this number of mixed Main/Jabber blocks 
MaxNMemBlocks=2;    % 2 for the Loc block...    

nPressFlashes=3;
nPressTrs=4;     % in a block of 40    
MainVsProbeInterruptRatio=0.67;

Photodiode=true;
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CODE BEGINS HERE -- DO NOT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CHANGE!

initdir=pwd;
setparameters_Texas
BlockTitles={'Memory Task','Sentence Task','Jabberwocky Task'};     % this is what gets shown to the patient using the PsychToolBox... 'Meaningless word sentence task'};
% This is the Block order for generating the stimuli...        
BlockOrder=[1 2 3];     % 1= Mem, 2= Sent, 3=Jabber   ... note this matters even for arranging the lists in        


% NeuroSyntaxSetPaths

savedir=pwd;
if ~exist(savedir,'dir')
    mkdir(savedir);
end

savedir=[savedir filesep subjectname];
if ~exist(savedir,'dir')
    mkdir(savedir);
end

tic;
sttime=cputime;

[Counts_Main, wordusecount_Main, TotRemCounts_Main, ProbeFromToCounts_Main, Counts_Jab, wordusecount_Jab, TotRemCounts_Jab, ProbeFromToCounts_Jab]=deal( [] );
[outfile_Main, outfile_Jab]=deal( cell(1,nBlocksToGen) );
for ibl=1:nBlocksToGen
    for curBlockType=BlockOrder
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    outfile_Loc{ibl} = StimulusGeneration_PassiveStimuli2(savedir,language,nsent_PerLocBl,1);
                end
            case 2
                [outfile_Main{ibl}, Counts_Main, wordusecount_Main, TotRemCounts_Main, ProbeFromToCounts_Main] = StimulusGeneration_PassiveStimuli2(savedir,language,nsent_PerBl,2,Counts_Main,wordusecount_Main,TotRemCounts_Main, ProbeFromToCounts_Main);
            case 3
                [outfile_Jab{ibl}, Counts_Jab, wordusecount_Jab, TotRemCounts_Jab, ProbeFromToCounts_Jab] = StimulusGeneration_PassiveStimuli2(savedir,language,nsent_PerBl,3,Counts_Jab,wordusecount_Jab,TotRemCounts_Jab, ProbeFromToCounts_Jab);
        end
    end
end
%entime=toc;
entime=cputime;
disp([' For total initial stimulus Generation: ' num2str(entime-sttime) ' seconds elapsed'])

PressStr='press'; % this must match what it is inside: StimulusGeneration_PassiveStimuli2.m     

%try
    ShowStimFromSavedFiles_Passive
%catch % if PTB crashes it will land here, allowing us to reset the screen to normal.
%    a = lasterror; a.message % find out what the error is
%end;

EndOverallExperiment


