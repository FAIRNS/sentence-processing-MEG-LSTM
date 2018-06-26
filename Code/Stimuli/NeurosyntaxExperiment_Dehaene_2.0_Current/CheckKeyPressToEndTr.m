% CheckKeyPressToEndTr.m

keyIsDown = 0;
[keyIsDown, secs, keyCode, deltaSecs] = KbCheck;

% Adjusting the code here to record the first button press on Faslealarm trials too, but it will only stop the trial if we're on a PressTrial       
 if keyIsDown
    % record all button presses       
    response{isent}{end+1} = KbName(find(keyCode));
    RT{isent}(end+1) = secs - startfix{isent}; %  not accurate,     
    
    if curPressTr
        EndTr=true;
        
        GoodJobScreen
        Screen(window,'Flip',window);
        WaitSecs(GoodJob_Dur)
    end
end

