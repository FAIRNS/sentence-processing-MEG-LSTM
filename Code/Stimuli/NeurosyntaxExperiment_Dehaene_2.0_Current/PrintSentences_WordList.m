% PrintSentences_WordList.m

for isent = 1:nsentences
    for inum=1:2
        tmpstr = '';
        for iw=1:length(wordlist{isent,inum})
            tmpstr=[tmpstr wordlist{isent,inum}{iw} ' '];
        end
        disp(tmpstr)
    end
    disp('************************************');
end





    