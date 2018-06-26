% FixPoint_PDOff.m  

Screen('TextSize',window, 9);
DrawFormattedText(window,'+','center','center',100);
if Photodiode == 1  %%% USA -- send flashes to the photodiode
    Screen('FillRect',window,black,PhotodiodeRect);
end
Screen('DrawingFinished', window);
prevtime = Screen(window,'Flip',fliptime);