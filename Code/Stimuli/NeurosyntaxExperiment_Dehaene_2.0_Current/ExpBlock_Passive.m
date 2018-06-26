% Run Experimental Block using stimuli loaded into the variable wordlist

Screen('TextSize',window, 24);
if curBlockType==1
    DrawFormattedText(window, 'Memory Block (Press Enter to continue)', 'center','center',black,wrapat,[],[],vSpacing);
else
    DrawFormattedText(window, 'Sentence Block (Passive) (Press Enter to continue)', 'center','center',black,wrapat,[],[],vSpacing);
end
prevtime=Screen(window,'Flip',prevtime+1);
WaitForEnter
if ismember( KbName(keyCode),escapekey )
    return
end

BlockPauseDur=toc;
tic

Screen('TextStyle',window, 1);
KbQueueRelease;

for isent=1:nsentences
    RunTrial_Passive
    %%%% interrupt the experiment?
    if ismember(response{isent},escapekey)
        break;
    end
end

KbQueueRelease;
HaveRunExpBlock=1;