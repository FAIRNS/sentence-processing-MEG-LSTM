prevtime=Screen(window,'Flip',prevtime+0.75);
WaitForEnter
if ismember( KbName(keyCode),escapekey )    
    return
end

setReassureText

Screen('TextSize',window, fs_TrainText);
Screen('TextStyle',window, 0);  %%% 0 = normal
DrawFormattedText(window,ReassureText,'center','center',black,wrapat,[],[],vSpacing);

prevtime=Screen(window,'Flip',prevtime+0.75);

DrawFormattedText(window,ReassureText,'center','center',black,wrapat,[],[],vSpacing);
DrawPressEnter4
