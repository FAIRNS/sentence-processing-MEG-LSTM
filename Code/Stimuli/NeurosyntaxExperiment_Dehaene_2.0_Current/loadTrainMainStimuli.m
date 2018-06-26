%loadTrainMainStimuli.m

StimFile='SampleGeneratedSentences_Main';
load(StimFile,'wordlist','nsentences','samestruct')        % should be in the same folder that has this file

nPreSpecSents=6;
wordlist{1,1}={'by' 'those' 'cars' 'that' 'woman' 'has' 'slowly' 'cried'};
wordlist{1,2}={'she' 'has' 'cried'};
samestruct(1)=1;

wordlist{2,1}={'three' 'very' 'huge' 'strollers' 'thrill' 'that' 'joyful' 'woman'};
wordlist{2,2}={'they' 'thrill' 'him'};
samestruct(2)=0;
ExtraExp{2}='"him" and "woman" have different genders';

wordlist{3,1}={'near' 'some' 'big' 'carts' 'fifty' 'very' 'large' 'strollers' 'have' 'exploded'};
wordlist{3,2}={'fifty' 'very' 'large' 'strollers' 'will' 'explode'};
samestruct(3)=0;
ExtraExp{3}='"will explode" and "have exploded" are different verb tenses';

wordlist{4,1}={'near' 'these' 'men' 'that' 'little' 'boy' 'met' 'an' 'actress'};
wordlist{4,2}={'near' 'these' 'girls' 'that' 'little' 'boy' 'met' 'her'};
samestruct(4)=0;
ExtraExp{4}='"girls" has a different meaning from "men"';

wordlist{5,1}={'the' 'cart' 'by' 'that' 'car' 'nudges' 'this' 'large' 'stroller'};
wordlist{5,2}={'it' 'nudges' 'this' 'tiny' 'stroller'};
samestruct(5)=0;
ExtraExp{5}='"tiny" has a different meaning from "large"';

wordlist{6,1}={'some' 'very' 'happy' 'girls' 'quickly' 'greeted' 'the' 'waiter'};
wordlist{6,2}={'they' 'greeted' 'him'};
samestruct(6)=1;


nPreSpecSentAdj=2;
nMaxExtraTrs=4;

setExplanation

