% RunTrial.m
%
% uses whatever is in wordlist{isent,1:2} to display the currrent trial

if Photodiode
    Screen('FillRect',window,black,PhotodiodeRect);
end
%       DrawFormattedText(window,'Ready?','center','center',0);
Screen(window,'Flip');
WaitSecs(inttrial);


%%% fixation point, with flash for photodiode if needed
%%%% fliptime=[]; % debug that this works w empty flip time!!!!!   
FixPoint_PDOn
startfix{isent} = prevtime;

%%% TRIGGERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% send a trigger at the onset of the fixation preceding the first sentence of each pair
if Photodiode   %%% after 50 ms, return to black screen with fixation
    Screen('TextSize',window, 9);
    DrawFormattedText(window,'+','center','center',100);
    Screen('FillRect',window,black,PhotodiodeRect);
    Screen(window,'Flip',prevtime + (WaitFrames_PD - 0.5) * ifi); %%% 50 millisecond flash
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


prevtime=WaitSecs( fixwait- interword );
%fliptime=prevtime+fixwait- interword;   
%FixPoint_PDOff;

for inum = 1:2
    nwords = length(wordlist{isent,inum});   
    
    Screen('TextSize',window, fs_Stim);
    for w=1:nwords
        %%% show the word
        DrawFormattedText(window, wordlist{isent,inum}{w}, 'center','center',black);
        %%%% add photodiode square to track each word onset
        if Photodiode == 1  %%% USA -- send flashes to the photodiode during each word    
            Screen('FillRect',window,white,PhotodiodeRect);
        end
        Screen('DrawingFinished', window);
        
        wordonset{isent,inum}{w} = Screen(window,'Flip', prevtime + (WaitFrames_IW-0.50) * ifi);        
        prevtime = wordonset{isent,inum}{w};        
        
        DrawFormattedText(window,'','center','center',100); 
        %%%% add empty photodiode square
        if Photodiode == 1  %%% USA -- send flashes to the photodiode
            Screen('FillRect',window,black,PhotodiodeRect);
        end
        Screen('DrawingFinished', window);
        
        wordoffset{isent,inum}{w} = Screen(window,'Flip', prevtime + (WaitFrames_WordDur-0.50) * ifi);        
        prevtime = wordoffset{isent,inum}{w};  
    end
    

    %%% intersentence fixation point
    fliptime=prevtime+ (WaitFrames_IW-0.50) * ifi;
    FixPoint_PDOff
    
    if inum==1
        prevtime=WaitSecs( DelayDurs(curBlockType) );
    end
end

%%% response screen
DrawQues
choicescreen{isent} = Screen(window,'Flip');
prevtime = choicescreen{isent};
    
%%%% [~,keyCode]=KbWait; %%% according to at least one website, the below code should have slightly better timing    
keyIsDown = 0;
while ~keyIsDown
    [keyIsDown, secs, keyCode, deltaSecs] = KbCheck;
end
response{isent} = KbName(find(keyCode));
RT{isent} = secs - prevtime;

    
%%% Saving every trial!!!....    
save(outfile,'response','RT','wordonset','wordoffset','choicescreen','startfix','-append')
