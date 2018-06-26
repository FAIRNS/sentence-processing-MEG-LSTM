function [outfile,deepstructure,surface] = StimulusGeneration_PureRandom(nsentences,varargin)
%%%% Generation of simple, controlled sentence stimuli
%
% MJN 150202: This version will create purely random, top-down generated
% stimuli wihtout yoking verbs and nouns based on animacy. Howevre, that's
% not what we want to do with the Neurosyntax 2.0 stimuli, and so will use
% a different version


global language

if size(varargin,2)>=1
    language = varargin{1};
else
  language = 1; %'English'
  %language = 2; %'French'
  %language = 3; %'Dutch'
  %language = 4; %'Spanish'
end

if size(varargin,2)>=2
    recordingsite= varargin{2};
else
    error('Need to specify the recording site')
end

outfile = [ 'GeneratedSentences' sprintf('_%d',fix(clock)) '.mat' ];

%%%%%%%%%%%%%%%%%% PARAMETERS FOR SENTENCE LENGTH
setparameters;

nsentences_per_length = ceil(nsentences/((maxlength-minlength)+1)); %% equalize the number of sentences per sentence length
%%% note that this might change the total number of sentences:
nsentences = nsentences_per_length * ((maxlength-minlength)+1);
table_length = zeros(1,maxlength);

%%% load the substitution rules
LoadRules_PureRandom;

%%% generate a lot of sentences
clear sent;

for isent = 1:nsentences
    disp(isent)
    
    leng_ok = 0;
    while leng_ok == 0
        
        %%%% create the deep structure from simplied X-bar theory
        deepstructure{isent} = GenerateSentence(r,minlength,maxlength);
        %DisplayAllNodesWithLabels(deepstructure{isent},1);
        
        %%% from the deep structure, create the final surface structure, arrange the plurals etc
        surface{isent} = DeepToSurface(deepstructure{isent});
        
        DisplaySentenceWithLabels(surface{isent},1,{});
        
        %%% from the surface structure, substitute two items to get a shortened
        %%% version
        shortened{isent} = Substitute(surface{isent});
        
        %%% check length
        leng = CountTrueTerminals(surface{isent},1);
        leng2 = CountTrueTerminals(shortened{isent},1);
        if (leng<=maxlength)&&(leng>=minlength)&&(leng2<=maxshort)
            if table_length(leng) < nsentences_per_length
                leng_ok = 1;
                table_length(leng) = table_length(leng) +1;
            end
        end
        
    end
    
    DisplaySentenceWithLabels(surface{isent},1,{});
%    figure(31);clf;DisplayTree(surface{isent},1);

    disp('********** SHORTENED VERSION **************');
    DisplaySentenceWithLabels(shortened{isent},1,{});
%    figure(32);clf;DisplayTree(shortened{isent},1);
    
%     outdir = 'outfigures';
%     %%%% print the figures
%     outfile=sprintf('%s\\sentence_%3d_long.png',outdir,isent);
%     h=figure(31);
%     print(h,'-dpng',outfile);
%     outfile=sprintf('%s\\sentence_%3d_short.png',outdir,isent);
%     h=figure(32);
%     print(h,'-dpng',outfile);
%         
end

save(outfile,'-mat');  %%% save everything including the rules and vocabulary
 
PrintStats;

outdir = 'outfigures';
if ~exist(outdir)
     mkdir(outdir);
end
 
%PrintTrees;
PrintSentences;
