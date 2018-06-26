% QuickBehAnal.m

setparameters_NYU % sets SameKey and DiffKey   
BlockShortLabs={'Loc','Main','Jab'};
BlockOutLabs={'Memory','Main Sentence','Jabberwocky'};
nTypes=length(BlockShortLabs);
curblock=zeros( 1,nTypes );

if strcmp(savedir,'?')
    savedir=uigetdir;
end
initdir=pwd;
cd(savedir)

analyzedfiles=dir('ExperimentalRun*');
for ifile=1:length(analyzedfiles)
    if isempty( strfind(analyzedfiles(ifile).name,'Train'))
        load( analyzedfiles(ifile).name )
        load(StimFile)
        response=response';
        
        %get curBlockType
        for curBlockType=1:nTypes
            if ~isempty( strfind(analyzedfiles(ifile).name,BlockShortLabs{curBlockType}) )
                break                                
            end
        end
        curblock( curBlockType )=curblock( curBlockType )+1;
        
        nTr=length(response);
        sameresp=strcmp( response,SameKey );
        diffresp=strcmp( response,DiffKey );
        corr= (sameresp & samestruct) | (diffresp & ~samestruct);
        ncorr=sum(corr);
        disp(['For ' BlockOutLabs{curBlockType} ' block ' num2str(curblock( curBlockType )) ': ' num2str(ncorr) ' correct trials out of ' num2str(nTr) ' (' num2str(myRoundForDisp3(100*ncorr/nTr),0) ' %)'])
    end
end

cd(initdir)