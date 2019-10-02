function [sentences_per_block, training_sentences] = load_stimuli(params)
% Returns: 
% --------
% sentences_per_block: cell array of cell arrays (1 x num_blocks). Each cell contains a
% cell array (1, num_trials), which in turn contains a cell array
% (1 x num_words)


% --------------- LOAD STIMULI FOR EACH BLOCK
sentences_per_block = cell(1, params.n_blocks);
for b_id = 1:params.n_blocks % block ID
%     warning off;
    curr_filename = fullfile(params.path2stim, ['Subj_', params.subject, '_block_', num2str(b_id), '.txt']);
    fid = fopen(curr_filename, 'r');
    stimuli = textscan(fid, '%s', 'delimiter','\n', 'headerLines', 1);
    fclose(fid);
    stimuli_sentences = cell(1, length(stimuli{1}));
    for i =1:length(stimuli{1})
       stimuli_sentences{i} = strsplit(stimuli{1}{i}, ','); 
       words_in_cells = strsplit(stimuli_sentences{i}{1});
       for w=1:length(words_in_cells)
           if strfind(words_in_cells{w}, '_')
              words_in_cells{w} = strrep(words_in_cells{w}, '_', ' ');
           end
       end
       stimuli_sentences{i}{1} = words_in_cells;
    end
    sentences_per_block{1, b_id} = stimuli_sentences;
end


% -------------------------
% -------- TRAINING --------
% --------------------------


curr_filename = fullfile(params.path2stim, 'training_block.txt');
fid = fopen(curr_filename, 'r');
stimuli = textscan(fid, '%s', 'delimiter','\n', 'headerLines', 1);
fclose(fid);
training_sentences = cell(1, length(stimuli{1}));
for i =1:length(stimuli{1})
   training_sentences{i} = strsplit(stimuli{1}{i}, ','); 
   words_in_cells = strsplit(training_sentences{i}{1});
   for w=1:length(words_in_cells)
       if strfind(words_in_cells{w}, '_')
          words_in_cells{w} = strrep(words_in_cells{w}, '_', ' ');
       end
   end
   training_sentences{i}{1} = words_in_cells;
end


end




