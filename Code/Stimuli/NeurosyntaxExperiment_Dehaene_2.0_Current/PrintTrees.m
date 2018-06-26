%PrintTrees.m

%%%%%%%%%%%%% User Inputs
%subjectname='Stanford_subject1';
SubjList={'Boston_subject66'};   
%SubjList={'Boston_subject59','Boston_subject62','Boston_subject63','Boston_subject66','ICM_subject1896','ICM_subject1907','ICM_subject1950','ICM_subject1998','ICM_subject2006','ICM_subject2012','ICM_subject2033','ICM_subject2040','ICM_subject2065'};

%%%%%%%%%%%%% End of User Inputs

NeuroSyntaxSetPaths

for isubj=1:length(SubjList)
    subjectname=SubjList{isubj};
    

cd([rootpath subjectname]);

analyzedfiles = dir('ExperimentalRun*.mat');


%%% scan all the data, searching for the request trials and conditions
for ifiles = 1:length(analyzedfiles)
    if isempty( strfind(analyzedfiles(ifiles).name,'NoMatData') )
        load(analyzedfiles(ifiles).name);
        outdir = ['outfigures' filesep 'Block' num2str(ifiles)];
        
        if ~exist(outdir,'dir');    mkdir(outdir);      end
        
        for isent = 1:nsentences
            %%%% create the deep structure from simplied X-bar theory
            % deepstructure{isent} = GenerateSentence(r);
            % DisplayAllNodesWithLabels(deepstructure{isent},1);
            
            %%% from the deep structure, create the final surface structure, arrange the plurals etc
            % surface{isent} = DeepToSurface(deepstructure{isent});
            
            % diplay long sentences
            inum=1;
            DisplaySentenceWithLabels(surface{ sentlist{isent,inum}{1} },1,{});
            sfigure(31);clf;DisplayTree( surface{ sentlist{isent,inum}{1} },1 );
            
            
            %display shortened versions
            inum=2;
            
            %%% from the surface structure, substitute two items to get a shortened
            %%% version
            % shortened{isent} = Substitute(surface{isent});
            disp('********** SHORTENED VERSION **************');
            DisplaySentenceWithLabels(shortened{ sentlist{isent,inum}{1} },1,{});
            sfigure(32);clf;DisplayTree(shortened{ sentlist{isent,inum}{1} },1);
            
            %%%% print the figures
            outfilefig=sprintf('%s\\sentence_%3d_long.png',outdir,isent);
            h=sfigure(31);
            print(h,'-dpng',outfilefig);
            outfilefig=sprintf('%s\\sentence_%3d_short.png',outdir,isent);
            h=sfigure(32);
            print(h,'-dpng',outfilefig);
            
        end
    end
end


end
