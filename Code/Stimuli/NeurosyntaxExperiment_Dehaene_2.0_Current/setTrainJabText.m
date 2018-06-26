% setTrainLocText  

TrainScreen=struct;
ExSentence='Near some glirts a very slithy birk esates';
ExSentence_sh='It esates';

TrainScreen(1).part{1}=['We are now going to have you read sentences with some silly words in them '...
    'that have no meaning. The sentences are silly but we hope are amusing to read.'];

TrainScreen(2).part{1}=['On each trial, you will see a simple sentence such as '...
    '"' ExSentence '". All you have to do is read this sentence and understand it as best as you can.']; % [without speaking out loud
TrainScreen(2).part_rect{1}=[0,0,xpix-1,ypix/2];  
TrainScreen(2).part{2}=['\n\n\n\n\n\nThen you will see a shortened version of that same sentence, for instance '...
    '"' ExSentence_sh '". Your task is just as before, to decide if the second sentence could have the '...
    'same meaning as the first. '];
TrainScreen(2).part_rect{2}=[0,0,xpix-1,ypix-1];

TrainScreen(3).part{1}=['In this example "' ExSentence_sh '" can mean the same thing as "' ExSentence '", '...
    'so you should press "' SameKey '" to denote that they are the same. However if the second sentence instead were '...
    '"They esate" you would press "' DiffKey '" to denote that they are different, because "they" '...
    'could not refer to "a very slithy birk".'];
TrainScreen(3).part_rect{1}=[0,0,xpix-1,ypix/2];
TrainScreen(3).part{2}=['\n\n\n\n\n\n\nWhen it is different, the second sentence may have differences in plural status '...
    '("They esate" instead of "It esates") or verb tense ("It will esate" instead of '...
    '"It esates").'];             
TrainScreen(3).part_rect{2}=[0,0,xpix-1,ypix-1];

TrainScreen(4).part{1}=['Let''s practice so you can get the feel of it.'];
if TrainMentionYouCanPressEscape
    TrainScreen(4).part{2}=['\n\n\n\n\n\n\n(You can press "' escapekey{1} '" at any response screen to quit practicing and go to the main block.)'];
end