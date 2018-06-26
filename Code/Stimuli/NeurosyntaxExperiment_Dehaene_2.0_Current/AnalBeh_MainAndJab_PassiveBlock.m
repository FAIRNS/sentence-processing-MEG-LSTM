% AnalBeh_MainAndJab_PassiveBlock.m

% More than this can be done, but for now just count the # of responses on PressTrs    
nPressTrPerBlock=4;
RespTrs=~cellfun('isempty',response);
nHit{iMainJab}=sum(RespTrs);


% create pointer variables bt ExpRun files and GenSent files     
if mod(iMainJab,2)>0
    iMain=iMain+1;        
    load( [datdir GSfNames{ GSNumsPerTask{2}(iMain) }] )
    wordlistMain=wordlist;
    AllLen_Main=cellfun('length',wordlistMain);
    iTr_Main=1;
    nMainSent=size(AllLen_Main,1)/2; % this designates the last sentence of the block      
    
    iJab=iJab+1;
    load( [datdir GSfNames{ GSNumsPerTask{3}(iJab) }] )
    wordlistJab=wordlist;
    AllLen_Jab=cellfun('length',wordlistJab);
    iTr_Jab=1;
    nJabSent=size(AllLen_Jab,1)/2; % this designates the last sentence of the block    
else
    % The last sentence of the block happens as the last sentence of each file here   
    nMainSent=nMainSent*2;  
    nJabSent=nJabSent*2;
end
StimFile={GSfNames{ GSNumsPerTask{2}(iMain) },GSfNames{ GSNumsPerTask{3}(iJab) }};

AllLen=cellfun('length',wordonset);
curn=size(AllLen,1);
[StimFilePerSent,SentNumInStimFile]=deal(ones(curn,1));
for iL=1:curn
    if iTr_Main>nMainSent
        MatchMain=false;
    else
        MatchMain=all( AllLen(iL,:)==AllLen_Main(iTr_Main,:) );
    end
    if iTr_Jab>nJabSent   
        MatchJab=false;
    else
        MatchJab=all( AllLen(iL,:)==AllLen_Jab(iTr_Jab,:) );
    end
    
    if RespTrs(iL)
        if any( AllLen(iL,1) > AllLen_Main(iTr_Main,1) )
            MatchJab=true;
            MatchMain=false;
        elseif any( AllLen(iL,1) > AllLen_Jab(iTr_Main,1) )
            MatchJab=false;
            MatchMain=true;
        else
            if iTr_Main>nMainSent
                MatchMain=false;       MatchJab=true;
            elseif iTr_Jab>nJabSent
                MatchJab=false;        MatchMain=true;
                
            elseif all( AllLen(iL+1,:)==AllLen_Main(iTr_Main,:) )
                MatchMain=false;    MatchJab=true;
            elseif all( AllLen(iL+1,:)==AllLen_Jab(iTr_Jab,:) )
                MatchJab=false;     MatchMain=true;
            else
                if iTr_Main==nMainSent
                    MatchMain=false;    MatchJab=true;
                elseif iTr_Jab==nJabSent
                    MatchJab=false;    MatchMain=true;
                    
                elseif all( AllLen(iL+1,:)==AllLen_Main(iTr_Main+1,:) )
                    MatchJab=false;     MatchMain=true;
                else
                    MatchMain=false;    MatchJab=true;
                end
            end
        end
    end
        
    if MatchMain && MatchJab && ~RespTrs(iL)
        if all( AllLen(iL+1,:)==AllLen(iL,:) )
            MatchJab=false;
        else
            % if the lengths don't repeat              
            if iTr_Main==nMainSent
                MatchMain=false;    % then the non-repeat after this must be a Jab sent, so the Jab counter on this trial must have gone up by 1           
            elseif iTr_Jab==nJabSent
                MatchJab=false;     % then the non-repeat after this must be a Main sent, so the Main counter on this trial must have gone up by 1  
            else
                if all( AllLen(iL+1,:)==AllLen_Main(iTr_Main+1,:) )
                    MatchJab=false;
                else
                    MatchMain=false;
                end
            end
        end
    end
    
    if MatchMain
        StimFilePerSent(iL)=1;
        SentNumInStimFile(iL)=iTr_Main;
        iTr_Main=iTr_Main+1;
    elseif MatchJab   
        StimFilePerSent(iL)=2;
        SentNumInStimFile(iL)=iTr_Jab;
        iTr_Jab=iTr_Jab+1;
    else
        error('Trials from neither block matched ExpRun file, something is wrong')
    end
end