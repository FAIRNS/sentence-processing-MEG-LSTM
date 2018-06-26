% FindDiffProbeWord.m

%%% draw a word completely at random, but avoiding any existing
%%% word in the first list
good = false;
while ~good
    newword = randi(ntotwords);
    curtw=TermWord.OrigList_Inds( newword );
    
    if ~ismember( TermWord.Root{ curtw },rootlist{isent,1} )
        good=true;
    end
end
wordlist{isent,inum} = { TermWord.List{curtw} };  %%% we reduce the second sentence to one word here
rootlist{isent,inum} = { TermWord.Root{curtw} };