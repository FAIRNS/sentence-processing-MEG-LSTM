%SendMarkers.m


%%% send a short sequence to unambiguously identify the experiment, just in
%%% case we get confused in the successive files...
mark_on  = round(((random('unid',5)+2)/FrameRate)*1000); %%% random duration in milliseconds
mark_off = round(((random('unid',5)+2)/FrameRate)*1000); %%% random duration in milliseconds
mark_number = random('unid',5)+5;

prevtime=GetSecs;
if Photodiode == 1  %%% send flashes to the photodiode
    for imark = 1:mark_number
        DrawFormattedText(window,'+','center','center',100);
        Screen('FillRect',window,white,PhotodiodeRect);
        prevtime=Screen(window,'Flip',prevtime + mark_on/1000 - 0.005);
        
        DrawFormattedText(window,'+','center','center',100);
        Screen('FillRect',window,black,PhotodiodeRect);
        prevtime=Screen(window,'Flip',prevtime + mark_off/1000 - 0.005);
    end
end

if TTLsending == 1  %%% USA
    for imark = 1:mark_number
        % for 32bit MATLAB on 64-bit windows - LPT3 expresscard output is address 0x2000
        outp(hex2dec('2000'),255);
        WaitSecs(mark_on/1000);
        outp(hex2dec('2000'),0);
        WaitSecs(mark_off/1000);
    end
end
if TTLsending == 2  %%% Paris
    for imark = 1:mark_number
        lptwrite(888,255);
        WaitSecs(mark_on/1000);
        lptwrite(888,0);
        WaitSecs(mark_off/1000);
    end
end