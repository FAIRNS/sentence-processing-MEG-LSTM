function run_visual_block(handles, block, stimuli_sentences, fid_log, cumTrial, params)

%% START BLOCK
% 'Event', 'Block', 'Trial', 'StimNum', 'WordNum', 'StimulusName', 'Time'
block_start = GetSecs;
log_str = createLogString('BlockStart', block, 0, 0, 0, ' ', block_start);
fprintf(fid_log,log_str); % WRITE-TO-LOG

%% LOOP OVER TRIALS
for trial=1:length(stimuli_sentences) % loop through trials
    %% RSVP parameters
    slide_cnt       = 0;
    curr_sentence  = stimuli_sentences{trial}{1};
    curr_sentence_type  = stimuli_sentences{trial}{2};
    curr_condition  = stimuli_sentences{trial}{3};
    curr_viol_on_slide  = stimuli_sentences{trial}{4};
    cumTrial = cumTrial+1;  
    curr_RT = 0;
    
    %% Response
    if str2double(stimuli_sentences{trial}{4}) > 0
        correct_response = 'VIOLATION';
    else
        correct_response = '';
    end
    subject_response = '';
    
    %%
    %%%%%%%%%%%%% FIXATION BEFORE TRIAL (ONSET) %%%%%%%%%%%%%%%%%%%%
    DrawFormattedText(handles.win, '+', 'center', 'center', handles.white);
    fixation_onset = Screen('Flip', handles.win);
    log_str = createLogString('FIX_ON', block, trial, 0, '-', '+', fixation_onset, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG   
    WaitSecs('UntilTime',fixation_onset+params.fixation_duration_visual_block); %Wait before trial
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%% START RSVP for current sentence %%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for word = 1:numel(curr_sentence)
        key_press_time = '';
        key_press_name = '';
        slide_cnt = slide_cnt + 1;
        %%%%%%%%%%%%% TEXT ON %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        DrawFormattedText(handles.win, curr_sentence{word}, 'center', 'center', handles.white);
        word_onset = Screen('Flip', handles.win); % Word ON
        log_str = createLogString('WORD_ON', block, trial, 0, slide_cnt, curr_sentence{word}, word_onset, curr_sentence_type, curr_condition, curr_viol_on_slide);
        fprintf(fid_log,log_str); % WRITE-TO-LOG
        [key_press_name, key_press_time] = getSubjectResponse(handles, word_onset, params.stimulus_ontime); % CHECK KEY PRESS
        if ~isempty(key_press_name) % WRITE TO LOG IF KEY PRESS
            log_str = createLogString('KEY_PRESS', block, trial, 0, slide_cnt, key_press_name, key_press_time, curr_sentence_type, curr_condition, curr_viol_on_slide);
            fprintf(fid_log,log_str); % WRITE-TO-LOG
        end
        if isempty(subject_response) && ~isempty(key_press_name) % FIRST KEY PRESS IN CURRENT TRIAL
            curr_RT = key_press_time - word_onset;
            if strcmp(key_press_name, 'SPACE')
                subject_response = 'VIOLATION';
            end
        end
        WaitSecs('UntilTime', word_onset + params.stimulus_ontime);
        %%%%%%%%%%%%% TEXT OFF %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        word_offset = Screen('Flip', handles.win); % Word OFF
        log_str = createLogString('WORD_OFF', block, trial, 0, slide_cnt, ' ', word_offset, curr_sentence_type, curr_condition, curr_viol_on_slide);
        fprintf(fid_log,log_str); % WRITE-TO-LOG 
        [key_press_name, key_press_time] = getSubjectResponse(handles, word_offset, params.stimulus_offtime); % CHECK KEY PRESS
        if ~isempty(key_press_name) % WRITE TO LOG IF KEY PRESS
            log_str = createLogString('KEY_PRESS', block, trial, 0, slide_cnt, key_press_name, key_press_time, curr_sentence_type, curr_condition, curr_viol_on_slide);
            fprintf(fid_log,log_str); % WRITE-TO-LOG
        end
        if isempty(subject_response) && ~isempty(key_press_name) % FIRST KEY PRESS IN CURRENT TRIAL
            curr_RT = key_press_time - word_onset;
            if strcmp(key_press_name, 'SPACE')
                subject_response = 'VIOLATION';
            end
        end
        WaitSecs('UntilTime', word_offset + params.stimulus_offtime);
        
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%% END RSVP for current sentence %%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%%%%%%%%% FIXATION-TO-RESPONSE-PANEL (ONSET) %%%%%%%%%%%%%%%%%%%%
    DrawFormattedText(handles.win, '+', 'center', 'center', [255,255,255]);
    fix2panel_onset  = Screen('Flip', handles.win);
    log_str = createLogString('FIX2PANEL_ON', block, trial, '-', '-', '+', fix2panel_onset, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    WaitSecs('UntilTime', fix2panel_onset + params.SOA_visual);
    
    %%%%%%%%%%%%% FIXATION-TO-RESPONSE-PANEL (OFFSET) %%%%%%%%%%%%%%%%%%%%
    fix2panel_offset = Screen('Flip', handles.win);
    log_str = createLogString('FIX2PANEL_OFF', block, trial, '-', '-', ' ', fix2panel_offset, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    
    %%%%%%%%%%%%% FEEDBACK SCREEN (ONSET) %%%%%%%%%%%%%%%%%%%
    if strcmp(correct_response, subject_response)
       feedback_answer = 'Bravo!';
       correct_wrong = 'CORRECT';
    else
       feedback_answer = 'Peccato...';
       correct_wrong = 'WRONG';
    end
    DrawFormattedText(handles.win, feedback_answer, 'center', 'center', handles.white);
    panel_onset= Screen('Flip', handles.win); % Pannel ON
    log_str = createLogString('PANEL_ON', block, trial, '-', '-', ' ', panel_onset, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    
    %%%%%%%%%%%%% DECISION PANEL OFF %%%%%%%%%%%%%%%%%%%%%
    panel_offset    = Screen('Flip', handles.win); % Pannel OFF
    log_str = createLogString('PANEL_OFF', block, trial, '-', '-', ' ', panel_offset, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    
    %%%%%%%%%%%%% ISI TO NEXT TRIAL %%%%%%%%%%%%%%%%%%%
    WaitSecs('UntilTime',panel_offset + params.ISI_visual);
    log_str = createLogString('END_TRIAL', block, trial, '-', '-', correct_wrong, curr_RT, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    
end  %trial
