%loadTrainLocStimuli.m   

StimFile='SampleGeneratedSentences_Loc';
load(StimFile,'wordlist','nsentences','samestruct')       % should be in the same folder that has this file  

nPreSpecSents=4;
wordlist{1,1}={'quickly' 'stroller' 'cart' 'very' 'cars' 'this'}; 
wordlist{1,2}={'cars'}; 
samestruct(1)=1;

wordlist{2,1}={'those' 'the' 'appears' 'small' 'quickly'};
wordlist{2,2}={'very'};
samestruct(2)=0;

wordlist{3,1}={'these' 'cars' 'by' 'this' 'stroller' 'exploded'};
wordlist{3,2}={'stroller'};
samestruct(3)=1;

wordlist{4,1}={'the' 'cars' 'push' 'some' 'huge' 'carts'}; 
wordlist{4,2}={'a'};
samestruct(4)=0;

nPreSpecSentAdj=1;
nMaxExtraTrs=5; 


%for generation ofPresentation stimuli   
for isent=1:nPreSpecSents+nMaxExtraTrs
    fbtext2{isent}=['\"' wordlist{isent,2}{1} '\"\n was '];
    if ~samestruct(isent)
        fbtext2{isent}=[fbtext2{isent} 'not '];
    end
    fbtext2{isent}=[fbtext2{isent} 'in the list of'];
    
    fbtext2{isent}=[fbtext2{isent} '\n\"'];
    for iw=1:length(wordlist{isent,1})
        fbtext2{isent}=[fbtext2{isent} wordlist{isent,1}{iw} ' '];
    end
    fbtext2{isent}=[fbtext2{isent}(1:end-1) '\"'];
end

% for Matlab psychophysics toolbox
% for isent=1:nPreSpecSents+nMaxExtraTrs
%     fbtext2{isent}=['''' wordlist{isent,2}{1} ''' was '];
%     if ~samestruct(isent)
%         fbtext2{isent}=[fbtext2{isent} 'not '];
%     end
%     fbtext2{isent}=[fbtext2{isent} 'in the list of'];
%     
%     fbtext2{isent}=[fbtext2{isent} '\n'''];
%     for iw=1:length(wordlist{isent,1})
%         fbtext2{isent}=[fbtext2{isent} wordlist{isent,1}{iw} ' '];
%     end
%     fbtext2{isent}=[fbtext2{isent}(1:end-1) ''''];
% end
