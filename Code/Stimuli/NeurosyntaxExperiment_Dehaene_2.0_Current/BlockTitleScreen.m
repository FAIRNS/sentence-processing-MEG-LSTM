%function BlockTitleScreen

Screen('TextSize',window, fs_BlockTitle);  %     round(24*fontscaling));
Screen('TextStyle',window, 1);  %%% 0 = normal
DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
prevtime=Screen(window,'Flip');


DispLoading=0;
if DispLoading
    DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
    Screen('TextSize',window, fs_Loading);  %
    Screen('TextStyle',window, 0);  %%% 0 = normal
    DrawFormattedText(window, 'Loading', 'center',ypix*.65,0,wrapat,[],[],vSpacing);
    prevtime=Screen(window,'Flip',prevtime+.5);
end

Screen('TextSize',window, fs_BlockTitle);  %     round(24*fontscaling));
Screen('TextStyle',window, 1);  %%% 0 = normal
DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
if MainExpFlag && BlockTitScreenText2Opt
    if BlockTitScreenText2Opt==2
        tmptext=['Do ' num2str(tmpnsent) ' of these trials then take a pause']; 
        y2pos=.73;
    elseif BlockTitScreenText2Opt==1
        tmptext=['Do a group of these trials then take a pause'];
        y2pos=.73;
    elseif BlockTitScreenText2Opt==3
        setReassureText
        tmptext=ReassureText;
        y2pos=.65;
    end
    
    Screen('TextSize',window, fs_TrainText)
    Screen('TextStyle',window, 0);  %%% 0 = normal
    DrawFormattedText(window,tmptext,'center',ypix*y2pos,black,wrapat,[],[],vSpacing)
    WaitSecs(0.75);
    prevtime = Screen(window,'Flip');
    
    %WaitSecs(0.75);
    Screen('TextSize',window, fs_BlockTitle)
    Screen('TextStyle',window, 1);  %%% 0 = normal
    DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
    Screen('TextSize',window, fs_TrainText)
    Screen('TextStyle',window, 0);  %%% 0 = normal
    DrawFormattedText(window,tmptext,'center',ypix*y2pos,black,wrapat,[],[],vSpacing) 
end


if MainExpFlag==0 || (ibl==1 && BlockTitScreenText2Opt~=3 )  % when this is true, the Reassurance Screen will follow this
    DrawPressEnter
else
    DrawPressEnter4
end


%Screen(window,'Flip');
%WaitForEnter
