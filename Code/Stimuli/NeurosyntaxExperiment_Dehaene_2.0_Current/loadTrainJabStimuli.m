%loadTrainJabStimuli.m   

StimFile='SampleGeneratedSentences_Jab';
load(StimFile,'wordlist','nsentences','samestruct')        % should be in the same folder that has this file  

nPreSpecSents=3;
wordlist{1,1}={'on' 'that' 'rab' 'fifty' 'brell' 'glirts' 'rasked' 'the' 'brillig' 'birk'}; 
wordlist{1,2}={'they' 'rasked' 'it'}; 
samestruct(1)=1;

wordlist{2,1}={'near' 'an' 'uptor' 'a' 'ganter' 'very' 'plagly' 'croils'};
wordlist{2,2}={'they' 'do'};
samestruct(2)=0;
ExtraExp{2}='"they" cannot refer to just one "ganter"';

wordlist{3,1}={'a' 'very' 'dag' 'rab' 'near' 'the' 'gantress' 'will' 'roft'};
wordlist{3,2}={'it' 'rofted'};
samestruct(3)=0;
ExtraExp{3}='"rofted" and "will roft" are different verb tenses';

nPreSpecSentAdj=0;
nMaxExtraTrs=4; 

setExplanation
