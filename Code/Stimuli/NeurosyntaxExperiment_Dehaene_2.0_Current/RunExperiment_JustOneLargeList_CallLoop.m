%RunExperiment_JustOneLargeList_CallLoop.m

%%%%%%%%%%%%% User Inputs
npresubj=3;
nsent=40;    %per block
nblocks=9;

recordingsite = 3;

% recordingsite = 1; % Stanford
% recordingsite = 2; % Paris
% recordingsite = 3; % MGH Boston
% recordingsite = 4; % New York
% recordingsite = 5; % Amsterdam

%%%%%%%%%%%%% End of User Inputs

setparameters;

enddir=pwd;
NeuroSyntaxSetPaths
cd([rootpath 'Raw_data' filesep 'StimuliForPresentation']);

for ips=1:1%npresubj
    presubjname=['Neurosyntax_' PlaceStr '_PresSubject' num2str(ips)]     
    
    if ~exist([pwd filesep presubjname],'dir')
        mkdir(presubjname)
    end
    
    cd(presubjname)
    
    %defaultlanguage is set per the recrding site in setparameters
    RunExperiment_JustOneLargeList(nsent,defaultlanguage,nblocks,recordingsite,presubjname)
    
    if exist('outfigures','dir')
        rmdir('outfigures')
    end
    
    cd ..
end

cd(enddir)
