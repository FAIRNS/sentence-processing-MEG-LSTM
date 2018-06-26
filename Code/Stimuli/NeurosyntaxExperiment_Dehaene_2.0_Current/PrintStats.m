
disp('**************************************');
disp('Statistics of sentence length');
disp('**************************************');
SentLen=zeros(nsentences,2);
for ii = 1:2    
    for isent=1:nsentences
        if ii==1
            [ wordlist{isent,ii} nodelist{isent,ii} ] = ListTerminals(surface{isent},1,{},{});
        else
            [ wordlist{isent,ii} nodelist{isent,ii} ] = ListTerminals(shortened{isent},1,{},{});
        end
        %disp(wordlist{isent,ii});
        SentLen(isent,ii) = length(wordlist{isent,ii});
    end
end

if PlotSentLenHists
    myHist(SentLen(:,1),1)
    title('Main Sentence sentence length Hist')
    myHist(SentLen(:,2),1)
    title('Probe Sentence sentence length Hist')
end
