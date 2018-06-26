
disp('**************************************');
disp('Calculating wordlist and nodelist');
disp('**************************************');
SentLen=zeros(nsentences,2);

PressTrInds=[];
for isent=1:nsentences
    for ii = 1:2
        if ii==2 && language==2
            continue    % probe sentences aren't working in French        
        end
        
        if ii==1
            [ wordlist{isent,ii} nodelist{isent,ii} ] = ListTerminals(surface{isent},1,{},{});
        else
            [ wordlist{isent,ii} nodelist{isent,ii} ] = ListTerminals(shortened{isent},1,{},{});
        end
        if CapFirstWord
            wordlist{isent,ii}{1}(1)=upper( wordlist{isent,ii}{1}(1) );
        end
        
        %disp(wordlist{isent,ii});
        SentLen(isent,ii) = length(wordlist{isent,ii});
    end
    
    if ~LocalizerFlag && ismember(isent,PressTrInds)
        % now add in the PressStrs for these trials
        Possible_st=[2:SentLen(isent,1)-nPressFlashes+1  SentLen(isent,1)+2:SentLen(isent,1)+SentLen(isent,2)-nPressFlashes+1];
        st=Possible_st(randi(length( Possible_st )));
        
        if st>SentLen(isent,1)
            wordlist{isent,2}(st-SentLen(isent,1) : st-SentLen(isent,1)+nPressFlashes-1)={PressStr};
        else
            wordlist{isent,1}(st:st+nPressFlashes-1)={PressStr};
        end
    end
end

nPressFlashes=3;
PressStr='press';

if PlotSentLenHists
    myHist(SentLen(:,1),1)
    title('Main Sentence sentence length Hist')
    myHist(SentLen(:,2),1)
    title('Probe Sentence sentence length Hist')
    
    tmptotnwords=sum(SentLen);
    disp(['totnwords: ' num2str(tmptotnwords)])
end
