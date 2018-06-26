% InitOutputFile.m  

clear response RT wordonset wordoffset choicescreen startfix
mark_on  = round(((random('unid',5)+2)/FrameRate)*1000); %%% random duration in milliseconds
mark_off = round(((random('unid',5)+2)/FrameRate)*1000); %%% random duration in milliseconds
mark_number = random('unid',5)+5;

if ~isTrain
    load(StimFile,'wordlist','nsentences')
    
    % interleave Main and Jab if needed     
    if WorkingMemoryInMainBlock && curBlockType>1
        wordlist1=wordlist;
        load(StimFile2,'wordlist','nsentences')
        wordlist2=wordlist;
        nsentences=nsentences*2;
        MainOrJab=zeros(nsentences,1);
        MainOrJab(nsentences/2+1:end)=1;
        MainOrJab=MainOrJab(randperm(nsentences));
        
        im=0;   ij=0;
        for isent=1:nsentences
            if MainOrJab(isent)==1
                ij=ij+1;                
                wordlist(isent,:)=wordlist2(ij,:);
            else
                im=im+1;                
                wordlist(isent,:)=wordlist1(im,:);
            end
        end
        disp('sd')
    end
end

% saving the time when the block STARTED as its label   *
outfile = [ 'ExperimentalRun_' BlockShortLabs{curBlockType} TrainLabs{isTrain+1} sprintf('_%d',fix(clock)) '.mat' ];

% saving here just the StimFile name, which tells the user where they can go to to get more information about the stimuli     
if isTrain
    save(outfile,'StimFile','SameKey','DiffKey','mark_on','mark_off','mark_number','wordlist','samestruct') % for training blocks, the wordlistmayhave been adjusted from what is in the stimulus file
else
    if WorkingMemoryInMainBlock && curBlockType>1
        save(outfile,'StimFile','SameKey','DiffKey','mark_on','mark_off','mark_number','MainOrJab') % for training blocks, the wordlistmayhave been adjusted from what is in the stimulus file
    else
        save(outfile,'StimFile','SameKey','DiffKey','mark_on','mark_off','mark_number') % for training blocks, the wordlistmayhave been adjusted from what is in the stimulus file
    end
end