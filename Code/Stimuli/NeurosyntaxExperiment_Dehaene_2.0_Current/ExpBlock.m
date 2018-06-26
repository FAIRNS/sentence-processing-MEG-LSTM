% Run Experimental Block using stimuli loaded into the variable wordlist   

Screen(window,'Flip',prevtime+0.75);
WaitForEnter
if ismember( KbName(keyCode),escapekey )    
    return
end

BlockPauseDur=toc;      
tic

Screen('TextStyle',window, 1);
for isent=1:nsentences
    RunTrial
    %%%% interrupt the experiment?
    if ismember(response{isent},escapekey)
        break;
    end
end

HaveRunExpBlock=1;