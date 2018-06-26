function [outfile ] = RunExperiment(nsentences,BlockType,varargin)
%%%%% NeuroSyntax experiment of sentence reading and ellipsis judgment
%%%%% (c) Stanislas Dehaene + Matthew Nelson
%%%%%
%%%%% USAGE:
%%%%% RunExperiment(nsentences,language)
%%%%%
%%%%% EXAMPLES:
%%%%%     RunExperiment(80,2,1);
%%%%% for a 12-minute Main Sentences experimental block with 80 sentences in English
%%%%%     RunExperiment(80,2,2);
%%%%% for a 12-minute experiment with 80 sentences in French
%%%%%
%%%%% The first parameter is the number of sentences. 
%%%%%
%%%%% The second parameter is the type of Block. Enter 1 for the Localizer block.    
%%%%% This is a working memory task with short real sentences and random
%%%%% word lists interleaved. Enter 2 for the Main sentence block (A Same or Different task
%%%%% using real sentences and shortened (and potentially altered) versions
%%%%% of those sentences). Enter 3 for the Jabberwocky block. This is the
%%%%% same task as the Main sentence block, with the content words of the
%%%%% sentences replaced with pseudowords.
%%%%%
%%%%% The third parameter (optional) is the language (1=English, 2=French,
%%%%% 3=Dutch, 4=Spanish).
%%%%%
%%%%% The program will automatically call the StimulusGeneration routine
%%%%% which will use the appropriate language to generate sentences according to the
%%%%% the current lexicon and rules (this takes about 35 seconds on my laptop).
%%%%% After this delay to generate the sentences, the experiment will run
%%%%% using the Psychophysics toolbox in matlab to display the stimuli.
%%%%%
%%%%% Everything will be automatically saved to a dated file.
%%%%%
%%%%% Note the behavioral data will be stored in the pwd
%%%%% It may be useful to navigate in matlab to where you want the 
%%%%% behavioral data to be stored before running this


%%%%%% ALL PARAMETERS ARE IN THE FOLLOWING FUNCTION -- they can be changed for a specific lab:
setparameters_NYU;

fontsizes=[24 36];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CODE BEGINS HERE -- DO NOT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CHANGE!

rand('twister',sum(10*clock)); %%% reset random numbers

global language

if nargin<2 || isempty(BlockType)
    BlockType=2;
end

if size(varargin,2)>=1
    language = varargin{1};
else
    language = defaultlanguage;
end

disp(' ');
disp('NEUROSYNTAX EXPERIMENT')
disp(' ');
disp([ 'You may interrupt the experiment by pressing the [' escapekey '] key' ]);
disp(' ');
disp('Stimulus generation may take a while, can be interrupted by CTRL-C');
disp(' ');
disp('Press RETURN to begin');
pause;

currentdirectory = pwd;  %%% saves the working directory

if nsentences > 0
    ControlExperiment = false;
    %%%%%%%% generate and randomize the stimuli for a full NeuroSyntax
    %%%%%%%% experiment
    outfile = StimulusGeneration(nsentences,BlockType);  %%% generate n sentences in language i (1=English, 2 = French)
    load(outfile);
    
    %clear wordonset startfix
    %%%% prepare the lists of randomized parameters
    
    %% Choose the font: large or small
%     fontused = ones(1,nsentences);
%     fontused(1:round(nsentences/2)) = 2;
%     fontused = Shuffle(fontused);
    
    
else %%%% generate a yoked control experiment
    SetControlBlockStimuli
end
disp('Launching PsychToolBox');

