% WaitForEnter.m    

isreturn=0;
while ~isreturn
    [~,keyCode]=KbWait;
    isreturn=ismember(KbName(keyCode),[{'Return','return'} escapekey]);
end