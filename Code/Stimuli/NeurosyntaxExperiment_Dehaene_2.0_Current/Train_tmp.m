%Train.m

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
            if iip>1
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center',ypix*ypos2,black,wrapat,[],[],vSpacing)
                %DrawFormattedText(window,TrainScreen(itscr).part{iip},'center',yPos(iip),black,wrapat,[],[],vSpacing)
            else
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center','center',black,wrapat,[],[],vSpacing)
            end
        end
        Screen(window,'Flip',window);
        WaitSecs(0.75);
        
        %if ip==np
        for iip=1:ip
            if iip>1
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center',ypix*ypos2,black,wrapat,[],[],vSpacing)
                %DrawFormattedText(window,TrainScreen(itscr).part{iip},'center',yPos(iip),black,wrapat,[],[],vSpacing)
            else
                DrawFormattedText(window,TrainScreen(itscr).part{iip},'center','center',black,wrapat,[],[],vSpacing)
            end
        end
        
        DrawPressEnter        
        Screen(window,'Flip',window);
        
        WaitForEnter
        %end
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
    if ismember(response{isent},escapekey)
        break;
    end
    
    if samestruct(isent)
        if strcmp( response{isent},SameKey )
            correct=1;
        else
            correct=0;
        end
    else
        if strcmp( response{isent},DiffKey )
            correct=1;
        else
            correct=0;
        end
    end
    if correct
        fbcol=[0 1 0];
        fbtext1='Yes, correct!';
    else
        fbcol=[1 0 0];
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
    DrawPressEnter
    Screen(window,'Flip',window);
    
    WaitForEnter
    
    if isent == nPreSpecSents + nMaxExtraTrs
        Screen('TextSize',window, fs_TrainText);
        DrawFormattedText(window,'Let''s move to the real experiment now.','center','center',black);
        
        Screen('TextSize',window, fs_PressEnter);  %     round(24*fontscaling));
        DrawFormattedText(window, 'Press any key to continue', 'center',round(ypix*2/3),0);
        
        Screen(window,'Flip',window);
        KbPressWait
        KeepPracticing=0;
    elseif isent>=nPreSpecSents
        % query thepatient as to whetherthey want to keep training or keep going
        % try making this its own screen for now
        Screen('TextSize',window, fs_TrainText);
        DrawFormattedText(window,'If you think you’ve got the hang of it, press Enter to move on to the real experiment. Or press any other key to continue practicing.','center','center',black,wrapat,[],[],vSpacing);
        
        Screen(window,'Flip',window);
        [~,keyCode]=KbPressWait;
        if ismember(KbName(keyCode),{'Return','return'});
            KeepPracticing=0;
        end
    end
end

curTit=[curTit '\nmain experiment'];