% GenLocProbes.m

nsame=round(SameToDiffRate*nsentences);
samestruct=zeros(nsentences,1);
samestruct(1:nsame)=1;

CalcBigTermWordList

inum=2; % we're adjusting the second sentence below...   
for isent=1:nsentences
    if samestruct(isent)  %%%% draw a word from the previous list
        nwords=length(wordlist{isent,1});
        newword = random('unid',nwords);
        wordlist{isent,inum} = { wordlist{isent,1}{newword} };
        rootlist{isent,inum} = { rootlist{isent,1}{newword} };
    else
        FindDiffProbeWord
    end
end

    
    