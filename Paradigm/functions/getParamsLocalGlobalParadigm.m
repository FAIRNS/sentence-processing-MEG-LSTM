function params = getParamsLocalGlobalParadigm(debug_mode)
%This function makes the struct that holds the parameters for the presentation of the stimuli and such.
%% SUBJECT AND SESSION NUMBERS

params.n_blocks = 2;
% refresh rate
params.r_rate =  60;

if debug_mode
    params.subject = '00';
    params.session = str2double('00');
else
    subject = inputdlg({'Enter subject number'},...
        'Subject Number',1,{''});
    params.subject = subject{1};
    
    session = inputdlg({'Enter session number'},...
        'Subject Number',1,{''});
    params.session=str2double(session{1});
    
end
%%%%%%%%% PATHS
params.path2intro_slide = fullfile('Stimuli','instructions_sentences.png');
params.path2stim        = fullfile('Stimuli', 'SUBJECT_FILES');

if ismac || isunix %comp == 'h'
    params.sio  = '/dev/tty.usbserial';
elseif ispc % strcmp(comp,'l')
    params.sio  = 'COM1';
end

%% %%%%%%% TEXT params
params.font_size    = 20; % Fontsize for words presented at the screen center
params.font_name    = 'Courier New';
params.font_color   = 'ffffff';
params.str_correct = 'corretta';
params.str_wrong = 'scorretta';

%% %%%%%%% TIMING params
params.fixation_duration_visual_block   = 0.6; %
params.stimulus_ontime                  = 0.250; % Duration of each word
params.stimulus_offtime                 = 0.250; % Duration of black between stimuli
params.SOA_visual                       = params.stimulus_ontime + params.stimulus_offtime;
params.ISI_to_response_panel            = 0.5;
params.panel_ontime                     = 2;  % Duration of panel on the screen
params.max_RT                           = 1.5;    % Maximum allowance for RT.
params.feedback_time                    = 0.5;
params.ISI_visual                      = 1; % from end of last trial to beginning of first trial

%% covert the default timings to round multiples of the rephresh rate
params = convert_toRR(params);

end
