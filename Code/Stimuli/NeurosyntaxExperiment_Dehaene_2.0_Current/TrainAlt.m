% TrainAlt
Screen(window,'Flip',prevtime+0.75);
WaitForEnter
if ismember( KbName(keyCode),escapekey )
    return
end

switch curBlockType
    case 1
        if WorkingMemoryInMainBlock
            text1='You''re now going to read word lists and short sentences, then a probe word. Decide whether or not the probe word was in the list or sentence.';
            text2=['Remember, press "' SameKey '" if the probe word was in the first list or sentence, '...
                'and "' DiffKey '" if it was not.'];
        else
            text1='You''re now going to read word lists and short sentences again, and respond as before, deciding whether or not the probe word was in the list or sentence.';
            text2=['Remember, press "' SameKey '" if the probe word was in the first list or sentence, '...
                'and "' DiffKey '" if it was not.'];
        end
    case 2
        if WorkingMemoryInMainBlock
            text1=['You''re now going to read word lists and longer sentences, some which will have silly, nonsense words in them. '...
            'Decide whether or not the probe word was in the list or sentence.'];
            text2=['Remember, press "' SameKey '" if the probe word was in the first list or sentence, '...
                'and "' DiffKey '" if it was not.'];
        else
            text1='You''re now going to read regular sentences again, and respond as before.';
            text2=['Remember, press "' SameKey '" if the meaning of the second sentence is the '...
                'same as the first, and "' DiffKey '" if it is different.\nWhen it is different, the second sentence may have differences in gender ("he" '...
                'instead of "she"), plural status ("they" instead of "he") verb tense ("polished" instead of '...
                '"will polish"), or a particular meaningful word will be changed.'];
        end
    case 3
        text1='You''re now going to read sentences with silly nonsense words in them again, and respond as before.';
        text2=['Remember, press "' SameKey '" if the meaning of the second sentence is the '...
            'same as the first, and "' DiffKey '" if it is different.\nWhen it is different, the second sentence may have differences in plural status '...
            '("They esate" instead of "It esates") or verb tense ("It will esate" instead of '...
            '"It esates").'];
end


Screen('TextSize',window, fs_TrainText);  %     round(24*fontscaling));
Screen('TextStyle',window, 1);  %%% 0 = normal

DrawFormattedText(window, text1, 'center','center',0,wrapat,[],[],vSpacing);
prevtime=Screen(window,'Flip');

%WaitSecs(0.75);

DrawFormattedText(window, text1, 'center','center',0,wrapat,[],[],vSpacing);
if MainExpFlag && DispNumTrialsToSubj
    if DispNumTrialsToSubj==2
        tmptext=['Do ' num2str(tmpnsent) ' trials then take a pause'];
    elseif  DispNumTrialsToSubj==1
        tmptext=['Do a block of trials then take a pause'];
    end
    Screen('TextStyle',window, 0);  %%% 0 = normal
    DrawFormattedText(window,tmptext,'center',ypix*.73,black,wrapat,[],[],vSpacing)
    Screen('TextStyle',window, 1);  %%% 0 = normal
end
DrawPressEnter
prevtime=Screen(window,'Flip',prevtime+0.75);

Screen('TextSize',window, fs_TrainText);  %     round(24*fontscaling));
Screen('TextStyle',window, 1);  %%% 0 = normal
DrawFormattedText(window, text2, 'center','center',0,wrapat,[],[],vSpacing);
WaitForEnter

prevtime=Screen(window,'Flip');

DrawFormattedText(window, text2, 'center','center',0,wrapat,[],[],vSpacing);
DrawPressEnter4   

%prevtime = Screen(window,'Flip');

%WaitSecs(0.75);
% Screen('TextStyle',window, 1);  %%% 0 = normal
% DrawFormattedText(window, curTit, 'center','center',0,wrapat,[],[],vSpacing);
% Screen('TextStyle',window, 0);  %%% 0 = normal
% DrawFormattedText(window,tmptext,'center',ypix*.73,black,wrapat,[],[],vSpacing)
%
% DrawPressEnter

%Screen(window,'Flip');
%WaitForEnter
