function RunExperiment_MEG( nsent_PerBl,nBlocksToGen,savedir_root,subjectname )
%%%%% NeuroSyntax experiment of sentence reading and ellipsis judgment
%%%%% (c) Stanislas Dehaene, Matthew Nelson
%%%%
%%%%% For questions, contact Matthew Nelson at
%%%%% matthew.nelson.neuro@gmail.com
%%%%% 2016-02-28

if nargin<1 || isempty(nsent_PerBl);        nsent_PerBl=60;        end
if nargin<2 || isempty(nBlocksToGen);       nBlocksToGen=6;        end
if nargin<3 || isempty(savedir_root);       savedir_root=pwd;        end
if nargin<4 || isempty(subjectname);        subjectname='NeuroSyntax2_MEGSubj1';        end   
    


%%%%%% ALL PARAMETERS ARE IN THE FOLLOWING FUNCTION -- they can be changed for a specific lab or other purpose:
setparameters_NYU   % Font size parameters and delay period parameters are stored here...    

GenCSVListOnly=1;    % Creates one large .csv file for use in Presentation later, and doesn't use Matlab Psychophysics Toolbox to present the stimuli   
%%% subjectname='NYU_subject8';

%%% nsent_PerBl=60;      %40;
nsent_PerLocBl=60;   %40;

%%% nBlocksToGen=6;     % 3 for Main and Jabber blocks...  
MaxNMemBlocks=0;    % 2 for the Loc block...    

% for displaying to the patient at the start of each block    
BlockTitles={'Memory Task','Sentence Task','Jabberwocky Task'};     % this is what gets shown to the patient using the PsychToolBox... 'Meaningless word sentence task'};
BlockOrder=[2];     % 1= Mem, 2= Sent, 3=Jabber   ... note this matters even for arranging the lists in     

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CODE BEGINS HERE -- DO NOT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CHANGE!

TrainMentionYouCanPressEscape=0;
skipPsychToolboxPres=0;     % for debugging, to run the code without actually presenting the stimuli     
BlockTitScreenText2Opt=3;      %can be 0, 1 or 2, or 3... see BlockTitleScreen.m for more   

BlockShortLabs={'Loc','Main','Jab'};  % this is only for naming files   
TrainLabs={'','Train'};


rand('twister',sum(10*clock)); %%% reset random numbers

%%%%%%%% adjust this line for where ou want the fils to be saved
disp(' ');
disp('NEUROSYNTAX EXPERIMENT')
disp(' ');
if strcmp(savedir_root,'?')
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
savedir=[savedir_root filesep subjectname];
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
                [outfile_Main{ibl}, Counts_Main, wordusecount_Main, TotRemCounts_Main, ProbeFromToCounts_Main] = StimulusGeneration(savedir,language,nsent_PerBl,2,Counts_Main,wordusecount_Main,TotRemCounts_Main, ProbeFromToCounts_Main,0);
            case 3
                [outfile_Jab{ibl}, Counts_Jab, wordusecount_Jab, TotRemCounts_Jab, ProbeFromToCounts_Jab] = StimulusGeneration(savedir,language,nsent_PerBl,3,Counts_Jab,wordusecount_Jab,TotRemCounts_Jab, ProbeFromToCounts_Jab,0);
        end
    end
end
%entime=toc;
entime=cputime;
disp([' For total initial stimulus Generation: ' num2str(entime-sttime) ' seconds elapsed'])


%%%%% Now present the stimuli
for ibl=1:nBlocksToGen
    for curBlockType=BlockOrder
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    load( [savedir filesep outfile_Loc{ibl}] );
                end
            case 2
                load( [savedir filesep outfile_Main{ibl}] );
            case 3
                load( [savedir filesep outfile_Jab{ibl}] );
        end
        
        %%%%%%% Call Seb's function right here
        %%%%%%% The function should present the sentences from the cell array wordlist, a nsentences x 2      
   
        
        
    end
end
