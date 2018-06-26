%function BlockTitleScreen

Screen('TextSize',window, fs_BlockTitle);  %     round(24*fontscaling));
Screen('TextStyle',window, 1);  %%% 0 = normal

DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
Screen(window,'Flip',window);

WaitSecs(0.75);

DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
if MainExpFlag
    tmptext=['Do ' num2str(nsentences) ' trials then take a pause and change blocks']; 
    Screen('TextStyle',window, 0);  %%% 0 = normal
    DrawFormattedText(window,tmptext,'center',ypix*ypos2,black,wrapat,[],[],vSpacing)
    Screen(window,'Flip');
    
    WaitSecs(0.75);
    Screen('TextStyle',window, 1);  %%% 0 = normal
    DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
    Screen('TextStyle',window, 0);  %%% 0 = normal
    DrawFormattedText(window,tmptext,'center',ypix*ypos2,black,wrapat,[],[],vSpacing) 
end

DrawPressEnter
Screen(window,'Flip');

WaitForEnter
