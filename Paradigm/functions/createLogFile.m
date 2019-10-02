function fid=createLogFile(params, is_training)
timestamp = gettimestamp();
subses=['Subj_' num2str(params.subject) '_sess_' num2str(params.session)];

fn = ['logLocalGlobalParadigm_' timestamp '_' subses '.csv'];
if is_training
   fn = ['train_', fn]; 
end
fn = fullfile('Logs', fn);

fid=fopen(fn ,'w');
fprintf(fid,['Event\t'...
            'Block\t'...
            'Trial\t'...
            'StimNum\t'...      %=stimCode. Based on stimulus order in text file.
            'SlideNum\t'...      % Serial number of word in the sentence 
            'WordStr\t'...      % String of word token 
            'Time\t' ...
            'Sentence_type\t' ...
            'Condition\t' ...
            'Viol_on_slide\r\n' ...
            ]);


end

