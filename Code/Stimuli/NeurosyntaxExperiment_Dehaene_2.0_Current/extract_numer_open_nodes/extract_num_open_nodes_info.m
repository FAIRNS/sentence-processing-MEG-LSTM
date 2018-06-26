clear all; close all; clc

%%
% French
Stimulus_files = {'GeneratedSentences_Main_2018_6_23_9_52_12.mat', 'GeneratedSentences_Main_2018_6_23_9_52_16.mat', 'GeneratedSentences_Main_2018_6_23_9_52_16.mat'};
% English
Stimulus_files = {'GeneratedSentences_Main_2018_6_23_10_8_36.mat', 'GeneratedSentences_Main_2018_6_23_10_8_41.mat', 'GeneratedSentences_Main_2018_6_23_10_8_44.mat'};

%%
f = fopen('num_open_nodes_English.txt', 'w');
for StimulusFile=fullfile('..', 'Stanford_subject9', Stimulus_files)
    load(StimulusFile{1},'Addstr','surface','wordlist','deepstructure')
    for i=1:size(deepstructure,1)
        [NbOpenNodes, WordList, EmptyTermList]= ComputeSyntacticProperties_NotEmpty_rec(surface{i});
        fprintf(f, '%s \n', strjoin(WordList));
        fprintf(f, '%i', NbOpenNodes);
        fprintf(f, '\n');
    end
end     