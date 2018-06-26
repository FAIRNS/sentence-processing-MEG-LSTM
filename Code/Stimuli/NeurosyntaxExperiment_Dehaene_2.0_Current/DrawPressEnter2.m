%DrawPressEnter2.m

Screen('TextStyle',window, 0);
Screen('TextSize',window, fs_PressEnter);  %     round(24*fontscaling));
DrawFormattedText(window,'Take as long as you need, then press enter when you''re ready to continue to the next block','center',ypix*.9,black)