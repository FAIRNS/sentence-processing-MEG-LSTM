function run_visual_block(handles, block, stimuli_sentences, fid_log, cumTrial, params)

%% START BLOCK
% 'Event', 'Block', 'Trial', 'StimNum', 'WordNum', 'StimulusName', 'Time'
block_start = GetSecs;
log_str = createLogString('BlockStart', block, 0, 0, 0, ' ', block_start);
fprintf(fid_log,log_str); % WRITE-TO-LOG

%% LOOP OVER TRIALS
for trial=1:length(stimuli_sentences) % loop through trials
    %% RSVP parameters
    slide       = 0;
    curr_sentence  = stimuli_sentences{trial}{1};
    curr_sentence_type  = stimuli_sentences{trial}{2};
    curr_condition  = stimuli_sentences{trial}{3};
    curr_viol_on_slide  = stimuli_sentences{trial}{4};
    violation_type  = stimuli_sentences{trial}{5};
    cumTrial = cumTrial+1;  
    curr_RT_trial = 0;
    
    %% Response
    if str2double(stimuli_sentences{trial}{4}) ~= 0
        slide_num_of_viol = abs(str2double(stimuli_sentences{trial}{4}));
        correct_response = 'VIOLATION';
    else
        correct_response = 'ACCEPTABLE';
        slide_num_of_viol = 0;
    end
    subject_detected_viol = false;
    
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
    first_press_time = 0;
    for slide = 1:numel(curr_sentence)
        %%%%%%%%%%%%% TEXT ON %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        DrawFormattedText(handles.win, curr_sentence{slide}, 'center', 'center', handles.white);
        slide_onset = Screen('Flip', handles.win); % Word ON
        if slide == slide_num_of_viol % Can be True only for violation trials (otherwise, slide_num_of_viol =0)
            violation_slide_onset = slide_onset;
        end
        log_str = createLogString('WORD_ON', block, trial, 0, slide, curr_sentence{slide}, slide_onset, curr_sentence_type, curr_condition, curr_viol_on_slide, violation_type);
        fprintf(fid_log,log_str); % WRITE-TO-LOG
        [key_press_name, key_press_time] = getSubjectResponse(handles.LKey, handles.escapeKey, slide_onset, params.stimulus_ontime); % CHECK KEY PRESS
        if ~isempty(key_press_name) % WRITE TO LOG IF KEY PRESS
            log_str = createLogString('KEY_PRESS', block, trial, 0, slide, key_press_name, key_press_time, curr_sentence_type, curr_condition, curr_viol_on_slide);
            fprintf(fid_log,log_str); % WRITE-TO-LOG
        end
        if ~subject_detected_viol && strcmp(key_press_name, 'VIOLATION') % FIRST KEY PRESS IN CURRENT TRIAL
            first_press_time = key_press_time;
            subject_detected_viol = true;
        end
%         if ~isempty(key_press_name) % complete onset duration if key was pressed
          WaitSecs('UntilTime', slide_onset + params.stimulus_ontime);
%         end
        %%%%%%%%%%%% TEXT OFF %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        slide_offset = Screen('Flip', handles.win); % Word OFF
        log_str = createLogString('WORD_OFF', block, trial, 0, slide, ' ', slide_offset, curr_sentence_type, curr_condition, curr_viol_on_slide);
        fprintf(fid_log,log_str); % WRITE-TO-LOG 
        [key_press_name, key_press_time] = getSubjectResponse(handles.LKey, handles.escapeKey, slide_offset, params.stimulus_offtime); % CHECK KEY PRESS
        if ~isempty(key_press_name) % WRITE TO LOG IF KEY PRESS
            log_str = createLogString('KEY_PRESS', block, trial, 0, slide, key_press_name, key_press_time, curr_sentence_type, curr_condition, curr_viol_on_slide);
            fprintf(fid_log,log_str); % WRITE-TO-LOG
        end
        if ~subject_detected_viol && strcmp(key_press_name, 'VIOLATION') % FIRST KEY PRESS IN CURRENT TRIAL
            first_press_time = key_press_time;
            subject_detected_viol = true;            
        end
%         if ~isempty(key_press_name) % complete onset duration if key was pressed
            WaitSecs('UntilTime', slide_offset + params.stimulus_offtime);
