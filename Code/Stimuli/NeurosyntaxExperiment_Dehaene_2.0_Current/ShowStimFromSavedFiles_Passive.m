% ShowStimFromSavedFiles_Passive.m

InitOverallExperiment

% save a diff csv file for each block below
% SendMarkers     % send a short sequence to unambiguously identify the experiment, just in case we get confused in the successive files...    


%%%%%% not sure if it ultimately will be needed, but include it for now
% output the maximum number of words in the first position of the output file
maxNWords=13;
for ibl=1:nBlocksToGen
    for curBlockType=1:2
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    curfile=[savedir filesep outfile_Loc{ibl}];
                    
                    load(curfile);
                    %fid = fopen([curfile(1:end-4) '.csv'],'w');

                    % Below pointers show which StimFile to look to for each sentence presented, and which sentence number within the given StimFile each sentence is                              
                    % For Loc blocks each sentence is from the same StimFile in order      
                    StimFilePerSent=ones(nsentences,1);
                    SentNumInStimFile=[1:nsentences]';
                    
                    PressTrs=[];
                    DisplayStimFromWordlist                                        
                end
            case 2
                curfile=[savedir filesep outfile_Jab{ibl}];
                load(curfile);
                wordlistJab=wordlist;
                
                curfile=[savedir filesep outfile_Main{ibl}];
                load(curfile);
                wordlistMain=wordlist;

                % now mix the two wordlists into a final wordlist, and then we're good      
                for ibl2=1:2  
                    inds=randperm(size(wordlistMain,1))';                                                          
                    inds1=inds<=nsentences/2;
                    inds2=inds>nsentences/2;
                    
                    wordlist(inds1,:)=wordlistMain(1+nsentences/2*(ibl2==2) : nsentences/2*ibl2,:);
                    wordlist(inds2,:)=wordlistJab(1+nsentences/2*(ibl2==2) : nsentences/2*ibl2,:);
                    
                    % Below pointers show which StimFile to look to for each sentence presented, and which sentence number within the given StimFile each sentence is                              
                    % For Loc blocks each sentence is from the same StimFile in order
                    [SentNumInStimFile,StimFilePerSent]=deal( ones(nsentences,1) );
                    StimFilePerSent(inds2)=2;
                    SentNumInStimFile(inds1)=1:nsentences/2;
                    SentNumInStimFile(inds2)=1:nsentences/2;
                    
                    % Add in the Press flashes    
                    PressTrs=randperm(size(wordlistMain,1),4);
                    MainInterrupts=rand(1,4)<=MainVsProbeInterruptRatio;
                    
                    for ipt=1:nPressTrs
                        if MainInterrupts(ipt) || length(wordlist{PressTrs(ipt),2})<nPressFlashes
                            inum=1;
                        else
                            inum=2;
                        end
                        
                        st=randi(length(wordlist{PressTrs(ipt),inum})- (nPressFlashes-1));
                        wordlist{PressTrs(ipt),inum}(st:st+nPressFlashes-1)={PressStr};
                    end
                                        
                    DisplayStimFromWordlist
                end
        end               
    end
end


