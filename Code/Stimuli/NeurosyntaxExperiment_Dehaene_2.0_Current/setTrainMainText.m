% setTrainLocText  

TrainScreen=struct;
ExSentence='Sixty waitresses will polish the little car';
ExSentence_sh='They will polish it';

TrainScreen(1).part{1}=['We are going to have you read sentences, slightly longer than before. ' ...
    'These sentences are a bit stupid, but amusing.'];

TrainScreen(2).part{1}=['On each trial, you will see a simple sentence such as '...
    '"' ExSentence '". All you have to do is read and understand '...
    'this sentence in your mind (without speaking out loud).'];
TrainScreen(2).part_rect{1}=[0,0,xpix-1,ypix/2];   
%TrainScreen(2).part_rect{1}=[0,ypix/2,xpix-1,ypix-1];
TrainScreen(2).part{2}=['\n\n\n\n\n\nThen you will see a shortened version of that same sentence, for instance '...
    '"' ExSentence_sh '". You just have to decide if the second sentence could have the same meaning '...
    'as the first.'];
TrainScreen(2).part_rect{2}=[0,0,xpix-1,ypix-1];
%TrainScreen(2).part_rect{2}=[0,0+200,xpix-1,ypix/2+200];
%TrainScreen(2).part_rect{2}=[0,ypix/2,xpix-1,ypix-1];

TrainScreen(3).part{1}=['In this example "' ExSentence_sh '" can mean the same thing as "' ExSentence '", '...
    'so you should press "' SameKey '" to denote that they are the same. However if the second sentence instead were '...
    '"She will polish it" you would press "' DiffKey '" to denote that they are different, because "she" '...
    'could not refer to "sixty waitresses".']; 
TrainScreen(3).part_rect{1}=[0,0,xpix-1,ypix/2]; 
%TrainScreen(3).part_rect{1}=[0,ypix/2,xpix-1,ypix-2]; 
TrainScreen(3).part{2}=['\n\n\n\n\n\n\nWhen it is different, the second sentence may have differences in gender ("he" '...
    'instead of "she"), plural status ("they" instead of "he") verb tense ("polished" instead of '...
    '"will polish"), or a particular meaningful word will be changed.']; 
TrainScreen(3).part_rect{2}=[0,0,xpix-1,ypix-1];
%TrainScreen(3).part_rect{2}=[0,ypix/2,xpix-1,ypix-1];        

TrainScreen(4).part{1}=['Let''s practice so you can get the feel of it.'];
if TrainMentionYouCanPressEscape
    TrainScreen(4).part{2}=['\n\n\n\n\n\n\n(You can press "' escapekey{1} '" at any response screen to quit practicing and go to the main block.)'];
end