%         end
        
    end
    
    %%%%%%%%%%%%%%%%%%%%%
    %%%% CALC RT %%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%
    if first_press_time > 0 && slide_num_of_viol > 0 % key was pressed and it's a violation trial
        curr_RT_trial = first_press_time - violation_slide_onset;
    else
        curr_RT_trial = 0;
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%% END RSVP for current sentence %%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    curr_RT_panel = 0;
    %%%%%%%%%%%%% FIXATION-TO-RESPONSE-PANEL (ONSET) %%%%%%%%%%%%%%%%%%%%
    DrawFormattedText(handles.win, '+', 'center', 'center', [255,255,255]);
    fix2panel_onset  = Screen('Flip', handles.win);
    log_str = createLogString('FIX2PANEL_ON', block, trial, '-', '-', '+', fix2panel_onset, curr_sentence_type, curr_condition, curr_viol_on_slide, violation_type);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    WaitSecs('UntilTime', fix2panel_onset + params.SOA_visual);
    
    
    %%%%%%%%%%%%%% DECISION SCREEN ONLINE %%%%%%%%%%%%%%%%%%%%%%%%%%
    decision_screen   = [params.str_correct, '                         ', params.str_wrong];
    DrawFormattedText(handles.win, decision_screen, 'center', 'center', handles.white);
    panel_onset= Screen('Flip', handles.win); % Pannel ON
    log_str = createLogString('PanelOn', block, trial, '-', '-', ' ', panel_onset, curr_sentence_type, curr_condition, curr_viol_on_slide, violation_type);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    
    %%%%%%%%%%%%%%% USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%
    clear Response pressed Key key_press_time
    panel_response  = '';
    % participant should respond now:
    key_press_time = panel_onset;
     while (GetSecs <= panel_onset + params.panel_ontime)
         [pressed,~,key_code] = KbCheck;
         if pressed~=0
             if key_code(handles.RKey)
                 panel_response = 'VIOLATION';
                 key_press_time = GetSecs;
                 break
             elseif key_code(handles.LKey)
                 panel_response = 'ACCEPTABLE';
                 key_press_time = GetSecs;
                 break
            elseif key_code(handles.escapeKey)
                sca
                psychrethrow(psychlasterror);
                KbQueueRelease;
                error('ESCAPE key was pressed')
             end
                     
         end
     end
     
    curr_RT_panel = key_press_time - panel_onset;
        
    log_str = createLogString('PanelResp', block, trial, '-', '-', panel_response, curr_RT_panel, curr_sentence_type, curr_condition, curr_viol_on_slide, violation_type);
    fprintf(fid_log,log_str); % WRITE-TO-LOG
    %%%%%%%%%%%%%% END OF DECISION SCREEN %%%%%%%%%%%%%
    
    
    %%%%%%%%%%%%% FEEDBACK SCREEN (ONSET) %%%%%%%%%%%%%%%%%%%
    [feedback_answer,correct_wrong] = checkResponse(correct_response, panel_response, subject_detected_viol);
    feedback2screen = feedback_answer(1:(strfind(feedback_answer, '_')-1));
    DrawFormattedText(handles.win, feedback2screen, 'center', 'center', handles.white);
    feedback_onset= Screen('Flip', handles.win); % Pannel ON
    log_str = createLogString('FeedbackOn', block, trial, '-', '-', ' ', feedback_onset, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    WaitSecs('UntilTime',feedback_onset + params.ISI_visual);
    feedback_offest = Screen('Flip', handles.win); % Feedback OFF
    log_str = createLogString('FeedbackOff', block, trial, '-', '-', ' ', feedback_offest, curr_sentence_type, curr_condition, curr_viol_on_slide);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    
    %%%%%%%%%%%%% ISI TO NEXT TRIAL %%%%%%%%%%%%%%%%%%%
    log_str = createLogString('END_TRIAL', block, trial, '-', '-', correct_wrong, curr_RT_trial, curr_sentence_type, curr_condition, curr_viol_on_slide, violation_type);
    fprintf(fid_log,log_str); % WRITE-TO-LOG 
    clear feedback_answer correct_wrong
    
end  %trial
