function handles = Initialize_PTB_devices(params, debug_mode)

%% DEBUG (comment out if not debug-mode)
%PsychDebugWindowConfiguration([0],[0.5])

%% KEYBOARD
handles.escapeKey = KbName('ESCAPE');
handles.LKey = KbName('x');
handles.RKey = KbName('m');
handles.Key = KbName('space');
keysOfInterest=zeros(1,256);
keysOfInterest(KbName({'a','l','ESCAPE'}))=1;
KbQueueCreate(-1, keysOfInterest);

%% SCREEN
Screen('Preference', 'SkipSyncTests', 0);
Screen('Preference', 'TextRenderer',  1);
screens = Screen('Screens');


handles.screenNumber = max(screens);
handles.black = BlackIndex(handles.screenNumber);
handles.white = WhiteIndex(handles.screenNumber);

% Screen('NominalFrameRate', handles.screenNumber) % screen refresh rate


rect = get(0, 'ScreenSize');
if debug_mode
    handles.rect = [0 0 rect(3:4)./2];
    handles.win = Screen('OpenWindow',handles.screenNumber, handles.black, handles.rect);
else
    handles.rect = [0 0 rect(3:4)./1.01];
    handles.win = Screen('OpenWindow',handles.screenNumber, handles.black, handles.rect);
end 



%% TEXT ON SCREEN
Screen('TextFont',handles.win, 'Arial');
Screen('TextSize',handles.win, 20);   % 160 --> ~25mm text height (from top of `d' to bottom of `g').
Screen('TextStyle', handles.win, 1);   % 0=normal text style. 1=bold. 2=italic.























