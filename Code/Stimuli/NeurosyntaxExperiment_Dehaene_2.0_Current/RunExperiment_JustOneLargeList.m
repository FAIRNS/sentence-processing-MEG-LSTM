function RunExperiment_JustOneLargeList(nsentences,lang,nblocks,recordingsite,csvfilename)
%%%%% MJN: This versions creates one entire experiment's worth of stimuli in
%%%%% one csv file for easy use with Presentation at distant labs. This
%%%%% interfaces with NeuroSyntaxScenario.sce in Presentation, as of 140317.
%%%%%
%%%%% The behavior of this per blocks is to make blocks in order of:
%%%%% Sentence Task - Word List Task - Sentence Task - ...
%%%%% Here the Word List Task blocks use the stimuli from the immediately
%%%%% preceding sentence task blocks.
%%%%%
%%%%% NeuroSyntax experiment of sentence reading and ellipsis judgment
%%%%% (c) Stanislas Dehaene
%%%%%
%%%%% USAGE:
%%%%% RunExperiment(nsentences,language)
%%%%%
%%%%% EXAMPLES:
%%%%%     RunExperiment(80,1);
%%%%% for a 10-minute experiment with 80 sentences in English
%%%%%     RunExperiment(80,2);
%%%%% for a 10-minute experiment with 80 sentences in French
%%%%%
%%%%%     RunExperiment(-1,2);
%%%%% for a control experiment yoked to an existing experimental file
%%%%%
%%%%% The first parameter is the number of sentences (rounded to a multiple
%%%%% of 8, in order to equalize the numbers of sentences at different
%%%%% lengths)
%%%%% Using -1 will let you run a "control experiment" that re-uses the
%%%%% same words as an existing recording, but scrambles them
%%%%%
%%%%% The second parameter (optional) is the language (1=English, 2=French, 3=Dutch, 4=Spanish)
%%%%%
%%%%% The program will automatically call the StimulusGeneration routine
%%%%% which will use the appropriate language to generate sentences according to the
%%%%% the current lexicon and rules (this may take a few minutes).
%%%%%
%%%%% Everything will be automatically saved to a dated file.
%%%%%

% Recommended call for NYU or Boston:
%MakePresentationExperimentStimuli(40,1,9)  %~5 minute blocks of 40 sentences each...

%%%%%% ALL PARAMETERS ARE IN THE FOLLOWING FUNCTION -- they can be changed for a specific lab:
setparameters;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CODE BEGINS HERE -- DO NOT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CHANGE!

rand('twister',sum(10*clock)); %%% reset random numbers

global language

if nargin<2 || isempty(lang)
    language = defaultlanguage;
else
    language = lang;
end
if nargin<3 || isempty(nblocks);      nblocks=9;       end


disp(' ');
disp('NEUROSYNTAX EXPERIMENT')
disp(' ');
disp([ 'You may interrupt the experiment by pressing the [' escapekey '] key' ]);
disp(' ');
disp('Stimulus generation may take a while, can be interrupted by CTRL-C');
disp(' ');
disp('Press RETURN to begin');
%pause;

currentdirectory = pwd;  %%% saves the working directory

