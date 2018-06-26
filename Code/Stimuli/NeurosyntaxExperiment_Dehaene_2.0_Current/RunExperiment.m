%function RunExperiment()
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

%%%%%% ALL PARAMETERS ARE IN THE FOLLOWING FUNCTION -- they can be changed for a specific lab or other purpose:
setparameters_Texas   % Font size parameters and delay period parameters are stored here...    

GenCSVListOnly=0;    % Creates one large .csv file for use in Presentation later, and doesn't use Matlab Psychophysics Toolbox to present the stimuli   
subjectname='NYU_subject8';

nsent_PerBl=6;      %40;
nsent_PerLocBl=8;   %40;

nBlocksToGen=3;     % 3 for Main and Jabber blocks...  
MaxNMemBlocks=2;    % 2 for the Loc block...    

% for displaying to the patient at the start of each block    
BlockTitles={'Memory Task','Sentence Task','Jabberwocky Task'};     % this is what gets shown to the patient using the PsychToolBox... 'Meaningless word sentence task'};
BlockOrder=[1 2 3];     % 1= Mem, 2= Sent, 3=Jabber   ... note this matters even for arranging the lists in     

WorkingMemoryInMainBlock=1; % 1 for working memory task in miain block, 2 for matching probe sentences task   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CODE BEGINS HERE -- DO NOT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CHANGE!

TrainMentionYouCanPressEscape=0;
skipPsychToolboxPres=0;     % for debugging, to run the code without actually presenting the stimuli     
BlockTitScreenText2Opt=3;      %can be 0, 1 or 2, or 3... see BlockTitleScreen.m for more   

BlockShortLabs={'Loc','Main','Jab'};  % this is only for naming files   
TrainLabs={'','Train'};


rand('twister',sum(10*clock)); %%% reset random numbers

%%%%%%%% adjust this line for where ou want the fils to be saved
savedir=pwd;
disp(' ');
disp('NEUROSYNTAX EXPERIMENT')
disp(' ');
if strcmp(savedir,'?')
    disp('Use the following dialog to navigate to the working directory of')
    disp('Presentation in your computer, and click Select Folder.')
    disp(' ')
    disp('Note that you can adjust the variable savedir permanently in the file')
    disp('setparameters_NYU.m in order to circumvent this prompt in the future.')
    disp(' ')
    input('Press Enter to continue and navigate to the Presentation directory.');
    savedir=uigetdir;
end
initdir=pwd;


if GenCSVListOnly
if iscell(escapekey)
    disp([ 'You may interrupt the Psychophysics Toolbox Experiment by pressing the [' escapekey{1} '] key' ]);
else
    disp([ 'You may interrupt the Psychophysics Toolbox Experiment by pressing the [' escapekey '] key' ]);
end
disp(' ');
end
disp('Starting stimulus generation. This may take a few minutes.')
disp('This part can be interrupted by CTRL-C');


% create subject dir if it dn exist  
%savedir=[savedir filesep subjectname];
savedir=pwd;
if ~exist(savedir,'dir')
    mkdir(savedir);
end


%%% Initial Stimulus Generation Loop       
tic;
sttime=cputime;

[Counts_Main, wordusecount_Main, TotRemCounts_Main, ProbeFromToCounts_Main, Counts_Jab, wordusecount_Jab, TotRemCounts_Jab, ProbeFromToCounts_Jab]=deal( [] );
[outfile_Main, outfile_Jab]=deal( cell(1,nBlocksToGen) );
for ibl=1:nBlocksToGen
    for curBlockType=BlockOrder
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    outfile_Loc{ibl} = StimulusGeneration(savedir,language,nsent_PerLocBl,1);
                end
            case 2
                [outfile_Main{ibl}, Counts_Main, wordusecount_Main, TotRemCounts_Main, ProbeFromToCounts_Main] = StimulusGeneration(savedir,language,nsent_PerBl,2,Counts_Main,wordusecount_Main,TotRemCounts_Main, ProbeFromToCounts_Main,WorkingMemoryInMainBlock);
            case 3
                [outfile_Jab{ibl}, Counts_Jab, wordusecount_Jab, TotRemCounts_Jab, ProbeFromToCounts_Jab] = StimulusGeneration(savedir,language,nsent_PerBl,3,Counts_Jab,wordusecount_Jab,TotRemCounts_Jab, ProbeFromToCounts_Jab,WorkingMemoryInMainBlock);
        end
    end
