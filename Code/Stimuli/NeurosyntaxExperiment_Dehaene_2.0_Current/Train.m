%Train.m

Screen(window,'Flip',prevtime+0.75);
WaitForEnter
if ismember( KbName(keyCode),escapekey )    
    EndExpNow=1;
    return
end

BlockPauseDur=toc;      
tic

% First go through text explanation screens
for itscr=1:length(TrainScreen)
    np=length(TrainScreen(itscr).part);
    %yPos= round( (1:np)/(np+1) .* ypix);
    %yPos=yPos-yPos(1)/2;
    
    for ip=1:np
        Screen('TextSize',window, fs_TrainText);  %     round(24*fontscaling));
        Screen('TextStyle',window, 1);  %%% 0 = normal
        
        % re-draw previous parts and draw current part
        for iip=1:ip
            if itscr==4 && iip==2
                Screen('TextStyle',window, 0);  %%% 0 = normal
                Screen('TextSize',window, fs_PressEnter);
            end
            if isfield(TrainScreen(itscr),'part_rect') && ~isempty(TrainScreen(itscr).part_rect) && ~isempty(TrainScreen(itscr).part_rect{iip})
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center','center',black,wrapat,[],[],vSpacing,[],TrainScreen(itscr).part_rect{iip});
            else
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center','center',black,wrapat,[],[],vSpacing);
            end
        end
        Screen(window,'Flip',window);
        WaitSecs(0.75);
        
        Screen('TextSize',window, fs_TrainText);  %     round(24*fontscaling));
        Screen('TextStyle',window, 1);  %%% 0 = normal
        
        for iip=1:ip
            if itscr==4 && iip==2
                Screen('TextStyle',window, 0);  %%% 0 = normal
                Screen('TextSize',window, fs_PressEnter);
            end
            if isfield(TrainScreen(itscr),'part_rect') && ~isempty(TrainScreen(itscr).part_rect) && ~isempty(TrainScreen(itscr).part_rect{iip})
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center','center',black,wrapat,[],[],vSpacing,[],TrainScreen(itscr).part_rect{iip});
            else
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center','center',black,wrapat,[],[],vSpacing);
            end
        end
        
        if ~(itscr==4 && np==2 && iip==1 )
            DrawPressEnter
            Screen(window,'Flip',window);
            
            WaitForEnter
            if ismember(KbName(keyCode),escapekey)
                return;
            end
        end
        
    end
end


% Train using stimuli loaded into the variable wordlist   
% go through preplanned training trials
KeepPracticing=1;
isent=0;
while KeepPracticing
    Screen('TextStyle',window, 1);
    isent=isent+1;
    
    RunTrial
    %%%% interrupt the experiment?
    if ismember(KbName(keyCode),escapekey)
        break;
    end
    
    if samestruct(isent)
        if strcmp( KbName(keyCode),SameKey )
            correct=1;
        else
            correct=0;
        end
    else
        if strcmp( KbName(keyCode),DiffKey )
            correct=1;
        else
            correct=0;
        end
    end
    if correct
        fbcol=green;
        fbtext1='Yes, correct!';
    else
        fbcol=red;
        fbtext1='No, incorrect';
    end
    
    %%% DisplayFeedback
    DrawQues
    DrawFB1
    Screen(window,'Flip',window);
    
    %KbPressWait
    WaitSecs(0.75)
    
    DrawQues
    DrawFB1
    DrawFB2
    Screen(window,'Flip',window);
        
    %KbPressWait
    WaitSecs(0.75)
    
    DrawQues
    DrawFB1
    DrawFB2
    
    
    if isent <= nPreSpecSents-nPreSpecSentAdj
        if isent==3 && curBlockType==2
            DrawPressEnter3
        else
            DrawPressEnter
        end
        Screen(window,'Flip',window);
        
        WaitForEnter
        if ismember(KbName(keyCode),escapekey)
            return;
        end
    else
        Screen('TextSize',window, fs_TrainText);
        DrawFormattedText(window,'Press Enter to move on to the real experiment. Press any other key to continue practicing.','center',ypix*.85,black,wrapat,[],[],vSpacing);
    end    
    
    if isent == nPreSpecSents + nMaxExtraTrs
        Screen('TextStyle',window, 0);
        Screen('TextSize',window, fs_PressEnter);  %     round(24*fontscaling));
        DrawFormattedText(window,'(press any key to continue)','center',ypix*.9,black);
        Screen(window,'Flip',window);
        KbPressWait;
        
        Screen('TextSize',window, fs_TrainText);
        DrawFormattedText(window,'Let''s move to the real experiment now.','center','center',black);
        
        Screen('TextSize',window, fs_PressEnter);  %     round(24*fontscaling));
        DrawFormattedText(window, 'Press any key to continue', 'center',round(ypix*2/3),0);
        
        Screen(window,'Flip',window);
        KbPressWait;
        KeepPracticing=0;
    elseif isent>=nPreSpecSents-nPreSpecSentAdj
        % query thepatient as to whetherthey want to keep training or keep going
        % try making this its own screen for now
        if isent==nPreSpecSents-nPreSpecSentAdj
            Screen('TextSize',window, fs_TrainText);
            DrawFormattedText(window,'If you think you''ve got the hang of it, press Enter to move on to the real experiment. Or press any other key to continue practicing.','center','center',black,wrapat,[],[],vSpacing);
        end
            
        Screen(window,'Flip',window);
        [~,keyCode]=KbPressWait;
        if ismember(KbName(keyCode),[{'Return','return'} escapekey]);
            KeepPracticing=0;
        end
    end
end