for iblock=1:nblocks
    disp(['*************** Block ' num2str(iblock) '******************']);
    
    if mod(iblock,3)~=2
        ControlExperiment = false;
        
        %%%%%%%% generate and randomize the stimuli for a full NeuroSyntax
        %%%%%%%% experiment
        outfile = StimulusGeneration(nsentences,language,recordingsite);  %%% generate n sentences in language i (1=English, 2 = French)
        load(outfile);
        clear wordonset startfix
        %%%% prepare the lists of randomized parameters
        
        %% Choose the font: large or small
        fontused = ones(1,nsentences);
        fontused(1:round(nsentences/2)) = 2;
        fontused = Shuffle(fontused);
        
        %% choose if second sentence is the same as the first
        samestruct = ones(1,nsentences);
        samestruct(1:round(nsentences/4)) = 0; %% one fourth of trials have a "different" response ie the ellipsis isn't appropriate to sentence 1
        samestruct = Shuffle(samestruct);
        
        %%% generate a random order for the sentences
        trialorder = Shuffle(1:nsentences);
        
        for isent = 1:nsentences  %%% this is the index of the trial in the experiment
            %%%%% note that the original sentences are shuffle through the variable TrialOrder
            
            %%% prepare the stimuli as a list of words
            
            %% first sentence
            inum = 1;
            sentenceID{isent,inum} = trialorder(isent);
            [ wordlist{isent,inum} nodelist{isent,inum} ] = ListTerminals(surface{sentenceID{isent,inum}},1,{},{});
            for iword =1:length(nodelist{isent,inum})
                sentlist{isent,inum}{iword} = sentenceID{isent,inum};
            end
            
            %% second sentence
            inum = 2;
            if samestruct(isent)
                sentenceID{isent,inum} = sentenceID{isent,1};
            else
                sentenceID{isent,inum}= random('unid',nsentences); %% pick another second sentence at random
                while sentenceID{isent,inum} == sentenceID{isent,1}
                    sentenceID{isent,inum} = random('unid',nsentences);
                end
            end
            [ wordlist{isent,inum} nodelist{isent,inum} ] = ListTerminals(shortened{sentenceID{isent,inum}},1,{},{});
            for iword =1:length(nodelist{isent,inum})
                sentlist{isent,inum}{iword} = sentenceID{isent,inum};
            end
        end
        
    else %%%% generate a yoked control experiment
        %disp('Select one of the existing data sets (''probably the most recent one'')');
        %outfile = uigetfile('ExperimentalRun*.mat');
        %load(outfile);
        
        %no need to reload file, we should already have eveyrthing in the workspace
        
        ControlExperiment = true;
        %%%% begin by listing all the words used in the existing experiment
        totwords = 0;
        for isent=1:nsentences
            nwords = length(wordlist{isent,1});
            for iword=1:nwords
                totwords = totwords +1;
                giantwordlist{totwords}.word = wordlist{isent,1}{iword};
                %%%% keep track of the original sentence and node from which
                %%%% each word was originally drawn
                giantwordlist{totwords}.sentenceID = sentenceID{isent,1};
                giantwordlist{totwords}.nodeID = nodelist{isent,1}(iword);
            end
        end
        
        %%%% shuffle word order
        newwordorder = Shuffle(1:totwords);
        
        itot = 0;
        for isent = 1:nsentences  %% we just change the wordlists
            %%%%% generate a random list replacing the existing one
            inum = 1;
            nwords = length(wordlist{isent,inum});
            for iword=1:nwords
                itot = itot+1;
                newword = newwordorder(itot);
                wordlist{isent,inum}{iword} = giantwordlist{newword}.word;
                nodelist{isent,inum}{iword} = giantwordlist{newword}.nodeID;
                sentlist{isent,inum}{iword} = giantwordlist{newword}.sentenceID;
            end
            
            inum = 2;
            wordlist{isent,2}=cell(1); %%% we reduce the second sentence to one word
            if samestruct(isent)  %%%% draw a word from the previous list
                newword = random('unid',nwords);
                wordlist{isent,inum}{1} = wordlist{isent,1}{newword};
                nodelist{isent,inum}{1} = nodelist{isent,1}{newword};
                sentlist{isent,inum}{1} = sentlist{isent,1}{newword};
            else
                %%% draw a word completely at random, but avoiding any existing
                %%% word in the previous list
                notgood = true;
                while notgood
                    newword = random('unid',totwords);
                    notgood = false;
                    rootword = surface{giantwordlist{newword}.sentenceID}.node{giantwordlist{newword}.nodeID{1}};
                    for iword =1:nwords
                        rootwordi = surface{sentlist{isent,1}{iword}}.node{nodelist{isent,1}{iword}{1}};
                        if strcmp(rootword,rootwordi)
                            notgood = true;
                        end
                    end
                end
                wordlist{isent,inum}{1} = giantwordlist{newword}.word;
                nodelist{isent,inum}{1} = giantwordlist{newword}.nodeID;
                sentlist{isent,inum}{1} = giantwordlist{newword}.sentenceID;
            end
        end
    end
    
    %The control stimuli is often generated too quickly and occurs at the same precise timestamp as the previous experimental run
    %so we need to check and adjust the strig generated by the clock to avoid overwriting the same matfile   
    clstr=sprintf('_%d',fix(clock));
    outfile = [ 'ExperimentalRun' clstr '.mat' ];
    if exist( outfile,'file' )
        clstr = [clstr(1:end-2)   num2str( str2num(clstr(end-1:end))+1 )];  %adds one second onto the clock string
        outfile = [ 'ExperimentalRun' clstr '.mat' ];
    end
    save(outfile);  %%% save everything: the wordlist, the sentences, even the rules used to generate the sentences
    
    if iblock==1
        %%% save to a csv file with the same name
        %outcsv = strrep(outfile,'.mat','.csv');
        %fid = fopen(outcsv,'w');
        fid = fopen([csvfilename '.csv'],'w');
        
        
        % output the maximum number of words in the first position of the output file
        maxNWords=maxlength;
        fprintf(fid,'%2d',maxlength);
        fprintf(fid,'\n');                
    end
    fprintf(fid,['new block,' outfile '\n']);
        
    for isent = 1:nsentences  %% we just change the wordlists
        for inum = 1:2
            nwords = length(wordlist{isent,inum});
            fprintf(fid,'%2d',nwords);
            fprintf(fid,',%s',num2str( fontsizes(fontused(isent)) ));
            for iword = 1:nwords
                fprintf(fid,',%s',wordlist{isent,inum}{iword});
            end
            fprintf(fid,'\n');
        end
    end
end
fclose(fid);