tic
try % use exceptions to return the screen to normal after crash
    
    %Screen('closeall'); % close any orphaned windows
    [window, ScreenRect] = Screen(0, 'OpenWindow',200);
    FrameRate=60;%Screen('FrameRate', window); %%% just used for the initial signature
    
    % set the rectangle for the photodiode flash
    PhotodiodeSize = 100; %% in pixels
    PhotodiodeRect = [ PhotodiodeSize PhotodiodeSize 2*PhotodiodeSize 2*PhotodiodeSize ];
    
    white = WhiteIndex(window); % pixel value for white
    black = BlackIndex(window); % pixel value for black
    
    %HideCursor; % turn off mouse cursor
    Screen('TextFont',window, 'Arial');
    %    Screen('TextStyle', w, 1+2); for Bold = 1, Italics = 2
    
    Screen(window, 'WaitBlanking'); % make sure that waitblanking has been called at least once before entering loop
    
    Priority(2); % set high priority for max performance
    
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
    DrawFormattedText(window,'Start recording NOW, then press a key to launch experiment','center','center',0);
    if Photodiode == 1  %%% set the photodiode to black
        Screen('FillRect',window,black,PhotodiodeRect);
    end
    Screen(window,'Flip');
    
    % don't start experiment until user pushes key
    %     keyIsDown = 0;
    %     while ~keyIsDown
    %         [keyIsDown, secs, keyCode, deltaSecs] = KbCheck;
    %     end
    KbPressWait;
    
    %%%%%% Experiment started -- clear the screen
    Screen('TextSize',window, 9);
    DrawFormattedText(window,'+','center','center',100);
    if Photodiode == 1  %%% set the photodiode to black
        Screen('FillRect',window,black,PhotodiodeRect);
    end
    prevtime = Screen(window,'Flip');
    
    %%% TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%% send a short sequence to unambiguously identify the experiment, just in
    %%% case we get confused in the successive files...
    mark_on  = round(((random('unid',5)+2)/FrameRate)*1000); %%% random duration in milliseconds
    mark_off = round(((random('unid',5)+2)/FrameRate)*1000); %%% random duration in milliseconds
    mark_number = random('unid',5)+5;
    
    if Photodiode == 1  %%% send flashes to the photodiode
        for imark = 1:mark_number
            DrawFormattedText(window,'+','center','center',100);
            Screen('FillRect',window,white,PhotodiodeRect);
            prevtime=Screen(window,'Flip',prevtime + mark_on/1000 - 0.005);
            
            DrawFormattedText(window,'+','center','center',100);
            Screen('FillRect',window,black,PhotodiodeRect);
            prevtime=Screen(window,'Flip',prevtime + mark_off/1000 - 0.005);
        end
    end
    
    if TTLsending == 1  %%% USA
        for imark = 1:mark_number
            % for 32bit MATLAB on 64-bit windows - LPT3 expresscard output is address 0x2000
            outp(hex2dec('2000'),255);
            WaitSecs(mark_on/1000);
            outp(hex2dec('2000'),0);
            WaitSecs(mark_off/1000);
        end
    end
    if TTLsending == 2  %%% Paris
        for imark = 1:mark_number
            lptwrite(888,255);
            WaitSecs(mark_on/1000);
            lptwrite(888,0);
            WaitSecs(mark_off/1000);
        end
    end
    %%% TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
    for isent = 1:nsentences  %%% this is the index of the trial in the experiment                
        %%%%% note that the original sentences are shuffle through the variable TrialOrder
        
        %%% fixation point
        Screen('TextSize',window, 9);
        DrawFormattedText(window,'+','center','center',100);
        if Photodiode == 1
            Screen('FillRect',window,black,PhotodiodeRect);
        end
        startfix{isent} = Screen(window,'Flip');
        prevtime = GetSecs;
        WaitSecs(0.4);
        
        %%% Ready?
        Screen('TextSize',window, 24);
        if Photodiode == 1
            Screen('FillRect',window,black,PhotodiodeRect);
        end
        %       DrawFormattedText(window,'Ready?','center','center',0);
        Screen(window,'Flip');
        WaitSecs(0.4);
        
        %%% wait for any key press
        %        keyIsDown = 0;
        %        while ~keyIsDown
        %            [keyIsDown, secs, keyCode, deltaSecs] = KbCheck;
        %        end
        
        %%% fixation point, with flash for photodiode if needed
        Screen('TextSize',window, 9);
        DrawFormattedText(window,'+','center','center',100);
        if Photodiode == 1  %%% USA -- send flashes to the photodiode
            Screen('FillRect',window,white,PhotodiodeRect);
        end
        prevtime = Screen(window,'Flip');
        startfix{isent} = prevtime;
        
        %%% TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % send a trigger at the onset of the fixation preceding the first sentence of
        % each pair
        if Photodiode == 1  %%% after 50 ms, return to black screen with fixation
            Screen('TextSize',window, 9);
            DrawFormattedText(window,'+','center','center',100);
            Screen('FillRect',window,black,PhotodiodeRect);
            Screen(window,'Flip',prevtime + 0.050 - 0.005); %%% 50 millisecond flash
        end
        if TTLsending == 1  %%% Paris
            outp(hex2dec('2000'),255);
            WaitSecs(0.05);
            outp(hex2dec('2000'),0);
        end
        if TTLsending == 2  %%% Paris
            lptwrite(888,255);
            WaitSecs(0.05);
            lptwrite(888,0);
        end
        %%% END TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        prevtime = GetSecs;
        WaitSecs(0.6);
        prevtime = GetSecs;
        
        for inum = 1:2
            nwords = length(wordlist{isent,inum});
            wordduration = soa/2;
            interword = soa/2;
            
            for w=1:nwords
                %%%% set the font
