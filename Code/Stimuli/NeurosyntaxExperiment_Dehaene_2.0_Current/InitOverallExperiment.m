% InitOverallExperiment.m

%Screen('closeall'); % close any orphaned windows
PsychDefaultSetup(2);
[window, ScreenRect] = Screen(0, 'OpenWindow',200);
Screen('Preference', 'SkipSyncTests', 1);
FrameRate=Screen('FrameRate', window); %%% 60
ifi=Screen('GetFlipInterval',window);
[xpix, ypix]=Screen('WindowSize',window);
%rect=Screen('Rect',window);

% set the rectangle for the photodiode flash
if Photodiode
    PhotodiodeSize = 100; %% in pixels
    %PhotodiodeRect = [ PhotodiodeSize PhotodiodeSize 2*PhotodiodeSize 2*PhotodiodeSize ];
    PhotodiodeRect = [ 0 0 PhotodiodeSize PhotodiodeSize ];

    WaitFrames_PD=round(PD_Dur/ifi);
    PD_Dur=WaitFrames_PD*ifi;
end

% durations
wordduration = soa/2;
interword = soa/2;
WaitFrames_WordDur=round(wordduration/ifi);
WaitFrames_IW=round(interword/ifi);
wordduration=WaitFrames_WordDur*ifi;
interword=WaitFrames_IW*ifi;

% colors   
white = WhiteIndex(window); % pixel value for white
black = BlackIndex(window); % pixel value for black
blue = [0 0 255];
red = [255 0 0];
green = [0 130 0];

HideCursor; % turn off mouse cursor
Screen('TextFont',window, 'Arial');
%    Screen('TextStyle', w, 1+2); for Bold = 1, Italics = 2

Screen(window, 'WaitBlanking'); % make sure that waitblanking has been called at least once before entering loop

Priority( MaxPriority(window) ); % set high priority for max performance

%%% TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if TTLsending == 1  %%% MGH-style sending of TTL signals
    config_io; % set up IO for 32-bit MATLAB on 64-bit Windows - Alex 20120515
    % for 32bit MATLAB on 64-bit windows - LPT3 expresscard output is address 0x2000
    outp(hex2dec('2000'),0);
end
if TTLsending == 2  %%% Paris
    %for intracranial recordings in Paris, first set parallel port to 0
    lptwrite(888,0);
end
%%% TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% Ready?
Screen('TextSize',window, 24);
DrawFormattedText(window,'Start the recording NOW, then press a key when ready to launch the experiment','center','center',0);
if Photodiode  %%% set the photodiode to black
    Screen('FillRect',window,black,PhotodiodeRect);
end
prevtime=Screen(window,'Flip');

% KbQueueCreate
% WaitSecs(.6)
% [pressed, firstPress]=KbQueueCheck;


KbPressWait;
