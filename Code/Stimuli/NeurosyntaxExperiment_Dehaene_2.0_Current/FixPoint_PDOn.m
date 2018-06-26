% FixPoint_PDOn.m  

Screen('TextSize',window, 9);
DrawFormattedText(window,'+','center','center',100);
if Photodiode == 1  %%% USA -- send flashes to the photodiode
    Screen('FillRect',window,white,PhotodiodeRect);
end
prevtime = Screen(window,'Flip');