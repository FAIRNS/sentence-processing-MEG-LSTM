%for Matlab PTB
% for isent=1:nPreSpecSents+nMaxExtraTrs
%     fbtext2{isent}='"';
%     for iw=1:length(wordlist{isent,2})
%         fbtext2{isent}=[fbtext2{isent} wordlist{isent,2}{iw} ' '];
%     end
%     fbtext2{isent}(end)='"';
%     
%     if samestruct(isent)
%         fbtext2{isent}=[fbtext2{isent} ' has '];
%     else
%         fbtext2{isent}=[fbtext2{isent} ' does not have '];
%     end
%     fbtext2{isent}=[fbtext2{isent} ' the same meaning as "'];
%     
%     for iw=1:length(wordlist{isent,1})
%         fbtext2{isent}=[fbtext2{isent} wordlist{isent,1}{iw} ' '];
%     end
%     fbtext2{isent}(end)='"';
%     
%     if isent<=nPreSpecSents && ~samestruct(isent)
%         fbtext2{isent}=[fbtext2{isent} ' because ' ExtraExp{isent}];
%     end
% end

%for Presentation
for isent=1:nPreSpecSents+nMaxExtraTrs
    fbtext2{isent}='"';
    for iw=1:length(wordlist{isent,2})
        fbtext2{isent}=[fbtext2{isent} wordlist{isent,2}{iw} ' '];
    end
    fbtext2{isent}(end:end+1)='",';
    
    if samestruct(isent)
        fbtext2{isent}=[fbtext2{isent} ' has '];
    else
        fbtext2{isent}=[fbtext2{isent} ' does not have '];
    end
    fbtext2{isent}=[fbtext2{isent} ' the same meaning as,"'];
    
    for iw=1:length(wordlist{isent,1})
        fbtext2{isent}=[fbtext2{isent} wordlist{isent,1}{iw} ' '];
    end
    fbtext2{isent}(end)='"';
    
    if isent<=nPreSpecSents && ~samestruct(isent)
        fbtext2{isent}=[fbtext2{isent} ', because ' ExtraExp{isent}];
    else
        fbtext2{isent}=[fbtext2{isent} ', '];
    end
end