end
%entime=toc;
entime=cputime;
disp([' For total initial stimulus Generation: ' num2str(entime-sttime) ' seconds elapsed'])

    
if GenCSVListOnly
    GenCSVList
else
    
disp('Launching PsychToolBox');

BlockPauseDur=[];   % the duration of the preceding pause block in seconds.... set to empty for the first block    
HaveRunExpBlock=0;
EndExpNow=0;
tic
if ~skipPsychToolboxPres
try % use exceptions to return the screen to normal after crash    
    InitOverallExperiment
               
    % will do this at the start of each training/experiment block
    SendMarkers     % send a short sequence to unambiguously identify the experiment, just in case we get confused in the successive files...    
    
    for ibl=1:nBlocksToGen
        for curBlockType=BlockOrder            
            if curBlockType==1 && ibl > MaxNMemBlocks
                continue
            end
            
            if HaveRunExpBlock   % if this is our first overallblock, don't run this screen
                PauseTitleScreen
                if ismember( KbName(keyCode),escapekey )
                    EndOverallExperiment
                    return
                end
            end
            
            curTit=BlockTitles{curBlockType};
            if ibl==1 && 0==54
                MainExpFlag=0;
                BlockTitleScreen      % making this a script here so that everything stays within the same workspace
                
                switch curBlockType
                    case 1
                        setTrainLocText
                        loadTrainLocStimuli
                    case 2
                        setTrainMainText
                        loadTrainMainStimuli
                    case 3
                        setTrainJabText
                        loadTrainJabStimuli
                end
                isTrain=1;
                InitOutputFile
                
                Train
                saveBlockDur      % can't do this inside Train, because we can exit Train unpredictably given an escapekey input from the patient 
                if EndExpNow
                    EndOverallExperiment
                    return
                end
                
                curTit=[curTit '\nmain experiment'];
                MainExpFlag=1;
                tmpnsent=nsent_PerBl;
                BlockTitleScreen
                
                if BlockTitScreenText2Opt~=3
                    ReassuranceScreen
                    if ismember( KbName(keyCode),escapekey )
                        EndOverallExperiment
                        return
                    end
                end
            else
                if curBlockType==3 && WorkingMemoryInMainBlock
                    continue
                end
                MainExpFlag=0;
                tmpnsent=nsent_PerBl;
                BlockTitleScreen                
                TrainAlt
            end                                    
                        
            switch curBlockType
                case 1
                    StimFile=outfile_Loc{ibl}; 
                case 2
                    StimFile=outfile_Main{ibl}; 
                    if WorkingMemoryInMainBlock
                        StimFile2=outfile_Jab{ibl};
                    end
                case 3
                    if WorkingMemoryInMainBlock
                        continue
                    else
                        StimFile=outfile_Jab{ibl};
                    end
            end 
            isTrain=0;
            InitOutputFile
                        
            ExpBlock
            saveBlockDur      % can't do this inside ExpBlock, because we can exit it unpredictably given an escapekey input from the patient 
            if ismember( KbName(keyCode),escapekey )
                EndOverallExperiment
                return
            end
        end        
    end
        
    GoodJobScreen
    Screen(window,'Flip',window);
    WaitSecs(0.75)
    GoodJobScreen
    ThankYouScreen    
    Screen(window,'Flip',window);
    WaitSecs(0.75)
    GoodJobScreen
    ThankYouScreen
    DrawPressAnyKey
    Screen(window,'Flip',window);
    KbPressWait    
    
catch % if PTB crashes it will land here, allowing us to reset the screen to normal.
    a = lasterror; a.message % find out what the error is
end;

EndOverallExperiment
end
end
