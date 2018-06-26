Screen('TextStyle',window, 1);
Screen('TextSize',window, fs_Ques);
DrawFormattedText(window,'?','center','center',0);
%%%% add empty photodiode square
if Photodiode == 1  %%% USA -- send flashes to the photodiode
    Screen('FillRect',window,black,PhotodiodeRect);
end