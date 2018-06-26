% AnalBeh2p0_Passive.m

%%%%%%%%%%%%% User Inputs
subjectname='TA724';    
%%%%%%%%%%%%% End of User Inputs

% datdir should indicate the folder where teh data for the current subject is stored     
NeuroSyntaxSetPaths
Twop0str=['2p0' filesep];
datdir=[rootpath Twop0str subjectname filesep subjectname '_NeuroSyntax2_Behavioral_Data' filesep];

SameKey_Texas='LeftArrow';
DiffKey_Texas='RightArrow';

% get all exp runs and Gen Sentences filenames      
ExpRunFiles= dir([datdir 'ExperimentalRun*.mat']);   
GenSentFiles= dir([datdir 'GeneratedSentences*.mat']);

nEfiles=length(ExpRunFiles);
nGSfiles=length(GenSentFiles);
if nEfiles==0;  disp(['No ExpRun files found!!!']);     end

% make sure filenames are in proper chronological order       
EfNames=cell(nEfiles,1);
for iE=1:nEfiles;
    EfNames{iE}=ExpRunFiles(iE).name;
end
EfNames=OrderFileNames(EfNames);

GSfNames=cell(nGSfiles,1);
for iGS=1:nGSfiles;
    GSfNames{iGS}=GenSentFiles(iGS).name;
end
GSfNames=OrderFileNames(GSfNames);


TaskStrs={'Loc','Main','Jab'};
nT=length(TaskStrs);
GSNumsPerTask=cell(1,3);
for iGSfiles=1:nGSfiles
    for iT=1:nT
        if ~isempty(strfind(GSfNames{iGSfiles},TaskStrs{iT}))
            GSNumsPerTask{iT}(end+1)=iGSfiles;
        end
    end
end


[iLoc,iMainJab,iMain,iJab]=deal(0);
BlockStrs={'Loc','MainAndJab'};
% Here we cycle through the ExpRunFiles in the order they were performed       
for iEfiles=1:nEfiles
    clear response
    load( [datdir EfNames{iEfiles}] );
    if ~exist('response','var')
        continue
    end
    
    % need to write over these values   
    SameKey=SameKey_Texas;      DiffKey=DiffKey_Texas;
    
    % get curBlockType
    AllLens=cellfun('length',wordonset);
    if all(AllLens(:,2)<=1);    curBlockType=1;     else    curBlockType=2;     end
    
    switch curBlockType
        case 1
            iLoc=iLoc+1;
            load( [datdir GSfNames{ GSNumsPerTask{1}(iLoc) }] )
            
            % assign StimFile and related variables to save in Loc Block ExpRun              
            StimFile= {GSfNames{ GSNumsPerTask{1}(iLoc) }};
            StimFilePerSent=ones(nsentences,1);
            SentNumInStimFile=[1:nsentences]';                     
            
            AnalBeh_LocBlock
        case 2       
            iMainJab=iMainJab+1;
            AnalBeh_MainAndJab_PassiveBlock
    end
    
    % save StimFile and pointer variables to the ExpRun file    
    BlockType=BlockStrs{curBlockType};
    disp(['Appending ' EfNames{iEfiles}])
    save( [datdir EfNames{iEfiles}],'BlockType','StimFile','StimFilePerSent','SentNumInStimFile','-append')
end

for curBlockType=1:2
    switch curBlockType
        case 1
            disp([num2str(iLoc) ' Loc blocks'])   
            nTrStr='nTr:';
            PctCorrStr='Pct Correct:';
            meanRTsStr='mean RTs (s):';
            TotnTr=0;
            TotCorr=0;
            for iiLoc=1:iLoc
                curnTr=length(RTs{iiLoc});
                TotnTr=TotnTr+curnTr;
                nTrStr=[nTrStr ' ' num2str(curnTr)];
                TotCorr=TotCorr+ nCorrSame{iiLoc} + nCorrDiff{iiLoc};
                
                meanRTsStr=[meanRTsStr ' ' sprintf('%0.2f',TotRT{iiLoc})];
                
                PctCorrStr=[PctCorrStr ' ' sprintf('%0.2f',PctTotCor{iiLoc})];
            end

            disp(nTrStr);
            disp(PctCorrStr);
            disp(meanRTsStr);
            disp([num2str(TotnTr) ' total trials; ' sprintf('%0.2f',(TotCorr/TotnTr*100)) ' Pct Correct'])
            
        case 2
            disp(' ')
            disp([num2str(iMainJab) ' Main/Jab blocks']) 
            TotnHit=0;
            nHitStr='nHits:';
            for iiMainJab=1:iMainJab
                TotnHit=TotnHit+nHit{iiMainJab};
                nHitStr=[nHitStr ' ' num2str( nHit{iiMainJab} )];
            end
            
            disp([nHitStr ' out of ' num2str(nPressTrPerBlock) ' Press Trials per block'])
            disp([sprintf('%0.2f',(TotnHit/(iMainJab*nPressTrPerBlock))*100) ' Pct Hit Rate on Press Trs'])
    end
end    
       
