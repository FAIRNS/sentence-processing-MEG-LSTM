% -------------------------------------
% Doubly nested long-range dependencies
% -------------------------------------
clear; close all; clc    
debug_mode = 0    ;
 
if debug_mode
    dbstop if error  
    training = 0;
else
    training = questdlg('Do yo u want to include a training block?','Training block','Yes','No','Yes');
    if training(1) == 'Y', training = 1; else training = 0; end
end

%% INITIALIZATION
addpath('functions')
KbName('UnifyKeyNames') 
params = getParamsLocalGlobalParadigm(debug_mode);
fid_log = createLogFile(params); % OPEN LOG 
handles = Initialize_PTB_devices(params, debug_mode); % Open screens 

%% LOAD STIMULI 
sentences_per_block = load_stimuli(params);     

%% START EXPERIMENT
 try  
    %%%%%%% INSTRUCTIONS (WAIT FOR STROKE KEY PRESS)
    present_intro_slide(params, handles);
    KbStrokeWait;
    
    %%%%%%% GRAND START
    KbQueueStart;
    log_str = createLogString('GrandStart', 0, 0, 0, 0, ' ', GetSecs);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
     
    %%%%%% TRAINING   alj
    if training 
         %%%%%%% LOOP OVER TRAINING STIMULI
         run_training_block(handles, training_words, params); 
    end
    cumTrial=0;
    
    %%%%%%% PRESENT LONG FIXATION ONLY AT THE BEGINING
    DrawFormattedText(handles.win, '+', 'center', 'center', handles.white);
    Screen('Flip', handles.win);
    WaitSecs(1.5); %Wait before experiment start
    
    
    %%%%%%%% START EXPERIMENT
    for block = 1 :params.n_blocks
                DrawFormattedText(handles.win, ...
                ['Starting block: ' num2str(block) '/' num2str(params.n_blocks) newline ...
                'Please wait for the block to start.'], ...
                 'center', 'center', handles.white);
                Screen('Flip',handles.win);
                wait_for_key_press()
                
                run_visual_block(handles, block, sentences_per_block{block}, ...
                                fid_log, cumTrial, ...
                                params);   
    end 
    
catch
    sca
    psychrethrow(psychlasterror);
    KbQueueRelease;
    fprintf('Error occured\n')
end

%% %%%%%%% CLOSE ALL - END EXPERIMENT
fprintf('Done\n')
KbQueueRelease;
sca