%                 if fontused(isent) == 1
                    Screen('TextSize',window, 36);  %     round(24*fontscaling));
                    Screen('TextStyle',window, 1);  %%% 0 = normal
%                 else
%                     Screen('TextSize',window, 72);  %      round(36*fontscaling));
%                     Screen('TextStyle',window, 1);  %%% bold
%                 end
                
                %%% show the word
                DrawFormattedText(window, wordlist{isent,inum}{w}, 'center','center',0);
                %%%% add empty photodiode square
                if Photodiode == 1  %%% USA -- send flashes to the photodiode
                    Screen('FillRect',window,black,PhotodiodeRect);
                end
                
                %wordonset{isent,inum}{w} = Screen(window,'Flip', prevtime + interword - 0.005);
                wordonset{isent,inum}{w} = Screen(window,'Flip', prevtime + 0.3 - 0.005);
                prevtime = GetSecs;
                
                Screen('TextSize',window, 9);
                DrawFormattedText(window,'','center','center',100); %%% change to plus for fixation point
                %%%% add empty photodiode square
                if Photodiode == 1  %%% USA -- send flashes to the photodiode
                    Screen('FillRect',window,black,PhotodiodeRect);
                end
                
                %wordoffset{isent,inum}{w} = Screen(window,'Flip', prevtime + wordduration - 0.005);
                wordoffset{isent,inum}{w} = Screen(window,'Flip', prevtime + 0.3 - 0.005);
                prevtime = GetSecs;
            end
            
            %%% intersentence fixation point
            Screen('TextSize',window, 9);
            DrawFormattedText(window,'+','center','center',100);
            %%%% add empty photodiode square
            if Photodiode == 1  %%% USA -- send flashes to the photodiode
                Screen('FillRect',window,black,PhotodiodeRect);
            end
            Screen(window,'Flip', prevtime + wordduration - 0.005);  %%% wait for the word duration, then erase the word
            prevtime = GetSecs;
            if (inum==1)                
                DrawFormattedText(window,'+','center','center',100);
                %%%% add empty photodiode square
                if Photodiode == 1  %%% USA -- send flashes to the photodiode
                    Screen('FillRect',window,black,PhotodiodeRect);
                end
                if BlockType==1
                    waittime = 0.7; 
                else
                    waittime = 2.0; %%% stick to the fixation screen for a long delay.
                end
                Screen(window,'Flip', prevtime + waittime - 0.005);  %%% after delay, move on to the next words
                prevtime = GetSecs;
            end
            
        end
        
        %%% response screen
        Screen('TextSize',window, 36);
        DrawFormattedText(window,'?','center','center',0);
        %%%% add empty photodiode square
        if Photodiode == 1  %%% USA -- send flashes to the photodiode
            Screen('FillRect',window,black,PhotodiodeRect);
        end
        choicescreen{isent} = Screen(window,'Flip');
        prevtime = GetSecs;
        
        keyIsDown = 0;
        while ~keyIsDown
            [keyIsDown, secs, keyCode, deltaSecs] = KbCheck;
        end
        response{isent} = KbName(find(keyCode));
        RT{isent} = secs - prevtime;
        
        %%% show word durations
        %worddurations = cell2mat(wordoffset{isent,1})- cell2mat(wordonset{isent,1})
        
        %%%% interrupt the experiment?
        if strcmp(response{isent},escapekey)
            break;
        end
    end
    
    
catch % if PTB crashes it will land here, allowing us to reset the screen to normal.
    a = lasterror; a.message % find out what the error is
end;

Priority(0);
Screen('closeall'); % this line deallocates the space pointed to by the buffers, and returns the screen to normal.
FlushEvents('keyDown'); % removed typed characters from queue.

toc

% example of how you would return screen to "normal resolution"
%!reschange -width=1280 -height=1024 -depth=32

outfile = [ 'ExperimentalRun' sprintf('_%d',fix(clock)) '.mat' ];
save(outfile);  %%% save everything: the wordlist, the sentences, even the rules used to generate the sentences



