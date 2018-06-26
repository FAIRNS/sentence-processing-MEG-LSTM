% IntersperseLocTrials.m   

if LocalizerFlag
nsentences=nsentences*2;

wordlist=[oldwordlist; wordlist];
rootlist=[oldrootlist; rootlist];
nodelist=[oldnodelist; nodelist];
samestruct=[oldsamestruct; samestruct];

SentInfo(nsentences).nToAdd=[];     % this creates empty structrues (with all the fields) for the word list trials     
end


trialorder=randperm(nsentences);
for ic=1:2
    wordlist(:,ic)=wordlist( trialorder,ic );
    rootlist(:,ic)=rootlist( trialorder,ic );
    nodelist(:,ic)=nodelist( trialorder,ic );    
end
samestruct=samestruct(trialorder);

SentInfo=SentInfo(trialorder);
deepstructure=deepstructure(trialorder);
surface=surface(trialorder);
shortened=shortened(trialorder);
